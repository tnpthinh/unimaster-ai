# -*- coding: utf-8 -*-
"""
PHẦN 2: THÍ NGHIỆM 2 - ĐỊNH LƯỢNG ACID URIC HUYẾT THANH & NƯỚC TIỂU (40 CÂU)
"""

QUESTIONS_PART2 = [
    {
        "q": "Acid uric trong cơ thể người là sản phẩm thoái hóa cuối cùng của nhóm hợp chất nào?",
        "a": "Các base purin (Adenin, Guanin) của acid nucleic",
        "b": "Các base pyrimidin (Cytosin, Uracil, Thymin)",
        "c": "Các acid amin chứa lưu huỳnh (Methionin, Cystein)",
        "d": "Phospholipid và Cholesterol",
        "c_opt": "A",
        "exp": "Acid uric là sản phẩm giáng hóa thoái biến cuối cùng của nhân purin (Adenin, Guanin) có nguồn gốc từ acid nucleic nội sinh và thức ăn ngoại sinh.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nguyên tắc định lượng Acid Uric trong bài thực hành dựa trên phương pháp nào?",
        "a": "Phương pháp enzym so màu đo điểm cuối bằng 2 phản ứng ghép (Uricase và Peroxidase)",
        "b": "Phương pháp đo động học 2 điểm bằng enzym GLDH",
        "c": "Phương pháp tạo phức màu với acid picric trong môi trường kiềm",
        "d": "Phương pháp đo độ đục kết tủa với acid trichloroacetic",
        "c_opt": "A",
        "exp": "Theo giáo trình trang 15: Acid uric trong mẫu thử được định lượng theo phương pháp đo điểm cuối bằng 2 phản ứng enzym liên tiếp: phản ứng Uricase và phản ứng Peroxidase.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Enzym xúc tác cho phản ứng đầu tiên trong quy trình định lượng acid uric là gì?",
        "a": "Uricase",
        "b": "Peroxidase",
        "c": "Urease",
        "d": "Xanthine oxidase",
        "c_opt": "A",
        "exp": "Phản ứng 1: $\\text{Acid uric} + \\ce{H2O} + \\ce{O2} \\xrightarrow{\\text{Uricase}} \\text{Allantoin} + \\ce{CO2} + \\ce{H2O2}$. Enzym xúc tác là Uricase.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Sản phẩm được tạo thành sau phản ứng oxy hóa acid uric dưới tác dụng của enzym Uricase gồm những chất nào?",
        "a": "Allantoin, $\\ce{CO2}$ và $\\ce{H2O2}$",
        "b": "Urê, $\\ce{CO2}$ và $\\ce{NH4+}$",
        "c": "Xanthine, $\\ce{H2O}$ và $\\ce{O2}$",
        "d": "Creatinin và acid phosphoric",
        "c_opt": "A",
        "exp": "Phương trình phản ứng: $\\text{Acid uric} + \\ce{H2O} + \\ce{O2} \\xrightarrow{\\text{Uricase}} \\text{Allantoin} + \\ce{CO2} + \\ce{H2O2}$.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Trong phản ứng thứ hai, $\\ce{H2O2}$ sinh ra phản ứng với những chất nào dưới tác dụng của Peroxidase?",
        "a": "DHBS (3,5 dichloro-2-hydroxybenzen-sulfonic acid) và 4AAP (4-aminoantipyrine)",
        "b": "Phenol và 4-aminoantipyrine",
        "c": "Acid picric và NaOH",
        "d": "NADH và $\\alpha$-ketoglutarate",
        "c_opt": "A",
        "exp": "Phương trình 2: $2\\ce{H2O2} + \\text{DHBS} + \\text{4AAP} \\xrightarrow{\\text{Peroxidase}} \\text{Quinoneimine dye} + \\ce{HCl} + 4\\ce{H2O}$.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tên và màu sắc của phức hợp màu được tạo thành ở phản ứng định lượng acid uric là gì?",
        "a": "Quinoneimine dye, màu hồng cánh sen",
        "b": "Creatinin - picrat, màu vàng cam",
        "c": "Phức chất Biuret, màu tím hồng",
        "d": "Formazan, màu xanh tím",
        "c_opt": "A",
        "exp": "Sản phẩm tạo màu là thuốc nhuộm Quinoneimine (Quinoneimine dye) có phức hợp màu hồng cánh sen đặc trưng.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Hệ đệm được sử dụng trong thuốc thử enzym định lượng acid uric là gì?",
        "a": "Pipes buffer (pH 7,0; 50 mmol/L)",
        "b": "Tris buffer (pH 7,6; 100 mmol/L)",
        "c": "Phosphate buffer (pH 8,0; 20 mmol/L)",
        "d": "Citrate buffer (pH 5,0; 50 mmol/L)",
        "c_opt": "A",
        "exp": "Tài liệu ghi rõ thành phần thuốc thử enzym: Pipes buffer (pH 7,0): 50 mmol/L.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Hoạt độ của enzym Uricase và Peroxidase trong thuốc thử tối thiểu là bao nhiêu?",
        "a": "Uricase > 320 U/L và Peroxidase $\\ge 1000\\text{ U/L}$",
        "b": "Uricase > 10 kU/L và Peroxidase $\\ge 3,8\\text{ kU/L}$",
        "c": "Uricase > 50 U/L và Peroxidase $\\ge 100\\text{ U/L}$",
        "d": "Uricase > 500 U/L và Peroxidase $\\ge 2000\\text{ U/L}$",
        "c_opt": "A",
        "exp": "Bảng thành phần thuốc thử: Uricase > 320 U/L; Peroxidase $\\ge 1000\\text{ U/L}$.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nhiệt độ bảo quản chuẩn của thuốc thử định lượng acid uric là:",
        "a": "2 – 8°C",
        "b": "-20°C",
        "c": "15 – 25°C",
        "d": "37°C",
        "c_opt": "A",
        "exp": "Mục 3 Bảo quản thuốc thử: Các thuốc thử có thể ổn định cho đến ngày hết hạn sử dụng khi được bảo quản ở 2 – 8°C.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Yêu cầu bắt buộc đối với mẫu huyết thanh khi làm xét nghiệm định lượng acid uric là gì?",
        "a": "Không được sử dụng mẫu bị tán huyết",
        "b": "Phải lấy máu vào buổi chiều sau ăn no",
        "c": "Phải làm ấm mẫu ở 56°C trước khi làm",
        "d": "Phải pha loãng huyết thanh 1/100 trước khi đo",
        "c_opt": "A",
        "exp": "Mục 4 Mẫu thử: 'Huyết thanh (không sử dụng mẫu bị tán huyết)'. Tán huyết giải phóng hemoglobin can thiệp quang học và các chất khử nội bào.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nếu sử dụng huyết tương để định lượng acid uric, loại chất chống đông nào được chấp nhận?",
        "a": "Heparin hoặc EDTA",
        "b": "Chỉ duy nhất Natri Citrat",
        "c": "Chất chống đông Oxalat kết hợp Natri Fluorid",
        "d": "Không được dùng huyết tương dưới mọi hình thức",
        "c_opt": "A",
        "exp": "Giáo trình nêu rõ: 'Huyết tương chống đông bằng heparin hay EDTA'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thời gian bảo quản mẫu huyết thanh/huyết tương để định lượng acid uric ở 20 – 25°C và 4 – 8°C lần lượt là:",
        "a": "72 giờ (ở 20 – 25°C) và 7 ngày (ở 4 – 8°C)",
        "b": "24 giờ (ở 20 – 25°C) và 3 ngày (ở 4 – 8°C)",
        "c": "12 giờ (ở 20 – 25°C) và 48 giờ (ở 4 – 8°C)",
        "d": "Không được bảo quản, phải đo ngay trong 1 giờ",
        "c_opt": "A",
        "exp": "Tài liệu ghi: 'có thể bảo quản trong 72 giờ (ở 20 – 25°C), 7 ngày (ở 4 – 8°C), 6 tháng (ở -20°C)'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khi định lượng acid uric trong nước tiểu 24 giờ, mẫu nước tiểu phải được xử lý sơ bộ như thế nào trước khi thử?",
        "a": "Pha loãng theo tỉ lệ 1 nước tiểu : 9 nước cất (pha loãng 1/10)",
        "b": "Pha loãng theo tỉ lệ 1 nước tiểu : 100 nước cất",
        "c": "Để nguyên nước tiểu không pha loãng",
        "d": "Ly tâm bỏ cặn rồi đun sôi trong 5 phút",
        "c_opt": "A",
        "exp": "Tài liệu ghi: 'Nước tiểu 24h, pha loãng tỉ lệ 1 nước tiểu: 9 nước cất'. Khi tính kết quả phải nhân hệ số pha loãng 10.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Để ngăn ngừa sự kết tủa của acid uric trong bình thu thập nước tiểu 24 giờ, cần bổ sung hóa chất nào?",
        "a": "Thêm 15 ml dung dịch NaOH 5M để giữ pH > 8",
        "b": "Thêm 10 ml dung dịch HCl 1M để acid hóa",
        "c": "Thêm 5 ml cồn tuyệt đối để bảo quản",
        "d": "Thêm 10 ml dung dịch Formalin 10%",
        "c_opt": "A",
        "exp": "Giáo trình trang 15: 'để ngăn sự kết tủa của acid uric nên thêm 15ml dung dịch NaOH 5M để giữ pH > 8'. Trong môi trường kiềm, acid uric tạo muối urat hòa tan.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao ở pH nước tiểu toan (< 5,5), acid uric lại rất dễ bị kết tủa?",
        "a": "Vì dạng acid uric tự do có độ tan rất kém trong nước so với dạng muối urat kiềm",
        "b": "Vì enzym uricase bị bất hoạt ở môi trường acid",
        "c": "Vì acid uric bị phân hủy thành allantoin kết tủa",
        "d": "Vì ion $\\ce{H+}$ oxy hóa acid uric thành phức chất không tan",
        "c_opt": "A",
        "exp": "Acid uric có pKa1 khoảng 5,75. Khi pH < 5,5, phần lớn acid uric tồn tại ở dạng phân tử tự do rất khó tan (dễ tạo tinh thể hình thoi lắng cặn hoặc sỏi urat).",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thể tích mẫu thử và thuốc thử trong quy trình định lượng acid uric là bao nhiêu?",
        "a": "12,5 $\\mu$L Mẫu thử + 500 $\\mu$L Thuốc thử",
        "b": "5 $\\mu$L Mẫu thử + 500 $\\mu$L Thuốc thử",
        "c": "50 $\\mu$L Mẫu thử + 500 $\\mu$L Thuốc thử",
        "d": "100 $\\mu$L Mẫu thử + 1000 $\\mu$L Thuốc thử",
        "c_opt": "A",
        "exp": "Bảng mục 5 Tiến hành định lượng: Mẫu thử (HT/ht): 12.5 $\\mu$L; Thuốc thử (Reagent): 500 $\\mu$L.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Điều kiện ủ phản ứng định lượng acid uric trong bài thực hành là:",
        "a": "Trộn đều và ủ 5 phút ở 37°C",
        "b": "Trộn đều và để ở nhiệt độ phòng 20 phút",
        "c": "Ủ trong 30 giây ở 25°C",
        "d": "Đun cách thủy 100°C trong 3 phút",
        "c_opt": "A",
        "exp": "Mục 5 ghi rõ: 'Trộn đều và ủ 5 phút ở 37°C'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Bước sóng quang phổ kế dùng để đo mật độ quang của phản ứng định lượng acid uric là bao nhiêu?",
        "a": "505 nm",
        "b": "530 nm",
        "c": "340 nm",
        "d": "405 nm",
        "c_opt": "A",
        "exp": "Theo giáo trình trang 16: 'Sau đó tiến hành đo mật độ quang ở bước sóng 505nm và ghi nhận lại kết quả hiển thị trên máy.'",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Độ bền màu của phức hợp màu hồng cánh sen trong phản ứng acid uric kéo dài trong bao lâu?",
        "a": "15 phút, tránh tiếp xúc trực tiếp với ánh sáng mặt trời",
        "b": "60 phút ở ngoài sáng",
        "c": "30 giây sau khi trộn",
        "d": "Bền vững trong 24 giờ",
        "c_opt": "A",
        "exp": "Tài liệu ghi: 'Độ bền màu: 15 phút, tránh tiếp xúc trực tiếp với ánh sáng mặt trời'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng tuyến tính (Linearity) của xét nghiệm định lượng acid uric được nêu trong bài là:",
        "a": "0,49 – 25 mg/dL",
        "b": "11,5 – 300 mg/dL",
        "c": "0,1 – 10 mg/dL",
        "d": "10 – 500 $\\mu$mol/L",
        "c_opt": "A",
        "exp": "Tài liệu ghi rõ: 'Độ tuyến tính: 0,49 – 25mg/dl'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nếu nồng độ acid uric của bệnh nhân vượt quá 25 mg/dL, kỹ thuật viên cần làm gì?",
        "a": "Pha loãng mẫu thử bằng nước muối sinh lý (NaCl 0,9%), làm lại xét nghiệm rồi nhân kết quả với độ pha loãng",
        "b": "Báo kết quả ngay là > 25 mg/dL mà không cần làm lại",
        "c": "Tăng thể tích thuốc thử lên gấp 10 lần",
        "d": "Ủ phản ứng trong thời gian dài hơn (30 phút)",
        "c_opt": "A",
        "exp": "Khi vượt quá giới hạn tuyến tính của phản ứng enzym, định luật Beer-Lambert không còn đúng, bắt buộc phải pha loãng mẫu và nhân hệ số pha loãng.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Ngưỡng can thiệp của Hemoglobin, Bilirubin và Triglycerides ảnh hưởng đến kết quả định lượng acid uric lần lượt là:",
        "a": "Hemoglobin > 1 g/dL, Bilirubin > 40 mg/dL, Triglycerides > 2 g/dL",
        "b": "Hemoglobin > 0,75 g/dL, Bilirubin > 30 mg/dL, Triglycerides > 2 g/dL",
        "c": "Hemoglobin > 2 g/dL, Bilirubin > 10 mg/dL, Triglycerides > 5 g/dL",
        "d": "Không có chất nào gây can thiệp vào phản ứng enzym",
        "c_opt": "A",
        "exp": "Chú ý trang 16: 'hemoglobin > 1g/dl, bilirubin > 40mg/dl, triglycerides > 2g/dl sẽ ảnh hưởng đến kết quả xét nghiệm'.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng tham chiếu nồng độ acid uric trong huyết thanh/huyết tương ở NAM GIỚI trưởng thành là:",
        "a": "210 – 432 $\\mu$mol/L (3,5 – 7,2 mg/dL)",
        "b": "156 – 360 $\\mu$mol/L (2,6 – 6,0 mg/dL)",
        "c": "53 – 97 $\\mu$mol/L (0,6 – 1,1 mg/dL)",
        "d": "2,8 – 7,2 mmol/L (17 – 43 mg/dL)",
        "c_opt": "A",
        "exp": "Giá trị tham chiếu: Nam: 210 – 432 $\\mu$mol/L (3,5 – 7,2 mg/dL).",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khoảng tham chiếu nồng độ acid uric trong huyết thanh/huyết tương ở NỮ GIỚI trưởng thành là:",
        "a": "156 – 360 $\\mu$mol/L (2,6 – 6,0 mg/dL)",
        "b": "210 – 432 $\\mu$mol/L (3,5 – 7,2 mg/dL)",
        "c": "44 – 80 $\\mu$mol/L (0,5 – 0,9 mg/dL)",
        "d": "1,5 – 4,5 mmol/L",
        "c_opt": "A",
        "exp": "Giá trị tham chiếu: Nữ: 156 – 360 $\\mu$mol/L (2,6 – 6,0 mg/dL).",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao trị số acid uric máu bình thường ở nam giới lại cao hơn nữ giới trong độ tuổi sinh sản?",
        "a": "Do hormon estrogen ở nữ thúc đẩy sự bài tiết acid uric qua thận",
        "b": "Do nam giới tổng hợp enzym uricase nhiều hơn",
        "c": "Do nữ giới không ăn thức ăn chứa nhân purin",
        "d": "Do thể tích máu của nữ giới lớn hơn nam giới",
        "c_opt": "A",
        "exp": "Estrogen có tác dụng cạnh tranh hoặc tăng cường đào thải acid uric qua ống thận. Sau mãn kinh, nồng độ acid uric ở nữ giới tăng lên tương đương nam giới.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Lượng acid uric đào thải qua nước tiểu 24 giờ ở người bình thường là bao nhiêu?",
        "a": "250 – 750 mg/24 giờ (1,5 – 4,5 mmol/24 giờ)",
        "b": "1000 – 1500 mg/24 giờ",
        "c": "26 – 43 g/24 giờ",
        "d": "50 – 100 mg/24 giờ",
        "c_opt": "A",
        "exp": "Tài liệu ghi: 'Nước tiểu: 250 – 750 mg/24 giờ hay 1,5 – 4,5 mmol/24 giờ'.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Bệnh lý điển hình nhất gây tăng acid uric máu NGUYÊN PHÁT là bệnh gì?",
        "a": "Bệnh thống phong (Gout)",
        "b": "Bệnh đái tháo đường",
        "c": "Bệnh suy tim ứ huyết",
        "d": "Bệnh xơ gan mất bù",
        "c_opt": "A",
        "exp": "Mục Biện luận nêu: 'Bệnh lý: acid uric máu và nước tiểu tăng: + Nguyên phát: bệnh thống phong (Gout)'.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Nhóm bệnh lý ác tính hệ tạo máu nào gây tăng acid uric THỨ PHÁT do tăng phá hủy tế bào?",
        "a": "Đa hồng cầu, bạch cầu cấp (leukemia), u hạch (lymphoma)",
        "b": "Thiếu máu thiếu sắt",
        "c": "Bệnh ưa chảy máu Hemophilia",
        "d": "Giảm tiểu cầu vô căn",
        "c_opt": "A",
        "exp": "Trong các bệnh máu ác tính, tốc độ tăng sinh và chết tế bào nhân rất cao, giải phóng lượng lớn nucleic acid làm tăng acid uric máu thứ phát.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Tại sao điều trị ung thư bằng tia X, chất phóng xạ hoặc hóa chất chống chuyển hóa lại làm tăng vọt acid uric máu?",
        "a": "Hội chứng tiêu hủy khối u (Tumor lysis syndrome) giải phóng ồ ạt acid nucleic vào máu",
        "b": "Tia X kích thích trực tiếp enzym uricase",
        "c": "Thuốc hóa trị gây ức chế lọc cầu thận hoàn toàn",
        "d": "Tia phóng xạ chuyển hóa mỡ thành acid uric",
        "c_opt": "A",
        "exp": "Giáo trình nêu: '+ Thứ phát: Trong trường hợp điều trị bằng tia X, chất phóng xạ, chất chống chuyển hóa...' do phá hủy tế bào u hàng loạt làm giải phóng purin.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Bệnh lý tại thận nào sau đây làm tăng acid uric máu do suy giảm khả năng bài tiết qua nước tiểu?",
        "a": "Viêm thận mãn, suy thận",
        "b": "Nhiễm khuẩn bàng quang cấp",
        "c": "Hội chứng thận hư đơn thuần",
        "d": "Sỏi san hô chưa gây ứ nước",
        "c_opt": "A",
        "exp": "Tài liệu ghi: '- Trong các bệnh về thận: viêm thận mãn, suy thận'. Khi chức năng lọc của cầu thận giảm, acid uric bị giữ lại trong máu gây tăng nồng độ.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Khi nồng độ acid uric huyết thanh vượt quá ngưỡng hòa tan sinh lý (khoảng > 420 $\\mu$mol/L hay > 7 mg/dL), hiện tượng gì xảy ra?",
        "a": "Lắng đọng tinh thể Monosodium Urat (MSU) tại các khớp và mô bào tạo hạt tophi",
        "b": "Acid uric lập tức chuyển hóa thành urê và bài tiết hết",
        "c": "Làm tan rã màng hồng cầu gây thiếu máu tán huyết",
        "d": "Gây giảm nồng độ protein toàn phần xuống < 40 g/L",
        "c_opt": "A",
        "exp": "Bão hòa acid uric làm kết tinh tinh thể muối Monosodium Urat hình kim nhọn tại bao khớp, kích hoạt phản ứng viêm khớp Gout cấp tính và tạo hạt tophi.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một bệnh nhân nam 48 tuổi vào viện vì sưng đau dữ dội khớp ngón chân cái. Kết quả xét nghiệm acid uric máu là $520\\text{ }\\mu\\text{mol/L}$. Nhận định kết quả này:",
        "a": "Acid uric máu tăng cao, phù hợp với cơn Gout cấp",
        "b": "Acid uric máu bình thường đối với nam giới",
        "c": "Acid uric máu giảm do suy gan",
        "d": "Chưa đủ tiêu chuẩn tăng acid uric máu",
        "c_opt": "A",
        "exp": "Khoảng tham chiếu ở nam là 210 – 432 $\\mu$mol/L. Giá trị $520\\text{ }\\mu\\text{mol/L} > 432\\text{ }\\mu\\text{mol/L}$ là tăng rõ rệt, kết hợp vị trí sưng khớp bàn ngón chân cái điển hình của Gout.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một bệnh nhân nữ có nồng độ acid uric máu là 252 $\\mu$mol/L. Kết luận xét nghiệm này là:",
        "a": "Nằm trong giới hạn bình thường của nữ (156 – 360 $\\mu$mol/L)",
        "b": "Tăng cao vượt ngưỡng bình thường",
        "c": "Giảm nặng cần bù đạm",
        "d": "Nghi ngờ bệnh đa u tủy",
        "c_opt": "A",
        "exp": "Giá trị tham chiếu ở nữ là 156 – 360 $\\mu$mol/L. Nồng độ 252 $\\mu$mol/L nằm hoàn toàn trong giới hạn sinh lý bình thường.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Công thức quy đổi nồng độ acid uric từ mg/dL sang $\\mu$mol/L xấp xỉ bằng cách:",
        "a": "Nhân với 59,48",
        "b": "Chia cho 6",
        "c": "Nhân với 88,4",
        "d": "Chia cho 10",
        "c_opt": "A",
        "exp": "Phân tử lượng acid uric $\\ce{C5H4N4O3} = 168,11\\text{ g/mol}$. $1\\text{ mg/dL} = 10\\text{ mg/L} = 10 / 0,16811 \\approx 59,48\\text{ }\\mu\\text{mol/L}$.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Một mẫu acid uric đo được nồng độ 6,0 mg/dL. Quy đổi sang đơn vị $\\mu$mol/L là khoảng:",
        "a": "Khoảng 357 $\\mu$mol/L",
        "b": "Khoảng 530 $\\mu$mol/L",
        "c": "Khoảng 210 $\\mu$mol/L",
        "d": "Khoảng 156 $\\mu$mol/L",
        "c_opt": "A",
        "exp": "$6,0 \\times 59,48 \\approx 356,9\\text{ }\\mu\\text{mol/L}$.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Thuốc Allopurinol thường dùng trong điều trị bệnh Gout hạ acid uric máu theo cơ chế nào?",
        "a": "Ức chế enzym Xanthine Oxidase làm giảm tổng hợp acid uric",
        "b": "Kích thích enzym Uricase ở người",
        "c": "Tăng cường tái hấp thu acid uric tại ống thận",
        "d": "Phá hủy trực tiếp tinh thể tophi",
        "c_opt": "A",
        "exp": "Allopurinol là chất ức chế cạnh tranh với enzym Xanthine Oxidase, ngăn cản quá trình chuyển Hypoxanthine -> Xanthine -> Acid Uric.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Loài người và linh trưởng bậc cao dễ bị tăng acid uric máu hơn các loài động vật có vú khác vì lý do di truyền nào?",
        "a": "Gen mã hóa enzym Uricase bị đột biến bất hoạt trong quá trình tiến hóa",
        "b": "Cầu thận người không lọc được acid uric",
        "c": "Người ăn nhiều thịt hơn tất cả động vật khác",
        "d": "Ống thận người không có thụ thể bài tiết acid uric",
        "c_opt": "A",
        "exp": "Ở đa số động vật có vú, enzym Uricase biến đổi acid uric thành Allantoin rất dễ tan. Ở người, gen Uricase bị đột biến mất chức năng, do đó acid uric là sản phẩm thoái hóa cuối cùng.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Trong thí nghiệm đo acid uric, nếu không ủ đủ 5 phút ở 37°C mà đo ngay thì kết quả sẽ ra sao?",
        "a": "Giảm giả tạo vì phản ứng enzym chưa đạt tới điểm kết thúc",
        "b": "Tăng giả tạo vì phức chất bị phân hủy",
        "c": "Không ảnh hưởng gì",
        "d": "Dung dịch bị đục không đo được",
        "c_opt": "A",
        "exp": "Đây là phương pháp đo điểm cuối dùng enzym, nếu thời gian và nhiệt độ ủ chưa đủ thì lượng $\\ce{H2O2}$ và Quinoneimine sinh ra chưa cực đại, dẫn đến OD thấp làm kết quả giảm giả tạo.",
        "diff": "medium",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Chế độ ăn nào sau đây KHUYẾN CÁO nên hạn chế ở bệnh nhân tăng acid uric máu và Gout?",
        "a": "Thịt đỏ (thịt bò, chó, dê), phủ tạng động vật (tim, gan, thận), hải sản, bia rượu",
        "b": "Rau xanh, cà rốt, dưa chuột",
        "c": "Trứng gà và sữa chua",
        "d": "Gạo tẻ và ngũ cốc nguyên hạt",
        "c_opt": "A",
        "exp": "Thịt đỏ, phủ tạng và hải sản giàu nhân purin; bia rượu kích thích dị hóa purin và acid lactic cạnh tranh đào thải acid uric ở ống thận.",
        "diff": "easy",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    },
    {
        "q": "Xét nghiệm acid uric trong nước tiểu 24 giờ có ý nghĩa quan trọng nhất trong việc:",
        "a": "Phân biệt tăng acid uric do tăng sản xuất hay do giảm đào thải tại thận",
        "b": "Chẩn đoán xác định đái tháo đường",
        "c": "Đánh giá mức độ tổn thương gan",
        "d": "Đo áp lực keo huyết tương",
        "c_opt": "A",
        "exp": "Nếu acid uric máu tăng kèm acid uric niệu > 750 mg/24h -> tăng sản xuất; nếu acid uric máu tăng mà acid uric niệu < 600 mg/24h -> giảm bài tiết qua thận.",
        "diff": "hard",
        "tag": "Bài 2: Chuyển hóa Protid & Chức năng thận"
    }
]

print(f"Loaded Part 2: {len(QUESTIONS_PART2)} questions")
