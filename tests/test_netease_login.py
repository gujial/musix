"""
测试网易云音乐登录认证功能
"""
import asyncio
import getpass
import sys
from pathlib import Path

# 添加父目录到系统路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.netease_service import NeteaseService


# 创建全局服务实例
service = NeteaseService(auto_login=True)


async def test_login_status():
    """测试登录状态"""
    print("\n检查当前登录状态...")
    status = await service.check_login_status()
    
    if status.get("is_logged_in"):
        print(f"✓ 已登录")
        print(f"  用户ID: {status.get('user_id')}")
        print(f"  昵称: {status.get('nickname')}")
        print(f"  VIP类型: {status.get('vip_type', 0)}")
        return True
    else:
        print("✗ 未登录")
        if status.get("error"):
            print(f"  错误: {status.get('error')}")
        return False


async def test_phone_login():
    """测试手机号登录"""
    print("\n" + "=" * 50)
    print("手机号登录测试")
    print("=" * 50)
    
    try:
        phone = input("\n请输入手机号: ").strip()
        if not phone:
            print("手机号不能为空")
            return False
        
        password = getpass.getpass("请输入密码: ")
        if not password:
            print("密码不能为空")
            return False
        
        country_code_input = input("国家代码 (默认86): ").strip()
        country_code = int(country_code_input) if country_code_input else 86
        
        print("\n正在登录...")
        result = await service.login_by_phone(phone, password, country_code)
        
        if result.get("success"):
            print(f"\n✓ {result.get('message')}")
            print(f"  用户ID: {result.get('user_id')}")
            print(f"  昵称: {result.get('nickname')}")
            return True
        elif result.get("need_captcha"):
            # 需要验证码验证
            print(f"\n⚠ {result.get('message')}")
            if result.get("redirect_url"):
                print(f"  风控链接: {result.get('redirect_url')}")
            
            # 询问是否发送验证码
            send = input("\n是否发送验证码到手机? (y/n): ").strip().lower()
            if send == 'y':
                print("\n正在发送验证码...")
                send_result = await service.send_login_captcha(phone, country_code)
                
                if send_result.get("success"):
                    print(f"✓ {send_result.get('message')}")
                    
                    # 输入验证码
                    captcha = input("\n请输入收到的验证码: ").strip()
                    if captcha:
                        print("\n正在使用验证码登录...")
                        captcha_result = await service.login_by_phone_with_captcha(
                            phone, captcha, country_code
                        )
                        
                        if captcha_result.get("success"):
                            print(f"\n✓ {captcha_result.get('message')}")
                            print(f"  用户ID: {captcha_result.get('user_id')}")
                            print(f"  昵称: {captcha_result.get('nickname')}")
                            return True
                        else:
                            print(f"\n✗ {captcha_result.get('message')}")
                            print(f"  错误码: {captcha_result.get('code')}")
                            return False
                    else:
                        print("验证码不能为空")
                        return False
                else:
                    print(f"✗ {send_result.get('message')}")
                    return False
            else:
                print("已取消验证码登录")
                return False
        else:
            print(f"\n✗ {result.get('message')}")
            print(f"  错误码: {result.get('code')}")
            return False
            
    except KeyboardInterrupt:
        print("\n\n登录已取消")
        return False
    except Exception as e:
        print(f"\n✗ 登录异常: {e}")
        return False


async def test_email_login():
    """测试邮箱登录"""
    print("\n" + "=" * 50)
    print("邮箱登录测试")
    print("=" * 50)
    
    try:
        email = input("\n请输入邮箱: ").strip()
        if not email:
            print("邮箱不能为空")
            return False
        
        password = getpass.getpass("请输入密码: ")
        if not password:
            print("密码不能为空")
            return False
        
        print("\n正在登录...")
        result = await service.login_by_email(email, password)
        
        if result.get("success"):
            print(f"\n✓ {result.get('message')}")
            print(f"  用户ID: {result.get('user_id')}")
            print(f"  昵称: {result.get('nickname')}")
            return True
        else:
            print(f"\n✗ {result.get('message')}")
            print(f"  错误码: {result.get('code')}")
            return False
            
    except KeyboardInterrupt:
        print("\n\n登录已取消")
        return False
    except Exception as e:
        print(f"\n✗ 登录异常: {e}")
        return False


