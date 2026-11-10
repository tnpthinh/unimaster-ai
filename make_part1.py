# -*- coding: utf-8 -*-
"""
Tập dữ liệu 200 câu hỏi trắc nghiệm chuẩn y khoa cho:
BÀI 2: CHUYỂN HÓA PROTID VÀ MỘT SỐ XÉT NGHIỆM ĐÁNH GIÁ CHỨC NĂNG THẬN
Giáo trình Thực hành Hóa sinh - Đại học Y Dược Cần Thơ (CTUMP)
"""

QUESTIONS_PART1 = [
    # --- PHẦN 1: THÍ NGHIỆM 1 - ĐỊNH LƯỢNG PROTEIN TOÀN PHẦN (BIURET) (40 CÂU) ---
    {
        "q": "Nguyên tắc của phương pháp Biuret dùng để định lượng protein toàn phần trong huyết thanh là gì?",
        "a": "Trong môi trường kiềm, liên kết peptid của protein phản ứng với $\\ce{Cu^2+}$ tạo phức hợp màu tím hồng",
        "b": "Trong môi trường acid, protein phản ứng với ninhydrin tạo phức hợp màu tím xanh",
        "c": "Trong môi trường kiềm, acid amin phản ứng với acid picric tạo phức hợp màu vàng cam",
        "d": "Trong môi trường trung tính, protein bị oxy hóa bởi enzym peroxidase tạo màu hồng cánh sen",
        "c_opt": "A",
        "exp": "Theo giáo trình thực hành: Trong môi trường kiềm, Protein trong huyết thanh phản ứng với $\\ce{Cu^2+}$ tạo thành phức hợp màu tím hồng. Cường độ màu tỉ lệ thuận với nồng độ protein trong huyết thanh.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Phương pháp đo quang áp dụng trong kỹ thuật định lượng protein toàn phần bằng phản ứng Biuret là gì?",
        "a": "Phương pháp đo điểm cuối (End-point)",
        "b": "Phương pháp đo động học 2 điểm (Fixed-time kinetic)",
        "c": "Phương pháp đo động học liên tục (Continuous monitoring)",
        "d": "Phương pháp đo độ đục miễn dịch (Immunoturbidimetry)",
        "c_opt": "A",
        "exp": "Phản ứng Biuret tạo phức hợp màu bền sau 20 phút và đo mật độ quang 1 lần tại điểm kết thúc phản ứng nên thuộc phương pháp đo điểm cuối.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Màu sắc của phức hợp tạo thành trong phản ứng Biuret định lượng protein là gì?",
        "a": "Màu tím hồng",
        "b": "Màu vàng cam",
        "c": "Màu xanh lục",
        "d": "Màu hồng cánh sen",
        "c_opt": "A",
        "exp": "Phức chất giữa $\\ce{Cu^2+}$ và các liên kết peptid trong môi trường kiềm có màu tím hồng đặc trưng.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Bước sóng ($\\lambda$) thích hợp nhất để đo mật độ quang của phức hợp màu Biuret là bao nhiêu?",
        "a": "530 nm",
        "b": "505 nm",
        "c": "340 nm",
        "d": "492 nm",
        "c_opt": "A",
        "exp": "Theo quy trình thực hành: Đo mật độ quang của phức hợp màu sau phản ứng bằng máy quang phổ kế ở bước sóng 530 nm.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Điều kiện tối thiểu về cấu trúc phân tử để một chất cho phản ứng Biuret dương tính là gì?",
        "a": "Có từ 2 liên kết peptid trở lên trong phân tử (từ tripeptid trở lên)",
        "b": "Có ít nhất 1 liên kết peptid (dipeptid)",
        "c": "Chỉ cần chứa nhóm amin tự do ($\\ce{-NH2}$)",
        "d": "Phải có vòng thơm chứa nhân benzen",
        "c_opt": "A",
        "exp": "Phản ứng Biuret đòi hỏi phân tử phải có ít nhất 2 liên kết peptid kề nhau (từ tripeptid trở lên). Dipeptid và acid amin tự do không cho phản ứng Biuret.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thành phần thuốc thử Gornall dùng trong phản ứng Biuret gồm những hóa chất nào?",
        "a": "$\\ce{CuSO4}$, Na K Tartrat, NaOH và Kali Iodua (KI)",
        "b": "$\\ce{CuSO4}$, Acid Picric, NaOH và NaCl",
        "c": "$\\ce{FeSO4}$, Na K Tartrat, KOH và KI",
        "d": "$\\ce{CuSO4}$, DHBS, 4-AAP và Pipes buffer",
        "c_opt": "A",
        "exp": "Thuốc thử Gornall gồm: $\\ce{CuSO4}$ 1,5g; Na K Tartrat 6g; Nước cất 500ml; 300ml dd NaOH 2,5N; 1g Kali Iodua (KI); thêm nước cất vừa đủ 1000ml.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Vai trò của $\\ce{CuSO4}$ trong thuốc thử Gornall (Biuret) là gì?",
        "a": "Cung cấp ion $\\ce{Cu^2+}$ để tạo phức phối trí với liên kết peptid",
        "b": "Tạo môi trường acid cho phản ứng",
        "c": "Ngăn cản sự kết tủa của protein",
        "d": "Chất chỉ thị màu thay đổi theo pH",
        "c_opt": "A",
        "exp": "$\\ce{CuSO4}$ phân ly cung cấp ion đồng(II) $\\ce{Cu^2+}$ phản ứng với nguyên tử N trong các liên kết peptid tạo phức màu tím hồng.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Vai trò của muối Natri Kali Tartrat (Na K Tartrat) trong thuốc thử Gornall là gì?",
        "a": "Giữ ion $\\ce{Cu^2+}$ tan trong môi trường kiềm, ngăn tạo kết tủa $\\ce{Cu(OH)2}$",
        "b": "Tạo phức màu tím hồng với protein",
        "c": "Tạo môi trường kiềm cho phản ứng",
        "d": "Khử $\\ce{Cu^2+}$ thành $\\ce{Cu^+}$",
        "c_opt": "A",
        "exp": "Na K Tartrat (muối Rochelle) là chất tạo phức chelat giữ $\\ce{Cu^2+}$ ở trạng thái hòa tan, ngăn chặn ion $\\ce{Cu^2+}$ phản ứng với $\\ce{OH^-}$ tạo kết tủa $\\ce{Cu(OH)2}$ lắng xuống đáy.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Vai trò của Kali Iodua (KI) trong thuốc thử Gornall là gì?",
        "a": "Chất chống oxy hóa/ổn định, ngăn chặn sự tự khử của ion $\\ce{Cu^2+}$",
        "b": "Tăng cường độ màu của phản ứng",
        "c": "Tạo môi trường kiềm mạnh",
        "d": "Phân cắt liên kết peptid của protein",
        "c_opt": "A",
        "exp": "Kali Iodua (KI) đóng vai trò là chất ổn định (stabilizer), ngăn ngừa sự tự oxy hóa - khử của ion đồng $\\ce{Cu^2+}$ giúp thuốc thử bền lâu.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nồng độ của dung dịch NaOH được bổ sung vào khi pha 1000 ml thuốc thử Gornall là bao nhiêu?",
        "a": "300 ml dung dịch NaOH 2,5N",
        "b": "100 ml dung dịch NaOH 1N",
        "c": "500 ml dung dịch NaOH 0,1N",
        "d": "300 ml dung dịch NaOH 5M",
        "c_opt": "A",
        "exp": "Theo công thức pha thuốc thử Gornall: lắc cho tan muối đồng và tartrat rồi thêm vào 300ml dd NaOH 2,5N, lắc đều.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nồng độ của dung dịch Protein chuẩn ($C_0$) sử dụng trong bài thực hành là bao nhiêu?",
        "a": "6,25 g/L",
        "b": "62,5 g/L",
        "c": "6,25 mg/dL",
        "d": "70 g/L",
        "c_opt": "A",
        "exp": "Dung dịch protein chuẩn: cân 6,25g albumin trứng, pha nước cất vừa đủ 1000ml, nồng độ là 6,25 g/L.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Chất nào được sử dụng để pha dung dịch protein chuẩn 6,25 g/L trong bài thực hành?",
        "a": "Albumin trứng",
        "b": "Globulin người",
        "c": "Hemoglobin tinh khiết",
        "d": "Gelatin thủy phân",
        "c_opt": "A",
        "exp": "Tài liệu ghi rõ: Dd protein (chuẩn) 6,25g/L: cân 6,25g albumin trứng, pha nước cất vừa đủ 1000ml.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Trong thí nghiệm định lượng Protein toàn phần, Ống Trắng được chuẩn bị gồm những thành phần nào?",
        "a": "5 ml Nước cất + 5 ml Thuốc thử Gornall",
        "b": "4 ml Nước cất + 1 ml dd Chuẩn + 5 ml Thuốc thử Gornall",
        "c": "4,9 ml Nước cất + 0,1 ml Huyết thanh + 5 ml Thuốc thử Gornall",
        "d": "5 ml Nước cất + 5 ml Nước muối sinh lý",
        "c_opt": "A",
        "exp": "Ống trắng gồm: Nước cất 5ml + Thuốc thử Gornall 5ml (không chứa protein).",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Mục đích chính của việc đưa Ống Trắng (Blank) vào quy trình đo quang phổ là gì?",
        "a": "Triệt tiêu độ hấp thu ánh sáng nền của bản thân thuốc thử và dung môi",
        "b": "Kiểm tra xem máy quang phổ có hoạt động hay không",
        "c": "Làm tăng độ nhạy của phản ứng tạo màu",
        "d": "Tạo phức màu đối chứng với huyết thanh",
        "c_opt": "A",
        "exp": "Ống trắng chứa mọi thành phần trừ chất cần đo, giúp máy quang phổ loại trừ độ hấp thu của thuốc thử (chỉnh OD về 0,000).",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thành phần hóa chất được cho vào Ống Chuẩn trong bài định lượng Protein gồm những gì?",
        "a": "4 ml Nước cất + 1 ml dd Protein chuẩn 6,25 g/L + 5 ml TT Gornall",
        "b": "5 ml Nước cất + 1 ml dd Protein chuẩn 6,25 g/L + 5 ml TT Gornall",
        "c": "4,9 ml Nước cất + 0,1 ml dd Protein chuẩn 6,25 g/L + 5 ml TT Gornall",
        "d": "1 ml dd Protein chuẩn 6,25 g/L + 5 ml TT Gornall",
        "c_opt": "A",
        "exp": "Theo bảng tiến hành: Ống chuẩn gồm Nước cất 4ml, DD Protein chuẩn 6,25 g/L 1ml, TT Gornall 5ml.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thành phần hóa chất được cho vào Ống Thử trong bài định lượng Protein gồm những gì?",
        "a": "4,9 ml Nước cất + 0,1 ml Huyết thanh + 5 ml TT Gornall",
        "b": "5 ml Nước cất + 0,1 ml Huyết thanh + 5 ml TT Gornall",
        "c": "4 ml Nước cất + 1 ml Huyết thanh + 5 ml TT Gornall",
        "d": "4,9 ml Nước cất + 0,1 ml Nước tiểu + 5 ml TT Gornall",
        "c_opt": "A",
        "exp": "Theo bảng tiến hành: Ống thử gồm Nước cất 4,9ml, Huyết thanh 0,1ml, TT Gornall 5ml.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Sau khi cho thuốc thử Gornall vào các ống nghiệm, điều kiện để phản ứng màu xảy ra hoàn toàn là gì?",
        "a": "Trộn đều và để ở nhiệt độ phòng thí nghiệm trong 20 phút",
        "b": "Ủ trong nồi cách thủy ở 37°C trong 5 phút",
        "c": "Đun sôi cách thủy trong 10 phút",
        "d": "Đo ngay lập tức sau khi lắc đều 30 giây",
        "c_opt": "A",
        "exp": "Quy trình thực hành ghi rõ: 'Trộn đều và để ở nhiệt độ phòng thí nghiệm 20 phút. Đo mật độ quang ở bước sóng 530nm.'",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Công thức tính nồng độ protein toàn phần trong huyết thanh (g/L) theo phương pháp Biuret trong bài là:",
        "a": "$C\\text{ (g/L)} = \\frac{OD - OD_{\\text{trắng}}}{OD_0 - OD_{\\text{trắng}}} \\times C_0 \\times 10$",
        "b": "$C\\text{ (g/L)} = \\frac{OD}{OD_0} \\times C_0$",
        "c": "$C\\text{ (g/L)} = \\frac{OD - OD_{\\text{trắng}}}{OD_0} \\times C_0 \\times 100$",
        "d": "$C\\text{ (g/L)} = (OD - OD_{\\text{trắng}}) \\times C_0 \\times 10$",
        "c_opt": "A",
        "exp": "Công thức chuẩn trong tài liệu: $C\\text{ (g/L)} = \\frac{OD - OD_{\\text{trắng}}}{OD_0 - OD_{\\text{trắng}}} \\times C_0 \\times 10$.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao trong công thức tính nồng độ Protein lại xuất hiện hệ số nhân 10?",
        "a": "Vì thể tích huyết thanh trong ống thử (0,1 ml) ít hơn 10 lần so với thể tích dd chuẩn trong ống chuẩn (1 ml)",
        "b": "Vì quy đổi từ đơn vị g/dL sang g/L",
        "c": "Vì nồng độ protein chuẩn đã bị pha loãng 10 lần",
        "d": "Vì thể tích thuốc thử Gornall gấp 10 lần thể tích mẫu thử",
        "c_opt": "A",
        "exp": "Ở ống chuẩn dùng 1 ml dung dịch protein chuẩn, còn ở ống thử chỉ dùng 0,1 ml huyết thanh (pha với 4,9 ml nước cất). Do đó, nồng độ protein trong ống thử bị pha loãng gấp 10 lần so với ống chuẩn, phải nhân bù hệ số 10.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Trong buổi thực hành, một sinh viên đo được: $OD_{\\text{trắng}} = 0,0754$; $OD_0 = 0,4411$; $OD = 0,3827$. Biết $C_0 = 6,25\\text{ g/L}$. Nồng độ protein toàn phần của mẫu thử là bao nhiêu?",
        "a": "Khoảng 43,97 g/L",
        "b": "Khoảng 54,20 g/L",
        "c": "Khoảng 62,50 g/L",
        "d": "Khoảng 72,15 g/L",
        "c_opt": "A",
        "exp": "$C = \\frac{0,3827 - 0,0754}{0,4411 - 0,0754} \\times 6,25 \\times 10 = \\frac{0,3073}{0,3657} \\times 62,5 \\approx 0,8403 \\times 62,5 \\approx 43,97\\text{ g/L}$. (Đúng với số liệu ghi chú trong giáo trình trang 14).",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng giá trị tham chiếu bình thường của nồng độ protein toàn phần trong huyết thanh người trưởng thành là:",
        "a": "60 – 80 g/L",
        "b": "40 – 60 g/L",
        "c": "80 – 100 g/L",
        "d": "35 – 50 g/L",
        "c_opt": "A",
        "exp": "Theo mục Biện luận trong giáo trình: 'Nồng độ protein huyết thanh bình thường là 60 – 80 g/L'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nếu biểu thị nồng độ protein toàn phần huyết thanh bình thường theo đơn vị g/dL (hoặc g%), khoảng giá trị này là:",
        "a": "6,0 – 8,0 g/dL",
        "b": "60 – 80 g/dL",
        "c": "0,6 – 0,8 g/dL",
        "d": "600 – 800 g/dL",
        "c_opt": "A",
        "exp": "$1\\text{ g/L} = 0,1\\text{ g/dL}$, do đó $60 - 80\\text{ g/L} = 6,0 - 8,0\\text{ g/dL}$.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Với kết quả định lượng protein toàn phần huyết thanh đạt 43,97 g/L, kết luận biện luận lâm sàng phù hợp nhất là:",
        "a": "Protein huyết thanh giảm bệnh lý",
        "b": "Protein huyết thanh bình thường",
        "c": "Protein huyết thanh tăng bệnh lý",
        "d": "Không thể kết luận khi chưa biết nồng độ albumin",
        "c_opt": "A",
        "exp": "Vì $43,97\\text{ g/L} < 60\\text{ g/L}$ (ngưỡng dưới của trị số bình thường 60 – 80 g/L), nên kết luận là giảm protein máu.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tình trạng sinh lý nào sau đây làm tăng nhu cầu protein của cơ thể?",
        "a": "Phụ nữ thai nghén và phụ nữ đang cho con bú",
        "b": "Người già ít vận động",
        "c": "Người đang ăn kiêng giảm cân",
        "d": "Thời kỳ sau mãn kinh",
        "c_opt": "A",
        "exp": "Giáo trình nêu rõ: 'Thay đổi sinh lý: Tăng nhu cầu protein (thai nghén, cho con bú)'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Trường hợp nào sau đây gây TĂNG nồng độ protein toàn phần huyết thanh do hiện tượng cô đặc máu?",
        "a": "Hội chứng mất nước liên tục do nôn nhiều, tiêu chảy cấp",
        "b": "Hội chứng thận hư",
        "c": "Xơ gan cổ trướng",
        "d": "Truyền dịch đẳng trương quá mức",
        "c_opt": "A",
        "exp": "Khi nôn ói hoặc tiêu chảy cấp mất nước liên tục, thể tích huyết tương giảm làm tăng giả tạo nồng độ protein huyết thanh (cô đặc máu).",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Bệnh lý nội tiết nào sau đây được nêu trong bài gây tăng protein toàn phần huyết thanh?",
        "a": "Bệnh Addison (Suy vỏ thượng thận mạn)",
        "b": "Hội chứng Cushing",
        "c": "Bệnh Basedow",
        "d": "Đái tháo nhạt",
        "c_opt": "A",
        "exp": "Giáo trình liệt kê các nguyên nhân tăng protein máu gồm: Hội chứng mất nước liên tục, Sốt kéo dài, Bệnh đa u tủy, Bệnh Addison.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Cơ chế chính làm tăng protein toàn phần huyết thanh trong bệnh Đa u tủy (bệnh Kahler) là gì?",
        "a": "Tế bào tương bào (plasma cell) ác tính tăng sinh tổng hợp quá mức globulin miễn dịch đơn dòng (Protein M)",
        "b": "Gan tăng cường tổng hợp albumin gấp 5 lần",
        "c": "Mất nước do sốt cao liên tục",
        "d": "Ống thận tăng tái hấp thu toàn bộ protein từ nước tiểu",
        "c_opt": "A",
        "exp": "Đa u tủy xương là bệnh lý ác tính tương bào tiết lượng lớn kháng thể đơn dòng (chủ yếu là IgG, IgA hoặc chuỗi nhẹ Bence-Jones), làm protein toàn phần tăng rất cao.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao trong bệnh lý Xơ gan và Viêm gan nặng, nồng độ protein toàn phần huyết thanh lại giảm?",
        "a": "Vì gan là cơ quan duy nhất tổng hợp albumin và phần lớn các protein huyết tương",
        "b": "Vì protein bị thoái hóa nhanh chóng ở lách",
        "c": "Vì cầu thận tăng tính thấm làm thoát protein ra nước tiểu",
        "d": "Vì ruột không hấp thu được acid amin",
        "c_opt": "A",
        "exp": "Gan là cơ quan chính sản xuất protein huyết tương (đặc biệt là 100% Albumin). Khi gan xơ hóa, số lượng tế bào gan chức năng giảm sút nghiêm trọng dẫn đến giảm tổng hợp protein.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Bệnh lý tại thận nào là nguyên nhân kinh điển gây giảm mạnh nồng độ protein toàn phần huyết thanh kèm phù to toàn thân?",
        "a": "Hội chứng thận hư",
        "b": "Sỏi đài bể thận",
        "c": "Viêm bàng quang cấp",
        "d": "U tuyến thượng thận",
        "c_opt": "A",
        "exp": "Trong Hội chứng thận hư, màng lọc cầu thận bị tổn thương nghiêm trọng làm thất thoát lượng lớn protein ra nước tiểu (> 3,5 g/24h), dẫn đến giảm protein máu nặng (< 60 g/L) và giảm albumin (< 30 g/L).",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nhóm nguyên nhân nào sau đây gây giảm nồng độ protein toàn phần do mất ra ngoài cơ thể?",
        "a": "Mất máu cấp, bỏng rộng diện tích lớn",
        "b": "Bệnh đa u tủy xương",
        "c": "Hội chứng mất nước liên tục",
        "d": "Sốt kéo dài",
        "c_opt": "A",
        "exp": "Mất máu (chảy máu nặng) và bỏng rộng (thoát huyết tương qua bề mặt da tổn thương) làm mất trực tiếp một lượng lớn protein ra ngoài cơ thể.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Phân số protein chiếm tỷ lệ lớn nhất (khoảng 55 – 65%) trong tổng lượng protein huyết thanh người bình thường là:",
        "a": "Albumin",
        "b": "Alpha-1 globulin",
        "c": "Beta globulin",
        "d": "Gamma globulin",
        "c_opt": "A",
        "exp": "Albumin chiếm từ 35 - 50 g/L (khoảng 55 - 65% protein toàn phần), đóng vai trò quyết định tạo áp suất keo của huyết tương.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Hậu quả sinh lý bệnh trực tiếp nhất khi nồng độ albumin và protein toàn phần huyết thanh giảm nặng là gì?",
        "a": "Giảm áp suất keo huyết tương, nước thoát ra gian bào gây phù",
        "b": "Tăng áp suất thủy tĩnh lòng mạch gây xuất huyết",
        "c": "Tăng độ nhớt của máu gây tắc mạch",
        "d": "Làm toan hóa máu do mất tính đệm",
        "c_opt": "A",
        "exp": "Albumin tạo khoảng 80% áp suất keo huyết tương. Khi protein/albumin giảm thấp, áp suất keo giảm làm nước từ lòng mạch thoát ra khoang gian bào gây phù mềm, dịch cổ trướng.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Trong thí nghiệm Biuret, nếu kỹ thuật viên vô tình dùng mẫu huyết thanh bị vỡ hồng cầu (tán huyết nặng), kết quả đo quang sẽ:",
        "a": "Tăng giả tạo do hemoglobin có màu đỏ hấp thu thêm ánh sáng ở bước sóng đo",
        "b": "Giảm giả tạo do enzym hồng cầu phân hủy thuốc thử",
        "c": "Không thay đổi vì hemoglobin không phải là protein",
        "d": "Làm mất màu tím hồng của phức chất",
        "c_opt": "A",
        "exp": "Hemoglobin vừa là protein (tác dụng với thuốc thử Biuret) vừa có màu đỏ tự nhiên hấp thụ quang phổ, gây tăng giả tạo mật độ quang OD.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao không nên dùng huyết tương chống đông bằng Heparin nồng độ cao hoặc mẫu có chứa nhiều amoniac trong một số phản ứng màu protein?",
        "a": "Vì có thể tạo độ đục hoặc tương tác với ion kim loại trong thuốc thử",
        "b": "Vì làm biến tính hoàn toàn liên kết peptid",
        "c": "Vì biến đổi $\\ce{Cu^2+}$ thành $\\ce{Cu^3+}$",
        "d": "Vì làm giảm pH dung dịch xuống môi trường acid",
        "c_opt": "A",
        "exp": "Chất chống đông không đúng loại hoặc tạp chất có thể gây tủa thuốc thử, gây đục làm sai lệch phép đo mật độ quang.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một mẫu thử protein cho $OD - OD_{\\text{trắng}} = 0,400$; ống chuẩn cho $OD_0 - OD_{\\text{trắng}} = 0,500$. Với $C_0 = 6,25\\text{ g/L}$, nồng độ protein của mẫu là:",
        "a": "50,0 g/L",
        "b": "5,0 g/L",
        "c": "80,0 g/L",
        "d": "62,5 g/L",
        "c_opt": "A",
        "exp": "$C = \\frac{0,400}{0,500} \\times 6,25 \\times 10 = 0,8 \\times 62,5 = 50,0\\text{ g/L}$.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nếu một bệnh nhân có $OD - OD_{\\text{trắng}} = 0,550$; ống chuẩn $OD_0 - OD_{\\text{trắng}} = 0,500$; $C_0 = 6,25\\text{ g/L}$. Nồng độ protein và biện luận lâm sàng là:",
        "a": "68,75 g/L — Nồng độ protein trong giới hạn bình thường",
        "b": "68,75 g/L — Nồng độ protein tăng cao bệnh lý",
        "c": "55,0 g/L — Nồng độ protein giảm nhẹ",
        "d": "85,25 g/L — Nồng độ protein tăng do đa u tủy",
        "c_opt": "A",
        "exp": "$C = \\frac{0,550}{0,500} \\times 62,5 = 1,1 \\times 62,5 = 68,75\\text{ g/L}$. Nằm trong khoảng 60 – 80 g/L nên bình thường.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Phản ứng Biuret có tên gọi bắt nguồn từ chất biuret. Hợp chất biuret có công thức cấu tạo là gì?",
        "a": "$\\ce{NH2-CO-NH-CO-NH2}$",
        "b": "$\\ce{NH2-CO-NH2}$",
        "c": "$\\ce{NH2-CH2-COOH}$",
        "d": "$\\ce{CH3-CO-NH-CH3}$",
        "c_opt": "A",
        "exp": "Biuret là dẫn xuất ngưng tụ từ 2 phân tử urê khi đun nóng: $2\\ce{NH2CONH2 -> NH2-CO-NH-CO-NH2 + NH3}$. Hợp chất này có 2 liên kết giống peptid nên phản ứng với $\\ce{Cu^2+}$ cho màu tím đặc trưng.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khi để các ống nghiệm phản ứng Biuret vượt quá thời gian quy định nhiều giờ trước khi đo quang, hiện tượng nào có thể xảy ra?",
        "a": "Có thể xuất hiện kết tủa hoặc biến đổi màu làm sai lệch độ hấp thu OD",
        "b": "Màu tím hồng sẽ chuyển sang màu xanh lá cây",
        "c": "Protein bị phân hủy thành acid amin tự do",
        "d": "Không có hiện tượng gì xảy ra vì phức chất bền vô hạn",
        "c_opt": "A",
        "exp": "Để quá lâu dung dịch có thể bị bay hơi, kết tủa tạp chất hoặc biến tính quang học làm sai lệch kết quả đo.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Điểm khác biệt căn bản giữa huyết thanh (serum) và huyết tương (plasma) về thành phần protein là gì?",
        "a": "Huyết thanh không chứa Fibrinogen vì đã bị tiêu hao trong quá trình đông máu",
        "b": "Huyết thanh chứa nhiều Albumin hơn huyết tương gấp 2 lần",
        "c": "Huyết tương không có Globulin",
        "d": "Huyết thanh chứa nhiều yếu tố đông máu hơn huyết tương",
        "c_opt": "A",
        "exp": "Huyết thanh = Huyết tương trừ đi các yếu tố đông máu (đặc biệt là Fibrinogen / sợi huyết). Khi máu đông, fibrinogen đã chuyển thành cục máu đông fibrin.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Để đánh giá sâu hơn tỷ lệ các phân đoạn protein (Albumin, $\\alpha_1, \\alpha_2, \\beta, \\gamma$ globulin), kỹ thuật xét nghiệm nào được chỉ định tiếp theo?",
        "a": "Điện di protein huyết thanh (Protein Electrophoresis)",
        "b": "Định lượng protein bằng phương pháp so màu Biuret",
        "c": "Xét nghiệm tổng phân tích tế bào máu",
        "d": "Đo áp suất thẩm thấu huyết tương",
        "c_opt": "A",
        "exp": "Điện di protein huyết thanh giúp tách và định lượng riêng biệt 5 phân đoạn protein, đặc biệt phát hiện dải tăng đơn dòng (Monoclonal spike) trong bệnh đa u tủy.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    }
]

print(f"Loaded Part 1: {len(QUESTIONS_PART1)} questions")
