"""Vòng lặp menu chính. Bảng MENU là nơi DUY NHẤT ánh xạ lựa chọn -> handler."""
from ui.context import AppContext
from ui.handlers import (crud_handler, department_handler, extension_handler,
                         report_handler, search_sort_handler)
from utils.exceptions import EmployeeManagementError
from utils.input_helper import confirm

MENU = {
    "1": ("Thêm nhân viên", crud_handler.handle_add),
    "2": ("Cập nhật nhân viên", crud_handler.handle_update),
    "3": ("Xóa nhân viên", crud_handler.handle_delete),
    "4": ("Hiển thị danh sách nhân viên", crud_handler.handle_display),
    "5": ("Tìm kiếm nhân viên", search_sort_handler.handle_search),
    "6": ("Sắp xếp nhân viên", search_sort_handler.handle_sort),
    "7": ("Quản lý phòng ban", department_handler.handle_manage_departments),
    "8": ("Chuyển phòng ban", department_handler.handle_transfer),
    "9": ("Thống kê - báo cáo", report_handler.handle_report),
    "10": ("Lưu dữ liệu ra file", extension_handler.handle_save),
    "11": ("Tải dữ liệu từ file", extension_handler.handle_load),
    "12": ("Chức năng mở rộng", extension_handler.handle_extension),
}


def _print_menu() -> None:
    print("\n" + "=" * 50)
    print("     QUẢN LÝ NHÂN VIÊN - EMPLOYEE MANAGEMENT")
    print("=" * 50)
    for key, (label, _) in MENU.items():
        print(f"  {key:>2}. {label}")
    print("   0. Thoát chương trình")
    print("-" * 50)


def run(ctx: AppContext) -> None:
    """Chạy menu cho đến khi người dùng thoát. Không bao giờ crash vì lỗi của handler."""
    while True:
        _print_menu()
        try:
            choice = input("Chọn chức năng: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nĐã thoát chương trình an toàn.")
            return
        if choice == "0":
            try:
                if confirm("Bạn có chắc muốn thoát?"):
                    print("Tạm biệt!")
                    return
            except (EOFError, KeyboardInterrupt):
                print("\nĐã thoát chương trình an toàn.")
                return
            continue
        item = MENU.get(choice)
        if item is None:
            print("[!] Lựa chọn không hợp lệ, vui lòng chọn lại.")
            continue
        try:
            item[1](ctx)
        except EmployeeManagementError as exc:
            print(f"[Lỗi] {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\n[!] Đã hủy thao tác.")
        except NotImplementedError as exc:
            print(f"[TODO] Chức năng chưa được cài đặt: {exc}")
        except Exception as exc:  # lưới an toàn cuối cùng
            print(f"[Lỗi không mong muốn] {type(exc).__name__}: {exc}")
