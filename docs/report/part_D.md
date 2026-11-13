# Gói D – Tìm kiếm, sắp xếp, in bảng

**Người phụ trách:** Minh Dương
**Nhánh:** `feature/d-search-sort`

## 1. Phạm vi

| Thành phần | File |
|---|---|
| Tìm kiếm | `services/search_service.py` |
| Sắp xếp | `services/sort_service.py` |
| In bảng | `utils/formatter.py` |
| Menu tìm kiếm, sắp xếp | `ui/handlers/search_sort_handler.py` |
| Kiểm thử | `tests/test_search_sort.py` |

## 2. Cách tìm kiếm

### 2.1. Tìm theo mã (chính xác)

`SearchService.find_by_id` so khớp **toàn bộ** mã nhân viên, không phân biệt hoa/thường (dùng `casefold()`), và bỏ khoảng trắng thừa ở hai đầu. Nhập `nv001` hay `NV001` đều tìm ra nhân viên `NV001`. Không thấy thì trả về `None`.

### 2.2. Tìm theo họ tên (gần đúng)

`SearchService.search_by_name` tìm các nhân viên mà họ tên **chứa** từ khóa. Cả họ tên và từ khóa đều được chuẩn hóa trước khi so sánh:

1. Đổi `đ`/`Đ` thành `d`/`D` (vì chữ này không tách được bằng Unicode NFD).
2. Chuẩn hóa `unicodedata.normalize("NFD", ...)` để tách dấu ra khỏi chữ cái.
3. Bỏ các ký tự dấu (nhóm Unicode `Mn`).
4. Đưa về chữ thường bằng `casefold()`.

Nhờ vậy nhập `nguyen` vẫn tìm ra `Nguyễn Văn An`, nhập `duc` tìm ra `Đức`. Từ khóa rỗng (hoặc chỉ có khoảng trắng) trả về danh sách rỗng, không trả về toàn bộ nhân viên.

**Hạn chế:** vì bỏ dấu nên các tên chỉ khác nhau ở dấu sẽ bị coi là giống nhau (ví dụ `van` khớp cả `Văn` lẫn `Vân`). Đây là chủ ý để tìm cho dễ.

### 2.3. Tìm theo phòng ban

`SearchService.search_by_department` lọc theo mã phòng ban, không phân biệt hoa/thường. Ở màn hình tìm kiếm, người dùng được nhập **mã hoặc tên** phòng ban; chương trình tự tra tên sang mã bằng `ctx.department_service.get_all()` rồi mới gọi hàm lọc.

## 3. Cách sắp xếp

`SortService.sort_employees(employees, criteria, descending)` hỗ trợ bốn tiêu chí:

| `criteria` | Khóa sắp xếp |
|---|---|
| `salary` | `calculate_salary()` |
| `name` | từ cuối của họ tên, sau đó là toàn bộ họ tên |
| `id` | mã nhân viên |
| `birth_year` | năm sinh |

Các nguyên tắc chung:

- Trả về **danh sách mới**, không làm thay đổi danh sách gốc.
- Dùng `sorted()` của Python (sắp xếp ổn định), nên hai nhân viên bằng nhau về tiêu chí vẫn giữ nguyên thứ tự ban đầu.
- `criteria` không hợp lệ thì ném `ValidationError`.

### Sắp xếp theo tên tiếng Việt

Người Việt gọi nhau bằng **tên** (từ cuối), không phải họ, nên khóa sắp xếp là:

```
(từ cuối của họ tên, toàn bộ họ tên), đều ở dạng chữ thường
```

Ví dụ `Nguyễn Văn An` có khóa `("an", "nguyễn văn an")`, nên được xếp theo chữ **An**. Nếu hai người trùng tên (cùng là `An`) thì so tiếp toàn bộ họ tên để phân thứ tự.

**Hạn chế:** việc so sánh dựa trên mã ký tự Unicode, nên các chữ có dấu như `Ă`, `Â`, `Đ` không nhất thiết theo đúng thứ tự bảng chữ cái tiếng Việt. Yêu cầu đề bài chỉ cần sắp xếp theo tên tăng dần nên cách này đủ dùng.

## 4. Ví dụ sắp xếp

Danh sách ban đầu:

| Mã | Họ tên | Lương |
|---|---|---|
| NV01 | Nguyễn Văn An | 12,000,000 |
| NV02 | Trần Thị Bình | 4,000,000 |
| NV03 | Lê Minh Châu | 15,000,000 |
| NV04 | Phạm Quang Dũng | 10,000,000 |
| NV05 | Hoàng Văn An | 8,000,000 |

**Sau khi sắp xếp lương giảm dần** (`salary`, `descending=True`):

| Thứ tự | Mã | Họ tên | Lương |
|---|---|---|---|
| 1 | NV03 | Lê Minh Châu | 15,000,000 |
| 2 | NV01 | Nguyễn Văn An | 12,000,000 |
| 3 | NV04 | Phạm Quang Dũng | 10,000,000 |
| 4 | NV05 | Hoàng Văn An | 8,000,000 |
| 5 | NV02 | Trần Thị Bình | 4,000,000 |

**Sau khi sắp xếp tên tăng dần** (`name`, `descending=False`):

| Thứ tự | Mã | Họ tên | Khóa sắp xếp |
|---|---|---|---|
| 1 | NV05 | Hoàng Văn An | `("an", "hoàng văn an")` |
| 2 | NV01 | Nguyễn Văn An | `("an", "nguyễn văn an")` |
| 3 | NV02 | Trần Thị Bình | `("bình", ...)` |
| 4 | NV03 | Lê Minh Châu | `("châu", ...)` |
| 5 | NV04 | Phạm Quang Dũng | `("dũng", ...)` |

Hai người cùng tên `An` được phân thứ tự theo toàn bộ họ tên (`hoàng` đứng trước `nguyễn`). Danh sách ban đầu vẫn giữ nguyên sau cả hai lần sắp xếp.

## 5. Các ca kiểm thử

| STT | Tình huống | Dữ liệu vào | Kết quả mong đợi |
|---|---|---|---|
| 1 | Tìm theo mã, khác hoa/thường | `find_by_id("nv01")` | Trả về nhân viên `NV01` |
| 2 | Tìm theo mã không tồn tại | `find_by_id("NV99")` | Trả về `None` |
| 3 | Tìm tên không dấu | `search_by_name("nguyen")` | Trả về `Nguyễn Văn An` |
| 4 | Từ khóa tìm tên rỗng | `search_by_name("")` | Trả về `[]` |
| 5 | Sắp xếp tên có cùng tên gọi | `sort_employees(..., "name", False)` với hai người đều tên `An` | `Hoàng Văn An` đứng trước `Nguyễn Văn An` |
| 6 | Hai người bằng nhau về lương | `sort_employees(..., "salary", True)` | Giữ nguyên thứ tự ban đầu của hai người đó |
| 7 | Không sửa danh sách gốc | Sắp xếp rồi so sánh với bản sao ban đầu | Danh sách gốc không đổi |
| 8 | Tiêu chí sai | `sort_employees(..., "abc", False)` | Ném `ValidationError` |

## 6. Cách chạy kiểm thử

```bash
python -m unittest tests.test_search_sort -v
```

Kiểm tra thủ công:

```bash
python main.py --seed     # chọn 5 (tìm kiếm), 6 (sắp xếp)
```
