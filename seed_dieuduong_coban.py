"""
Khởi tạo tự động Ngân hàng đề Điều Dưỡng Cơ Bản (10 Bài - 600 Câu chuẩn giáo trình)
- 10 bài x 60 câu/bài = 600 câu trắc nghiệm bám sát 100% nội dung sách giáo khoa (không hỏi ngoài bài, đáp án chống lộ).
- Tự động nạp idempotent khi khởi động server trên cả Local PC và Render Cloud.
"""
import json
import os
import database as db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_JSON_PATH = os.path.join(BASE_DIR, "seed", "dieuduong_coban_600.json")

SUBJECT_CODE = "DIEUDUONG_CB"
SUBJECT_NAME = "Điều Dưỡng Cơ Bản (10 Bài - 600 Câu)"
SUBJECT_ICON = "🩺"
SUBJECT_CATEGORY = "Y Dược & Lâm sàng"
SUBJECT_DESC = (
    "Trọn bộ 600 câu hỏi trắc nghiệm Điều Dưỡng Cơ Bản bám sát 100% nội dung giáo trình "
    "(10 bài × 60 câu/bài: Bài 7, 8, 9, 12, 14, 15, 19, 21, 23, 27 — đáp án nhiễu cao, không hỏi ngoài bài)."
)

