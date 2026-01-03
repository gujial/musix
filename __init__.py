"""
Musix - 音乐和视频服务模块
提供网易云音乐和Bilibili视频的API接口

使用示例:
    from musix import NeteaseService, BilibiliService
    from musix.services import NeteaseService  # 也可以从子包导入
    
    # 创建服务实例
    netease = NeteaseService()
    bilibili = BilibiliService()
    
    # 搜索
    songs = await netease.search("歌曲名")
    videos = await bilibili.search("视频名")
"""

from .services import NeteaseService, BilibiliService
from .media_service import MediaService, AuthenticatedMediaService

__version__ = "0.1.0"
__all__ = [
    "NeteaseService",
    "BilibiliService",
    "MediaService",
    "AuthenticatedMediaService"
]
