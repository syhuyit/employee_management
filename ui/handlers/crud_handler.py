"""Handler CRUD nhân viên (Gói C)."""
from ui.context import AppContext
from ui.handlers._common import todo


def handle_add(ctx: AppContext) -> None:
    """Thêm nhân viên toàn thời gian / bán thời gian."""
    todo("Thêm nhân viên", "C")


def handle_update(ctx: AppContext) -> None:
    """Cập nhật nhân viên theo mã."""
    todo("Cập nhật nhân viên", "C")


def handle_delete(ctx: AppContext) -> None:
    """Xóa nhân viên (có xác nhận)."""
    todo("Xóa nhân viên", "C")


def handle_display(ctx: AppContext) -> None:
    """Hiển thị danh sách nhân viên dạng bảng."""
    todo("Hiển thị danh sách", "C")
