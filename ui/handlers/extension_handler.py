"""Handler chức năng mở rộng: lưu/tải file, tính năng bổ sung (Gói E)."""
import csv
import os

from services.report_service import ReportService
from ui.context import AppContext
from utils.exceptions import StorageError  # xem luu y so 2
from utils.input_helper import confirm  # xem luu y so 3

CSV_PATH = "data/employees.csv"


def handle_save(ctx: AppContext) -> None:
    """Lưu dữ liệu ra file JSON."""
    employees = ctx.employee_service.get_all()
    departments = ctx.department_service.get_all()
    try:
        ctx.storage.save(employees, departments)
    except StorageError as exc:
        print(f"Lỗi: {exc}")
        return
    print("Đã lưu dữ liệu thành công.")
    print(f"File: {os.path.abspath(ctx.storage.file_path)}")
    print(f"({len(departments)} phòng ban, {len(employees)} nhân viên)")


def handle_load(ctx: AppContext) -> None:
    """Tải dữ liệu từ file JSON."""
    if not ctx.storage.exists():
        print(f"Chưa có file dữ liệu: {ctx.storage.file_path}")
        return

    # Tai se ghi de du lieu hien tai nen phai hoi xac nhan
    if not confirm("Tải dữ liệu sẽ GHI ĐÈ dữ liệu hiện tại. Tiếp tục?"):
        print("Đã hủy tải dữ liệu.")
        return

    # Doc xong het roi moi set_all: neu file hong thi du lieu hien tai khong bi mat
    try:
        employees, departments = ctx.storage.load()
    except StorageError as exc:
        print(f"Lỗi: {exc}")
        print("Dữ liệu hiện tại được giữ nguyên.")
        return

    # Phong ban truoc, nhan vien sau
    ctx.department_service.set_all(departments)
    ctx.employee_service.set_all(employees)
    print(f"Đã tải {len(departments)} phòng ban và {len(employees)} nhân viên.")


def _export_csv(employees, path: str) -> None:
    """Ghi danh sach nhan vien ra CSV. utf-8-sig de Excel doc dung tieng Viet."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Mã NV", "Họ tên", "Năm sinh", "Mã phòng ban", "Loại", "Lương cơ bản", "Lương thực lĩnh"]
        )
        for e in employees:
            kind = type(e).__name__.removesuffix("Employee") or type(e).__name__
            writer.writerow(
                [
                    e.employee_id,
                    e.full_name,
                    e.birth_year,
                    e.department_id,
                    kind,
                    e.base_salary,
                    e.calculate_salary(),
                ]
            )


def handle_extension(ctx: AppContext) -> None:
    """Chức năng mở rộng: xuất danh sách nhân viên ra file CSV."""
    employees = ctx.employee_service.get_all()
    if not employees:
        print("Chưa có nhân viên nào để xuất.")
        return
    try:
        _export_csv(employees, CSV_PATH)
    except OSError as exc:
        print(f"Lỗi: không thể ghi file CSV: {exc}")
        return
    print("Đã xuất danh sách nhân viên ra CSV.")
    print(f"File: {os.path.abspath(CSV_PATH)}")
    print(f"Tổng quỹ lương: {ReportService.total_salary_fund(employees):,.0f}")