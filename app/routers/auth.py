"""
认证路由
处理用户登录、登出和认证相关的API
不使用 JWT Token，直接使用 pyncm 的 session 管理
"""
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import (
    LoginRequest, ResponseModel, 
    CaptchaRequest, UserStatusResponse
)
from app.auth import session_manager, require_netease_login
from services.netease_service import NeteaseService
from services.bilibili_service import BilibiliService

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=ResponseModel[UserStatusResponse])
async def login(request: LoginRequest):
    """
    用户登录
    
    登录后 session 会保存在服务器端（pyncm 管理），无需返回 token
    
    支持多种登录方式：
    - cookie: Cookie 登录
    - phone: 手机号密码登录
    - captcha: 手机号验证码登录
    - email: 邮箱登录
    """
    platform = request.platform.lower()
    method = request.method.lower()
    
    # 选择服务
    service = session_manager.get_service(platform)
    
    # 执行登录
    try:
        if method == "cookie":
            if not request.credentials.cookie:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cookie 不能为空"
                )
            result = await service.login_by_cookie(cookie=request.credentials.cookie)
        
        elif method == "phone":
            if not request.credentials.phone or not request.credentials.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="手机号和密码不能为空"
                )
            result = await service.login_by_phone(
                phone=request.credentials.phone,
                password=request.credentials.password
            )
        
        elif method == "captcha":
            if not request.credentials.phone or not request.credentials.captcha:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="手机号和验证码不能为空"
                )
            result = await service.login_by_phone_with_captcha(
                phone=request.credentials.phone,
                captcha=request.credentials.captcha
            )
        
        elif method == "email":
            if not request.credentials.email or not request.credentials.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱和密码不能为空"
                )
            result = await service.login_by_email(
                email=request.credentials.email,
                password=request.credentials.password
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的登录方式: {method}"
            )
        
        # 检查登录结果
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result.get("message", "登录失败")
            )
        
        # 返回登录成功信息
        return ResponseModel(
            code=200,
            message="登录成功",
            data=UserStatusResponse(
                user_id=result.get("user_id") or 0,
                nickname=result.get("nickname") or "未知用户",
                platform=platform,
                vip_type=result.get("vip_type", 0),
                is_logged_in=True
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录过程中发生错误: {str(e)}"
        )


@router.post("/captcha/send", response_model=ResponseModel)
async def send_captcha(request: CaptchaRequest):
    """
    发送验证码
    
    向指定手机号发送登录验证码
    """
    platform = request.platform.lower()
    
    # 选择服务（仅 NetEase 支持验证码）
    if platform != "netease":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"平台 {platform} 不支持验证码登录"
        )
    
    # 明确获取 NetEase 服务（类型安全）
    service: NeteaseService = session_manager.netease_service
    
    # 发送验证码
    try:
        result = await service.send_captcha(
            phone=request.phone,
            country_code=request.country_code
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("message", "发送验证码失败")
            )
        
        return ResponseModel(
            code=200,
            message="验证码已发送"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送验证码时发生错误: {str(e)}"
        )


@router.post("/logout", response_model=ResponseModel)
async def logout(service: NeteaseService = Depends(require_netease_login)):
    """
    退出登录
    
    清除服务器端的 session 数据
    """
    try:
        # pyncm 的 session 会自动管理
        return ResponseModel(
            code=200,
            message="已退出登录"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"退出登录时发生错误: {str(e)}"
        )


@router.get("/me", response_model=ResponseModel[UserStatusResponse])
async def get_current_user_info(service: NeteaseService = Depends(require_netease_login)):
    """
    获取当前用户信息
    
    返回当前登录用户的详细信息（基于服务器端 session）
    """
    # TODO: 从 pyncm session 获取实际用户信息
    # 目前简化处理，返回登录状态
    return ResponseModel(
        code=200,
        data=UserStatusResponse(
            user_id=None,  # 可从 pyncm session 获取
            nickname=None,  # 可从 pyncm session 获取
            platform="netease",
            vip_type=0,
            is_logged_in=True
        )
    )
