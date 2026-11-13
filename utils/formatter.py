
"""Định dạng và in bảng ra console."""

from models.department import Department
from models.employee import Employee


def format_money(value: float) -> str:
    """Định dạng số tiền: 12,500,000."""
    return f"{value:,.0f}"


def print_employee_table(
    employees: list[Employee],
    department_names: dict[str, str] | None = None
) -> None:
    """In danh sách nhân viên theo cột.
    department_names: {mã phòng ban: tên} (tùy chọn).
    """
    if not employees:
        print("(Danh sách nhân viên trống)")
        return

    names = department_names or {}

    header = (
        f"{'STT':<4}"
        f"{'Mã NV':<10}"
        f"{'Họ tên':<26}"
        f"{'Loại':<10}"
        f"{'Năm sinh':<10}"
        f"{'Phòng ban':<20}"
        f"{'Lương':>15}"
    )

    print(header)
    print("-" * len(header))

    for i, e in enumerate(employees, 1):
        dept = names.get(e.department_id, e.department_id)

        # Rút gọn tên và tên phòng ban nếu quá dài
        full_name = e.full_name
        if len(full_name) > 23:
            full_name = full_name[:20] + "..."

        if len(dept) > 17:
            dept = dept[:14] + "..."

        print(
            f"{i:<4}"
            f"{e.employee_id:<10}"
            f"{full_name:<26}"
            f"{e.employee_type:<10}"
            f"{e.birth_year:<10}"
            f"{dept:<20}"
            f"{format_money(e.calculate_salary()):>15}"
        )


def print_department_table(departments: list[Department]) -> None:
    """In danh sách phòng ban theo cột."""
    if not departments:
        print("(Danh sách phòng ban trống)")
        return

    header = f"{'STT':<4}{'Mã PB':<10}{'Tên phòng ban':<30}"

    print(header)
    print("-" * len(header))

    for i, d in enumerate(departments, 1):
        department_name = d.department_name

        if len(department_name) > 27:
            department_name = department_name[:24] + "..."

        print(
            f"{i:<4}"
            f"{d.department_id:<10}"
            f"{department_name:<30}"
        )
