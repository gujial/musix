"""
媒体服务抽象基类
定义统一的媒体服务接口
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, List


class MediaService(ABC):
    """媒体服务抽象基类"""
    
    @abstractmethod
    async def search(self, keywords: str, page: int = 1, **kwargs) -> dict:
        """
        搜索媒体资源
        
        Args:
            keywords: 搜索关键词
            page: 页码（从1开始）
            **kwargs: 其他搜索参数
            
        Returns:
            dict: 搜索结果字典，应包含:
                - items: 媒体项列表
                - total_count: 总数量
                - current_page: 当前页码
        """
        pass
    
    @abstractmethod
    async def get_media_info(self, media_id: Any, **kwargs) -> dict:
        """
        获取媒体详细信息
        
        Args:
            media_id: 媒体ID（可以是字符串、整数等类型）
            **kwargs: 其他参数
            
        Returns:
            dict: 媒体详细信息字典
        """
        pass
    
    async def get_hot_list(self, limit: int = 50, **kwargs) -> dict:
        """
        获取热门/排行榜列表（可选实现）
        
        Args:
            limit: 返回数量限制
            **kwargs: 其他参数
            
        Returns:
            dict: 热门列表，包含:
                - items: 媒体项列表
                - count: 数量
        """
        return {
            "items": [],
            "count": 0,
            "error": "此服务暂不支持热门列表功能"
        }
    
    async def get_recommendations(self, limit: int = 20, **kwargs) -> dict:
        """
        获取推荐内容（可选实现）
        
        Args:
            limit: 返回数量限制
            **kwargs: 其他参数
            
        Returns:
            dict: 推荐列表，包含:
                - items: 媒体项列表
                - count: 数量
        """
        return {
            "items": [],
            "count": 0,
            "error": "此服务暂不支持推荐功能"
        }


class AuthenticatedMediaService(MediaService):
    """需要认证的媒体服务抽象基类"""
    
    def __init__(self, auto_login: bool = True):
        """
        初始化认证服务
        
        Args:
            auto_login: 是否自动尝试登录
        """
        self.is_logged_in: bool = False
        self.user_info: dict[str, Any] = {}
    
    @abstractmethod
    async def check_login_status(self) -> dict:
        """
        检查登录状态
        
        Returns:
            dict: 登录状态信息，应包含:
                - is_logged_in: 是否已登录
                - user_id: 用户ID（如果已登录）
                - nickname: 用户昵称（如果已登录）
        """
        pass
    
    @abstractmethod
    async def logout(self) -> dict:
        """
        登出
        
        Returns:
            dict: 登出结果，应包含:
                - success: 是否成功
                - message: 消息
        """
        pass
    
    async def get_user_playlists(self, user_id: Optional[Any] = None, **kwargs) -> dict:
        """
        获取用户播放列表/收藏夹（可选实现）
        
        Args:
            user_id: 用户ID（如果为None，则获取当前登录用户的）
            **kwargs: 其他参数
            
        Returns:
            dict: 播放列表，包含:
                - playlists: 播放列表数组
                - count: 数量
        """
        return {
            "playlists": [],
            "count": 0,
            "error": "此服务暂不支持获取用户播放列表"
        }
    
    async def get_user_info(self, user_id: Optional[Any] = None, **kwargs) -> dict:
        """
        获取用户详细信息（可选实现）
        
        Args:
            user_id: 用户ID（如果为None，则获取当前登录用户的）
            **kwargs: 其他参数
            
        Returns:
            dict: 用户信息
        """
        return {
            "error": "此服务暂不支持获取用户详细信息"
        }
    
    async def add_to_favorites(self, media_id: Any, **kwargs) -> dict:
        """
        添加到收藏（可选实现）
        
        Args:
            media_id: 媒体ID
            **kwargs: 其他参数（如播放列表ID等）
            
        Returns:
            dict: 操作结果，包含:
                - success: 是否成功
                - message: 消息
        """
        return {
            "success": False,
            "message": "此服务暂不支持收藏功能"
        }
    
    async def remove_from_favorites(self, media_id: Any, **kwargs) -> dict:
        """
        从收藏中移除（可选实现）
        
        Args:
            media_id: 媒体ID
            **kwargs: 其他参数（如播放列表ID等）
            
        Returns:
            dict: 操作结果，包含:
                - success: 是否成功
                - message: 消息
        """
        return {
            "success": False,
            "message": "此服务暂不支持取消收藏功能"
        }
    
    # 登录相关方法（可选实现）
    
    async def login_by_cookie(self, cookie: Optional[str] = None, **kwargs) -> dict:
        """
        使用Cookie登录（可选实现）
        
        Args:
            cookie: Cookie值（如果不提供，则从环境变量中读取）
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果，包含:
                - success: 是否成功
                - code: 状态码
                - message: 消息
        """
        return {
            "success": False,
            "code": -1,
            "message": "此服务暂不支持Cookie登录"
        }
    
    async def login_by_phone(self, phone: str, password: str, country_code: int = 86, **kwargs) -> dict:
        """
        使用手机号和密码登录（可选实现）
        
        Args:
            phone: 手机号
            password: 密码
            country_code: 国家代码（默认86为中国）
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果，包含:
                - success: 是否成功
                - code: 状态码
                - message: 消息
                - need_captcha: 是否需要验证码（可选）
        """
        return {
            "success": False,
            "code": -1,
            "message": "此服务暂不支持手机号密码登录"
        }
    
    async def login_by_email(self, email: str, password: str, **kwargs) -> dict:
        """
        使用邮箱登录（可选实现）
        
        Args:
            email: 邮箱
            password: 密码
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果，包含:
                - success: 是否成功
                - code: 状态码
                - message: 消息
        """
        return {
            "success": False,
            "code": -1,
            "message": "此服务暂不支持邮箱登录"
        }
    
    async def send_login_captcha(self, phone: str, country_code: int = 86, **kwargs) -> dict:
        """
        发送登录验证码到手机（可选实现）
        
        Args:
            phone: 手机号
            country_code: 国家代码（默认86为中国）
            **kwargs: 其他参数
            
        Returns:
            dict: 发送结果，包含:
                - success: 是否成功
                - code: 状态码
                - message: 消息
        """
        return {
            "success": False,
            "code": -1,
            "message": "此服务暂不支持发送验证码"
        }
    
    async def login_by_phone_with_captcha(
        self,
        phone: str,
        captcha: str,
        country_code: int = 86,
        **kwargs
    ) -> dict:
        """
        使用手机号和验证码登录（可选实现）
        
        Args:
            phone: 手机号
            captcha: 验证码
            country_code: 国家代码（默认86为中国）
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果，包含:
                - success: 是否成功
                - code: 状态码
                - message: 消息
        """
        return {
            "success": False,
            "code": -1,
            "message": "此服务暂不支持手机号验证码登录"
        }
    
    async def login_by_qr_code(self, **kwargs) -> dict:
        """
        使用二维码登录（可选实现）
        
        Args:
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果，包含:
                - success: 是否成功
                - code: 状态码
                - message: 消息
                - qr_url: 二维码URL（可选）
        """
        return {
            "success": False,
            "code": -1,
            "message": "此服务暂不支持二维码登录"
        }
