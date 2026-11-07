"""Handler thống kê - báo cáo (Gói E)."""
from ui.context import AppContext
from ui.handlers._common import todo


def handle_report(ctx: AppContext) -> None:
    """Hiển thị thống kê: tổng quỹ lương, số NV theo phòng ban, NV lương cao nhất."""
    todo("Thống kê - báo cáo", "E")
