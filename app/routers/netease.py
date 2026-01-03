"""
网易云音乐 API 路由
处理网易云音乐相关的所有API请求
"""
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Optional
from app.schemas import (
    ResponseModel, PaginatedResponse, SongSearchResult, SongDetail,
    PlaylistInfo, PlaylistDetail, TopListResponse, TopListItem,
    ArtistInfo, AlbumInfo, PaginationInfo, PlaylistCreator
)
from app.auth import optional_netease_login, require_netease_login
from services.netease_service import NeteaseService

router = APIRouter(prefix="/netease", tags=["网易云音乐"])


@router.get("/search", response_model=ResponseModel[PaginatedResponse[SongSearchResult]])
async def search_songs(
    keywords: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    service: NeteaseService = Depends(optional_netease_login)
):
    """
    搜索歌曲
    
    支持按关键词搜索歌曲，返回包含歌曲基本信息的分页结果
    """
    try:
        # 计算偏移量
        offset = (page - 1) * limit
        
        # 调用搜索服务
        result = await service.search(keywords=keywords, limit=limit, offset=offset)
        
        # 解析搜索结果
        songs_data = result.get("result", {}).get("songs", [])
        total_count = result.get("result", {}).get("songCount", 0)
        
        # 转换为响应模型
        items = []
        for song in songs_data:
            items.append(SongSearchResult(
                id=song.get("id"),
                name=song.get("name"),
                artists=[
                    ArtistInfo(id=artist.get("id"), name=artist.get("name"))
                    for artist in song.get("artists", [])
                ],
                album=AlbumInfo(
                    id=song.get("album", {}).get("id"),
                    name=song.get("album", {}).get("name"),
                    pic_url=song.get("album", {}).get("picUrl")
                ),
                duration=song.get("duration", 0),
                fee=song.get("fee")
            ))
        
        # 计算总页数
        total_pages = (total_count + limit - 1) // limit
        
        return ResponseModel(
            code=200,
            data=PaginatedResponse(
                items=items,
                pagination=PaginationInfo(
                    current_page=page,
                    page_size=limit,
                    total_count=total_count,
                    total_pages=total_pages
                )
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"搜索失败: {str(e)}"
        )


@router.get("/songs/{song_id}", response_model=ResponseModel[SongDetail])
async def get_song_detail(
    song_id: int,
    service: NeteaseService = Depends(optional_netease_login)
):
    """
    获取歌曲详情
    
    返回歌曲的详细信息，包括播放链接
    """
    try:
        # 获取歌曲信息
        song_info = await service.get_media_info(media_id=song_id)
        
        return ResponseModel(
            code=200,
            data=SongDetail(
                song_id=song_info.get("song_id", 0),
                title=song_info.get("title", ""),
                author=song_info.get("author", ""),
                album_name=song_info.get("album_name", ""),
                album_pic=song_info.get("album_pic"),
                duration=song_info.get("duration", "00:00:00"),
                download_url=song_info.get("download_url"),  # 允许 None
                bitrate=song_info.get("bitrate")
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取歌曲详情失败: {str(e)}"
        )


@router.get("/playlists", response_model=ResponseModel[dict])
async def get_user_playlists(
    service: NeteaseService = Depends(require_netease_login),
    user_id: Optional[int] = Query(None, description="用户ID")
):
    """
    获取用户歌单列表
    
    需要登录。如果不提供user_id，则返回当前登录用户的歌单
    """
    try:
        # 如果没有提供user_id，使用当前用户的ID
        # TODO: 从 pyncm session 获取当前用户 ID
        target_user_id = user_id if user_id else None
        
        # 获取用户歌单
        result = await service.get_user_playlists(user_id=target_user_id)
        
        # 转换为响应格式
        playlists_data = result.get("playlist", [])
        playlists = []
        
        for playlist in playlists_data:
            playlists.append({
                "id": playlist.get("id"),
                "name": playlist.get("name"),
                "cover_img_url": playlist.get("coverImgUrl"),
                "track_count": playlist.get("trackCount"),
                "play_count": playlist.get("playCount"),
                "creator": {
                    "user_id": playlist.get("creator", {}).get("userId"),
                    "nickname": playlist.get("creator", {}).get("nickname")
                }
            })
        
        return ResponseModel(
            code=200,
            data={
                "playlists": playlists,
                "count": len(playlists)
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取歌单列表失败: {str(e)}"
        )


@router.get("/playlists/{playlist_id}", response_model=ResponseModel[PlaylistDetail])
async def get_playlist_detail(
    playlist_id: int,
    service: NeteaseService = Depends(optional_netease_login)
):
    """
    获取歌单详情
    
    返回歌单的详细信息，包括歌曲列表
    """
    try:
        # 获取歌单详情
        result = await service.get_playlist_detail(playlist_id=playlist_id)
        playlist_data = result.get("playlist", {})
        
        # 转换歌曲列表
        tracks = []
        for track in playlist_data.get("tracks", []):
            tracks.append(SongSearchResult(
                id=track.get("id"),
                name=track.get("name"),
                artists=[
                    ArtistInfo(id=artist.get("id"), name=artist.get("name"))
                    for artist in track.get("ar", [])
                ],
                album=AlbumInfo(
                    id=track.get("al", {}).get("id"),
                    name=track.get("al", {}).get("name"),
                    pic_url=track.get("al", {}).get("picUrl")
                ),
                duration=track.get("dt", 0),
                fee=track.get("fee")
            ))
        
        # 构建响应
        creator = playlist_data.get("creator", {})
        return ResponseModel(
            code=200,
            data=PlaylistDetail(
                id=playlist_data.get("id"),
                name=playlist_data.get("name"),
                description=playlist_data.get("description"),
                cover_img_url=playlist_data.get("coverImgUrl"),
                creator=PlaylistCreator(
                    id=creator.get("userId", 0),
                    nickname=creator.get("nickname", ""),
                    avatar_url=creator.get("avatarUrl")
                ),
                track_count=playlist_data.get("trackCount"),
                play_count=playlist_data.get("playCount"),
                subscribed_count=playlist_data.get("subscribedCount"),
                create_time=playlist_data.get("createTime", 0) // 1000,
                update_time=playlist_data.get("updateTime", 0) // 1000,
                tags=playlist_data.get("tags", []),
                tracks=tracks
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取歌单详情失败: {str(e)}"
        )


@router.get("/toplist/{list_id}", response_model=ResponseModel[TopListResponse])
async def get_toplist(
    list_id: int,
    service: NeteaseService = Depends(optional_netease_login)
):
    """
    获取排行榜
    
    常用榜单ID:
    - 19723756: 云音乐飙升榜
    - 3779629: 云音乐新歌榜
    - 3778678: 云音乐热歌榜
    - 2884035: 云音乐原创榜
    - 60198: 黑胶VIP爱听榜
    """
    try:
        # 获取排行榜详情（排行榜实际上就是特殊的歌单）
        result = await service.get_playlist_detail(playlist_id=list_id)
        playlist_data = result.get("playlist", {})
        
        # 转换为排行榜格式
        items = []
        for index, track in enumerate(playlist_data.get("tracks", []), start=1):
            items.append(TopListItem(
                rank=index,
                song=SongSearchResult(
                    id=track.get("id"),
                    name=track.get("name"),
                    artists=[
                        ArtistInfo(id=artist.get("id"), name=artist.get("name"))
                        for artist in track.get("ar", [])
                    ],
                    album=AlbumInfo(
                        id=track.get("al", {}).get("id"),
                        name=track.get("al", {}).get("name"),
                        pic_url=track.get("al", {}).get("picUrl")
                    ),
                    duration=track.get("dt", 0),
                    fee=track.get("fee")
                )
            ))
        
        return ResponseModel(
            code=200,
            data=TopListResponse(
                list_id=list_id,
                list_name=playlist_data.get("name", ""),
                update_time=playlist_data.get("updateTime", 0) // 1000,
                items=items
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取排行榜失败: {str(e)}"
        )
