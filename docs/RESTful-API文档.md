# Musix RESTful API 文档

> **版本**: v1.0  
> **更新时间**: 2026年1月3日  
> **基础URL**: `http://localhost:8000/api/v1`

## 目录

- [1. 概述](#1-概述)
- [2. 认证](#2-认证)
- [3. 通用响应格式](#3-通用响应格式)
- [4. 网易云音乐API](#4-网易云音乐api)
- [5. Bilibili API](#5-bilibili-api)
- [6. 错误码](#6-错误码)

---

## 1. 概述

### 1.1 API规范

- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8
- **请求方法**: GET, POST, PUT, DELETE

### 1.2 请求头

所有请求应包含以下请求头：

```http
Content-Type: application/json
Accept: application/json
```

对于需要认证的接口，还需要包含：

```http
Authorization: Bearer {access_token}
```

### 1.3 分页参数

支持分页的接口统一使用以下查询参数：

- `page`: 页码，从1开始，默认为1
- `limit`: 每页数量，默认为20，最大100

---

## 2. 认证

### 2.1 登录获取Token

**接口**: `POST /auth/login`

**描述**: 用户登录获取访问令牌

**请求体**:
```json
{
  "platform": "netease",
  "method": "cookie",
  "credentials": {
    "cookie": "MUSIC_U=xxx"
  }
}
```

**method 可选值**:
- `cookie`: Cookie登录
- `phone`: 手机号密码登录
- `captcha`: 手机号验证码登录
- `email`: 邮箱登录

**请求示例（手机号密码登录）**:
```json
{
  "platform": "netease",
  "method": "phone",
  "credentials": {
    "phone": "13800138000",
    "password": "password123"
  }
}
```

**响应**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "user": {
      "user_id": 123456789,
      "nickname": "用户昵称",
      "platform": "netease"
    }
  }
}
```

---

### 2.2 发送验证码

**接口**: `POST /auth/captcha/send`

**描述**: 发送登录验证码到手机

**请求体**:
```json
{
  "platform": "netease",
  "phone": "13800138000",
  "country_code": 86
}
```

**响应**:
```json
{
  "code": 200,
  "message": "验证码已发送"
}
```

---

### 2.3 退出登录

**接口**: `POST /auth/logout`

**描述**: 退出登录，使令牌失效

**请求头**:
```http
Authorization: Bearer {access_token}
```

**响应**:
```json
{
  "code": 200,
  "message": "已退出登录"
}
```

---

### 2.4 获取当前用户信息

**接口**: `GET /auth/me`

**描述**: 获取当前登录用户信息

**请求头**:
```http
Authorization: Bearer {access_token}
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "user_id": 123456789,
    "nickname": "用户昵称",
    "platform": "netease",
    "vip_type": 0,
    "is_logged_in": true
  }
}
```

---

## 3. 通用响应格式

### 3.1 成功响应

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    // 业务数据
  }
}
```

### 3.2 错误响应

```json
{
  "code": 400,
  "message": "错误描述",
  "error": "详细错误信息"
}
```

### 3.3 分页响应

```json
{
  "code": 200,
  "data": {
    "items": [...],
    "pagination": {
      "current_page": 1,
      "page_size": 20,
      "total_count": 100,
      "total_pages": 5
    }
  }
}
```

---

## 4. 网易云音乐API

### 4.1 搜索歌曲

**接口**: `GET /netease/search`

**描述**: 搜索歌曲

**查询参数**:
- `keywords` (必需): 搜索关键词
- `page` (可选): 页码，默认1
- `limit` (可选): 每页数量，默认20

**请求示例**:
```http
GET /api/v1/netease/search?keywords=周杰伦&page=1&limit=10
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 186016,
        "name": "稻香",
        "artists": [
          {
            "id": 6452,
            "name": "周杰伦"
          }
        ],
        "album": {
          "id": 18903,
          "name": "魔杰座",
          "pic_url": "https://p1.music.126.net/..."
        },
        "duration": 223000,
        "fee": 0
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 10,
      "total_count": 1000,
      "total_pages": 100
    }
  }
}
```

---

### 4.2 获取歌曲详情

**接口**: `GET /netease/songs/{song_id}`

**描述**: 获取歌曲详细信息，包括播放链接

**路径参数**:
- `song_id`: 歌曲ID

**请求示例**:
```http
GET /api/v1/netease/songs/186016
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "song_id": 186016,
    "title": "稻香",
    "author": "周杰伦",
    "album_name": "魔杰座",
    "album_pic": "https://p1.music.126.net/...",
    "duration": "00:03:43",
    "download_url": "https://music.163.com/song/media/outer/url?id=186016",
    "bitrate": 320000
  }
}
```

---

### 4.3 获取用户歌单

**接口**: `GET /netease/playlists`

**描述**: 获取当前用户的歌单列表（需要登录）

**请求头**:
```http
Authorization: Bearer {access_token}
```

**查询参数**:
- `user_id` (可选): 用户ID，不提供则获取当前登录用户的

**请求示例**:
```http
GET /api/v1/netease/playlists
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "playlists": [
      {
        "id": 123456789,
        "name": "我喜欢的音乐",
        "cover_img_url": "https://p1.music.126.net/...",
        "track_count": 150,
        "play_count": 5000,
        "creator": {
          "user_id": 123456,
          "nickname": "用户昵称"
        }
      }
    ],
    "count": 10
  }
}
```

---

### 4.4 获取歌单详情

**接口**: `GET /netease/playlists/{playlist_id}`

**描述**: 获取歌单详细信息

**路径参数**:
- `playlist_id`: 歌单ID

**请求示例**:
```http
GET /api/v1/netease/playlists/123456789
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "id": 123456789,
    "name": "华语经典",
    "description": "精选华语经典歌曲",
    "cover_img_url": "https://p1.music.126.net/...",
    "creator": {
      "id": 123456,
      "nickname": "创建者",
      "avatar_url": "https://p1.music.126.net/..."
    },
    "track_count": 200,
    "play_count": 100000,
    "subscribed_count": 5000,
    "create_time": 1609459200,
    "update_time": 1704268800,
    "tags": ["华语", "经典", "流行"],
    "tracks": [
      {
        "id": 186016,
        "name": "稻香",
        "artists": [{"id": 6452, "name": "周杰伦"}]
      }
    ]
  }
}
```

---

### 4.6 获取排行榜

**接口**: `GET /netease/toplist/{list_id}`

**描述**: 获取指定排行榜

**路径参数**:
- `list_id`: 榜单ID（可选值见下表）

**常用榜单ID**:
- `19723756`: 云音乐飙升榜
- `3779629`: 云音乐新歌榜
- `3778678`: 云音乐热歌榜
- `2884035`: 云音乐原创榜
- `60198`: 黑胶VIP爱听榜

**请求示例**:
```http
GET /api/v1/netease/toplist/3778678
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "list_id": 3778678,
    "list_name": "云音乐热歌榜",
    "update_time": 1704268800,
    "items": [
      {
        "rank": 1,
        "song": {
          "id": 186016,
          "name": "稻香",
          "artists": [{"id": 6452, "name": "周杰伦"}]
        }
      }
    ]
  }
}
```

---

## 5. Bilibili API

### 5.1 获取热门视频

**接口**: `GET /bilibili/popular`

**描述**: 获取热门视频，支持按标签和时间范围筛选

**查询参数**:
- `tag` (可选): 标签名称，如"编程"、"音乐"等，不提供则获取全站热门
- `page` (可选): 页码，默认1
- `page_size` (可选): 每页数量，默认20，最大50
- `days` (可选): 时间范围（天数），1=当天，7=本周，30=本月，不提供则不限制时间

**请求示例**:
```http
# 获取全站热门视频（不限时间）
GET /api/v1/bilibili/popular

# 获取当天全站热门视频
GET /api/v1/bilibili/popular?days=1

# 获取当天"编程"标签的热门视频
GET /api/v1/bilibili/popular?tag=编程&days=1&page=1&page_size=20

# 获取本周"音乐"标签的热门视频
GET /api/v1/bilibili/popular?tag=音乐&days=7

# 获取"编程"标签的热门视频（不限时间）
GET /api/v1/bilibili/popular?tag=编程
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "bvid": "BV1xx411c7mD",
        "aid": 123456789,
        "title": "Python入门教程",
        "description": "从零开始学习Python",
        "pic": "https://i0.hdslb.com/...",
        "author": "UP主名称",
        "mid": 987654321,
        "duration": "10:30",
        "play": 100000,
        "pubdate": 1704268800
      }
    ],
    "pagination": {
      "current_page": 1,
      "page_size": 20,
      "total_count": 100,
      "total_pages": 5
    }
  }
}
```

---

### 5.2 搜索视频

**接口**: `GET /bilibili/search`

**描述**: 搜索视频

**查询参数**:
- `keywords` (必需): 搜索关键词
- `page` (可选): 页码，默认1

**请求示例**:
```http
GET /api/v1/bilibili/search?keywords=Python教程&page=1
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "bvid": "BV1xx411c7mD",
        "aid": 123456789,
        "title": "Python入门教程",
        "description": "从零开始学习Python",
        "pic": "https://i0.hdslb.com/...",
        "author": "UP主名称",
        "mid": 987654321,
        "duration": "10:30",
        "play": 100000,
        "pubdate": 1704268800
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 50
    }
  }
}
```

---

### 5.3 获取视频详情

**接口**: `GET /bilibili/videos/{bvid}`

**描述**: 获取视频详细信息

**路径参数**:
- `bvid`: 视频BV号

**查询参数**:
- `page` (可选): 分P编号，默认0

**请求示例**:
```http
GET /api/v1/bilibili/videos/BV1xx411c7mD?page=0
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "bvid": "BV1xx411c7mD",
    "title": "Python入门教程",
    "desc": "这是一个适合初学者的Python教程",
    "pic": "https://i0.hdslb.com/...",
    "pubdate": 1704268800,
    "owner": {
      "mid": 987654321,
      "name": "UP主名称",
      "face": "https://i0.hdslb.com/..."
    },
    "stat": {
      "view": 100000,
      "danmaku": 500,
      "reply": 200,
      "favorite": 3000,
      "coin": 1500,
      "share": 800,
      "like": 5000
    },
    "video_url": "https://...",
    "audio_url": "https://...",
    "page": 0,
    "pages": [
      {
        "page": 0,
        "part": "第一集",
        "duration": 630
      }
    ]
  }
}
```

---

### 5.4 获取视频分P列表

**接口**: `GET /bilibili/videos/{bvid}/pages`

**描述**: 获取视频的所有分P信息

**路径参数**:
- `bvid`: 视频BV号

**请求示例**:
```http
GET /api/v1/bilibili/videos/BV1xx411c7mD/pages
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "bvid": "BV1xx411c7mD",
    "pages": [
      {
        "page": 0,
        "cid": 123456,
        "part": "第一集",
        "duration": 630,
        "dimension": {
          "width": 1920,
          "height": 1080
        }
      },
      {
        "page": 1,
        "cid": 123457,
        "part": "第二集",
        "duration": 720
      }
    ],
    "count": 2
  }
}
```

---

### 5.5 获取视频下载链接

**接口**: `GET /bilibili/videos/{bvid}/download`

**描述**: 获取视频的下载链接（需要认证）

**路径参数**:
- `bvid`: 视频BV号

**查询参数**:
- `page` (可选): 分P编号，默认0
- `quality` (可选): 视频质量（16: 360P, 32: 480P, 64: 720P, 80: 1080P）

**请求头**:
```http
Authorization: Bearer {access_token}
```

**请求示例**:
```http
GET /api/v1/bilibili/videos/BV1xx411c7mD/download?page=0&quality=80
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**响应**:
```json
{
  "code": 200,
  "data": {
    "video_url": "https://...",
    "audio_url": "https://...",
    "quality": 80,
    "format": "mp4",
    "expires_at": 1704355200
  }
}
```

---

## 6. 错误码

### 6.1 HTTP状态码

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权/令牌无效 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

### 6.2 业务错误码

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 1001 | 参数错误 |
| 1002 | 参数缺失 |
| 2001 | 未登录 |
| 2002 | 登录失败 |
| 2003 | 令牌过期 |
| 2004 | 令牌无效 |
| 2005 | 需要验证码 |
| 3001 | 资源不存在 |
| 3002 | 搜索失败 |
| 3003 | 获取详情失败 |
| 4001 | 平台API错误 |
| 4002 | 网络错误 |
| 5000 | 服务器内部错误 |

### 6.3 错误响应示例

```json
{
  "code": 2002,
  "message": "登录失败",
  "error": "用户名或密码错误"
}
```

---

## 7. 完整请求示例

### 7.1 使用 cURL

#### 搜索歌曲
```bash
curl -X GET "http://localhost:8000/api/v1/netease/search?keywords=周杰伦&page=1" \
  -H "Content-Type: application/json"
```

#### 登录
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "netease",
    "method": "phone",
    "credentials": {
      "phone": "13800138000",
      "password": "password123"
    }
  }'
```

#### 获取歌曲详情（需要登录）
```bash
curl -X GET "http://localhost:8000/api/v1/netease/songs/186016" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 7.2 使用 Python requests

```python
import requests

# 基础URL
BASE_URL = "http://localhost:8000/api/v1"

# 1. 登录
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "platform": "netease",
        "method": "cookie",
        "credentials": {
            "cookie": "MUSIC_U=xxx"
        }
    }
)
token = login_response.json()["data"]["access_token"]

