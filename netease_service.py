"""
网易云音乐服务模块
处理网易云音乐的音频获取
"""
import datetime
from typing import Any
from pyncm import apis


async def search_songs(keywords: str, page: int = 1, page_limit: int = 25) -> dict:
    """
    搜索网易云音乐
    
    Args:
        keywords: 搜索关键词
        page: 页码（从1开始）
        page_limit: 每页结果数量（默认25）
        
    Returns:
        dict: 包含搜索结果的字典，包括:
            - songs: 歌曲列表，每个歌曲包含:
                - id: 歌曲ID
                - name: 歌曲名
                - ar: 艺术家列表
                - al: 专辑信息
            - total_count: 总结果数
            - current_page: 当前页码
            - page_limit: 每页数量
    """
    offset = page_limit * (page - 1)
    response = apis.cloudsearch.GetSearchResult(
        keyword=keywords,
        stype=1,  # 1表示单曲
        limit=page_limit,
        offset=offset
    )
    
    response_data: dict[str, Any] = response  # type: ignore
    songs = response_data.get("result", {}).get("songs", [])
    total_count = response_data.get("result", {}).get("songCount", 0)
    
    return {
        "songs": songs,
        "total_count": total_count,
        "current_page": page,
        "page_limit": page_limit
    }


async def get_netease_audio_info(song_id: int) -> dict:
    """
    获取网易云音乐的详细信息和音频URL
    
    Args:
        song_id: 歌曲ID
        
    Returns:
        dict: 包含歌曲信息的字典，包括:
            - title: 歌曲名称
            - author: 作者
            - album_name: 专辑名
            - album_pic: 专辑封面URL
            - download_url: 下载URL
            - duration: 时长
            - song_id: 歌曲ID
    """
    detail = apis.track.GetTrackDetail([song_id])
    audio = apis.track.GetTrackAudio([song_id])
    
    detail_data: dict[str, Any] = detail  # type: ignore
    audio_data: dict[str, Any] = audio  # type: ignore
    song: dict[str, Any] = detail_data["songs"][0]
    data: dict[str, Any] = audio_data["data"][0]
    
    # 格式化时长
    time_td = datetime.timedelta(milliseconds=data["time"])
    time_str = str(time_td).split('.')[0]
    
    return {
        "title": song["name"],
        "author": song["ar"][0]["name"],
        "album_name": song["al"]["name"],
        "album_pic": song["al"]["picUrl"],
        "download_url": data["url"],
        "duration": time_str,
        "song_id": song_id
    }