DIEUDUONG_FLASHCARDS = [
    ("Bài 7: Các yếu tố ảnh hưởng đến thân nhiệt & Vị trí đo nhiệt độ chuẩn?", "Thân nhiệt trung tâm bình thường: **36,5°C – 37,5°C**. Đo ở trực tràng cao hơn nách ~0,5°C; đo ở miệng cao hơn nách ~0,2–0,3°C. Không đo nhiệt độ ở miệng cho trẻ nhỏ, người hôn mê, co giật hoặc mới ăn uống nóng/lạnh.", "Nhớ quy tắc chênh lệch: Trực tràng > Miệng > Nách"),
    ("Bài 7: Phân loại sốt theo mức nhiệt độ cơ thể?", "- **Sốt nhẹ:** 37,5°C – 38°C\n- **Sốt vừa:** > 38°C – 39°C\n- **Sốt cao:** > 39°C – 40°C\n- **Sốt rất cao (quá cao):** > 40°C", "Mốc 37,5 - 38 - 39 - 40°C"),
    ("Bài 8: Công thức tính lượng nước tiểu bình thường và phân loại Thiểu niệu / Vô niệu ở người lớn?", "- **Bình thường:** 1.000 – 1.500 mL/24h (trung bình ~1 mL/kg/giờ)\n- **Thiểu niệu:** < 400 mL/24h (hoặc < 0,5 mL/kg/giờ)\n- **Vô niệu:** < 100 mL/24h", "Thiểu niệu < 400 mL/24h; Vô niệu < 100 mL/24h"),
    ("Bài 8: Các vị trí đặt ống thông tiểu lưu và lượng nước cất bơm bóng chèn ở người lớn?", "Bơm **10 – 15 mL nước cất vô khuẩn** vào bóng chèn (không dùng NaCl 0,9% vì dễ kết tinh làm tắc van bóng). Cố định ống thông mặt trong đùi (nữ) hoặc bẹn/bụng dưới (nam), túi câu thấp hơn mặt giường.", "Chỉ bơm bóng chèn bằng nước cất vô khuẩn"),
    ("Bài 9: Quy trình 5 thời điểm vệ sinh tay của WHO & Thời gian rửa tay thường quy?", "**5 thời điểm:** (1) Trước khi chạm BN; (2) Trước thủ thuật vô khuẩn; (3) Sau nguy cơ phơi nhiễm dịch tiết; (4) Sau khi chạm BN; (5) Sau khi chạm vật dụng xung quanh BN.\n- Chà tay nhanh bằng cồn: **20 – 30 giây**\n- Rửa tay với xà phòng và nước: **40 – 60 giây**", "2 Trước - 3 Sau • Cồn 20-30s, Xà phòng 40-60s"),
    ("Bài 9: Thứ tự Mặc (Donning) và Tháo (Doffing) phương tiện phòng hộ cá nhân (PPE)?", "- **Mặc PPE:** Áo choàng → Khẩu trang → Kính/mặt nạ → Găng tay.\n- **Tháo PPE (từ bẩn nhất đến sạch nhất):** Găng tay → Kính/mặt nạ → Áo choàng → Khẩu trang → Vệ sinh tay ngay.", "Găng tay bẩn nhất nên mặc sau cùng và tháo đầu tiên"),
    ("Bài 12: Nguyên tắc an toàn và chiều dài đoạn ống thông dạ dày (Levin) cần đưa vào ở người lớn?", "**Đo chiều dài ống:** Từ **đỉnh mũi → dái tai → mũi ức** (hoặc từ trán → mũi → mũi ức), trung bình ở người lớn khoảng **45 – 55 cm**. Kiểm tra ống vào đúng dạ dày bằng cách hút dịch vị thử giấy quỳ hoặc bơm 10–20 mL khí nghe vùng thượng vị.", "Đỉnh mũi -> Dái tai -> Mũi ức (45-55 cm)"),
    ("Bài 12: Tư thế và nhiệt độ thức ăn khi cho bệnh nhân ăn qua ống thông dạ dày?", "- Nâng đầu giường cao **30° – 45° (Fowler thấp/bán Fowler)** trong khi ăn và giữ nguyên 30–60 phút sau ăn để chống trào ngược.\n- Nhiệt độ thức ăn ấm **37°C – 40°C**. Nếu dịch tồn lưu dạ dày > 100–200 mL phải báo bác sĩ.", "Đầu cao 30-45 độ • Nhiệt độ thức ăn 37-40°C"),
    ("Bài 14: Nguyên tắc thay băng rửa vết thương Sạch và vết thương Nhiễm khuẩn?", "- **Vết thương sạch (khâu kín):** Rửa từ **trong ra ngoài** (dọc theo đường khâu ra hai bên), cách mép vết thương ≥ 5 cm.\n- **Vết thương nhiễm khuẩn / hở có mủ:** Rửa từ **ngoài vào trong** (vùng sạch quanh vết thương trước, ổ mủ rửa sau cùng).", "Sạch: Trong ra ngoài • Nhiễm khuẩn: Ngoài vào trong"),
    ("Bài 14: Thứ tự ưu tiên khi thay băng cho nhiều vết thương trên cùng một người bệnh?", "Thay băng từ **vết thương vô khuẩn / sạch trước → vết thương sạch-nhiễm → vết thương nhiễm khuẩn / có mủ làm sau cùng**. Mỗi vết thương dùng bộ dụng cụ hoặc kẹp gắp vô khuẩn riêng.", "Vô khuẩn trước -> Nhiễm khuẩn sau"),
    ("Bài 15: Công thức tính lưu lượng Oxy ẩm (FiO2) qua gọng kính mũi (Cannula) và mặt nạ?", "**Công thức ước tính FiO2 qua gọng kính mũi:** $\\text{FiO}_2 (\\%) \\approx 20 + 4 \\times \\text{Lưu lượng (L/phút)}$ (tối đa 1 – 6 L/phút cho FiO2 ~24% – 44%). Nước làm ẩm dùng nước cất vô khuẩn đổ đến vạch quy định.", "FiO2 (%) = 20 + 4 × L/phút (Gọng mũi 1-6 L/p)"),
    ("Bài 15: Áp lực hút đờm nhớt đường hô hấp chuẩn theo lứa tuổi và thời gian mỗi lần hút?", "- **Áp lực hút (máy hút tường):** Người lớn **100 – 120 mmHg**; Trẻ em **80 – 100 mmHg**; Sơ sinh **60 – 80 mmHg**.\n- **Thời gian mỗi lần đưa ống hút:** Không quá **10 – 15 giây**, tăng oxy 100% trước và sau mỗi lần hút.", "Không hút quá 10-15 giây mỗi lần để tránh thiếu oxy"),
    ("Bài 19: 5 Đúng (5 Rights) kinh điển trong dùng thuốc và góc đâm kim của 4 đường tiêm?", "**5 Đúng:** Đúng người bệnh • Đúng thuốc • Đúng liều lượng • Đúng đường dùng • Đúng thời gian.\n**Góc tiêm:**\n- Tiêm trong da (ID): **10° – 15°**\n- Tiêm dưới da (SC): **45°** (hoặc 90° với kim ngắn)\n- Tiêm tĩnh mạch (IV): **15° – 30°**\n- Tiêm bắp (IM): **60° – 90°**", "ID: 10-15° • IV: 15-30° • SC: 45° • IM: 90°"),
    ("Bài 19: Vị trí tiêm bắp sâu an toàn tránh tổn thương dây thần kinh tọa (hông to)?", "Chia mông làm 4 phần: chọn **1/4 trên ngoài** (hoặc lấy **1/3 ngoài đường nối từ gai chậu trước trên đến mỏm xương cụt**). Tuyệt đối không tiêm thuốc dầu hoặc thuốc gây hoại tử mô vào tĩnh mạch.", "1/4 trên ngoài mông hoặc 1/3 ngoài đường gai chậu - xương cụt"),
    ("Bài 21: Công thức tính tốc độ truyền dịch (số giọt/phút) và Thời gian chảy hết dịch?", "$$\\text{Số giọt/phút} = \\frac{\\text{Tổng thể tích dịch (mL)} \\times \\text{Hệ số dây truyền (giọt/mL)}}{\\text{Tổng thời gian truyền (phút)}}$$\n(Hệ số dây truyền chuẩn thông thường: **20 giọt/mL**; dây truyền máu: **15 giọt/mL**; dây vi giọt trẻ em: **60 giọt/mL**).", "Giọt/phút = (V × Hệ số giọt) / Thời gian (phút)"),
    ("Bài 21: Quy tắc 15 phút đầu tiên (phản ứng sinh vật Oehlecker) khi truyền máu?", "Trong **15 phút đầu** truyền máu chậm (**15 – 20 giọt/phút**), điều dưỡng đứng tại giường theo dõi sát mạch, huyết áp, sắc mặt, đau lưng, rét run để phát hiện sớm bất đồng nhóm máu. Túi máu lấy khỏi tủ lạnh truyền trong vòng 30 phút và kết thúc < 4 giờ.", "15 phút đầu truyền chậm 15-20 giọt/phút tại giường"),
    ("Bài 23: Các giai đoạn tiến triển của Loét tỳ đè (Pressure Ulcer) và thời gian xoay trở?", "- **Độ I:** Đỏ da khu trú ấn không mất màu, da còn nguyên vẹn.\n- **Độ II:** Mất lớp thượng bì/trung bì nông (phỏng nước, vết trợt nông).\n- **Độ III:** Hoại tử toàn bộ chiều dày da tới mô mỡ dưới da.\n- **Độ IV:** Lan sâu tới cơ, gân, xương.\n**Dự phòng:** Xoay trở tối thiểu **2 giờ/lần**.", "Độ I đỏ da ấn không trắng • Xoay trở mỗi 2 giờ"),
    ("Bài 23: Các vị trí dễ bị loét tỳ đè nhất theo từng tư thế nằm?", "- **Nằm ngửa:** Vùng chẩm, gai sống bả vai, khuỷu tay, **vùng cùng cụt** (hay gặp nhất), gót chân.\n- **Nằm nghiêng:** Tai, mỏm cùng vai, mấu chuyển lớn xương đùi, mắt cá trong/ngoài.\n- **Nằm sấp:** Trán, cằm, đầu gối, ngón chân.", "Nằm ngửa: Cùng cụt & Gót chân • Nằm nghiêng: Mấu chuyển lớn"),
    ("Bài 27: Phác đồ C-A-B trong Hồi sức tim phổi cơ bản (BLS) người lớn?", "- **C (Compressions):** Ép tim ngoài lồng ngực ở **1/2 dưới xương ức**, tần số **100 – 120 lần/phút**, biên độ sâu **5 – 6 cm**, để lồng ngực nở lại hoàn toàn.\n- **A (Airway):** Ngửa đầu – nâng cằm (hoặc ấn hàm nếu nghi chấn thương cột sống cổ).\n- **B (Breathing):** Tỷ lệ ép tim : thổi ngạt là **30 : 2**.", "Tần số 100-120 l/p • Độ sâu 5-6 cm • Tỷ lệ 30:2"),
    ("Bài 27: Dấu hiệu nhận biết và xử trí đầu tiên khi Nạn nhân Ngừng tuần hoàn - hô hấp?", "**3 dấu hiệu vàng:** (1) Bất tỉnh (gọi hỏi không đáp ứng); (2) Ngừng thở hoặc thở ngáp cá; (3) Mất mạch cảnh (kiểm tra ≤ 10 giây).\n**Xử trí ngay:** Gọi hỗ trợ cấp cứu & tiến hành ép tim ngoài lồng ngực ngay lập tức trên nền phẳng cứng.", "Bất tỉnh + Ngừng thở + Mất mạch cảnh (kiểm tra <= 10s)"),
]