# 2. 搜索歌曲
search_response = requests.get(
    f"{BASE_URL}/netease/search",
    params={
        "keywords": "周杰伦",
        "page": 1,
        "limit": 10
    }
)
songs = search_response.json()["data"]["items"]

# 3. 获取歌曲详情（带认证）
song_id = songs[0]["id"]
headers = {"Authorization": f"Bearer {token}"}
detail_response = requests.get(
    f"{BASE_URL}/netease/songs/{song_id}",
    headers=headers
)
song_detail = detail_response.json()["data"]

print(f"歌曲: {song_detail['title']}")
print(f"播放链接: {song_detail['download_url']}")
```

---

### 7.3 使用 JavaScript fetch

```javascript
const BASE_URL = 'http://localhost:8000/api/v1';

// 1. 登录
async function login() {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      platform: 'netease',
      method: 'cookie',
      credentials: {
        cookie: 'MUSIC_U=xxx'
      }
    })
  });
  
  const data = await response.json();
  return data.data.access_token;
}

// 2. 搜索歌曲
async function searchSongs(keywords) {
  const response = await fetch(
    `${BASE_URL}/netease/search?keywords=${encodeURIComponent(keywords)}&page=1`
  );
  
  const data = await response.json();
  return data.data.items;
}

// 3. 获取歌曲详情
async function getSongDetail(songId, token) {
  const response = await fetch(`${BASE_URL}/netease/songs/${songId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  return data.data;
}

// 使用示例
(async () => {
  const token = await login();
  const songs = await searchSongs('周杰伦');
  const detail = await getSongDetail(songs[0].id, token);
  console.log('歌曲:', detail.title);
  console.log('播放链接:', detail.download_url);
})();
```
