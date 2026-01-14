"""
Bilibili 视频服务模块
处理 Bilibili 视频信息获取
"""
import os
from typing import Any, Optional
from dotenv import load_dotenv
from bilibili_api import video, sync, Credential, search
from media_service import AuthenticatedMediaService

# 加载 .env 文件
load_dotenv()

class BilibiliService(AuthenticatedMediaService):
    """Bilibili 视频服务类"""
    
    def __init__(self, auto_login: bool = True):
        """
        初始化 Bilibili 凭证
        
        Args:
            auto_login: 是否自动尝试登录（默认True，当前未实现）
        """
        super().__init__(auto_login)
        self.credential = Credential(
            sessdata=os.getenv("SESSDATA", ""),
            bili_jct=os.getenv("BILI_JCT", ""),
            buvid3=os.getenv("BUVID3", "")
        )
    
    async def search(self, keywords: str, page: int = 1, **kwargs) -> dict:
        """搜索 Bilibili 视频（实现抽象方法）"""
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
            "items": video_results,  # 统一字段名
            "videos": video_results,  # 保持向后兼容
            "total_count": len(video_results),  # 与 MediaService 接口一致
            "total_pages": total_pages,
            "current_page": page
        }
    
    async def get_media_info(self, media_id: Any, **kwargs) -> dict:
        """获取 Bilibili 视频信息（实现抽象方法）"""
        bvid = str(media_id)
        page = kwargs.get('page', 0)
        
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
            "duration": info_data["duration"],
            "bvid": bvid,
            "page": page
        }
    
    async def get_video_pages(self, bvid: str, **kwargs) -> dict:
        """
        获取视频所有分P信息
        
        Args:
            bvid: 视频BV号
            **kwargs: 其他参数
            
        Returns:
            dict: 分P信息
        """
        v = video.Video(bvid=bvid, credential=self.credential)
        info = await v.get_info()
        info_data: dict[str, Any] = info  # type: ignore
        
        return {
            "bvid": bvid,
            "pages": info_data.get("pages", [])
        }
    
    async def check_login_status(self) -> dict:
        """
        检查登录状态
        
        Returns:
            dict: 登录状态信息
        """
        # TODO: 实现Bilibili登录状态检查
        return {
            "is_logged_in": False,
            "message": "Bilibili登录功能待实现"
        }
    
    async def logout(self) -> dict:
        """
        登出
        
        Returns:
            dict: 登出结果
        """
        # TODO: 实现Bilibili登出功能
        return {
            "success": True,
            "message": "Bilibili登出功能待实现"
        }
    
    async def login_by_cookie(self, cookie: Optional[str] = None, **kwargs) -> dict:
        """
        使用Cookie登录Bilibili
        
        Args:
            cookie: Cookie值（如果不提供，则从环境变量中读取）
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果
        """

        return {
            "success": True,
            "code": 0,
            "message": "Bilibili Cookie登录功能待实现"
        }
    
    async def login_by_phone(self, phone: str, password: str, country_code: int = 86, **kwargs) -> dict:
        """
        使用手机号和密码登录Bilibili
        
        Args:
            phone: 手机号
            password: 密码
            country_code: 国家代码（默认86为中国）
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果
        """
        # TODO: 实现Bilibili手机号密码登录功能
        return {
            "success": False,
            "code": -1,
            "message": "Bilibili手机号密码登录功能待实现"
        }
    
    async def send_login_captcha(self, phone: str, country_code: int = 86, **kwargs) -> dict:
        """
        发送登录验证码到手机
        
        Args:
            phone: 手机号
            country_code: 国家代码（默认86为中国）
            **kwargs: 其他参数
            
        Returns:
            dict: 发送结果
        """
        # TODO: 实现Bilibili发送验证码功能
        return {
            "success": False,
            "code": -1,
            "message": "Bilibili发送验证码功能待实现"
        }
    
    async def login_by_phone_with_captcha(
        self,
        phone: str,
        captcha: str,
        country_code: int = 86,
        **kwargs
    ) -> dict:
        """
        使用手机号和验证码登录Bilibili
        
        Args:
            phone: 手机号
            captcha: 验证码
            country_code: 国家代码（默认86为中国）
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果
        """
        # TODO: 实现Bilibili手机号验证码登录功能
        return {
            "success": False,
            "code": -1,
            "message": "Bilibili手机号验证码登录功能待实现"
        }
    
    async def login_by_qr_code(self, **kwargs) -> dict:
        """
        使用二维码登录Bilibili
        
        Args:
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果，包含二维码URL
        """
        # TODO: 实现Bilibili二维码登录功能
        # 1. 获取二维码URL和登录密钥
        # 2. 轮询检查登录状态
        # 3. 登录成功后保存凭证
        return {
            "success": False,
            "code": -1,
            "message": "Bilibili二维码登录功能待实现"
        }
    
    async def get_popular_videos(
        self,
        tag: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        days: Optional[int] = None,
        **kwargs
    ) -> dict:
        """
        获取热门视频
        
        Args:
            tag: 标签名称（可选），如果不提供则获取全站热门
            page: 页码
            page_size: 每页数量
            days: 时间范围（天数），可选，1=当天，7=本周，30=本月，不提供则不限制时间
            **kwargs: 其他参数
            
        Returns:
            dict: 热门视频列表
        """
        from bilibili_api import search as bilibili_search
        from datetime import datetime, timedelta
        
        # 计算时间范围
        if days is not None:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
        else:
            start_time = None
            end_time = None
        
        if tag:
            # 使用标签搜索，按综合排序（包含播放量、点赞等因素）
            search_params = {
                "keyword": tag,
                "search_type": bilibili_search.SearchObjectType.VIDEO,
                "order_type": bilibili_search.OrderVideo.TOTALRANK,  # 综合排序
                "page": page,
                "page_size": page_size
            }
            # 只在提供days参数时才添加时间范围
            if start_time is not None and end_time is not None:
                search_params["time_start"] = start_time.strftime("%Y-%m-%d")
                search_params["time_end"] = end_time.strftime("%Y-%m-%d")
            
            search_result = sync(
                bilibili_search.search_by_type(**search_params)
            )
        else:
            # 获取全站热门（使用搜索接口的热门视频）
            search_result = sync(
                bilibili_search.search(
                    "",  # 空关键词
                    page=page
                )
            )
        
        response_data: dict[str, Any] = search_result  # type: ignore
        
        # 提取视频结果
        video_results = []
        result_list = response_data.get('result', [])
        if isinstance(result_list, list):
            for item in result_list:
                if isinstance(item, dict) and item.get('result_type') == 'video':
                    video_results = item.get('data', [])
                    break
        
        # 如果通过标签搜索失败，尝试使用关键词搜索
        if not video_results and tag:
            search_result = sync(bilibili_search.search(tag, page=page))
            response_data = search_result  # type: ignore
            result_list = response_data.get('result', [])
            if isinstance(result_list, list):
                for item in result_list:
                    if isinstance(item, dict) and item.get('result_type') == 'video':
                        video_results = item.get('data', [])
                        break
        
        # 按播放量排序（确保返回真正的热门视频）
        if video_results:
            video_results = sorted(
                video_results,
                key=lambda x: x.get('play', 0) if isinstance(x.get('play'), int) else 0,
                reverse=True
            )
        
        # 获取总页数
        total_pages = response_data.get('numPages', 0)
        if total_pages == 0 and video_results:
            total_pages = 1
        
        return {
            "items": video_results,
            "total_count": len(video_results),
            "total_pages": total_pages,
            "current_page": page,
            "tag": tag,
            "days": days
        }
    
    async def get_playlist_detail(self, playlist_id: Any, **kwargs) -> dict:
        """
        获取Bilibili收藏夹详细信息
        
        Args:
            playlist_id: 收藏夹ID
            **kwargs: 其他参数
            
        Returns:
            dict: 收藏夹详细信息
        """
        # TODO: 实现Bilibili获取收藏夹详细信息功能
        # 需要使用 bilibili_api.favorite 模块
        return {
            "error": "Bilibili获取收藏夹详细信息功能待实现"
        }
