# -*- coding: utf-8 -*-
"""Handler điều khiển giao diện Console cho các chức năng CRUD nhân viên (Gói C).
Đảm nhiệm việc tương tác với người dùng: hiển thị menu, nhận input, kiểm tra lỗi tức thì,
gọi tầng dịch vụ EmployeeManager và hiển thị kết quả ra màn hình.
"""

from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee
from ui.context import AppContext
from utils.exceptions import DuplicateIdError, NotFoundError, ValidationError
from utils.formatter import print_employee_table
from utils.input_helper import confirm, input_choice
from utils.validators import (
    validate_birth_year,
    validate_department_id,
    validate_employee_id,
    validate_full_name,
    validate_hours_worked,
    validate_non_negative,
)


def _ask(prompt: str, validator):
    """Hàm bổ trợ nhập liệu thông minh (Cơ chế kiểm tra tức thì tại chỗ - On-the-fly Validation).
    
    Luồng hoạt động:
      - Sử dụng vòng lặp vô hạn `while True` để liên tục nhận input từ bàn phím.
      - Gọi hàm `validator` truyền vào để kiểm tra tính hợp lệ của dữ liệu.
      - NẾU HỢP LỆ: Trả về giá trị đã chuẩn hóa và thoát vòng lặp.
      - NẾU SAI (bắt được ValidationError): In câu thông báo lỗi cụ thể và yêu cầu người dùng
        nhập lại NGAY TẠI CHÍNH TRƯỜNG ĐÓ mà không bắt người dùng phải nhập lại từ đầu.
    """
    while True:
        raw = input(prompt).strip()
        try:
            return validator(raw)
        except ValidationError as exc:
            print(f"[!] Lỗi: {exc} Vui lòng nhập lại.")


def _validate_year_input(raw: str) -> int:
    """Hàm bổ trợ kiểm tra năm sinh nhập từ bàn phím.
    
    Luồng hoạt động:
      - Bước 1: Ép kiểu chuỗi sang số nguyên (int). Nếu thất bại (chứa chữ cái), ném ValidationError.
      - Bước 2: Gọi validate_birth_year để kiểm tra độ tuổi lao động từ 18 đến 65 tuổi (Quy tắc R3).
    """
    try:
        year = int(raw)
    except ValueError:
        raise ValidationError("Năm sinh phải là một số nguyên.")
    return validate_birth_year(year)


# =============================================================================
# 1. CHỨC NĂNG THÊM MỚI NHÂN VIÊN (CREATE) - MENU 1
# =============================================================================

