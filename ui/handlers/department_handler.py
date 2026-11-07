"""Handler quản lý phòng ban (Gói B)."""
from ui.context import AppContext
from ui.handlers._common import todo


def handle_manage_departments(ctx: AppContext) -> None:
    """Quản lý phòng ban: thêm, sửa, xóa, hiển thị."""
    todo("Quản lý phòng ban", "B")


def handle_transfer(ctx: AppContext) -> None:
    """Chuyển nhân viên sang phòng ban khác."""
    todo("Chuyển phòng ban", "B")
