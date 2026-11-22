# -*- coding: utf-8 -*-
"""
UniMaster AI Pro v11.0 — Advanced University & Medical Capabilities Extension:
1. Virtual Patient / Multi-Step Clinical Case Simulator (Hỏi bệnh -> Khám -> Cận lâm sàng -> Chẩn đoán -> Điều trị)
2. Real-Time Multiplayer Quiz Arena via WebSocket (Chủ phòng + Người chơi thời gian thực)
3. Clinical Pharmacology & Renal Dose Adjustment Calculator (eGFR, CrCl, Tương tác thuốc)
4. Biostatistics & Medical Research Lab (2x2 Table, Odds Ratio, Sens/Spec, Chi-square, t-test, Trích dẫn Vancouver)
5. 1-Click Anki (.txt / TSV) & Printable A4 Exam Word (.doc) Exporter
"""

import os
import re
import json
import math
import time
import asyncio
from aiohttp import web, WSMsgType
import database as db
import ai_service as ai

# In-memory Real-time Arena Rooms: { room_code: { host_ws, players: { pid: { name, score, ws } }, questions: [], q_idx: 0, state: 'waiting' } }
ARENA_ROOMS = {}

# Clinical Drug Database with Renal Adjustments (Dược Lý Lâm Sàng & Hiệu Chỉnh Liều Thận)
DRUG_DATABASE = [
    {
        "id": "vancomycin",
        "name": "Vancomycin",
        "group": "Kháng sinh Glycopeptid",
        "indication": "Nhiễm khuẩn tụ cầu vàng kháng methicillin (MRSA), viêm nội tâm mạc, viêm phổi bệnh viện",
        "std_dose": "15 – 20 mg/kg mỗi 8 – 12 giờ (truyền tĩnh mạch chậm)",
        "crcl_normal": "CrCl ≥ 50 ml/phút: 100% liều tiêu chuẩn (15 mg/kg mỗi 12 giờ)",
        "crcl_mod": "CrCl 20 – 49 ml/phút: 15 mg/kg mỗi 24 – 48 giờ",
        "crcl_severe": "CrCl < 20 ml/phút: 15 mg/kg liều nạp, sau đó theo dõi nồng độ đáy (TDM Cmin: 15 – 20 mcg/ml)",
        "hd_dose": "Lọc máu chu kỳ: Liều nạp 15 – 25 mg/kg, bổ sung 500 – 1000 mg sau mỗi lần lọc máu",
        "warning": "Độc tính cao trên tai và thận! Tuyệt đối không truyền nhanh (< 60 phút) vì nguy cơ 'Hội chứng người đỏ' (Red Man Syndrome)."
    },
    {
        "id": "ciprofloxacin",
        "name": "Ciprofloxacin",
        "group": "Kháng sinh Fluoroquinolon",
        "indication": "Nhiễm khuẩn tiết niệu có biến chứng, viêm tuyến tiền liệt, nhiễm khuẩn tiêu hóa",
        "std_dose": "500 – 750 mg uống mỗi 12 giờ (hoặc 400 mg IV mỗi 12 giờ)",
        "crcl_normal": "CrCl ≥ 50 ml/phút: 100% liều (500 – 750 mg mỗi 12 giờ)",
        "crcl_mod": "CrCl 30 – 49 ml/phút: 250 – 500 mg mỗi 12 giờ",
        "crcl_severe": "CrCl < 30 ml/phút: 250 – 500 mg mỗi 18 – 24 giờ",
        "hd_dose": "Thẩm phân phúc mạc / HD: 250 – 500 mg mỗi 24 giờ sau lọc",
        "warning": "Nguy cơ viêm/đứt gân gót Achilles, kéo dài khoảng QT tim mạch và độc thần kinh ở người già."
    },
    {
        "id": "meropenem",
        "name": "Meropenem",
        "group": "Kháng sinh Carbapenem",
        "indication": "Nhiễm khuẩn nặng đa kháng, nhiễm khuẩn ổ bụng, viêm màng não, sốc nhiễm khuẩn",
        "std_dose": "1000 mg IV mỗi 8 giờ (viêm màng não: 2000 mg mỗi 8 giờ)",
        "crcl_normal": "CrCl ≥ 50 ml/phút: 1000 mg mỗi 8 giờ",
        "crcl_mod": "CrCl 26 – 49 ml/phút: 1000 mg mỗi 12 giờ",
        "crcl_severe": "CrCl 10 – 25 ml/phút: 500 mg mỗi 12 giờ; CrCl < 10 ml/phút: 500 mg mỗi 24 giờ",
        "hd_dose": "Lọc máu: 500 mg mỗi 24 giờ, cho thêm 1 liều sau lọc máu",
        "warning": "Thận trọng nguy cơ co giật khi dùng liều cao trên bệnh nhân tổn thương thần kinh trung ương."
    },
    {
        "id": "gentamicin",
        "name": "Gentamicin",
        "group": "Kháng sinh Aminoglycosid",
        "indication": "Nhiễm khuẩn huyết Gram âm phối hợp, viêm đài bể thận cấp",
        "std_dose": "5 – 7 mg/kg tiêm truyền tĩnh mạch 1 lần/ngày (Hartford nomogram)",
        "crcl_normal": "CrCl ≥ 60 ml/phút: Mỗi 24 giờ 1 lần",
        "crcl_mod": "CrCl 40 – 59 ml/phút: Kéo dài khoảng cách mỗi 36 giờ; CrCl 20 – 39 ml/phút: Mỗi 48 giờ",
        "crcl_severe": "CrCl < 20 ml/phút: Liều nạp 2 mg/kg, sau đó chỉ dùng tiếp khi nồng độ đỉnh/đáy đạt mục tiêu TDM",
        "hd_dose": "Sau lọc máu: Bổ sung 1 – 1,5 mg/kg sau mỗi buổi lọc",
        "warning": "Độc tính không hồi phục trên tiền đình - ốc tai và hoại tử ống thận cấp! Bắt buộc theo dõi chức năng thận."
    },
    {
        "id": "allopurinol",
        "name": "Allopurinol",
        "group": "Thuốc ức chế Xanthine Oxidase hạ Acid Uric",
        "indication": "Bệnh Gout mạn tính, sỏi thận acid uric, phòng ngừa hội chứng ly giải u",
        "std_dose": "100 – 300 mg/ngày uống sau ăn (khởi đầu 100 mg/ngày)",
        "crcl_normal": "CrCl ≥ 50 ml/phút: 200 – 300 mg/ngày",
        "crcl_mod": "CrCl 20 – 49 ml/phút: 100 – 200 mg/ngày",
        "crcl_severe": "CrCl 10 – 19 ml/phút: 100 mg/ngày; CrCl < 10 ml/phút: 100 mg mỗi 2 – 3 ngày",
        "hd_dose": "Sau lọc máu: 50 – 100 mg sau mỗi lần lọc máu",
        "warning": "Nguy cơ hội chứng quá mẫn nghiêm trọng (Stevens-Johnson / TEN, DRESS) đặc biệt ở bệnh nhân mang gen HLA-B*5801."
    },
    {
        "id": "enalapril",
        "name": "Enalapril",
        "group": "Thuốc ức chế men chuyển (ACEi)",
        "indication": "Tăng huyết áp, suy tim, bệnh thận đái tháo đường có tiểu đạm",
        "std_dose": "5 – 20 mg/ngày uống 1 – 2 lần",
        "crcl_normal": "CrCl ≥ 30 ml/phút: Khởi đầu 5 mg/ngày, duy trì 10 – 20 mg/ngày",
        "crcl_mod": "CrCl 10 – 29 ml/phút: Khởi đầu 2,5 mg/ngày, tối đa 10 mg/ngày",
        "crcl_severe": "CrCl < 10 ml/phút: Khởi đầu 2,5 mg vào những ngày không lọc máu",
        "hd_dose": "Lọc máu: Có thể thẩm phân được, dùng sau buổi lọc máu",
        "warning": "Theo dõi sát Kali máu và Creatinin máu sau 1 – 2 tuần khởi trị. Chống chỉ định trong hẹp động mạch thận hai bên và thai kỳ!"
    },
    {
        "id": "metformin",
        "name": "Metformin",
        "group": "Thuốc hạ đường huyết Biguanide",
        "indication": "Đái tháo đường týp 2 hàng đầu (First-line)",
        "std_dose": "500 – 2000 mg/ngày chia 2 lần uống cùng bữa ăn",
        "crcl_normal": "eGFR ≥ 60 ml/phút/1.73m²: Liều tối đa 2000 mg/ngày",
        "crcl_mod": "eGFR 45 – 59: Tối đa 1500 mg/ngày; eGFR 30 – 44: Tối đa 1000 mg/ngày (không khởi trị mới)",
        "crcl_severe": "eGFR < 30 ml/phút/1.73m²: CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI!",
        "hd_dose": "Chống chỉ định tuyệt đối ở bệnh nhân lọc máu chu kỳ",
        "warning": "Nguy cơ nhiễm toan Lactic máu (Lactic Acidosis) đe dọa tính mạng khi dùng ở bệnh nhân suy thận nặng hoặc thiếu oxy mô."
    },
    {
        "id": "levofloxacin",
        "name": "Levofloxacin",
        "group": "Kháng sinh Fluoroquinolon hô hấp",
        "indication": "Viêm phổi mắc phải cộng đồng (CAP), đợt cấp COPD, nhiễm khuẩn tiết niệu phức tạp",
        "std_dose": "500 – 750 mg uống hoặc IV mỗi 24 giờ",
        "crcl_normal": "CrCl ≥ 50 ml/phút: 500 – 750 mg mỗi 24 giờ",
        "crcl_mod": "CrCl 20 – 49 ml/phút: Liều nạp 750 mg, sau đó 750 mg mỗi 48 giờ (hoặc nạp 500 mg, duy trì 250 mg mỗi 24 giờ)",
        "crcl_severe": "CrCl < 20 ml/phút: Liều nạp 750 mg, sau đó 500 mg mỗi 48 giờ (hoặc nạp 500 mg, duy trì 250 mg mỗi 48 giờ)",
        "hd_dose": "Lọc máu / CAPD: Liều như CrCl < 20 ml/phút, không cần bổ sung liều sau lọc máu",
        "warning": "Nguy cơ kéo dài khoảng QT, xoắn đỉnh, viêm gân gót Achilles và rối loạn đường huyết ở bệnh nhân đái tháo đường."
    },
    {
        "id": "ceftriaxone",
        "name": "Ceftriaxone",
        "group": "Kháng sinh Cephalosporin thế hệ 3",
        "indication": "Viêm màng não mủ, viêm phổi, nhiễm khuẩn huyết, lậu cầu, thương hàn",
        "std_dose": "1 – 2 g IV/IM mỗi 24 giờ (viêm màng não: 2 g mỗi 12 giờ)",
        "crcl_normal": "CrCl ≥ 50 ml/phút: 1 – 2 g mỗi 24 giờ (thải trừ kép qua cả mật và thận)",
        "crcl_mod": "CrCl 10 – 49 ml/phút: Không cần chỉnh liều chuẩn (tối đa 2 g/ngày nếu suy cả gan và thận)",
        "crcl_severe": "CrCl < 10 ml/phút: Không vượt quá 2 g/24 giờ",
        "hd_dose": "Lọc máu: Không thẩm phân qua màng lọc, không cần bổ sung liều sau HD",
        "warning": "TUYỆT ĐỐI KHÔNG pha chung hoặc truyền cùng đường truyền chứa Calcium (Ringer Lactate, Calcium gluconate) đặc biệt ở trẻ sơ sinh do kết tủa Ceftriaxone-Calci tại phổi và thận!"
    },
    {
        "id": "digoxin",
        "name": "Digoxin",
        "group": "Glycosid trợ tim",
        "indication": "Suy tim phân suất tống máu giảm (HFrEF), kiểm soát tần số thất trong rung nhĩ",
        "std_dose": "0,125 – 0,25 mg/ngày uống 1 lần",
        "crcl_normal": "CrCl ≥ 50 ml/phút: 0,125 – 0,25 mg mỗi 24 giờ",
        "crcl_mod": "CrCl 10 – 49 ml/phút: 0,0625 – 0,125 mg mỗi 24 giờ (hoặc 0,125 mg cách ngày)",
        "crcl_severe": "CrCl < 10 ml/phút: 0,0625 mg mỗi 48 giờ; theo dõi nồng độ thuốc trong máu (0,5 – 0,9 ng/mL)",
        "hd_dose": "Lọc máu: Không bị loại bỏ qua lọc máu, dùng 0,0625 mg mỗi 48 giờ",
        "warning": "Cửa sổ điều trị cực hẹp! Hạ Kali máu, hạ Magie máu hoặc tăng Calci máu làm tăng mạnh nguy cơ ngộ độc Digoxin (loạn nhịp thất, nhìn mờ sắc vàng-xanh)."
    }
]

