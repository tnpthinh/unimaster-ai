"""
Seed sample university courses, multiple-choice questions, and flashcards into UniMaster AI
"""
from database import init_db, add_subject, add_question, add_flashcard, get_all_subjects

def seed_everything():
    init_db()
    existing = get_all_subjects()
    if len(existing) > 0:
        print("Database already has subjects, skipping seed.")
        return

    print("Seeding university subjects and questions...")

    # ==========================================
    # 1. Triết học Mác - Lênin
    # ==========================================
    s1 = add_subject(
        code="MLN101",
        name="Triết học Mác - Lênin",
        icon="🧠",
        category="Lý luận chính trị",
        description="Môn học nền tảng về thế giới quan duy vật biện chứng và phương pháp luận biện chứng duy vật."
    )

    q_triet = [
        (
            "Vấn đề cơ bản của triết học là gì?",
            "Vấn đề mối quan hệ giữa vật chất và ý thức (tư duy và tồn tại)",
            "Vấn đề nguồn gốc của vũ trụ và loài người",
            "Vấn đề đạo đức và chuẩn mực xã hội",
            "Vấn đề phương pháp nhận thức khoa học",
            "A",
            "Theo Ăngghen, vấn đề cơ bản lớn của mọi triết học là vấn đề mối quan hệ giữa tư duy và tồn tại (giữa ý thức và vật chất)."
        ),
        (
            "Định nghĩa vật chất của V.I.Lênin nhấn mạnh thuộc tính quan trọng nhất của vật chất là gì?",
            "Tính vận động và biến đổi liên tục",
            "Thuộc tính thực tại khách quan (tồn tại độc lập với ý thức)",
            "Tính có khối lượng và cấu trúc nguyên tử",
            "Tính có thể đo lường và định lượng",
            "B",
            "Vật chất là một phạm trù triết học dùng để chỉ thực tại khách quan, được đem lại cho con người trong cảm giác, không phụ thuộc vào ý thức."
        ),
        (
            "Quy luật nào vạch ra NGUỒN GỐC và ĐỘNG LỰC của sự phát triển?",
            "Quy luật chuyển hóa từ những thay đổi về lượng dẫn đến sự thay đổi về chất",
            "Quy luật phủ định của phủ định",
            "Quy luật thống nhất và đấu tranh của các mặt đối lập (Quy luật mâu thuẫn)",
            "Quy luật nhân quả",
            "C",
            "Quy luật mâu thuẫn là hạt nhân của phép biện chứng, vạch ra nguồn gốc và động lực nội tại của sự vận động và phát triển."
        ),
        (
            "Khái niệm 'Điểm nút' trong quy luật lượng - chất biểu thị điều gì?",
            "Thời điểm mâu thuẫn lên tới đỉnh điểm",
            "Khoảng giới hạn mà sự thay đổi về lượng chưa làm chất biến đổi",
            "Thời điểm mà tại đó sự thay đổi về lượng đạt tới giới hạn để xảy ra bước nhảy biến đổi về chất",
            "Giai đoạn bắt đầu của sự tích lũy lượng mới",
            "C",
            "Điểm nút là giới hạn mà tại đó sự tích lũy về lượng dẫn đến sự thay đổi căn bản về chất thông qua bước nhảy."
        ),
        (
            "Thực tiễn đóng vai trò gì đối với nhận thức?",
            "Chỉ là công cụ kiểm tra phụ trợ cho lý thuyết",
            "Là cơ sở, động lực, mục đích của nhận thức và là tiêu chuẩn của chân lý",
            "Là sản phẩm thuần túy do nhận thức tạo ra",
            "Không có vai trò quyết định đến nhận thức khoa học",
            "B",
            "Thực tiễn là điểm xuất phát, nguồn động lực thúc đẩy nhận thức phát triển, là đích đến của nhận thức và thước đo chân lý duy nhất."
        )
    ]
    for q in q_triet:
        add_question(s1, q[0], q[1], q[2], q[3], q[4], q[5], q[6])

    fc_triet = [
        ("Vật chất (Lênin)", "Phạm trù triết học chỉ thực tại khách quan được đem lại trong cảm giác, tồn tại độc lập với ý thức con người.", "Thực tại khách quan"),
        ("3 Quy luật biện chứng", "1. Lượng - Chất (Cách thức) | 2. Mâu thuẫn (Nguồn gốc/Động lực) | 3. Phủ định của phủ định (Khuynh hướng)", "Cách thức - Nguồn gốc - Khuynh hướng"),
        ("Thực tiễn", "Toàn bộ hoạt động vật chất - cảm tính, có tính lịch sử - xã hội của con người nhằm cải tạo tự nhiên và xã hội.", "Sản xuất vật chất, CT-XH, Thực nghiệm KH")
    ]
    for fc in fc_triet:
        add_flashcard(s1, fc[0], fc[1], fc[2])

    # ==========================================
    # 2. Pháp luật đại cương
    # ==========================================
    s2 = add_subject(
        code="PLDC101",
        name="Pháp luật đại cương",
        icon="⚖️",
        category="Khoa học xã hội",
        description="Kiến thức nền tảng về Nhà nước, hệ thống pháp luật, vi phạm pháp luật và trách nhiệm pháp lý."
    )

    q_pldc = [
        (
            "Cấu trúc của một quy phạm pháp luật điển hình gồm các bộ phận nào?",
            "Chủ thể, Khách thể, Nội dung",
            "Giả định, Quy định, Chế tài",
            "Mặt khách quan, Mặt chủ quan, Chủ thể, Khách thể",
            "Mở đầu, Nội dung, Kết luận",
            "B",
            "Cấu trúc quy phạm pháp luật cơ bản gồm 3 bộ phận: Giả định (hoàn cảnh, điều kiện), Quy định (mệnh lệnh hành vi), Chế tài (hậu quả xử lý)."
        ),
        (
            "Yếu tố nào sau đây thuộc MẶT CHỦ QUAN của vi phạm pháp luật?",
            "Hành vi vi phạm và thiệt hại cho xã hội",
            "Lỗi (cố ý hoặc vô ý), động cơ và mục đích vi phạm",
            "Mối quan hệ xã hội được pháp luật bảo vệ",
            "Độ tuổi và khả năng nhận thức của người vi phạm",
            "B",
            "Mặt chủ quan thể hiện trạng thái tâm lý bên trong của chủ thể khi thực hiện hành vi, bao gồm: Lỗi, Động cơ, Mục đích."
        ),
        (
            "Hình thức văn bản quy phạm pháp luật nào do Quốc hội Việt Nam ban hành?",
            "Nghị định và Nghị quyết",
            "Hiến pháp, Luật và Nghị quyết của Quốc hội",
            "Quyết định của Thủ tướng Chính phủ",
            "Thông tư của các Bộ trưởng",
            "B",
            "Quốc hội là cơ quan quyền lực cao nhất ban hành Hiến pháp, Luật và các Nghị quyết của Quốc hội."
        )
    ]
    for q in q_pldc:
        add_question(s2, q[0], q[1], q[2], q[3], q[4], q[5], q[6])

    fc_pldc = [
        ("Cấu trúc QPPL", "Giả định (Ai? Ở đâu?), Quy định (Được làm gì/Phải làm gì?), Chế tài (Nếu vi phạm thì bị xử lý ra sao?)", "3 phần G-Q-C"),
        ("4 Yếu tố cấu thành VPPL", "1. Mặt khách quan (hành vi, hậu quả) | 2. Mặt chủ quan (lỗi cố ý/vô ý) | 3. Chủ thể (độ tuổi, năng lực) | 4. Khách thể (quan hệ xã hội bị xâm hại)", "Khách quan, Chủ quan, Chủ thể, Khách thể")
    ]
    for fc in fc_pldc:
        add_flashcard(s2, fc[0], fc[1], fc[2])

    # ==========================================
    # 3. Giải tích & Toán Cao Cấp
    # ==========================================
    s3 = add_subject(
        code="MATH101",
        name="Giải tích & Đại số tuyến tính",
        icon="📐",
        category="Khoa học tự nhiên",
        description="Ma trận, định thức, hệ phương trình tuyến tính, giới hạn, đạo hàm và tích phân nhiều biến."
    )

    q_math = [
        (
            "Nếu ma trận vuông A cấp n có định thức det(A) = 3, thì det(2A) bằng bao nhiêu?",
            "6",
            "3 * 2^n",
            "6^n",
            "3^n * 2",
            "B",
            "Theo tính chất định thức: det(k*A) = k^n * det(A). Ở đây k=2, nên det(2A) = 2^n * 3."
        ),
        (
            "Điều kiện cần và đủ để hệ phương trình tuyến tính thuần nhất AX = 0 có nghiệm không tầm thường là gì?",
            "det(A) != 0",
            "rank(A) = n (hạng bằng số ẩn)",
            "det(A) = 0 (ma trận A suy biến, rank(A) < n)",
            "A là ma trận đơn vị",
            "C",
            "Hệ phương trình thuần nhất AX=0 luôn có nghiệm tầm thường X=0. Để có nghiệm không tầm thường thì det(A) phải bằng 0."
        ),
        (
            "Tích phân bất định $\\int x \\cdot e^x dx$ có kết quả là gì?",
            "$e^x (x - 1) + C$",
            "$e^x (x + 1) + C$",
            "$\\frac{x^2}{2} e^x + C$",
            "$x e^x - x + C$",
            "A",
            "Dùng phương pháp từng phần: đặt u = x => du = dx, dv = e^x dx => v = e^x. Ta có: uv - \\int v du = x*e^x - e^x + C = e^x(x - 1) + C."
        )
    ]
    for q in q_math:
        add_question(s3, q[0], q[1], q[2], q[3], q[4], q[5], q[6])

    fc_math = [
        ("Quy tắc nhân ma trận", "Số cột của ma trận A PHẢI BẰNG số dòng của ma trận B: (m x k) * (k x n) = (m x n)", "Cột A = Dòng B"),
        ("Tích phân từng phần", "∫ u dv = u*v - ∫ v du (Đặt u theo thứ tự: Nhất lô, nhì đa, tam lượng, tứ mũ)", "u*v - ∫ v du")
    ]
    for fc in fc_math:
        add_flashcard(s3, fc[0], fc[1], fc[2])

    # ==========================================
    # 4. Cấu trúc dữ liệu & Lập trình C++
    # ==========================================
    s4 = add_subject(
        code="CS101",
        name="Lập trình & Cấu trúc dữ liệu",
        icon="💻",
        category="Công nghệ thông tin",
        description="Ngôn ngữ C/C++, con trỏ, danh sách liên kết, ngăn xếp (Stack), hàng đợi (Queue), Cây và Đồ thị."
    )

    q_cs = [
        (
            "Độ phức tạp thời gian trung bình của thuật toán tìm kiếm nhị phân (Binary Search) trên mảng đã sắp xếp là gì?",
            "O(1)",
            "O(n)",
            "O(log n)",
            "O(n log n)",
            "C",
            "Tìm kiếm nhị phân chia đôi không gian tìm kiếm sau mỗi bước, do đó độ phức tạp là O(log n)."
        ),
        (
            "Cấu trúc dữ liệu Stack (Ngăn xếp) hoạt động theo nguyên lý nào?",
            "FIFO (First In First Out)",
            "LIFO (Last In First Out)",
            "Random Access",
            "Priority Ordering",
            "B",
            "Stack hoạt động theo cơ chế vào sau - ra trước (Last In, First Out). Phần tử thêm vào cuối cùng sẽ được lấy ra đầu tiên."
        ),
        (
            "Trong C++, điều gì xảy ra nếu cấp phát bộ nhớ bằng `new` nhưng không dùng `delete` để giải phóng?",
            "Chương trình tự động giải phóng khi thoát hàm",
            "Gây hiện tượng rò rỉ bộ nhớ (Memory Leak)",
            "Trình biên dịch báo lỗi cú pháp (Syntax Error)",
            "Bộ nhớ heap bị xóa ngay lập tức",
            "B",
            "C++ không có bộ gom rác tự động (Garbage Collector). Nếu không `delete`, vùng nhớ đó vẫn bị chiếm dụng gây memory leak."
        )
    ]
    for q in q_cs:
        add_question(s4, q[0], q[1], q[2], q[3], q[4], q[5], q[6])

    fc_cs = [
        ("Stack vs Queue", "Stack: LIFO (vào sau ra trước, ví dụ Ctrl+Z) | Queue: FIFO (vào trước ra trước, ví dụ xếp hàng in ấn)", "LIFO vs FIFO"),
        ("Con trỏ trong C++", "`int* p` lưu địa chỉ ô nhớ. `&x` lấy địa chỉ của x. `*p` truy xuất giá trị tại ô nhớ p trỏ đến.", "*p: giá trị, &x: địa chỉ")
    ]
    for fc in fc_cs:
        add_flashcard(s4, fc[0], fc[1], fc[2])

    print("Seed completed successfully!")

if __name__ == "__main__":
    seed_everything()
