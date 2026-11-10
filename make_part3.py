# -*- coding: utf-8 -*-
"""
PHẦN 3: THÍ NGHIỆM 3 - ĐỊNH LƯỢNG URÊ MÁU & NƯỚC TIỂU (40 CÂU)
"""

QUESTIONS_PART3 = [
    {
        "q": "Urê là sản phẩm thoái hóa quan trọng nhất của hợp chất nào trong cơ thể người?",
        "a": "Protein (protid)",
        "b": "Acid nucleic (DNA, RNA)",
        "c": "Triglycerid và acid béo",
        "d": "Glycogen và Glucose",
        "c_opt": "A",
        "exp": "Theo giáo trình trang 18: 'Urê là sản phẩm thoái hóa quan trọng nhất của protein', chiếm khoảng 80 – 90% lượng nitơ phi protein đào thải qua nước tiểu.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Cơ quan chính trong cơ thể đảm nhiệm chức năng tổng hợp Urê từ amoniac độc hại là:",
        "a": "Gan (thông qua chu trình Urê / Ornithin)",
        "b": "Thận (thông qua ống lượn gần)",
        "c": "Cơ vân (thông qua chu trình Cori)",
        "d": "Tụy (thông qua các tế bào nang)",
        "c_opt": "A",
        "exp": "Chu trình tổng hợp Urê (chu trình Krebs-Henseleit / Ornithin) diễn ra gần như duy nhất tại tế bào gan nhằm khử độc $\\ce{NH3}$.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nguyên tắc định lượng Urê trong bài thực hành áp dụng phương pháp nào?",
        "a": "Phương pháp đo động học 2 điểm (Fixed time kinetic) bằng 2 phản ứng enzym",
        "b": "Phương pháp đo điểm cuối tạo màu với thuốc thử Biuret",
        "c": "Phương pháp chuẩn độ acid - base bằng NaOH",
        "d": "Phương pháp so màu phản ứng Jaffé",
        "c_opt": "A",
        "exp": "Tài liệu trang 16 ghi rõ: 'Urê trong mẫu thử được định lượng theo phương pháp đo động học 2 điểm (fixed time kinetic) bằng 2 phản ứng'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Enzym xúc tác cho phản ứng thủy phân Urê ở bước thứ nhất là gì?",
        "a": "Urease",
        "b": "Uricase",
        "c": "Glutamate Dehydrogenase (GLDH)",
        "d": "Peroxidase",
        "c_opt": "A",
        "exp": "Phản ứng 1: $\\text{Urê} + \\ce{H2O} \\xrightarrow{\\text{Urease}} 2\\ce{NH4+} + \\ce{CO3^2-}$. Enzym xúc tác là Urease.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nguồn gốc của enzym Urease được sử dụng trong bộ kit xét nghiệm là từ đâu?",
        "a": "Chiết xuất từ hạt đậu Jack (Jack Bean)",
        "b": "Chiết xuất từ gan lợn",
        "c": "Tổng hợp từ nấm men bia",
        "d": "Chiết xuất từ vi khuẩn E. coli",
        "c_opt": "A",
        "exp": "Thành phần thuốc thử R1 trang 17 ghi rõ: 'Urease (Jack Bean) $\\ge 10\\text{ kU/L}$'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Sản phẩm sinh ra từ phản ứng thủy phân Urê bởi enzym Urease là gì?",
        "a": "Ion Amoni ($\\ce{NH4+}$) và ion Carbonat ($\\ce{CO3^2-}$)",
        "b": "Allantoin và $\\ce{CO2}$",
        "c": "Acid uric và $\\ce{H2O2}$",
        "d": "Creatinin và acid phosphoric",
        "c_opt": "A",
        "exp": "Phương trình: $\\text{Urê} + \\ce{H2O} \\xrightarrow{\\text{Urease}} 2\\ce{NH4+} + \\ce{CO3^2-}$.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Phương trình phản ứng thứ hai trong xét nghiệm định lượng Urê là:",
        "a": "$2\\ce{NH4+} + \\alpha\\text{-KG} + \\ce{NADH} \\xrightarrow{\\text{GLDH}} \\text{L-Glutamate} + \\ce{NAD+} + \\ce{H2O}$",
        "b": "$\\ce{NH4+} + \\text{Pyruvate} + \\ce{NADH} \\xrightarrow{\\text{LDH}} \\text{Alanine} + \\ce{NAD+}$",
        "c": "$\\text{Urê} + \\ce{H2O} \\xrightarrow{\\text{Urease}} 2\\ce{NH3} + \\ce{CO2}$",
        "d": "$2\\ce{H2O2} + \\text{DHBS} + \\text{4AAP} \\xrightarrow{\\text{POD}} \\text{Quinoneimine}$",
        "c_opt": "A",
        "exp": "Phản ứng 2 trang 16: $2\\ce{NH4+} + \\alpha\\text{-KG} + \\ce{NADH} \\xrightarrow{\\text{GLDH}} \\text{L-Glutamate} + \\ce{NAD+} + \\ce{H2O}$.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "GLDH là tên viết tắt của enzym nào trong phản ứng định lượng Urê?",
        "a": "Glutamate Dehydrogenase",
        "b": "Glucose Dehydrogenase",
        "c": "Glycerol Dehydrogenase",
        "d": "Glutamine Synthetase",
        "c_opt": "A",
        "exp": "GLDH là Glutamate Dehydrogenase, xúc tác phản ứng khử amin hóa khử giữa $\\alpha$-ketoglutarate và ion amoni với sự tham gia của coenzym NADH.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nguyên lý biến thiên quang học được đo trên máy quang phổ trong xét nghiệm Urê là gì?",
        "a": "Sự GIẢM mật độ quang do NADH chuyển thành $\\ce{NAD+}$ tỉ lệ thuận với nồng độ urê trong mẫu thử",
        "b": "Sự TĂNG mật độ quang do $\\ce{NAD+}$ sinh ra hấp thụ ánh sáng mạnh",
        "c": "Sự đổi màu từ không màu sang màu tím hồng của phức chất Biuret",
        "d": "Sự tăng độ đục do kết tủa protein",
        "c_opt": "A",
        "exp": "Giáo trình trang 17: 'Sự giảm mật độ quang do NADH chuyển thành NAD tỉ lệ thuận với nồng độ urê trong mẫu thử'. Coenzym NADH hấp thụ ánh sáng mạnh ở 340 nm, khi phản ứng xảy ra NADH mất đi làm OD giảm dần.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Bước sóng ($\\lambda$) đo quang phổ kế trong xét nghiệm định lượng Urê là bao nhiêu?",
        "a": "340 nm",
        "b": "505 nm",
        "c": "530 nm",
        "d": "492 nm",
        "c_opt": "A",
        "exp": "Bước sóng 340 nm là đỉnh hấp thụ cực đại đặc trưng của nhân nicotinamid khử trong phân tử NADH.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thành phần của Thuốc thử 1 (R1 - Thuốc thử enzym) gồm những chất nào?",
        "a": "Tris Buffer (100 mmol/L), $\\alpha$-Ketoglutarate (5,49 mmol/L), Urease ($\\ge 10\\text{ kU/L}$), GLDH ($\\ge 3,8\\text{ kU/L}$)",
        "b": "Pipes buffer (50 mmol/L), DHBS, 4AAP và Uricase",
        "c": "$\\ce{CuSO4}$, Na K Tartrat và NaOH",
        "d": "Acid Picric (17,5 mmol/L) và NaOH (0,29 mol/L)",
        "c_opt": "A",
        "exp": "Tài liệu trang 17 liệt kê chi tiết: R1 gồm Tris Buffer, $\\alpha$-Ketoglutarate, Urease và Glutamate Dehydrogenase.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thành phần duy nhất có trong Thuốc thử 2 (R2) của bộ kit Urê là gì?",
        "a": "NADH (1,66 mmol/L)",
        "b": "$\\ce{NAD+}$ (5,0 mmol/L)",
        "c": "Sodium hydroxide 2,5N",
        "d": "Peroxidase 1000 U/L",
        "c_opt": "A",
        "exp": "Tài liệu trang 17: '- Thuốc thử 2 (R2): NADH 1.66 mmol/L'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khi pha dung dịch hoạt động (trộn lẫn R1 và R2) để định lượng Urê, tỷ lệ thể tích chuẩn là bao nhiêu?",
        "a": "$4\\text{ R1} + 1\\text{ R2}$ (tỷ lệ 4 : 1)",
        "b": "$1\\text{ R1} + 1\\text{ R2}$ (tỷ lệ 1 : 1)",
        "c": "$5\\text{ R1} + 1\\text{ R2}$ (tỷ lệ 5 : 1)",
        "d": "$1\\text{ R1} + 4\\text{ R2}$ (tỷ lệ 1 : 4)",
        "c_opt": "A",
        "exp": "Tài liệu trang 17: 'Phương pháp 2: Với thuốc thử trộn lẫn (pha theo tỷ lệ thể tích $4\\text{R1} + 1\\text{R2}$)...'",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Dung dịch hoạt động đã trộn ($4\\text{R1} + 1\\text{R2}$) có thời gian ổn định là bao lâu khi bảo quản ở 2 – 8°C và ở 15 – 25°C?",
        "a": "4 tuần ở 2 – 8°C và 5 ngày ở 15 – 25°C (trong tối)",
        "b": "1 tuần ở 2 – 8°C và 24 giờ ở 15 – 25°C",
        "c": "12 tháng ở 2 – 8°C",
        "d": "Chỉ dùng ngay trong vòng 2 giờ sau khi pha",
        "c_opt": "A",
        "exp": "Giáo trình trang 17: 'dung dịch hoạt động sau khi pha ổn định trong 4 tuần ở 2–8°C và 5 ngày ở 15–25°C, bảo quản trong tối, tránh ánh sáng trực tiếp'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Chất chống đông nào TUYỆT ĐỐI KHÔNG ĐƯỢC DÙNG khi lấy mẫu máu định lượng Urê bằng phương pháp enzym?",
        "a": "Amoni Heparin (Heparin chứa gốc $\\ce{NH4+}$)",
        "b": "Natri Heparin",
        "c": "EDTA dipotassium",
        "d": "Natri Citrat",
        "c_opt": "A",
        "exp": "Giáo trình trang 17 ghi rõ: 'Huyết tương chống đông bằng EDTA hay heparin (không dùng amoni heparin)'. Vì ion $\\ce{NH4+}$ trong thuốc chống đông sẽ tham gia vào phản ứng của GLDH làm kết quả urê tăng giả tạo cực kỳ cao.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Hậu quả gì xảy ra nếu dùng ống chống đông Amoni Heparin để định lượng Urê?",
        "a": "Kết quả nồng độ Urê tăng giả tạo rất cao vượt ngưỡng đo",
        "b": "Kết quả nồng độ Urê giảm về bằng 0",
        "c": "Enzym Urease bị ức chế hoàn toàn",
        "d": "Mẫu máu bị đông lại trong cuvet đo",
        "c_opt": "A",
        "exp": "Ion $\\ce{NH4+}$ ngoại sinh từ chất chống đông tiêu thụ ngay NADH trong phản ứng 2, làm mật độ quang sụt giảm mạnh dẫn đến kết luận urê tăng vọt sai sự thật.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Độ pha loãng mẫu nước tiểu 24 giờ khi tiến hành định lượng Urê theo quy trình là:",
        "a": "Pha loãng tỉ lệ 1 nước tiểu : 100 nước cất (1/101)",
        "b": "Pha loãng tỉ lệ 1 nước tiểu : 9 nước cất (1/10)",
        "c": "Pha loãng tỉ lệ 1 nước tiểu : 50 nước cất (1/51)",
        "d": "Không pha loãng, đo trực tiếp",
        "c_opt": "A",
        "exp": "Giáo trình trang 17 ghi rõ: 'Nước tiểu 24h, pha loãng tỉ lệ 1 nước tiểu: 100 nước cất'. Khi tính kết quả phải nhân với hệ số pha loãng 100.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao nước tiểu phải pha loãng tới 1 : 100 khi định lượng Urê trong khi mẫu huyết thanh không cần pha loãng?",
        "a": "Vì nồng độ urê trong nước tiểu bình thường cao gấp hàng trăm lần nồng độ urê trong máu",
        "b": "Vì nước tiểu có tính acid làm hỏng cuvet đo",
        "c": "Vì nước tiểu chứa nhiều vi khuẩn phân hủy thuốc thử",
        "d": "Vì để loại bỏ màu vàng của sắc tố urobilin",
        "c_opt": "A",
        "exp": "Nồng độ urê nước tiểu bình thường lên tới 26 – 43 g/24h (khoảng 15 – 30 g/L), trong khi dải đo tuyến tính của kit chỉ đến 300 mg/dL (3 g/L), nên bắt buộc phải pha loãng 1:100.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Theo phương pháp 2 (thuốc thử trộn lẫn), thể tích dung dịch hoạt động và thể tích mẫu thử là bao nhiêu?",
        "a": "500 $\\mu$L Dung dịch hoạt động + 5 $\\mu$L Mẫu thử",
        "b": "500 $\\mu$L Dung dịch hoạt động + 50 $\\mu$L Mẫu thử",
        "c": "400 $\\mu$L Dung dịch hoạt động + 12,5 $\\mu$L Mẫu thử",
        "d": "1000 $\\mu$L Dung dịch hoạt động + 10 $\\mu$L Mẫu thử",
        "c_opt": "A",
        "exp": "Bảng Phương pháp 2 trang 18: Thuốc thử đã trộn: 500 $\\mu$L; Mẫu thử (HT/ht): 5 $\\mu$L.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thời gian đọc độ hấp thu của phản ứng định lượng Urê theo phương pháp 2 là bao lâu sau khi trộn đều?",
        "a": "Sau 30 giây ở bước sóng 340 nm",
        "b": "Sau 5 phút ở 37°C",
        "c": "Sau 20 phút ở nhiệt độ phòng",
        "d": "Sau 15 phút tránh ánh sáng",
        "c_opt": "A",
        "exp": "Mục Phương pháp 2 trang 18: 'Trộn đều, đọc độ hấp thu sau 30 giây ở bước sóng 340nm. Ghi nhận lại kết quả hiển thị trên máy'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng tuyến tính của xét nghiệm định lượng Urê trong bài là:",
        "a": "11,5 – 300 mg/dL",
        "b": "0,49 – 25 mg/dL",
        "c": "50 – 1000 mg/dL",
        "d": "1 – 50 mmol/L",
        "c_opt": "A",
        "exp": "Tài liệu ghi rõ: '* Độ tuyến tính: 11,5 – 300mg/dl'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng tham chiếu nồng độ Urê máu ở NGƯỜI LỚN bình thường là bao nhiêu?",
        "a": "17 – 43 mg/dL (tương đương 2,8 – 7,2 mmol/L)",
        "b": "53 – 97 mg/dL",
        "c": "60 – 80 g/L",
        "d": "3,5 – 7,2 mg/dL",
        "c_opt": "A",
        "exp": "Tài liệu trang 18: '* Bình thường - Urê máu: + Người lớn: 17 – 43 mg/dl (2,8 – 7,2 mmol/l)'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Công thức toán học dùng để chuyển đổi nồng độ Urê từ đơn vị mg/dL sang mmol/L là:",
        "a": "$\\text{mmol/L} = \\frac{\\text{mg/dL}}{6}$ (hoặc $\\text{mmol/L} = \\text{mg/dL} \\times 0,1665$)",
        "b": "$\\text{mmol/L} = \\text{mg/dL} \\times 88,4$",
        "c": "$\\text{mmol/L} = \\text{mg/dL} \\times 59,48$",
        "d": "$\\text{mmol/L} = \\frac{\\text{mg/dL}}{18}$",
        "c_opt": "A",
        "exp": "Phân tử lượng của Urê $\\ce{CO(NH2)2} = 60\\text{ g/mol}$. $1\\text{ mg/dL} = 10\\text{ mg/L} = 10/60\\text{ mmol/L} = 1/6\\text{ mmol/L} \\approx 0,1665\\text{ mmol/L}$.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng tham chiếu Urê máu ở trẻ em từ 1 đến 3 tuổi là:",
        "a": "11 – 36 mg/dL (1,8 – 6,0 mmol/L)",
        "b": "15 – 36 mg/dL (2,5 – 6,0 mmol/L)",
        "c": "18 – 45 mg/dL (2,9 – 7,5 mmol/L)",
        "d": "17 – 43 mg/dL (2,8 – 7,2 mmol/L)",
        "c_opt": "A",
        "exp": "Giáo trình trang 18: '+ Trẻ em: 1 – 3 tuổi: 11 – 36 mg/dl (1,8 – 6,0 mmol/L)'.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng tham chiếu Urê máu ở trẻ em từ 14 đến 19 tuổi là:",
        "a": "18 – 45 mg/dL (2,9 – 7,5 mmol/L)",
        "b": "11 – 36 mg/dL (1,8 – 6,0 mmol/L)",
        "c": "15 – 36 mg/dL (2,5 – 6,0 mmol/L)",
        "d": "5 – 15 mg/dL",
        "c_opt": "A",
        "exp": "Giáo trình trang 18: '14 – 19 tuổi: 18 – 45 mg/dl (2,9 – 7,5 mmol/L)'.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Lượng Urê bài xuất ra ngoài theo nước tiểu 24 giờ ở người bình thường là:",
        "a": "26 – 43 g/24 giờ (430 – 720 mmol/24 giờ)",
        "b": "1000 – 1500 mg/24 giờ",
        "c": "250 – 750 mg/24 giờ",
        "d": "1 – 2 g/24 giờ",
        "c_opt": "A",
        "exp": "Tài liệu trang 18: '- Urê nước tiểu: 26 – 43g/24 giờ (430 – 720 mmol/24 giờ)'. Chú ý đơn vị là GAM (g/24h) chứ không phải miligam.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tỉ số [Urê máu / Creatinin máu] bình thường tính theo đơn vị [(mg/dL)/(mg/dL)] nằm trong khoảng nào?",
        "a": "20 – 35",
        "b": "10 – 15",
        "c": "40 – 60",
        "d": "5 – 10",
        "c_opt": "A",
        "exp": "Tài liệu trang 18 ghi rõ: '- Urê máu / creatinin máu: 20 – 35 [(mg/dl)/(mg/dl)]'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Yếu tố sinh lý nào sau đây ảnh hưởng trực tiếp đến nồng độ Urê trong máu?",
        "a": "Chế độ ăn uống (lượng protid ăn vào) và lứa tuổi",
        "b": "Nhóm máu hệ ABO",
        "c": "Màu da và chủng tộc",
        "d": "Thời gian ngủ trong ngày",
        "c_opt": "A",
        "exp": "Giáo trình ghi: '* Thay đổi sinh lý: nồng độ urê thay đổi tùy theo chế độ ăn uống và theo tuổi'. Ăn nhiều đạm làm urê máu tăng; ăn chay ít đạm làm urê máu thấp.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nhóm nguyên nhân TẠI THẬN gây tăng urê máu CẤP TÍNH được nêu trong tài liệu gồm:",
        "a": "Viêm cầu thận cấp, viêm ống thận cấp do nhiễm độc/tai biến truyền nhầm nhóm máu, sốt vàng da do xoắn khuẩn Leptospira",
        "b": "Sỏi bàng quang, u xơ tuyến tiền liệt",
        "c": "Xơ gan cổ trướng, suy dinh dưỡng",
        "d": "Chế độ ăn nhiều thịt đỏ, phụ nữ có thai",
        "c_opt": "A",
        "exp": "Trang 19: '+ Nguyên nhân tại thận: - Cấp tính: viêm cầu thận cấp, viêm ống thận cấp do nhiễm độc hoặc do tai biến truyền nhầm nhóm máu, sốt vàng da chảy máu do xoắn khuẩn Leptospira gây nên hội chứng gan thận cấp...'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nhóm nguyên nhân NGOÀI THẬN gây tăng urê máu do bít tắc cơ học đường tiết niệu (sau thận) là:",
        "a": "Ứ nước tiểu do chướng ngại tiết niệu như sỏi niệu quản, u tiền liệt tuyến",
        "b": "Viêm thận mạn tính",
        "c": "Bệnh hoại tử ống thận cấp",
        "d": "Suy tim ứ huyết",
        "c_opt": "A",
        "exp": "Trang 19: '+ Nguyên nhân ngoài thận: ứ nước tiểu do chướng ngại tiết niệu: Sỏi niệu quản, u tiền liệt tuyến...'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tình trạng tăng Urê máu ngoại sinh do hủy hoại tế bào mạnh xảy ra trong trường hợp nào?",
        "a": "Bỏng rộng, chấn thương dập nát, phẫu thuật lớn",
        "b": "Bệnh Addison",
        "c": "Có thai thời kỳ cuối",
        "d": "Nhiễm độc giáp Basedow",
        "c_opt": "A",
        "exp": "Trang 19: '- Tăng urê ngoại sinh do hủy hoại mạnh tế bào: bỏng rộng, chấn thương, phẫu thuật lớn...'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nguyên nhân nào sau đây làm GIẢM nồng độ Urê trong máu?",
        "a": "Tổn thương tế bào gan nặng (suy gan, xơ gan giai đoạn cuối)",
        "b": "Viêm cầu thận cấp tính",
        "c": "Chấn thương phần mềm diện rộng",
        "d": "Tắc mật do sỏi ống mật chủ",
        "c_opt": "A",
        "exp": "Gan là nơi duy nhất tổng hợp urê. Khi gan bị tổn thương nặng (viêm gan tối cấp, xơ gan mất bù), chức năng tổng hợp urê bị suy giảm nghiêm trọng làm nồng độ urê máu hạ thấp.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tình trạng sinh lý nào sau đây làm GIẢM nồng độ Urê máu?",
        "a": "Phụ nữ đang có thai",
        "b": "Nam thanh niên tập thể hình",
        "c": "Vận động viên điền kinh thi đấu",
        "d": "Người ăn khẩu phần 200g protein/ngày",
        "c_opt": "A",
        "exp": "Giáo trình trang 19 nêu các nguyên nhân giảm urê máu gồm: Có thai, Truyền nước quá nhiều, Tổn thương gan nặng, Chế độ ăn thiếu protid lâu ngày. Ở thai phụ, tăng lưu lượng lọc cầu thận và tăng thể tích tuần hoàn làm urê máu giảm.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao truyền nước (dịch truyền tĩnh mạch) quá nhiều lại làm giảm nồng độ Urê máu?",
        "a": "Gây pha loãng máu (tăng thể tích huyết tương) và kích thích tăng bài niệu",
        "b": "Nước truyền vào phá hủy phân tử urê",
        "c": "Nước ức chế enzym urease ở thận",
        "d": "Tạo phức hợp chelat làm tủa urê",
        "c_opt": "A",
        "exp": "Truyền dịch thể tích lớn làm tăng thể tích tuần hoàn gây pha loãng các chất tan trong huyết tương (hemodilution) và thúc đẩy thận tăng lọc thải urê.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một bệnh nhân nam 65 tuổi tiểu khó, bí tiểu do u phì đại tuyến tiền liệt. Kết quả xét nghiệm Urê máu là 85 mg/dL. Tình trạng tăng urê này thuộc nhóm nào?",
        "a": "Tăng urê sau thận do tắc nghẽn đường dẫn niệu",
        "b": "Tăng urê trước thận do mất nước",
        "c": "Tăng urê tại thận do tổn thương nhu mô",
        "d": "Tăng urê ngoại sinh do chế độ ăn",
        "c_opt": "A",
        "exp": "U tiền liệt tuyến gây chướng ngại dòng nước tiểu (sau thận), áp lực ngược dòng lên thận cản trở lọc cầu thận và tăng tái hấp thu urê vào máu.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một bệnh nhân bị xuất huyết tiêu hóa trên do loét dạ dày nôn ra máu. Sau đó xét nghiệm thấy Urê máu tăng vọt nhưng Creatinin máu tăng không đáng kể. Cơ chế là gì?",
        "a": "Protein từ máu chảy vào ống tiêu hóa bị vi khuẩn ruột phân hủy sinh ra lượng lớn $\\ce{NH3}$, được hấp thu về gan tổng hợp thành Urê",
        "b": "Xuất huyết làm thủng cầu thận",
        "c": "Dạ dày tiết trực tiếp urê vào lòng ruột",
        "d": "Creatinin bị phân hủy trong dạ dày",
        "c_opt": "A",
        "exp": "Máu chảy vào ruột là nguồn nạp protein nội sinh khổng lồ, vi khuẩn đường ruột chuyển hóa tạo nhiều $\\ce{NH3}$, gan tăng tổng hợp urê đưa vào máu (kết hợp với giảm thể tích tuần hoàn).",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một bệnh nhân có nồng độ Urê máu là 4,5 mmol/L. Quy đổi sang đơn vị mg/dL là:",
        "a": "27 mg/dL",
        "b": "45 mg/dL",
        "c": "75 mg/dL",
        "d": "15 mg/dL",
        "c_opt": "A",
        "exp": "$\\text{mg/dL} = \\text{mmol/L} \\times 6 = 4,5 \\times 6 = 27\\text{ mg/dL}$. Nằm trong giới hạn bình thường (17 – 43 mg/dL).",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một sinh viên ghi chú trên hình trang 17: $[\\text{Urê}] = 145,8\\text{ mg/dL}$. Nhận định về kết quả này là:",
        "a": "Tăng rất cao so với bình thường (17 – 43 mg/dL), chỉ điểm suy thận nặng hoặc tăng dị hóa nghiêm trọng",
        "b": "Bình thường đối với người ăn nhiều đạm",
        "c": "Giảm thấp gợi ý xơ gan",
        "d": "Nằm trong khoảng tham chiếu người cao tuổi",
        "c_opt": "A",
        "exp": "145,8 mg/dL cao gấp hơn 3 lần ngưỡng trên bình thường (43 mg/dL), tương đương khoảng 24,3 mmol/L, là mức tăng bệnh lý rất nghiêm trọng.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Hiện tượng tái hấp thu Urê tại ống thận có đặc điểm gì nổi bật?",
        "a": "Được tái hấp thu thụ động khoảng 40 – 50% ở ống lượn gần và ống góp, phụ thuộc vào tốc độ dòng nước tiểu",
        "b": "Được tái hấp thu chủ động 100% nhờ bơm tiêu tốn ATP",
        "c": "Hoàn toàn không được tái hấp thu ở bất kỳ đoạn nào của ống thận",
        "d": "Chỉ được bài tiết thêm mà không tái hấp thu",
        "c_opt": "A",
        "exp": "Urê được lọc tự do qua cầu thận nhưng sau đó bị tái hấp thu thụ động khoảng 40 - 50%. Khi dòng nước tiểu chảy chậm (mất nước, thiểu niệu), urê bị tái hấp thu nhiều hơn làm urê máu tăng mạnh.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao Urê máu không phải là chỉ số lý tưởng nhất để phản ánh chính xác mức lọc cầu thận (GFR) khi so sánh với Creatinin?",
        "a": "Vì nồng độ urê bị ảnh hưởng nhiều bởi chế độ ăn, mức độ dị hóa protein và hiện tượng tái hấp thu tại ống thận",
        "b": "Vì urê phân tử quá lớn không qua được màng lọc cầu thận",
        "c": "Vì urê bị phá hủy nhanh chóng trong máu",
        "d": "Vì phương pháp định lượng urê không chính xác",
        "c_opt": "A",
        "exp": "Urê thay đổi theo lượng đạm ăn vào, tốc độ dị hóa tế bào và bị tái hấp thu một lượng biến đổi ở ống thận. Do đó, Creatinin là chỉ số ổn định và phản ánh GFR trung thực hơn.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    }
]

print(f"Loaded Part 3: {len(QUESTIONS_PART3)} questions")