# Clinical Case Scenarios for Virtual Patient Simulator (5-Step Clinical Decision Schema)
VIRTUAL_CASES = [
    {
        "id": "case_nephrotic_01",
        "title": "Ca 1: Hội chứng thận hư nguyên phát ở người trưởng thành",
        "patient": {
            "name": "Nguyễn Văn H.",
            "age": 45,
            "gender": "Nam",
            "chief_complaint": "Phù hai mi mắt buổi sáng, lan xuống hai chân kèm tiểu nhiều bọt lâu tan 2 tuần nay",
            "history": "Tăng 5 kg trong 2 tuần, không sốt, không tiểu máu đại thể, không dùng thuốc giảm đau NSAIDs hay thảo dược.",
            "vital_signs": {"bp": "135/85", "hr": 78, "temp": 37.0, "spo2": 98}
        },
        "steps": [
            {
                "step_title": "Khai thác bệnh sử & Tiền căn",
                "prompt": "Bệnh nhân vào viện vì phù toàn thân và tiểu nhiều bọt. Câu hỏi bệnh sử nào quan trọng nhất giúp định hướng nguyên nhân phù do thận?",
                "options": [
                    {"text": "Hỏi tính chất phù xuất hiện ở đâu trước, diễn tiến theo thời gian trong ngày và đặc điểm nước tiểu (bọt lâu tan, lượng nước tiểu 24h)", "score": 20, "feedback": "Chính xác! Phù do cầu thận điển hình xuất hiện ở mi mắt buổi sáng, phù trắng mềm ấn lõm đối xứng kèm tiểu bọt lâu tan do đạm niệu cao."},
                    {"text": "Chỉ hỏi tiền sử đau khớp gối khi leo cầu thang", "score": 5, "feedback": "Chưa đúng trọng tâm: Đau khớp gối cơ học ít liên quan trực tiếp đến hội chứng phù toàn thân cấp tính."},
                    {"text": "Chỉ hỏi thói quen đọc sách và thời gian ngủ buổi tối", "score": 0, "feedback": "Không có giá trị định hướng chẩn đoán nguyên nhân phù toàn thân."},
                    {"text": "Yêu cầu bệnh nhân nhịn uống nước hoàn toàn trước khi hỏi bệnh", "score": 0, "feedback": "Sai nguyên tắc tiếp cận lâm sàng ban đầu."}
                ]
            },
            {
                "step_title": "Thăm khám lâm sàng",
                "prompt": "Khi thăm khám thực thể cho bệnh nhân nghi ngờ Hội chứng thận hư, thao tác nào cần ưu tiên thực hiện đầy đủ?",
                "options": [
                    {"text": "Chỉ bắt mạch quay và bỏ qua khám phù hay khám màng bụng", "score": 5, "feedback": "Thiếu sót lớn: Bắt buộc đánh giá mức độ phù và dịch các màng."},
                    {"text": "Ấn tìm dấu phù lõm mặt trước xương chày, cân nặng, đo huyết áp, gõ bụng tìm dịch cổ trướng và nghe phổi tìm tràn dịch màng phổi", "score": 20, "feedback": "Xuất sắc! Hội chứng thận hư gây giảm áp lực keo máu dẫn đến phù trắng mềm ấn lõm và tràn dịch đa màng (màng bụng, màng phổi)."},
                    {"text": "Khám phản xạ gân xương bánh chè đơn thuần", "score": 0, "feedback": "Không giúp đánh giá tình trạng ứ dịch hay biến chứng hội chứng thận hư."},
                    {"text": "Nghiệm pháp Lasègue hai chân", "score": 0, "feedback": "Lasègue dùng cho đau thần kinh tọa, không phải khám phù thận."}
                ]
            },
            {
                "step_title": "Chỉ định Cận lâm sàng",
                "prompt": "Bộ xét nghiệm cận lâm sàng nào là TIÊU CHUẨN BẮT BUỘC để xác lập chẩn đoán Hội chứng thận hư?",
                "options": [
                    {"text": "Chụp X-quang khớp cổ chân hai bên", "score": 0, "feedback": "Phù chân trong bệnh thận là phù mô mềm do giảm áp lực keo, không phải tổn thương xương khớp."},
                    {"text": "Đo điện tâm đồ 12 chuyển đạo đơn thuần", "score": 5, "feedback": "ECG không thể chẩn đoán xác định hội chứng thận hư."},
                    {"text": "Định lượng Protein niệu 24 giờ (hoặc tỷ lệ Protein/Creatinin niệu), Albumin & Protein máu toàn phần, Bộ mỡ máu (Lipid) và Tổng phân tích nước tiểu", "score": 20, "feedback": "Hoàn hảo! Kết quả trả về: Protein niệu 24h = 5,8 g/24h (> 3,5 g/24h), Albumin máu = 21 g/L (< 30 g/L), Cholesterol = 9,8 mmol/L, cặn lắng có trụ mỡ."},
                    {"text": "Nội soi dạ dày – tá tràng ống mềm", "score": 0, "feedback": "Không có chỉ định trong bối cảnh phù thận tiểu đạm."}
                ]
            },
            {
                "step_title": "Chẩn đoán xác định",
                "prompt": "Dựa trên: Phù trắng mềm ấn lõm + Protein niệu 5,8 g/24h + Albumin máu 21 g/L + Cholesterol 9,8 mmol/L + Creatinin máu 88 µmol/L, chẩn đoán chính xác nhất là:",
                "options": [
                    {"text": "Viêm bàng quang cấp không biến chứng", "score": 0, "feedback": "Viêm bàng quang không gây protein niệu ngưỡng thận hư (> 3,5 g/24h) và giảm albumin máu nặng."},
                    {"text": "Hội chứng thận hư nguyên phát thể đơn thuần (đủ tiêu chuẩn Protein niệu > 3,5 g/24h và Albumin máu < 30 g/L)", "score": 20, "feedback": "Chính xác! Hai tiêu chuẩn bắt buộc của Hội chứng thận hư là Protein niệu > 3,5 g/24h/1,73m² và Albumin máu < 30 g/L (Protein máu < 60 g/L)."},
                    {"text": "Cơn đau quặn thận do sỏi niệu quản", "score": 0, "feedback": "Bệnh nhân không đau hông lưng và không tiểu máu."},
                    {"text": "Suy gan cấp do ngộ độc Paracetamol", "score": 5, "feedback": "Suy gan có thể giảm albumin nhưng không gây tiểu đạm 5,8 g/24h và trụ mỡ niệu."}
                ]
            },
            {
                "step_title": "Điều trị & Chăm sóc theo dõi",
                "prompt": "Phác đồ điều trị và chăm sóc điều dưỡng chuẩn cho bệnh nhân Hội chứng thận hư giai đoạn phù nhiều là:",
                "options": [
                    {"text": "Truyền thật nhiều dung dịch NaCl 0,9% tốc độ nhanh và ăn mặn để bù muối", "score": 0, "feedback": "Nguy hiểm! Ăn mặn và truyền NaCl làm tình trạng phù và ứ muối nước nặng thêm."},
                    {"text": "Dùng kháng sinh liều cao kéo dài 6 tháng cho mọi bệnh nhân", "score": 0, "feedback": "Hội chứng thận hư nguyên phát có cơ chế miễn dịch cầu thận, không điều trị đặc hiệu bằng kháng sinh."},
                    {"text": "Ăn nhạt (< 2g Na/ngày), theo dõi cân nặng & lượng nước xuất-nhập 24h, Corticosteroid (Prednisone 1 mg/kg/ngày) + Lợi tiểu quai + Ức chế men chuyển giảm đạm niệu + Statin", "score": 20, "feedback": "Tuyệt vời! Phác đồ toàn diện gồm ức chế miễn dịch bằng Corticoid, hạn chế muối-nước, lợi tiểu kiểm soát phù, ACEi/ARB giảm đạm niệu và theo dõi cân nặng/nước tiểu hàng ngày."},
                    {"text": "Chỉ chườm nóng hai cẳng chân và cho xuất viện ngay", "score": 5, "feedback": "Không giải quyết được cơ chế mất protein qua màng lọc cầu thận và nguy cơ huyết khối/nhiễm trùng."}
                ]
            }
        ]
    },
    {
        "id": "case_gout_02",
        "title": "Ca 2: Cơn Gout cấp tính trên nền tăng huyết áp",
        "patient": {
            "name": "Trần Văn T.",
            "age": 52,
            "gender": "Nam",
            "chief_complaint": "Đau buốt, sưng nóng đỏ dữ dội khớp bàn ngón 1 chân phải khởi phát đột ngột lúc nửa đêm",
            "history": "Khởi phát sau bữa tiệc hải sản và bia tối hôm trước. Tiền sử tăng huyết áp 3 năm đang dùng thuốc đều.",
            "vital_signs": {"bp": "145/90", "hr": 92, "temp": 37.8, "spo2": 98}
        },
        "steps": [
            {
                "step_title": "Khai thác bệnh sử & Yếu tố khởi phát",
                "prompt": "Đặc điểm lâm sàng nào kinh điển nhất khi khai thác bệnh sử cơn Gout cấp?",
                "options": [
                    {"text": "Đau âm ỉ hai khớp gối tăng dần suốt 5 năm không sưng đỏ", "score": 5, "feedback": "Đây là đặc điểm của thoái hóa khớp mạn tính, không phải cơn Gout cấp."},
                    {"text": "Khởi phát đột ngột lúc nửa đêm về sáng tại khớp bàn ngón chân cái (Podagra) sau bữa ăn giàu purin/rượu bia, đau đạt đỉnh trong 12–24 giờ đầu", "score": 20, "feedback": "Chính xác! Cơn Gout cấp kinh điển khởi phát đột ngột ban đêm ở khớp bàn ngón 1 chân cái, đau dữ dội đến mức chạm nhẹ ga giường cũng đau."},
                    {"text": "Cứng khớp bàn tay buổi sáng kéo dài trên 2 giờ đối xứng hai bên", "score": 5, "feedback": "Đây là triệu chứng điển hình của Viêm khớp dạng thấp (RA)."},
                    {"text": "Đau lan từ thắt lưng xuống mặt sau đùi và cẳng chân", "score": 0, "feedback": "Đây là hội chứng chèn ép rễ thần kinh tọa."}
                ]
            },
            {
                "step_title": "Thăm khám thực thể",
                "prompt": "Khi khám khớp và toàn thân cho bệnh nhân nghi ngờ Gout, cần chú ý tìm dấu hiệu đặc hiệu nào?",
                "options": [
                    {"text": "Khám khớp bàn ngón 1 sưng to, da căng bóng đỏ rực, nóng, tăng cảm đau; đồng thời tìm hạt Tophi ở vành tai, khuỷu tay, gân gót", "score": 20, "feedback": "Rất chuẩn! Khám tại khớp viêm cấp và tìm hạt Tophi dưới da giúp đánh giá giai đoạn bệnh Gout."},
                    {"text": "Chỉ nghe tiếng nhu động ruột vùng hố chậu phải", "score": 0, "feedback": "Không liên quan đến viêm khớp bàn ngón chân cái."},
                    {"text": "Bắt bệnh nhân chạy bộ tại chỗ 15 phút để xem mức độ đau", "score": 0, "feedback": "Sai hoàn toàn: Khớp đang viêm cấp cực đau cần được nghỉ ngơi bất động."},
                    {"text": "Chỉ đo thị lực hai mắt", "score": 0, "feedback": "Không phải trọng tâm khám viêm khớp Gout cấp."}
                ]
            },
            {
                "step_title": "Chỉ định Cận lâm sàng & Tiêu chuẩn vàng",
                "prompt": "Xét nghiệm nào là TIÊU CHUẨN VÀNG để chẩn đoán xác định Gout, kèm bộ xét nghiệm sinh hóa cần làm?",
                "options": [
                    {"text": "Định lượng Glucose máu bất kỳ đơn thuần", "score": 5, "feedback": "Không đủ để chẩn đoán Gout."},
                    {"text": "Chụp CT sọ não không cản quang", "score": 0, "feedback": "Không có chỉ định trong viêm khớp bàn ngón chân."},
                    {"text": "Soi dịch khớp dưới kính hiển vi phân cực tìm tinh thể Monosodium Urat (MSU) hình kim nằm trong bạch cầu đa nhân, kèm Acid Uric máu, CRP và Creatinin/eGFR", "score": 20, "feedback": "Hoàn hảo! Tinh thể MSU hình kim nhọn lưỡng chiết quang âm tính trong dịch khớp là tiêu chuẩn vàng; kết quả Acid Uric máu = 585 µmol/L, CRP = 48 mg/L, eGFR = 82 mL/phút."},
                    {"text": "Siêu âm tuyến giáp", "score": 0, "feedback": "Không liên quan đến bệnh cảnh Gout cấp."}
                ]
            },
            {
                "step_title": "Chẩn đoán & Biện luận hóa sinh",
                "prompt": "Cơ chế hóa sinh trực tiếp hình thành Acid Uric ở người và ngưỡng bão hòa kết tinh tinh thể Monosodium Urat trong huyết tương là:",
                "options": [
                    {"text": "Thoái hóa base Pyrimidin nhờ enzyme Amylase; ngưỡng > 100 µmol/L", "score": 0, "feedback": "Sai: Acid uric là sản phẩm thoái hóa của base Purin (Adenin, Guanin), không phải Pyrimidin."},
                    {"text": "Thoái hóa base Purin qua trung gian Xanthine nhờ enzyme Xanthine Oxidase; kết tinh MSU khi Acid Uric máu vượt ngưỡng bão hòa > 420 µmol/L (7,0 mg/dL)", "score": 20, "feedback": "Chính xác tuyệt đối! Người thiếu enzyme Uricase nên Acid Uric là sản phẩm cuối cùng của thoái hóa Purin; khi nồng độ > 420 µmol/L (7 mg/dL) sẽ dễ kết tinh tinh thể MSU tại khớp."},
                    {"text": "Tổng hợp từ Cholesterol tại gan nhờ HMG-CoA reductase", "score": 0, "feedback": "HMG-CoA reductase là enzyme tổng hợp Cholesterol, không phải Acid Uric."},
                    {"text": "Thủy phân Glycogen tại cơ vân", "score": 0, "feedback": "Thủy phân glycogen tạo Glucose-1-phosphate."}
                ]
            },
            {
                "step_title": "Phác đồ điều trị & Nguyên tắc dùng Allopurinol",
                "prompt": "Nguyên tắc điều trị ĐÚNG NHẤT cho bệnh nhân đang trong cơn Gout cấp bùng phát dữ dội là:",
                "options": [
                    {"text": "Khởi trị ngay Allopurinol liều cao 600 mg/ngày ngay trong ngày đầu cơn đau cấp mà không dùng thuốc kháng viêm", "score": 0, "feedback": "SAI LẦM NGUY HIỂM! Khởi trị mới Allopurinol trong cơn Gout cấp làm biến động nồng độ acid uric máu đột ngột, khiến tinh thể urat bong ra nhiều hơn và làm cơn đau kéo dài/nặng hơn!"},
                    {"text": "Cắt cơn viêm cấp bằng Colchicine liều thấp (1 mg liều đầu, sau 1 giờ uống 0,5 mg) phối hợp NSAID, nghỉ ngơi chườm lạnh; CHỈ khởi trị Allopurinol sau khi cơn viêm cấp đã ổn định hoàn toàn", "score": 20, "feedback": "Xuất sắc! Quy tắc vàng: Cắt cơn viêm cấp trước (Colchicine/NSAID/Corticoid), tuyệt đối không khởi trị mới Allopurinol trong lúc đang bùng phát cơn Gout cấp."},
                    {"text": "Chườm nước thật nóng lên khớp đang sưng đỏ và xoa bóp mạnh", "score": 0, "feedback": "Chườm nóng và xoa bóp làm giãn mạch tăng sung huyết khiến khớp sưng đau dữ dội hơn."},
                    {"text": "Tiêm Penicillin tĩnh mạch liều cao", "score": 0, "feedback": "Gout cấp là viêm khớp tinh thể vô khuẩn, không điều trị bằng kháng sinh."}
                ]
            }
        ]
    },
    {
        "id": "case_anaphylaxis_03",
        "title": "Ca 3: Xử trí & Chăm sóc Điều dưỡng Sốc phản vệ độ II–III sau tiêm kháng sinh",
        "patient": {
            "name": "Lê Thị M.",
            "age": 31,
            "gender": "Nữ",
            "chief_complaint": "Khó thở, nổi mày đay toàn thân, choáng váng chỉ 5 phút sau khi bắt đầu truyền kháng sinh Ceftriaxone",
            "history": "Vào viện vì viêm phổi cộng đồng. Đang truyền Ceftriaxone tĩnh mạch được 5 phút thì bồn chồn, ngứa ran, khàn tiếng, tụt huyết áp.",
            "vital_signs": {"bp": "80/50", "hr": 124, "temp": 37.2, "spo2": 89}
        },
        "steps": [
            {
                "step_title": "Nhận định cấp cứu & Hành động đầu tiên tại giường",
                "prompt": "Ngay khi phát hiện người bệnh nổi mày đay, khó thở rít, HA tụt 80/50 mmHg trong lúc đang truyền kháng sinh, hành động ĐẦU TIÊN của điều dưỡng là:",
                "options": [
                    {"text": "Tăng tốc độ truyền kháng sinh chảy thật nhanh để hết chai thuốc sớm", "score": 0, "feedback": "Nguy hiểm tính mạng! Tiếp tục đưa dị nguyên vào máu sẽ gây ngừng tuần hoàn ngay lập tức."},
                    {"text": "Khóa ngay đường truyền kháng sinh (giữ nguyên kim luồn tĩnh mạch), cho người bệnh nằm đầu thấp chân cao, gọi hỗ trợ cấp cứu và lấy hộp thuốc chống sốc phản vệ", "score": 20, "feedback": "Chính xác! Bước đầu tiên sống còn là NGỪNG NGAY tiếp xúc với dị nguyên (khóa dây truyền thuốc nhưng giữ đường truyền tĩnh mạch để cấp cứu) và gọi cấp cứu tại chỗ."},
                    {"text": "Rút bỏ kim luồn tĩnh mạch rồi cho bệnh nhân tự đi bộ sang phòng khám khác", "score": 0, "feedback": "Sai nghiêm trọng: Rút mất đường truyền tĩnh mạch khi đang tụt huyết áp sẽ rất khó lấy lại ven, và bệnh nhân sốc tuyệt đối không được đứng dậy đi lại."},
                    {"text": "Chờ 30 phút xem triệu chứng có tự hết không rồi mới báo bác sĩ", "score": 0, "feedback": "Sốc phản vệ diễn tiến tính bằng phút, trì hoãn sẽ dẫn tới tử vong."}
                ]
            },
            {
                "step_title": "Thuốc cấp cứu đầu tay & Đường dùng chuẩn",
                "prompt": "Theo phác đồ xử trí phản vệ của Bộ Y tế, thuốc SỐNG CÒN ĐẦU TAY, liều lượng và đường tiêm chuẩn ngay lập tức cho người lớn là:",
                "options": [
                    {"text": "Adrenalin 1 mg/1 mL: tiêm BẮP (IM) mặt trước ngoài đùi 1/2 – 1 ống (0,5 – 1 mg) ngay lập tức", "score": 20, "feedback": "Chuẩn xác 100%! Adrenalin tiêm bắp mặt trước ngoài đùi là thuốc duy nhất cứu sống người bệnh phản vệ từ độ II trở lên, có thể nhắc lại mỗi 3–5 phút nếu huyết áp chưa lên."},
                    {"text": "Chỉ uống 1 viên Loratadin 10 mg và theo dõi", "score": 0, "feedback": "Kháng Histamin đường uống tác dụng quá chậm và không nâng được huyết áp hay chống co thắt phế quản cấp."},
                    {"text": "Tiêm thẳng 1 ống Adrenalin nguyên chất 1 mg tĩnh mạch nhanh (bolus) không pha loãng", "score": 0, "feedback": "Nguy hiểm! Tiêm tĩnh mạch nhanh Adrenalin nguyên chất dễ gây rung thất và xuất huyết não; đường chuẩn ban đầu là TIÊM BẮP."},
                    {"text": "Chỉ bôi kem dưỡng ẩm ngoài da vùng nổi mề đay", "score": 0, "feedback": "Không có tác dụng cấp cứu sốc phản vệ."}
                ]
            },
            {
                "step_title": "Hồi sức Hô hấp – Tuần hoàn phối hợp",
                "prompt": "Song song với tiêm bắp Adrenalin, điều dưỡng thực hiện các y lệnh hồi sức hô hấp và tuần hoàn nào tiếp theo?",
                "options": [
                    {"text": "Cho bệnh nhân uống 2 lít nước lọc thật nhanh", "score": 0, "feedback": "Bệnh nhân đang khó thở, tụt huyết áp uống nước dễ sặc vào phổi."},
                    {"text": "Thở Oxy qua mặt nạ 6–10 L/phút (giữ SpO2 ≥ 95%) và truyền nhanh NaCl 0,9% 1.000–2.000 mL qua đường truyền tĩnh mạch lớn để bù thể tích tuần hoàn", "score": 20, "feedback": "Chính xác! Trong sốc phản vệ có giãn mạch và thoát dịch lòng mạch mạnh nên bắt buộc thở oxy lưu lượng cao và bù dịch tinh thể NaCl 0,9% tốc độ nhanh."},
                    {"text": "Truyền dung dịch ưu trương Glucose 30% duy nhất", "score": 5, "feedback": "Dịch hồi sức thể tích đầu tay trong sốc phản vệ là NaCl 0,9%, không phải Glucose ưu trương."},
                    {"text": "Đặt bệnh nhân ngồi thõng hai chân xuống giường", "score": 0, "feedback": "Ngồi thõng chân làm giảm máu về tim khiến tụt huyết áp nặng hơn (trừ khi phù phổi cấp)."}
                ]
            },
            {
                "step_title": "Thuốc phối hợp giải phóng muộn (Pha 2)",
                "prompt": "Sau khi huyết áp và hô hấp đã tạm ổn định nhờ Adrenalin và truyền dịch, nhóm thuốc hỗ trợ nào được dùng để ngăn ngừa phản vệ pha 2?",
                "options": [
                    {"text": "Methylprednisolone 1–2 mg/kg IV (Corticoid) phối hợp Diphenhydramin (Kháng Histamin H1) theo y lệnh", "score": 20, "feedback": "Đúng! Corticoid và kháng Histamin là thuốc hàng thứ hai giúp ổn định dưỡng bào và dự phòng phản ứng phản vệ pha 2 (tái phát sau 4–24 giờ)."},
                    {"text": "Tiêm lại ngay kháng sinh Ceftriaxone vừa gây dị ứng để thử lại", "score": 0, "feedback": "Chống chỉ định tuyệt đối việc thử lại thuốc vừa gây sốc phản vệ!"},
                    {"text": "Dùng thuốc hạ huyết áp Nifedipin ngậm dưới lưỡi", "score": 0, "feedback": "Bệnh nhân đang sốc tụt huyết áp, dùng thuốc hạ áp sẽ gây trụy mạch."},
                    {"text": "Dùng Insulin tiêm dưới da", "score": 0, "feedback": "Không có chỉ định trong phác đồ chống sốc phản vệ."}
                ]
            },
            {
                "step_title": "Theo dõi sau cấp cứu & Dự phòng tái diễn",
                "prompt": "Thời gian bắt buộc theo dõi bệnh nhân tại bệnh viện sau khi cắt cơn phản vệ và quy định ghi hồ sơ dị ứng là:",
                "options": [
                    {"text": "Cho xuất viện về nhà ngay sau 15 phút khi thấy hết nổi mề đay", "score": 0, "feedback": "Rất nguy hiểm vì nguy cơ phản vệ pha 2 (biphasic anaphylaxis) có thể xảy ra trong 24 giờ đầu!"},
                    {"text": "Theo dõi sát mạch, HA, nhịp thở, SpO2 ít nhất 24 giờ tại viện để phòng phản vệ pha 2; ghi rõ dị ứng Ceftriaxone vào hồ sơ bệnh án và cấp thẻ theo dõi dị ứng cho người bệnh", "score": 20, "feedback": "Hoàn hảo! Phải theo dõi tối thiểu 24 giờ tại cơ sở y tế và cấp thẻ ghi nhận dị ứng thuốc suốt đời cho người bệnh."},
                    {"text": "Không cần ghi vào hồ sơ bệnh án vì bệnh nhân đã khỏi", "score": 0, "feedback": "Bắt buộc phải ghi rõ tiền sử dị ứng và cấp thẻ dị ứng để tránh tái phơi nhiễm gây tử vong lần sau."},
                    {"text": "Chỉ theo dõi nhiệt độ 1 lần rồi ngưng mọi theo dõi", "score": 5, "feedback": "Không đảm bảo an toàn người bệnh sau sốc phản vệ."}
                ]
            }
        ]
    }
]


