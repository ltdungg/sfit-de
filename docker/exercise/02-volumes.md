# Docker volumes

Cùng tạo một volume 

```bash
docker volume create volume1
```

và check xem volume đã được tạo thành công chưa:

```bash
docker volume ls
```

Hãy cùng tạo một volume thứ 2 

```bash
docker volume create volume2
```

Kiểm tra lại danh sách các volume:

```bash
docker volume ls
```

Giờ chúng ta sẽ xóa volume2 đã tạo
```bash
docker volume rm volume2
```

Kiểm tra lại danh sách các volume:

```bash
docker volume ls
```

Giờ hãy cùng đi vào một ví dụ thực tế sử dụng Docker volumes
```bash
docker container run -d -p 80:80 nginx2 nginx
```

Vào trang web Nginx tại địa chỉ `http://localhost:80` sẽ thấy nội dung welcome page của Nginx.

Ta sẽ sử dụng `docker exec` để thay đổi nội dung welcome page của Nginx
```bash
docker exec -it nginx2 bash
```

Nó sẽ mở một bash shell bên trong container. Chạy lệnh sau để thay đổi nội dung welcome page:

```bash
echo "I changed the content of this file inside the running container..." > /usr/share/nginx/html/index.html
```

Bây giờ chúng ta truy cập vào trang web Nginx bằng trình duyệt tại địa chỉ `http://localhost:80` và sẽ thấy nội dung đã thay đổi.

Hoặc phương pháp khác là sử dụng lệnh:
```bash
curl localhost:80
```

Giờ ta sẽ khởi động lại container Nginx:
```bash
docker container restart nginx2
```

Giờ điều gì xảy ra? Chúng ta có thể thấy rằng nội dung thay đổi trên welcome page vẫn còn.

Điều gì xảy ra nếu stop container này và chạy một container khác và tải lại page.
```bash
docker container run -d -p 8080:80 --name nginx3 nginx
```

!!! cảnh báo cho container thứ hai này bạn cần chỉ định một port khác, nếu không nó sẽ xảy ra xung đột và container của bạn không thể chạy.

Bây giờ truy cập vào trang web Nginx tại địa chỉ `http://localhost:8080` sẽ thấy nội dung welcome page của Nginx như mặc định.

Không có cách nào để truy cập vào tệp chúng ta đã thay đổi ở một container khác.

## Sử dụng Docker volumes
Giờ hãy tạo một volume sử dụng cho nginx container
```bash
docker volume create myvol
```
Chúng ta có thể xem địa chỉ volume được đặt bằng
```
docker volume inspect myvol
```

Giờ ta sẽ tạo lại container nginx và gắn vào volume này.

Xóa container cũ bằng cách (1 là stop container trước sau đó mới xóa, 2 là xóa trực tiếp không cần stop bằng -f hoặc --force):
```bash
docker container rm -f nginx3
```

Tạo lại và gắn volume bằng cách sử dụng --mount:
```bash
docker container run -d -p 8080:80 --name nginx3 --mount type=volume,source=myvol,target=/usr/share/nginx/html nginx
```

Giờ hãy chỉnh sửa nội dung welcome page của Nginx trong container này, mặc định nằm ở `/usr/share/nginx/html/index.html`:
```bash
docker exec -it nginx3 bash

echo "I've changed the content of this file in the docker volume" > /usr/share/nginx/html/index.html
```

Vào trang web Nginx tại địa chỉ `http://localhost:8080` sẽ thấy nội dung đã thay đổi.

Giờ ta sẽ dừng và xóa container này:
```bash
docker container rm -f nginx3
```

Giờ ta sẽ tạo lại container Nginx và gắn vào volume này:
```bash
docker container run -d -p 8080:80 --name nginx3 --mount type=volume,source=myvol,destination=/usr/share/nginx/html nginx
```

Và kiểm tra trên trang web Nginx tại địa chỉ `http://localhost:8080` sẽ thấy nội dung đã thay đổi vẫn còn.

Giờ hãy thử tạo một container mới và gắn vào volume này:
```bash
docker container run -d -p 8081:80 --name nginx3-2 --mount type=volume,source=myvol,destination=/usr/share/nginx/html nginx
```

Vào trang web Nginx tại địa chỉ `http://localhost:8081` sẽ thấy nội dung đã thay đổi vẫn còn.

## Sử dụng bind mounts
Giờ chúng ta sẽ tạo một container chạy Nginx và sử dụng bind mount để gắn thư mục từ máy chủ vào container thay vì volume
(sử dụng `type=bind`).

Chạy lệnh này
```bash
docker container run -d -p 8088:80 --name nginx4 --mount type=bind,source=./tmp/nginx,destination=/usr/share/nginx/html nginx
```

Ta sẽ nhận được một lỗi /tmp/nginx không tồn tại. Vì vậy, hãy tạo thư mục này trước:
```bash
mkdir ./tmp/nginx
```

Chạy lại lệnh tạo container
```bash
docker container run -d -p 8088:80 --name nginx4 --mount type=bind,source=./tmp/nginx,destination=/usr/share/nginx/html nginx
```

Khi truy cập vào loại trang web Nginx tại địa chỉ `http://localhost:8088`.

Bạn sẽ thấy một lỗi 403 Forbidden. Vì chúng ta đã gán nội dung của thư mục /usr/share/nginx/html vào thư mục ./tmp/nginx nhưng trong thư mục này chưa có tệp nào.

Để giải quyết vấn đề này, hãy tạo một tệp index.html trong thư mục ./tmp/nginx:
```bash
echo "I've changed the content of this file on the host" > ./tmp/nginx/index.html
```

Sau đó reload lại trang web Nginx tại địa chỉ `http://localhost:8088`, bạn sẽ thấy nội dung đã thay đổi.

## Bài tập về nhà
Hãy tạo một Jupyter Notebook và gán folder từ máy của bạn vào container Jupyter Notebook. Sau đó bạn có thể code trên đó mà không cần phải cài đặt Jupyter Notebook trên máy của bạn.

Gợi ý: Tìm jupyter docker image trên Docker Hub và sử dụng lệnh `docker run` với tùy chọn `--mount` để gắn thư mục từ máy chủ vào container.


