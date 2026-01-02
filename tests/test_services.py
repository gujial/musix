"""
测试网易云音乐和Bilibili服务模块
"""
import asyncio
import sys
import subprocess
from pathlib import Path

# 添加父目录到系统路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from netease_service import search_songs, get_netease_audio_info
from bilibili_service import BilibiliService


# 修复 bilibili_api 的 atexit 错误
def fix_bilibili_atexit():
    """修复 bilibili_api 在退出时的事件循环错误"""
    try:
        import bilibili_api.utils.network as network
        import atexit
        # 尝试移除所有可能的清理函数避免 atexit 错误
        for attr_name in dir(network):
            if 'clean' in attr_name.lower():
                attr = getattr(network, attr_name, None)
                if callable(attr):
                    try:
                        atexit.unregister(attr)
                    except:
                        pass
    except:
        pass


def play_with_ffmpeg(url: str, media_type: str = "audio", duration: int = 30):
    """
    使用ffmpeg播放URL
    
    Args:
        url: 媒体URL
        media_type: 媒体类型，"audio" 或 "video"
        duration: 播放时长（秒），默认30秒
    """
    if not url:
        print("   ✗ URL为空，无法播放")
        return
    
    print(f"\n   使用ffmpeg播放{media_type}... (播放 {duration} 秒)")
    print(f"   URL: {url[:80]}...")
    
    try:
        # 检查ffmpeg是否存在
        check = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        if check.returncode != 0:
            print("   ✗ 未找到ffmpeg，请先安装: sudo apt install ffmpeg")
            return
        
        # 构建ffmpeg命令
        if media_type == "audio":
            # 仅播放音频
            cmd = [
                'ffmpeg',
                '-i', url,
                '-t', str(duration),  # 限制播放时长
                '-f', 'pulse',  # Linux音频输出
                '-'
            ]
        else:
            # 播放视频
            cmd = [
                'ffplay',  # 使用ffplay来播放视频
                '-i', url,
                '-t', str(duration),
                '-autoexit'  # 播放结束后自动退出
            ]
        
        print(f"   按 Ctrl+C 可随时停止播放")
        print(f"   开始播放...\n")
        
        # 执行播放
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        
        try:
            process.wait(timeout=duration + 5)
        except subprocess.TimeoutExpired:
            process.kill()
        
        print(f"\n   播放完成")
        
    except KeyboardInterrupt:
        print(f"\n   播放已停止")
        if process:
            process.kill()
    except Exception as e:
        print(f"   ✗ 播放错误: {e}")
        print(f"   提示: 确保安装了ffmpeg和ffplay")


def ask_to_play(url: str, media_type: str = "audio"):
    """询问用户是否播放"""
    try:
        response = input(f"\n   是否使用ffmpeg播放{media_type}? (y/n): ").strip().lower()
        if response == 'y':
            duration = input("   播放时长(秒, 默认30): ").strip()
            duration = int(duration) if duration.isdigit() else 30
            play_with_ffmpeg(url, media_type, duration)
    except KeyboardInterrupt:
        print("\n   已跳过播放")
    except Exception as e:
        print(f"   输入错误: {e}")


async def test_netease_service():
    """测试网易云音乐服务"""
    print("=" * 50)
    print("测试网易云音乐服务")
    print("=" * 50)
    
    # 测试搜索功能
    print("\n1. 测试搜索歌曲...")
    try:
        search_result = await search_songs("周杰伦", page=1, page_limit=5)
        print(f"   总结果数: {search_result['total_count']}")
        print(f"   当前页: {search_result['current_page']}")
        print(f"   返回歌曲数: {len(search_result['songs'])}")
        
        if search_result['songs']:
            print("\n   前3首歌曲:")
            for i, song in enumerate(search_result['songs'][:3], 1):
                print(f"   {i}. {song['name']} - {song['ar'][0]['name']}")
                print(f"      ID: {song['id']}")
        
        # 测试获取音频信息
        if search_result['songs']:
            print("\n2. 测试获取音频信息...")
            song_id = search_result['songs'][0]['id']
            audio_info = await get_netease_audio_info(song_id)
            print(f"   歌曲名: {audio_info['title']}")
            print(f"   作者: {audio_info['author']}")
            print(f"   专辑: {audio_info['album_name']}")
            print(f"   时长: {audio_info['duration']}")
            print(f"   下载链接: {audio_info['download_url'][:50]}..." if audio_info['download_url'] else "   下载链接: None")
            
            # 询问是否播放
            if audio_info['download_url']:
                ask_to_play(audio_info['download_url'], "audio")
            
    except Exception as e:
        print(f"   ✗ 错误: {e}")
    
    print("\n网易云音乐服务测试完成\n")


