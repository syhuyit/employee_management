# -*- coding: utf-8 -*-
"""Lớp quản lý nhân viên (tách khỏi lớp thực thể).
Đảm nhiệm các nghiệp vụ CRUD (Thêm, Tìm kiếm, Cập nhật, Xóa) và lưu trữ danh sách nhân viên trong bộ nhớ.
"""

from models.employee import Employee
from services.department_service import DepartmentService
from services.report_service import ReportService
from services.search_service import SearchService
from services.sort_service import SortService
from utils.exceptions import DuplicateIdError, NotFoundError, ValidationError
from utils.validators import validate_employee_id


class EmployeeManager:
    """Lớp quản lý danh sách nhân viên: thêm, sửa, xóa, tra cứu.
    Tuân thủ nguyên lý Đơn trách nhiệm (Single Responsibility Principle - SRP):
    Thực thể Employee chỉ đại diện cho 1 nhân viên, còn EmployeeManager quản lý tập hợp nhân viên.
    """

    def __init__(self, department_service: DepartmentService) -> None:
        """Khởi tạo bộ quản lý nhân viên.
        
        Args:
            department_service: Dịch vụ phòng ban dùng để kiểm tra tính hợp lệ của phòng ban
                                khi thêm hoặc cập nhật nhân viên (ràng buộc R8).
        """
        self._department_service = department_service
        # Bảng băm lưu trữ nhân viên trong bộ nhớ: key là employee_id, value là đối tượng Employee
        # Giúp việc tra cứu theo mã đạt độ phức tạp tối ưu O(1).
        self._employees: dict[str, Employee] = {}

    # =========================================================================
    # CÁC PHƯƠNG THỨC CRUD CỐT LÕI
    # =========================================================================

    def add_employee(self, employee: Employee) -> None:
        """Thao tác THÊM (Create): Thêm một nhân viên mới vào hệ thống.
        
        Luồng hoạt động:
          - Bước 1: Kiểm tra mã nhân viên đã tồn tại chưa -> Nếu đã có thì ném DuplicateIdError (Quy tắc R7).
          - Bước 2: Kiểm tra phòng ban của nhân viên có tồn tại trong hệ thống không -> Nếu không có thì ném NotFoundError (Quy tắc R8).
          - Bước 3: Lưu nhân viên vào từ điển nội bộ với khóa là employee_id.
        """
        # Bước 1: Chặn trùng mã nhân viên (R7)
        if employee.employee_id in self._employees:
            raise DuplicateIdError(f"Mã nhân viên {employee.employee_id} đã tồn tại.")

        # Bước 2: Chặn thêm nhân viên vào phòng ban không tồn tại (R8)
        if not self._department_service.exists(employee.department_id):
            raise NotFoundError(f"Phòng ban {employee.department_id} không tồn tại.")

        # Bước 3: Lưu đối tượng vào hệ thống
        self._employees[employee.employee_id] = employee

    def find_employee(self, employee_id: str) -> Employee:
        """Thao tác ĐỌC (Read): Tra cứu nhân viên theo mã định danh.
        
        Luồng hoạt động:
          - Bước 1: Chuẩn hóa mã nhân viên (in hoa, cắt khoảng trắng thừa) qua hàm validate_employee_id.
          - Bước 2: Kiểm tra mã trong từ điển: nếu không tồn tại thì ném NotFoundError (Quy tắc R13).
          - Bước 3: Trả về đối tượng Employee tìm thấy.
        """
        # Bước 1: Chuẩn hóa mã định danh (ví dụ 'nv001' -> 'NV001')
        key = validate_employee_id(employee_id)

        # Bước 2: Kiểm tra sự tồn tại trong danh bạ nội bộ
        if key not in self._employees:
            raise NotFoundError(f"Không tìm thấy nhân viên {key}.")

        # Bước 3: Trả về thực thể nhân viên
        return self._employees[key]

    def get_all(self) -> list[Employee]:
        """Lấy toàn bộ danh sách nhân viên hiện có.
        
        Luồng hoạt động:
          - Trả về một BẢN SAO (list copy) của danh sách các đối tượng nhân viên.
          - Mục đích: Bảo vệ tính đóng gói, ngăn chặn mã bên ngoài can thiệp làm thay đổi từ điển nội bộ.
        """
        return list(self._employees.values())

    def set_all(self, employees: list[Employee]) -> None:
        """Thiết lập / Thay thế toàn bộ danh sách nhân viên.
        
        Luồng hoạt động:
          - Xây dựng lại từ điển nội bộ từ danh sách nhân viên truyền vào.
          - Thường được gọi bởi tầng lưu trữ (FileStorage) khi nạp dữ liệu từ file JSON vào chương trình.
        """
        self._employees = {e.employee_id: e for e in employees}

    def count(self) -> int:
        """Trả về tổng số lượng nhân viên hiện có trong hệ thống."""
        return len(self._employees)

    def update_employee(self, employee_id: str, **fields) -> Employee:
        """Thao tác CẬP NHẬT (Update): Cập nhật thông tin nhân viên theo cơ chế nguyên tử (Atomic Update).
        
        Áp dụng nguyên tắc 'Tất cả hoặc không gì' (All-or-Nothing):
          Nếu có bất kỳ trường nào bị lỗi (dữ liệu không hợp lệ hoặc phòng ban không tồn tại),
          toàn bộ các thay đổi trước đó sẽ được khôi phục (Rollback) về trạng thái cũ.
        
        Luồng hoạt động:
          - Bước 1: Tra cứu nhân viên cần sửa qua find_employee (báo lỗi R13 nếu không thấy).
          - Bước 2: Nếu không truyền trường nào cần sửa thì giữ nguyên và trả về.
          - Bước 3: Phân quyền các trường cho phép sửa theo loại nhân viên:
                    + FullTime: full_name, birth_year, department_id, base_salary, allowance.
                    + PartTime: full_name, birth_year, department_id, base_salary, hours_worked, hourly_rate.
          - Bước 4: Kiểm tra tính bất biến (R14) - Cấm sửa 'employee_id' hoặc đổi 'type' của nhân viên.
          - Bước 5: Nếu có cập nhật phòng ban mới ('department_id'), kiểm tra phòng ban mới có tồn tại (R8).
          - Bước 6: THỰC HIỆN CƠ CHẾ NGUYÊN TỬ:
                    + Snapshot (Sao lưu): Lưu lại giá trị cũ của tất cả các trường sắp sửa vào dict 'backup'.
                    + Gán giá trị mới: Lần lượt gán qua setter của model (kích hoạt kiểm tra tính hợp lệ dữ liệu).
                    + Rollback (Khôi phục): Nếu phát sinh bất kỳ ngoại lệ nào, duyệt lại các trường đã gán
                      và khôi phục giá trị ban đầu từ 'backup', sau đó ném lại ngoại lệ.
          - Bước 7: Trả về đối tượng nhân viên đã cập nhật thành công.
        """
        # Bước 1: Tìm nhân viên theo mã định danh
        emp = self.find_employee(employee_id)

        # Bước 2: Không có trường nào cần cập nhật thì trả về ngay
        if not fields:
            return emp

        # Bước 3: Xác định danh sách các trường được phép sửa theo loại nhân viên
        allowed_fields = {"full_name", "birth_year", "department_id", "base_salary"}
        if emp.employee_type == "FullTime":
            allowed_fields.add("allowance")
        elif emp.employee_type == "PartTime":
            allowed_fields.update({"hours_worked", "hourly_rate"})

        # Bước 4: Kiểm tra nếu cố tình cập nhật trường không được phép (ví dụ đổi mã hoặc đổi loại NV - R14)
        for field in fields:
            if field not in allowed_fields:
                raise ValidationError(
                    f"Trường '{field}' không được phép cập nhật cho nhân viên {emp.employee_type} (R14)."
                )

        # Bước 5: Kiểm tra tính hợp lệ của phòng ban mới nếu có thay đổi department_id (R8)
        if "department_id" in fields:
            new_dept_id = str(fields["department_id"]).strip().upper()
            if not self._department_service.exists(new_dept_id):
                raise NotFoundError(f"Phòng ban {new_dept_id} không tồn tại (R8).")

        # Bước 6: Cơ chế nguyên tử 'Tất cả hoặc không gì' (Atomic Snapshot & Rollback)
        # 6.1. Lưu lại bản sao giá trị hiện tại của các trường sắp sửa (Snapshot)
        backup = {field: getattr(emp, field) for field in fields}
        applied = []  # Ghi nhận các trường đã gán thành công
        try:
            # 6.2. Tiến hành gán giá trị mới vào đối tượng (qua các setter kiểm tra hợp lệ)
            for field, value in fields.items():
                setattr(emp, field, value)
                applied.append(field)
        except Exception:
            # 6.3. Gặp lỗi -> Khôi phục (Rollback) toàn bộ trường đã thay đổi về giá trị cũ
            for field in applied:
                setattr(emp, field, backup[field])
            # Ném lại ngoại lệ để thông báo cho tầng UI xử lý
            raise

        # Bước 7: Cập nhật thành công trọn vẹn
        return emp

    def delete_employee(self, employee_id: str) -> Employee:
        """Thao tác XÓA (Delete): Xóa nhân viên ra khỏi hệ thống theo mã.
        
        Luồng hoạt động:
          - Bước 1: Tra cứu nhân viên cần xóa qua find_employee (nếu không thấy sẽ ném NotFoundError - R13).
          - Bước 2: Xóa đối tượng ra khỏi từ điển nội bộ self._employees.
          - Bước 3: Trả về đối tượng vừa bị xóa để tầng UI có thể in thông báo xác nhận.
        """
        # Bước 1: Tìm nhân viên (báo lỗi R13 nếu không tồn tại)
        emp = self.find_employee(employee_id)

        # Bước 2: Xóa khỏi từ điển
        del self._employees[emp.employee_id]

        # Bước 3: Trả về đối tượng vừa xóa
        return emp

    # =========================================================================
    # KHỐI ỦY QUYỀN (DELEGATION) CHO CÁC DỊCH VỤ CHUYÊN BIỆT
    # =========================================================================

    def search_by_name(self, keyword: str) -> list[Employee]:
        """Ủy quyền tìm kiếm gần đúng theo họ tên cho SearchService."""
        return SearchService.search_by_name(self.get_all(), keyword)

    def search_by_department(self, department_id: str) -> list[Employee]:
        """Ủy quyền tìm kiếm theo phòng ban cho SearchService."""
        return SearchService.search_by_department(self.get_all(), department_id)

    def sort_employees(self, criteria: str, descending: bool = False) -> list[Employee]:
        """Ủy quyền sắp xếp danh sách nhân viên cho SortService."""
        return SortService.sort_employees(self.get_all(), criteria, descending)

    def total_salary_fund(self) -> float:
        """Ủy quyền tính tổng quỹ lương cho ReportService."""
        return ReportService.total_salary_fund(self.get_all())
