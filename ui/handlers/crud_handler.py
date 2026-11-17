"""Handler CRUD nhân viên (Gói C)."""
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
    """Hỏi người dùng lặp lại cho đến khi nhập đúng validator, in lỗi nếu sai."""
    while True:
        raw = input(prompt).strip()
        try:
            return validator(raw)
        except ValidationError as exc:
            print(f"[!] Lỗi: {exc} Vui lòng nhập lại.")


def _validate_year_input(raw: str) -> int:
    """Kiểm tra năm sinh từ chuỗi console."""
    try:
        year = int(raw)
    except ValueError:
        raise ValidationError("Năm sinh phải là một số nguyên.")
    return validate_birth_year(year)


def handle_add(ctx: AppContext) -> None:
    """Thêm nhân viên toàn thời gian / bán thời gian."""
    print("\n========== THÊM NHÂN VIÊN MỚI ==========")
    print("Chọn loại nhân viên:")
    print("  1. Toàn thời gian (FullTime)")
    print("  2. Bán thời gian (PartTime)")
    print("  0. Quay lại")
    choice = input_choice("Lựa chọn của bạn: ", ["1", "2", "0"])
    if choice == "0":
        return

    # Chỉ kiểm tra định dạng ở đây; mã trùng là lỗi nghiệp vụ cần báo rồi quay lại menu.
    def _validate_new_id(raw: str) -> str:
        return validate_employee_id(raw)

    # Tách định dạng khỏi tồn tại để mã đúng dạng nhưng không có sẽ quay lại menu.
    def _validate_dept(raw: str) -> str:
        return validate_department_id(raw)

    # Nhập các trường chung, sai trường nào nhập lại trường đó
    print("\nNhập thông tin nhân viên:")
    emp_id = _ask("  - Mã nhân viên (ví dụ NV001): ", _validate_new_id)
    try:
        ctx.employee_manager.find_employee(emp_id)
    except NotFoundError:
        pass
    else:
        # Mã trùng không phải lỗi định dạng; báo lỗi và kết thúc thao tác thêm.
        print(f"[!] Mã nhân viên '{emp_id}' đã tồn tại (R7).")
        return

    full_name = _ask("  - Họ tên: ", validate_full_name)
    birth_year = _ask("  - Năm sinh: ", _validate_year_input)

    # Hiển thị các phòng ban hiện có để người dùng tiện tra cứu
    depts = ctx.department_service.get_all()
    if depts:
        dept_hint = ", ".join(f"{d.department_id} ({d.department_name})" for d in depts)
        print(f"    (Phòng ban hiện có: {dept_hint})")
    department_id = _ask("  - Mã phòng ban: ", _validate_dept)
    if not ctx.department_service.exists(department_id):
        # Phòng ban không tồn tại là lỗi nghiệp vụ; báo lỗi và kết thúc thao tác thêm.
        print(f"[!] Phòng ban '{department_id}' không tồn tại trong hệ thống (R8).")
        return

    # Nhập thông tin đặc thù theo loại
    if choice == "1":
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
        hours_worked = _ask("  - Số giờ làm (0 - 300): ", validate_hours_worked)
        hourly_rate = _ask("  - Đơn giá giờ: ", lambda v: validate_non_negative(v, "Đơn giá giờ"))
        new_emp = PartTimeEmployee(
            employee_id=emp_id,
            full_name=full_name,
            birth_year=birth_year,
            department_id=department_id,
            base_salary=0.0,
            hours_worked=hours_worked,
            hourly_rate=hourly_rate,
        )

    try:
        ctx.employee_manager.add_employee(new_emp)
        print("\n[✓] Thêm nhân viên thành công!")
        new_emp.display_info()
    except (DuplicateIdError, NotFoundError) as exc:
        print(f"[!] Lỗi khi thêm nhân viên: {exc}")


def handle_update(ctx: AppContext) -> None:
    """Cập nhật nhân viên theo mã."""
    print("\n========== CẬP NHẬT THÔNG TIN NHÂN VIÊN ==========")
    raw_id = input("Nhập mã nhân viên cần cập nhật (hoặc 0 để quay lại): ").strip()
    if raw_id == "0" or not raw_id:
        return

    try:
        emp = ctx.employee_manager.find_employee(raw_id)
    except (NotFoundError, ValidationError) as exc:
        print(f"[!] Lỗi: {exc}")
        return

    print("\n--- THÔNG TIN HIỆN TẠI ---")
    emp.display_info()

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

    if choice == "1":
        field_name = "full_name"
        new_value = _ask("Nhập họ tên mới: ", validate_full_name)
    elif choice == "2":
        field_name = "birth_year"
        new_value = _ask("Nhập năm sinh mới: ", _validate_year_input)
    elif choice == "3":
        field_name = "department_id"
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

    try:
        updated = ctx.employee_manager.update_employee(emp.employee_id, **{field_name: new_value})
        print("\n[✓] Cập nhật nhân viên thành công!")
        updated.display_info()
    except (ValidationError, NotFoundError) as exc:
        print(f"[!] Lỗi khi cập nhật: {exc}")


def handle_delete(ctx: AppContext) -> None:
    """Xóa nhân viên (có xác nhận)."""
    print("\n========== XÓA NHÂN VIÊN ==========")
    raw_id = input("Nhập mã nhân viên cần xóa (hoặc 0 để quay lại): ").strip()
    if raw_id == "0" or not raw_id:
        return

    try:
        emp = ctx.employee_manager.find_employee(raw_id)
    except (NotFoundError, ValidationError) as exc:
        print(f"[!] Lỗi: {exc}")
        return

    print("\n--- THÔNG TIN NHÂN VIÊN CẦN XÓA ---")
    emp.display_info()

    if confirm(f"Bạn có chắc chắn muốn xóa nhân viên '{emp.employee_id} - {emp.full_name}'?"):
        deleted = ctx.employee_manager.delete_employee(emp.employee_id)
        print(f"[✓] Đã xóa thành công nhân viên {deleted.employee_id} ({deleted.full_name}).")
    else:
        print("[-] Đã hủy thao tác xóa.")


def handle_display(ctx: AppContext) -> None:
    """Hiển thị danh sách nhân viên dạng bảng."""
    employees = ctx.employee_manager.get_all()
    departments = ctx.department_service.get_all()
    dept_names = {d.department_id: d.department_name for d in departments}

    print("\n========== DANH SÁCH NHÂN VIÊN ==========")
    print_employee_table(employees, dept_names)
    if employees:
        print(f"Tổng số nhân viên: {len(employees)}")