# ==========================================
# 1. HANDLERS: EXPORT ANKI & PRINTABLE EXAM
# ==========================================
async def export_anki_handler(request):
    """Xuất câu hỏi sang file TSV (Tab-Separated Values) chuẩn để nhập 1-click vào app Anki trên ĐT/PC"""
    try:
        sid_raw = request.query.get("subject_id")
        subjects = db.get_all_subjects()
        target_sids = [int(sid_raw)] if sid_raw and sid_raw.isdigit() else [s["id"] for s in subjects]

        lines = ["#separator:tab", "#html:true", "#tags column:3"]
        count = 0
        for sid in target_sids:
            sub = next((s for s in subjects if s["id"] == sid), None)
            sname = sub["code"] if sub else "UniMaster"
            questions = db.get_questions_by_subject(sid)
            for q in questions:
                # Front: Question text + code + options
                front_parts = [f"<b>{q['question_text']}</b>"]
                if q.get("code_snippet"):
                    front_parts.append(f"<pre><code>{q['code_snippet']}</code></pre>")
                if q.get("image_url"):
                    front_parts.append(f"<img src='{q['image_url']}'>")
                if q.get("option_a"):
                    front_parts.append(f"<div>A. {q['option_a']}<br>B. {q['option_b']}<br>C. {q['option_c']}<br>D. {q['option_d']}</div>")
                front = "<br>".join(front_parts).replace("\t", " ").replace("\n", "<br>")

                # Back: Correct Answer + Explanation
                corr = q.get("correct_option", "A")
                expl = q.get("explanation", "")
                back = f"<b>Đáp án đúng: {corr}</b><br><br>{expl}".replace("\t", " ").replace("\n", "<br>")

                tag = f"{sname} {q.get('topic_tag', '').replace(' ', '_')}"
                lines.append(f"{front}\t{back}\t{tag}")
                count += 1

        body = "\n".join(lines)
        return web.Response(
            text=body,
            content_type="text/tab-separated-values",
            charset="utf-8",
            headers={"Content-Disposition": 'attachment; filename="UniMaster_Anki_Deck.txt"'}
        )
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


