### Docker Compose
- Giới thiệu về Docker Compose:
  - Docker Compose là công cụ để định nghĩa và chạy nhiều container Docker cùng một lúc.
  - Sử dụng file `docker-compose.yml` để cấu hình các dịch vụ, mạng và volumes.
  - Trong Docker Desktop đã tích hợp sẵn Docker Compose, bạn có thể sử dụng trực tiếp mà không cần cài đặt thêm.

- Cấu trúc của file `docker-compose.yml`:

**Ví dụ 1: Xây Node.JS app trên docker compose**
```yaml
version: '3.8' # Phiên bản của Docker Compose
services: # Định nghĩa các dịch vụ
  web: # Tên dịch vụ
    # Chỉ định image cơ sở
    image: node:20-alpine
    # Hoặc sử dụng Dockerfile để xây dựng image
    build:
       context: . # Thư mục chứa Dockerfile
       dockerfile: Dockerfile # Tên file Dockerfile
    ports:
      - "8080:80" # Mở cổng 8080 trên máy chủ và ánh xạ đến cổng 80 trong container
    volumes:
      - ./app:/usr/src/app # Gắn kết thư mục app từ máy chủ vào container
    environment:
      - NODE_ENV=production # Thiết lập biến môi trường
```


**Ví dụ 2: Data Engineering Stack với PostgreSQL, Redis và Jupyter Notebook**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: dataeng
      POSTGRES_USER: dataeng
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql:/docker-entrypoint-initdb.d

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  jupyter:
    image: jupyter/datascience-notebook:latest
    ports:
      - "8888:8888"
    environment:
      JUPYTER_ENABLE_LAB: "yes"
    volumes:
      - ./notebooks:/home/jovyan/work
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```