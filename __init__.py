"""
Musix - 音乐和视频服务模块
提供网易云音乐和Bilibili视频的API接口
"""

from .netease_service import NeteaseService
from .bilibili_service import BilibiliService

__version__ = "0.1.0"
__all__ = ["NeteaseService", "BilibiliService"]
