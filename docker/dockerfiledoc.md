* **`FROM`** - mọi Dockerfile đều bắt đầu bằng `FROM`. Với sự ra đời của build đa giai đoạn (multi-stage builds), bạn có thể có nhiều hơn một chỉ thị `FROM` trong một Dockerfile.
* **`COPY` vs `ADD`** - Thêm thư mục và tệp vào image Docker của bạn. (Đôi khi gây nhầm lẫn...)
* **`ENV`** - thiết lập các biến môi trường.
* **`RUN`** - cho phép chạy các câu lệnh.
* **`USER`** - khi bạn không muốn dùng quyền `root`.
* **`WORKDIR`** - thiết lập thư mục làm việc.
* **`EXPOSE`** - khai báo đúng các port của bạn.
---

### FROM

Mọi Dockerfile phải bắt đầu bằng chỉ thị `FROM` theo dạng `FROM <image>[:tag]`. Chỉ thị này sẽ thiết lập **image cơ sở** (base image) cho Dockerfile của bạn, có nghĩa là các chỉ thị tiếp theo sẽ được áp dụng trên image cơ sở này.

**Giá trị `tag` là tùy chọn**, nếu bạn không chỉ định tag, Docker sẽ sử dụng tag **`latest`** và sẽ cố gắng sử dụng hoặc tải về phiên bản mới nhất của image cơ sở trong quá trình build.

Ở một cấp độ nâng cao hơn một chút, hãy lưu ý những điều sau:

* Có một chỉ thị bạn có thể đặt trước `FROM` trong Dockerfile của mình. Đó là **`ARG`**. `ARG` được sử dụng để chỉ định các đối số cho lệnh `docker build` với cờ **`--build-arg <varname>=<value>`**.
* Bạn có thể có nhiều hơn một chỉ thị `FROM` trong Dockerfile. Bạn sẽ muốn sử dụng tính năng này, ví dụ, khi bạn dùng một image cơ sở để build ứng dụng và một image cơ sở khác để chạy nó.
* Đây được gọi là **build đa giai đoạn** (multi-stage build).

Đây là lý do tại sao mỗi phần bắt đầu bằng `FROM` trong Dockerfile của bạn được gọi là một **giai đoạn build** (build stage) (ngay cả trong trường hợp đơn giản chỉ có một chỉ thị `FROM`). Bạn có thể chỉ định tên của giai đoạn build theo dạng `FROM <image>[:tag] [AS <name>]`.

---

### COPY vs ADD

Cả `ADD` và `COPY` đều được thiết kế để thêm thư mục và tệp vào image Docker của bạn theo dạng `ADD <src>... <dest>` hoặc `COPY <src>... <dest>`. Hầu hết các tài liệu đều **khuyên dùng `COPY`**.

Lý do đằng sau điều này là `ADD` có các tính năng bổ sung so với `COPY`, khiến `ADD` trở nên khó đoán hơn và có phần được thiết kế quá mức cần thiết. `ADD` có thể tải tệp từ các nguồn URL, điều mà `COPY` không thể làm được. `ADD` cũng có thể giải nén các tệp tin nén với điều kiện nó có thể nhận dạng và xử lý định dạng đó. Bạn không thể giải nén các file lưu trữ bằng `COPY`.

Chỉ thị `ADD` được thêm vào Docker trước, và `COPY` được thêm vào sau để cung cấp một giải pháp đơn giản, vững chắc cho việc sao chép tệp và thư mục vào hệ thống tệp của container.

Nếu bạn muốn tải tệp từ web vào image của mình, tôi khuyên bạn nên sử dụng `RUN` và `curl`, sau đó giải nén tệp bằng `RUN` và các lệnh bạn thường dùng trên dòng lệnh.

---

### ENV

`ENV` được sử dụng để định nghĩa các biến môi trường. Điều thú vị về `ENV` là nó thực hiện hai việc:

* Bạn có thể dùng nó để định nghĩa các biến môi trường sẽ có sẵn trong container của bạn. Vì vậy, khi bạn build một image và khởi động một container từ image đó, bạn sẽ thấy biến môi trường có sẵn và được đặt thành giá trị bạn đã chỉ định trong Dockerfile.
* Bạn có thể sử dụng các biến mà bạn chỉ định bằng `ENV` ngay trong chính Dockerfile. Do đó, trong các chỉ thị tiếp theo, biến môi trường đó sẽ có sẵn.

---

### RUN

`RUN` sẽ thực thi các câu lệnh, vì vậy nó là một trong những chỉ thị được sử dụng nhiều nhất. Tôi muốn nhấn mạnh hai điểm:

* Bạn sẽ sử dụng rất nhiều lệnh kiểu `apt-get` để thêm các gói mới vào image của mình. Luôn luôn nên **đặt các lệnh `apt-get update` và `apt-get install` trên cùng một dòng**. Điều này quan trọng vì cơ chế cache theo layer (layer caching). Việc đặt chúng trên hai dòng riêng biệt có nghĩa là nếu bạn thêm một gói mới vào danh sách cài đặt, layer chứa `apt-get update` sẽ không bị vô hiệu hóa trong bộ đệm cache và bạn có thể gặp rắc rối.
* `RUN` có hai dạng: `RUN <command>` (gọi là dạng shell) và `RUN ["executable", "param1", "param2"]` (gọi là dạng exec). Xin lưu ý rằng `RUN <command>` sẽ tự động gọi một shell (mặc định là `/bin/sh -c`), trong khi dạng exec sẽ không gọi shell lệnh.

---

### USER

Đừng chạy ứng dụng của bạn với quyền `root`, hãy sử dụng chỉ thị `USER` để chỉ định người dùng. Người dùng này sẽ được sử dụng để chạy bất kỳ chỉ thị `RUN`, `CMD` và `ENDPOINT` nào sau đó trong Dockerfile của bạn.

---

### WORKDIR

Một cách rất tiện lợi để định nghĩa thư mục làm việc, nó sẽ được sử dụng với các chỉ thị `RUN`, `CMD`, `ENTRYPOINT`, `COPY` và `ADD` tiếp theo. Bạn có thể chỉ định `WORKDIR` nhiều lần trong một Dockerfile.

**Nếu thư mục không tồn tại, Docker sẽ tự động tạo nó cho bạn.**

---

### EXPOSE

Một chỉ thị quan trọng để thông báo cho người dùng của bạn về các port mà ứng dụng của bạn đang lắng nghe. **`EXPOSE` sẽ không công bố (publish) port**, bạn cần sử dụng `docker run -p...` để làm điều đó khi bạn khởi động container.

---

### CMD và ENTRYPOINT

`CMD` là chỉ thị để chỉ định thành phần nào sẽ được chạy bởi image của bạn cùng với các đối số theo dạng sau: `CMD ["executable", "param1", "param2"...]`.

Bạn có thể ghi đè `CMD` khi khởi động container bằng cách chỉ định lệnh của bạn sau tên image như thế này: `$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]`.

Bạn chỉ có thể chỉ định một `CMD` trong một Dockerfile (về mặt kỹ thuật, bạn có thể chỉ định nhiều hơn một, nhưng chỉ có cái cuối cùng được sử dụng).

Vậy `ENTRYPOINT` có gì đặc biệt? Khi bạn chỉ định một điểm vào (entry point), image của bạn sẽ hoạt động hơi khác một chút. Bạn sử dụng `ENTRYPOINT` như là **tệp thực thi chính của image**. Trong trường hợp này, bất cứ điều gì bạn chỉ định trong `CMD` sẽ được thêm vào `ENTRYPOINT` dưới dạng tham số.