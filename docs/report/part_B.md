# Gói B – Quản lý phòng ban và chuyển phòng ban

**Người phụ trách:** Nguyễn Mạnh Thảo  
**Nhánh:** `feature/b-department`

## 1. Phạm vi

| Thành phần | File | Chức năng |
|---|---|---|
| Thực thể phòng ban | `models/department.py` | Lưu mã, tên phòng ban; kiểm tra tên; chuyển đổi dữ liệu sang/từ dict |
| Dịch vụ phòng ban | `services/department_service.py` | Thêm, tìm, đổi tên, xóa phòng ban và chuyển nhân viên |
| Giao diện console | `ui/handlers/department_handler.py` | Menu quản lý phòng ban và luồng chuyển nhân viên |
| Kiểm thử | `tests/test_department.py` | Chưa có file kiểm thử riêng cho nghiệp vụ Gói B |

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

## 5. Rà soát mã nguồn

Các mã mục **B3, B5, B6, B7** chưa được định nghĩa trong tài liệu hiện có của repository. Phần rà soát dưới đây bao quát các nghiệp vụ Gói B đang có trong mã nguồn; cần đối chiếu với bảng phân công nếu các mã trên có ý nghĩa riêng.

### 5.1. Đổi tên phòng ban

`update_department()` tìm phòng ban bằng `get_department()`, nên mã sai định dạng hoặc không tồn tại được báo lỗi. Tên mới được kiểm tra qua setter của `Department`. Phòng ban đã cập nhật được trả về để giao diện hiển thị.

### 5.2. Xóa phòng ban

`delete_department()` kiểm tra mã phòng ban trước, sau đó so khớp mã phòng ban của nhân viên. Nếu còn nhân viên thì ném `BusinessRuleError`; nếu không thì xóa và trả về phòng ban. Handler truyền danh sách nhân viên hiện tại từ `EmployeeManager`.

### 5.3. Chuyển nhân viên

`transfer_employee()` dùng `get_department()` để xác nhận phòng đích tồn tại, từ chối trường hợp phòng đích trùng phòng hiện tại, rồi cập nhật thuộc tính `department_id`. Handler tìm nhân viên qua `EmployeeManager.find_employee()` và hiển thị thông tin phòng ban trước khi nhận mã đích.

### 5.4. Giao diện quản lý

Handler có các luồng xem, thêm, đổi tên và xóa phòng ban; lỗi nghiệp vụ được bắt và hiển thị để menu không bị dừng. Luồng chuyển phòng ban xử lý trường hợp danh sách nhân viên rỗng và hiển thị lỗi khi mã nhân viên hoặc phòng đích không hợp lệ.

## 6. Kiểm thử và điểm cần bổ sung

`tests/test_smoke.py` hiện kiểm tra khứ hồi dữ liệu của `Department`, nhưng chưa kiểm tra các nghiệp vụ trong `DepartmentService`. Repository chưa có `tests/test_department.py`; nên bổ sung ca cho mã phòng ban trùng, đổi tên hợp lệ/không hợp lệ, xóa phòng ban đang có nhân viên, xóa phòng trống, chuyển tới phòng không tồn tại, chuyển về phòng hiện tại và chuyển thành công.

Kiểm thử tự động chưa được chạy trong lần rà soát này.
