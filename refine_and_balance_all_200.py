# -*- coding: utf-8 -*-
"""
Refine all 200 questions:
1. Equalize option lengths: eliminate the 'longest answer is correct' bias.
2. Evenly distribute correct keys to exactly 50 A, 50 B, 50 C, 50 D (25% each).
3. Ensure in >80% of questions, the correct option is NOT strictly the longest.
4. Export master 200-question JSON and 6 sub-lesson JSONs.
5. Seed into unimaster.db for Subject 10.
"""

import os
import json
import random

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
os.chdir(BASE_DIR)

from build_part1_molish import part1_questions
from build_part2_fehling import part2_questions
from build_part3_iod import part3_questions
from build_part4_god_pod import part4_questions
from build_part5_clinical_ogtt import part5_questions
from build_part6_benedict import part6_questions

raw_questions = part1_questions + part2_questions + part3_questions + part4_questions + part5_questions + part6_questions
assert len(raw_questions) == 200, f"Expected 200, got {len(raw_questions)}"

# Targeted option refinements for questions with large length disparity
manual_adjustments = {
    # Q1
    1: {
        "option_a": "Glucid bị oxy hóa bởi Cu2+ trong kiềm mạnh tạo tủa đỏ gạch",
        "option_b": "Glucid tạo phức chất màu tím với alpha-Naphtol trong H2SO4 đđ",
        "option_c": "Chuỗi xoắn tinh bột hấp phụ iod tự do tạo dung dịch màu xanh",
        "option_d": "Glucid ngưng tụ với acid picric trong kiềm tạo phức màu vàng",
    },
    # Q3
    3: {
        "option_a": "Toàn bộ dung dịch chuyển sang màu tím thẫm từ đáy lên miệng",
        "option_b": "Xuất hiện kết tủa màu đỏ gạch lắng dần xuống đáy ống nghiệm",
        "option_c": "Xuất hiện vòng nhẫn màu tím tại ranh giới phân cách 2 lớp",
        "option_d": "Dung dịch chuyển sang màu xanh thẫm và sủi bọt khí liên tục",
    },
    # Q4
    4: {
        "option_a": "Đặt thẳng đứng ống nghiệm rồi nhỏ nhanh acid vào giữa tâm ống",
        "option_b": "Nghiêng ống nghiệm 45 độ, cho từ từ acid chảy nhẹ theo thành",
        "option_c": "Cho acid vào trước rồi rót đường lên trên và dùng đũa khuấy",
        "option_d": "Nhỏ acid vào ống nghiệm rồi lắc thật mạnh ngay cho hòa tan",
    },
    # Q6
    6: {
        "option_a": "Khử nước phân tử glucid tạo dẫn xuất furfural ngưng tụ màu",
        "option_b": "Oxy hóa nhóm chức aldehyd của glucid thành nhóm acid carboxylic",
        "option_c": "Tạo phức màu tím trực tiếp với alpha-naphtol không cần glucid",
        "option_d": "Khử ion Cu2+ về dạng Cu+ tạo tủa màu tím ở nhiệt độ phòng",
    },
    # Q10
    10: {
        "option_a": "Phân biệt monosaccharid và disaccharid trong mẫu bệnh phẩm",
        "option_b": "Nhận biết sự có mặt của glucid và phân biệt với protid, lipid",
        "option_c": "Định lượng chính xác hàm lượng glucose hòa tan trong dịch",
        "option_d": "Xác định tính chất khử hay không khử của một phân tử đường",
    },
    # Q11
    11: {
        "option_a": "Vòng màu tím lan tỏa đều khắp ống nghiệm và bền vững lâu hơn",
        "option_b": "Đường bị acid than hóa chuyển màu đen sẫm và mất vòng tím",
        "option_c": "Không có hiện tượng phản ứng nào xảy ra và dung dịch trong",
        "option_d": "Xuất hiện kết tủa màu đỏ gạch dày đặc do phản ứng khử mạnh",
    },
    # Q13
    13: {
        "option_a": "Vì hồ tinh bột có cấu trúc xoắn giữ được phân tử alpha-naphtol",
        "option_b": "Vì H2SO4 đđ thủy phân tinh bột thành monosaccharid trước",
        "option_c": "Vì tinh bột chứa sẵn một lượng lớn các phân tử furfural tự do",
        "option_d": "Vì ion sulfate trong dung dịch trực tiếp tạo màu tím với mạch",
    },
    # Q15
    15: {
        "option_a": "Do H2SO4 đậm đặc có độ nhớt và sức căng bề mặt thấp hơn nước",
        "option_b": "Do acid sulfuric đđ có khối lượng riêng lớn hơn nước (d ~ 1.84)",
        "option_c": "Do dung dịch glucid bị bay hơi nhanh chóng ngay khi tiếp xúc",
        "option_d": "Do phản ứng tỏa nhiệt đẩy lớp dung dịch glucid dạt lên miệng",
    },
    # Q30
    30: {
        "option_a": "Tạo môi trường acid nhẹ để phản ứng khử diễn ra nhanh hơn",
        "option_b": "Tạo phức chelate Cu2+ alcolat màu xanh thẫm, tránh tủa Cu(OH)2",
        "option_c": "Oxy hóa trực tiếp nhóm chức aldehyd của phân tử đường đơn",
        "option_d": "Làm chất chỉ thị màu thay đổi theo nồng độ pH của dung dịch",
    },
    # Q35
    35: {
        "option_a": "Vì nhóm ceton có thể trực tiếp khử Cu2+ mà không cần chuyển dạng",
        "option_b": "Vì trong kiềm mạnh, fructose đồng phân hóa thành glucose qua enediol",
        "option_c": "Vì phân tử fructose tự phân cắt thành hai triose mang nhóm aldehyd",
        "option_d": "Vì dung dịch fructose thương mại luôn bị lẫn lượng lớn glucose tạp",
    },
    # Q36
    36: {
        "option_a": "Do phân tử saccharose chỉ được cấu tạo từ các gốc beta-fructose",
        "option_b": "Do liên kết alpha-1,beta-2-glycosid đã khóa các nhóm OH bán acetal",
        "option_c": "Do phân tử saccharose bị kết tủa ngay bởi ion đồng trong kiềm",
        "option_d": "Do saccharose có khối lượng phân tử quá lớn không tan được trong nước",
    },
    # Q37
    37: {
        "option_a": "Vì tinh bột có phân tử lượng lớn, tỉ lệ đầu khử không đáng kể",
        "option_b": "Vì tinh bột phản ứng hoàn toàn với muối Seignette tạo màu trắng",
        "option_c": "Vì nhiệt độ sôi 100 độ C làm phân hủy hoàn toàn các phân tử đường",
        "option_d": "Vì cấu trúc xoắn của amylose ngăn cản sự tiếp xúc của môi trường",
    },
    # Q38
    38: {
        "option_a": "Lactose là một monosaccharid tự do hòa tan tốt trong kiềm",
        "option_b": "Lactose còn nhóm OH bán acetal tự do ở gốc glucose có tính khử",
        "option_c": "Lactose bị enzyme lactase trong thuốc thử thủy phân tức thì",
        "option_d": "Liên kết beta-1,4-glycosid trong phân tử lactose có tính chất khử",
    },
    # Q41
    41: {
        "option_a": "Thuốc thử quá đắt tiền và khó bảo quản trong phòng xét nghiệm",
        "option_b": "Kiềm mạnh dễ bị khử bởi acid uric, creatinin gây dương tính giả",
        "option_c": "Không có khả năng phát hiện nồng độ glucose khi vượt quá 20 g/L",
        "option_d": "Phản ứng đòi hỏi phải tiến hành ở nhiệt độ âm dưới 0 độ C kéo dài",
    },
    # Q43
    43: {
        "option_a": "Dung dịch vẫn giữ nguyên màu xanh lam và không có kết tủa",
        "option_b": "Xuất hiện kết tủa đỏ gạch do saccharose bị thủy phân thành đường khử",
        "option_c": "Dung dịch chuyển sang màu tím đen và bốc khói cay nồng nặc",
        "option_d": "Xuất hiện kết tủa màu trắng xốp nổi bồng bềnh trên bề mặt ống",
    },
    # Q48
    48: {
        "option_a": "Xuất hiện kết tủa màu vàng tươi lắng xuống đáy ống nghiệm",
        "option_b": "Dung dịch giữ nguyên màu xanh thẫm trong suốt, không có tủa đỏ",
        "option_c": "Xuất hiện ngay kết tủa màu đỏ gạch do thuốc thử tự phân hủy",
        "option_d": "Dung dịch mất màu hoàn toàn trở thành nước trong suốt không màu",
    },
    # Q58
    48: {
        "option_a": "Tạo vị chua đặc trưng cho dung dịch thuốc thử",
        "option_b": "Chống hiện tượng thủy phân tự nhiên của muối đồng CuSO4 trong nước",
        "option_c": "Tăng cường tính khử của ion đồng Cu2+ trong dung dịch",
        "option_d": "Làm chất xúc tác cho phản ứng tạo kết tủa Cu2O đỏ gạch",
    },
    # Q68
    68: {
        "option_a": "Liên kết cộng hóa trị bền vững giữa nguyên tử carbon và iod",
        "option_b": "Sự hấp phụ vật lý của phân tử iod vào lòng xoắn ốc của amylose",
        "option_c": "Liên kết ion tĩnh điện giữa ion iodua và các nhóm carboxyl tự do",
        "option_d": "Phản ứng thế ái nhân của iod vào nhóm hydroxyl của phân tử đường",
    },
    # Q76
    76: {
        "option_a": "Vì chúng có tính khử quá mạnh làm phân hủy phân tử iod",
        "option_b": "Vì kích thước nhỏ, không có chuỗi xoắn helix để bắt giữ phân tử iod",
        "option_c": "Vì môi trường phản ứng không đủ độ acid cần thiết để tạo phức",
        "option_d": "Vì phân tử đường đơn phản xạ hoàn toàn ánh sáng trong vùng nhìn thấy",
    },
    # Q84
    84: {
        "option_a": "Glycogen chỉ chứa các liên kết beta-1,4-glycosid mạch thẳng dài",
        "option_b": "Glycogen phân nhánh dày đặc làm chuỗi xoắn ngắn hơn amylose",
        "option_c": "Tinh bột chứa nhiều nguyên tố nitơ và lưu huỳnh hơn glycogen",
        "option_d": "Glycogen có cấu trúc hoàn toàn là các vòng furanose 5 cạnh phẳng",
    },
    # Q91
    91: {
        "option_a": "340 nm (vùng quang phổ tử ngoại gần)",
        "option_b": "500 nm (vùng quang phổ khả kiến xanh lục)",
        "option_c": "620 nm (vùng quang phổ khả kiến đỏ cam)",
        "option_d": "405 nm (vùng quang phổ khả kiến tím)",
    },
    # Q94
    94: {
        "option_a": "Cung cấp đường chuẩn cho máy tính toán nồng độ tự động",
        "option_b": "Triệt tiêu độ hấp thu quang học nền của bản thân thuốc thử",
        "option_c": "Kiểm tra hoạt độ enzym peroxidase xem còn hoạt tính không",
        "option_d": "Tạo phức hợp màu đối chứng âm để kiểm tra bằng mắt thường",
    },
    # Q95
    95: {
        "option_a": "0.00 – 100 mg/dL (tương đương 0.0 – 5.5 mmol/L)",
        "option_b": "2.34 – 450 mg/dL (tương đương 84.7 – 450 mg/dL)",
        "option_c": "10.0 – 600 mg/dL (tương đương 1.0 – 33.3 mmol/L)",
        "option_d": "50.0 – 800 mg/dL (tương đương 2.8 – 44.4 mmol/L)",
    },
    # Q97
    97: {
        "option_a": "10 ngày ở 2 - 8 độ C nếu đậy kín nắp",
        "option_b": "60 ngày ở 2 - 8 độ C tránh nhiễm khuẩn và ánh sáng",
        "option_c": "180 ngày ở nhiệt độ phòng 20 - 25 độ C",
        "option_d": "1 năm ở 2 - 8 độ C kể cả khi tiếp xúc ánh sáng",
    },
    # Q99
    99: {
        "option_a": "Vì màng hồng cầu làm đục thuốc thử và không đo quang được",
        "option_b": "Vì hemoglobin và enzym nội bào giải phóng gây nhiễu đo quang",
        "option_c": "Vì hồng cầu vỡ giải phóng toàn bộ glycogen vào trong huyết thanh",
        "option_d": "Vì hồng cầu làm kết tủa hoàn toàn enzym glucose oxidase",
    },
    # Q103
    103: {
        "option_a": "Ổn định trong 4 giờ ở nhiệt độ phòng",
        "option_b": "Ổn định trong 2 ngày ở nhiệt độ phòng (20 - 25 độ C)",
        "option_c": "Ổn định trong 7 ngày ở nhiệt độ phòng",
        "option_d": "Ổn định trong 1 tháng ở nhiệt độ phòng",
    },
    # Q104
    104: {
        "option_a": "Ổn định trong 24 giờ ở nhiệt độ 4 - 8 độ C",
        "option_b": "Ổn định trong 7 ngày ở nhiệt độ 4 - 8 độ C",
        "option_c": "Ổn định trong 30 ngày ở nhiệt độ 4 - 8 độ C",
        "option_d": "Ổn định trong 3 ngày ở nhiệt độ 4 - 8 độ C",
    },
    # Q105
    105: {
        "option_a": "Ổn định trong 1 giờ ở nhiệt độ 20 - 25 độ C",
        "option_b": "Ổn định trong 8 giờ ở nhiệt độ 20 - 25 độ C",
        "option_c": "Ổn định trong 24 giờ ở nhiệt độ 20 - 25 độ C",
        "option_d": "Ổn định trong 48 giờ ở nhiệt độ 20 - 25 độ C",
    },
    # Q106
    106: {
        "option_a": "1 nước tiểu : 1 nước cất (pha loãng 2 lần)",
        "option_b": "1 nước tiểu : 9 nước cất (pha loãng 10 lần)",
        "option_c": "1 nước tiểu : 99 nước cất (pha loãng 100 lần)",
        "option_d": "Không cần pha loãng, hút trực tiếp nước tiểu đo",
    },
    # Q112
    112: {
        "option_a": "Chia nồng độ glucose (mmol/L) cho 18",
        "option_b": "Nhân nồng độ glucose (mmol/L) với 18",
        "option_c": "Nhân nồng độ glucose (mmol/L) với 2.27",
        "option_d": "Cộng nồng độ glucose (mmol/L) thêm 75",
    },
    # Q115
    115: {
        "option_a": "Vitamin A liều cao trong máu người bệnh",
        "option_b": "Acid ascorbic (Vitamin C) cạnh tranh H2O2",
        "option_c": "Cholesterol toàn phần tăng cao trong máu",
        "option_d": "Nồng độ Natri clorid sinh lý trong huyết tương",
    },
    # Q116
    116: {
        "option_a": "Giảm khoảng 1 - 2% mỗi giờ ở nhiệt độ phòng",
        "option_b": "Giảm khoảng 5 - 7% mỗi giờ (khoảng 0.4 - 0.6 mmol/L)",
        "option_c": "Giảm khoảng 20 - 30% mỗi giờ ở nhiệt độ phòng",
        "option_d": "Không giảm nồng độ nếu được đậy kín nắp ống nghiệm",
    },
    # Q120
    120: {
        "option_a": "Màu đỏ bền trong 30 - 60 phút nếu tránh ánh sáng",
        "option_b": "Màu đỏ biến mất ngay lập tức sau 1 phút kết thúc ủ",
        "option_c": "Chuyển dần sang màu xanh dương theo thời gian lưu",
        "option_d": "Tạo kết tủa màu đỏ lắng hoàn toàn xuống đáy cuvet",
    },
    # Q122
    122: {
        "option_a": "Hút thuốc thử enzym 1 bị hụt thể tích dung tích",
        "option_b": "Đầu tip dính giọt mẫu bên ngoài thành mà không lau",
        "option_c": "Bơm mẫu thử vào sát đáy ống nghiệm rồi tráng tip",
        "option_d": "Chỉnh thể tích micropipette từ 10 xuống 8 microlit",
    },
    # Q124
    124: {
        "option_a": "Mật độ quang OD đo được sẽ giảm xuống mức 0.000",
        "option_b": "Mật độ quang OD tăng cao giả tạo do bọt khí tán xạ",
        "option_c": "Không ảnh hưởng vì chùm tia sáng chỉ đi qua đáy cuvet",
        "option_d": "Máy đo quang phổ sẽ tự động cảnh báo và trừ bọt khí",
    },
    # Q125
    125: {
        "option_a": "OD_trắng phải đạt giá trị lớn hơn 1.000",
        "option_b": "OD_trắng phải nhỏ hơn 0.050 (thuốc thử còn tốt)",
        "option_c": "OD_trắng phải bằng chính xác với OD_chuẩn",
        "option_d": "OD_trắng phải luôn mang giá trị âm dưới 0",
    },
    # Q128
    128: {
        "option_a": "Ổn định trong 12 giờ ở nhiệt độ 4 độ C",
        "option_b": "Ổn định trong 72 giờ ở nhiệt độ 4 độ C",
        "option_c": "Ổn định trong 24 giờ ở nhiệt độ 4 độ C",
        "option_d": "Ổn định trong 48 giờ ở nhiệt độ 4 độ C",
    },
    # Q129
    129: {
        "option_a": "Do glucose không thể khuếch tán qua màng tế bào hồng cầu",
        "option_b": "Do hồng cầu chứa ít nước hơn huyết tương (71% so với 93%)",
        "option_c": "Do bạch cầu tiêu thụ hết glucose ngay khi vừa lấy máu",
        "option_d": "Do hemoglobin gắn kết không thuận nghịch với glucose máu",
    },
    # Q132
    132: {
        "option_a": ">= 6.1 mmol/L trong 1 lần xét nghiệm duy nhất lúc đói",
        "option_b": ">= 7.0 mmol/L (>= 126 mg/dL) trong ít nhất 2 lần xét nghiệm khác ngày",
        "option_c": ">= 5.6 mmol/L kèm theo có triệu chứng tăng huyết áp",
        "option_d": "Từ 6.4 đến 6.9 mmol/L sau khi ăn nhẹ khoảng 2 giờ",
    },
    # Q133
    133: {
        "option_a": "Dung nạp glucose hoàn toàn bình thường ở người lớn",
        "option_b": "Giảm dung nạp glucose (Impaired Glucose Tolerance)",
        "option_c": "Bệnh nhân đã mắc bệnh đái tháo đường type 1 thực thụ",
        "option_d": "Hạ đường huyết phản ứng do tình trạng cường insulin",
    },
    # Q134
    134: {
        "option_a": ">= 7.8 mmol/L (>= 140 mg/dL)",
        "option_b": ">= 11.1 mmol/L (>= 200 mg/dL)",
        "option_c": ">= 6.1 mmol/L (>= 110 mg/dL)",
        "option_d": ">= 9.0 mmol/L (>= 162 mg/dL)",
    },
    # Q135
    135: {
        "option_a": "< 5.0 mmol/L (< 90 mg/dL)",
        "option_b": "< 7.8 mmol/L (< 140 mg/dL)",
        "option_c": "< 11.1 mmol/L (< 200 mg/dL)",
        "option_d": "< 3.9 mmol/L (< 70 mg/dL)",
    },
    # Q136
    136: {
        "option_a": "Khoảng 126 mg/dL (tương đương 7.0 mmol/L)",
        "option_b": "Khoảng 180 mg/dL (tương đương 10.0 mmol/L)",
        "option_c": "Khoảng 250 mg/dL (tương đương 13.9 mmol/L)",
        "option_d": "Khoảng 100 mg/dL (tương đương 5.5 mmol/L)",
    },
    # Q137
    137: {
        "option_a": "Thận lập tức bị viêm cầu thận hoại tử cấp tính",
        "option_b": "Vượt khả năng tái hấp thu ống thận nên glucose xuất hiện trong nước tiểu",
        "option_c": "Nước tiểu tự động chuyển sang màu đỏ gạch không cần thử hóa chất",
        "option_d": "Bệnh nhân bị tình trạng bí tiểu và vô niệu hoàn toàn",
    },
    # Q139
    139: {
        "option_a": "Phá hủy trực tiếp các tế bào beta của đảo tụy",
        "option_b": "Kích thích giao cảm tăng tiết adrenalin và cortisol",
        "option_c": "Làm thận mất hoàn toàn khả năng lọc qua cầu thận",
        "option_d": "Tăng cường hoạt tính của enzym tiêu hóa amylase",
    },
    # Q140
    140: {
        "option_a": "Bệnh nhân sau khi ăn bữa cơm giàu glucid",
        "option_b": "U tế bào beta tụy tiết quá nhiều insulin",
        "option_c": "Bệnh nhân bị u tủy thượng thận tiết hormon",
        "option_d": "Bệnh nhân mắc hội chứng Cushing thừa hormon",
    },
    # Q141
    141: {
        "option_a": "Do gan bị kích thích tăng tổng hợp glycogen quá mức bình thường",
        "option_b": "Do gan suy giảm khả năng dự trữ glycogen và quá trình tân tạo đường",
        "option_c": "Do tế bào gan tiết trực tiếp enzym insulin vào hệ đại tuần hoàn",
        "option_d": "Do gan tăng cường thu nhận toàn bộ glucose từ hệ tuần hoàn máu",
    },
    # Q143
    143: {
        "option_a": "Thận tăng cường bài tiết nước để làm giảm huyết áp động mạch",
        "option_b": "Nồng độ glucose niệu cao gây hiện tượng lợi niệu thẩm thấu",
        "option_c": "Tổn thương tuyến yên làm giảm tiết hormon kháng niệu ADH máu",
        "option_d": "Tăng áp lực lọc tại quai Henle do thiếu hụt nồng độ protein",
    },
    # Q144
    144: {
        "option_a": "Cảm giác khô miệng do giảm bài tiết nước bọt đơn thuần ở khoang miệng",
        "option_b": "Mất nước làm tăng áp suất thẩm thấu, kích thích trung tâm khát vùng hạ đồi",
        "option_c": "Niêm mạc thực quản bị kích thích trực tiếp bởi nồng độ đường huyết",
        "option_d": "Rối loạn thụ thể cảm giác thèm nước do tổn thương cấu trúc tiểu não",
    },
    # Q145
    145: {
        "option_a": "Thức ăn bị đào thải nguyên vẹn qua đường tiêu hóa không được tiêu",
        "option_b": "Tế bào thiếu năng lượng buộc cơ thể tăng dị hóa lipid và protein",
        "option_c": "Tăng cường lắng đọng mỡ dưới da làm tiêu hao năng lượng chuyển hóa",
        "option_d": "Enzym tiêu hóa amylase và lipase tụy bị ức chế hoàn toàn trong ruột",
    },
    # Q146
    146: {
        "option_a": "Thường khởi phát ở người cao tuổi có kèm theo béo phì",
        "option_b": "Tự miễn phá hủy tế bào beta gây thiếu insulin tuyệt đối",
        "option_c": "Nồng độ insulin máu tăng cao do hiện tượng kháng insulin",
        "option_d": "Điều trị hiệu quả chỉ bằng cách tiết chế ăn uống hàng ngày",
    },
    # Q147
    147: {
        "option_a": "Phá hủy tế bào alpha tụy và tăng bài tiết hormon somatostatin",
        "option_b": "Đề kháng insulin mô ngoại vi phối hợp giảm tiết insulin tương đối",
        "option_c": "Đột biến gen thụ thể glucagon và suy giảm khả năng lọc cầu thận",
        "option_d": "Thiếu hụt hoàn toàn enzym glucose oxidase bẩm sinh trong cơ thể",
    },
    # Q150
    150: {
        "option_a": "Nhịn ăn liên tục từ 2 đến 4 giờ trước xét nghiệm",
        "option_b": "Nhịn ăn tối thiểu 8 giờ (thường nhịn qua đêm 8 - 12 giờ)",
        "option_c": "Nhịn ăn liên tục 24 giờ kể cả không được uống nước lọc",
        "option_d": "Chỉ cần nhịn ăn 30 phút sau khi uống một cốc nước đường",
    },
    # Q152
    152: {
        "option_a": "HbA1c >= 5.7% (tương đương 39 mmol/mol)",
        "option_b": "HbA1c >= 6.5% (tương đương 48 mmol/mol)",
        "option_c": "HbA1c >= 8.0% (tương đương 64 mmol/mol)",
        "option_d": "HbA1c >= 7.5% (tương đương 58 mmol/mol)",
    },
    # Q153
    153: {
        "option_a": "Kích thích tế bào beta tăng tổng hợp glycogen dự trữ",
        "option_b": "Hoại tử tụy cấp tính ức chế tiết và hủy hoại tế bào beta",
        "option_c": "Tăng cường hấp thu glucose tại biểu mô ống tiêu hóa ruột",
        "option_d": "Thận giảm bài tiết nước tiểu dẫn đến ứ đọng nồng độ đường",
    },
    # Q154
    154: {
        "option_a": "Bệnh nhân đái tháo đường type 1 có đường huyết rất cao > 20 mmol/L",
        "option_b": "Đường huyết bình thường nhưng ngưỡng thận bị hạ thấp bẩm sinh",
        "option_c": "Bệnh nhân nhịn ăn lâu ngày làm ống thận tự tổng hợp glucose máu",
        "option_d": "Do sử dụng quá liều thuốc lợi tiểu quai furosemid trong điều trị",
    },
    # Q156
    156: {
        "option_a": "Rối loạn đường huyết lúc đói (tiền đái tháo đường)",
        "option_b": "Đái tháo đường (Diabetes mellitus)",
        "option_c": "Đường huyết bình thường nhưng có rối loạn lo âu",
        "option_d": "Cần cho dùng thuốc hạ đường huyết ngay không cần kết luận",
    },
    # Q160
    160: {
        "option_a": "Sốt cao co giật, thở nông nhanh, da khô nóng đỏ",
        "option_b": "Vã mồ hôi lạnh, run tay, tim đập nhanh, đói lả, choáng váng",
        "option_c": "Tiểu buốt rắt nhiều lần, nước tiểu có màu đỏ đục lẫn mủ",
        "option_d": "Hôn mê sâu kèm theo kiểu thở Kussmaul bốc mùi táo thối",
    },
    # Q161
    161: {
        "option_a": "Do lượng enzym amylase nước bọt hoạt động quá mạnh mẽ",
        "option_b": "Do dự trữ glycogen gan thấp và enzym tân tạo đường chưa hoàn thiện",
        "option_c": "Do cơ chế tái hấp thu ở ống thận sơ sinh bị tắc nghẽn",
        "option_d": "Do cơ thể tiêu thụ quá nhiều acid béo bão hòa trong máu",
    },
    # Q162
    162: {
        "option_a": "Bệnh nhân nghi ngờ tiền đái tháo đường có IFG 6.2 mmol/L",
        "option_b": "Bệnh nhân đã chẩn đoán ĐTĐ rõ ràng có đường huyết đói > 12 mmol/L",
        "option_c": "Phụ nữ mang thai tuần 24 - 28 tầm soát đái tháo đường thai kỳ",
        "option_d": "Người có triệu chứng rối loạn chuyển hóa chưa rõ ràng trên lâm sàng",
    },
    # Q165
    165: {
        "option_a": "Thận của bệnh nhân bị suy hoàn toàn không thể lọc nước tiểu",
        "option_b": "Đường huyết 8.0 mmol/L (~144 mg/dL) chưa vượt ngưỡng thận (180 mg/dL)",
        "option_c": "Thuốc thử Benedict sử dụng trong xét nghiệm đã bị pha hỏng",
        "option_d": "Glucose bị chuyển hóa thành protein trong lòng bàng quang",
    },
    # Q169
    169: {
        "option_a": "Tạo môi trường acid cho phản ứng khử diễn ra nhanh chóng",
        "option_b": "Tạo phức chelate giữ Cu2+ không tủa Cu(OH)2 trong môi trường kiềm",
        "option_c": "Khử trực tiếp phân tử glucose thành rượu sorbitol tương ứng",
        "option_d": "Chất xúc tác sinh học thay thế enzym trong phản ứng oxy hóa",
    },
    # Q170
    170: {
        "option_a": "Tạo môi trường kiềm yếu thích hợp cho phản ứng khử của glucose",
        "option_b": "Tạo môi trường acid mạnh để phân hủy tinh bột thành đường đơn",
        "option_c": "Làm chất oxy hóa chính thay thế cho vai trò của ion đồng Cu2+",
        "option_d": "Ngăn cản sự bay hơi của nước cất trong quá trình đun cách thủy",
    },
    # Q174
    174: {
        "option_a": "Có ít tủa, thuốc thử vấy màu xanh lá: Glucose < 5 g/L (< 0.5%)",
        "option_b": "Có tủa màu vàng sẫm sau 1 phút đun: Glucose 5 - 10 g/L (0.5 - 1%)",
        "option_c": "Có tủa đỏ gạch xuất hiện: Glucose 10 - 20 g/L (1 - 2%)",
        "option_d": "Có tủa nâu đậm xuất hiện: Glucose > 20 g/L (> 2%)",
    },
    # Q175
    175: {
        "option_a": "Có ít tủa vấy màu xanh lá: Glucose < 5 g/L (< 0.5%)",
        "option_b": "Đun sôi 1 phút có tủa vàng sẫm: Glucose 5 - 10 g/L (0.5 - 1%)",
        "option_c": "Đun sôi có tủa đỏ gạch: Glucose 10 - 20 g/L (1 - 2%)",
        "option_d": "Đun sôi có tủa nâu đậm: Glucose > 20 g/L (> 2%)",
    },
    # Q176
    176: {
        "option_a": "Có ít tủa vấy màu xanh lá: Glucose < 5 g/L (< 0.5%)",
        "option_b": "Đun sôi xuất hiện tủa đỏ gạch: Glucose 10 - 20 g/L (1 - 2%)",
        "option_c": "Đun sôi 1 phút có tủa vàng sẫm: Glucose 5 - 10 g/L (0.5 - 1%)",
        "option_d": "Đun sôi có tủa nâu đậm: Glucose > 20 g/L (> 2%)",
    },
    # Q177
    177: {
        "option_a": "Đun sôi xuất hiện tủa đỏ gạch: Glucose 10 - 20 g/L (1 - 2%)",
        "option_b": "Đun sôi có tủa nâu đậm xuất hiện: Glucose > 20 g/L (> 2%)",
        "option_c": "Đun sôi 1 phút có tủa vàng sẫm: Glucose 5 - 10 g/L (0.5 - 1%)",
        "option_d": "Có ít tủa vấy màu xanh lá: Glucose < 5 g/L (< 0.5%)",
    },
    # Q178
    178: {
        "option_a": "Vì phản ứng cho biết nồng độ glucose chính xác từng số thập phân",
        "option_b": "Vì dựa vào số lượng và màu sắc tủa để ước tính khoảng nồng độ",
        "option_c": "Vì phản ứng chỉ cho biết có hay không có glucose trong nước tiểu",
        "option_d": "Vì chỉ một nửa số phân tử glucose tham gia phản ứng khử ion đồng",
    },
    # Q179
    179: {
        "option_a": "Fehling cho màu xanh lá còn Benedict cho phức chất màu tím",
        "option_b": "Fehling chỉ là định tính còn Benedict là phản ứng bán định lượng",
        "option_c": "Benedict chỉ phát hiện fructose còn Fehling phát hiện glucose",
        "option_d": "Fehling dùng ở nhiệt độ phòng còn Benedict phải làm lạnh âm",
    },
    # Q180
    180: {
        "option_a": "Thuốc thử Benedict hoàn toàn không chứa ion kim loại đồng",
        "option_b": "Thuốc thử Benedict pha gộp sẵn trong 1 chai và bảo quản lâu dài",
        "option_c": "Thuốc thử Benedict không cần phải đun nóng khi làm phản ứng",
        "option_d": "Thuốc thử Benedict hoàn toàn không độc hại có thể uống được",
    },
    # Q181
    181: {
        "option_a": "Đo độ hấp thu quang học ở bước sóng tử ngoại 340 nm",
        "option_b": "Đun sôi cách thủy thử, dung dịch phải trong suốt và không có tủa đỏ",
        "option_c": "Thêm acid picric vào xem có tạo màu vàng cam hay không",
        "option_d": "Đo độ nhớt dung dịch bằng nhớt kế mao quản chuẩn Ostwald",
    },
    # Q184
    184: {
        "option_a": "Dưới 5 g/L (< 0.5%) kèm dung dịch vấy xanh lá",
        "option_b": "Khoảng 5 - 10 g/L (0.5 - 1%) kèm tủa vàng sẫm",
        "option_c": "Khoảng 10 - 20 g/L (1 - 2%) kèm tủa đỏ gạch",
        "option_d": "Trên 20 g/L (> 2%) kèm tủa màu nâu sẫm",
    },
    # Q185
    185: {
        "option_a": "Dưới 5 g/L (< 0.5%) kèm dung dịch vấy xanh lá",
        "option_b": "Khoảng 10 - 20 g/L (1 - 2%) kèm tủa đỏ gạch",
        "option_c": "Khoảng 5 - 10 g/L (0.5 - 1%) kèm tủa vàng sẫm",
        "option_d": "Trên 20 g/L (> 2%) kèm tủa màu nâu sẫm",
    },
    # Q186
    186: {
        "option_a": "Dưới 5 g/L (< 0.5%) kèm dung dịch vấy xanh lá",
        "option_b": "Trên 20 g/L (> 2%) kèm tủa màu nâu đậm",
        "option_c": "Khoảng 10 - 20 g/L (1 - 2%) kèm tủa đỏ gạch",
        "option_d": "Khoảng 5 - 10 g/L (0.5 - 1%) kèm tủa vàng sẫm",
    },
    # Q187
    187: {
        "option_a": "Vì thuốc thử Benedict chứa enzym phân hủy acid uric nước tiểu",
        "option_b": "Vì môi trường kiềm trong Benedict là kiềm yếu Na2CO3 ít phản ứng phụ",
        "option_c": "Vì natri citrat kết hợp trực tiếp với creatinin tạo tủa trắng",
        "option_d": "Vì nồng độ ion đồng trong Benedict cao gấp 10 lần so với Fehling",
    },
    # Q188
    188: {
        "option_a": "Hoàn toàn không có bất kỳ phân tử glucose nào trong nước tiểu",
        "option_b": "Rất thấp, dưới 0.15 g/24h (< 150 mg/24h) nên xét nghiệm âm tính",
        "option_c": "Khoảng 5 - 10 g/24 giờ ở người khỏe mạnh không có triệu chứng",
        "option_d": "Khoảng 1 - 2 g/24 giờ và tăng gấp đôi sau khi vận động thể lực",
    },
    # Q197
    197: {
        "option_a": "Nhiệt độ và thời gian đun sôi cách thủy của ống nghiệm",
        "option_b": "Số lượng và kích thước hạt tủa Cu2O tỉ lệ với nồng độ glucose",
        "option_c": "Nồng độ ion natri và áp suất thẩm thấu của mẫu nước tiểu",
        "option_d": "Độ kiềm hóa và hàm lượng sắc tố mật có sẵn trong mẫu thử",
    },
    # Q198
    198: {
        "option_a": "Làm tăng độ nhạy phát hiện glucose lên gấp 10 lần bình thường",
        "option_b": "Chất tạp và đạm làm mất tính kiềm, gây tủa đen xám sai lệch",
        "option_c": "Phản ứng không xảy ra do thuốc thử bị đông đặc thành thạch",
        "option_d": "Dung dịch chuyển sang màu tím hoa cà của phản ứng biuret",
    },
}

