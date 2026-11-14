# BẢNG KỊCH BẢN KIỂM THỬ (TEST CASES SPECIFICATION)

> **Dự án:** Quản lý nhân viên – Employee Management System (Python OOP)  
> **Môn học:** Lập trình Python (INT13162) – Nhóm 1  
> **Người tổng hợp:** Nguyễn Sỹ Huy (Trưởng nhóm / Phụ trách Gói F)  
> **Tiêu chuẩn đề tài:** Tối thiểu 10 ca kiểm thử bao quát: dữ liệu hợp lệ, không hợp lệ, trùng mã, danh sách rỗng, ràng buộc nghiệp vụ và các trường hợp biên.

---

## 1. Bảng 20 kịch bản kiểm thử chi tiết

| Mã TC | Phân loại | Chức năng kiểm thử | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Expected Result) | Kết quả thực tế (Actual Result) | Trạng thái (PASS/FAIL) | Gói phụ trách |
|---|---|---|---|---|---|:---:|:---:|
| **TC01** | Hợp lệ | Thêm nhân viên toàn thời gian (FT) | Mã NV: `NV007`, Họ tên: `Hoàng Gia Bảo`, Năm sinh: `1993`, Phòng ban: `PB01`, Lương CB: `14000000`, Phụ cấp: `1500000` | Thêm thành công vào hệ thống. Tính lương đa hình: Lương = $14,000,000 + 1,500,000 = 15,500,000$ VNĐ. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C |
| **TC02** | Hợp lệ | Thêm nhân viên bán thời gian (PT) | Mã NV: `NV008`, Họ tên: `Lý Thu Trang`, Năm sinh: `2001`, Phòng ban: `PB02`, Giờ làm: `80`, Đơn giá: `50000` | Thêm thành công. Tính lương đa hình: Lương = $80 \times 50,000 = 4,000,000$ VNĐ. Lương CB tự động đặt là `0`. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C |
| **TC03** | Trùng mã | Thêm nhân viên trùng mã định danh | Mã NV: `NV001` (đã tồn tại trong cơ sở dữ liệu) | Hệ thống từ chối thêm, ném ngoại lệ `DuplicateIdError`, hiển thị thông báo mã đã tồn tại. Dữ liệu gốc không đổi. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C |
| **TC04** | Không hợp lệ | Thêm nhân viên bỏ trống mã | Mã NV: `""` hoặc chuỗi toàn khoảng trắng `"   "` | Hệ thống báo lỗi `ValidationError`: "Mã nhân viên không được để trống", yêu cầu người dùng nhập lại. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C / A |
| **TC05** | Không hợp lệ | Kiểm tra định dạng Họ tên có số/ký tự lạ | Họ tên: `Nguyễn Văn An123` hoặc `Trần @ Bình` | Báo lỗi `ValidationError`: "Họ tên chỉ được chứa chữ cái và khoảng trắng", yêu cầu nhập lại ngay tại trường họ tên. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | A |
| **TC06** | Biên | Kiểm tra biên Năm sinh / Tuổi (18 và 17 tuổi) | Giả sử năm hiện tại $Y$:<br>1) Nhập năm $Y - 18$ (đủ 18 tuổi)<br>2) Nhập năm $Y - 17$ (17 tuổi) | 1) Tuổi 18: Hợp lệ, chấp nhận.<br>2) Tuổi 17: Báo lỗi `ValidationError` tuổi phải từ 18 đến 65, yêu cầu nhập lại. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | A |
| **TC07** | Biên | Kiểm tra biên Số giờ làm PT (300h và 301h) | 1) Giờ làm: `300`<br>2) Giờ làm: `301` | 1) `300`: Hợp lệ, chấp nhận.<br>2) `301`: Báo lỗi `ValidationError` (Số giờ làm phải $\le 300$). | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | A |
| **TC08** | Không hợp lệ | Cập nhật lương âm | Chọn NV `NV001`, cập nhật Lương cơ bản = `-5000000` | Báo lỗi `ValidationError` (Lương phải $\ge 0$). Áp dụng nguyên tắc "Tất cả hoặc không gì": Lương cũ giữ nguyên. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C |
| **TC09** | Ràng buộc | Cập nhật trường không thuộc loại nhân viên | Chọn nhân viên PT `NV005`, yêu cầu cập nhật `allowance` (phụ cấp) | Báo lỗi `ValidationError`: Trường `allowance` không áp dụng cho nhân viên bán thời gian. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C |
| **TC10** | Ràng buộc | Thêm NV vào phòng ban không tồn tại | Mã phòng ban: `PB99` (chưa có trong danh mục phòng ban) | Báo lỗi `NotFoundError`: "Không tìm thấy phòng ban PB99". Yêu cầu nhập mã phòng ban hợp lệ. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C / B |
| **TC11** | Nghiệp vụ | Xóa nhân viên nhưng hủy xác nhận (Confirm = 'n') | Chọn xóa `NV002`, tại bước hỏi xác nhận chọn `n` | Hệ thống in thông báo "Đã hủy thao tác xóa", nhân viên `NV002` vẫn còn nguyên trong hệ thống. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C |
| **TC12** | Không tồn tại | Tìm kiếm / Xóa nhân viên không tồn tại | Mã NV: `NV999` (mã không tồn tại) | Báo lỗi `NotFoundError`: "Không tìm thấy nhân viên NV999". Menu không bị văng. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | C / D |
| **TC13** | Danh sách rỗng | Hiển thị bảng khi chưa có dữ liệu | Chạy chương trình không seed, danh sách rỗng, chọn chức năng 4 | In thông báo thân thiện: "(Danh sách nhân viên trống)", không xảy ra lỗi index hay format. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | D / C |
| **TC14** | Danh sách rỗng | Thống kê báo cáo khi danh sách rỗng | Danh sách nhân viên rỗng, chọn chức năng 9 (Thống kê) | Tổng quỹ lương $= 0.0$, lương trung bình $= 0.0$, không phát sinh lỗi chia cho 0 (`ZeroDivisionError`). | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | E |
| **TC15** | Hợp lệ | Sắp xếp lương giảm dần | Chọn sắp xếp tiêu chí `salary`, chiều giảm dần (`descending=True`) | Danh sách trả về được sắp xếp theo mức lương từ cao xuống thấp. Danh sách gốc không bị đảo lộn. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | D |
| **TC16** | Hợp lệ | Sắp xếp theo tên tăng dần (theo từ cuối) | Danh sách gồm: `Nguyễn Văn An`, `Trần Thị Bình`, `Lê Hoàng Cường` | Sắp xếp theo tên gọi (từ cuối): `An` $\rightarrow$ `Bình` $\rightarrow$ `Cường`. Hiển thị bảng chuẩn xác. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | D |
| **TC17** | Hợp lệ | Tìm kiếm gần đúng theo họ tên (chứa từ khóa) | Nhập từ khóa: `nguyen` hoặc `NGUYỄN` (không phân biệt hoa thường / không dấu) | Tìm thấy nhân viên `Nguyễn Văn An`. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | D |
| **TC18** | Ràng buộc toàn vẹn | Xóa phòng ban khi còn nhân viên trực thuộc (R10) | Chọn xóa phòng ban `PB01` (đang có 2 nhân viên thuộc phòng này) | Báo lỗi `BusinessRuleError`: Nêu rõ số lượng nhân viên còn lại trong phòng và từ chối xóa để đảm bảo toàn vẹn. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | B |
| **TC19** | Ràng buộc toàn vẹn | Chuyển phòng ban sang đúng phòng ban hiện tại (R12) | Nhân viên `NV001` đang ở `PB01`, yêu cầu chuyển sang `PB01` | Báo lỗi `BusinessRuleError`: "Nhân viên đã thuộc phòng ban này", từ chối thực hiện. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | B |
| **TC20** | Mở rộng | Lưu dữ liệu và tải lại từ file JSON an toàn | Thực hiện lưu dữ liệu ra file `company_data.json`, thoát chương trình, khởi động lại và tải file | Dữ liệu phòng ban và nhân viên (đủ cả FT và PT) được phục hồi nguyên vẹn đúng kiểu dữ liệu ban đầu. | _(Chờ nghiệm thu GĐ2)_ | ⏳ Pending | E |

---

## 2. Hướng dẫn thực hiện kiểm thử cho Giai đoạn 2 (Tích hợp)

1. **Chuẩn bị môi trường:** Đảm bảo toàn bộ các nhánh `feature/a-models` đến `feature/e-report-extension` đã được merge vào `main` theo đúng thứ tự.
2. **Quy trình chạy kiểm thử Console:**
   - Chạy lệnh: `python main.py --seed`
   - Nhập lần lượt các kịch bản theo bảng trên.
   - Quan sát màn hình, so sánh kết quả thực tế với kết quả mong đợi.
   - Điền kết quả vào cột **Kết quả thực tế** và cập nhật cột **Trạng thái** thành `✅ PASS` hoặc `❌ FAIL`.
3. **Quy trình xử lý khi phát hiện FAIL:**
   - Nếu ca kiểm thử bị `FAIL`, người kiểm thử (Gói F) lập tức tạo một **GitHub Issue** gắn nhãn `bug` và gán cho chủ sở hữu gói tương ứng sửa chữa trước khi chốt nghiệm thu.
