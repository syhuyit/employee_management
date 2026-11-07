# CONTRACT – Bảng Chữ Ký Công Khai

> **Thay đổi chữ ký ở file này chỉ do trưởng nhóm thực hiện.**

---

## Quy tắc nghiệp vụ R1–R14

| Mã | Quy tắc | Lỗi khi vi phạm |
|----|---------|-----------------|
| R1 | Mã NV/PB: chỉ chữ+số, dài 3–10 ký tự, tự in hoa | `ValidationError` |
| R2 | Họ tên: 2–50 ký tự, chỉ chữ cái và khoảng trắng | `ValidationError` |
| R3 | Năm sinh: tuổi từ 18 đến 65 | `ValidationError` |
| R4 | `base_salary` ≥ 0; `allowance` ≥ 0; `hourly_rate` ≥ 0; `hours_worked` 0–300 | `ValidationError` |
| R5 | Lương FT = `base_salary + allowance` | – |
| R6 | Lương PT = `hours_worked * hourly_rate` | – |
| R7 | Thêm NV trùng mã | `DuplicateIdError` |
| R8 | Thêm NV vào phòng ban không tồn tại | `NotFoundError` |
| R9 | Thêm phòng ban trùng mã | `DuplicateIdError` |
| R10 | Xóa phòng ban còn nhân viên | `BusinessRuleError` |
| R11 | Chuyển sang phòng ban không tồn tại | `NotFoundError` |
| R12 | Chuyển sang đúng phòng ban hiện tại | `BusinessRuleError` |
| R13 | Tìm/sửa/xóa theo mã không tồn tại | `NotFoundError` |
| R14 | Không đổi mã NV và loại NV sau khi tạo | `ValidationError` |
