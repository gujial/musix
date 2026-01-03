# Musix API 接口文档

## 目录

- [1. 概述](#1-概述)
- [2. 通用接口](#2-通用接口)
- [3. 网易云音乐接口](#3-网易云音乐接口)
- [4. Bilibili接口](#4-bilibili接口)
- [5. 错误码说明](#5-错误码说明)
- [6. 数据类型定义](#6-数据类型定义)

---

## 1. 概述

### 1.1 接口规范

所有接口均为异步方法，需要使用 `await` 关键字调用。

### 1.2 响应格式

所有接口返回 `dict` 类型的数据，具体字段根据接口而定。

### 1.3 通用参数

- `**kwargs`: 扩展参数，用于传递额外的平台特定参数

---

## 2. 通用接口

所有媒体服务（网易云音乐、Bilibili等）都实现以下通用接口。

### 2.1 搜索媒体资源

**方法**: `search(keywords, page=1, **kwargs)`

**描述**: 搜索音乐或视频资源

**参数**:
- `keywords` (str): 搜索关键词
- `page` (int, 可选): 页码，从1开始，默认为1
- `**kwargs`: 其他参数
  - `page_limit` (int): 每页数量，默认25（网易云音乐）

**返回**:
```python
{
    "items": [          # 媒体项列表
        {
            # 具体字段见各平台数据结构
        }
    ],
    "total_count": int,  # 总数量
    "current_page": int, # 当前页码
    "page_limit": int    # 每页数量（可选）
}
```

**示例**:
```python
# 网易云音乐
service = NeteaseService()
result = await service.search("周杰伦", page=1, page_limit=10)

# Bilibili
service = BilibiliService()
result = await service.search("技术分享", page=1)
```

---

### 2.2 获取媒体详情

**方法**: `get_media_info(media_id, **kwargs)`

**描述**: 获取单个媒体资源的详细信息

**参数**:
- `media_id` (Any): 媒体ID
  - 网易云音乐: 歌曲ID (int)
  - Bilibili: BV号 (str)
- `**kwargs`: 其他参数
  - `page` (int): Bilibili视频分P编号，默认0

**返回**:
```python
{
    # 具体字段见各平台数据结构
}
```

**示例**:
```python
# 网易云音乐
info = await netease.get_media_info(123456789)

# Bilibili
info = await bilibili.get_media_info("BV1xx411c7mD", page=0)
```

---

### 2.3 获取热门排行榜

**方法**: `get_hot_list(limit=50, **kwargs)`

**描述**: 获取热门/排行榜列表（可选实现）

**参数**:
- `limit` (int, 可选): 返回数量限制，默认50
- `**kwargs`: 其他参数

**返回**:
```python
{
    "items": [],      # 媒体项列表
    "count": int,     # 数量
    "error": str      # 错误信息（如果不支持）
}
```

---

### 2.4 获取推荐内容

**方法**: `get_recommendations(limit=20, **kwargs)`

**描述**: 获取推荐内容（可选实现）

**参数**:
- `limit` (int, 可选): 返回数量限制，默认20
- `**kwargs`: 其他参数

**返回**:
```python
{
    "items": [],      # 媒体项列表
    "count": int,     # 数量
    "error": str      # 错误信息（如果不支持）
}
```

---

## 3. 网易云音乐接口

### 3.1 认证相关

#### 3.1.1 检查登录状态

**方法**: `check_login_status()`

**描述**: 检查当前登录状态

**参数**: 无

**返回**:
```python
{
    "is_logged_in": bool,    # 是否已登录
    "user_id": int,          # 用户ID（如果已登录）
    "nickname": str,         # 用户昵称（如果已登录）
    "vip_type": int,         # VIP类型（如果已登录）
    "error": str             # 错误信息（可选）
}
```

**示例**:
```python
status = await netease.check_login_status()
if status["is_logged_in"]:
    print(f"已登录: {status['nickname']}")
```

---

#### 3.1.2 Cookie登录

**方法**: `login_by_cookie(cookie=None, **kwargs)`

**描述**: 使用MUSIC_U Cookie登录

**参数**:
- `cookie` (str, 可选): MUSIC_U cookie值，如不提供则从环境变量读取
- `**kwargs`: 其他参数

**返回**:
```python
{
    "success": bool,         # 是否成功
    "code": int,             # 状态码（200表示成功）
    "message": str,          # 消息
    "user_id": int,          # 用户ID（成功时）
    "nickname": str,         # 用户昵称（成功时）
    "vip_type": int          # VIP类型（成功时）
}
```

**示例**:
```python
result = await netease.login_by_cookie("your_music_u_cookie")
```

---

#### 3.1.3 手机号密码登录

**方法**: `login_by_phone(phone, password, country_code=86, **kwargs)`

**描述**: 使用手机号和密码登录

**参数**:
- `phone` (str): 手机号
- `password` (str): 密码
- `country_code` (int, 可选): 国家代码，默认86（中国）
- `**kwargs`: 其他参数

**返回**:
```python
{
    "success": bool,         # 是否成功
    "code": int,             # 状态码
    "message": str,          # 消息
    "user_id": int,          # 用户ID（成功时）
    "nickname": str,         # 用户昵称（成功时）
    "cookie": str,           # Cookie（成功时）
    "need_captcha": bool,    # 是否需要验证码（失败且code=8821时）
    "redirect_url": str      # 重定向URL（可选）
}
```

**示例**:
```python
result = await netease.login_by_phone("13800138000", "password")
if result["success"]:
    print("登录成功")
elif result.get("need_captcha"):
    print("需要验证码登录")
```

---

#### 3.1.4 发送登录验证码

**方法**: `send_login_captcha(phone, country_code=86, **kwargs)`

**描述**: 发送登录验证码到手机

**参数**:
- `phone` (str): 手机号
- `country_code` (int, 可选): 国家代码，默认86（中国）
- `**kwargs`: 其他参数

**返回**:
```python
{
    "success": bool,         # 是否成功
    "code": int,             # 状态码
    "message": str           # 消息
}
```

**示例**:
```python
result = await netease.send_login_captcha("13800138000")
```

---

#### 3.1.5 验证码登录

**方法**: `login_by_phone_with_captcha(phone, captcha, country_code=86, **kwargs)`

**描述**: 使用手机号和验证码登录

**参数**:
- `phone` (str): 手机号
- `captcha` (str): 验证码
- `country_code` (int, 可选): 国家代码，默认86（中国）
- `**kwargs`: 其他参数

**返回**:
```python
{
    "success": bool,         # 是否成功
    "code": int,             # 状态码
    "message": str,          # 消息
    "user_id": int,          # 用户ID（成功时）
    "nickname": str,         # 用户昵称（成功时）
    "cookie": str            # Cookie（成功时）
}
```

**示例**:
```python
# 先发送验证码
await netease.send_login_captcha("13800138000")
# 用户输入验证码后登录
result = await netease.login_by_phone_with_captcha("13800138000", "123456")
```

---

#### 3.1.6 邮箱登录

**方法**: `login_by_email(email, password, **kwargs)`

**描述**: 使用邮箱和密码登录

**参数**:
- `email` (str): 邮箱
- `password` (str): 密码
- `**kwargs`: 其他参数

**返回**:
```python
{
    "success": bool,         # 是否成功
    "code": int,             # 状态码
    "message": str,          # 消息
    "user_id": int,          # 用户ID（成功时）
    "nickname": str,         # 用户昵称（成功时）
    "cookie": str            # Cookie（成功时）
}
```

**示例**:
```python
result = await netease.login_by_email("user@example.com", "password")
```

---

#### 3.1.7 登出

**方法**: `logout()`

**描述**: 退出登录

**参数**: 无

**返回**:
```python
{
    "success": bool,         # 是否成功
    "message": str           # 消息
}
```

**示例**:
```python
result = await netease.logout()
```

---

### 3.2 歌曲相关

#### 3.2.1 搜索歌曲

**方法**: `search(keywords, page=1, **kwargs)`

**描述**: 搜索歌曲

**参数**:
- `keywords` (str): 搜索关键词
- `page` (int, 可选): 页码，从1开始
- `**kwargs`:
  - `page_limit` (int): 每页数量，默认25

**返回**:
```python
{
    "items": [              # 歌曲列表
        {
            "id": int,              # 歌曲ID
            "name": str,            # 歌曲名称
            "ar": [                 # 艺术家列表
                {
                    "id": int,
                    "name": str
                }
            ],
            "al": {                 # 专辑信息
                "id": int,
                "name": str,
                "picUrl": str       # 封面图片
            },
            "dt": int,              # 时长(ms)
            "fee": int              # 收费类型
        }
    ],
    "songs": [...],         # 同items（向后兼容）
    "total_count": int,     # 总数量
    "current_page": int,    # 当前页
    "page_limit": int       # 每页数量
}
```

---

#### 3.2.2 获取歌曲详情

**方法**: `get_media_info(media_id, **kwargs)`

**描述**: 获取歌曲详细信息，包括播放链接

**参数**:
- `media_id` (int): 歌曲ID
- `**kwargs`: 其他参数

**返回**:
```python
{
    "title": str,           # 歌曲名
    "author": str,          # 作者
    "album_name": str,      # 专辑名
    "album_pic": str,       # 专辑封面URL
    "download_url": str,    # 播放/下载链接
    "duration": str,        # 时长（格式: HH:MM:SS）
    "song_id": int          # 歌曲ID
}
```

**示例**:
```python
info = await netease.get_media_info(123456789)
print(f"歌曲: {info['title']}")
print(f"播放链接: {info['download_url']}")
```

---

### 3.3 歌单相关

#### 3.3.1 获取用户歌单

**方法**: `get_user_playlists(user_id=None, **kwargs)`

**描述**: 获取用户的歌单列表

**参数**:
- `user_id` (int, 可选): 用户ID，如不提供则获取当前登录用户的
- `**kwargs`: 其他参数

**返回**:
```python
{
    "playlists": [          # 歌单列表
        {
            "id": int,
            "name": str,
            "coverImgUrl": str,
            "trackCount": int,
            "playCount": int,
            "creator": {...},
            # ... 其他字段
        }
    ],
    "count": int,           # 数量
    "error": str            # 错误信息（可选）
}
```

**示例**:
```python
playlists = await netease.get_user_playlists()
for playlist in playlists["playlists"]:
    print(f"{playlist['name']} - {playlist['trackCount']}首")
```

---

#### 3.3.2 获取歌单详情

**方法**: `get_playlist_detail(playlist_id, **kwargs)`

**描述**: 获取歌单详细信息

**参数**:
- `playlist_id` (int): 歌单ID
- `**kwargs`: 其他参数

**返回**:
```python
{
    "id": int,                      # 歌单ID
    "name": str,                    # 歌单名
    "description": str,             # 描述
    "cover_img_url": str,           # 封面URL
    "creator": {                    # 创建者信息
        "id": int,
        "nickname": str,
        "avatar_url": str
    },
    "tracks": [...],                # 歌曲列表
    "track_ids": [...],             # 歌曲ID列表
    "track_count": int,             # 歌曲数量
    "play_count": int,              # 播放次数
    "subscribed_count": int,        # 订阅数
    "create_time": int,             # 创建时间戳
    "update_time": int,             # 更新时间戳
    "tags": [...],                  # 标签
    "error": str                    # 错误信息（可选）
}
```

**示例**:
```python
detail = await netease.get_playlist_detail(123456789)
print(f"歌单: {detail['name']}")
print(f"共{detail['track_count']}首歌曲")
```

---

## 4. Bilibili接口

### 4.1 认证相关

#### 4.1.1 检查登录状态

**方法**: `check_login_status()`

**描述**: 检查当前登录状态（待实现）

**参数**: 无

**返回**:
```python
{
    "is_logged_in": bool,    # 是否已登录
    "message": str           # 消息
}
```

---

#### 4.1.2 登出

**方法**: `logout()`

**描述**: 退出登录（待实现）

**参数**: 无

**返回**:
```python
{
    "success": bool,         # 是否成功
    "message": str           # 消息
}
```

---

### 4.2 视频相关

#### 4.2.1 搜索视频

**方法**: `search(keywords, page=1, **kwargs)`

**描述**: 搜索视频

**参数**:
- `keywords` (str): 搜索关键词
- `page` (int, 可选): 页码，从1开始
- `**kwargs`: 其他参数

**返回**:
```python
{
    "items": [              # 视频列表
        {
            "bvid": str,           # 视频BV号
            "title": str,          # 标题
            "author": str,         # UP主
            "description": str,    # 描述
            "pic": str,            # 封面
            "play": int,           # 播放量
            "duration": str,       # 时长
            "pubdate": int         # 发布时间
        }
    ],
    "videos": [...],        # 同items（向后兼容）
    "total_count": int,     # 总数量
    "total_pages": int,     # 总页数
    "current_page": int     # 当前页
}
```

**示例**:
```python
result = await bilibili.search("编程教程", page=1)
for video in result["items"]:
    print(f"{video['title']} - {video['author']}")
```

---

#### 4.2.2 获取视频详情

**方法**: `get_media_info(media_id, **kwargs)`

**描述**: 获取视频详细信息，包括视频流和音频流链接

**参数**:
- `media_id` (str): 视频BV号
- `**kwargs`:
  - `page` (int): 分P编号，默认0

**返回**:
```python
{
    "title": str,               # 标题
    "desc": str,                # 描述
    "pic": str,                 # 封面URL
    "pubdate": int,             # 发布时间戳
    "owner": {                  # UP主信息
        "mid": int,
        "name": str,
        "face": str
    },
    "stat": {                   # 统计信息
        "view": int,            # 播放量
        "danmaku": int,         # 弹幕数
        "reply": int,           # 评论数
        "favorite": int,        # 收藏数
        "coin": int,            # 投币数
        "share": int,           # 分享数
        "like": int             # 点赞数
    },
    "video_url": str,           # 视频流URL
    "audio_url": str,           # 音频流URL
    "bvid": str,                # BV号
    "page": int                 # 分P编号
}
```

**示例**:
```python
info = await bilibili.get_media_info("BV1xx411c7mD", page=0)
print(f"视频: {info['title']}")
print(f"UP主: {info['owner']['name']}")
print(f"播放量: {info['stat']['view']}")
print(f"视频流: {info['video_url']}")
```

---

## 5. 错误码说明

### 5.1 通用错误码

| 错误码 | 说明 |
|-------|------|
| 200   | 成功 |
| -1    | 通用错误/异常 |

### 5.2 网易云音乐错误码

| 错误码 | 说明 |
|-------|------|
| 200   | 成功 |
| 8821  | 需要验证码验证 |
| 其他  | 平台返回的具体错误码 |

### 5.3 Bilibili错误码

待补充

---

## 6. 数据类型定义

### 6.1 网易云音乐

#### 6.1.1 歌曲对象 (Song)
```python
{
    "id": int,              # 歌曲ID
    "name": str,            # 歌曲名称
    "ar": [                 # 艺术家列表
        {
            "id": int,
            "name": str
        }
    ],
    "al": {                 # 专辑信息
        "id": int,
        "name": str,
        "picUrl": str       # 封面图片URL
    },
    "dt": int,              # 时长(毫秒)
    "fee": int,             # 收费类型（0: 免费, 1: VIP, 4: 购买, 8: 低音质免费）
    "mv": int,              # MV ID（0表示无MV）
    "publishTime": int      # 发布时间戳（可选）
}
```

#### 6.1.2 歌单对象 (Playlist)
```python
{
    "id": int,                      # 歌单ID
    "name": str,                    # 歌单名
    "description": str,             # 描述
    "coverImgUrl": str,             # 封面URL
    "trackCount": int,              # 歌曲数量
    "playCount": int,               # 播放次数
    "subscribedCount": int,         # 订阅数
    "creator": {                    # 创建者
        "userId": int,
        "nickname": str,
        "avatarUrl": str
    },
    "tracks": [...],                # 歌曲列表
    "trackIds": [...],              # 歌曲ID列表
    "createTime": int,              # 创建时间戳
    "updateTime": int,              # 更新时间戳
    "tags": [str]                   # 标签列表
}
```

### 6.2 Bilibili

#### 6.2.1 视频对象 (Video)
```python
{
    "bvid": str,                    # BV号
    "aid": int,                     # AV号
    "title": str,                   # 标题
    "description": str,             # 描述
    "pic": str,                     # 封面URL
    "author": str,                  # UP主名称
    "mid": int,                     # UP主ID
    "duration": str,                # 时长（格式: MM:SS）
    "play": int,                    # 播放量
    "pubdate": int,                 # 发布时间戳
    "video_review": int             # 弹幕数（可选）
}
```

#### 6.2.2 UP主对象 (Owner)
```python
{
    "mid": int,                     # UP主ID
    "name": str,                    # 昵称
    "face": str                     # 头像URL
}
```

#### 6.2.3 统计对象 (Stat)
```python
{
    "view": int,                    # 播放量
    "danmaku": int,                 # 弹幕数
    "reply": int,                   # 评论数
    "favorite": int,                # 收藏数
    "coin": int,                    # 投币数
    "share": int,                   # 分享数
    "like": int,                    # 点赞数
    "dislike": int                  # 点踩数
}
```

---

## 7. 使用完整示例

### 7.1 网易云音乐完整流程

```python
import asyncio
from services.netease_service import NeteaseService

async def main():
    # 1. 初始化服务
    netease = NeteaseService()
    
    # 2. 检查登录状态
    status = await netease.check_login_status()
    if not status["is_logged_in"]:
        # 3. 如果未登录，使用Cookie登录
        login_result = await netease.login_by_cookie()
        if not login_result["success"]:
            print("登录失败")
            return
    
    # 4. 搜索歌曲
    search_result = await netease.search("周杰伦", page=1)
    print(f"找到 {search_result['total_count']} 首歌曲")
    
    # 5. 获取第一首歌的详情
    if search_result["items"]:
        song_id = search_result["items"][0]["id"]
        song_info = await netease.get_media_info(song_id)
        print(f"歌曲: {song_info['title']}")
        print(f"播放链接: {song_info['download_url']}")
    
    # 6. 获取用户歌单
    playlists = await netease.get_user_playlists()
    print(f"共有 {playlists['count']} 个歌单")
    
    # 7. 登出
    await netease.logout()

if __name__ == "__main__":
    asyncio.run(main())
```

### 7.2 Bilibili完整流程

```python
import asyncio
from services.bilibili_service import BilibiliService

async def main():
    # 1. 初始化服务
    bilibili = BilibiliService()
    
    # 2. 搜索视频
    search_result = await bilibili.search("Python教程", page=1)
    print(f"找到 {len(search_result['items'])} 个视频")
    
    # 3. 获取第一个视频的详情
    if search_result["items"]:
        bvid = search_result["items"][0]["bvid"]
        video_info = await bilibili.get_media_info(bvid)
        print(f"视频: {video_info['title']}")
        print(f"UP主: {video_info['owner']['name']}")
        print(f"播放量: {video_info['stat']['view']}")
        print(f"视频流: {video_info['video_url']}")
        print(f"音频流: {video_info['audio_url']}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 8. 注意事项

### 8.1 认证相关

- 网易云音乐的某些功能需要登录才能使用（如获取用户歌单、每日推荐等）
- 建议在 `.env` 文件中配置好认证信息，服务初始化时会自动登录
- Cookie有效期有限，需要定期更新

### 8.2 请求限制

- 各平台都有API调用频率限制，请合理控制请求频率
- 建议添加缓存机制以减少API调用次数

### 8.3 播放链接

- 网易云音乐和Bilibili返回的播放链接都有时效性，需要及时使用
- Bilibili的视频和音频是分离的，需要分别下载后合并

### 8.4 错误处理

- 所有接口都可能抛出异常，建议使用 try-except 包裹调用
- 网络异常、API变更等都可能导致接口调用失败
- 建议检查返回结果中的 `error` 字段和 `success` 字段