async def test_captcha_login():
    """测试验证码登录"""
    print("\n" + "=" * 50)
    print("验证码登录测试")
    print("=" * 50)
    
    try:
        phone = input("\n请输入手机号: ").strip()
        if not phone:
            print("手机号不能为空")
            return False
        
        country_code_input = input("国家代码 (默认86): ").strip()
        country_code = int(country_code_input) if country_code_input else 86
        
        # 发送验证码
        print("\n正在发送验证码...")
        send_result = await service.send_login_captcha(phone, country_code)
        
        if not send_result.get("success"):
            print(f"✗ {send_result.get('message')}")
            print(f"  错误码: {send_result.get('code')}")
            return False
        
        print(f"✓ {send_result.get('message')}")
        
        # 输入验证码
        captcha = input("\n请输入收到的验证码: ").strip()
        if not captcha:
            print("验证码不能为空")
            return False
        
        # 使用验证码登录
        print("\n正在登录...")
        result = await service.login_by_phone_with_captcha(phone, captcha, country_code)
        
        if result.get("success"):
            print(f"\n✓ {result.get('message')}")
            print(f"  用户ID: {result.get('user_id')}")
            print(f"  昵称: {result.get('nickname')}")
            return True
        else:
            print(f"\n✗ {result.get('message')}")
            print(f"  错误码: {result.get('code')}")
            return False
            
    except KeyboardInterrupt:
        print("\n\n登录已取消")
        return False
    except Exception as e:
        print(f"\n✗ 登录异常: {e}")
        return False


async def test_user_playlist():
    """测试获取用户歌单"""
    print("\n" + "=" * 50)
    print("获取用户歌单测试")
    print("=" * 50)
    
    # 先检查登录状态
    is_logged_in = await test_login_status()
    if not is_logged_in:
        print("\n需要先登录才能获取歌单")
        return
    
    print("\n正在获取歌单...")
    result = await service.get_user_playlists()
    
    if result.get("error"):
        print(f"✗ 错误: {result.get('error')}")
        return
    
    playlists = result.get("playlists", [])
    count = result.get("count", 0)
    
    print(f"\n✓ 共有 {count} 个歌单")
    
    if playlists:
        print("\n歌单列表:")
        for i, playlist in enumerate(playlists[:10], 1):
            name = playlist.get("name", "未知歌单")
            track_count = playlist.get("trackCount", 0)
            creator = playlist.get("creator", {}).get("nickname", "未知")
            print(f"  {i}. {name}")
            print(f"     创建者: {creator} | 歌曲数: {track_count}")
        
        if count > 10:
            print(f"\n  ... 还有 {count - 10} 个歌单")


async def test_playlist_detail():
    """测试获取歌单详细信息"""
    print("\n" + "=" * 50)
    print("获取歌单详细信息测试")
    print("=" * 50)
    
    # 先检查登录状态
    is_logged_in = await test_login_status()
    if not is_logged_in:
        print("\n提示: 未登录，将无法获取部分私密歌单")
    
    try:
        # 选择1: 从用户歌单中选择
        print("\n请选择歌单来源:")
        print("1. 从我的歌单中选择")
        print("2. 手动输入歌单ID")
        
        choice = input("\n请选择 (1/2): ").strip()
        
        playlist_id = None
        
        if choice == "1":
            if not is_logged_in:
                print("\n需要先登录才能获取我的歌单")
                return
            
            print("\n正在获取歌单列表...")
            result = await service.get_user_playlists()
            
            if result.get("error"):
                print(f"✗ 错误: {result.get('error')}")
                return
            
            playlists = result.get("playlists", [])
            if not playlists:
                print("✗ 没有找到歌单")
                return
            
            # 显示歌单列表
            print(f"\n找到 {len(playlists)} 个歌单:")
            for i, playlist in enumerate(playlists[:20], 1):
                name = playlist.get("name", "未知歌单")
                playlist_id_item = playlist.get("id")
                track_count = playlist.get("trackCount", 0)
                print(f"  {i}. {name} (ID: {playlist_id_item}, 歌曲数: {track_count})")
            
            if len(playlists) > 20:
                print(f"\n  ... 还有 {len(playlists) - 20} 个歌单")
            
            # 选择歌单
            selection = input("\n请输入歌单编号 (1-20): ").strip()
            try:
                index = int(selection) - 1
                if 0 <= index < min(20, len(playlists)):
                    playlist_id = playlists[index].get("id")
                else:
                    print("无效的编号")
                    return
            except ValueError:
                print("请输入有效的数字")
                return
        
        elif choice == "2":
            playlist_id_input = input("\n请输入歌单ID: ").strip()
            if not playlist_id_input:
                print("歌单ID不能为空")
                return
            try:
                playlist_id = int(playlist_id_input)
            except ValueError:
                print("请输入有效的数字ID")
                return
        else:
            print("无效的选择")
            return
        
        if not playlist_id:
            print("未能获取歌单ID")
            return
        
        # 获取歌单详情
        print(f"\n正在获取歌单 {playlist_id} 的详细信息...")
        detail = await service.get_playlist_detail(playlist_id)
        
        if detail.get("error"):
            print(f"\n✗ 错误: {detail.get('error')}")
            if detail.get("code"):
                print(f"  错误码: {detail.get('code')}")
            return
        
        # 显示歌单详情
        print(f"\n\u2713 成功获取歌单详情")
        print(f"\n{'=' * 50}")
        print(f"歌单ID: {detail.get('id')}")
        print(f"歌单名称: {detail.get('name')}")
        print(f"创建者: {detail.get('creator', {}).get('nickname')} (ID: {detail.get('creator', {}).get('id')})")
        print(f"歌曲数量: {detail.get('track_count')}")
        print(f"播放次数: {detail.get('play_count')}")
        print(f"收藏次数: {detail.get('subscribed_count')}")
        
        tags = detail.get('tags')
        if tags:
            print(f"标签: {', '.join(tags)}")
        
        if detail.get('description'):
            desc = detail.get('description', '')
            if len(desc) > 100:
                desc = desc[:100] + "..."
            print(f"描述: {desc}")
        
        # 显示部分歌曲
        tracks = detail.get('tracks', [])
        if tracks:
            print(f"\n歌曲列表 (前10首):")
            for i, track in enumerate(tracks[:10], 1):
                track_name = track.get('name', '未知歌曲')
                artists = track.get('ar', [])
                artist_names = ', '.join([ar.get('name', '') for ar in artists])
                print(f"  {i}. {track_name} - {artist_names}")
            
            if len(tracks) > 10:
                print(f"\n  ... 还有 {len(tracks) - 10} 首歌曲")
        else:
            # 如果没有tracks，可能只有track_ids
            track_count = detail.get('track_count', 0)
            if track_count > 0:
                print(f"\n歌单包含 {track_count} 首歌曲（需要单独查询歌曲详情）")
        
        print(f"{'=' * 50}")
        
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n✗ 异常: {e}")
        import traceback
        traceback.print_exc()