def handle_add(ctx: AppContext) -> None:
    """Điều hướng luồng thêm mới nhân viên (Toàn thời gian hoặc Bán thời gian).
    
    Luồng hoạt động từng bước:
      - Bước 1: Hiển thị menu cho phép người dùng chọn loại nhân viên (1: FullTime, 2: PartTime, 0: Quay lại).
      - Bước 2: Nhập mã nhân viên và kiểm tra trùng mã (Quy tắc R7).
                Nếu mã đã tồn tại -> In thông báo lỗi nghiệp vụ và dừng thao tác thêm.
      - Bước 3: Nhập các trường thông tin chung (Họ tên, Năm sinh) qua cơ chế nhập sai nhập lại tại chỗ.
      - Bước 4: Hiển thị danh sách các phòng ban hiện có để hỗ trợ người dùng tra cứu;
                Nhập mã phòng ban và kiểm tra tồn tại (Quy tắc R8). Nếu không có -> Báo lỗi và dừng.
      - Bước 5: Nhập các thông tin đặc thù tùy theo loại nhân viên đã chọn ở Bước 1:
                + Toàn thời gian: Nhập Lương cơ bản và Phụ cấp.
                + Bán thời gian: Nhập Số giờ làm (0-300h) và Đơn giá giờ.
      - Bước 6: Khởi tạo đối tượng thực thể (FullTimeEmployee hoặc PartTimeEmployee) tương ứng.
      - Bước 7: Gọi ctx.employee_manager.add_employee() để lưu vào hệ thống,
                In thông báo thành công và hiển thị thẻ thông tin nhân viên vừa tạo.
    """
    print("\n========== THÊM NHÂN VIÊN MỚI ==========")
    print("Chọn loại nhân viên:")
    print("  1. Toàn thời gian (FullTime)")
    print("  2. Bán thời gian (PartTime)")
    print("  0. Quay lại")
    
    # Bước 1: Chọn loại nhân viên cần thêm
    choice = input_choice("Lựa chọn của bạn: ", ["1", "2", "0"])
    if choice == "0":
        return

    # Các hàm validator cục bộ cho mã NV và mã phòng ban
    def _validate_new_id(raw: str) -> str:
        return validate_employee_id(raw)

    def _validate_dept(raw: str) -> str:
        return validate_department_id(raw)

    print("\nNhập thông tin nhân viên:")
    
    # Bước 2: Nhập và kiểm tra mã nhân viên
    emp_id = _ask("  - Mã nhân viên (ví dụ NV001): ", _validate_new_id)
    try:
        # Kiểm tra xem mã nhân viên đã tồn tại trong hệ thống hay chưa
        ctx.employee_manager.find_employee(emp_id)
    except NotFoundError:
        # Nếu ném NotFoundError nghĩa là mã này chưa tồn tại -> Hợp lệ để thêm mới
        pass
    else:
        # Nếu tìm thấy nhân viên trùng mã -> Báo lỗi vi phạm quy tắc R7 và quay lại menu
        print(f"[!] Mã nhân viên '{emp_id}' đã tồn tại (R7).")
        return

    # Bước 3: Nhập các trường thông tin cá nhân chung
    full_name = _ask("  - Họ tên: ", validate_full_name)
    birth_year = _ask("  - Năm sinh: ", _validate_year_input)

    # Bước 4: Nhập và kiểm tra phòng ban trực thuộc
    # Gợi ý danh sách phòng ban đang có sẵn để người dùng dễ chọn
    depts = ctx.department_service.get_all()
    if depts:
        dept_hint = ", ".join(f"{d.department_id} ({d.department_name})" for d in depts)
        print(f"    (Phòng ban hiện có: {dept_hint})")
    
    department_id = _ask("  - Mã phòng ban: ", _validate_dept)
    if not ctx.department_service.exists(department_id):
        # Phòng ban không tồn tại trong danh mục -> Báo lỗi vi phạm quy tắc R8 và quay lại
        print(f"[!] Phòng ban '{department_id}' không tồn tại trong hệ thống (R8).")
        return

    # Bước 5 & 6: Nhập thông tin chuyên biệt và khởi tạo đối tượng tương ứng
    if choice == "1":
        # Nhập thông tin nhân viên toàn thời gian (FullTime)
        base_salary = _ask("  - Lương cơ bản: ", lambda v: validate_non_negative(v, "Lương cơ bản"))
        allowance = _ask("  - Phụ cấp: ", lambda v: validate_non_negative(v, "Phụ cấp"))
        new_emp = FullTimeEmployee(
            employee_id=emp_id,
            full_name=full_name,
            birth_year=birth_year,
            department_id=department_id,
            base_salary=base_salary,
            allowance=allowance,
        )
    else:
        # Nhập thông tin nhân viên bán thời gian (PartTime)
        hours_worked = _ask("  - Số giờ làm (0 - 300): ", validate_hours_worked)
        hourly_rate = _ask("  - Đơn giá giờ: ", lambda v: validate_non_negative(v, "Đơn giá giờ"))
        new_emp = PartTimeEmployee(
            employee_id=emp_id,
            full_name=full_name,
            birth_year=birth_year,
            department_id=department_id,
            base_salary=0.0,  # PartTime có base_salary mặc định bằng 0
            hours_worked=hours_worked,
            hourly_rate=hourly_rate,
        )

    # Bước 7: Thêm vào tầng dịch vụ và hiển thị kết quả
    try:
        ctx.employee_manager.add_employee(new_emp)
        print("\n[✓] Thêm nhân viên thành công!")
        new_emp.display_info()
    except (DuplicateIdError, NotFoundError) as exc:
        print(f"[!] Lỗi khi thêm nhân viên: {exc}")


# =============================================================================
# 2. CHỨC NĂNG CẬP NHẬT THÔNG TIN NHÂN VIÊN (UPDATE) - MENU 2
# =============================================================================

