# Báo cáo phần C – Quản lý nhân viên (CRUD) và Giao diện

**Người phụ trách:** Phạm Hải  
**Nhánh:** `feature/c-crud`

---

## 1. Lý do tách biệt `EmployeeManager` khỏi `Employee`

Trong thiết kế hướng đối tượng (OOP) và kiến trúc phần mềm, việc phân tách `EmployeeManager` và `Employee` mang lại các lợi ích quan trọng:

1. **Nguyên lý đơn trách nhiệm (Single Responsibility Principle - SRP):**
   - Lớp `Employee` (Entity/Model) chỉ chịu trách nhiệm đại diện cho dữ liệu của một nhân viên duy nhất và các hành vi gắn liền với chính nhân viên đó (tính lương của bản thân, chuyển đổi dict, hiển thị thông tin cá nhân).
   - Lớp `EmployeeManager` (Service/Controller) chịu trách nhiệm quản lý tập hợp các nhân viên (thêm mới, tìm kiếm, cập nhật, xóa, thống kê, kiểm soát tính duy nhất của mã nhân viên và kiểm tra ràng buộc phòng ban).

2. **Khả năng mở rộng và bảo trì (Maintainability & Extensibility):**
   - Nếu để lớp `Employee` tự quản lý danh sách của nó, mỗi đối tượng `Employee` sẽ phải gánh thêm danh sách toàn bộ các nhân viên khác, gây ra sự phụ thuộc chặt (tight coupling) và lãng phí bộ nhớ.
   - Khi cần đổi cách lưu trữ danh sách (ví dụ: chuyển từ `dict` sang cơ sở dữ liệu SQL hay MongoDB), ta chỉ cần thay đổi trong `EmployeeManager` mà không làm xáo trộn lớp thực thể `Employee`.

3. **Tách biệt tầng dữ liệu và nghiệp vụ hệ thống:**
   - `EmployeeManager` có thể phối hợp với các dịch vụ khác như `DepartmentService` để kiểm tra sự tồn tại của phòng ban (`R8`), ủy quyền tìm kiếm cho `SearchService`, sắp xếp cho `SortService` một cách độc lập và trong sáng.

---

## 2. Mô tả luồng nghiệp vụ Thêm / Sửa / Xóa nhân viên

### 2.1. Luồng Thêm mới nhân viên (`handle_add` & `add_employee`)
- **Chọn loại nhân viên:** Người dùng chọn thêm nhân viên Toàn thời gian (`FullTime`) hoặc Bán thời gian (`PartTime`).
- **Kiểm tra tức thì (On-the-fly Validation):**
  - Nhập từng trường thông tin (`Mã NV`, `Họ tên`, `Năm sinh`, `Mã phòng ban`...).
  - Áp dụng hàm phụ `_ask(prompt, validator)`: Nếu sai định dạng (ví dụ mã sai định dạng, năm sinh không hợp lệ hoặc lương âm), hệ thống in lỗi và **yêu cầu nhập lại ngay tại trường đó**.
  - Nếu mã nhân viên đã tồn tại (`R7`) hoặc mã phòng ban hợp lệ về định dạng nhưng không tồn tại (`R8`), hệ thống báo lỗi và quay lại menu thêm nhân viên.
  - `EmployeeManager.add_employee` luôn kiểm tra phòng ban bằng `DepartmentService.exists(...)`; danh mục phòng ban rỗng cũng không cho phép thêm nhân viên tham chiếu tới phòng không tồn tại.
- **Khởi tạo và lưu:** Tạo đối tượng `FullTimeEmployee` hoặc `PartTimeEmployee`, sau đó gọi `ctx.employee_manager.add_employee(new_emp)` và in thông báo thành công.

### 2.2. Luồng Cập nhật nhân viên (`handle_update` & `update_employee`)
- **Tra cứu nhân viên:** Nhập mã nhân viên cần sửa ➔ Gọi `find_employee(emp_id)`. Nếu không thấy, báo lỗi `NotFoundError` và quay lại.
- **Hiển thị thông tin hiện tại:** In chi tiết thông tin nhân viên để người dùng nắm rõ.
- **Chọn trường muốn cập nhật:** Menu hiển thị các trường được phép sửa tùy theo loại nhân viên:
  - Chung: `Họ tên`, `Năm sinh`, `Mã phòng ban`, `Lương cơ bản`.
  - Toàn thời gian: Có thêm trường `Phụ cấp`.
  - Bán thời gian: Có thêm trường `Số giờ làm`, `Đơn giá giờ`.
  - Cấm đổi: `employee_id`, `type` (`R14`).
