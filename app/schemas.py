"""
Pydantic 数据模型
定义 API 的请求和响应数据模型
"""
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field


# ========== 通用响应模型 ==========

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    """通用响应模型"""
    code: int = 200
    message: str = "成功"
    data: Optional[T] = None
    error: Optional[str] = None


class PaginationInfo(BaseModel):
    """分页信息"""
    current_page: int = Field(description="当前页码")
    page_size: int = Field(description="每页数量")
    total_count: int = Field(description="总数量")
    total_pages: int = Field(description="总页数")


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应数据"""
    items: List[T] = Field(description="数据列表")
    pagination: PaginationInfo = Field(description="分页信息")


# ========== 认证相关模型 ==========

class LoginCredentials(BaseModel):
    """登录凭证"""
    cookie: Optional[str] = Field(None, description="Cookie凭证")
    phone: Optional[str] = Field(None, description="手机号")
    password: Optional[str] = Field(None, description="密码")
    captcha: Optional[str] = Field(None, description="验证码")
    email: Optional[str] = Field(None, description="邮箱")


class LoginRequest(BaseModel):
    """登录请求"""
    platform: str = Field(description="平台: netease, bilibili")
    method: str = Field(description="登录方式: cookie, phone, captcha, email")
    credentials: LoginCredentials = Field(description="登录凭证")


class UserInfo(BaseModel):
    """用户信息"""
    user_id: int = Field(description="用户ID")
    nickname: str = Field(description="用户昵称")
    platform: str = Field(description="平台")
    vip_type: Optional[int] = Field(0, description="VIP类型")
    avatar_url: Optional[str] = Field(None, description="头像URL")


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str = Field(description="访问令牌")
    token_type: str = Field("Bearer", description="令牌类型")
    expires_in: int = Field(86400, description="过期时间（秒）")
    user: UserInfo = Field(description="用户信息")


class UserStatusResponse(BaseModel):
    """用户状态响应"""
    user_id: Optional[int] = Field(None, description="用户ID")
    nickname: Optional[str] = Field(None, description="用户昵称")
    platform: str = Field(description="平台")
    vip_type: int = Field(description="VIP类型")
    is_logged_in: bool = Field(description="是否已登录")


class CaptchaRequest(BaseModel):
    """验证码请求"""
    platform: str = Field(description="平台")
    phone: str = Field(description="手机号")
    country_code: int = Field(86, description="国家代码")


# ========== 网易云音乐模型 ==========

class ArtistInfo(BaseModel):
    """艺术家信息"""
    id: int = Field(description="艺术家ID")
    name: str = Field(description="艺术家名称")


class AlbumInfo(BaseModel):
    """专辑信息"""
    id: int = Field(description="专辑ID")
    name: str = Field(description="专辑名称")
    pic_url: Optional[str] = Field(None, description="专辑封面URL")


class SongSearchResult(BaseModel):
    """歌曲搜索结果"""
    id: int = Field(description="歌曲ID")
    name: str = Field(description="歌曲名称")
    artists: List[ArtistInfo] = Field(description="艺术家列表")
    album: AlbumInfo = Field(description="专辑信息")
    duration: int = Field(description="时长（毫秒）")
    fee: Optional[int] = Field(None, description="费用类型")


class SongDetail(BaseModel):
    """歌曲详情"""
    song_id: int = Field(description="歌曲ID")
    title: str = Field(description="歌曲标题")
    author: str = Field(description="作者")
    album_name: str = Field(description="专辑名称")
    album_pic: Optional[str] = Field(None, description="专辑封面")
    duration: str = Field(description="时长（格式化）")
    download_url: Optional[str] = Field(None, description="下载链接")
    bitrate: Optional[int] = Field(None, description="比特率")


class PlaylistCreator(BaseModel):
    """歌单创建者"""
    user_id: int = Field(alias="id", description="用户ID")
    nickname: str = Field(description="昵称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    
    class Config:
        populate_by_name = True


class PlaylistInfo(BaseModel):
    """歌单信息"""
    id: int = Field(description="歌单ID")
    name: str = Field(description="歌单名称")
    cover_img_url: Optional[str] = Field(None, description="封面图片URL")
    track_count: int = Field(description="歌曲数量")
    play_count: int = Field(description="播放次数")
    creator: PlaylistCreator = Field(description="创建者")


class PlaylistDetail(BaseModel):
    """歌单详情"""
    id: int = Field(description="歌单ID")
    name: str = Field(description="歌单名称")
    description: Optional[str] = Field(None, description="描述")
    cover_img_url: Optional[str] = Field(None, description="封面图片")
    creator: PlaylistCreator = Field(description="创建者")
    track_count: int = Field(description="歌曲数量")
    play_count: int = Field(description="播放次数")
    subscribed_count: int = Field(description="订阅数")
    create_time: int = Field(description="创建时间")
    update_time: int = Field(description="更新时间")
    tags: List[str] = Field(description="标签")
    tracks: List[SongSearchResult] = Field(description="歌曲列表")


class TopListItem(BaseModel):
    """排行榜项目"""
    rank: int = Field(description="排名")
    song: SongSearchResult = Field(description="歌曲信息")


class TopListResponse(BaseModel):
    """排行榜响应"""
    list_id: int = Field(description="榜单ID")
    list_name: str = Field(description="榜单名称")
    update_time: int = Field(description="更新时间")
    items: List[TopListItem] = Field(description="榜单项目")


# ========== Bilibili 模型 ==========

class VideoSearchResult(BaseModel):
    """视频搜索结果"""
    bvid: str = Field(description="BV号")
    aid: int = Field(description="AV号")
    title: str = Field(description="标题")
    description: str = Field(description="描述")
    pic: str = Field(description="封面图片")
    author: str = Field(description="作者")
    mid: int = Field(description="作者UID")
    duration: str = Field(description="时长")
    play: int = Field(description="播放量")
    pubdate: int = Field(description="发布时间")


class VideoOwner(BaseModel):
    """视频作者"""
    mid: int = Field(description="作者UID")
    name: str = Field(description="作者名称")
    face: str = Field(description="头像")


class VideoStat(BaseModel):
    """视频统计"""
    view: int = Field(description="播放量")
    danmaku: int = Field(description="弹幕数")
    reply: int = Field(description="评论数")
    favorite: int = Field(description="收藏数")
    coin: int = Field(description="投币数")
    share: int = Field(description="分享数")
    like: int = Field(description="点赞数")


class VideoPage(BaseModel):
    """视频分P信息"""
    page: int = Field(description="分P编号")
    cid: Optional[int] = Field(None, description="CID")
    part: str = Field(description="分P标题")
    duration: int = Field(description="时长（秒）")
    dimension: Optional[dict] = Field(None, description="尺寸信息")


class VideoDetail(BaseModel):
    """视频详情"""
    bvid: str = Field(description="BV号")
    title: str = Field(description="标题")
    desc: str = Field(description="描述")
    pic: str = Field(description="封面")
    pubdate: int = Field(description="发布时间")
    owner: VideoOwner = Field(description="作者")
    stat: VideoStat = Field(description="统计数据")
    video_url: Optional[str] = Field(None, description="视频URL")
    audio_url: Optional[str] = Field(None, description="音频URL")
    page: int = Field(description="当前分P")
    pages: List[VideoPage] = Field(description="所有分P")


class VideoPagesResponse(BaseModel):
    """视频分P列表响应"""
    bvid: str = Field(description="BV号")
    pages: List[VideoPage] = Field(description="分P列表")
    count: int = Field(description="分P总数")


class VideoDownloadResponse(BaseModel):
    """视频下载响应"""
    video_url: Optional[str] = Field(None, description="视频URL")
    audio_url: Optional[str] = Field(None, description="音频URL")
    quality: int = Field(description="视频质量")
    format: str = Field("mp4", description="格式")
    expires_at: int = Field(description="过期时间")