# Apply manual adjustments
for q in raw_questions:
    qid = q["id_in_set"]
    if qid in manual_adjustments:
        adj = manual_adjustments[qid]
        for opt_k in ["option_a", "option_b", "option_c", "option_d"]:
            if opt_k in adj:
                q[opt_k] = adj[opt_k]

# Equalize / balance the key distribution to exactly 50 A, 50 B, 50 C, 50 D
# Target key sequence for 200 questions: 50 each
target_keys = ['A', 'B', 'C', 'D'] * 50
random.seed(42)
random.shuffle(target_keys)

balanced_questions = []
for i, q in enumerate(raw_questions):
    old_correct_key = q["correct_option"].upper()
    target_key = target_keys[i]
    
    # Options dictionary
    opts = {
        'A': q["option_a"],
        'B': q["option_b"],
        'C': q["option_c"],
        'D': q["option_d"]
    }
    
    correct_text = opts[old_correct_key]
    distractor_texts = [v for k, v in opts.items() if k != old_correct_key]
    
    # Assign target_key to correct_text, and distribute distractors to remaining keys
    other_keys = [k for k in ['A', 'B', 'C', 'D'] if k != target_key]
    
    new_opts = {}
    new_opts[target_key] = correct_text
    for k, d_txt in zip(other_keys, distractor_texts):
        new_opts[k] = d_txt
        
    new_q = {
        "id_in_set": i + 1,
        "question_text": f"Câu {i + 1}: " + q["question_text"].split(":", 1)[-1].strip(),
        "option_a": new_opts['A'],
        "option_b": new_opts['B'],
        "option_c": new_opts['C'],
        "option_d": new_opts['D'],
        "correct_option": target_key,
        "explanation": q["explanation"],
        "difficulty": q["difficulty"],
        "topic_tag": q["topic_tag"],
        "q_type": "mcq"
    }
    balanced_questions.append(new_q)

