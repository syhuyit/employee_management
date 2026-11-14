# LƯU ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAMS / FLOWCHARTS)

> **Dự án:** Quản lý nhân viên (Employee Management System)  
> **Gói phụ trách:** Gói F – Tài liệu và Kiểm thử (Nguyễn Sỹ Huy - Nhóm trưởng)

---

## 1. Lưu đồ hoạt động Menu chính (Main Menu Flowchart)

Biểu đồ mô tả vòng đời chạy ứng dụng từ lúc khởi động, nạp dữ liệu, hiển thị menu lặp, xử lý ngoại lệ nghiệp vụ và cơ chế thoát an toàn:

```mermaid
flowchart TD
    Start([Khởi động: python main.py]) --> ConfigUTF8[Cấu hình Console UTF-8]
    ConfigUTF8 --> InitContext[Khởi tạo AppContext:\nEmployeeManager, DepartmentService, FileStorage]
    InitContext --> LoadData{Tải dữ liệu từ FileStorage?}
    
    LoadData -->|Thành công| PopulateData[Nạp PB vào DepartmentService\nNạp NV vào EmployeeManager]
    LoadData -->|Thất bại / Chưa có| WarnEmpty[In cảnh báo, dùng dữ liệu rỗng]
    
    PopulateData --> CheckSeed{Có tham số --seed\nvà danh sách rỗng?}
    WarnEmpty --> CheckSeed
    
    CheckSeed -->|Đúng| SeedData[Gọi seed_sample_data:\nNạp 3 PB và 6 NV mẫu]
    CheckSeed -->|Sai| ShowMenu
    SeedData --> ShowMenu
    
    ShowMenu[Hiển thị Menu chính:\n12 chức năng + mục 0. Thoát] --> ReadChoice[/Nhập lựa chọn/]
    
    ReadChoice --> CheckExit{Lựa chọn == '0'?}
    
    CheckExit -->|Đúng| ConfirmExit{Xác nhận thoát\nconfirm y/n?}
    ConfirmExit -->|'y' Đồng ý| Bye([In 'Tạm biệt!' & Dừng an toàn])
    ConfirmExit -->|'n' Hủy| ShowMenu
    
    CheckExit -->|Sai| ValidChoice{Có trong MENU 1..12?}
    ValidChoice -->|Không hợp lệ| ErrorMenu[In: Lựa chọn không hợp lệ] --> ShowMenu
    
    ValidChoice -->|Hợp lệ| ExecHandler[Gọi handler tương ứng ctx]
    
    ExecHandler --> CatchErr{Bắt ngoại lệ?}
    CatchErr -->|EmployeeManagementError| ShowBizErr[In thông báo lỗi nghiệp vụ] --> ShowMenu
    CatchErr -->|NotImplementedError| ShowTodo[In thông báo: TODO chức năng đang hoàn thiện] --> ShowMenu
    CatchErr -->|KeyboardInterrupt / EOFError| ShowCancel[In: Đã hủy thao tác] --> ShowMenu
    CatchErr -->|Thành công| ShowMenu
```

---

## 2. Lưu đồ quy trình Thêm mới nhân viên (Gói C - CRUD)

Quy trình nhập liệu từng trường, kiểm tra tức thì (validate on-the-fly), lỗi ở trường nào nhập lại ngay tại trường đó mà không phải nhập lại từ đầu:

