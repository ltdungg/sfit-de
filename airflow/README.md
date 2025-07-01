# Kiến trúc Apache Airflow cơ bản

![alt](../static/images/airflow/img.png)

- **Scheduler**:
  - Là trái tim của Airflow, quản lý toàn bộ tasks và Dags và lên lịch cho các nhiệm vụ thất bại một cách sớm nhất
  - Khi chạy một DAG, Scheduler luôn lấy phiên bản mới nhất của DAG đó.
- **API server**: FastAPI server cung cấp UI và 3 API chính cho Airflow:
  - Một API cho workers khi chạy một task
  - Một Internal API cho Airflow UI cung cấp khả năng cập nhật động các trạng thái của DAGs và tasks
  - Một public API cho phép người dùng tương tác với Airflow https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html
- **Dag processor**
  - Chịu trách nhiệm cho việc nhận và phân tích file DAGs từ thư mục được cấu hình
- **Meta database**:
  - Lưu trữ thông tin thiết yếu về Airlow, như connections, serialized DAGs, và các XCOM information.
  - Lưu trữ lịch sử chạy DAG và nhiệm vụ bao gồm trạng thái
  - PostgreSQL là lựa chọn phổ biến nhất cho Meta database, nhưng Airflow cũng hỗ trợ SQLite và MySQL.
- **Triggerer**:
  - là một đoạn mã Python nhỏ, bất đồng bộ (asynchronous), chạy trong tiến trình riêng biệt
  - Khi một task cần chờ đợi một sự kiện, triggerer sẽ được kích hoạt để theo dõi sự kiện đó và thông báo khi sự kiện xảy ra.
  - Ví dụ: nếu một task cần chờ đợi một file được tải lên, triggerer sẽ theo dõi thư mục và thông báo khi file đó xuất hiện.
  - Bạn cần chờ bạn mình mang đồ ăn tới. Thay vì cứ ngồi ở cửa đợi (tốn thời gian), bạn nhờ người gác cổng (trigger) đứng đó. Khi đồ ăn tới, người gác cổng gọi bạn ra nhận. Trong lúc chờ, bạn có thể làm việc khác.

## Đây là những bước xảy ra khi thêm một DAG mới vào Airflow:
1. DAG được phân tích bởi Dag Processor, lưu trữ một phiên bản tuần tự hóa (tức là DAG được chuyển đổi thành một định dạng có thể lưu trữ) vào Meta Database.
2. Scheduler kiểm tra bản DAG được tuần tự hóa này đẻ xác định xem có đủ điều kiện để thực thi theo lịch trình đã xác định hay không. 
3. Khi DAG được xác định là đủ điều kiện, Scheduler sẽ cấu hình executor để quyết định cách mà task đầu tiên sẽ được thực hiện.
4. Các task tiếp theo được lên lịch trong một hàng đợi. Các workers sẽ lấy từ queue cho các nhiệm vụ nó có thể thực hiện được
5. Worker khi lấy task và chạy task đó, các thông tin về trạng thái hay XCOM sẽ được gửi về meta database thông qua API server. Nếu task cần thêm các thông tin, như là các Connections, thì worker sẽ gửi yêu cầu tới API server để lấy thông tin. Trong quá trình task chạy, worker sẽ ghi các log trực tiếp vào nơi lưu trữ logs đã được cấu hình.
6. Scheduler cần những trạng thái của task trong DAG để quyết định các task tiếp theo có thể được chạy.