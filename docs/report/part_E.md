# Gói E – Thống kê, lưu file, chức năng mở rộng

**Người phụ trách:** Phạm Quang Đạt
**Nhánh:** `feature/e-report-extension`

## 1. Phạm vi

| Thành phần | File |
|---|---|
| Báo cáo thống kê (logic) | `services/report_service.py` |
| Báo cáo thống kê (hiển thị) | `ui/handlers/report_handler.py` |
| Lưu/đọc JSON | `storage/file_storage.py` |
| Handler lưu/tải, xuất CSV | `ui/handlers/extension_handler.py` |
| Kiểm thử | `tests/test_report.py`, `tests/test_storage.py` |

## 2. Hai chức năng mở rộng

### 2.1. Chức năng mở rộng 1: Lưu/đọc dữ liệu ra file JSON

**Mục đích:** dữ liệu không bị mất khi thoát chương trình; lần chạy sau tự nạp lại.

**Cách dùng:**

- Menu **10 – Lưu dữ liệu**: ghi toàn bộ phòng ban và nhân viên ra `data/company_data.json`, in đường dẫn file.
- Menu **11 – Tải dữ liệu**: hỏi xác nhận (vì sẽ ghi đè dữ liệu hiện tại), sau đó nạp phòng ban trước, nhân viên sau.
- Chạy `python main.py` (không `--seed`): dữ liệu đã lưu tự nạp lại.

**Cơ chế an toàn:**

- Ghi ra file tạm rồi `os.replace` sang file thật, nên nếu ghi dở bị lỗi thì file cũ vẫn còn nguyên.
- Tự tạo thư mục `data/` nếu chưa có.
- Lỗi I/O, JSON hỏng hoặc dữ liệu sai đều quy về `StorageError`, chương trình không bị sập.
- Chỉ gọi `set_all` sau khi đọc thành công, nên file hỏng không làm mất dữ liệu đang có trong bộ nhớ.

**Ví dụ:**

```
Chọn chức năng: 10
Đã lưu dữ liệu thành công.
File: D:\baitap\data\company_data.json
(2 phòng ban, 2 nhân viên)
```

### 2.2. Chức năng mở rộng 2: Xuất danh sách nhân viên ra CSV

**Mục đích:** chia sẻ danh sách cho người khác, mở và xử lý tiếp bằng Excel.

**Cách dùng:** chọn mục chức năng mở rộng trong menu. Chương trình ghi `data/employees.csv` gồm các cột: Mã NV, Họ tên, Năm sinh, Mã phòng ban, Loại, Lương cơ bản, Lương thực lĩnh.

**Lưu ý kỹ thuật:** file ghi bằng `utf-8-sig` để Excel hiển thị đúng tiếng Việt.

**Ví dụ:**

```
Đã xuất danh sách nhân viên ra CSV.
File: D:\baitap\data\employees.csv
Tổng quỹ lương: 16,000,000
```

Nội dung file CSV:

```
Mã NV,Họ tên,Năm sinh,Mã phòng ban,Loại,Lương cơ bản,Lương thực lĩnh
NV01,Nguyễn Văn An,1995,PB01,FullTime,10000000,12000000
NV02,Trần Thị Bình,2001,PB02,PartTime,0,4000000
```

## 3. Cấu trúc file JSON mẫu

File `data/company_data.json` có hai khóa gốc: `departments` và `employees`.

```json
{
  "departments": [
    {
      "department_id": "PB01",
      "department_name": "Kỹ thuật"
    },
    {
      "department_id": "PB02",
      "department_name": "Kinh doanh"
    }
  ],
  "employees": [
    {
      "type": "FullTime",
      "employee_id": "NV01",
      "full_name": "Nguyễn Văn An",
      "birth_year": 1995,
      "department_id": "PB01",
      "base_salary": 10000000,
      "allowance": 2000000
    },
    {
      "type": "PartTime",
      "employee_id": "NV02",
      "full_name": "Trần Thị Bình",
      "birth_year": 2001,
      "department_id": "PB02",
      "base_salary": 0,
      "hours_worked": 80,
      "hourly_rate": 50000
    }
  ]
}
```

File được ghi với `ensure_ascii=False` và `indent=2` nên đọc được tiếng Việt trực tiếp.

## 4. Các ca kiểm thử

| STT | Tình huống | Dữ liệu vào | Kết quả mong đợi |
|---|---|---|---|
| 1 | Danh sách nhân viên rỗng | `[]` | `total_salary_fund` = `0.0`, `average_salary` = `0.0`, `highest_paid` = `[]`, `count_by_type` = `{}`; màn hình báo cáo in thông báo, không lỗi chia cho 0 |
| 2 | Lương cao nhất đồng hạng | Hai nhân viên cùng mức lương cao nhất | `highest_paid` trả về cả hai người |
| 3 | Phòng ban không có nhân viên | Phòng ban `PB03` chưa có ai | Báo cáo vẫn hiện `PB03: 0` nhờ ghép với danh sách phòng ban |
| 4 | File dữ liệu chưa tồn tại | `load()` khi chưa từng lưu | Trả về `([], [])`, không lỗi |
| 5 | File JSON hỏng | File chứa nội dung không phải JSON, file rỗng, thiếu khóa, thiếu trường nhân viên | Ném `StorageError`, chương trình không sập, dữ liệu hiện tại được giữ nguyên |
| 6 | Lưu rồi tải lại | `save()` rồi `load()` | Dữ liệu giống hệt ban đầu (đúng lớp `FullTime`/`PartTime`, cùng lương) |

## 5. Cách chạy kiểm thử

```bash
python -m unittest tests.test_report tests.test_storage -v
```

Kiểm tra thủ công:

```bash
python main.py --seed     # chọn 9 (báo cáo), 10 (lưu), thoát
python main.py            # dữ liệu tự nạp lại; có thể chọn 11 (tải)
```
