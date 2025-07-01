# Apache Iceberg Lakehouse

## The Data Layer
Đây là lớp mà dữ liệu thực tế được lưu trữ cho một bảng

Bao gồm các định dạng dữ liệu như Parquet, ORC, Avro...

Đây là nơi dữ liệu thô cho các truy vấn được đặt.

Lưu trữ các delete files để xử lý cho việc xóa dữ liệu mà không cần chỉnh sửa file gốc.

Dữ liệu có thể được lưu trữ dưới các hệ thống lưu trữ chi phí thấp bằng cách sử dụng các hệ thống lưu trữ phân tán như:
- Hadoop Distributed File System (HDFS)
- Amazon S3
- Azure Data Lake Storage (ADLS)
- Google Cloud Storage (GCS)

## Metadata Layer
Thay vì sắp xếp các bảng vào các thư mục riêng lẻ, Iceberg duy trì một danh sách các files. 

Metadata Layer này quản lý các snapshot của bảng, lược đồ và các dữ liệu thống kê về tập tin.

- **Manifest file**: Nó theo dõi từng data files và delete files. Cung cấp thống kê, bao gồm một phạm vi dữ liệu của một cột giúp cho việc truy vấn dữ liệu bằng cách giảm số lượng file không liên quan cần phải quét.
- **Manifest list**: Một danh sách các manifest file làm nên một snapshot cụ thể của một bảng Iceberg tại một thời điểm. Nó cũng tóm tắt dữ liệu trong các manifest file như là các phân vùng phạm vi và các thống kê cho các cột, cho phép các công cụ truy vấn xác định file nào có liên quan.
- **Metadata file**: Phía trên cùng là metadata file, nó theo dõi trạng thái của bảng. Nó lưu trữ thông tin toàn bảng như là lược đồ, các phân vùng, và các con trỏ tới các snapshots. Iceberg hỗ trợ time travel (du hành thời gian) thông qua các snapshots của bảng trong quá khứ có thể truy cập bằng manifest list trỏ đến các manifests files đại diện cho phiên bản cũ hơn của bảng.

## The Iceberg Catalog
Catalog là nơi lưu trữ trung tâm quản lý các bảng Iceberg. Cung cấp một điểm truy cập duy nhất để khám phá và quản lý các bảng, đảm bảo tính nhất quán và cho phép tuân thủ ACID.

Bằng cách cung cấp một con trỏ tới file metadata hiện tại của bảng. Khi cập nhật metadata của bảng, catalog đảm bảo thay đổi được cam kết trước khi phơi bày cho các người dùng khác, cho phép các cập nhật nguyên tử (atomic)

Catalog tạo điều kiện để khám phá các bảng, tạo và sửa đổi bảng và đảm bảo tính nhất quán của giao dịch.

Bằng cách cung cấp một cách tiêu chuẩn để tương tác với các bảng Iceberg hỗ trợ nhiều hệ thống lưu trữ phân tán và các công cụ xử lý dữ liệu khác nhau.

Iceberg hỗ trợ nhiều loại catalog khác nhau (open source và thương mại), bao gồm: Iceberg REST catalog, AWS Glue Data Catalog, Apache Polaris, Hive Metastore.

## Ví dụ 
**Tạo một bảng mới**:
- Tạo một metadata file mới cho bảng.
- Tạo một tham chiếu tới metadata file trong catalog.

**Chèn dữ liệu vào một bảng (bottom-up)**
- Tạo một data file mới
- Tạo một manifest file trỏ tới data file này
- Tạo manifest list trỏ tới manifest file này
- Tạo một metadata file mới với cả snapshot cũ cũng như là snapshot mới của bảng của bảng có chèn dữ liệu trỏ tới manifest list.
- Cập nhật catalog tham chiếu tới metadata file mới nhất. Catalog chỉ được cập nhật khi giao dịch hoàn thành.

**Truy xuất từ một bảng (top-down)**
- Lấy metadata file mới nhất từ Catalog Layer.
- Sử dụng các file thống kê và địa chỉ để tối ưu kế hoạch truy vấn.
- Nhận những files cần thiết từ Data Layer cho truy vấn