async def export_printable_exam_handler(request):
    """Tạo đề thi định dạng Word / HTML in ấn chuẩn Bộ Giáo Dục & ĐHYD Cần Thơ có bảng đáp án riêng"""
    try:
        sid_raw = request.query.get("subject_id", "10")
        sid = int(sid_raw) if sid_raw.isdigit() else 10
        limit = min(100, max(10, int(request.query.get("limit", "40"))))

        subjects = db.get_all_subjects()
        sub = next((s for s in subjects if s["id"] == sid), None)
        sub_name = sub["name"] if sub else "Hóa Sinh Y Khoa"

        questions = db.get_questions_by_subject(sid, random_order=True, limit=limit)

        q_html = []
        key_rows = []
        for idx, q in enumerate(questions, 1):
            q_html.append(f"""
            <div style="margin-bottom: 14px; page-break-inside: avoid;">
              <p style="margin: 0 0 6px 0; font-weight: bold;">Câu {idx}: {q['question_text']}</p>
              {f"<p style='margin: 4px 0;'><img src='{q['image_url']}' style='max-height: 180px;'></p>" if q.get('image_url') else ""}
              <table style="width: 100%; border: none; margin-left: 10px;">
                <tr>
                  <td style="width: 50%;">A. {q['option_a']}</td>
                  <td style="width: 50%;">B. {q['option_b']}</td>
                </tr>
                <tr>
                  <td style="width: 50%;">C. {q['option_c']}</td>
                  <td style="width: 50%;">D. {q['option_d']}</td>
                </tr>
              </table>
            </div>
            """)
            key_rows.append(f"<td style='border: 1px solid #000; padding: 4px 6px; text-align: center;'><b>{idx}</b>: {q['correct_option']}</td>")

        # Split keys into rows of 10
        key_tables = []
        for i in range(0, len(key_rows), 10):
            chunk = "".join(key_rows[i:i+10])
            key_tables.append(f"<tr>{chunk}</tr>")

        html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Đề thi trắc nghiệm {sub_name}</title>
