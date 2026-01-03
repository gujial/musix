"""
Bilibili API 路由
处理 Bilibili 视频相关的所有API请求
"""
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Optional
import time
from app.schemas import (
    ResponseModel, PaginatedResponse, VideoSearchResult, VideoDetail,
    VideoOwner, VideoStat, VideoPage, VideoPagesResponse, VideoDownloadResponse,
    PaginationInfo
)
from app.auth import session_manager
from services.bilibili_service import BilibiliService

router = APIRouter(prefix="/bilibili", tags=["Bilibili"])


# 获取 Bilibili 服务的依赖函数
def get_bilibili_service() -> BilibiliService:
    """获取 Bilibili 服务实例"""
    return session_manager.bilibili_service


@router.get("/search", response_model=ResponseModel[PaginatedResponse[VideoSearchResult]])
async def search_videos(
    keywords: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    service: BilibiliService = Depends(get_bilibili_service)
):
    """
    搜索视频
    
    按关键词搜索 Bilibili 视频
    """
    try:
        # 调用搜索服务
        result = await service.search(keywords=keywords, page=page)
        
        # 转换为响应格式
        items = []
        for video in result.get("items", []):
            items.append(VideoSearchResult(
                bvid=video.get("bvid", ""),
                aid=video.get("aid", 0),
                title=video.get("title", ""),
                description=video.get("description", ""),
                pic=video.get("pic", ""),
                author=video.get("author", ""),
                mid=video.get("mid", 0),
                duration=video.get("duration", ""),
                play=video.get("play", 0),
                pubdate=video.get("pubdate", 0)
            ))
        
        return ResponseModel(
            code=200,
            data=PaginatedResponse(
                items=items,
                pagination=PaginationInfo(
                    current_page=result.get("current_page", page),
                    page_size=len(items),
                    total_count=result.get("total_count", len(items)),
                    total_pages=result.get("total_pages", 1)
                )
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"搜索视频失败: {str(e)}"
        )


@router.get("/videos/{bvid}", response_model=ResponseModel[VideoDetail])
async def get_video_detail(
    bvid: str,
    page: int = Query(0, ge=0, description="分P编号"),
    service: BilibiliService = Depends(get_bilibili_service)
):
    """
    获取视频详情
    
    返回视频的详细信息，包括播放链接
    """
    try:
        # 获取视频信息
        video_info = await service.get_media_info(media_id=bvid, page=page)
        
        # 构建响应
        return ResponseModel(
            code=200,
            data=VideoDetail(
                bvid=video_info.get("bvid", ""),
                title=video_info.get("title", ""),
                desc=video_info.get("desc", ""),
                pic=video_info.get("pic", ""),
                pubdate=video_info.get("pubdate", 0),
                owner=VideoOwner(
                    mid=video_info.get("owner", {}).get("mid"),
                    name=video_info.get("owner", {}).get("name"),
                    face=video_info.get("owner", {}).get("face")
                ),
                stat=VideoStat(
                    view=video_info.get("stat", {}).get("view", 0),
                    danmaku=video_info.get("stat", {}).get("danmaku", 0),
                    reply=video_info.get("stat", {}).get("reply", 0),
                    favorite=video_info.get("stat", {}).get("favorite", 0),
                    coin=video_info.get("stat", {}).get("coin", 0),
                    share=video_info.get("stat", {}).get("share", 0),
                    like=video_info.get("stat", {}).get("like", 0)
                ),
                video_url=video_info.get("video_url"),
                audio_url=video_info.get("audio_url"),
                page=video_info.get("page", 0),
                pages=[
                    VideoPage(
                        page=p.get("page", 0),
                        cid=p.get("cid"),
                        part=p.get("part", ""),
                        duration=p.get("duration", 0),
                        dimension=p.get("dimension")
                    )
                    for p in video_info.get("pages", [])
                ]
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取视频详情失败: {str(e)}"
        )


@router.get("/videos/{bvid}/pages", response_model=ResponseModel[VideoPagesResponse])
async def get_video_pages(
    bvid: str,
    service: BilibiliService = Depends(get_bilibili_service)
):
    """
    获取视频分P列表
    
    返回视频的所有分P信息
    """
    try:
        # 获取视频所有分P信息
        video_info = await service.get_video_pages(bvid=bvid)
        
        pages = [
            VideoPage(
                page=p.get("page", 0),
                cid=p.get("cid"),
                part=p.get("part", ""),
                duration=p.get("duration", 0),
                dimension=p.get("dimension")
            )
            for p in video_info.get("pages", [])
        ]
        
        return ResponseModel(
            code=200,
            data=VideoPagesResponse(
                bvid=bvid,
                pages=pages,
                count=len(pages)
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取分P列表失败: {str(e)}"
        )


@router.get("/videos/{bvid}/download", response_model=ResponseModel[VideoDownloadResponse])
async def get_video_download_url(
    bvid: str,
    page: int = Query(0, ge=0, description="分P编号"),
    quality: int = Query(80, description="视频质量：16=360P, 32=480P, 64=720P, 80=1080P"),
    service: BilibiliService = Depends(get_bilibili_service)
):
    """
    获取视频下载链接
    
    返回视频的下载URL
    """
    try:
        # 获取视频信息和下载链接
        video_info = await service.get_media_info(media_id=bvid, page=page)
        
        # 计算过期时间（假设链接1小时后过期）
        expires_at = int(time.time()) + 3600
        
        return ResponseModel(
            code=200,
            data=VideoDownloadResponse(
                video_url=video_info.get("video_url"),
                audio_url=video_info.get("audio_url"),
                quality=quality,
                format="mp4",
                expires_at=expires_at
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取下载链接失败: {str(e)}"
        )
