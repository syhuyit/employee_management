"""Handler chức năng mở rộng: lưu/tải file, tính năng bổ sung (Gói E)."""
from ui.context import AppContext
from ui.handlers._common import todo


def handle_save(ctx: AppContext) -> None:
    """Lưu dữ liệu ra file JSON."""
    todo("Lưu dữ liệu ra file", "E")


def handle_load(ctx: AppContext) -> None:
    """Tải dữ liệu từ file JSON."""
    todo("Tải dữ liệu từ file", "E")


def handle_extension(ctx: AppContext) -> None:
    """Chức năng mở rộng (sẽ bổ sung sau)."""
    todo("Chức năng mở rộng", "E")