async def test_bilibili_service():
    """测试Bilibili服务"""
    print("=" * 50)
    print("测试Bilibili服务")
    print("=" * 50)
    
    service = BilibiliService()
    
    # 测试搜索功能
    print("\n1. 测试搜索视频...")
    try:
        search_result = await service.search_videos("周杰伦", page=1)
        print(f"   当前页: {search_result['current_page']}")
        print(f"   总页数: {search_result['total_pages']}")
        print(f"   返回视频数: {len(search_result['videos'])}")
        
        if search_result['videos']:
            print("\n   前3个视频:")
            for i, video in enumerate(search_result['videos'][:3], 1):
                title = video.get('title', '未知标题')
                author = video.get('author', video.get('upname', '未知作者'))
                bvid = video.get('bvid', video.get('bv_id', '未知BV号'))
                print(f"   {i}. {title}")
                print(f"      UP主: {author}")
                print(f"      BVID: {bvid}")
        else:
            print("   提示: 没有返回视频结果，可能需要配置Bilibili凭证或API不可用")
        
        # 测试获取视频信息
        if search_result['videos']:
            print("\n2. 测试获取视频信息...")
            video_item = search_result['videos'][1]
            bvid = video_item.get('bvid') or video_item.get('bv_id')
            if bvid:
                video_info = await service.get_video_info(bvid, page=0)
                print(f"   标题: {video_info['title']}")
                print(f"   UP主: {video_info['owner']['name']}")
                print(f"   播放量: {video_info['stat']['view']}")
                print(f"   点赞数: {video_info['stat']['like']}")
                print(f"   视频URL: {video_info['video_url'][:50]}..." if video_info['video_url'] else "   视频URL: None")
                print(f"   音频URL: {video_info['audio_url'][:50]}..." if video_info['audio_url'] else "   音频URL: None")
                
                # 询问是否播放
                if video_info['audio_url'] or video_info['video_url']:
                    print("\n   可用的播放选项:")
                    if video_info['video_url']:
                        print("   1. 播放视频")
                    if video_info['audio_url']:
                        print("   2. 仅播放音频")
                    
                    try:
                        choice = input("\n   选择播放选项 (1/2/n): ").strip()
                        if choice == '1' and video_info['video_url']:
                            duration = input("   播放时长(秒, 默认30): ").strip()
                            duration = int(duration) if duration.isdigit() else 30
                            play_with_ffmpeg(video_info['video_url'], "video", duration)
                        elif choice == '2' and video_info['audio_url']:
                            duration = input("   播放时长(秒, 默认30): ").strip()
                            duration = int(duration) if duration.isdigit() else 30
                            play_with_ffmpeg(video_info['audio_url'], "audio", duration)
                    except KeyboardInterrupt:
                        print("\n   已跳过播放")
            else:
                print("   ✗ 无法获取BVID")
                
    except Exception as e:
        print(f"   ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nBilibili服务测试完成\n")


async def main():
    """主函数"""
    print("\n开始测试音乐服务模块\n")
    
    # 修复 bilibili_api 的 atexit 问题
    fix_bilibili_atexit()
    
    # 测试网易云音乐服务
    await test_netease_service()
    
    # 测试Bilibili服务
    await test_bilibili_service()
    
    print("=" * 50)
    print("所有测试完成")
    print("=" * 50)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n测试已中断")
        sys.exit(0)
