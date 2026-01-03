"""
网易云音乐服务模块
处理网易云音乐的音频获取
"""
import datetime
import os
from typing import Any, Optional
from dotenv import load_dotenv
from pyncm import apis, GetCurrentSession
from media_service import AuthenticatedMediaService

# 加载 .env 文件
load_dotenv()

class NeteaseService(AuthenticatedMediaService):
    """网易云音乐服务类"""
    
    def __init__(self, auto_login: bool = True):
        """
        初始化网易云音乐服务
        
        Args:
            auto_login: 是否自动尝试使用cookie登录（默认True）
        """
        super().__init__(auto_login)
        self.session = GetCurrentSession()
        
        # 自动尝试cookie登录
        if auto_login:
            music_u = os.getenv("NETEASE_MUSIC_U", "")
            if music_u:
                try:
                    response = apis.login.LoginViaCookie(MUSIC_U=music_u)
                    if response and response.get("code") == 200:
                        # 同步检查登录状态
                        status_response = apis.login.GetCurrentLoginStatus()
                        status_data: dict[str, Any] = status_response  # type: ignore
                        if status_data.get("code") == 200 and status_data.get("account"):
                            self.is_logged_in = True
                            account = status_data.get("account", {})
                            profile = status_data.get("profile", {})
                            self.user_info = {
                                "user_id": account.get("id"),
                                "nickname": profile.get("nickname"),
                                "vip_type": account.get("vipType", 0)
                            }
                except Exception:
                    # 静默失败，不影响服务使用
                    pass
    
    async def login_by_cookie(self, cookie: Optional[str] = None, **kwargs) -> dict:
        """
        使用Cookie登录网易云音乐
        
        Args:
            cookie: MUSIC_U cookie值（如果不提供，则从环境变量NETEASE_MUSIC_U中读取）
            **kwargs: 其他参数
            
        Returns:
            dict: 登录结果
        """
        try:
            music_u = cookie
            if music_u is None:
                music_u = os.getenv("NETEASE_MUSIC_U", "")
            
            if not music_u:
                return {
                    "success": False,
                    "code": -1,
                    "message": "未提供MUSIC_U cookie，请设置环境变量NETEASE_MUSIC_U或传入参数"
                }
            
            response = apis.login.LoginViaCookie(MUSIC_U=music_u)
            response_data: dict[str, Any] = response  # type: ignore
            
            if response_data.get("code") == 200:
                status = await self.check_login_status()
                if status.get("is_logged_in"):
                    self.is_logged_in = True
                    self.user_info = {
                        "user_id": status.get("user_id"),
                        "nickname": status.get("nickname"),
                        "vip_type": status.get("vip_type")
                    }
                    return {
                        "success": True,
                        "code": 200,
                        "message": "Cookie登录成功",
                        **self.user_info
                    }
                else:
                    return {
                        "success": False,
                        "code": -1,
                        "message": "Cookie无效或已过期"
                    }
            else:
                return {
                    "success": False,
                    "code": response_data.get("code"),
                    "message": response_data.get("message", "Cookie登录失败")
                }
        except Exception as e:
            return {
                "success": False,
                "code": -1,
                "message": f"Cookie登录异常: {str(e)}"
            }
    
    async def send_login_captcha(self, phone: str, country_code: int = 86, **kwargs) -> dict:
        """发送登录验证码到手机"""
        try:
            response = apis.login.SetSendRegisterVerifcationCodeViaCellphone(
                cell=phone,
                ctcode=country_code
            )
            response_data: dict[str, Any] = response  # type: ignore
            
            if response_data.get("code") == 200:
                return {
                    "success": True,
                    "code": 200,
                    "message": "验证码已发送，24小时内最多发送5次"
                }
            else:
                return {
                    "success": False,
                    "code": response_data.get("code"),
                    "message": response_data.get("message", "发送验证码失败")
                }
        except Exception as e:
            return {
                "success": False,
                "code": -1,
                "message": f"发送验证码异常: {str(e)}"
            }
    
    async def login_by_phone_with_captcha(
        self,
        phone: str,
        captcha: str,
        country_code: int = 86,
        **kwargs
    ) -> dict:
        """使用手机号和验证码登录"""
        try:
            response = apis.login.LoginViaCellphone(
                phone=phone,
                captcha=captcha,
                ctcode=country_code
            )
            response_data: dict[str, Any] = response  # type: ignore
            
            if response_data.get("code") == 200:
                result = response_data.get("result", {})
                account = result.get("account", {})
                profile = result.get("profile", {})
                
                self.is_logged_in = True
                self.user_info = {
                    "user_id": account.get("id"),
                    "nickname": profile.get("nickname")
                }
                
                return {
                    "success": True,
                    "code": 200,
                    "message": "登录成功",
                    **self.user_info,
                    "cookie": result.get("cookie")
                }
            else:
                return {
                    "success": False,
                    "code": response_data.get("code"),
                    "message": response_data.get("message", "登录失败")
                }
        except Exception as e:
            return {
                "success": False,
                "code": -1,
                "message": f"登录异常: {str(e)}"
            }
    
    async def login_by_phone(self, phone: str, password: str, country_code: int = 86, **kwargs) -> dict:
        """使用手机号和密码登录"""
        try:
            response = apis.login.LoginViaCellphone(phone=phone, password=password, ctcode=country_code)
            response_data: dict[str, Any] = response  # type: ignore
            
            if response_data.get("code") == 200:
                result = response_data.get("result", {})
                account = result.get("account", {})
                profile = result.get("profile", {})
                
                self.is_logged_in = True
                self.user_info = {
                    "user_id": account.get("id"),
                    "nickname": profile.get("nickname")
                }
                
                return {
                    "success": True,
                    "code": 200,
                    "message": "登录成功",
                    **self.user_info,
                    "cookie": result.get("cookie")
                }
            elif response_data.get("code") == 8821:
                return {
                    "success": False,
                    "code": 8821,
                    "message": "需要验证码验证，请使用验证码登录",
                    "need_captcha": True,
                    "phone": phone,
                    "country_code": country_code,
                    "redirect_url": response_data.get("redirectUrl")
                }
            else:
                return {
                    "success": False,
                    "code": response_data.get("code"),
                    "message": response_data.get("message", response_data.get("msg", "登录失败"))
                }
        except Exception as e:
            error_str = str(e)
            if "8821" in error_str or "验证码" in error_str:
                return {
                    "success": False,
                    "code": 8821,
                    "message": "需要验证码验证，请使用验证码登录",
                    "need_captcha": True,
                    "phone": phone,
                    "country_code": country_code
                }
            return {
                "success": False,
                "code": -1,
                "message": f"登录异常: {error_str}"
            }
    
    async def login_by_email(self, email: str, password: str, **kwargs) -> dict:
        """使用邮箱登录"""
        try:
            response = apis.login.LoginViaEmail(email=email, password=password)
            response_data: dict[str, Any] = response  # type: ignore
            
            if response_data.get("code") == 200:
                account = response_data.get("account", {})
                profile = response_data.get("profile", {})
                
                self.is_logged_in = True
                self.user_info = {
                    "user_id": account.get("id"),
                    "nickname": profile.get("nickname")
                }
                
                return {
                    "success": True,
                    "code": 200,
                    "message": "登录成功",
                    **self.user_info,
                    "cookie": response_data.get("cookie")
                }
            else:
                return {
                    "success": False,
                    "code": response_data.get("code"),
                    "message": response_data.get("msg", "登录失败")
                }
        except Exception as e:
            return {
                "success": False,
                "code": -1,
                "message": f"登录异常: {str(e)}"
            }
    
    async def check_login_status(self) -> dict:
        """检查当前登录状态"""
        try:
            response = apis.login.GetCurrentLoginStatus()
            response_data: dict[str, Any] = response  # type: ignore
            
            if response_data.get("code") == 200 and response_data.get("account"):
                account = response_data.get("account", {})
                profile = response_data.get("profile", {})
                return {
                    "is_logged_in": True,
                    "user_id": account.get("id"),
                    "nickname": profile.get("nickname"),
                    "vip_type": account.get("vipType", 0)
                }
            else:
                return {
                    "is_logged_in": False
                }
        except Exception as e:
            return {
                "is_logged_in": False,
                "error": str(e)
            }
    
    async def logout(self) -> dict:
        """登出"""
        try:
            self.session.cookies.clear()
            self.is_logged_in = False
            self.user_info = {}
            return {
                "success": True,
                "message": "登出成功"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"登出异常: {str(e)}"
            }
    
    async def get_user_playlists(self, user_id: Optional[int] = None, **kwargs) -> dict:
        """获取用户歌单列表（实现抽象方法）"""
        try:
            if user_id is None:
                status = await self.check_login_status()
                if not status.get("is_logged_in"):
                    return {
                        "playlists": [],
                        "count": 0,
                        "error": "未登录"
                    }
                user_id = status.get("user_id")
            
            response = apis.user.GetUserPlaylists(user_id=user_id)
            response_data: dict[str, Any] = response  # type: ignore
            
            playlists = response_data.get("playlist", [])
            return {
                "playlists": playlists,
                "count": len(playlists)
            }
        except Exception as e:
            return {
                "playlists": [],
                "count": 0,
                "error": str(e)
            }
    
    async def get_playlist_detail(self, playlist_id: Any, **kwargs) -> dict:
        """
        获取歌单详细信息
        
        Args:
            playlist_id: 歌单ID
            **kwargs: 其他参数
            
        Returns:
            dict: 歌单详细信息
        """
        try:
            playlist_id = int(playlist_id)
            response = apis.playlist.GetPlaylistInfo(playlist_id)
            response_data: dict[str, Any] = response  # type: ignore
            
            if response_data.get("code") != 200:
                return {
                    "error": response_data.get("message", "获取歌单信息失败"),
                    "code": response_data.get("code")
                }
            
            playlist = response_data.get("playlist", {})
            
            return {
                "id": playlist.get("id"),
                "name": playlist.get("name"),
                "description": playlist.get("description"),
                "cover_img_url": playlist.get("coverImgUrl"),
                "creator": {
                    "id": playlist.get("creator", {}).get("userId"),
                    "nickname": playlist.get("creator", {}).get("nickname"),
                    "avatar_url": playlist.get("creator", {}).get("avatarUrl")
                },
                "tracks": playlist.get("tracks", []),
                "track_ids": playlist.get("trackIds", []),
                "track_count": playlist.get("trackCount", 0),
                "play_count": playlist.get("playCount", 0),
                "subscribed_count": playlist.get("subscribedCount", 0),
                "create_time": playlist.get("createTime"),
                "update_time": playlist.get("updateTime"),
                "tags": playlist.get("tags", [])
            }
        except Exception as e:
            return {
                "error": f"获取歌单详情异常: {str(e)}"
            }
    
    async def search(self, keywords: str, page: int = 1, **kwargs) -> dict:
        """搜索网易云音乐（实现抽象方法）"""
        page_limit = kwargs.get('page_limit', 25)
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
            "items": songs,  # 统一字段名
            "songs": songs,  # 保持向后兼容
            "total_count": total_count,
            "current_page": page,
            "page_limit": page_limit
        }
    
    async def get_media_info(self, media_id: Any, **kwargs) -> dict:
        """获取网易云音乐的详细信息（实现抽象方法）"""
        song_id = int(media_id)
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
