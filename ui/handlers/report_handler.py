"""Handler thống kê - báo cáo (Gói E)."""
from services.report_service import ReportService
from ui.context import AppContext


def _money(value: float) -> str:
    """Dinh dang tien: 12,500,000."""
    return f"{value:,.0f}"


def handle_report(ctx: AppContext) -> None:
    """Hiển thị thống kê: tổng quỹ lương, số NV theo phòng ban, NV lương cao nhất."""
    employees = ctx.employee_service.get_all()
    departments = ctx.department_service.get_all()

    print("\n===== THỐNG KÊ - BÁO CÁO =====")

    # Danh sach rong -> thong bao, khong tinh toan (tranh chia cho 0)
    if not employees:
        print("Chưa có nhân viên nào để thống kê.")
        return

    # 1. Tong quy luong
    print(f"Tổng quỹ lương: {_money(ReportService.total_salary_fund(employees))}")

    # 2. So nhan vien theo phong ban (ghep voi danh sach phong ban de hien ca phong 0 nguoi)
    print("\nSố nhân viên theo phòng ban:")
    counts = ReportService.count_by_department(employees)
    known_ids = set()
    for d in departments:
        known_ids.add(d.department_id)
        print(f"  - {d.department_name} ({d.department_id}): {counts.get(d.department_id, 0)}")
    # Nhan vien co ma phong ban khong con trong danh sach phong ban
    for dept_id, n in counts.items():
        if dept_id not in known_ids:
            print(f"  - (Không rõ phòng ban) ({dept_id}): {n}")

    # 3. Nhan vien luong cao nhat (co the dong hang)
    print("\nNhân viên có lương cao nhất:")
    for e in ReportService.highest_paid(employees):
        print(f"  - {e.employee_id} | {e.full_name} | {_money(e.calculate_salary())}")

    # 4. Luong trung binh
    print(f"\nLương trung bình: {_money(ReportService.average_salary(employees))}")

    # 5. So nhan vien theo loai
    print("\nSố nhân viên theo loại:")
    for kind, n in ReportService.count_by_type(employees).items():
        print(f"  - {kind}: {n}")