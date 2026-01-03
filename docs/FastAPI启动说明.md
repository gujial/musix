# Musix FastAPI 启动说明

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
# 网易云音乐 Cookie（可选，用于自动登录和测试）
# 获取方式：登录 music.163.com，按 F12 -> Application -> Cookies -> MUSIC_U
NETEASE_MUSIC_U=your_music_u_cookie

# Bilibili 凭证（可选）
SESSDATA=your_sessdata
BILI_JCT=your_bili_jct
BUVID3=your_buvid3

# JWT 密钥（生产环境必须修改为强随机字符串）
# 生成方式：openssl rand -hex 32
SECRET_KEY=your-secret-key-change-in-production

# JWT 配置（可选）
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## 运行服务器

### 开发模式

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
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