async def test_cookie_login():
    """测试Cookie登录"""
    print("\n" + "=" * 50)
    print("Cookie登录测试")
    print("=" * 50)
    
    try:
        print("\n提示: 将从环境变量NETEASE_MUSIC_U读取Cookie")
        print("或者手动输入MUSIC_U cookie值")
        
        use_env = input("\n是否使用环境变量中的Cookie? (y/n): ").strip().lower()
        
        if use_env == 'y':
            print("\n正在使用环境变量登录...")
            result = await service.login_by_cookie()
        else:
            music_u = input("\n请输入MUSIC_U cookie: ").strip()
            if not music_u:
                print("Cookie不能为空")
                return False
            
            print("\n正在登录...")
            result = await service.login_by_cookie(music_u)
        
        if result.get("success"):
            print(f"\n✓ {result.get('message')}")
            print(f"  用户ID: {result.get('user_id')}")
            print(f"  昵称: {result.get('nickname')}")
            print(f"  VIP类型: {result.get('vip_type', 0)}")
            return True
        else:
            print(f"\n✗ {result.get('message')}")
            print(f"  错误码: {result.get('code')}")
            return False
            
    except KeyboardInterrupt:
        print("\n\n登录已取消")
        return False
    except Exception as e:
        print(f"\n✗ 登录异常: {e}")
        return False


async def test_logout():
    """测试登出"""
    print("\n" + "=" * 50)
    print("登出测试")
    print("=" * 50)
    
    result = await service.logout()
    
    if result.get("success"):
        print(f"\n✓ {result.get('message')}")
    else:
        print(f"\n✗ {result.get('message')}")
    
    # 再次检查登录状态
    await test_login_status()


async def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("网易云音乐登录认证功能测试")
    print("=" * 50)
    
    while True:
        print("\n请选择测试选项:")
        print("1. 检查登录状态")
        print("2. Cookie登录（从环境变量）")
        print("3. 手机号+密码登录")
        print("4. 邮箱登录")
        print("5. 手机号+验证码登录")
        print("6. 获取用户歌单")
        print("7. 获取歌单详细信息")
        print("8. 登出")
        print("0. 退出")
        
        try:
            choice = input("\n请输入选项 (0-8): ").strip()
            
            if choice == "0":
                print("\n测试结束")
                break
            elif choice == "1":
                await test_login_status()
            elif choice == "2":
                await test_cookie_login()
            elif choice == "3":
                await test_phone_login()
            elif choice == "4":
                await test_email_login()
            elif choice == "5":
                await test_captcha_login()
            elif choice == "6":
                await test_user_playlist()
            elif choice == "7":
                await test_playlist_detail()
            elif choice == "8":
                await test_logout()
            else:
                print("无效选项，请重新选择")
                
        except KeyboardInterrupt:
            print("\n\n测试已中断")
            break
        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n程序已退出")
