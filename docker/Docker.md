## Các khái niệm chính
- Isolation: Điều này là cực kỳ quan trọng. Hãy hình dung bạn có nhiều ứng dụng chạy trên cùng một máy chủ. Nếu không có isolation, một ứng dụng có thể vô tình làm hỏng hoặc can thiệp vào ứng dụng khác, hoặc thậm chí là làm sập toàn bộ hệ thống. Docker sử dụng các tính năng của kernel Linux như cgroups và namespaces để tạo ra ranh giới ảo này, đảm bảo mỗi container có "không gian" riêng của nó mà không làm ảnh hưởng đến phần còn lại.

- Portability: Đây là một trong những lợi ích lớn nhất của Docker. Câu nói "It works on my machine" (Nó chạy trên máy của tôi) không còn là vấn đề nữa. Khi bạn đóng gói ứng dụng vào container, tất cả các phụ thuộc (thư viện, cấu hình, thậm chí cả một hệ điều hành nhỏ) đều đi kèm. Vì vậy, cho dù bạn đang phát triển trên máy tính xách tay của mình, kiểm thử trên môi trường staging, hay triển khai lên production server, container sẽ chạy y hệt nhau. Điều này giúp giảm thiểu rủi ro và tăng tốc quá trình phát triển.

- Efficiency: Không giống như máy ảo (VM) phải có toàn bộ hệ điều hành riêng của nó (bao gồm cả nhân), các container chia sẻ nhân Linux của hệ thống máy chủ. Điều này làm cho container nhẹ hơn đáng kể, khởi động nhanh hơn và tiêu tốn ít tài nguyên hơn (CPU, RAM). Bạn có thể chạy nhiều container hơn trên cùng một máy chủ so với chạy nhiều máy ảo, tối ưu hóa việc sử dụng hạ tầng.

## Docker 
**Một kiến trúc client-server:**
- Nói một cách đơn giản, bạn ra lệnh cho Docker thông qua Client, và Daemon là "bộ não" thực sự làm tất cả công việc phía sau hậu trường.

**Các thành phần trong hệ sinh thái**
1. IMAGE (Hình ảnh)
- Khái niệm: Một Docker Image là một khuôn mẫu tĩnh, chỉ đọc, chứa tất cả các hướng dẫn cần thiết để tạo ra một container. Nó bao gồm mã ứng dụng, thư viện, công cụ hệ thống, và các thiết lập cần thiết khác. Image giống như một bản thiết kế hoặc một "snapshot" của một ứng dụng và môi trường của nó.

2. CONTAINER (Bộ chứa)
- Khái niệm: Một Container là một phiên bản đang chạy (run-time instance) của một Docker Image. Bạn có thể hình dung Image là bản thiết kế của một ngôi nhà, thì Container chính là ngôi nhà đã được xây dựng và đang hoạt động. Một Image có thể tạo ra nhiều Container.

3. IMAGE REGISTRY (Kho lưu trữ hình ảnh)
- Khái niệm: Image Registry là một dịch vụ lưu trữ tập trung cho các Docker Image. Các Registry công khai phổ biến nhất là Docker Hub, nhưng cũng có các Registry riêng tư. Chúng cho phép bạn lưu trữ, quản lý và chia sẻ các Image của mình.

**Tóm tắt quy trình:**
1. Bạn xây dựng (docker build) một Image từ mã nguồn và Dockerfile của mình.
2. Bạn có thể đẩy (docker push) Image này lên một Image Registry để lưu trữ và chia sẻ.
3. Người khác (hoặc chính bạn) có thể kéo (docker pull) Image đó từ Registry về máy cục bộ.
4. Sau đó, bạn chạy (docker run) Image đó để tạo ra một Container đang hoạt động.

Đây là một vòng lặp liên tục trong quá trình phát triển và triển khai ứng dụng với Docker.

## Kiến trúc Docker
Chia thành ba thành phần chính: Docker Client, Docker Host, và Docker Registry.

1. Docker Client (Máy khách Docker)
- Đây là giao diện chính mà người dùng tương tác với Docker. Khi bạn gõ các lệnh như docker build, docker pull, hoặc docker run vào terminal của mình, bạn đang sử dụng Docker Client. Client sẽ gửi các lệnh này tới Docker Daemon.
- Các lệnh chính
  - Docker build: Dùng để xây dựng một Docker Image từ một Dockerfile.
  - Docker pull: Dùng để tải một Docker Image từ Docker Registry về Docker Host.
  - Docker run: Dùng để khởi chạy một Container từ một Docker Image.

2.  Docker Host (Máy chủ Docker)
- Chức năng: Đây là nơi Docker Daemon chạy và quản lý tất cả các đối tượng Docker: Images, Containers, Networks, và Volumes.
- Các thành phần bên trong Docker Host:
  - Daemon (Tiến trình nền): Đây là "bộ não" của Docker. Docker Daemon (thường là dockerd) lắng nghe các yêu cầu từ Docker Client và quản lý các đối tượng Docker. Nó thực hiện tất cả các công việc nặng nhọc như xây dựng, kéo, chạy, và quản lý các Container.
  - Images (Hình ảnh): Các Docker Image được lưu trữ trên Docker Host. Đây là các khuôn mẫu chỉ đọc dùng để tạo ra các Container. Ví dụ trong sơ đồ có Image Ubuntu, NGINX.
  - Containers (Bộ chứa): Các Container đang chạy được quản lý bởi Docker Daemon trên Docker Host. Mỗi Container là một thể hiện độc lập, biệt lập của một Image.

3. Docker Registry (Kho lưu trữ Docker)
- Chức năng: Đây là nơi lưu trữ tập trung các Docker Image. Docker Hub là Registry công khai lớn nhất, nhưng bạn cũng có thể có các Registry riêng tư. Registry cho phép bạn lưu trữ và chia sẻ các Image của mình với người khác hoặc giữa các môi trường khác nhau.

