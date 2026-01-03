# Musix FastAPI 启动说明

## 特性

✨ **启动时自动登录**：服务启动时会自动从环境变量读取凭证并登录，无需手动调用登录接口

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

复制示例配置文件并修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下内容：

```bash
# ========== 网易云音乐配置 ==========
# 获取方式：登录 music.163.com，按 F12 -> Application -> Cookies -> MUSIC_U
NETEASE_MUSIC_U=your_music_u_cookie

# ========== Bilibili 配置 ==========
# 获取方式：登录 bilibili.com，按 F12 -> Application -> Cookies
BILIBILI_SESSDATA=your_sessdata
BILIBILI_BILI_JCT=your_bili_jct
BILIBILI_BUVID3=your_buvid3
```

**注意**：
- 如果配置了 `NETEASE_MUSIC_U`，服务启动时会自动登录网易云音乐
- 如果配置了 `BILIBILI_SESSDATA`，服务启动时会自动登录 Bilibili
- 未配置的平台将跳过自动登录，但仍可通过 API 手动登录

## 运行服务器

### 开发模式

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

启动时会看到类似输出：

```
============================================================
🔐 初始化自动登录...
============================================================
📝 检测到 NETEASE_MUSIC_U，尝试登录网易云音乐...
✅ 网易云音乐登录成功：张三 (ID: 123456789)
⚠️  未找到 BILIBILI_SESSDATA 环境变量，跳过 Bilibili 自动登录
============================================================
✅ 自动登录初始化完成

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 生产模式

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 访问 API 文档

启动服务后，访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **根路径**: http://localhost:8000/

## API 端点

### 认证 (/api/v1/auth)
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/captcha/send` - 发送验证码
- `POST /api/v1/auth/logout` - 退出登录
- `GET /api/v1/auth/me` - 获取当前用户信息

### 网易云音乐 (/api/v1/netease)
- `GET /api/v1/netease/search` - 搜索歌曲
- `GET /api/v1/netease/songs/{song_id}` - 获取歌曲详情
- `GET /api/v1/netease/playlists` - 获取用户歌单
- `GET /api/v1/netease/playlists/{playlist_id}` - 获取歌单详情
- `GET /api/v1/netease/toplist/{list_id}` - 获取排行榜

### Bilibili (/api/v1/bilibili)
- `GET /api/v1/bilibili/search` - 搜索视频
- `GET /api/v1/bilibili/videos/{bvid}` - 获取视频详情
- `GET /api/v1/bilibili/videos/{bvid}/pages` - 获取视频分P列表
- `GET /api/v1/bilibili/videos/{bvid}/download` - 获取视频下载链接

## 示例请求

### 1. 登录（Cookie方式）

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "netease",
    "method": "cookie",
    "credentials": {
      "cookie": "MUSIC_U=your_cookie_here"
    }
  }'
```

### 2. 搜索歌曲

```bash
curl -X GET "http://localhost:8000/api/v1/netease/search?keywords=周杰伦&page=1&limit=10"
```

### 3. 获取歌曲详情

```bash
curl -X GET "http://localhost:8000/api/v1/netease/songs/186016"
```

### 4. 搜索 Bilibili 视频

```bash
curl -X GET "http://localhost:8000/api/v1/bilibili/search?keywords=Python教程&page=1"
```

## 注意事项

1. 部分接口需要先登录获取 Token
2. 在请求头中添加：`Authorization: Bearer {your_token}`
3. 生产环境请务必修改 `app/auth.py` 中的 `SECRET_KEY`
4. CORS 配置在 `main.py` 中，生产环境应限制允许的域名
