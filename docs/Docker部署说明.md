# Musix Docker 部署说明

## 快速开始

### 1. 准备环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入必要的配置。

### 2. 使用 Docker Compose（推荐）

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 3. 使用 Docker

```bash
# 构建镜像
docker build -t musix-api .

# 运行容器
docker run -d \
  --name musix-api \
  -p 8000:8000 \
  --env-file .env \
  musix-api

# 查看日志
docker logs -f musix-api

# 停止容器
docker stop musix-api
docker rm musix-api
```

## 访问服务

服务启动后，可以通过以下地址访问：

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 配置说明

### 环境变量

在 `.env` 文件中配置以下环境变量：

```bash
# CORS 配置
ALLOWED_ORIGINS=*

# 网易云音乐
NETEASE_MUSIC_U=your_cookie_here

# Bilibili
BILIBILI_SESSDATA=your_sessdata_here
BILIBILI_BILI_JCT=your_bili_jct_here
BILIBILI_BUVID3=your_buvid3_here
```

### 端口映射

默认端口为 8000，可以通过修改 `docker-compose.yml` 或运行命令更改：

```bash
docker run -d -p 3000:8000 --env-file .env musix-api
```

## 常用命令

### Docker Compose

```bash
# 重新构建并启动
docker-compose up -d --build

# 查看容器状态
docker-compose ps

# 进入容器
docker-compose exec musix-api bash

# 查看实时日志
docker-compose logs -f musix-api
```

### Docker

```bash
# 查看运行中的容器
docker ps

# 进入容器
docker exec -it musix-api bash

# 重启容器
docker restart musix-api

# 删除镜像
docker rmi musix-api
```

## 健康检查

容器配置了健康检查，每 30 秒检查一次服务状态：

```bash
# 查看容器健康状态
docker inspect --format='{{.State.Health.Status}}' musix-api
```

## 生产环境部署

### 1. 使用环境变量文件

不要将 `.env` 文件提交到版本控制，在生产环境中单独管理：

```bash
# 创建生产环境配置
cp .env.example .env.production

# 使用生产配置启动
docker-compose --env-file .env.production up -d
```

### 2. 配置 CORS

生产环境建议设置具体的域名：

```bash
ALLOWED_ORIGINS=https://example.com,https://app.example.com
```

### 3. 反向代理

建议使用 Nginx 作为反向代理：

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 故障排查

### 查看日志

```bash
# Docker Compose
docker-compose logs -f musix-api

# Docker
docker logs -f musix-api
```

### 容器无法启动

1. 检查端口是否被占用：`netstat -tuln | grep 8000`
2. 检查 .env 文件是否存在
3. 查看容器日志找出错误原因

### 自动登录失败

检查环境变量是否正确设置：

```bash
docker exec musix-api env | grep NETEASE_MUSIC_U
```

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build

# 或使用 Docker
docker build -t musix-api .
docker stop musix-api
docker rm musix-api
docker run -d --name musix-api -p 8000:8000 --env-file .env musix-api
```
