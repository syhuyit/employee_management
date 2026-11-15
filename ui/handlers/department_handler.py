"""Handler quản lý phòng ban (Gói B)."""
from models.department import Department
from models.employee import Employee
from ui.context import AppContext
from utils.exceptions import EmployeeManagementError
from utils.formatter import print_department_table, print_employee_table
from utils.input_helper import confirm, input_choice, input_string
from utils.validators import validate_department_id, validate_department_name


def _input_department_id(prompt: str) -> str:
    """Tiếp tục hỏi đến khi nhận được mã phòng ban hợp lệ."""
    while True:
        value = input_string(prompt)
        try:
            return validate_department_id(value)
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc} Vui lòng nhập lại.")


def _input_new_department_id(ctx: AppContext) -> str:
    """Hỏi lại mã đến khi hợp lệ và chưa được sử dụng."""
    while True:
        department_id = _input_department_id("Mã phòng ban: ")
        if ctx.department_service.exists(department_id):
            print(f"[Lỗi] Mã phòng ban {department_id} đã tồn tại. Vui lòng nhập mã khác.")
            continue
        return department_id


def _input_department_name(prompt: str) -> str:
    """Tiếp tục hỏi đến khi nhận được tên phòng ban hợp lệ."""
    while True:
        value = input_string(prompt)
        try:
            return validate_department_name(value)
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc} Vui lòng nhập lại.")


def _input_existing_department(ctx: AppContext, prompt: str) -> Department:
    """Hỏi lại mã đến khi tìm thấy phòng ban."""
    while True:
        department_id = _input_department_id(prompt)
        try:
            return ctx.department_service.get_department(department_id)
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc} Vui lòng nhập lại.")


def _input_employee(ctx: AppContext) -> Employee:
    """Hỏi lại mã nhân viên đến khi tìm thấy nhân viên."""
    while True:
        employee_id = input_string("Mã nhân viên cần chuyển: ")
        try:
            return ctx.employee_manager.find_employee(employee_id)
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc} Vui lòng nhập lại.")


def handle_manage_departments(ctx: AppContext) -> None:
    """Quản lý phòng ban: thêm, đổi tên, xóa, hiển thị danh sách."""
    while True:
        print("\n========== QUẢN LÝ PHÒNG BAN ==========")
        print("1. Thêm phòng ban")
        print("2. Sửa tên phòng ban")
        print("3. Xóa phòng ban")
        print("4. Danh sách phòng ban")
        print("0. Quay lại")
        choice = input_choice("Chọn chức năng: ", ["0", "1", "2", "3", "4"])

        if choice == "0":
            return

        if choice == "1":
            department_id = _input_new_department_id(ctx)
            department_name = _input_department_name("Tên phòng ban: ")
            department = Department(department_id, department_name)
            try:
                ctx.department_service.add_department(department)
                print(f"Đã thêm phòng ban: {department}")
            except EmployeeManagementError as exc:
                print(f"[Lỗi] {exc}")

        elif choice == "2":
            department = _input_existing_department(
                ctx, "Mã phòng ban cần sửa: "
            )
            new_name = _input_department_name("Tên mới: ")
            try:
                updated = ctx.department_service.update_department(
                    department.department_id, new_name
                )
                print(f"Đã cập nhật phòng ban: {updated}")
            except EmployeeManagementError as exc:
                print(f"[Lỗi] {exc}")

        elif choice == "3":
            department = _input_existing_department(
                ctx, "Mã phòng ban cần xóa: "
            )
            if confirm(f"Bạn có chắc muốn xóa phòng ban {department}?"):
                try:
                    deleted = ctx.department_service.delete_department(
                        department.department_id, ctx.employee_manager.get_all()
                    )
                    print(f"Đã xóa phòng ban: {deleted}")
                except EmployeeManagementError as exc:
                    print(f"[Lỗi] {exc}")
            else:
                print("Đã hủy thao tác.")

        elif choice == "4":
            print_department_table(ctx.department_service.get_all())


def handle_transfer(ctx: AppContext) -> None:
    """Chuyển nhân viên sau khi xem rõ phòng nguồn và xác nhận phòng đích."""
    employees = ctx.employee_manager.get_all()
    if not employees:
        print("Danh sách nhân viên trống, không thể chuyển phòng ban.")
        return

    departments = ctx.department_service.get_all()
    department_names = {
        department.department_id: department.department_name
        for department in departments
    }

    print("\n========== CHUYỂN PHÒNG BAN ==========")
    print_employee_table(employees, department_names)
    employee = _input_employee(ctx)

    try:
        source_department = ctx.department_service.get_department(
            employee.department_id
        )
    except EmployeeManagementError as exc:
        print(f"[Lỗi] Không xác định được phòng ban hiện tại: {exc}")
        return

    print(f"\nNhân viên: {employee.employee_id} - {employee.full_name}")
    print(
        f"Phòng ban hiện tại: {source_department.department_id} - "
        f"{source_department.department_name}"
    )
    print("\nDanh sách phòng ban đích:")
    print_department_table(departments)

    while True:
        target_id = _input_department_id("Mã phòng ban muốn chuyển đến: ")
        try:
            target_department = ctx.department_service.get_department(target_id)
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc} Vui lòng chọn lại phòng ban đích.")
            continue

        if target_department.department_id == source_department.department_id:
            print(
                f"[Lỗi] Nhân viên đã thuộc phòng ban {source_department.department_id}. "
                "Vui lòng chọn phòng ban khác."
            )
            continue

        if not confirm(
            f"Xác nhận chuyển {employee.employee_id} từ "
            f"{source_department.department_id} sang {target_department.department_id}?"
        ):
            print(
                f"Đã hủy. {employee.employee_id} vẫn thuộc "
                f"phòng ban {source_department.department_id}."
            )
            return

        try:
            ctx.department_service.transfer_employee(employee, target_department.department_id)
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc} Vui lòng chọn lại phòng ban đích.")
            continue

        print(
            f"Đã chuyển {employee.employee_id} từ "
            f"{source_department.department_id} sang {target_department.department_id}."
        )
        return
