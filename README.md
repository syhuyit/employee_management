# Quản Lý Nhân Viên – Employee Management

Ứng dụng quản lý nhân viên bằng Python, sử dụng lập trình hướng đối tượng (OOP), chạy menu trên Console.

**Môn học:** Lập trình Python – INT13162  
**Nhóm 1 – Đề tài 01**

---

## Yêu cầu

- Python ≥ 3.10
- Không cần cài thêm thư viện ngoài

---

## Cách chạy

```bash
# Chạy chương trình
python main.py

# Chạy với dữ liệu mẫu
python main.py --seed

# Chạy kiểm thử
python -m unittest discover -s tests -v
```

---

## Cấu trúc thư mục

```
employee_management/
├── main.py                    # Điểm vào chương trình
├── models/                    # Lớp thực thể (Employee, Department, ...)
├── services/                  # Lớp dịch vụ nghiệp vụ
├── storage/                   # Lưu trữ dữ liệu (JSON)
├── ui/                        # Giao diện console (menu, handler)
├── utils/                     # Tiện ích dùng chung
├── tests/                     # Kiểm thử tự động
├── data/                      # Dữ liệu JSON (không commit)
└── docs/                      # Tài liệu, UML, báo cáo
```

---

## Chức năng menu

| Số | Chức năng |
|----|-----------|
| 1  | Thêm nhân viên |
| 2  | Cập nhật nhân viên |
| 3  | Xóa nhân viên |
| 4  | Hiển thị danh sách nhân viên |
| 5  | Tìm kiếm nhân viên |
| 6  | Sắp xếp nhân viên |
| 7  | Quản lý phòng ban |
| 8  | Chuyển phòng ban |
| 9  | Thống kê - báo cáo |
| 10 | Lưu dữ liệu ra file |
| 11 | Tải dữ liệu từ file |
| 12 | Chức năng mở rộng |
| 0  | Thoát chương trình |

---

## Tài liệu

- [CONTRACT.md](docs/CONTRACT.md) – Bảng contract lớp/hàm công khai
- [OWNERSHIP.md](docs/OWNERSHIP.md) – Bảng phân công file
- [CONTRIBUTING.md](CONTRIBUTING.md) – Hướng dẫn đóng góp

---

## Thành viên nhóm

| Họ tên | MSSV | Gói | GitHub |
|--------|------|-----|--------|
| _(để trống)_ | | | |
| _(để trống)_ | | | |
| _(để trống)_ | | | |
| _(để trống)_ | | | |
| _(để trống)_ | | | |
| _(để trống)_ | | | |
