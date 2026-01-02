"""
网易云音乐服务模块
处理网易云音乐的音频获取
"""
import datetime
from typing import Any, Optional
from pyncm import apis, GetCurrentSession


async def send_login_captcha(phone: str, country_code: int = 86) -> dict:
    """
    发送登录验证码到手机
    
    Args:
        phone: 手机号
        country_code: 国家代码（默认86为中国）
        
    Returns:
        dict: 发送结果，包括:
            - success: 是否成功
            - code: 返回码
            - message: 消息
    """
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
    phone: str,
    captcha: str,
    country_code: int = 86
) -> dict:
    """
    使用手机号和验证码登录网易云音乐
    
    Args:
        phone: 手机号
        captcha: 验证码
        country_code: 国家代码（默认86为中国）
        
    Returns:
        dict: 登录结果，包括:
            - success: 是否成功
            - code: 返回码
            - message: 消息
            - user_id: 用户ID（登录成功时）
            - nickname: 用户昵称（登录成功时）
    """
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
            return {
                "success": True,
                "code": 200,
                "message": "登录成功",
                "user_id": account.get("id"),
                "nickname": profile.get("nickname"),
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


async def login_by_phone(phone: str, password: str, country_code: int = 86) -> dict:
    """
    使用手机号登录网易云音乐
    
    Args:
        phone: 手机号
        password: 密码（明文）
        country_code: 国家代码（默认86为中国）
        
    Returns:
        dict: 登录结果，包括:
            - success: 是否成功
            - code: 返回码
            - message: 消息
            - user_id: 用户ID（登录成功时）
            - nickname: 用户昵称（登录成功时）
            - need_captcha: 是否需要验证码（当遇到风控时）
            - phone: 手机号（需要验证码时返回，方便后续使用）
    """
    try:
        response = apis.login.LoginViaCellphone(phone=phone, password=password, ctcode=country_code)
        response_data: dict[str, Any] = response  # type: ignore
        
        if response_data.get("code") == 200:
            result = response_data.get("result", {})
            account = result.get("account", {})
            profile = result.get("profile", {})
            return {
                "success": True,
                "code": 200,
                "message": "登录成功",
                "user_id": account.get("id"),
                "nickname": profile.get("nickname"),
                "cookie": result.get("cookie")
            }
        # 检查是否需要验证码（错误码8821表示需要行为验证码）
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
        # 检查异常信息中是否包含验证码相关错误
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


async def login_by_email(email: str, password: str) -> dict:
    """
    使用邮箱登录网易云音乐
    
    Args:
        email: 邮箱地址
        password: 密码（明文）
        
    Returns:
        dict: 登录结果，包括:
            - success: 是否成功
            - code: 返回码
            - message: 消息
            - user_id: 用户ID（登录成功时）
            - nickname: 用户昵称（登录成功时）
    """
    try:
        response = apis.login.LoginViaEmail(email=email, password=password)
        response_data: dict[str, Any] = response  # type: ignore
        
        if response_data.get("code") == 200:
            account = response_data.get("account", {})
            profile = response_data.get("profile", {})
            return {
                "success": True,
                "code": 200,
                "message": "登录成功",
                "user_id": account.get("id"),
                "nickname": profile.get("nickname"),
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


async def check_login_status() -> dict:
    """
    检查当前登录状态
    
    Returns:
        dict: 登录状态信息，包括:
            - is_logged_in: 是否已登录
            - user_id: 用户ID（如果已登录）
            - nickname: 用户昵称（如果已登录）
    """
    try:
        session = GetCurrentSession()
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


async def logout() -> dict:
    """
    登出网易云音乐
    
    Returns:
        dict: 登出结果
            - success: 是否成功
            - message: 消息
    """
    try:
        # 清除当前 session
        session = GetCurrentSession()
        session.cookies.clear()
        return {
            "success": True,
            "message": "登出成功"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"登出异常: {str(e)}"
        }


async def get_user_playlist(user_id: Optional[int] = None) -> dict:
    """
    获取用户歌单列表
    
    Args:
        user_id: 用户ID（如果不提供，则获取当前登录用户的歌单）
        
    Returns:
        dict: 包含歌单信息的字典，包括:
            - playlists: 歌单列表
            - count: 歌单数量
    """
    try:
        if user_id is None:
            # 获取当前登录用户ID
            status = await check_login_status()
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
