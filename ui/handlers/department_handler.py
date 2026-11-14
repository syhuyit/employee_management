"""Handler quản lý phòng ban (Gói B)."""
from models.department import Department
from ui.context import AppContext
from utils.exceptions import EmployeeManagementError
from utils.formatter import print_department_table, print_employee_table
from utils.input_helper import confirm, input_choice, input_string


def handle_manage_departments(ctx: AppContext) -> None:
    """Quản lý phòng ban: thêm, sửa, xóa, hiển thị."""
    while True:
        print("\n========== QUẢN LÝ PHÒNG BAN ==========")
        print("1. Hiển thị danh sách phòng ban")
        print("2. Thêm phòng ban")
        print("3. Đổi tên phòng ban")
        print("4. Xóa phòng ban")
        print("0. Quay lại")
        choice = input_choice("Chọn chức năng: ", ["0", "1", "2", "3", "4"])

        if choice == "0":
            return

        try:
            if choice == "1":
                print_department_table(ctx.department_service.get_all())
            elif choice == "2":
                department = Department(
                    input_string("Mã phòng ban: "),
                    input_string("Tên phòng ban: "),
                )
                ctx.department_service.add_department(department)
                print(f"Đã thêm phòng ban: {department}")
            elif choice == "3":
                department_id = input_string("Mã phòng ban cần sửa: ")
                new_name = input_string("Tên mới: ")
                department = ctx.department_service.update_department(
                    department_id, new_name
                )
                print(f"Đã cập nhật phòng ban: {department}")
            elif choice == "4":
                department_id = input_string("Mã phòng ban cần xóa: ")
                department = ctx.department_service.get_department(department_id)
                if confirm(f"Bạn có chắc muốn xóa phòng ban {department}?"):
                    deleted = ctx.department_service.delete_department(
                        department_id, ctx.employee_manager.get_all()
                    )
                    print(f"Đã xóa phòng ban: {deleted}")
                else:
                    print("Đã hủy thao tác.")
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc}")


def handle_transfer(ctx: AppContext) -> None:
    """Chuyển nhân viên sang phòng ban khác."""
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
    try:
        employee_id = input_string("Mã nhân viên cần chuyển: ")
        employee = ctx.employee_manager.find_employee(employee_id)

        print("\nPhòng ban hiện có:")
        print_department_table(departments)
        new_department_id = input_string("Mã phòng ban muốn chuyển đến: ")
        ctx.department_service.transfer_employee(employee, new_department_id)

        new_department = ctx.department_service.get_department(new_department_id)
        print(
            f"Đã chuyển {employee.employee_id} - {employee.full_name} "
            f"đến {new_department.department_name} ({new_department.department_id})."
        )
    except EmployeeManagementError as exc:
        print(f"[Lỗi] {exc}")
