# Quản lý Image

## Tạo Image và thay đổi một số thứ

```bash
docker run -it ubuntu:18.04
```

Chạy apt-get update để làm mới danh sách các gói cài đặt có sẵn. Trong phần này ta sẽ sử dụng `figlet`

Figlet là một chương trình dùng để tạo chữ nghệ thuật ASCII.

```bash
apt-get update && apt-get install -y figlet
```
## Kiểm tra sự khác nhau với Image gốc
Sau khi cài đặt xong, ta sẽ thoát container bằng lệnh `exit`. Bây giờ ta sẽ kiểm tra sự khác nhau giữa Image gốc và Image mới tạo ra.

```bash
docker diff <container_id>
```

Output: 

```
C /root
A /root/.bash_history
C /etc
A /etc/emacs
A /etc/emacs/site-start.d
A /etc/emacs/site-start.d/50figlet.el
C /etc/alternatives
A /etc/alternatives/figlet
C /usr
C /usr/share****
A /usr/share/figlet
A /usr/share/figlet/646-ca.flc
A /usr/share/figlet/646-ca2.flc
A /usr/share/figlet/646-hu.flc  
```

**Tip:**
> Nếu cần phải sử dụng container ID, bạn có thể sử dụng lệnh `docker ps -a` để liệt kê tất cả các container và tìm ID của container mà bạn muốn.

> Các loại thay đổi theo dõi bởi lệnh `docker diff`: `A` một file hoặc thư mục được thêm, `C` một file hoặc thư mục đã thay đổi, `D` một file hoặc thư mục đã bị xóa.

## Commit thay đổi và sử dụng Image 

Commit là một lệnh dùng để lưu lại các thay đổi của container thành một Image mới. Bạn có thể sử dụng lệnh `docker commit` để tạo một Image mới từ container hiện tại.

Giờ bước cuối là ta sẽ commit các thay đổi này, tức là sẽ tạo một layer với sự thay đổi ta đã làm trước đó, và một image mới sử dụng layer mới này.

```bash
docker commit <container_id> interactivefiglet
```

Giờ ta đã tạo image mới thành công, chạy và kiểm tra xem nó có hoạt động không:

```bash
docker run -it interactivefiglet
```

Giờ bạn có thể sử dụng `figlet` trong container này. Ví dụ:

```bash
figlet ciao ciao 
```

Nếu muốn chỉ sử dụng 1 lệnh để chạy ta có thể sử dụng lệnh thay thế sau

```bash
docker run -it interactivefiglet figlet ciao ciao
```
