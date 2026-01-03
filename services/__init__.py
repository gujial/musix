"""
Services 子包
包含所有媒体服务实现

目前支持的服务:
- NeteaseService: 网易云音乐服务
- BilibiliService: Bilibili视频服务

使用示例:
    from musix.services import NeteaseService, BilibiliService
    
    # 创建服务实例
    netease = NeteaseService()
    bilibili = BilibiliService()
    
    # 搜索
    songs = await netease.search("歌曲名")
    videos = await bilibili.search("视频名")
"""

from .netease_service import NeteaseService
from .bilibili_service import BilibiliService

__all__ = ["NeteaseService", "BilibiliService"]