def ensure_dieuduong_coban_seeded(force_replace: bool = False) -> dict:
    if not os.path.exists(SEED_JSON_PATH):
        return {"seeded": False, "reason": "seed json missing"}

    with open(SEED_JSON_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    if not isinstance(questions, list) or not questions:
        return {"seeded": False, "reason": "empty seed json"}

    conn = db.get_connection()
    try:
        cur = conn.cursor()
        row = cur.execute("SELECT id FROM subjects WHERE code = ?", (SUBJECT_CODE,)).fetchone()
        if row:
            sid = row[0]
            cur.execute(
                "UPDATE subjects SET name = ?, icon = ?, category = ?, description = ? WHERE id = ?",
                (SUBJECT_NAME, SUBJECT_ICON, SUBJECT_CATEGORY, SUBJECT_DESC, sid),
            )
        else:
            cur.execute(
                "INSERT INTO subjects (code, name, icon, category, description) VALUES (?, ?, ?, ?, ?)",
                (SUBJECT_CODE, SUBJECT_NAME, SUBJECT_ICON, SUBJECT_CATEGORY, SUBJECT_DESC),
            )
            sid = cur.lastrowid

        existing_cnt = cur.execute(
            "SELECT COUNT(*) FROM questions WHERE subject_id = ?", (sid,)
        ).fetchone()[0]

        if force_replace or existing_cnt < len(questions):
            cur.execute("DELETE FROM questions WHERE subject_id = ?", (sid,))
            for q in questions:
                cur.execute(
                    """
                    INSERT INTO questions (
                        subject_id, question_text, code_snippet, image_url, q_type,
                        option_a, option_b, option_c, option_d,
                        correct_option, explanation, difficulty, topic_tag
                    ) VALUES (?, ?, '', '', 'mcq', ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sid,
                        str(q.get("question_text", "")).strip(),
                        str(q.get("option_a", "")).strip(),
                        str(q.get("option_b", "")).strip(),
                        str(q.get("option_c", "")).strip(),
                        str(q.get("option_d", "")).strip(),
                        str(q.get("correct_option", "A")).strip().upper(),
                        str(q.get("explanation", "")).strip(),
                        str(q.get("difficulty", "medium")).strip().lower(),
                        str(q.get("topic_tag", "")).strip(),
                    ),
                )
            replaced_q = True
        else:
            replaced_q = False

        fc_cnt = cur.execute("SELECT COUNT(*) FROM flashcards WHERE subject_id = ?", (sid,)).fetchone()[0]
        if force_replace or fc_cnt < len(DIEUDUONG_FLASHCARDS):
            cur.execute("DELETE FROM flashcards WHERE subject_id = ?", (sid,))
            for front, back, hint in DIEUDUONG_FLASHCARDS:
                cur.execute(
                    "INSERT INTO flashcards (subject_id, front, back, hint, interval_days) VALUES (?, ?, ?, ?, 1)",
                    (sid, front, back, hint),
                )

        conn.commit()
        return {"seeded": True, "subject_id": sid, "count": len(questions) if replaced_q else existing_cnt, "replaced": replaced_q}
    finally:
        conn.close()


if __name__ == "__main__":
    print(ensure_dieuduong_coban_seeded(force_replace=True))
