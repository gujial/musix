"""
Musix FastAPI 主应用
提供音乐和视频媒体服务的 RESTful API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, netease, bilibili

# 创建 FastAPI 应用
app = FastAPI(
    title="Musix API",
    description="统一音乐和视频媒体服务接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该配置具体的域名
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
