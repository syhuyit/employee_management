# BẢNG PHÂN CÔNG QUYỀN SỞ HỮU FILE (OWNERSHIP MATRIX)

> **Nguyên tắc vàng:** "Một file một chủ" – Chỉ chủ sở hữu mới được phép sửa file của mình trên nhánh tính năng tương ứng. Muốn sửa file người khác, hãy tạo GitHub Issue gửi người phụ trách hoặc Trưởng nhóm.

---

## 1. Bảng phân công chi tiết theo thành viên

| Gói | Nội dung công việc | Người phụ trách | Nhánh Git | Danh sách file sở hữu |
|:---:|---|---|---|---|
| **Lead & F** | Trưởng nhóm, kiến trúc, review PR, UML, báo cáo, test cases | **Nguyễn Sỹ Huy** | `feature/f-docs` | `main.py`, `ui/menu.py`, `ui/context.py`, `ui/handlers/_common.py`, `utils/exceptions.py`, `utils/sample_data.py`, `README.md`, `CONTRIBUTING.md`, `requirements.txt`, `.gitignore`, `.github/**`, mọi `__init__.py`, `docs/CONTRACT.md`, `docs/OWNERSHIP.md`, `docs/uml/**`, `docs/report/**`, `docs/screenshots/**`, `docs/test_cases.md`, `tests/test_smoke.py` |
| **A** | Models nhân viên & Bộ kiểm tra dữ liệu | **Nông Quang Vinh** | `feature/a-models` | `models/employee.py`, `models/fulltime.py`, `models/parttime.py`, `models/factory.py`, `utils/validators.py`, `tests/test_models.py`, `tests/test_validators.py`, `docs/report/part_A.md` |
| **B** | Phòng ban & Nghiệp vụ chuyển phòng ban | **Mạnh Thảo** | `feature/b-department` | `models/department.py`, `services/department_service.py`, `ui/handlers/department_handler.py`, `tests/test_department.py`, `docs/report/part_B.md` |
| **C** | Quản trị nhân viên (CRUD) & Nhập liệu | **Phạm Hải** | `feature/c-crud` | `services/employee_manager.py`, `ui/handlers/crud_handler.py`, `utils/input_helper.py`, `tests/test_employee_manager.py`, `docs/report/part_C.md` |
| **D** | Tìm kiếm, Sắp xếp & Hiển thị bảng | **Minh Dương** | `feature/d-search-sort` | `services/search_service.py`, `services/sort_service.py`, `utils/formatter.py`, `ui/handlers/search_sort_handler.py`, `tests/test_search_sort.py`, `docs/report/part_D.md` |
| **E** | Thống kê, Lưu trữ JSON & Chức năng mở rộng | **Phạm Quang Đạt** | `feature/e-report-extension` | `services/report_service.py`, `storage/file_storage.py`, `ui/handlers/report_handler.py`, `ui/handlers/extension_handler.py`, `tests/test_report.py`, `tests/test_storage.py`, `docs/report/part_E.md` |

---

## 2. Quy tắc phụ thuộc và tương tác giữa các gói

1. **Giao tiếp qua Hợp đồng (Contract):** Các gói chỉ gọi hàm của nhau dựa trên chữ ký đã chốt trong `docs/CONTRACT.md`.
2. **Không import chéo giữa các service:** `services/*` không import lẫn nhau (ngoại lệ duy nhất: `EmployeeManager` sử dụng `DepartmentService`, `SearchService`, `SortService`, `ReportService` như đã thiết kế).
3. **Phân tầng nghiêm ngặt:** Chỉ có thư mục `ui/` và `utils/input_helper.py` được phép gọi `print()` và `input()`.
4. **Quy trình khi cần đổi chữ ký hàm:** Mở GitHub Issue gửi Trưởng nhóm (Nguyễn Sỹ Huy), không tự ý sửa đổi chữ ký đã công bố.
