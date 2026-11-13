# Báo cáo phần A – Mô hình nhân viên và OOP

## 1. Sơ đồ kế thừa

```text
                         Employee (ABC)
                         /            \
                        /              \
        FullTimeEmployee              PartTimeEmployee
        - allowance                   - hours_worked
        - base_salary + allowance     - hourly_rate
                                       - hours_worked * hourly_rate
```

`Employee` kế thừa `ABC` và khai báo trừu tượng `employee_type` cùng
`calculate_salary()`. Không thể tạo trực tiếp một `Employee` vì lớp này chưa
xác định loại nhân viên cụ thể và công thức tính lương tương ứng. Hai lớp con
phải cung cấp loại nhân viên và cách tính lương riêng, đồng thời dùng chung
các trường và hành vi cơ bản như mã nhân viên, họ tên, năm sinh, phòng ban,
kiểm tra dữ liệu và chuyển đổi sang dict.

## 2. Minh chứng các tính chất OOP

| Tính chất | Minh chứng trong mã nguồn |
|---|---|
| **Kế thừa** | `FullTimeEmployee` và `PartTimeEmployee` kế thừa `Employee`; gọi `super().__init__()` để khởi tạo các thông tin chung và tái sử dụng `to_dict()`. Mỗi lớp chỉ bổ sung dữ liệu đặc thù của mình. |
| **Đóng gói** | Dữ liệu được lưu trong thuộc tính private như `__employee_id`, `__full_name`, `__allowance`, `__hours_worked`. Các thuộc tính được truy cập qua property/setter để kiểm tra dữ liệu. `employee_id` chỉ có getter nên không thể đổi qua giao diện thuộc tính thông thường. |
| **Đa hình** | `Employee` định nghĩa hợp đồng `calculate_salary()` và `employee_type`; mỗi lớp con triển khai riêng. Cùng lời gọi `calculate_salary()` cho kết quả theo công thức toàn thời gian (`base_salary + allowance`) hoặc bán thời gian (`hours_worked * hourly_rate`). `Employee.__str__()` cũng gọi phương thức tính lương của đối tượng cụ thể. |

## 3. Tổng hợp luật validate dữ liệu

Các validator ném `ValidationError` khi dữ liệu không hợp lệ. Riêng các luật
kiểm tra số, giá trị được chuyển thành `float` nếu có thể; boolean, số không
hữu hạn hoặc giá trị ngoài giới hạn đều bị từ chối.

| Dữ liệu | Luật kiểm tra |
|---|---|
| Trường bắt buộc (`validate_not_empty`) | Không nhận `None` hoặc chuỗi rỗng/chỉ có khoảng trắng; loại bỏ khoảng trắng ở hai đầu. |
| Mã nhân viên/phòng ban (`validate_identifier`) | Sau khi bỏ khoảng trắng đầu/cuối, chuyển thành chữ hoa; chỉ gồm chữ cái A–Z và chữ số 0–9; dài 3–10 ký tự; không chấp nhận dấu cách bên trong hoặc dấu gạch nối. |
| Họ tên (`validate_full_name`) | Thu gọn khoảng trắng liên tiếp; dài 2–50 ký tự; chỉ gồm chữ cái và khoảng trắng. |
| Tên phòng ban (`validate_department_name`) | Không rỗng, thu gọn khoảng trắng; dài 2–50 ký tự. |
| Năm sinh (`validate_birth_year`) | Phải là số nguyên, không nhận boolean; tuổi tính theo năm hiện tại phải từ 18 đến 65. |
| Lương cơ bản, phụ cấp, đơn giá giờ (`validate_non_negative`) | Phải là số hữu hạn và không âm. |
| Số giờ làm (`validate_hours_worked`) | Phải là số hữu hạn trong khoảng từ 0 đến 300, bao gồm cả hai biên. |

## 4. Một số ca kiểm thử đại diện

| Ca kiểm thử | Dữ liệu/hành động | Kết quả mong đợi |
|---|---|---|
| `test_employee_cannot_be_instantiated` | Thử tạo trực tiếp `Employee`. | Ném `TypeError` vì đây là lớp trừu tượng. |
| `test_fulltime_salary_calculation` | Lương cơ bản 15.000.000 và phụ cấp 2.000.000. | `calculate_salary()` trả về 17.000.000; chuỗi hiển thị có phụ cấp. |
| `test_parttime_salary_calculation` | Làm 40 giờ với đơn giá 200.000/giờ. | `calculate_salary()` trả về 8.000.000; chuỗi hiển thị số giờ và đơn giá. |
| `test_setters_validation_errors` | Gán năm sinh tương ứng tuổi 17, họ tên sai định dạng, lương âm hoặc mã phòng ban không hợp lệ. | Các setter tương ứng ném `ValidationError`; mã nhân viên chỉ đọc. |
| `test_fulltime_dict_roundtrip` | Chuyển nhân viên toàn thời gian sang dict rồi dựng lại qua factory. | Đối tượng khôi phục là `FullTimeEmployee` và có cùng mức lương. |

Các ca trên được cài đặt trong `tests/test_models.py`.