def handle_update(ctx: AppContext) -> None:
    """Điều hướng luồng cập nhật thông tin nhân viên theo mã.
    
    Luồng hoạt động từng bước:
      - Bước 1: Yêu cầu nhập mã nhân viên cần cập nhật (cho phép nhập 0 để hủy).
      - Bước 2: Gọi find_employee() để tra cứu nhân viên; nếu không tìm thấy báo lỗi và dừng.
      - Bước 3: In thẻ thông tin chi tiết hiện tại của nhân viên để người dùng đối chiếu.
      - Bước 4: Hiển thị menu các trường được phép sửa tùy biến theo loại nhân viên:
                + FullTime: Có mục '5. Phụ cấp'.
                + PartTime: Có mục '5. Số giờ làm' và '6. Đơn giá giờ'.
                + KHÔNG hiển thị mã nhân viên và loại nhân viên (bảo toàn tính bất biến R14).
      - Bước 5: Người dùng chọn 1 trường muốn sửa, tiến hành nhập giá trị mới (kiểm tra hợp lệ ngay).
      - Bước 6: Gọi ctx.employee_manager.update_employee() với cơ chế nguyên tử (Atomic Update).
      - Bước 7: In thông báo thành công và hiển thị lại thẻ thông tin sau khi cập nhật.
    """
    print("\n========== CẬP NHẬT THÔNG TIN NHÂN VIÊN ==========")
    
    # Bước 1: Nhận mã nhân viên
    raw_id = input("Nhập mã nhân viên cần cập nhật (hoặc 0 để quay lại): ").strip()
    if raw_id == "0" or not raw_id:
        return

    # Bước 2: Tra cứu nhân viên trong hệ thống
    try:
        emp = ctx.employee_manager.find_employee(raw_id)
    except (NotFoundError, ValidationError) as exc:
        print(f"[!] Lỗi: {exc}")
        return

    # Bước 3: Hiển thị thông tin hiện tại
    print("\n--- THÔNG TIN HIỆN TẠI ---")
    emp.display_info()

    # Bước 4: Xây dựng menu động theo loại nhân viên
    print("\nChọn trường cần cập nhật:")
    print("  1. Họ tên")
    print("  2. Năm sinh")
    print("  3. Mã phòng ban")
    print("  4. Lương cơ bản")
    if emp.employee_type == "FullTime":
        print("  5. Phụ cấp")
        valid_options = ["1", "2", "3", "4", "5", "0"]
    else:
        print("  5. Số giờ làm")
        print("  6. Đơn giá giờ")
        valid_options = ["1", "2", "3", "4", "5", "6", "0"]
    print("  0. Hủy / Quay lại")

    choice = input_choice("Lựa chọn của bạn: ", valid_options)
    if choice == "0":
        return

    field_name = ""
    new_value = None

    # Bước 5: Nhập giá trị mới cho trường đã chọn (kiểm tra tức thì tại chỗ)
    if choice == "1":
        field_name = "full_name"
        new_value = _ask("Nhập họ tên mới: ", validate_full_name)
    elif choice == "2":
        field_name = "birth_year"
        new_value = _ask("Nhập năm sinh mới: ", _validate_year_input)
    elif choice == "3":
        field_name = "department_id"
        # Kiểm tra cả định dạng mã và sự tồn tại của phòng ban mới trong hệ thống (R8)
        def _validate_dept_update(raw: str) -> str:
            d_id = validate_department_id(raw)
            if not ctx.department_service.exists(d_id):
                raise ValidationError(f"Phòng ban '{d_id}' không tồn tại trong hệ thống (R8).")
            return d_id
        new_value = _ask("Nhập mã phòng ban mới: ", _validate_dept_update)
    elif choice == "4":
        field_name = "base_salary"
        new_value = _ask("Nhập lương cơ bản mới: ", lambda v: validate_non_negative(v, "Lương cơ bản"))
    elif choice == "5":
        if emp.employee_type == "FullTime":
            field_name = "allowance"
            new_value = _ask("Nhập phụ cấp mới: ", lambda v: validate_non_negative(v, "Phụ cấp"))
        else:
            field_name = "hours_worked"
            new_value = _ask("Nhập số giờ làm mới (0 - 300): ", validate_hours_worked)
    elif choice == "6":
        field_name = "hourly_rate"
        new_value = _ask("Nhập đơn giá giờ mới: ", lambda v: validate_non_negative(v, "Đơn giá giờ"))

    # Bước 6 & 7: Thực thi cập nhật nguyên tử ở tầng Service và in kết quả
    try:
        updated = ctx.employee_manager.update_employee(emp.employee_id, **{field_name: new_value})
        print("\n[✓] Cập nhật nhân viên thành công!")
        updated.display_info()
    except (ValidationError, NotFoundError) as exc:
        print(f"[!] Lỗi khi cập nhật: {exc}")


