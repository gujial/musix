# Services 子包

这个目录包含所有具体的媒体服务实现。

## 当前支持的服务

### NeteaseService (网易云音乐)
- 搜索歌曲
- 获取歌曲详细信息和下载链接
- 用户登录（Cookie、手机号、邮箱等）
- 获取用户歌单

### BilibiliService (Bilibili视频)
- 搜索视频
- 获取视频详细信息和流媒体链接
- 登录功能（待实现）

## 添加新服务

要添加新的媒体服务，请按以下步骤操作：

1. **创建新的服务文件**
   在 `services/` 目录下创建新文件，例如 `spotify_service.py`

2. **继承抽象基类**
   ```python
   from ..media_service import AuthenticatedMediaService  # 需要登录
   # 或
   from ..media_service import MediaService  # 不需要登录
   
   class SpotifyService(AuthenticatedMediaService):
       def __init__(self, auto_login: bool = True):
           super().__init__(auto_login)
           # 初始化代码
       
       async def search(self, keywords: str, page: int = 1, **kwargs) -> dict:
           # 实现搜索
           pass
       
       async def get_media_info(self, media_id: Any, **kwargs) -> dict:
           # 实现获取媒体信息
           pass
       
       # 实现其他必需的抽象方法...
   ```

3. **更新 __init__.py**
   在 `services/__init__.py` 中添加导入：
   ```python
   from .spotify_service import SpotifyService
   
   __all__ = ["NeteaseService", "BilibiliService", "SpotifyService"]
   ```

4. **更新主包的 __init__.py**
   在 `/home/gujial/repos/musix/__init__.py` 中添加导出（可选）

## 使用示例

```python
from musix.services import NeteaseService, BilibiliService

# 创建服务实例
netease = NeteaseService(auto_login=True)
bilibili = BilibiliService()

# 搜索
songs = await netease.search("周杰伦")
videos = await bilibili.search("Python教程")

# 获取详细信息
song_info = await netease.get_media_info(song_id=12345)
video_info = await bilibili.get_media_info("BV1xx411c7mD")
```

## 架构说明

所有服务都继承自 `MediaService` 或 `AuthenticatedMediaService`，这确保了：
- 统一的接口规范
- 一致的返回格式
- 易于扩展和维护
- 类型安全

参见 `media_service.py` 了解完整的接口定义。
