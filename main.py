"""Điểm vào của chương trình. Chạy: python main.py  (thêm --seed để nạp dữ liệu mẫu)."""
import argparse
import sys

from ui import menu
from ui.context import build_context
from utils.exceptions import EmployeeManagementError
from utils.sample_data import seed_sample_data


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # hiển thị tiếng Việt trên console Windows
    except (AttributeError, OSError):
        pass
    parser = argparse.ArgumentParser(description="Quản lý nhân viên")
    parser.add_argument("--seed", action="store_true", help="nạp dữ liệu mẫu nếu chưa có dữ liệu")
    args = parser.parse_args()

    ctx = build_context()
    try:
        employees, departments = ctx.storage.load()
        ctx.department_service.set_all(departments)  # nạp phòng ban trước
        ctx.employee_manager.set_all(employees)
    except EmployeeManagementError as exc:
        print(f"[Cảnh báo] Không tải được dữ liệu: {exc}")

    if args.seed and ctx.employee_manager.count() == 0:
        seed_sample_data(ctx)
        print("Đã nạp dữ liệu mẫu.")
    menu.run(ctx)


if __name__ == "__main__":
    main()