# =============================================================================
# 3. CHỨC NĂNG XÓA NHÂN VIÊN (DELETE) - MENU 3
# =============================================================================

def handle_delete(ctx: AppContext) -> None:
    """Điều hướng luồng xóa nhân viên với cơ chế xác nhận an toàn (Confirm Prompt).
    
    Luồng hoạt động từng bước:
      - Bước 1: Yêu cầu người dùng nhập mã nhân viên cần xóa (nhập 0 để hủy).
      - Bước 2: Tra cứu nhân viên qua find_employee(); nếu không có thì báo lỗi (R13).
      - Bước 3: In thông tin nhân viên để người dùng rà soát chính xác đối tượng sắp xóa.
      - Bước 4: Yêu cầu xác nhận an toàn qua hàm confirm() (chấp nhận y/n hoặc yes/no):
                + Nếu chọn 'y': Gọi delete_employee() để xóa khỏi bộ nhớ và in thông báo thành công.
                + Nếu chọn 'n': Hủy thao tác, in thông báo 'Đã hủy' và bảo toàn nguyên vẹn dữ liệu.
    """
    print("\n========== XÓA NHÂN VIÊN ==========")
    
    # Bước 1: Nhận mã nhân viên
    raw_id = input("Nhập mã nhân viên cần xóa (hoặc 0 để quay lại): ").strip()
    if raw_id == "0" or not raw_id:
        return

    # Bước 2: Kiểm tra sự tồn tại của nhân viên
    try:
        emp = ctx.employee_manager.find_employee(raw_id)
    except (NotFoundError, ValidationError) as exc:
        print(f"[!] Lỗi: {exc}")
        return

    # Bước 3: Hiển thị thông tin đối tượng trước khi hỏi xác nhận
    print("\n--- THÔNG TIN NHÂN VIÊN CẦN XÓA ---")
    emp.display_info()

    # Bước 4: Xác nhận an toàn từ người dùng
    if confirm(f"Bạn có chắc chắn muốn xóa nhân viên '{emp.employee_id} - {emp.full_name}'?"):
        # Người dùng chọn đồng ý (y) -> Tiến hành xóa
        deleted = ctx.employee_manager.delete_employee(emp.employee_id)
        print(f"[✓] Đã xóa thành công nhân viên {deleted.employee_id} ({deleted.full_name}).")
    else:
        # Người dùng chọn hủy (n) -> Giữ nguyên dữ liệu
        print("[-] Đã hủy thao tác xóa.")


# =============================================================================
# 4. CHỨC NĂNG HIỂN THỊ DANH SÁCH NHÂN VIÊN (READ ALL) - MENU 4
# =============================================================================

def handle_display(ctx: AppContext) -> None:
    """Hiển thị toàn bộ danh sách nhân viên dạng bảng có cấu trúc thẳng hàng.
    
    Luồng hoạt động từng bước:
      - Bước 1: Lấy danh sách toàn bộ nhân viên từ employee_manager.get_all().
      - Bước 2: Lấy danh sách phòng ban từ department_service.get_all() và tạo từ điển
                ánh xạ {mã_phòng: tên_phòng} để hiển thị tên phòng ban tường minh thay vì chỉ hiển thị mã.
      - Bước 3: Gọi hàm print_employee_table() để định dạng in bảng thẳng cột,
                tự động căn chỉnh tiền tệ và hiển thị thông báo thân thiện khi danh sách rỗng.
      - Bước 4: In tổng số lượng nhân viên hiện có trong hệ thống.
    """
    # Bước 1: Lấy bản sao danh sách nhân viên
    employees = ctx.employee_manager.get_all()
    
    # Bước 2: Lập từ điển tra cứu tên phòng ban
    departments = ctx.department_service.get_all()
    dept_names = {d.department_id: d.department_name for d in departments}

    # Bước 3 & 4: In bảng và tổng số lượng
    print("\n========== DANH SÁCH NHÂN VIÊN ==========")
    print_employee_table(employees, dept_names)
    if employees:
        print(f"Tổng số nhân viên: {len(employees)}")
