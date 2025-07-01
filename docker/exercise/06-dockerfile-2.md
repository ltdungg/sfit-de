# Dockerfiles

Phần này mục tiêu của chúng talà tạo một Dockerfile chạy Python App. 
Và chúng ta sẽ có một app để làm việc sau
- Chúng ta cần tạo dockerfile chạy python app và mở ra một port. Giả sử là 9000. Thì chúng ta sẽ muốn nó trả về một JSON dưới dạng
```
{
    env: <environment>
}
```
<environment> là chuỗi được định nghĩa thông qua biến môi trường ENVIRONMENT chúng ta có thể kiểm soát thông qua Docer 

- Docker sẽ chạy và cài đặt ENVIRONMENT, ví dụ là `production`

## App
Đầu tiên ta sẽ tạo folder tên là `flask`:
```bash
mkdir flask
cd flask
```

Tạo một file tên là `app.py` với nội dung như sau:
```python
from flask import Flask
import os
import sys

app = Flask(__name__)

@app.route("/")
def index():
    env = os.getenv("ENVIRONMENT", None)
    return {
        "env": env
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Needs port number as a commandline argument.")
        sys.exit(1)
    port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)
```
Và giờ chúng ta sẽ tạo một entrypoint cho app này đặt tên là `startup.sh`:
```bash
#!/bin/bash

python app.py ${PORT}
```

Và tạo một file requirements.txt với nội dung như sau:
```
Click==7.0
Flask==1.1.1
itsdangerous==1.1.0
Jinja2==2.11.3
MarkupSafe==1.1.1
Werkzeug==0.16.0
```

Và giờ cùng tạo một Dockerfile như sau

```dockerfile
## FROM defines the image to start from. It will be pulled automatically if not available locally.
FROM python:3.7-slim-buster

## RUN executes a shell command, here we install curl
RUN apt-get update && apt-get install -y curl

## COPY imports files from the host to the container file system
COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

## ENV sets environment variables
ENV PORT="3000"
ENV ENVIRONMENT="prod" 

## EXPOSE defines ports intended to be exposed, note how we use env variables defined above
EXPOSE ${PORT}

## It is a good idea to create dedicated users to run the containers instead of running as root
RUN useradd --create-home pythonappuser
## WORKDIR define the working directory where docker run will land to
WORKDIR /home/pythonappuser

## We import the the Flask application scripts
COPY startup.sh .
COPY app.py .

## We make them executable and owned by the new user
RUN chmod +x startup.sh && chmod +x app.py && chown -R pythonappuser:pythonappuser .

## USER selects the default user docker run will land to
USER pythonappuser

## Entrypoint defines the script executed by docker run. Arguments to docker run are passed
## to the entry point.
ENTRYPOINT ["./startup.sh"]
```

Giờ ta sẽ build image này:
```bash
docker build -t flask-app .
```

Đầu tiên, ta sẻ thử chạy Python app 
```bash
docker run -d flask-app
```

Và giờ chúng ta có ID của container và mở bash 
```bash
docker exec -it <container_id> bash
```

Và giờ ta sẽ kiểm tra nếu nó chạy đúng thì nó sẽ trả ra kết quả JSON trên port 3000
```bash
curl http://localhost:3000
```
Thành công.

Giờ ta sẽ ánh xạ port 3000 của container với port của máy Host.
```bash
docker run -d -p 3000:3000 flask-app
```

Giờ thử lại lệnh curl ở trên máy host:
```bash 
curl http://localhost:3000
```

Giờ ta sẽ thử thanh đổi biến môi trường ENVIRONMENT thành `test`:
```bash
docker run -d -p 3000:3000 -e ENVIRONMENT=test flask-app
```

Nếu nó hoạt động đúng như chuúng ta mong muốn, ta sẽ thử lệnh
```bash
curl http://localhost:3000
```