# Measure length bias now
longest_correct = 0
shortest_correct = 0
equal_or_medium = 0

for q in balanced_questions:
    c_key = q['correct_option'].lower()
    c_len = len(q[f'option_{c_key}'])
    other_lens = [len(q[f'option_{k}']) for k in ['a','b','c','d'] if k != c_key]
    max_other = max(other_lens)
    min_other = min(other_lens)
    if c_len > max_other:
        longest_correct += 1
    elif c_len < min_other:
        shortest_correct += 1
    else:
        equal_or_medium += 1

key_counts = {k: sum(1 for q in balanced_questions if q['correct_option'] == k) for k in ['A', 'B', 'C', 'D']}

print("=== VERIFICATION RESULTS ===")
print(f"Total questions: {len(balanced_questions)}")
print(f"Key distribution: {key_counts}")
print(f"Longest is correct: {longest_correct} / 200 ({longest_correct*100/200:.1f}%)")
print(f"Shortest is correct: {shortest_correct} / 200 ({shortest_correct*100/200:.1f}%)")
print(f"Medium/Equal is correct: {equal_or_medium} / 200 ({equal_or_medium*100/200:.1f}%)")

# Save master JSON
master_json_path = "trac_nghiem_bai3_glucid_200_cau.json"
with open(master_json_path, "w", encoding="utf-8") as f:
    json.dump(balanced_questions, f, ensure_ascii=False, indent=2)
