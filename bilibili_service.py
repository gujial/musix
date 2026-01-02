"""
Bilibili 视频服务模块
处理 Bilibili 视频信息获取
"""
import os
from typing import Any
from dotenv import load_dotenv
from bilibili_api import video, sync, Credential, search

# 加载 .env 文件
load_dotenv()


class BilibiliService:
    """Bilibili 视频服务类"""
    
    def __init__(self):
        """初始化 Bilibili 凭证"""
        self.credential = Credential(
            sessdata=os.getenv("SESSDATA", ""),
            bili_jct=os.getenv("BILI_JCT", ""),
            buvid3=os.getenv("BUVID3", "")
        )
    
    async def search_videos(self, keywords: str, page: int = 1) -> dict:
        """
        搜索 Bilibili 视频
        
        Args:
            keywords: 搜索关键词
            page: 页码（从1开始）
            
        Returns:
            dict: 包含搜索结果的字典，包括:
                - videos: 视频列表，每个视频包含:
                    - title: 标题
                    - author: UP主
                    - duration: 时长
                    - bvid: BV号
                    - pic: 封面
                    - play: 播放量
                    - description: 描述
                - total_pages: 总页数
                - current_page: 当前页码
        """
        search_result = sync(search.search(keywords, page=page))
        response_data: dict[str, Any] = search_result  # type: ignore
        
        # 提取视频结果
        video_results = []
        result_list = response_data.get('result', [])
        if isinstance(result_list, list):
            for item in result_list:
                if isinstance(item, dict) and item.get('result_type') == 'video':
                    video_results = item.get('data', [])
                    break
        
        # 获取总页数
        total_pages = response_data.get('numPages', 0)
        if total_pages == 0 and video_results:
            total_pages = 1
        
        return {
            "videos": video_results,
            "total_pages": total_pages,
            "current_page": page
        }
    
    async def get_video_info(self, bvid: str, page: int = 0) -> dict:
        """
        获取 Bilibili 视频的信息
        
        Args:
            bvid: BV号
            page: 分P号（默认为0，表示第一个分P）
            
        Returns:
            dict: 包含视频信息的字典，包括:
                - title: 视频标题
                - desc: 视频描述
                - pic: 封面图片URL
                - pubdate: 发布时间（时间戳）
                - owner: 作者信息 (name, face)
                - stat: 统计信息 (view, like, coin, favorite, danmaku, share)
                - video_url: 视频流URL
                - audio_url: 音频流URL
                - bvid: BV号
                - page: 分P号
        """
        v = video.Video(bvid=bvid, credential=self.credential)
        
        # 获取视频信息
        info = await v.get_info()
        info_data: dict[str, Any] = info  # type: ignore
        
        # 获取下载链接
        download_url = await v.get_download_url(page)
        detector = video.VideoDownloadURLDataDetecter(download_url)  # type: ignore
        streams = detector.detect_best_streams()
        
        # streams[0] 是视频流，streams[1] 是音频流
        video_url = streams[0].url if len(streams) > 0 else None
        audio_url = streams[1].url if len(streams) > 1 else None
        
        return {
            "title": info_data["title"],
            "desc": info_data["desc"],
            "pic": info_data["pic"],
            "pubdate": info_data["pubdate"],
            "owner": info_data["owner"],
            "stat": info_data["stat"],
            "video_url": video_url,
            "audio_url": audio_url,
            "bvid": bvid,
            "page": page
        }
