
# Tạo Docker Container đầu tiên

### Lệnh thực thi

```bash
docker container run --name firsttest-$USER hello-world
```

## Tìm hiểu điều gì đã xảy ra trong quá trình trên

Bạn đã chạy lệnh `docker run hello-world` trong đó `hello-world` là tên của image.

Docker client yêu cầu Docker daemon tải image `hello-world` và chạy container từ image đó.

Docker daemon kiểm tra image cục bộ, và nhận thấy image này chưa tồn tại:

`Unable to find image 'hello-world:latest' locally`.

Daemon sau đó kết nối tới registry mặc định là [Docker Hub](https://hub.docker.com/) và tải bản mới nhất của image `hello-world`:

`Pulling from library/hello-world`.

Sau đó Docker daemon tạo một container mới từ image vừa tải.

Cuối cùng Docker daemon chạy container và thực thi chương trình trong image `hello-world`.

Chức năng duy nhất của container `hello-world` là in ra thông điệp lên terminal, sau đó container sẽ thoát.

### Kiểm tra container đã tạo

Bạn có thể sử dụng lệnh sau để liệt kê các container đang chạy (thêm tùy chọn `-a` để hiển thị cả các container đã dừng):

```bash
docker container ps -a
```

Bạn sẽ thấy container vừa được tạo và thực thi từ image `hello-world`:

```bash
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                        PORTS     NAMES
c0ba7d45168a   hello-world   "/hello"   About a minute ago   Exited (0) About a minute ago           thirsty_poitras
```

Dừng container:
   ```bash
     # Sử dụng lệnh docker ps để lấy container_id
     # Sau đó dừng container bằng lệnh:
     docker stop <container_id>
   ```
Xoá container:
  ```bash
    # Sử dụng lệnh docker ps -a để lấy container_id
    # Sau đó xoá container bằng lệnh:
    docker rm <container_id>
  ```

#### Lưu ý

> Khi tạo container mà không đặt tên cụ thể, Docker sẽ tự tạo tên ngẫu nhiên.

> Tên được tạo bằng cách kết hợp:

> - Một tính từ mô tả cảm xúc (furious, goofy, suspicious, boring...)
> - Tên của một nhà phát minh nổi tiếng (tesla, darwin, wozniak...)

> Ví dụ: `happy_curie`, `jovial_lovelace` ...
