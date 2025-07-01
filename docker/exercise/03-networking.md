# Networking in Docker

Hãy bắt đầu với một container nginx mới
```bash
docker container run -d --name nginx nginx
```

Sử dụng lệnh `inspect` để xem thông tin về networking trong container nginx:
```bash
docker container inspect nginx
```

Giờ để liệt kê các mạng hiện có trong Docker, sử dụng lệnh:
```bash
docker network ls
```

Như bản có thể thấy, container cuủa chúng ta được gán mặc định là **bridge network**
. Chúng ta sẽ nhận chi tiết sâu hơn về network này thông qua lệnh
```bash
docker network inspect <network_id>
```

- "IPv4Address": "172.17.0.2/16": Đây là thông tin quan trọng nhất. Nó cho biết container "nginx" đã được cấp phát địa chỉ IP là 172.17.0.2 từ dải mạng con 172.17.0.0/16.

- "com.docker.network.bridge.name": "docker0": Tên của giao diện mạng (network interface) ảo được tạo ra trên máy chủ để làm "cầu nối" cho mạng này. Bạn có thể kiểm tra bằng lệnh ifconfig hoặc ip addr trên máy chủ Linux và sẽ thấy một interface tên là docker0.

Giờ chúng ta thấy dịch vụ nginx chạy port 80 bên trong container,
Chúng ta có thể liên hệ với dịch vụ trên port 80 của nginx trên máy chủ docker:


```bash
docker exec -it nginx bash

curl http://127.17.0.2:80
```

Chúng ta có thể thử liên hệ với dịch vụ trên port 80 của nginx trên máy của bạn:
```bash
curl http://127.17.0.2:80
```
Bạn sẽ thấy lỗi connection refused, vì hãy thử tưởng tượng
- Máy chủ (Host) của bạn: Giống như bạn đang đứng ở ngoài đường. Địa chỉ IP của bạn là địa chỉ của con đường đó (ví dụ: 192.168.1.10)
- Docker: Giống như một tòa nhà chung cư tên là "Docker Building".
- Mạng Bridge của Docker (172.17.0.0/16): Là hệ thống mạng nội bộ, hệ thống hành lang và số phòng bên trong tòa nhà đó.
- Container của bạn: Là một căn hộ, ví dụ căn hộ số 172.17.0.2.

Khi bạn đứng ngoài đường (máy chủ) và gọi curl 172.17.0.2, bạn đang hét lên "Ai ở căn hộ 172.17.0.2 trả lời!". Không ai trong tòa nhà có thể nghe thấy bạn, vì địa chỉ đó chỉ có ý nghĩa bên trong tòa nhà mà thôi. Người đi đường khác cũng không biết tòa nhà nào có căn hộ đó.

Giải pháp là bạn cần mở một cổng trên tòa nhà (máy chủ) để có thể liên hệ với căn hộ đó. Bạn có thể làm điều này bằng cách sử dụng tùy chọn `-p` khi chạy container.

Tức là bạn phải công bố (publish) cổng của container ra ngoài máy của bạn. Có thể sử dụng tùy chọn `--publish` hoặc `-p` để làm điều này

```
--publish <host_port>:<container_port>
```

Giờ hãy chạy lại container nginx với tùy chọn `-p` để công bố cổng 80 của container ra cổng 80 trên máy chủ:
```bash
docker container run -d --name nginx2 -p 80:80 nginx
```

Hãy xem sự khác biệt về mô tả của 2 container này khi chạy lệnh
```bash
docker ps
```

Output

```
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                               NAMES
8d5609a40033   nginx     "/docker-entrypoint.…"   35 seconds ago   Up 33 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp   nginx2
2f03f1f2cd10   nginx     "/docker-entrypoint.…"   2 hours ago      Up 2 hours      80/tcp                              nginx
```

Chúng ta có thể thấy container port 80 được ánh xạ tới host port 80 (0.0.0.0:80->80/tcp, :::80->80/tcp)

Và giờ chúng ta sử dụng lệnh inspect để cung cấp thông tin về container
```bash
docker container inspect
```

Giờ chúng ta có thể liên hệ với dịch vụ nginx trên máy của bạn bằng cách sử dụng địa chỉ IP của máy chủ (hoặc localhost nếu bạn đang chạy trên máy cục bộ):
```bash
curl http://127.0.0.1:80
```

## Tự định nghĩa một mạng riêng (bridge network)

Giờ dùng lệnh sau để tạo một mạng riêng (bridge network) mới:
```bash
docker network create mynet
```

Bạn sẽ nhận được 1 ID của mạng mới được tạo ra, ví dụ:
```
d3b2f8c4e5a1c8b9f0e1d2c3b4a5b6c7d8e9f0a1b2c3d4e5f6g7h8i9j0k1l2m
```

Liệt kê các mạng hiện có để xác nhận mạng mới đã được tạo:
```bash
docker network ls
```

Giờ có thể dùng `network connect` để kết nối một container vào mạng mới này

```bash
docker network connect <network_identifier> <container_identifier>

docker network connect mynet nginx
```

Giờ bạn có thể kiểm tra lại thông tin của container nginx để xem nó đã được kết nối vào mạng mới chưa:
```bash
docker inspect nginx
```

Bạn sẽ thấy container chứa 2 giao diện với IP 127.17.0.2 (trên mạng mặc định) và một IP mới là 127.18.0.2 (trên mạng mynet).

Chúng ta cũng có thể gán mạng mới này khi khởi tạo container bằng cách sử dụng tùy chọn `--network`:
```bash
docker run -it --net mynet ubuntu bash
```
Đây là cách để tạo một container mới và kết nối nó vào mạng mynet ngay từ đầu.

Tất cả các container trong cùng một mạng sẽ có thể giao tiếp với nhau thông qua tên của chúng (Vì nó tự động được DNS resolution trong Docker).

Nên bạn có thể liên lạc với `nginx` từ container mới này trực tiếp mà không cần phải nhớ IP.

Trong container mới, bạn có thể thử lệnh:
```bash
apt update && apt install -y curl
```

Giờ chạy thử lệnh này bên trong ubuntu container để xác nhận tự động phân giải DNS hoạt động. 
```
curl http://nginx
```

**! Lưu ý**: Nếu muốn tự động phân giải DNS hoạt động, bạn cần phải gán tên cho container. Sử dụng tên được tạo random sẽ không hoạt động.