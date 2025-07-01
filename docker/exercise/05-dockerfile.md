Dockerfile là một công thức cho một Docker Image. Nó bao gồm chuỗi các chỉ thị nói với Docker rằng cấu trúc của Image sẽ như thế nào.

## First Dockerfile

Tạo một folder mới để chứa Dockerfile
```bash
mkdir myimage
cd myimage
```

Và giờ tạo một file có tên là `Dockerfile` trong thư mục này. Nội dung của Dockerfile sẽ như sau:

```dockerfile
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y figlet
```

Lệnh FROM chỉ định Image cơ sở mà bạn muốn sử dụng. Trong trường hợp này, chúng ta sử dụng `ubuntu:18.04`. Mỗi lệnh RUN sẽ được thực thi trong quá trình Docker build, tất cả các câu lệnh RUN đều không có khả năng tương tác.
Tức là không thể cung cấp input trong suốt quá trình build. Đó là lý do tại soa chúng ta thêm `-y` vào lệnh `apt-get install`, để tự động xác nhận cài đặt mà không cần người dùng xác nhận.

Thực thi lệnh `docker build` để tạo Image từ Dockerfile:

```bash
docker build -t myfiglet .
```
Chú ý: `-t` là gán một tag cho Image, còn `.` là chỉ định thư mục hiện tại là nơi chứa Dockerfile.

Giờ cùng phân tích output của lệnh `docker build`:

```Sending build context to Docker daemon 2.048 kB```

- Build context là thư mục tại `.` được đưa cho docker build
  - Được gửi bởi Docker Client đến Docker Daemon
    - Cho phép sử dụng các máy chủ từ xa để xây image trên local files
  - Nên là phải cẩn thận nếu folder quá lớn và dẫn đến việc gửi quá nhiều dữ liệu không cần thiết làm cho quá trình build chậm hơn
    - Bạn có thể sử dụng file `.dockerignore` để loại trừ các file không cần thiết khỏi build context.

```
Step 2/3 : RUN apt-get update
 ---> Running in 9f07f31f5608
...(..cut RUN output..)...
Reading package lists...
Removing intermediate container 9f07f31f5608
 ---> e2ed94338e24
```

Một container `9f07f31f5608` được tạo ra từ base image, 
- Câu lệnh RUN được thực thi trong container này
- Container được commit thành một image mới `e2ed94338e24`
- Container này sẽ bị xóa đi
- Và output từ bước này là base image của các bước tiếp theo

#### Tips:
Sau mỗi bước build này, Docker sẽ tạo một snapshot cho image kết quả trước khi thực hiện bước tiếp theo. Docker kiểm tra nếu nó đã được xây dựng với cùng một trình tự.

Docker sử dụng chính xác cái chuỗi mà bạn định nghĩa bên trong Dockerfile, tức là ví dụ 2 lệnh này sẽ khác hoàn toàn nhau
```dockerfile
RUN apt-get install figlet cowsay

RUN apt-get install cowsay figlet
```
Bạn có thể buộc Docker build lại bằng cách sử dụng tùy chọn `--no-cache`:

Giờ ta sẽ chạy image
```bash
docker run -ti myfiglet  bash
```

Và giờ bạn có thể sử dụng `figlet` trong container này. Ví dụ:
```bash
figlet "Hello, Docker!"
```

