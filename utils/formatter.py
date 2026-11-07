"""Định dạng và in bảng ra console."""
from models.department import Department
from models.employee import Employee


def format_money(value: float) -> str:
    """Định dạng số tiền: 12,500,000."""
    return f"{value:,.0f}"


def print_employee_table(employees: list[Employee], department_names: dict[str, str] | None = None) -> None:
    """In danh sách nhân viên theo cột. department_names: {mã phòng ban: tên} (tùy chọn)."""
    if not employees:
        print("(Danh sách nhân viên trống)")
        return
    names = department_names or {}
    header = f"{'STT':<4}{'Mã NV':<10}{'Họ tên':<26}{'Loại':<10}{'Năm sinh':<10}{'Phòng ban':<20}{'Lương':>15}"
    print(header)
    print("-" * len(header))
    for i, e in enumerate(employees, 1):
        dept = names.get(e.department_id, e.department_id)
        print(f"{i:<4}{e.employee_id:<10}{e.full_name:<26}{e.employee_type:<10}"
              f"{e.birth_year:<10}{dept:<20}{format_money(e.calculate_salary()):>15}")


def print_department_table(departments: list[Department]) -> None:
    """In danh sách phòng ban theo cột."""
    if not departments:
        print("(Danh sách phòng ban trống)")
        return
    print(f"{'STT':<4}{'Mã PB':<10}{'Tên phòng ban':<30}")
    print("-" * 44)
    for i, d in enumerate(departments, 1):
        print(f"{i:<4}{d.department_id:<10}{d.department_name:<30}")
