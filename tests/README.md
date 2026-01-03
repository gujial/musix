# Musix Tests

测试程序目录

## 测试文件

- `test_services.py` - 测试网易云音乐和Bilibili服务的基本功能
- `test_netease_login.py` - 测试网易云音乐登录认证功能

## 运行测试

从项目根目录运行：

```bash
# 测试服务功能
python tests/test_services.py

# 测试登录认证
python tests/test_netease_login.py

# 或使用模块方式运行
python -m tests.test_services
python -m tests.test_netease_login
```

或者从 tests 目录运行：

```bash
cd tests

# 测试服务功能
python test_services.py

# 测试登录认证
python test_netease_login.py
```

## 项目结构说明

测试程序已更新以适配新的包结构：

- 服务类现在从 `services` 子包导入
- 使用统一的API方法名：
  - `search()` 替代 `search_songs()` 和 `search_videos()`
  - `get_media_info()` 替代 `get_netease_audio_info()` 和 `get_video_info()`
  - `get_user_playlists()` 替代 `get_user_playlist()`

旧的方法名仍然可用以保持向后兼容性。

## 导入示例

```python
# 新的导入方式
from services.netease_service import NeteaseService
from services.bilibili_service import BilibiliService

# 或从主包导入
from musix import NeteaseService, BilibiliService
from musix.services import NeteaseService, BilibiliService
```

