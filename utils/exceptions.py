"""Các lỗi nghiệp vụ tự định nghĩa của ứng dụng."""


class EmployeeManagementError(Exception):
    """Lớp cha của mọi lỗi nghiệp vụ trong ứng dụng."""


class ValidationError(EmployeeManagementError):
    """Dữ liệu đầu vào không hợp lệ."""


class DuplicateIdError(EmployeeManagementError):
    """Mã định danh bị trùng."""


class NotFoundError(EmployeeManagementError):
    """Không tìm thấy đối tượng theo mã."""


class BusinessRuleError(EmployeeManagementError):
    """Vi phạm ràng buộc nghiệp vụ (ví dụ xóa phòng ban còn nhân viên)."""


class StorageError(EmployeeManagementError):
    """Lỗi đọc/ghi file dữ liệu."""