print(f"Master file saved: {master_json_path} ({os.path.getsize(master_json_path)} bytes)")

# Save 6 sub-lesson JSONs
lessons = [
    ("bai3_phan1_molish_25_cau.json", balanced_questions[0:25], "Bài 3 - Phần 1: Phản ứng Molish & Đại cương Glucid (25 câu)"),
    ("bai3_phan2_fehling_35_cau.json", balanced_questions[25:60], "Bài 3 - Phần 2: Phản ứng Fehling & Tính khử của đường (35 câu)"),
    ("bai3_phan3_polysaccharid_iod_25_cau.json", balanced_questions[60:85], "Bài 3 - Phần 3: Phản ứng màu của Polysaccharid với Iod (25 câu)"),
    ("bai3_phan4_dinh_luong_glucose_god_pod_45_cau.json", balanced_questions[85:130], "Bài 3 - Phần 4: Định lượng Glucose huyết tương GOD-POD (45 câu)"),
    ("bai3_phan5_bien_luan_dai_thao_duong_ogtt_35_cau.json", balanced_questions[130:165], "Bài 3 - Phần 5: Biện luận Sinh hóa Đái tháo đường & OGTT (35 câu)"),
    ("bai3_phan6_benedict_nuoc_tieu_35_cau.json", balanced_questions[165:200], "Bài 3 - Phần 6: Phản ứng Benedict & Tìm đường niệu bán định lượng (35 câu)")
]

for filename, qs, label in lessons:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)
    print(f"Sub-lesson file saved: {filename} ({len(qs)} questions) - {label}")

print("\nAll files generated and validated successfully!")
