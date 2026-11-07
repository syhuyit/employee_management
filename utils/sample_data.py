"""Dữ liệu mẫu để chạy thử/chụp màn hình: python main.py --seed"""
from models.department import Department
from models.fulltime import FullTimeEmployee
from models.parttime import PartTimeEmployee


def seed_sample_data(ctx) -> None:
    """Nạp 3 phòng ban và 6 nhân viên (4 toàn thời gian, 2 bán thời gian)."""
    for dept_id, name in [("PB01", "Kỹ thuật"), ("PB02", "Nhân sự"), ("PB03", "Kinh doanh")]:
        ctx.department_service.add_department(Department(dept_id, name))
    employees = [
        FullTimeEmployee("NV001", "Nguyễn Văn An", 1990, "PB01", 15_000_000, 2_000_000),
        FullTimeEmployee("NV002", "Trần Thị Bình", 1995, "PB02", 12_000_000, 1_000_000),
        FullTimeEmployee("NV003", "Lê Hoàng Cường", 1988, "PB01", 20_000_000, 3_000_000),
        FullTimeEmployee("NV004", "Phạm Minh Dũng", 1992, "PB03", 13_000_000, 1_500_000),
        PartTimeEmployee("NV005", "Võ Thu Hà", 2000, "PB03", 0, 80, 50_000),
        PartTimeEmployee("NV006", "Đặng Quốc Khánh", 2001, "PB02", 0, 120, 45_000),
    ]
    for employee in employees:
        ctx.employee_manager.add_employee(employee)
