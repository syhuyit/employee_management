"""Ngữ cảnh ứng dụng: gom các đối tượng dùng chung, truyền vào mọi handler."""
from dataclasses import dataclass

from services.department_service import DepartmentService
from services.employee_manager import EmployeeManager
from storage.file_storage import FileStorage


@dataclass
class AppContext:
    employee_manager: EmployeeManager
    department_service: DepartmentService
    storage: FileStorage


def build_context() -> AppContext:
    """Khởi tạo các đối tượng và nối chúng với nhau."""
    department_service = DepartmentService()
    employee_manager = EmployeeManager(department_service)
    return AppContext(employee_manager, department_service, FileStorage())
