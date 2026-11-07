"""Handler tìm kiếm và sắp xếp (Gói D)."""
from ui.context import AppContext
from ui.handlers._common import todo


def handle_search(ctx: AppContext) -> None:
    """Tìm kiếm nhân viên theo mã hoặc họ tên."""
    todo("Tìm kiếm nhân viên", "D")


def handle_sort(ctx: AppContext) -> None:
    """Sắp xếp danh sách nhân viên theo tiêu chí."""
    todo("Sắp xếp nhân viên", "D")
