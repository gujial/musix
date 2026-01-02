"""
测试网易云音乐登录认证功能
"""
import asyncio
import getpass
import sys
from pathlib import Path

# 添加父目录到系统路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from netease_service import (
    login_by_phone,
    login_by_phone_with_captcha,
    send_login_captcha,
    login_by_email,
    check_login_status,
    logout,
    get_user_playlist
)


async def test_login_status():
    """测试登录状态"""
    print("\n检查当前登录状态...")
    status = await check_login_status()
    
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
        result = await login_by_phone(phone, password, country_code)
        
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
                send_result = await send_login_captcha(phone, country_code)
                
                if send_result.get("success"):
                    print(f"✓ {send_result.get('message')}")
                    
                    # 输入验证码
                    captcha = input("\n请输入收到的验证码: ").strip()
                    if captcha:
                        print("\n正在使用验证码登录...")
                        captcha_result = await login_by_phone_with_captcha(
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
        result = await login_by_email(email, password)
        
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
        send_result = await send_login_captcha(phone, country_code)
        
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
        result = await login_by_phone_with_captcha(phone, captcha, country_code)
        
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
    result = await get_user_playlist()
    
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


async def test_logout():
    """测试登出"""
    print("\n" + "=" * 50)
    print("登出测试")
    print("=" * 50)
    
    result = await logout()
    
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
        print("2. 手机号+密码登录")
        print("3. 邮箱登录")
        print("4. 手机号+验证码登录")
        print("5. 获取用户歌单")
        print("6. 登出")
        print("0. 退出")
        
        try:
            choice = input("\n请输入选项 (0-6): ").strip()
            
            if choice == "0":
                print("\n测试结束")
                break
            elif choice == "1":
                await test_login_status()
            elif choice == "2":
                await test_phone_login()
            elif choice == "3":
                await test_email_login()
            elif choice == "4":
                await test_captcha_login()
            elif choice == "5":
                await test_user_playlist()
            elif choice == "6":
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
