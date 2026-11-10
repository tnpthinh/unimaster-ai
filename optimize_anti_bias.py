# -*- coding: utf-8 -*-
"""
Anti-bias length optimizer:
Ensures correct option is NOT systematically the longest.
Target: < 22% of questions have correct option as the strictly longest.
Key distribution: Exactly 50 A, 50 B, 50 C, 50 D (25% each).
"""

import json
import re

with open("trac_nghiem_bai3_glucid_200_cau.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Specific refinements to equalize option lengths across the 99 biased questions
replacements = {
    # Q25
    25: {
        "correct_sub": ("Lắc đều để thuốc thử phân tán đồng nhất trong dung dịch glucid", "Lắc đều để thuốc thử phân tán đều vào dung dịch"),
        "distractors_add": {
            "Đun sôi cách thủy trong 3 phút": "Đun sôi cách thủy ống nghiệm trong 3 phút",
            "Làm lạnh ống nghiệm trong nước đá 5 phút": "Làm lạnh ống nghiệm trong nước đá 5 phút liên tục"
        }
    },
    # Q47
    47: {
        "correct_sub": ("Sự đứt gãy mạch carbon tại vị trí nối đôi của dạng trung gian enediol", "Sự đứt gãy mạch carbon tại nối đôi của enediol"),
        "distractors_add": {
            "Khử nước hoàn toàn của phân tử hexose": "Khử nước hoàn toàn phân tử hexose tạo dẫn xuất furfural",
            "Sự ngưng tụ giữa monosaccharid và alpha-naphtol": "Sự ngưng tụ giữa monosaccharid và alpha-naphtol trong acid",
            "Sự trùng hợp của các gốc glucose thành glycogen": "Sự trùng hợp các gốc glucose tạo mạch đại phân tử glycogen"
        }
    },
    # Q52
    52: {
        "correct_sub": ("Tìm đường trong nước tiểu bệnh nhân nghi ngờ đái tháo đường", "Tìm đường trong nước tiểu người nghi đái tháo đường"),
        "distractors_add": {
            "Định lượng nồng độ cholesterol máu": "Định lượng nồng độ cholesterol toàn phần trong máu",
            "Đo hoạt độ enzym amylase dịch vị": "Đo hoạt lực enzym amylase trong mẫu dịch tiêu hóa",
            "Xác định nồng độ bilirubin toàn phần": "Xác định nồng độ sắc tố mật bilirubin toàn phần"
        }
    },
    # Q53
    53: {
        "correct_sub": ("Chỉ làm mất nhẹ màu xanh hoặc dung dịch chuyển màu xanh ngả vàng đục không rõ tủa", "Dung dịch chuyển sang màu xanh ngả vàng đục không rõ tủa"),
        "distractors_add": {
            "Vẫn cho tủa đỏ gạch dày đặc ở đáy ống": "Vẫn xuất hiện kết tủa đỏ gạch dày đặc ở đáy ống",
            "Dung dịch bùng cháy sủi bọt trắng": "Dung dịch sủi nhiều bọt khí trắng và sôi trào",
            "Lập tức xuất hiện vòng nhẫn màu tím": "Lập tức xuất hiện vòng nhẫn màu tím đậm ở ranh giới"
        }
    },
    # Q54
    54: {
        "correct_sub": ("Khử ion Cu2+ (màu xanh) thành ion Cu+ trong kết tủa Cu2O (đỏ gạch)", "Khử ion Cu2+ màu xanh thành ion Cu+ trong Cu2O"),
        "distractors_add": {
            "Oxy hóa Cu+ thành Cu2+": "Oxy hóa ion Cu+ thành Cu2+ trong môi trường kiềm",
            "Khử gốc sulfat SO4 2- thành khí SO2": "Khử ion sulfate SO4 2- tạo thành khí SO2 bay lên",
            "Oxy hóa muối tartrat thành khí CO2": "Oxy hóa hoàn toàn muối tartrat giải phóng khí CO2"
        }
    },
    # Q79
    79: {
        "correct_sub": ("Màu xanh lập tức biến mất do kiềm phản ứng với iod tạo thành iodua và iodat không màu", "Màu xanh biến mất do kiềm phản ứng với iod tạo iodua"),
        "distractors_add": {
            "Màu xanh chuyển thành màu đỏ gạch do khử kiềm": "Màu xanh chuyển sang đỏ gạch do phản ứng khử kiềm",
            "Màu xanh đậm hơn gấp đôi và không bị mất màu khi đun": "Màu xanh đậm lên gấp đôi và hoàn toàn không mất khi đun",
            "Dung dịch bốc cháy sinh ra khói màu tím": "Dung dịch sủi bọt mạnh và sinh ra làn khói màu tím"
        }
    },
    # Q80
    80: {
        "correct_sub": ("Không xuất hiện màu xanh dương (chỉ có màu vàng của dung dịch Lugol)", "Không xuất hiện màu xanh, chỉ có màu vàng của Lugol"),
        "distractors_add": {
            "Xuất hiện màu xanh dương rực rỡ như tinh bột": "Xuất hiện màu xanh dương rực rỡ tương tự như tinh bột",
            "Xuất hiện kết tủa màu đỏ nâu": "Xuất hiện kết tủa màu đỏ nâu lắng dần xuống đáy",
            "Xuất hiện phức chất màu tím hoa cà": "Xuất hiện phức chất màu tím hoa cà bền vững trong ống"
        }
    },
    # Q127
    127: {
        "correct_sub": ("Lượng enzym chuyển hóa 1 micromol cơ chất trong 1 phút ở điều kiện tiêu chuẩn", "Lượng enzym chuyển hóa 1 micromol cơ chất trong 1 phút"),
        "distractors_add": {
            "Lượng gam enzym hòa tan trong 1 lít dung dịch": "Lượng gam protein enzym hòa tan trong 1 lít dung dịch",
            "Số phân tử enzym có trong 1 mililit dung dịch": "Số lượng phân tử enzym hiện diện trong 1 ml dung dịch",
            "Khối lượng cơ chất bị phân hủy trong 1 giờ": "Khối lượng cơ chất bị xúc tác phân hủy trong 1 giờ"
        }
    },
    # Q148
    148: {
        "correct_sub": ("Rối loạn đường huyết lúc đói (Impaired Fasting Glucose - IFG, tiền đái tháo đường)", "Rối loạn đường huyết lúc đói (tiền đái tháo đường)"),
        "distractors_add": {
            "Đái tháo đường type 1 thể nhẹ": "Đái tháo đường type 1 giai đoạn tiềm ẩn thể nhẹ",
            "Đường huyết hoàn toàn bình thường không cần theo dõi": "Đường huyết hoàn toàn bình thường không cần theo dõi thêm",
            "Hạ đường huyết cận lâm sàng": "Hạ đường huyết cận lâm sàng sau bữa ăn nhẹ"
        }
    },
    # Q166
    166: {
        "correct_sub": ("Trong môi trường kiềm đun nóng, glucose trong nước tiểu khử Cu2+ thành Cu+ tạo kết tủa Cu2O màu đỏ gạch", "Glucose khử Cu2+ thành Cu+ tạo kết tủa Cu2O đỏ gạch"),
        "distractors_add": {
            "Glucose bị oxy hóa bởi enzym peroxidase tạo phức hợp màu đỏ hồng": "Glucose bị oxy hóa bởi enzym peroxidase tạo phức màu đỏ hồng",
            "Glucose phản ứng ngưng tụ với alpha-naphtol tạo vòng màu tím ở ranh giới": "Glucose ngưng tụ với alpha-naphtol tạo vòng tím ở ranh giới hai lớp chất lỏng",
            "Glucose kết hợp trực tiếp với natri citrat tạo phức chelate màu vàng": "Glucose kết hợp trực tiếp với natri citrat tạo phức chelate màu vàng cam"
        }
    },
    # Q167
    167: {
        "correct_sub": ("Natri Citrat 173g, Na2CO3 200g và nước cất đun nóng vừa đủ 1000ml", "Natri Citrat 173g, Na2CO3 200g, nước cất vđ 1000ml"),
        "distractors_add": {
            "CuSO4 kết tinh 35g và acid sulfuric 5ml": "CuSO4 kết tinh 35g, acid sulfuric đđ 5ml, nước cất vđ 1000ml",
            "NaOH 135g và Natri Kali Tartrat 150g": "NaOH 135g, Natri Kali Tartrat 150g, nước cất vđ 1000ml",
            "Iod tinh thể 0.1g và KI 0.2g": "Iod tinh thể 0.1g, Kali Iodid 0.2g, nước cất vđ 1000ml"
        }
    },
    # Q190
    190: {
        "correct_sub": ("Galactose (ở trẻ mắc bệnh galactosemia bẩm sinh)", "Galactose (đường đơn có trong sữa)"),
        "distractors_add": {
            "Albumin": "Albumin huyết thanh người",
            "Ure": "Ure nội sinh trong nước tiểu",
            "Thể ceton acetoacetat": "Thể ceton acetoacetat hòa tan"
        }
    },
    # Q192
    192: {
        "correct_sub": ("Bệnh nhân dùng kháng sinh nhóm cephalosporin hoặc vitamin C liều rất cao", "Dùng kháng sinh cephalosporin hoặc vitamin C liều cao"),
        "distractors_add": {
            "Bệnh nhân uống nhiều nước lọc làm nước tiểu trong": "Bệnh nhân uống quá nhiều nước lọc làm loãng mẫu nước tiểu",
            "Nước tiểu có nhiều bạch cầu do nhiễm trùng tiểu": "Nước tiểu có nhiều bạch cầu thoái hóa do nhiễm khuẩn niệu",
            "Nước tiểu để lâu bị kiềm hóa": "Mẫu nước tiểu để quá lâu bị kiềm hóa bởi vi khuẩn phân hủy"
        }
    },
    # Q194
    194: {
        "correct_sub": ("Phản ứng enzyme đặc hiệu Glucose oxydase - Peroxidase trên vùng thử", "Phản ứng enzym kép Glucose oxidase - Peroxidase"),
        "distractors_add": {
            "Phản ứng Fehling với ion đồng": "Phản ứng khử Cu2+ với thuốc thử Fehling kiềm",
            "Phản ứng Molish với alpha-naphtol": "Phản ứng tạo vòng màu tím với thuốc thử Molish",
            "Phản ứng tạo phức màu với thuốc thử Lugol": "Phản ứng hấp phụ tạo màu với thuốc thử Lugol 0.1%"
        }
    },
    # Q200
    200: {
        "correct_sub": ("Định lượng Glucose trong huyết tương (GOD-POD) và Tìm Glucose trong nước tiểu (Benedict)", "Định lượng Glucose huyết tương và Tìm Glucose nước tiểu"),
        "distractors_add": {
            "Phản ứng Molish và phản ứng màu của Polysaccharid với Iod": "Phản ứng Molish với alpha-naphtol và Phản ứng màu Polysaccharid với Iod",
            "Phản ứng Fehling và phản ứng Molish": "Phản ứng tạo tủa đỏ Fehling và Phản ứng tạo vòng tím Molish",
            "Phản ứng màu Polysaccharid và phản ứng Fehling": "Phản ứng màu tinh bột với Iod và Phản ứng khử Fehling trong kiềm"
        }
    }
}

for qid, data in replacements.items():
    idx = qid - 1
    q = questions[idx]
    ck = q["correct_option"].lower()
    correct_opt_key = f"option_{ck}"
    
    # Substitute correct
    old_c, new_c = data["correct_sub"]
    if q[correct_opt_key] == old_c or old_c in q[correct_opt_key]:
        q[correct_opt_key] = new_c
        
    # Substitute distractors
    for dk in ['a', 'b', 'c', 'd']:
        if dk != ck:
            opt_key = f"option_{dk}"
            cur_val = q[opt_key]
            if cur_val in data.get("distractors_add", {}):
                q[opt_key] = data["distractors_add"][cur_val]

# General programmatic balancer for remaining questions where correct is strictly longest
for q in questions:
    ck = q['correct_option'].lower()
    c_val = q[f'option_{ck}']
    other_keys = [k for k in ['a','b','c','d'] if k != ck]
    other_lens = [len(q[f'option_{k}']) for k in other_keys]
    max_o = max(other_lens)
    
    # If correct is longer than max by more than 10 characters
    if len(c_val) > max_o + 10:
        # Check if correct has parenthetical notes that can be cleaned
        if " (" in c_val and ")" in c_val:
            # Check length without parenthetical
            cleaned = re.sub(r'\s*\([^)]*\)', '', c_val).strip()
            if len(cleaned) >= min(other_lens) - 5:
                q[f'option_{ck}'] = cleaned

# Recalculate
longest_count = 0
shortest_count = 0
equal_or_med_count = 0

for q in questions:
    ck = q['correct_option'].lower()
    c_len = len(q[f'option_{ck}'])
    other_lens = [len(q[f'option_{k}']) for k in ['a','b','c','d'] if k != ck]
    max_o = max(other_lens)
    min_o = min(other_lens)
    if c_len > max_o:
        longest_count += 1
    elif c_len < min_o:
        shortest_count += 1
    else:
        equal_or_med_count += 1

print(f"After optimization:")
print(f"  Longest is correct: {longest_count} / 200 ({longest_count*100/200:.1f}%)")
print(f"  Shortest is correct: {shortest_count} / 200 ({shortest_count*100/200:.1f}%)")
print(f"  Equal/Medium is correct: {equal_or_med_count} / 200 ({equal_or_med_count*100/200:.1f}%)")

# Overwrite master JSON
with open("trac_nghiem_bai3_glucid_200_cau.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

# Update the 6 sub-lesson JSONs
lessons = [
    ("bai3_phan1_molish_25_cau.json", questions[0:25]),
    ("bai3_phan2_fehling_35_cau.json", questions[25:60]),
    ("bai3_phan3_polysaccharid_iod_25_cau.json", questions[60:85]),
    ("bai3_phan4_dinh_luong_glucose_god_pod_45_cau.json", questions[85:130]),
    ("bai3_phan5_bien_luan_dai_thao_duong_ogtt_35_cau.json", questions[130:165]),
    ("bai3_phan6_benedict_nuoc_tieu_35_cau.json", questions[165:200])
]

for filename, qs in lessons:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)

print("Saved updated master and sub-lesson JSONs!")
