"""
Musix FastAPI 主应用
提供音乐和视频媒体服务的 RESTful API
启动时自动从环境变量读取凭证并登录
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, netease, bilibili
from app.auth import session_manager
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理 - 启动时自动登录"""
    # 启动时执行
    await session_manager.initialize_login()
    yield
    # 关闭时执行（如果需要清理资源）
    print("\n👋 服务正在关闭...")


# 创建 FastAPI 应用
app = FastAPI(
    title="Musix API",
    description="统一音乐和视频媒体服务接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置 CORS
# 从环境变量读取允许的源，如果未设置则使用默认值
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")] if allowed_origins_str != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(netease.router, prefix="/api/v1")
app.include_router(bilibili.router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "Musix API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/v1/auth",
            "netease": "/api/v1/netease",
            "bilibili": "/api/v1/bilibili"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
