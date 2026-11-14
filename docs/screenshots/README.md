# HƯỚNG DẪN VÀ DANH MỤC ẢNH CHỤP MÀN HÌNH MINH HỌA (SCREENSHOTS)

> **Dự án:** Quản lý nhân viên (Employee Management System)  
> **Gói phụ trách:** Gói F – Tài liệu và Kiểm thử (Nguyễn Sỹ Huy - Nhóm trưởng)  
> **Thư mục lưu trữ ảnh:** `docs/screenshots/`  
> **Định dạng file:** PNG (`.png`), ảnh rõ nét, chụp thẳng cửa sổ Terminal/Console.

---

## 1. Quy ước đặt tên ảnh chuẩn

Tên ảnh được đặt theo quy tắc: `NN_ten-ngan.png` trong đó:
- `NN`: Số thứ tự gồm 2 chữ số (`01`, `02`, ..., `20`).
- `ten-ngan`: Tên ngắn gọn mô tả chức năng, viết bằng chữ thường không dấu, nối nhau bằng dấu gạch ngang `-`.

---

## 2. Danh mục 20 ảnh chụp màn hình bắt buộc (Kèm hướng dẫn thao tác)

| STT | Tên file ảnh | Mô tả nội dung cần chụp | Thao tác trên Console để chụp | Gói phụ trách |
|:---:|---|---|---|:---:|
| 1 | `01_menu-chinh.png` | Giao diện Menu chính hoàn chỉnh gồm 12 chức năng và mục 0 | Chạy `python main.py --seed`, chụp toàn bộ khung menu chính hiển thị từ mục 1 đến 12 và mục 0. | Lead |
| 2 | `02_them-fulltime.png` | Thao tác thêm nhân viên toàn thời gian thành công | Chọn `1` $\rightarrow$ Chọn `1` (Toàn thời gian) $\rightarrow$ Nhập: Mã: `NV007`, Tên: `Hoàng Gia Bảo`, Năm sinh: `1993`, PB: `PB01`, Lương: `14000000`, Phụ cấp: `1500000`. Chụp thông báo thêm thành công và thông tin NV. | C |
| 3 | `03_them-parttime.png` | Thao tác thêm nhân viên bán thời gian thành công | Chọn `1` $\rightarrow$ Chọn `2` (Bán thời gian) $\rightarrow$ Nhập: Mã: `NV008`, Tên: `Lý Thu Trang`, Năm sinh: `2001`, PB: `PB02`, Giờ làm: `80`, Đơn giá: `50000`. Chụp màn hình kết quả lương $4,000,000$. | C |
| 4 | `04_them-trung-ma.png` | Hệ thống từ chối khi nhập trùng mã nhân viên | Chọn `1` $\rightarrow$ Nhập mã `NV001` (đã có trong dữ liệu mẫu). Chụp thông báo lỗi `[Lỗi] Mã nhân viên NV001 đã tồn tại`. | C |
| 5 | `05_nhap-sai-nhap-lai.png` | Cơ chế kiểm tra tức thì: nhập sai trường nào nhập lại ngay trường đó | Chọn `1` $\rightarrow$ Nhập tên có số: `An123` (báo lỗi, bắt nhập lại) $\rightarrow$ Nhập năm sinh `2015` (dưới 18 tuổi, bắt nhập lại) $\rightarrow$ Nhập đúng. Chụp cả đoạn hội thoại. | C / A |
| 6 | `06_cap-nhat.png` | Cập nhật thông tin nhân viên thành công | Chọn `2` $\rightarrow$ Nhập mã `NV001` $\rightarrow$ Chọn cập nhật Lương cơ bản $\rightarrow$ Nhập `18000000`. Chụp thông báo cập nhật thành công. | C |
| 7 | `07_xoa-xac-nhan.png` | Thao tác xóa nhân viên có xác nhận an toàn | Chọn `3` $\rightarrow$ Nhập `NV002` $\rightarrow$ Nhập `n` (in "Đã hủy") $\rightarrow$ Xóa lại và nhập `y` (in "Xóa thành công"). Chụp cả hai tình huống `n` và `y`. | C |
| 8 | `08_hien-thi.png` | Bảng hiển thị danh sách nhân viên dạng cột thẳng hàng | Chọn `4` (Hiển thị danh sách). Chụp bảng danh sách nhân viên đầy đủ các cột: STT, Mã NV, Họ tên, Loại, Năm sinh, Phòng ban, Lương. | C / D |
| 9 | `09_danh-sach-rong.png` | Xử lý danh sách nhân viên rỗng | Khởi động chương trình mới không có data (`python main.py`), chọn `4`. Chụp thông báo: `(Danh sách nhân viên trống)`. | C / D |
| 10 | `10_tim-ma.png` | Tìm kiếm chính xác theo mã nhân viên | Chọn `5` $\rightarrow$ Chọn `1` (Theo mã) $\rightarrow$ Nhập `nv003` (chữ thường). Chụp kết quả tìm thấy đúng nhân viên `NV003` - Lê Hoàng Cường. | D |
| 11 | `11_tim-ten.png` | Tìm kiếm gần đúng theo họ tên (chứa từ khóa) | Chọn `5` $\rightarrow$ Chọn `2` (Theo họ tên) $\rightarrow$ Nhập `nguyen` hoặc `cường`. Chụp bảng danh sách các nhân viên khớp từ khóa. | D |
| 12 | `12_tim-phong-ban.png` | Lọc danh sách nhân viên theo phòng ban | Chọn `5` $\rightarrow$ Chọn `3` $\rightarrow$ Nhập `PB01` (hoặc tên `Kỹ thuật`). Chụp danh sách các nhân viên trực thuộc phòng Kỹ thuật. | D |
| 13 | `13_sap-xep-luong.png` | Bảng danh sách nhân viên sắp xếp lương giảm dần | Chọn `6` $\rightarrow$ Chọn `1` (Lương giảm dần). Chụp bảng danh sách kết quả với mức lương xếp từ lớn nhất xuống nhỏ nhất. | D |
| 14 | `14_sap-xep-ten.png` | Sắp xếp nhân viên theo tên tăng dần | Chọn `6` $\rightarrow$ Chọn `2` (Tên tăng dần). Chụp bảng kết quả với thứ tự tên gọi: `An` $\rightarrow$ `Bình` $\rightarrow$ `Cường` $\rightarrow$ `Dũng` $\rightarrow$ `Hà`. | D |
| 15 | `15_chuyen-phong-ban.png` | Thao tác chuyển phòng ban thành công | Chọn `8` $\rightarrow$ Nhập mã NV: `NV001` $\rightarrow$ Nhập phòng ban mới: `PB02` $\rightarrow$ Xác nhận `y`. Chụp thông báo: "Đã chuyển NV001 từ PB01 sang PB02". | B |
| 16 | `16_xoa-phong-ban-loi.png` | Từ chối xóa phòng ban khi còn nhân viên trực thuộc (R10) | Chọn `7` (Quản lý PB) $\rightarrow$ Chọn xóa $\rightarrow$ Nhập mã `PB01`. Chụp thông báo lỗi: `[Lỗi] Phòng ban PB01 còn X nhân viên, hãy chuyển họ sang phòng khác trước khi xóa.` | B |
| 17 | `17_thong-ke.png` | Báo cáo thống kê tổng quỹ lương, số NV theo PB, lương cao nhất | Chọn `9` (Thống kê - báo cáo). Chụp màn hình đầy đủ các chỉ số: Tổng quỹ lương, nhân viên lương cao nhất, số nhân viên từng phòng ban (kể cả PB có 0 NV). | E |
| 18 | `18_da-hinh.png` | **Minh họa tính chất Đa hình (Polymorphism):** Cùng một danh sách hỗn hợp gọi chung `calculate_salary()`, nhân viên FT tính theo lương CB + phụ cấp, nhân viên PT tính theo giờ làm * đơn giá | Chạy bảng hiển thị hoặc chạy test đa hình in rõ sự khác biệt trong công thức tính của `NV001` (FT: $15M + 2M = 17M$) và `NV005` (PT: $80 \times 50k = 4M$). | A / F |
| 19 | `19_luu-tai-file.png` | Lưu trữ dữ liệu ra file JSON và nạp lại an toàn | Chọn `10` (Lưu file) $\rightarrow$ Báo "Đã lưu thành công ra data/company_data.json" $\rightarrow$ Chọn `11` (Tải file có xác nhận). Chụp kết quả thực hiện. | E |
| 20 | `20_chuc-nang-mo-rong.png` | Chức năng mở rộng: Xuất danh sách nhân viên ra file CSV | Chọn `12` (Chức năng mở rộng) $\rightarrow$ Chọn Xuất CSV $\rightarrow$ Báo xuất thành công ra `data/employees.csv`. Mở file CSV chụp minh họa. | E |

---

## 3. Mẹo chụp ảnh đẹp và nhanh trên Windows (Dành cho Trưởng nhóm)

1. **Phím tắt chụp nhanh từng vùng:** Nhấn tổ hợp phím `Windows + Shift + S`.
2. Dùng chuột kéo chọn chính xác khung cửa sổ dòng lệnh Terminal / PowerShell.
3. Nhấp vào thông báo góc phải màn hình của công cụ **Snipping Tool**, nhấn `Ctrl + S` để lưu ảnh.
4. Đặt tên file đúng theo bảng trên (ví dụ: `01_menu-chinh.png`) và lưu trực tiếp vào thư mục:  
   `d:\INT13162_HuyNS_Python\Bai_tap_lon\Python_Nhom_1\2.Code\employee_management\docs\screenshots\`
