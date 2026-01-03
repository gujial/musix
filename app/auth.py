"""
认证依赖和工具
直接使用 pyncm 的 session 管理，不使用 JWT Token
启动时自动从环境变量读取凭证并登录
"""
import os
import asyncio
from typing import Optional
from fastapi import Depends, HTTPException, status
from services.netease_service import NeteaseService
from services.bilibili_service import BilibiliService


class SessionManager:
    """会话管理器 - 管理各平台的服务实例，启动时自动登录"""
    
    def __init__(self):
        # 为每个平台创建服务实例，启用自动登录
        self.netease_service = NeteaseService(auto_login=True)
        self.bilibili_service = BilibiliService(auto_login=True)
        
        # 标记是否已初始化登录
        self._login_initialized = False
    
    async def initialize_login(self):
        """从环境变量读取凭证并自动登录"""
        if self._login_initialized:
            return
        
        print("\n" + "="*60)
        print("🔐 初始化自动登录...")
        print("="*60)
        
        # NetEase 自动登录
        netease_music_u = os.getenv("NETEASE_MUSIC_U")
        if netease_music_u:
            try:
                print("📝 检测到 NETEASE_MUSIC_U，尝试登录网易云音乐...")
                result = await self.netease_service.login_by_cookie(cookie=netease_music_u)
                if result.get("success"):
                    nickname = result.get("nickname", "未知用户")
                    user_id = result.get("user_id", "N/A")
                    print(f"✅ 网易云音乐登录成功：{nickname} (ID: {user_id})")
                else:
                    print(f"❌ 网易云音乐登录失败：{result.get('message', '未知错误')}")
            except Exception as e:
                print(f"❌ 网易云音乐登录异常：{e}")
        else:
            print("⚠️  未找到 NETEASE_MUSIC_U 环境变量，跳过网易云音乐自动登录")
        
        # Bilibili 自动登录（如果需要）
        bilibili_sessdata = os.getenv("BILIBILI_SESSDATA")
        if bilibili_sessdata:
            try:
                print("📝 检测到 BILIBILI_SESSDATA，尝试登录 Bilibili...")
                # Bilibili 需要更多凭证
                bili_jct = os.getenv("BILIBILI_BILI_JCT", "")
                buvid3 = os.getenv("BILIBILI_BUVID3", "")
                cookie = f"SESSDATA={bilibili_sessdata}"
                if bili_jct:
                    cookie += f"; bili_jct={bili_jct}"
                if buvid3:
                    cookie += f"; buvid3={buvid3}"
                
                result = await self.bilibili_service.login_by_cookie(cookie=cookie)
                if result.get("success"):
                    print(f"✅ Bilibili 登录成功")
                else:
                    print(f"❌ Bilibili 登录失败：{result.get('message', '未知错误')}")
            except Exception as e:
                print(f"❌ Bilibili 登录异常：{e}")
        else:
            print("⚠️  未找到 BILIBILI_SESSDATA 环境变量，跳过 Bilibili 自动登录")
        
        print("="*60)
        print("✅ 自动登录初始化完成\n")
        self._login_initialized = True
    
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