```mermaid
flowchart TD
    StartAdd([Bắt đầu Thêm Nhân Viên]) --> ChooseType[/Chọn loại: 1. Toàn thời gian | 2. Bán thời gian/]
    
    ChooseType --> InputID[/Nhập Mã NV: 3-10 ký tự chữ/số/]
    InputID --> ValidateID{Hợp lệ & Chưa trùng?}
    ValidateID -->|Sai/Trùng| ErrID[Báo lỗi: Nhập lại Mã NV] --> InputID
    
    ValidateID -->|Đúng| InputName[/Nhập Họ tên: 2-50 ký tự/]
    InputName --> ValidateName{Hợp lệ chỉ chữ/khoảng trắng?}
    ValidateName -->|Sai| ErrName[Báo lỗi: Nhập lại Họ tên] --> InputName
    
    ValidateName -->|Đúng| InputBirth[/Nhập Năm sinh/]
    InputBirth --> ValidateBirth{Số nguyên, tuổi 18 - 65?}
    ValidateBirth -->|Sai| ErrBirth[Báo lỗi: Nhập lại Năm sinh] --> InputBirth
    
    ValidateBirth -->|Đúng| InputDept[/Nhập Mã Phòng ban/]
    InputDept --> ValidateDept{Phòng ban tồn tại?}
    ValidateDept -->|Không tồn tại| ErrDept[Báo lỗi NotFoundError: Nhập lại] --> InputDept
    
    ValidateDept -->|Đúng| CheckTypeSpecific{Loại nhân viên?}
    
    %% Toàn thời gian
    CheckTypeSpecific -->|Toàn thời gian| InputSalary[/Nhập Lương cơ bản >= 0/]
    InputSalary --> ValidateSal{Số hợp lệ >= 0?}
    ValidateSal -->|Sai| ErrSal[Báo lỗi: Nhập lại lương] --> InputSalary
    ValidateSal -->|Đúng| InputAllowance[/Nhập Phụ cấp >= 0/]
    InputAllowance --> ValidateAllow{Số hợp lệ >= 0?}
    ValidateAllow -->|Sai| ErrAllow[Báo lỗi: Nhập lại phụ cấp] --> InputAllowance
    ValidateAllow -->|Đúng| CreateFT[Tạo FullTimeEmployee]
    
    %% Bán thời gian
    CheckTypeSpecific -->|Bán thời gian| InputHours[/Nhập Số giờ làm 0 - 300/]
    InputHours --> ValidateHours{Số hợp lệ 0 - 300?}
    ValidateHours -->|Sai| ErrHours[Báo lỗi: Nhập lại giờ làm] --> InputHours
    ValidateHours -->|Đúng| InputRate[/Nhập Đơn giá theo giờ >= 0/]
    InputRate --> ValidateRate{Số hợp lệ >= 0?}
    ValidateRate -->|Sai| ErrRate[Báo lỗi: Nhập lại đơn giá] --> InputRate
    ValidateRate -->|Đúng| CreatePT[Tạo PartTimeEmployee]
    
    CreateFT --> SaveManager[manager.add_employee]
    CreatePT --> SaveManager
    SaveManager --> SuccessMsg[/In thông báo Thêm thành công & thông tin NV/] --> EndAdd([Kết thúc])
```

---

## 3. Lưu đồ quy trình Chuyển phòng ban & Xóa phòng ban (Gói B - Integrity Rules)

Thể hiện ràng buộc toàn vẹn dữ liệu quan hệ **R10, R11, R12**:

```mermaid
flowchart TD
    subgraph Transfer["Nghiệp vụ Chuyển phòng ban (R11, R12)"]
        T1([Bắt đầu Chuyển PB]) --> T2[/Nhập Mã NV/]
        T2 --> T3{NV tồn tại?}
        T3 -->|Không| T4[Báo NotFoundError] --> TEnd([Kết thúc])
        T3 -->|Có| T5[Hiện PB hiện tại & DS các PB]
        T5 --> T6[/Nhập Mã PB mới/]
        T6 --> T7{PB mới tồn tại? R11}
        T7 -->|Không| T8[Báo NotFoundError] --> TEnd
        T7 -->|Có| T9{Trùng PB hiện tại? R12}
        T9 -->|Trùng| T10[Báo BusinessRuleError:\nNV đã ở phòng ban này] --> TEnd
        T9 -->|Khác| T11{Xác nhận chuyển y/n?}
        T11 -->|'y'| T12[Cập nhật employee.department_id = new_id\nIn thông báo thành công] --> TEnd
        T11 -->|'n'| T13[In: Đã hủy chuyển] --> TEnd
    end

    subgraph DeleteDept["Nghiệp vụ Xóa phòng ban (R10)"]
        D1([Bắt đầu Xóa PB]) --> D2[/Nhập Mã PB/]
        D2 --> D3{PB tồn tại?}
        D3 -->|Không| D4[Báo NotFoundError] --> DEnd([Kết thúc])
        D3 -->|Có| D5{Còn nhân viên thuộc PB? R10}
        D5 -->|Còn >= 1 NV| D6[Báo BusinessRuleError:\nPB còn X nhân viên, hãy chuyển NV trước khi xóa] --> DEnd
        D5 -->|0 NV| D7{Xác nhận xóa y/n?}
        D7 -->|'y'| D8[Xóa phòng ban khỏi hệ thống\nIn thông báo thành công] --> DEnd
        D7 -->|'n'| D9[In: Đã hủy xóa] --> DEnd
    end
```
