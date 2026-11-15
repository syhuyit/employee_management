# Gói B – Quản lý phòng ban và chuyển phòng ban

**Người phụ trách:** Nguyễn Mạnh Thảo  
**Nhánh:** `feature/b-department`

## 1. Phạm vi

| Thành phần | File | Chức năng |
|---|---|---|
| Thực thể phòng ban | `models/department.py` | Lưu mã, tên phòng ban; kiểm tra tên; chuyển đổi dữ liệu sang/từ dict |
| Dịch vụ phòng ban | `services/department_service.py` | Thêm, tìm, đổi tên, xóa phòng ban và chuyển nhân viên |
| Giao diện console | `ui/handlers/department_handler.py` | Menu quản lý phòng ban và luồng chuyển nhân viên |
| Kiểm thử | `tests/test_department.py` | 14 unit test cho service và 7 test cho handler/menu |

## 2. Thực thể Department

`Department` giữ `department_id` ở chế độ chỉ đọc. Mã được chuẩn hóa và kiểm tra theo quy tắc R1. Tên phòng ban đi qua setter, được thu gọn khoảng trắng và phải dài từ 2 đến 50 ký tự. Hai phương thức `to_dict()` và `from_dict()` hỗ trợ lưu, tải dữ liệu.

## 3. Nghiệp vụ DepartmentService

| Nghiệp vụ | Hành vi | Quy tắc |
|---|---|---|
| Thêm phòng ban | Từ chối mã đã có trong danh sách bằng `DuplicateIdError` | R9 |
| Tìm phòng ban | Chuẩn hóa mã; không tìm thấy thì ném `NotFoundError` | — |
| Đổi tên | Tìm phòng ban rồi gán tên mới qua setter có kiểm tra | — |
| Xóa phòng ban | Chặn thao tác nếu còn nhân viên thuộc phòng ban; nếu xóa được thì trả về đối tượng đã xóa | R10 |
| Chuyển nhân viên | Phòng đích phải tồn tại; không cho chuyển sang phòng hiện tại; cập nhật `employee.department_id` khi hợp lệ | R11, R12 |

## 4. Giao diện sử dụng

- **Menu 7 – Quản lý phòng ban:** xem danh sách, thêm, đổi tên, xóa. Khi xóa, chương trình hỏi xác nhận và dịch vụ vẫn kiểm tra nhân viên đang thuộc phòng ban đó.
- **Menu 8 – Chuyển phòng ban:** hiển thị nhân viên và phòng ban, nhận mã nhân viên cùng mã phòng ban đích, sau đó báo kết quả hoặc lỗi nghiệp vụ.
- `main.py` đã khởi tạo `DepartmentService`, nạp danh sách phòng ban trước nhân viên; `ui/menu.py` đã ánh xạ lựa chọn 7 và 8 tới handler tương ứng.

## 5. Rà soát theo yêu cầu B3, B5, B6, B7

### B3 – Báo số nhân viên khi chặn xóa

`delete_department()` đếm số nhân viên có `department_id` trùng phòng ban cần xóa. Khi số lượng lớn hơn 0, dịch vụ ném `BusinessRuleError` kèm mã phòng ban và số nhân viên, ví dụ `Phòng ban PB01 còn 2 nhân viên, không thể xóa.` Danh sách phòng ban không bị thay đổi. Nếu phòng ban trống, thao tác xóa vẫn hoạt động như trước.

### B5 – Thứ tự menu và nhập lại khi sai

Menu quản lý phòng ban hiển thị theo thứ tự: **1. Thêm**, **2. Sửa tên**, **3. Xóa**, **4. Danh sách**, **0. Quay lại**. `input_choice()` tiếp tục hỏi khi lựa chọn menu không hợp lệ. Các trường mã phòng ban, tên phòng ban và mã nhân viên được kiểm tra trong vòng lặp riêng; lỗi định dạng, mã trùng hoặc không tìm thấy sẽ báo lỗi rồi hỏi lại ngay trường đó.

### B6 – Xác nhận và hiển thị rõ luồng chuyển phòng

Sau khi tìm nhân viên, handler hiển thị phòng ban nguồn rồi liệt kê phòng ban đích. Mã đích được kiểm tra trước khi hỏi xác nhận. Nếu người dùng từ chối, dịch vụ không được gọi và phòng của nhân viên giữ nguyên. Nếu xác nhận thành công, thông báo nêu rõ mã nguồn và đích, ví dụ `Đã chuyển NV001 từ PB01 sang PB02.` Mã sai định dạng, không tồn tại hoặc trùng phòng hiện tại đều được báo và hỏi lại.

### B7 – Unit test nghiệp vụ

`tests/test_department.py` có 14 test trực tiếp cho `DepartmentService`, bao gồm thêm trùng mã, tìm và sửa phòng ban, kiểm tra tên, xóa phòng trống/không tồn tại/còn nhân viên với số lượng chính xác, và các trường hợp chuyển phòng hợp lệ hoặc bị từ chối. Bảy test handler/menu kiểm tra thứ tự menu, nhập lại dữ liệu sai, xác nhận hủy không làm đổi phòng, xác nhận chuyển thành công và nhập lại phòng đích sai.

## 6. Kết quả kiểm thử

```text
python -m unittest tests.test_department -v
Ran 21 tests — OK

python -m unittest discover -s tests -v
Ran 106 tests — OK
```

## 7. Báo cáo B8

Tài liệu này tổng hợp thực thể, nghiệp vụ, mã lỗi, menu, cách xử lý nhập sai và xác nhận chuyển phòng; phần trên cũng ghi lại các ca kiểm thử cùng kết quả chạy suite.
