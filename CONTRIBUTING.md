# Hướng Dẫn Đóng Góp – CONTRIBUTING

## 1. Nguyên tắc "một file một chủ"

Mỗi file có một chủ sở hữu duy nhất (xem [OWNERSHIP.md](docs/OWNERSHIP.md)).  
**Chỉ chủ sở hữu mới được sửa file của mình.** Muốn sửa file của người khác → tạo Issue cho trưởng nhóm.

---

## 2. Quy ước nhánh

```
feature/<gói>-<tên-ngắn>
```

Ví dụ:
- `feature/a-models` – Gói A: hoàn thiện models
- `feature/b-department` – Gói B: phòng ban
- `feature/c-crud` – Gói C: CRUD nhân viên
- `feature/d-search` – Gói D: tìm kiếm, sắp xếp
- `feature/e-report` – Gói E: thống kê, lưu trữ
- `feature/f-docs` – Gói F: tài liệu, kiểm thử

---

## 3. Quy ước commit

```
feat(gói): mô tả ngắn
fix(gói): mô tả ngắn
docs: mô tả ngắn
test: mô tả ngắn
```

Ví dụ:
- `feat(c): hoàn thiện update_employee`
- `fix(a): sửa validate_full_name với ký tự đặc biệt`
- `test(b): thêm test cho delete_department`

---

## 4. Quy trình làm việc

```bash
# 1. Cập nhật main
git checkout main
git pull

# 2. Tạo nhánh mới
git checkout -b feature/<gói>-<tên-ngắn>

# 3. Code và commit thường xuyên
git add .
git commit -m "feat(gói): ..."

# 4. Trước khi push: rebase với main mới nhất
git pull origin main --rebase

# 5. Chạy kiểm thử
python -m unittest discover -s tests -v

# 6. Push và tạo Pull Request
git push origin feature/<gói>-<tên-ngắn>
```

**Trưởng nhóm duyệt Pull Request trước khi merge vào `main`.**

---

## 5. Cấm push thẳng vào `main`

Mọi thay đổi phải qua Pull Request và được trưởng nhóm duyệt.

---

## 6. Xử lý conflict

1. **Dừng lại**, không tự ý "chấp nhận tất cả của mình".
2. **Báo trưởng nhóm** để giải quyết cùng nhau.
3. Sau khi giải quyết, chạy lại kiểm thử trước khi push.

---

## 7. Quy ước code

| Hạng mục | Quy ước |
|----------|---------|
| Python | ≥ 3.10, chỉ dùng thư viện chuẩn |
| Đặt tên | `snake_case` cho hàm/biến/file, `PascalCase` cho lớp, `UPPER_CASE` cho hằng |
| Chú thích | Docstring và comment bằng tiếng Việt |
| Type hint | Bắt buộc cho tham số và kiểu trả về của hàm công khai |
| Tách tầng | `models/` và `services/` KHÔNG dùng `print()`/`input()` |
| Lỗi | Dùng lỗi tự định nghĩa trong `utils/exceptions.py` |