<style>
  @page {{ size: A4; margin: 20mm; }}
  body {{ font-family: 'Times New Roman', Times, serif; font-size: 13pt; line-height: 1.35; color: #000; }}
  .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }}
  .header-left {{ text-align: center; font-weight: bold; width: 45%; }}
  .header-right {{ text-align: center; font-weight: bold; width: 50%; }}
  .title {{ text-align: center; font-size: 16pt; font-weight: bold; margin: 15px 0 25px 0; text-transform: uppercase; }}
  .answer-sheet {{ page-break-before: always; margin-top: 30px; }}
</style>
</head>
<body>
  <div class="header">
    <div class="header-left">
      TRƯỜNG ĐẠI HỌC Y DƯỢC CẦN THƠ<br>
      KHOA Y — BỘ MÔN HÓA SINH<br>
      -------***-------
    </div>
    <div class="header-right">
      CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM<br>
      Độc lập - Tự do - Hạnh phúc<br>
      ---------------------
    </div>
  </div>

  <div class="title">
    ĐỀ THI TRẮC NGHIỆM HỌC PHẦN: {sub_name}<br>
    <span style="font-size: 12pt; font-weight: normal; font-style: italic;">(Thời gian làm bài: {int(limit * 1.2)} phút — Gồm {len(questions)} câu hỏi)</span>
  </div>

  <div class="content">
    {"".join(q_html)}
  </div>

  <div class="answer-sheet">
    <h3 style="text-align: center; text-transform: uppercase;">BẢNG ĐÁP ÁN CHUẨN (DÀNH CHO GIẢNG VIÊN CHẤM THI)</h3>
    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
      {"".join(key_tables)}
    </table>
  </div>
