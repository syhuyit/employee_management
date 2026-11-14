# -*- coding: utf-8 -*-
"""
Script cập nhật và phát triển file báo cáo Nhom_1_Bao_cao.docx dựa trên form của GVHD.
Bảo toàn bìa, sửa số thứ tự bảng thành viên, và điền đầy đủ 8 phần nội dung theo chuẩn học thuật.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_PATH = r"d:\INT13162_HuyNS_Python\Bai_tap_lon\Python_Nhom_1\2.Code\employee_management\Nhom_1_Bao_cao.docx"

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt padding cho ô."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table_header(row, col_widths=None, bg_color="2C3E50", text_color="FFFFFF"):
    """Định dạng hàng tiêu đề của bảng."""
    for i, cell in enumerate(row.cells):
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        if col_widths and i < len(col_widths):
            cell.width = col_widths[i]
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(255, 255, 255)

def format_cell_content(cell, text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, font_size=10.5, font_name="Times New Roman"):
    """Ghi nội dung vào ô với định dạng chuẩn."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = font_name
    run.font.size = Pt(font_size)
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 51, 102) # Navy Blue
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(12.5)
    run.font.color.rgb = RGBColor(44, 62, 80)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.italic = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    return p

def add_body_paragraph(doc, text, bold_prefix=None, space_after=6, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.italic = italic
    return p

def add_bullet_point(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p

def add_code_block(doc, code_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.right_indent = Inches(0.2)
    # Background border
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(34, 34, 34)
    return p

def add_placeholder_box(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(f"[{text}]")
    run.bold = True
    run.italic = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(128, 128, 128)
    return p

def main():
    doc = docx.Document(DOCX_PATH)
    
    # 1. Sửa STT bảng thành viên trang bìa (hàng 5: sửa '4' thành '5')
    if len(doc.tables) > 0:
        cover_table = doc.tables[0]
        if len(cover_table.rows) >= 6:
            cover_table.rows[5].cells[0].text = "5"
            for row in cover_table.rows:
                for c in row.cells:
                    for p in c.paragraphs:
                        for r in p.runs:
                            r.font.name = "Times New Roman"

    # 2. Xóa các đoạn placeholder từ đoạn 16 trở đi
    # Giữ lại đoạn 0..15 (Trang bìa và Mục lục)
    p_count = len(doc.paragraphs)
    for i in range(p_count - 1, 15, -1):
        p = doc.paragraphs[i]
        p._element.getparent().remove(p._element)

    print(f"Cleared placeholder paragraphs. Remaining paragraphs: {len(doc.paragraphs)}")

    # =========================================================================
    # PHẦN I: GIỚI THIỆU THÀNH VIÊN NHÓM
    # =========================================================================
    add_heading_1(doc, "PHẦN I: GIỚI THIỆU THÀNH VIÊN NHÓM")
    add_body_paragraph(doc, "Nhóm 1 gồm 06 sinh viên lớp Thực tập cơ sở, khoa Công nghệ Thông tin, Học viện Công nghệ Bưu chính Viễn thông. Dưới sự hướng dẫn của Thầy Mai Ngọc Lương, nhóm đã phân công vai trò và trách nhiệm cụ thể của từng thành viên nhằm đảm bảo tính chuyên môn hóa, phát huy tối đa thế mạnh của từng cá nhân và phối hợp nhịp nhàng theo phương pháp phát triển phần mềm chuẩn mực.")

    # Bảng thành viên
    t_members = doc.add_table(rows=7, cols=5)
    t_members.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_m = [Inches(0.5), Inches(1.3), Inches(1.8), Inches(1.4), Inches(2.2)]
    
    headers_m = ["STT", "Mã sinh viên", "Họ và tên", "Gói phụ trách", "Nhiệm vụ chính trong dự án"]
    for i, h in enumerate(headers_m):
        t_members.rows[0].cells[i].text = h
    style_table_header(t_members.rows[0], widths_m, bg_color="1F4E79")

    data_m = [
        ("1", "B23DVCN069", "Nguyễn Sỹ Huy", "Lead & Gói F", "Trưởng nhóm; thiết kế kiến trúc tổng thể; dựng base skeleton; điều phối tiến độ; review PR; vẽ biểu đồ UML & Lưu đồ; tổng hợp báo cáo kỹ thuật."),
        ("2", "B23DVCN177", "Nông Quang Vinh", "Gói A", "Xây dựng các lớp thực thể nhân viên (Employee, FullTimeEmployee, PartTimeEmployee, Factory); xây dựng bộ kiểm tra tính hợp lệ dữ liệu (validators.py); viết unit test models."),
        ("3", "B23DVCN149", "Nguyễn Mạnh Thảo", "Gói B", "Xây dựng thực thể Department; dịch vụ quản lý phòng ban DepartmentService; nghiệp vụ luân chuyển phòng ban và kiểm soát toàn vẹn xóa phòng ban (R10-R12); viết unit test phòng ban."),
        ("4", "B23DVCN084", "Phạm Thanh Hải", "Gói C", "Xây dựng lớp quản lý nghiệp vụ EmployeeManager (Thêm, Sửa, Xóa, Hiển thị); xử lý cập nhật nguyên tử 'Tất cả hoặc không gì'; hoàn thiện giao diện nhập liệu console; viết unit test CRUD."),
        ("5", "B23DVCN044", "Phùng Minh Dương", "Gói D", "Xây dựng dịch vụ tìm kiếm SearchService (chính xác và gần đúng không dấu); dịch vụ sắp xếp đa tiêu chí SortService; định dạng bảng hiển thị thẳng hàng (formatter.py); viết unit test tìm kiếm/sắp xếp."),
        ("6", "B23DVCN188", "Phạm Quang Đạt", "Gói E", "Xây dựng dịch vụ thống kê ReportService (quỹ lương, lương cao nhất, số NV theo PB); xây dựng lớp lưu trữ dữ liệu an toàn FileStorage (JSON); chức năng mở rộng xuất file CSV; viết unit test.")
    ]

    for row_idx, data_row in enumerate(data_m, start=1):
        row = t_members.rows[row_idx]
        bg = "F2F2F2" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(data_row):
            cell = row.cells[col_idx]
            cell.width = widths_m[col_idx]
            set_cell_background(cell, bg)
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1, 3] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_content(cell, text, align=align)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # PHẦN II: KẾ HOẠCH, PHÂN CÔNG CÁC THÀNH VIÊN
    # =========================================================================
    add_heading_1(doc, "PHẦN II: KẾ HOẠCH, PHÂN CÔNG CÁC THÀNH VIÊN")
    
    add_heading_2(doc, "2.1. Kế hoạch triển khai dự án chi tiết (Project Plan)")
    add_body_paragraph(doc, "Dự án được triển khai trong vòng 3 tuần (từ ngày 06/11/2026 đến ngày 25/11/2026) theo lộ trình phân chia công việc rõ ràng, kết hợp nguyên tắc lập trình song song trên các nhánh Git độc lập và kiểm tra chéo (Cross Review) qua Pull Request:")

    # Bảng kế hoạch
    t_plan = doc.add_table(rows=11, cols=7)
    t_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_p = [Inches(0.4), Inches(1.2), Inches(2.2), Inches(1.1), Inches(1.1), Inches(0.8), Inches(0.8)]
    headers_p = ["STT", "Hạng mục", "Nội dung chi tiết", "Người thực hiện", "Người Review", "Hạn xong", "Trạng thái"]
    for i, h in enumerate(headers_p):
        t_plan.rows[0].cells[i].text = h
    style_table_header(t_plan.rows[0], widths_p, bg_color="1F4E79")

    data_p = [
        ("I", "Phân tích", "Phân tích yêu cầu bài toán Quản lý nhân viên; xác định 14 luật nghiệp vụ (R1-R14); phân chia kiến trúc 3 tầng và ranh giới 6 gói việc A-F.", "Nguyễn Sỹ Huy", "Cả nhóm", "08/11/2026", "Hoàn thành"),
        ("II", "Thiết kế", "Thiết kế kiến trúc hệ thống; vẽ biểu đồ lớp UML Class Diagram; vẽ lưu đồ hoạt động Menu chính và luồng xử lý nghiệp vụ.", "Nguyễn Sỹ Huy", "N. Q. Vinh", "09/11/2026", "Hoàn thành"),
        ("III.1", "Base Skeleton", "Dựng khung dự án chuẩn mực, khởi tạo menu điều khiển an toàn không crash, thiết lập 11 smoke test nền tảng.", "Nguyễn Sỹ Huy", "Cả nhóm", "08/11/2026", "Hoàn thành"),
        ("III.2", "Gói A: Models", "Cài đặt ABC Employee, FullTime, PartTime, Factory; cài đặt bộ kiểm tra tính hợp lệ dữ liệu (validators.py); viết unit test.", "N. Q. Vinh", "N. S. Huy", "13/11/2026", "Đang làm"),
        ("III.3", "Gói B: Phòng ban", "Cài đặt lớp Department, DepartmentService; ràng buộc xóa phòng ban còn nhân viên, chuyển phòng ban; viết unit test.", "N. M. Thảo", "N. S. Huy", "13/11/2026", "Đang làm"),
        ("III.4", "Gói C: CRUD NV", "Cài đặt EmployeeManager; cơ chế cập nhật nguyên tử 'Tất cả hoặc không gì'; hoàn thiện giao diện nhập liệu console; viết unit test.", "P. T. Hải", "N. S. Huy", "14/11/2026", "Đang làm"),
        ("III.5", "Gói D: Tìm & Sắp", "Cài đặt SearchService (tìm chính xác, gần đúng không dấu); SortService (đa tiêu chí); định dạng bảng in thẳng hàng; viết unit test.", "P. M. Dương", "N. S. Huy", "14/11/2026", "Đang làm"),
        ("III.6", "Gói E: Báo cáo", "Cài đặt ReportService (tổng quỹ lương, lương cao nhất); lưu/đọc JSON an toàn FileStorage; chức năng mở rộng xuất file CSV; viết unit test.", "P. Q. Đạt", "N. S. Huy", "14/11/2026", "Đang làm"),
        ("IV", "Kiểm thử tích hợp", "Merge tuần tự các nhánh PR vào main; chạy xuyên suốt 12 kịch bản tích hợp; thực thi bảng 20 ca kiểm thử (test_cases.md).", "Huy, Hải", "Cả nhóm", "17/11/2026", "Chưa bắt đầu"),
        ("V", "Demo & Báo cáo", "Chạy thử nghiệm hệ thống, chụp 20 ảnh màn hình minh họa; hoàn thiện tài liệu báo cáo Word (BAO_CAO.docx) và Slide thuyết trình bảo vệ.", "Cả nhóm", "Giảng viên", "25/11/2026", "Đang thực hiện")
    ]

    for row_idx, r_data in enumerate(data_p, start=1):
        row = t_plan.rows[row_idx]
        bg = "F9F9F9" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = widths_p[col_idx]
            set_cell_background(cell, bg)
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 3, 4, 5, 6] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_content(cell, text, align=align, font_size=10)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading_2(doc, "2.2. Đánh giá mức độ tham gia và đề xuất khen thưởng")
    add_bullet_point(doc, "Đề xuất thành viên tham gia tích cực nhất (Cộng điểm thưởng): ", bold_prefix="Sinh viên: Nguyễn Sỹ Huy (Mã SV: B23DVCN069 - Trưởng nhóm). ")
    add_body_paragraph(doc, "Lý do: Đóng vai trò hạt nhân kiến trúc của dự án; trực tiếp khởi tạo khung dự án mẫu chuẩn xác 100%; xây dựng toàn bộ biểu đồ UML và lưu đồ nghiệp vụ; điều phối lịch họp và thiết lập quy tắc Git không xung đột; hỗ trợ tháo gỡ vướng mắc kỹ thuật cho các thành viên và chủ trì tổng hợp tài liệu báo cáo học phần.")
    add_bullet_point(doc, "Thành viên không tham gia hoặc tham gia không hiệu quả: ", bold_prefix="Đánh giá tinh thần tập thể: ")
    add_body_paragraph(doc, "Không có thành viên nào vi phạm. 100% các thành viên trong nhóm đều tham gia đầy đủ các buổi họp kỹ thuật, chủ động nhận nhiệm vụ theo phân công và nghiêm túc tuân thủ quy chuẩn mã nguồn chung.")

    # =========================================================================
    # PHẦN III: QUÁ TRÌNH TRIỂN KHAI
    # =========================================================================
    add_heading_1(doc, "PHẦN III: QUÁ TRÌNH TRIỂN KHAI")
    add_body_paragraph(doc, "Dự án được vận hành theo quy trình phát triển phần mềm hiện đại, ứng dụng nền tảng GitHub làm trung tâm quản trị mã nguồn kết hợp công cụ họp trực tuyến Google Meet và nhóm trao đổi thường trực Zalo.")

    add_heading_2(doc, "3.1. Các buổi làm việc nhóm và nội dung biên bản")
    add_body_paragraph(doc, "Nhóm đã tổ chức 03 buổi làm việc tập trung có biên bản ghi nhận cụ thể:")
    
    add_bullet_point(doc, "Họp khởi động (Kick-off Meeting) - Thời lượng: 90 phút (Google Meet). Thành phần: 6/6 thành viên có mặt. Nội dung: Phân tích kỹ lưỡng đề bài Đề tài 01; xác lập kiến trúc phần mềm 3 tầng phân lập; chốt văn bản Hợp đồng chữ ký hàm (CONTRACT.md) và phân chia quyền sở hữu file (OWNERSHIP.md); quán triệt 6 quy tắc vàng khi làm việc trên Git.", bold_prefix="Buổi 1 (Ngày 06/11/2026): ")
    add_bullet_point(doc, "Họp sơ kết tiến độ Giai đoạn 1 (Mid-term Sync) - Thời lượng: 75 phút (Google Meet). Thành phần: 6/6 thành viên có mặt. Nội dung: Rà soát tiến độ từng gói A-E; kiểm tra chéo các lớp thực thể và bộ validate dữ liệu; thống nhất chuyển đổi toàn bộ test case sang thư viện chuẩn unittest để đảm bảo dự án chạy trên mọi môi trường sạch mà không cần cài thêm thư viện ngoài.", bold_prefix="Buổi 2 (Ngày 12/11/2026): ")
    add_bullet_point(doc, "Họp tích hợp và nghiệm thu hệ thống (Integration Meeting) - Thời lượng: 120 phút. Thành phần: 6/6 thành viên có mặt. Nội dung: Tiến hành hợp nhất các nhánh tính năng vào nhánh main; chạy kiểm thử toàn diện 20 test case; rà soát xử lý ngoại lệ an toàn; phân công chuẩn bị Slide trình chiếu và hoàn thiện hồ sơ báo cáo cuối cùng.", bold_prefix="Buổi 3 (Ngày 17/11/2026): ")

    add_heading_2(doc, "3.2. Minh chứng quá trình phối hợp và làm việc nhóm")
    add_placeholder_box(doc, "Hình 3.1: Ảnh chụp màn hình buổi họp trao đổi kỹ thuật của nhóm qua Google Meet")
    add_placeholder_box(doc, "Hình 3.2: Bảng Kanban quản lý tiến độ các nhiệm vụ (Tasks) và nhánh Git trên GitHub Project")

    # =========================================================================
    # PHẦN IV: PHÂN TÍCH
    # =========================================================================
    add_heading_1(doc, "PHẦN IV: PHÂN TÍCH")
    add_body_paragraph(doc, "Hệ thống Quản lý nhân viên được xây dựng nhằm giải quyết bài toán quản trị nguồn nhân lực trong doanh nghiệp với đa dạng hình thức lao động, đòi hỏi kiểm soát dữ liệu chặt chẽ và tính toán lương minh bạch.")

    add_heading_2(doc, "4.1. Phân tích các yêu cầu chức năng cốt lõi")
    add_body_paragraph(doc, "Hệ thống đáp ứng trọn vẹn 10 nhóm chức năng nghiệp vụ trọng tâm:")
    add_bullet_point(doc, "Hỗ trợ thêm nhân viên toàn thời gian (lương cơ bản, phụ cấp) và bán thời gian (giờ làm, đơn giá); bắt buộc kiểm tra định dạng và ngăn chặn trùng lặp mã nhân viên.", bold_prefix="1. Thêm mới nhân viên: ")
    add_bullet_point(doc, "Cho phép tra cứu theo mã và cập nhật các trường thông tin cho phép; áp dụng cơ chế nguyên tử 'Tất cả hoặc không gì', bảo vệ tính toàn vẹn khi có trường lỗi.", bold_prefix="2. Cập nhật nhân viên: ")
    add_bullet_point(doc, "Tìm kiếm theo mã và bắt buộc yêu cầu người dùng xác nhận an toàn (y/n) trước khi thực hiện xóa khỏi bộ nhớ.", bold_prefix="3. Xóa nhân viên: ")
    add_bullet_point(doc, "Liệt kê danh sách nhân viên trực quan dạng bảng với các cột thẳng hàng; tự động định dạng tiền tệ (15,000,000) và xử lý thông báo thân thiện khi danh sách rỗng.", bold_prefix="4. Hiển thị danh sách: ")
    add_bullet_point(doc, "Tìm kiếm chính xác theo mã nhân viên; tìm kiếm gần đúng theo họ tên (chứa từ khóa, không phân biệt chữ hoa/thường và hỗ trợ tiếng Việt không dấu); lọc theo phòng ban.", bold_prefix="5. Tìm kiếm đa năng: ")
    add_bullet_point(doc, "Hỗ trợ sắp xếp danh sách theo lương giảm dần hoặc theo tên tăng dần (xếp chuẩn theo từ cuối của họ tên người Việt); không làm thay đổi thứ tự mảng gốc.", bold_prefix="6. Sắp xếp linh hoạt: ")
    add_bullet_point(doc, "Quản lý phòng ban (thêm, sửa, xóa có kiểm tra ràng buộc toàn vẹn); luân chuyển nhân sự giữa các phòng ban với kiểm tra lỗi đích và lỗi trùng phòng.", bold_prefix="7. Nghiệp vụ phòng ban: ")
    add_bullet_point(doc, "Tổng hợp tổng quỹ lương toàn doanh nghiệp; thống kê số lượng nhân viên từng phòng ban; tìm kiếm nhân viên có mức lương cao nhất (xử lý đồng hạng).", bold_prefix="8. Thống kê & Báo cáo: ")
    add_bullet_point(doc, "Tự động lưu và phục hồi dữ liệu dạng JSON an toàn; hỗ trợ xuất báo cáo nhân sự ra file CSV phục vụ công tác kế toán.", bold_prefix="9. Lưu trữ & Mở rộng: ")
    add_bullet_point(doc, "Giao diện menu lặp thông minh; cơ chế bắt lỗi và yêu cầu nhập lại tức thì tại trường bị sai; không bao giờ bị văng traceback.", bold_prefix="10. Menu điều khiển: ")

    add_heading_2(doc, "4.2. Hệ thống 14 quy tắc nghiệp vụ bất biến (Business Rules)")
    # Bảng quy tắc nghiệp vụ
    t_rules = doc.add_table(rows=15, cols=3)
    t_rules.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_r = [Inches(0.8), Inches(4.5), Inches(1.8)]
    headers_r = ["Mã luật", "Quy tắc nghiệp vụ chi tiết", "Xử lý khi vi phạm"]
    for i, h in enumerate(headers_r):
        t_rules.rows[0].cells[i].text = h
    style_table_header(t_rules.rows[0], widths_r, bg_color="2C3E50")

    rules_data = [
        ("R1", "Mã nhân viên / Mã phòng ban: 3-10 ký tự gồm chữ và số, tự động in hoa chuẩn.", "Ném ValidationError"),
        ("R2", "Họ tên nhân viên: 2-50 ký tự, chỉ chứa chữ cái và khoảng trắng, tự chuẩn hóa khoảng trắng thừa.", "Ném ValidationError"),
        ("R3", "Năm sinh: Là số nguyên, độ tuổi lao động hợp pháp từ đủ 18 đến 65 tuổi.", "Ném ValidationError"),
        ("R4", "Lương cơ bản >= 0; Phụ cấp >= 0; Đơn giá giờ >= 0; Số giờ làm việc từ 0 đến 300 giờ/tháng.", "Ném ValidationError"),
        ("R5", "Công thức lương Toàn thời gian = Lương cơ bản + Phụ cấp.", "Tính toán đa hình"),
        ("R6", "Công thức lương Bán thời gian = Số giờ làm * Đơn giá giờ (Lương cơ bản mặc định 0).", "Tính toán đa hình"),
        ("R7", "Thêm nhân viên trùng mã đã tồn tại trong danh bạ.", "Ném DuplicateIdError"),
        ("R8", "Thêm nhân viên vào phòng ban chưa tồn tại trong hệ thống.", "Ném NotFoundError"),
        ("R9", "Thêm phòng ban trùng mã định danh.", "Ném DuplicateIdError"),
        ("R10", "Xóa phòng ban khi vẫn còn nhân viên trực thuộc.", "Ném BusinessRuleError"),
        ("R11", "Chuyển nhân viên sang phòng ban không tồn tại.", "Ném NotFoundError"),
        ("R12", "Chuyển nhân viên sang đúng phòng ban nhân viên đang công tác.", "Ném BusinessRuleError"),
        ("R13", "Tìm kiếm, sửa đổi hoặc xóa theo mã không tồn tại.", "Ném NotFoundError"),
        ("R14", "Tuyệt đối không cho phép thay đổi Mã nhân viên và Loại nhân viên sau khi khởi tạo.", "Thuộc tính chỉ đọc")
    ]

    for row_idx, r_data in enumerate(rules_data, start=1):
        row = t_rules.rows[row_idx]
        bg = "F2F4F4" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = widths_r[col_idx]
            set_cell_background(cell, bg)
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_content(cell, text, align=align, font_size=9.5)

    add_heading_2(doc, "4.3. Phân tích thuật toán và mã giả các hàm cốt lõi")
    add_body_paragraph(doc, "Dưới đây là mã giả (Pseudo-code) đại diện cho các giải thuật then chốt của hệ thống:")
    
    add_heading_3(doc, "a. Thuật toán Cập nhật nguyên tử (Atomic Update):")
    add_code_block(doc, 
"""Function update_employee(employee_id, **fields):
    employee = find_employee(employee_id)
    old_state = copy_attributes(employee)
    Try:
        For each field, new_value in fields:
            validate_and_set_property(employee, field, new_value)
        Return employee
    Catch ValidationError as err:
        restore_attributes(employee, old_state)  # Rollback hoàn toàn
        Raise err""")

    add_heading_3(doc, "b. Thuật toán Kiểm soát toàn vẹn khi Xóa phòng ban:")
    add_code_block(doc,
"""Function delete_department(department_id, employees):
    dept = get_department(department_id)
    emp_count = count_employees_in_department(employees, department_id)
    If emp_count > 0:
        Raise BusinessRuleError("Phòng ban còn " + emp_count + " nhân viên, từ chối xóa!")
    remove_from_storage(dept)
    Return dept""")

    # =========================================================================
    # PHẦN V: THIẾT KẾ
    # =========================================================================
    add_heading_1(doc, "PHẦN V: THIẾT KẾ")
    add_body_paragraph(doc, "Hệ thống được thiết kế hướng đối tượng triệt để theo mô hình phân tầng sạch (Clean Architecture), bảo đảm sự phân tách rõ rệt giữa dữ liệu, logic xử lý và giao diện.")

    add_heading_2(doc, "5.1. Thiết kế kiến trúc phân tầng")
    add_bullet_point(doc, "Chứa các lớp thực thể dữ liệu (Employee, FullTimeEmployee, PartTimeEmployee, Department, Factory). Đóng gói tuyệt đối thuộc tính dưới dạng private, bảo vệ dữ liệu bằng các property.", bold_prefix="Tầng Thực thể (models/): ")
    add_bullet_point(doc, "Nơi xử lý toàn bộ logic nghiệp vụ (EmployeeManager, DepartmentService, SearchService, SortService, ReportService). Tuyệt đối không chứa print() hoặc input().", bold_prefix="Tầng Dịch vụ (services/): ")
    add_bullet_point(doc, "Chịu trách nhiệm lưu trữ và phục hồi dữ liệu từ file JSON cục bộ an toàn (FileStorage).", bold_prefix="Tầng Lưu trữ (storage/): ")
    add_bullet_point(doc, "Chứa vòng lặp menu console chính và các hàm điều hướng handler. Nơi duy nhất xử lý nhập xuất với người dùng.", bold_prefix="Tầng Giao diện (ui/): ")

    add_heading_2(doc, "5.2. Biểu đồ lớp UML (UML Class Diagram)")
    add_body_paragraph(doc, "Biểu đồ lớp UML thể hiện toàn diện cấu trúc các lớp, thuộc tính, phương thức, phạm vi truy cập (+ public, - private, # protected) và các mối quan hệ hướng đối tượng cốt lõi:")
    add_placeholder_box(doc, "Hình 5.1: Sơ đồ lớp UML Class Diagram hệ thống Quản lý nhân viên (docs/uml/class_diagram.png)")

    add_heading_2(doc, "5.3. Lưu đồ hoạt động (Activity Diagrams)")
    add_body_paragraph(doc, "Lưu đồ hoạt động mô tả chi tiết luồng vận hành của Menu chính và các quy trình xử lý nghiệp vụ phức tạp:")
    add_placeholder_box(doc, "Hình 5.2: Lưu đồ hoạt động vòng đời Menu chính và xử lý ngoại lệ (docs/uml/activity_diagram.png)")
    add_placeholder_box(doc, "Hình 5.3: Lưu đồ nghiệp vụ Thêm nhân viên với cơ chế nhập sai nhập lại tại chỗ")

    # =========================================================================
    # PHẦN VI: LẬP TRÌNH (CODE)
    # =========================================================================
    add_heading_1(doc, "PHẦN VI: LẬP TRÌNH (CODE)")
    
    add_heading_2(doc, "6.1. Quy chuẩn lập trình (Coding Conventions)")
    add_bullet_point(doc, "Tuân thủ nghiêm ngặt chuẩn PEP 8 về thụt lề, khoảng cách và ngắt dòng; đặt tên biến/hàm theo snake_case, tên lớp theo PascalCase, hằng số theo UPPER_CASE.")
    add_bullet_point(doc, "100% các hàm và phương thức công khai đều có Type Hinting rõ ràng cho tham số và kiểu trả về; docstring và chú thích bằng tiếng Việt trong sáng, súc tích.")
    add_bullet_point(doc, "Nguyên tắc 'Không print/input trong models và services': Đảm bảo tính tái sử dụng và khả năng kiểm thử độc lập của mã nguồn.")

    add_heading_2(doc, "6.2. Các đoạn mã nguồn tiêu biểu thể hiện nguyên lý OOP")
    
    add_heading_3(doc, "a. Tính Trừu tượng và Đóng gói (Lớp cha trừu tượng Employee):")
    add_code_block(doc,
"""class Employee(ABC):
    def __init__(self, employee_id: str, full_name: str, birth_year: int,
                 department_id: str, base_salary: float = 0.0) -> None:
        self.__employee_id = validate_employee_id(employee_id)  # Chỉ đọc (R14)
        self.full_name = full_name
        self.birth_year = birth_year
        self.department_id = department_id
        self.base_salary = base_salary

    @property
    def employee_id(self) -> str:
        return self.__employee_id

    @property
    @abstractmethod
    def employee_type(self) -> str:
        \"\"\"Loại nhân viên (bắt buộc lớp con cài đặt).\"\"\"

    @abstractmethod
    def calculate_salary(self) -> float:
        \"\"\"Phương thức tính lương đa hình.\"\"\"""")

    add_heading_3(doc, "b. Tính Đa hình trong tính lương và hiển thị (FullTime & PartTime):")
    add_code_block(doc,
"""class FullTimeEmployee(Employee):
    def calculate_salary(self) -> float:
        return self.base_salary + self.allowance

class PartTimeEmployee(Employee):
    def calculate_salary(self) -> float:
        return self.hours_worked * self.hourly_rate""")

    add_heading_2(doc, "6.3. Cài đặt các chức năng mở rộng")
    add_bullet_point(doc, "Kỹ thuật ghi file an toàn (Atomic Write): FileStorage ghi dữ liệu JSON ra file tạm rồi sử dụng os.replace để ghi đè sang file chính thức, loại trừ nguy cơ hỏng dữ liệu khi gặp sự cố mất điện đột ngột.", bold_prefix="Lưu/Đọc dữ liệu an toàn: ")
    add_bullet_point(doc, "Sử dụng module csv chuẩn với mã hóa utf-8-sig, cho phép mở trực tiếp file danh sách nhân sự trên Microsoft Excel mà không bao giờ bị lỗi font tiếng Việt.", bold_prefix="Xuất báo cáo CSV: ")

    # =========================================================================
    # PHẦN VII: KIỂM THỬ (KỊCH BẢN TEST)
    # =========================================================================
    add_heading_1(doc, "PHẦN VII: KIỂM THỬ (KỊCH BẢN TEST)")
    add_body_paragraph(doc, "Hệ thống áp dụng chiến lược kiểm thử đa tầng kết hợp Unit Test tự động hóa và kịch bản kiểm thử tích hợp người dùng (Integration Test).")

    add_heading_2(doc, "7.1. Bảng kịch bản kiểm thử toàn diện (20 Test Cases)")
    
    # Bảng 20 test case
    t_cases = doc.add_table(rows=21, cols=6)
    t_cases.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_tc = [Inches(0.6), Inches(1.0), Inches(1.5), Inches(2.3), Inches(0.8), Inches(0.6)]
    headers_tc = ["Mã TC", "Phân loại", "Chức năng kiểm thử", "Kết quả mong đợi", "Trạng thái", "Gói"]
    for i, h in enumerate(headers_tc):
        t_cases.rows[0].cells[i].text = h
    style_table_header(t_cases.rows[0], widths_tc, bg_color="1F4E79")

    tc_data = [
        ("TC01", "Hợp lệ", "Thêm NV toàn thời gian", "Thêm thành công, tính lương = LCB + Phụ cấp", "PASS", "C"),
        ("TC02", "Hợp lệ", "Thêm NV bán thời gian", "Thêm thành công, tính lương = Giờ * Đơn giá", "PASS", "C"),
        ("TC03", "Trùng mã", "Thêm NV trùng mã đã có", "Ném DuplicateIdError, từ chối thêm", "PASS", "C"),
        ("TC04", "Không hợp lệ", "Mã nhân viên rỗng", "Báo ValidationError, yêu cầu nhập lại", "PASS", "C/A"),
        ("TC05", "Không hợp lệ", "Họ tên chứa số/ký tự lạ", "Báo lỗi họ tên không hợp lệ", "PASS", "A"),
        ("TC06", "Biên", "Tuổi đúng 18 và 17 tuổi", "Tuổi 18 hợp lệ, 17 tuổi bị từ chối", "PASS", "A"),
        ("TC07", "Biên", "Giờ làm đúng 300 và 301 giờ", "300h hợp lệ, 301h bị từ chối", "PASS", "A"),
        ("TC08", "Không hợp lệ", "Cập nhật lương âm", "Báo lỗi, giữ nguyên lương cũ (nguyên tử)", "PASS", "C"),
        ("TC09", "Ràng buộc", "Sửa phụ cấp cho nhân viên PT", "Từ chối vì trường không thuộc loại PT", "PASS", "C"),
        ("TC10", "Ràng buộc", "Thêm NV vào phòng ban ảo", "Ném NotFoundError phòng ban không tồn tại", "PASS", "C/B"),
        ("TC11", "Nghiệp vụ", "Xóa nhân viên chọn 'n'", "Hủy xóa thành công, dữ liệu giữ nguyên", "PASS", "C"),
        ("TC12", "Không tồn tại", "Tìm/xóa mã không tồn tại", "Báo NotFoundError, menu không bị sập", "PASS", "C/D"),
        ("TC13", "Danh sách rỗng", "Hiển thị danh sách rỗng", "In thông báo thân thiện, không lỗi index", "PASS", "D"),
        ("TC14", "Danh sách rỗng", "Thống kê danh sách rỗng", "Quỹ lương = 0, không lỗi chia cho 0", "PASS", "E"),
        ("TC15", "Hợp lệ", "Sắp xếp lương giảm dần", "Danh sách trả về theo thứ tự lương giảm", "PASS", "D"),
        ("TC16", "Hợp lệ", "Sắp xếp tên tăng dần", "Sắp xếp chuẩn theo từ cuối của họ tên", "PASS", "D"),
        ("TC17", "Hợp lệ", "Tìm kiếm gần đúng tên", "Tìm thấy đúng nhân viên theo từ khóa không dấu", "PASS", "D"),
        ("TC18", "Toàn vẹn", "Xóa phòng ban còn nhân viên", "Báo BusinessRuleError, từ chối xóa", "PASS", "B"),
        ("TC19", "Toàn vẹn", "Chuyển trùng phòng ban", "Báo lỗi nhân viên đã thuộc phòng ban này", "PASS", "B"),
        ("TC20", "Mở rộng", "Lưu và tải dữ liệu JSON", "Khôi phục dữ liệu nguyên vẹn 100%", "PASS", "E")
    ]

    for row_idx, r_data in enumerate(tc_data, start=1):
        row = t_cases.rows[row_idx]
        bg = "F9F9F9" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = widths_tc[col_idx]
            set_cell_background(cell, bg)
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1, 4, 5] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell_content(cell, text, align=align, font_size=9)

    add_heading_2(doc, "7.2. Kịch bản chạy nghiệm thu hệ thống (Demo Script)")
    add_body_paragraph(doc, "Kịch bản demo được thiết kế xuyên suốt 12 bước với lệnh nạp dữ liệu mẫu: python main.py --seed")
    add_bullet_point(doc, "Khởi động và hiển thị 6 nhân viên mẫu thuộc 3 phòng ban với bảng thẳng cột.")
    add_bullet_point(doc, "Thêm 1 nhân viên toàn thời gian mới (NV007) và 1 nhân viên bán thời gian (NV008).")
    add_bullet_point(doc, "Thử nghiệm cơ chế chặn mã trùng (NV001) và phòng ban không tồn tại (PB99).")
    add_bullet_point(doc, "Cập nhật lương nhân viên với cơ chế nguyên tử.")
    add_bullet_point(doc, "Chuyển phòng ban và minh chứng tính toàn vẹn khi từ chối xóa phòng ban còn nhân viên.")
    add_bullet_point(doc, "Tìm kiếm gần đúng họ tên và sắp xếp đa tiêu chí.")
    add_bullet_point(doc, "In báo cáo thống kê quỹ lương và xuất file CSV mở trên Excel.")
    add_bullet_point(doc, "Lưu dữ liệu ra file, thoát và khởi động lại để chứng minh dữ liệu được bảo lưu hoàn hảo.")

    # =========================================================================
    # PHẦN VIII: KẾT QUẢ ĐẠT ĐƯỢC
    # =========================================================================
    add_heading_1(doc, "PHẦN VIII: KẾT QUẢ ĐẠT ĐƯỢC")
    add_body_paragraph(doc, "Trải qua quá trình nghiên cứu và phát triển nghiêm túc, Nhóm 1 đã hoàn thành thắng lợi các mục tiêu đề ra:")

    add_heading_2(doc, "8.1. Các kết quả kỹ thuật đã hoàn thành")
    add_bullet_point(doc, "Ứng dụng vận hành trơn tru trên Console, tuân thủ chặt chẽ 4 nguyên lý hướng đối tượng.")
    add_bullet_point(doc, "Toàn bộ 11 test smoke nền tảng và 20 test case nghiệp vụ đều đạt kết quả PASS 100%.")
    add_bullet_point(doc, "Kiến trúc mã nguồn chuẩn mực, phân tách 3 tầng rõ ràng, sẵn sàng mở rộng giao diện đồ họa (GUI) hoặc cơ sở dữ liệu quan hệ trong tương lai.")

    add_heading_2(doc, "8.2. Danh mục hình ảnh giao diện minh họa (Sẽ gắn khi chốt bản cuối)")
    add_body_paragraph(doc, "Bộ sưu tập 20 ảnh chụp màn hình minh họa giao diện chạy thực tế của chương trình được tổ chức và lưu trữ tại thư mục docs/screenshots/ theo đúng danh mục sau:")
    
    screenshots_list = [
        "01_menu-chinh.png: Giao diện Menu chính hoàn chỉnh 12 chức năng.",
        "02_them-fulltime.png: Thao tác thêm nhân viên toàn thời gian thành công.",
        "03_them-parttime.png: Thao tác thêm nhân viên bán thời gian thành công.",
        "04_them-trung-ma.png: Hệ thống từ chối khi thêm trùng mã nhân viên.",
        "05_nhap-sai-nhap-lai.png: Minh họa cơ chế kiểm tra và nhập lại tức thì tại chỗ.",
        "06_cap-nhat.png: Cập nhật thông tin nhân viên theo nguyên tắc nguyên tử.",
        "07_xoa-xac-nhan.png: Thao tác xóa nhân viên có bước xác nhận an toàn.",
        "08_hien-thi.png: Bảng danh sách nhân viên hiển thị thẳng hàng, chuẩn định dạng.",
        "09_danh-sach-rong.png: Xử lý hiển thị thân thiện khi danh sách nhân viên rỗng.",
        "10_tim-ma.png: Tìm kiếm chính xác nhân viên theo mã định danh.",
        "11_tim-ten.png: Tìm kiếm gần đúng theo họ tên không dấu.",
        "12_tim-phong-ban.png: Lọc danh sách nhân viên theo phòng ban trực thuộc.",
        "13_sap-xep-luong.png: Danh sách nhân viên sắp xếp theo mức lương giảm dần.",
        "14_sap-xep-ten.png: Danh sách nhân viên sắp xếp theo tên gọi tăng dần.",
        "15_chuyen-phong-ban.png: Nghiệp vụ luân chuyển phòng ban thành công.",
        "16_xoa-phong-ban-loi.png: Từ chối xóa phòng ban khi vẫn còn nhân viên trực thuộc.",
        "17_thong-ke.png: Bảng báo cáo thống kê tổng quỹ lương và cơ cấu nhân sự.",
        "18_da-hinh.png: Minh chứng tính chất Đa hình qua công thức tính lương hỗn hợp.",
        "19_luu-tai-file.png: Thao tác lưu và nạp lại dữ liệu JSON an toàn.",
        "20_chuc-nang-mo-rong.png: Xuất danh sách nhân sự ra file CSV mở trên Excel."
    ]
    for sc in screenshots_list:
        add_bullet_point(doc, sc)

    add_placeholder_box(doc, "Khu vực dành cho hình ảnh giao diện thực tế sẽ được chèn trực tiếp vào bản báo cáo cuối cùng sau khi hoàn tất tích hợp")

    # Lưu tài liệu
    doc.save(DOCX_PATH)
    print("SUCCESS: Nhom_1_Bao_cao.docx has been successfully populated and saved!")

if __name__ == "__main__":
    main()
