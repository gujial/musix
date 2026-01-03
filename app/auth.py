"""
认证依赖和工具
直接使用 pyncm 的 session 管理，不使用 JWT Token
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from services.netease_service import NeteaseService
from services.bilibili_service import BilibiliService


class SessionManager:
    """会话管理器 - 管理各平台的服务实例"""
    
    def __init__(self):
        # 为每个平台创建服务实例，启用自动登录
        self.netease_service = NeteaseService(auto_login=True)
        self.bilibili_service = BilibiliService(auto_login=True)
    
    def get_service(self, platform: str):
        """
        获取指定平台的服务实例
        
        Args:
            platform: 平台名称 (netease, bilibili)
            
        Returns:
            NeteaseService | BilibiliService: 对应平台的服务实例
        """
        if platform == "netease":
            return self.netease_service
        elif platform == "bilibili":
            return self.bilibili_service
        else:
            raise ValueError(f"不支持的平台: {platform}")


# 创建全局会话管理器实例
session_manager = SessionManager()


async def get_netease_service() -> NeteaseService:
    """
    获取网易云音乐服务实例（依赖项）
    
    Returns:
        NeteaseService: 网易云音乐服务实例
    """
    return session_manager.netease_service


async def get_bilibili_service() -> BilibiliService:
    """
    获取 Bilibili 服务实例（依赖项）
    
    Returns:
        BilibiliService: Bilibili 服务实例
    """
    return session_manager.bilibili_service


async def require_netease_login(
    service: NeteaseService = Depends(get_netease_service)
) -> NeteaseService:
    """
    要求网易云音乐登录状态（依赖项）
    
    Args:
        service: 网易云音乐服务实例
        
    Returns:
        NeteaseService: 已登录的服务实例
        
    Raises:
        HTTPException: 未登录
    """
    if not service.is_logged_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要登录才能访问此资源，请先调用登录接口"
        )
    return service


async def optional_netease_login(
    service: NeteaseService = Depends(get_netease_service)
) -> NeteaseService:
    """
    可选的网易云音乐登录状态（依赖项）
    
    Args:
        service: 网易云音乐服务实例
        
    Returns:
        NeteaseService: 服务实例（可能未登录）
    """
    return service