</body>
</html>"""

        safe_code = re.sub(r"[^A-Za-z0-9_-]", "_", str(sub.get("code") if sub else "UniMaster"))
        return web.Response(
            text=html_doc,
            content_type="application/msword",
            charset="utf-8",
            headers={"Content-Disposition": f'attachment; filename="De_Thi_{safe_code}.doc"'}
        )
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


# ==========================================
# 2. HANDLERS: CLINICAL DRUG DOSING ENGINE
# ==========================================
async def get_drug_database_handler(request):
    query = request.query.get("q", "").strip().lower()
    if query:
        filtered = [d for d in DRUG_DATABASE if query in d["name"].lower() or query in d["group"].lower() or query in d["indication"].lower()]
    else:
        filtered = DRUG_DATABASE
    return web.json_response({"success": True, "drugs": filtered})


async def calculate_renal_dose_handler(request):
    try:
        data = await request.json()
        drug_id = data.get("drug_id")
        crcl = float(data.get("crcl", 80))
        weight = float(data.get("weight", 60))
        age = int(data.get("age", 50))
        is_female = bool(data.get("is_female", False))

        drug = next((d for d in DRUG_DATABASE if d["id"] == drug_id), DRUG_DATABASE[0])

        if crcl >= 50:
            rec = drug["crcl_normal"]
            status = "normal"
        elif crcl >= 20:
            rec = drug["crcl_mod"]
            status = "moderate_reduction"
        else:
            rec = drug["crcl_severe"]
            status = "severe_reduction"

        return web.json_response({
            "success": True,
            "drug": drug,
            "crcl_used": crcl,
            "status": status,
            "recommendation": rec,
            "hd_recommendation": drug["hd_dose"],
            "warning": drug["warning"]
        })
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


# ==========================================
# 3. HANDLERS: BIOSTATISTICS & RESEARCH LAB
# ==========================================
async def biostat_calculate_handler(request):
    try:
        data = await request.json()
        calc_type = data.get("type", "2x2")

        if calc_type == "2x2":
            # Contingency table:
            #          Disease+    Disease-
            # Test+       a           b
            # Test-       c           d
            a = float(data.get("a", 80))
            b = float(data.get("b", 20))
            c = float(data.get("c", 10))
            d = float(data.get("d", 90))

            total = a + b + c + d
            sens = (a / (a + c)) * 100 if (a + c) > 0 else 0.0
            spec = (d / (b + d)) * 100 if (b + d) > 0 else 0.0
            ppv = (a / (a + b)) * 100 if (a + b) > 0 else 0.0
            npv = (d / (c + d)) * 100 if (c + d) > 0 else 0.0
            accuracy = ((a + d) / total) * 100 if total > 0 else 0.0

            # Odds Ratio (OR) = (a * d) / (b * c)
            odds_ratio = (a * d) / (b * c) if (b * c) > 0 else 0.0
            # 95% CI for OR: exp(ln(OR) ± 1.96 * SE)
            if a > 0 and b > 0 and c > 0 and d > 0:
                se_ln_or = math.sqrt(1/a + 1/b + 1/c + 1/d)
                ln_or = math.log(odds_ratio)
                or_ci_low = math.exp(ln_or - 1.96 * se_ln_or)
                or_ci_high = math.exp(ln_or + 1.96 * se_ln_or)
            else:
                or_ci_low, or_ci_high = 0.0, 0.0

            # Relative Risk (RR) = [a / (a + b)] / [c / (c + d)]
            risk_exp = a / (a + b) if (a + b) > 0 else 0
            risk_unexp = c / (c + d) if (c + d) > 0 else 0
            relative_risk = risk_exp / risk_unexp if risk_unexp > 0 else 0.0

            # Chi-square with Yates' correction: (|ad - bc| - N/2)^2 * N / [(a+b)(c+d)(a+c)(b+d)]
            num = max(0, abs(a * d - b * c) - total / 2) ** 2 * total
            denom = (a + b) * (c + d) * (a + c) * (b + d)
            chi2 = num / denom if denom > 0 else 0.0
            p_val = "< 0.001" if chi2 > 10.83 else "< 0.01" if chi2 > 6.63 else "< 0.05" if chi2 > 3.84 else "≥ 0.05 (Không có ý nghĩa thống kê)"

            return web.json_response({
                "success": True,
                "sensitivity": round(sens, 1),
                "specificity": round(spec, 1),
                "ppv": round(ppv, 1),
                "npv": round(npv, 1),
                "accuracy": round(accuracy, 1),
                "odds_ratio": round(odds_ratio, 2),
                "or_ci": f"{round(or_ci_low, 2)} – {round(or_ci_high, 2)}",
                "relative_risk": round(relative_risk, 2),
                "chi_square": round(chi2, 2),
                "p_value": p_val
            })

        return web.json_response({"success": False, "error": "Chưa hỗ trợ loại phép tính này"}, status=400)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


# ==========================================
# 4. HANDLERS: VIRTUAL PATIENT SIMULATOR
# ==========================================
async def get_virtual_cases_handler(request):
    return web.json_response({"success": True, "cases": VIRTUAL_CASES})


# ==========================================
# 5. WEBSOCKET: REAL-TIME MULTIPLAYER ARENA
# ==========================================
async def websocket_arena_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    current_room = None
    player_id = None
    is_host = False

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = json.loads(msg.data)
                action = data.get("action")

                if action == "create_room":
                    room_code = data.get("room_code", "CTUMP88").upper().strip()
                    subject_id = int(data.get("subject_id", 10))
                    q_count = min(30, max(5, int(data.get("count", 10))))

                    questions = db.get_questions_by_subject(subject_id, random_order=True, limit=q_count)
                    ARENA_ROOMS[room_code] = {
                        "host_ws": ws,
                        "players": {},
                        "questions": questions,
                        "current_q": 0,
                        "status": "waiting"
                    }
                    current_room = room_code
                    is_host = True
                    await ws.send_json({"type": "room_created", "room_code": room_code, "total_questions": len(questions)})

                elif action == "join_room":
                    room_code = data.get("room_code", "").upper().strip()
                    p_name = data.get("player_name", "Sinh viên").strip()
                    player_id = f"p_{int(time.time() * 1000)}"

                    if room_code not in ARENA_ROOMS:
                        await ws.send_json({"type": "error", "message": f"Phòng {room_code} không tồn tại!"})
                        continue

                    room = ARENA_ROOMS[room_code]
                    room["players"][player_id] = {"name": p_name, "score": 0, "ws": ws}
                    current_room = room_code

                    # Broadcast new player to all in room
                    player_list = [{"id": pid, "name": p["name"], "score": p["score"]} for pid, p in room["players"].items()]
                    msg_payload = {"type": "player_joined", "player_name": p_name, "players": player_list}

                    if room["host_ws"] and not room["host_ws"].closed:
                        await room["host_ws"].send_json(msg_payload)
                    for p in room["players"].values():
                        if p["ws"] and not p["ws"].closed:
                            await p["ws"].send_json(msg_payload)

                elif action == "start_quiz":
                    if not is_host or not current_room or current_room not in ARENA_ROOMS:
                        continue
                    room = ARENA_ROOMS[current_room]
                    room["status"] = "in_game"
                    room["current_q"] = 0
                    q = room["questions"][0]

                    payload = {
                        "type": "new_question",
                        "q_idx": 1,
                        "total": len(room["questions"]),
                        "question": {
                            "text": q["question_text"],
                            "a": q["option_a"],
                            "b": q["option_b"],
                            "c": q["option_c"],
                            "d": q["option_d"],
                            "image_url": q.get("image_url", "")
                        }
                    }
                    for p in room["players"].values():
                        if p["ws"] and not p["ws"].closed:
                            await p["ws"].send_json(payload)
                    await ws.send_json(payload)

                elif action == "submit_answer":
                    if not current_room or current_room not in ARENA_ROOMS or not player_id:
                        continue
                    room = ARENA_ROOMS[current_room]
                    q = room["questions"][room["current_q"]]
                    ans = data.get("answer", "").upper().strip()
                    time_taken = float(data.get("time_taken", 5.0))  # seconds

                    is_correct = (ans == q["correct_option"])
                    added_score = 0
                    if is_correct:
                        # Speed bonus: faster answer gives up to 1000 points
                        added_score = int(max(400, 1000 - time_taken * 40))

                    if player_id in room["players"]:
                        room["players"][player_id]["score"] += added_score

                    # Send feedback to this player
                    await ws.send_json({
                        "type": "answer_feedback",
                        "is_correct": is_correct,
                        "correct_option": q["correct_option"],
                        "explanation": q.get("explanation", ""),
                        "added_score": added_score,
                        "total_score": room["players"][player_id]["score"]
                    })

                    # Update leaderboard for Host
                    leaderboard = sorted(
                        [{"name": p["name"], "score": p["score"]} for p in room["players"].values()],
                        key=lambda x: x["score"],
                        reverse=True
                    )
                    lb_msg = {"type": "leaderboard_update", "leaderboard": leaderboard}
                    if room["host_ws"] and not room["host_ws"].closed:
                        await room["host_ws"].send_json(lb_msg)

                elif action == "next_question":
                    if not is_host or not current_room or current_room not in ARENA_ROOMS:
                        continue
                    room = ARENA_ROOMS[current_room]
                    room["current_q"] += 1
                    if room["current_q"] < len(room["questions"]):
                        q = room["questions"][room["current_q"]]
                        payload = {
                            "type": "new_question",
                            "q_idx": room["current_q"] + 1,
                            "total": len(room["questions"]),
                            "question": {
                                "text": q["question_text"],
                                "a": q["option_a"],
                                "b": q["option_b"],
                                "c": q["option_c"],
                                "d": q["option_d"],
                                "image_url": q.get("image_url", "")
                            }
                        }
                        for p in room["players"].values():
                            if p["ws"] and not p["ws"].closed:
                                await p["ws"].send_json(payload)
                        await ws.send_json(payload)
                    else:
                        # Game Over
                        podium = sorted(
                            [{"name": p["name"], "score": p["score"]} for p in room["players"].values()],
                            key=lambda x: x["score"],
                            reverse=True
                        )
                        fin_msg = {"type": "game_over", "podium": podium}
                        for p in room["players"].values():
                            if p["ws"] and not p["ws"].closed:
                                await p["ws"].send_json(fin_msg)
                        await ws.send_json(fin_msg)

    except Exception:
        pass
    finally:
        if current_room and current_room in ARENA_ROOMS:
            room = ARENA_ROOMS[current_room]
            if is_host:
                del ARENA_ROOMS[current_room]
            elif player_id and player_id in room["players"]:
                del room["players"][player_id]
    return ws