- **Cơ chế "Tất cả hoặc không gì" (All-or-Nothing):**
  - Trong `EmployeeManager.update_employee`, giá trị cũ của các trường được sao lưu trước khi gán.
  - Gán lần lượt các giá trị mới qua setter.
  - Nếu bất kỳ trường nào phát sinh lỗi validate (hoặc mã phòng ban mới không tồn tại), hệ thống sẽ **khôi phục lại 100% dữ liệu ban đầu** và ném ngoại lệ, đảm bảo không có tình trạng cập nhật nửa vời gây sai lệch dữ liệu.

### 2.3. Luồng Xóa nhân viên (`handle_delete` & `delete_employee`)
- **Nhập mã:** Nhập mã nhân viên ➔ Tìm trong danh sách.
- **Hiển thị & Xác nhận:** Hiển thị thông tin nhân viên cần xóa và gọi hàm xác nhận `confirm("Bạn có chắc chắn muốn xóa nhân viên này? (y/n)")`.
- **Thực thi:**
  - Nếu người dùng chọn `y`: Gọi `delete_employee(emp_id)`, xóa khỏi `_employees` và in thông báo thành công.
  - Nếu người dùng chọn `n`: Hủy thao tác an toàn, không xóa dữ liệu.

---

## 3. Các ca kiểm thử tiêu biểu của Gói C

| Mã TC | Chức năng kiểm thử | Dữ liệu đầu vào / Thao tác | Kết quả mong đợi |
|---|---|---|---|
| **TC-C01** | Thêm nhân viên trùng mã | Thêm NV `NV001`, sau đó thêm tiếp một NV khác cũng mang mã `NV001` | Ném `DuplicateIdError`, không cho phép ghi đè mã đã có |
| **TC-C02** | Thêm NV vào phòng ban không tồn tại | Nhập mã phòng ban `PB99` (đúng định dạng nhưng chưa có trong `DepartmentService`) | Báo lỗi `NotFoundError` theo quy tắc R8 và quay lại menu thêm nhân viên |
| **TC-C03** | Cập nhật trường bị cấm | Gọi `update_employee("NV001", type="PartTime")` hoặc trường không hợp lệ | Ném `ValidationError`, bảo đảm quy tắc bất biến R14 |
| **TC-C04** | Cập nhật "Tất cả hoặc không gì" | Cập nhật `full_name="Tên Mới"` (hợp lệ) và `base_salary=-5000` (lương âm, lỗi) | Ném `ValidationError`, đồng thời `full_name` được khôi phục về tên cũ |
| **TC-C05** | Xóa nhân viên không tồn tại | Gọi `delete_employee("NV999")` khi mã không có trong hệ thống | Ném `NotFoundError`, danh sách không bị thay đổi |
| **TC-C06** | Tính đóng gói danh sách `get_all` | Lấy danh sách qua `get_all()`, sau đó gọi `clear()` trên danh sách nhận được | Danh sách nội bộ của `EmployeeManager` vẫn giữ nguyên toàn bộ nhân viên |
| **TC-C07** | Thêm khi danh mục phòng ban rỗng | Tạo `EmployeeManager` với `DepartmentService` rỗng rồi thêm nhân viên | Ném `NotFoundError`; không thêm nhân viên vào danh sách |
| **TC-C08** | Kiểm tra luồng nhập khi thêm | Nhập mã sai định dạng rồi nhập đúng; thử mã NV trùng hoặc mã PB không tồn tại | Mã sai định dạng được hỏi lại tại trường; mã trùng/PB không tồn tại báo lỗi rồi kết thúc thao tác thêm |

---

## 4. Hướng dẫn chạy kiểm thử

Chạy toàn bộ unit test của gói C:
```bash
python -m unittest tests.test_employee_manager -v
python -m unittest tests.test_crud_handler -v
```

Chạy kiểm thử tích hợp toàn bộ hệ thống:
```bash
python -m unittest discover -s tests -v
```

Kiểm tra giao diện thủ công với dữ liệu mẫu:
```bash
python main.py --seed
# Chọn 4: Xem danh sách nhân viên
# Chọn 1: Thử thêm nhân viên (thử nhập sai mã trùng, sai phòng ban, tuổi sai biên)
# Chọn 2: Thử sửa thông tin nhân viên
# Chọn 3: Thử xóa nhân viên (thử chọn n hủy xóa và y xác nhận xóa)
```
