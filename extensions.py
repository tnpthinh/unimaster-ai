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
    }
]

# 4 Clinical Case Scenarios for Virtual Patient Simulator
VIRTUAL_CASES = [
    {
        "id": "case_nephrotic",
        "title": "Ca 1: Bệnh nhân nam 45 tuổi phù toàn thân, tiểu bọt",
        "patient": "Nguyễn Văn H., 45 tuổi, thợ mộc",
        "chief_complaint": "Phù mi mắt sáng thức dậy, sau đó lan xuống hai chân kèm tiểu nhiều bọt 2 tuần nay.",
        "vitals": "Huyết áp: 135/85 mmHg | Mạch: 78 lần/phút | Thân nhiệt: 37.0°C | Cân nặng: 68 kg (tăng 5 kg trong 2 tuần)",
        "history": [
            {"label": "Tiền sử dùng thuốc", "content": "Không dùng thuốc giảm đau NSAIDs, không dùng thuốc nam thảo dược bắc."},
            {"label": "Triệu chứng đi kèm", "content": "Không sốt, không đau hông lưng, không tiểu buốt dắt, nước tiểu màu vàng trong nhưng có nhiều bọt lâu tan."},
            {"label": "Tiền sử gia đình", "content": "Chưa ghi nhận người thân mắc bệnh thận mạn."}
        ],
        "exam": [
            {"label": "Khám phù", "content": "Phù trắng, mềm, ấn lõm rõ ở hai cẳng chân và mu bàn chân. Phù đều hai bên, không đau."},
            {"label": "Khám tim mạch - hô hấp", "content": "Tim đều rõ, không âm thổi. Phổi rì rào phế nang êm dịu, không rale."},
            {"label": "Khám bụng", "content": "Bụng mềm, gõ đục vùng thấp nhẹ (nghi ngờ có ít dịch màng bụng cổ trướng)."}
        ],
        "lab_options": [
            {"id": "protein_24h", "name": "Định lượng Protein niệu 24 giờ", "result": "🔴 Protein nước tiểu 24h: 5.8 g/24 giờ (Rất cao, > 3.5 g/24h)"},
            {"id": "albumin_blood", "name": "Định lượng Albumin & Protein máu", "result": "🔴 Albumin máu: 21.0 g/L (Giảm nặng, < 30 g/L) | Protein toàn phần: 44.5 g/L"},
            {"id": "creatinine", "name": "Creatinin máu & eGFR", "result": "🟢 Creatinin máu: 88.0 µmol/L (1.0 mg/dL) | eGFR: 92 ml/phút/1.73m² (Bình thường)"},
            {"id": "lipid_panel", "name": "Bộ mỡ máu (Lipid panel)", "result": "🔴 Cholesterol toàn phần: 9.8 mmol/L | Triglycerid: 3.8 mmol/L | LDL-C: 6.2 mmol/L"},
            {"id": "urine_microscopy", "name": "Soi cặn lắng nước tiểu", "result": "Trụ mỡ (Fatty cast), thể mỡ lưỡng chiết quang (Maltese cross). Không thấy hồng cầu."}
        ],
        "diagnoses": [
            {"id": "d1", "text": "Hội chứng thận hư nguyên phát (Protein niệu > 3.5g/24h, Albumin máu < 30g/L, Phù, Tăng lipid máu)", "is_correct": True},
            {"id": "d2", "text": "Viêm cầu thận cấp sau nhiễm liên cầu khuẩn", "is_correct": False},
            {"id": "d3", "text": "Xơ gan mất bù cổ trướng", "is_correct": False},
            {"id": "d4", "text": "Suy tim ứ huyết sung huyết giai đoạn C", "is_correct": False}
        ],
        "treatment_steps": [
            "1. Corticosteroid liều tấn công: Prednisone 1 mg/kg/ngày (uống buổi sáng sau ăn)",
            "2. Kiểm soát phù: Thuốc lợi tiểu quai Furosemide phối hợp Spironolactone, chế độ ăn giảm muối (< 2g Natri/ngày)",
            "3. Giảm đạm niệu và bảo vệ thận: Thuốc ức chế men chuyển (ACEi) hoặc ức chế thụ thể (ARB)",
            "4. Kiểm soát rối loạn lipid máu: Statin (Atorvastatin 20mg/ngày)",
            "5. Chỉ định sinh thiết thận qua da để xác định thể mô bệnh học (Sang thương tối thiểu, Xơ chai cầu thận khu trú từng vùng FSGS hay Bệnh màng)"
        ]
    },
    {
        "id": "case_acute_gout",
        "title": "Ca 2: Bệnh nhân nam 52 tuổi sưng nóng đỏ đau dữ dội ngón chân cái",
        "patient": "Trần Văn T., 52 tuổi, giám đốc kinh doanh",
        "chief_complaint": "Thức giấc lúc nửa đêm vì đau buốt kinh hoàng ở khớp bàn ngón 1 chân phải sau bữa tiệc hải sản và uống rượu bia tối hôm trước.",
        "vitals": "Huyết áp: 145/90 mmHg | Mạch: 92 lần/phút | Thân nhiệt: 37.8°C | BMI: 28.5 (Tiền béo phì)",
        "history": [
            {"label": "Chế độ ăn & rượu bia", "content": "Thường xuyên tiếp khách, ăn thịt bò, lòng lợn và uống 5–6 cốc bia mỗi tuần."},
            {"label": "Tiền sử đau khớp", "content": "Cách đây 1 năm từng bị đau tương tự nhẹ hơn, tự mua thuốc giảm đau uống thì hết sau 3 ngày."},
            {"label": "Bệnh kèm theo", "content": "Tăng huyết áp 3 năm, đang uống Amlodipine 5mg."}
        ],
        "exam": [
            {"label": "Khám khớp bàn ngón 1 chân phải", "content": "Khớp sưng to, da căng bóng đỏ rực, nóng rát, đau dữ dội khi chạm nhẹ (thậm chí chạm vào ga giường cũng đau chói). Giới hạn vận động hoàn toàn."},
            {"label": "Tìm hạt Tophi", "content": "Chưa thấy hạt tophi rõ ở vành tai hay gân gót."},
            {"label": "Khám toàn thân", "content": "Hội chứng đáp ứng viêm toàn thân nhẹ, không phát ban ngoài da."}
        ],
        "lab_options": [
            {"id": "uric_acid", "name": "Định lượng Acid Uric máu", "result": "🔴 Acid Uric máu: 585 µmol/L (9.8 mg/dL - Tăng rất cao)"},
            {"id": "synovial_fluid", "name": "Chọc hút dịch khớp soi kính hiển vi phân cực", "result": "Tinh thể Monosodium Urat (MSU) hình kim nhọn lưỡng chiết quang âm tính mạnh nằm trong bạch cầu đa nhân."},
            {"id": "crp_esr", "name": "Chỉ số viêm CRP và máu lắng", "result": "🔴 CRP: 48 mg/L (Tăng cao) | Tốc độ máu lắng ESR: 55 mm/giờ"},
            {"id": "creatinine", "name": "Creatinin máu & chức năng thận", "result": "🟢 Creatinin máu: 92 µmol/L | eGFR: 82 ml/phút/1.73m²"}
        ],
        "diagnoses": [
            {"id": "d1", "text": "Cơn Gout cấp tính (Acute Gouty Arthritis) khớp bàn ngón chân cái", "is_correct": True},
            {"id": "d2", "text": "Viêm khớp nhiễm khuẩn cấp", "is_correct": False},
            {"id": "d3", "text": "Thoái hóa khớp ngón chân cái biến dạng", "is_correct": False},
            {"id": "d4", "text": "Viêm mô tế bào bàn chân do tụ cầu", "is_correct": False}
        ],
        "treatment_steps": [
            "1. Cắt cơn viêm cấp tính ngay: Colchicine 1mg uống liều đầu, sau đó 0.5mg sau 1 giờ (phác đồ liều thấp chuẩn EULAR/ACR)",
            "2. Phối hợp NSAID (Naproxen, Ibuprofen hoặc Celecoxib) nếu không có chống chỉ định loét dạ dày/suy thận",
            "3. LƯU Ý SỐNG CÒN: KHÔNG ĐƯỢC khởi trị thuốc hạ acid uric (Allopurinol / Febuxostat) trong lúc cơn Gout đang bùng phát cấp tính! (Chỉ bắt đầu hạ acid uric sau khi cơn đau khớp đã lắng xuống hoàn toàn 2–4 tuần).",
            "4. Bất động khớp, chườm lạnh tại chỗ, kiêng hoàn toàn rượu bia, phủ tạng động vật và hải sản."
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

        return web.Response(
            text=html_doc,
            content_type="application/msword",
            charset="utf-8",
            headers={"Content-Disposition": f'attachment; filename="De_Thi_{sub_name.replace(" ", "_")}.doc"'}
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
