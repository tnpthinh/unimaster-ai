r"""
UniMaster AI v7.0 — STEM Multi-Subject Migration & Formula Seeder
1. Upgrades existing MATH101 questions & flashcards to crisp KaTeX LaTeX notation.
2. Non-destructively seeds 3 comprehensive STEM subjects:
   - CHEM101: Hóa học Đại cương & Hữu cơ (with mhchem \ce{...} chemical equations)
   - PHYS101: Vật lý Đại cương — Cơ Nhiệt Điện Quang (with physics LaTeX equations)
   - BIO101: Sinh học Phân tử & Di truyền học (with genetics & biochemical formulas)
"""
import sqlite3
from datetime import date
import database as db


def ensure_stem_and_math_upgraded():
    conn = db.get_connection()
    c = conn.cursor()
    today_str = date.today().isoformat()

    # 1. Upgrade legacy ASCII math formulas in MATH101 (subject_id = 3) if still raw
    c.execute("SELECT id, question_text, option_b FROM questions WHERE subject_id = 3 ORDER BY id ASC")
    math_rows = c.fetchall()
    for row in math_rows:
        qid = row["id"]
        qtxt = row["question_text"]
        if "det(A) = 3" in qtxt and "$" not in qtxt:
            c.execute("""
                UPDATE questions
                SET question_text = ?,
                    option_a = ?, option_b = ?, option_c = ?, option_d = ?,
                    explanation = ?, difficulty = 'medium'
                WHERE id = ?
            """, (
                r"Câu 1 (Thông hiểu - Định thức ma trận): Nếu ma trận vuông $A$ cấp $n$ có định thức $\det(A) = 3$, thì $\det(2A)$ bằng bao nhiêu?",
                r"$6$",
                r"$3 \cdot 2^n$",
                r"$6^n$",
                r"$2 \cdot 3^n$",
                r"Theo tính chất định thức của ma trận vuông cấp $n$: $\det(kA) = k^n \cdot \det(A)$. Thay $k = 2$ và $\det(A) = 3$, ta được $\det(2A) = 2^n \cdot 3 = 3 \cdot 2^n$.",
                qid
            ))
        elif "AX = 0" in qtxt and "$" not in qtxt:
            c.execute("""
                UPDATE questions
                SET question_text = ?,
                    option_a = ?, option_b = ?, option_c = ?, option_d = ?,
                    explanation = ?, difficulty = 'medium'
                WHERE id = ?
            """, (
                r"Câu 2 (Thông hiểu - Hệ tuyến tính): Điều kiện cần và đủ để hệ phương trình tuyến tính thuần nhất $A X = \mathbf{0}$ (với $A$ là ma trận vuông cấp $n$) có nghiệm không tầm thường là gì?",
                r"$\det(A) \neq 0$",
                r"$\mathrm{rank}(A) = n$",
                r"$\det(A) = 0$ (tức $\mathrm{rank}(A) < n$)",
                r"$A = I_n$ (ma trận đơn vị)",
                r"Hệ thuần nhất $AX = \mathbf{0}$ luôn có nghiệm tầm thường $X = \mathbf{0}$. Để tồn tại nghiệm không tầm thường ($X \neq \mathbf{0}$), ma trận $A$ phải suy biến: $\det(A) = 0 \iff \mathrm{rank}(A) < n$.",
                qid
            ))
        elif "e^x" in qtxt:
            c.execute("""
                UPDATE questions
                SET question_text = ?,
                    option_a = ?, option_b = ?, option_c = ?, option_d = ?,
                    explanation = ?, difficulty = 'hard'
                WHERE id = ?
            """, (
                r"Câu 3 (Vận dụng - Tích phân từng phần): Tính tích phân bất định $I = \int x \cdot e^x \, \mathrm{d}x$:",
                r"$e^x (x - 1) + C$",
                r"$e^x (x + 1) + C$",
                r"$\frac{x^2}{2} e^x + C$",
                r"$x e^x - x + C$",
                r"Đặt $u = x \Rightarrow \mathrm{d}u = \mathrm{d}x$ và $\mathrm{d}v = e^x \mathrm{d}x \Rightarrow v = e^x$. Áp dụng $\int u\,\mathrm{d}v = uv - \int v\,\mathrm{d}u = x e^x - \int e^x\,\mathrm{d}x = e^x(x - 1) + C$.",
                qid
            ))

    # Add extra rich Calculus/Linear Algebra questions to MATH101 if count < 6
    c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = 3")
    if c.fetchone()[0] < 6:
        extra_math = [
            (
                "mcq",
                r"Câu 4 (Nhận biết - Giới hạn cơ bản): Giá trị của giới hạn $\lim_{x \to 0} \frac{\sin(3x)}{x}$ bằng bao nhiêu?",
                r"$0$", r"$1$", r"$3$", r"$\frac{1}{3}$", "C",
                r"Áp dụng giới hạn lượng giác cơ bản $\lim_{u \to 0} \frac{\sin u}{u} = 1$: ta biến đổi $\lim_{x \to 0} 3 \cdot \frac{\sin(3x)}{3x} = 3 \cdot 1 = 3$.",
                "easy"
            ),
            (
                "mcq",
                r"Câu 5 (Vận dụng - Đạo hàm riêng): Cho hàm hai biến $f(x, y) = x^3 y^2 - 4xy + 5$. Đạo hàm riêng cấp một $\frac{\partial f}{\partial x}$ tại điểm $(1, 2)$ bằng:",
                r"$4$", r"$12$", r"$8$", r"$0$", "A",
                r"Coi $y$ là hằng số: $\frac{\partial f}{\partial x} = 3x^2 y^2 - 4y$. Thay $(x, y) = (1, 2)$: $\frac{\partial f}{\partial x}(1, 2) = 3(1)^2(2)^2 - 4(2) = 12 - 8 = 4$.",
                "hard"
            ),
            (
                "mcq",
                r"Câu 6 (Vận dụng cao - Giá trị riêng): Tổng các giá trị riêng ($\lambda_1 + \lambda_2$) của ma trận $A = \begin{pmatrix} 5 & -2 \\ 1 & 2 \end{pmatrix}$ bằng bao nhiêu?",
                r"$7$", r"$12$", r"$8$", r"$3$", "A",
                r"Tổng các giá trị riêng của ma trận vuông luôn bằng vết của ma trận ($\mathrm{tr}(A) = a_{11} + a_{22}$). Do đó $\lambda_1 + \lambda_2 = 5 + 2 = 7$ (không cần giải phương trình đặc trưng!).",
                "very_hard"
            ),
            (
                "short_answer",
                r"Câu 7 (Vận dụng - Tích phân xác định): Tính giá trị số của tích phân $I = \int_{0}^{1} (3x^2 + 2x) \, \mathrm{d}x$:",
                "2", "", "", "", "2",
                r"Nguyên hàm là $F(x) = x^3 + x^2$. Thế cận từ $0$ đến $1$: $F(1) - F(0) = (1 + 1) - 0 = 2$.",
                "hard"
            ),
        ]
        for qt, qtext, oa, ob, oc, od, corr, expl, diff in extra_math:
            c.execute("""
                INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty)
                VALUES (3, ?, ?, '', ?, ?, ?, ?, ?, ?, ?)
            """, (qt, qtext, oa, ob, oc, od, corr, expl, diff))

        c.execute("DELETE FROM flashcards WHERE subject_id = 3")
        math_fcs = [
            (r"Điều kiện nhân hai ma trận $A_{m \times k} \cdot B_{k \times n}$", r"Số cột của ma trận $A$ phải bằng số dòng của ma trận $B$. Ma trận tích $C = AB$ có kích thước $m \times n$.", "Cột trước = Dòng sau"),
            (r"Công thức Tích phân từng phần", r"$$\int u \, \mathrm{d}v = u \cdot v - \int v \, \mathrm{d}u$$ Thứ tự ưu tiên đặt $u$: **Nhất lô ($\ln x$) – Nhì đa ($P(x)$) – Tam lượng ($\sin, \cos$) – Tứ mũ ($e^x$)**.", "Nhất lô - Nhì đa - Tam lượng - Tứ mũ"),
            (r"Tính chất Vết & Định thức theo Giá trị riêng $\lambda_i$", r"- Tổng các giá trị riêng: $\sum_{i=1}^n \lambda_i = \mathrm{tr}(A)$\n- Tích các giá trị riêng: $\prod_{i=1}^n \lambda_i = \det(A)$", "Tổng = Vết (Trace) | Tích = Định thức"),
        ]
        for fr, bk, hn in math_fcs:
            c.execute("INSERT INTO flashcards (subject_id, front, back, hint, repetitions, interval_days, ease_factor, next_review) VALUES (3, ?, ?, ?, 0, 1, 2.5, ?)", (fr, bk, hn, today_str))

    conn.commit()

    existing_codes = {r["code"] for r in c.execute("SELECT code FROM subjects").fetchall()}

    # =========================================================================
    # 2. HÓA HỌC ĐẠI CƯƠNG & HỮU CƠ (CHEM101)
    # =========================================================================
    if "CHEM101" not in existing_codes:
        c.execute("""
            INSERT INTO subjects (code, name, icon, category, description)
            VALUES ('CHEM101', 'Hóa học Đại cương & Hữu cơ', '⚗️', 'Khoa học tự nhiên',
                    'Cân bằng hóa học, pH dung dịch, nhiệt động học, điện hóa, phản ứng vô cơ & hữu cơ hiển thị chuẩn phương trình hóa học.')
        """)
        chem_id = c.lastrowid
        chem_questions = [
            (
                "mcq",
                r"Câu 1 (Nhận biết - Tính pH dung dịch): Dung dịch axit mạnh $\ce{H2SO4}$ có nồng độ $0,005\text{ M}$ (coi phân li hoàn toàn cả 2 nấc: $\ce{H2SO4 -> 2H+ + SO4^{2-}}$) có giá trị $\text{pH}$ bằng bao nhiêu?",
                r"$\text{pH} = 2$",
                r"$\text{pH} = 2,3$",
                r"$\text{pH} = 3$",
                r"$\text{pH} = 1,7$",
                "A",
                r"Ta có $[\ce{H+}] = 2 \cdot C_{\ce{H2SO4}} = 2 \cdot 0,005 = 0,01 = 10^{-2}\text{ M}$. Suy ra $\text{pH} = -\log[\ce{H+}] = -\log(10^{-2}) = 2$.",
                "easy"
            ),
            (
                "mcq",
                r"Câu 2 (Thông hiểu - Chuyển dịch cân bằng Le Chatelier): Cho cân bằng tổng hợp amoniac tỏa nhiệt: $$\ce{N2(g) + 3H2(g) <=> 2NH3(g)} \quad (\Delta H^\circ < 0)$$ Biện pháp nào sau đây làm cân bằng chuyển dịch theo chiều thuận (tạo thêm $\ce{NH3}$)?",
                r"Tăng nhiệt độ và giảm áp suất chung của hệ",
                r"Hạ nhiệt độ vừa phải và tăng áp suất chung của hệ",
                r"Thêm chất xúc tác bột $\ce{Fe}$ để tăng hiệu suất cực đại",
                r"Giảm nồng độ khí $\ce{H2}$ trong bình phản ứng",
                "B",
                r"Chiều thuận có $\Delta n_{\text{khí}} = 2 - (1 + 3) = -2 < 0$ (giảm số mol khí) và $\Delta H^\circ < 0$ (tỏa nhiệt). Theo nguyên lý Le Chatelier, **tăng áp suất** và **hạ nhiệt độ** giúp cân bằng dịch chuyển theo chiều thuận. (Xúc tác chỉ làm tăng tốc độ đạt cân bằng, không làm dịch chuyển cân bằng).",
                "medium"
            ),
            (
                "mcq",
                r"Câu 3 (Thông hiểu - Phản ứng Oxi hóa - Khử): Trong phản ứng $\ce{Cu + 4HNO3(\text{đặc, nóng}) -> Cu(NO3)2 + 2NO2 ^ + 2H2O}$, vai trò của $\ce{HNO3}$ là gì?",
                r"Chỉ đóng vai trò chất oxi hóa",
                r"Chỉ đóng vai trò môi trường tạo muối",
                r"Vừa là chất oxi hóa (tạo $\ce{NO2}$), vừa là môi trường (tạo muối $\ce{Cu(NO3)2}$)",
                r"Là chất khử nhường electron",
                "C",
                r"Trong $4$ phân tử $\ce{HNO3}$: có $2$ gốc $\ce{NO3-}$ nhận electron giảm số oxi hóa từ $\overset{+5}{\text{N}} \to \overset{+4}{\text{N}}$ ($\ce{NO2}$) đóng vai trò **chất oxi hóa**, và $2$ gốc $\ce{NO3-}$ giữ nguyên số oxi hóa kết hợp với $\ce{Cu^{2+}}$ tạo muối đóng vai trò **môi trường**.",
                "medium"
            ),
            (
                "mcq",
                r"Câu 4 (Vận dụng - Nhiệt động hóa học): Một phản ứng có $\Delta H^\circ = -92\text{ kJ/mol}$ và $\Delta S^\circ = -200\text{ J/(mol}\cdot\text{K)}$. Tại nhiệt độ $T = 300\text{ K}$, biến thiên năng lượng tự do Gibbs $\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ$ bằng bao nhiêu?",
                r"$-32\text{ kJ/mol}$ (phản ứng tự diễn biến)",
                r"$+32\text{ kJ/mol}$ (phản ứng không tự diễn biến)",
                r"$-152\text{ kJ/mol}$",
                r"$+59908\text{ kJ/mol}$",
                "A",
                r"Đổi đơn vị đồng nhất về $\text{kJ}$: $\Delta S^\circ = -0,2\text{ kJ/(mol}\cdot\text{K)}$. Khi đó: $$\Delta G^\circ = -92 - 300 \times (-0,2) = -92 + 60 = -32\text{ kJ/mol} < 0$$ Vì $\Delta G^\circ < 0$ nên phản ứng tự xảy ra ở $300\text{ K}$! (Bẫy kinh điển là quên đổi $\text{J}$ sang $\text{kJ}$).",
                "hard"
            ),
            (
                "mcq",
                r"Câu 5 (Thông hiểu - Hóa hữu cơ Este): Thủy phân hoàn toàn etyl axetat ($\ce{CH3COOC2H5}$) trong dung dịch $\ce{NaOH}$ đun nóng thu được sản phẩm nào?",
                r"$\ce{CH3COOH}$ và $\ce{C2H5OH}$",
                r"$\ce{CH3COONa}$ và $\ce{C2H5OH}$",
                r"$\ce{C2H5COONa}$ và $\ce{CH3OH}$",
                r"$\ce{HCOONa}$ và $\ce{C3H7OH}$",
                "B",
                r"Phương trình xà phòng hóa (một chiều): $$\ce{CH3COOC2H5 + NaOH ->[t^\circ] CH3COONa + C2H5OH}$$ thu được muối natri axetat và ancol etylic.",
                "easy"
            ),
            (
                "mcq",
                r"Câu 6 (Vận dụng cao - Điện hóa): Cho thế điện cực chuẩn $E^\circ_{\ce{Zn^{2+}/Zn}} = -0,76\text{ V}$ và $E^\circ_{\ce{Cu^{2+}/Cu}} = +0,34\text{ V}$. Suất điện động chuẩn $E^\circ_{\text{pin}}$ của pin Galvani $\ce{Zn - Cu}$ là:",
                r"$1,10\text{ V}$",
                r"$0,42\text{ V}$",
                r"$-1,10\text{ V}$",
                r"$0,76\text{ V}$",
                "A",
                r"Cực dương (Catot) là cặp có thế khử lớn hơn ($\ce{Cu^{2+}/Cu}$), cực âm (Anot) là $\ce{Zn^{2+}/Zn}$. Công thức: $$E^\circ_{\text{pin}} = E^\circ_{\text{catot}} - E^\circ_{\text{anot}} = 0,34 - (-0,76) = 1,10\text{ V}$$",
                "very_hard"
            ),
            (
                "true_false",
                r"Câu 7 (Nhận biết - Lưỡng tính): Nhận định Đúng hay Sai: Nhôm hiđroxit $\ce{Al(OH)3}$ và natri hiđrocacbonat $\ce{NaHCO3}$ đều là các chất có tính lưỡng tính (tác dụng được với cả dung dịch $\ce{HCl}$ và $\ce{NaOH}$).",
                "Đúng", "Sai", "", "", "A",
                r"Đúng! $\ce{Al(OH)3}$ tan trong $\ce{HCl}$ tạo $\ce{AlCl3}$ và tan trong $\ce{NaOH}$ tạo $\ce{Na[Al(OH)4]}$. Tương tự, ion $\ce{HCO3-}$ vừa nhận $\ce{H+}$ tạo $\ce{CO2 ^ + H2O}$, vừa nhường $\ce{H+}$ cho $\ce{OH-}$ tạo $\ce{CO3^{2-}}$.",
                "easy"
            ),
            (
                "short_answer",
                r"Câu 8 (Vận dụng - Bảo toàn electron): Hòa tan hoàn toàn $5,6\text{ gam}$ sắt ($\ce{Fe}$, $M = 56$) trong dung dịch $\ce{HCl}$ dư: $\ce{Fe + 2HCl -> FeCl2 + H2 ^}$. Thể tích khí $\ce{H2}$ thu được ở đktc ($22,4\text{ L/mol}$) bằng bao nhiêu lít?",
                "2.24", "", "", "", "2.24",
                r"Số mol sắt: $n_{\ce{Fe}} = \frac{5,6}{56} = 0,1\text{ mol}$. Theo phương trình: $n_{\ce{H2}} = n_{\ce{Fe}} = 0,1\text{ mol} \Rightarrow V_{\ce{H2}} = 0,1 \times 22,4 = 2,24\text{ L}$.",
                "hard"
            ),
            (
                "essay",
                r"Câu 9 (Tự luận Hóa học): Trình bày hiện tượng và viết phương trình phân tử, phương trình ion rút gọn khi nhỏ từ từ dung dịch $\ce{NaOH}$ đến dư vào dung dịch $\ce{AlCl3}$.",
                "", "", "", "",
                r"Hiện tượng: Ban đầu xuất hiện kết tủa keo trắng Al(OH)3 tăng dần đến cực đại, sau đó kết tủa tan dần tạo dung dịch trong suốt Na[Al(OH)4]. Phương trình ion: Al3+ + 3OH- -> Al(OH)3 và Al(OH)3 + OH- -> [Al(OH)4]-.",
                r"1) **Giai đoạn 1:** Xuất hiện kết tủa keo trắng tăng dần: $\ce{Al^{3+} + 3OH- -> Al(OH)3 v}$.\n2) **Giai đoạn 2 ($\ce{NaOH}$ dư):** Kết tủa keo trắng tan dần đến hết tạo dung dịch không màu: $\ce{Al(OH)3 + OH- -> [Al(OH)4]-}$.",
                "hard"
            ),
        ]
        for qt, qtext, oa, ob, oc, od, corr, expl, diff in chem_questions:
            c.execute("""
                INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty)
                VALUES (?, ?, ?, '', ?, ?, ?, ?, ?, ?, ?)
            """, (chem_id, qt, qtext, oa, ob, oc, od, corr, expl, diff))

        chem_fcs = [
            (r"Công thức Năng lượng tự do Gibbs ($\Delta G^\circ$)", r"$$\Delta G^\circ = \Delta H^\circ - T\Delta S^\circ = -RT\ln K$$ - $\Delta G < 0$: Phản ứng tự xảy ra.\n- $\Delta G > 0$: Không tự xảy ra.\n- $\Delta G = 0$: Hệ đạt trạng thái cân bằng.", "Nhớ đổi ΔS từ J sang kJ!"),
            (r"Dãy điện hóa của kim loại (Mẹo nhớ 5 giây)", r"**Khi Nào Ba Cần May Áo Giáp Sắt Nhớ Sang Phố Hỏi Cửa Hàng Á Phi Âu**\n$$\ce{K, Na, Ba, Ca, Mg, Al, Zn, Fe, Ni, Sn, Pb, (H), Cu, Hg, Ag, Pt, Au}$$ Quy tắc $\alpha$: Chất oxi hóa mạnh + Chất khử mạnh $\to$ Oxi hóa yếu hơn + Khử yếu hơn.", "Quy tắc Alpha (α)"),
            (r"Công thức tính $\text{pH}$ & Tích số ion của nước", r"Ở $25^\circ\text{C}$: $K_w = [\ce{H+}][\ce{OH-}] = 10^{-14}$$\text{pH} = -\log[\ce{H+}], \quad \text{pOH} = -\log[\ce{OH-}], \quad \text{pH} + \text{pOH} = 14$", "pH + pOH = 14"),
        ]
        for fr, bk, hn in chem_fcs:
            c.execute("INSERT INTO flashcards (subject_id, front, back, hint, repetitions, interval_days, ease_factor, next_review) VALUES (?, ?, ?, ?, 0, 1, 2.5, ?)", (chem_id, fr, bk, hn, today_str))

    # =========================================================================
    # 3. VẬT LÝ ĐẠI CƯƠNG — CƠ NHIỆT ĐIỆN QUANG (PHYS101)
    # =========================================================================
    if "PHYS101" not in existing_codes:
        c.execute("""
            INSERT INTO subjects (code, name, icon, category, description)
            VALUES ('PHYS101', 'Vật lý Đại cương (Cơ • Nhiệt • Điện • Quang)', '⚛️', 'Khoa học tự nhiên',
                    'Dao động & sóng cơ, nhiệt động lực học, điện từ trường Maxwell-Faraday, mạch xoay chiều RLC và vật lý lượng tử.')
        """)
        phys_id = c.lastrowid
        phys_questions = [
            (
                "mcq",
                r"Câu 1 (Nhận biết - Dao động điều hòa): Một chất điểm dao động điều hòa theo phương trình $x = 6\cos(4\pi t + \frac{\pi}{3})\text{ (cm)}$. Tốc độ cực đại $v_{\max}$ của chất điểm là:",
                r"$24\pi\text{ cm/s}$",
                r"$1,5\pi\text{ cm/s}$",
                r"$96\pi^2\text{ cm/s}$",
                r"$12\pi\text{ cm/s}$",
                "A",
                r"Từ phương trình $x = A\cos(\omega t + \varphi)$, ta có biên độ $A = 6\text{ cm}$ và tần số góc $\omega = 4\pi\text{ rad/s}$. Tốc độ cực đại khi qua vị trí cân bằng: $v_{\max} = \omega A = 4\pi \times 6 = 24\pi\text{ cm/s}$.",
                "easy"
            ),
            (
                "mcq",
                r"Câu 2 (Thông hiểu - Mạch điện xoay chiều RLC): Cho đoạn mạch $RLC$ mắc nối tiếp có điện trở $R = 30\,\Omega$, cảm kháng $Z_L = 60\,\Omega$ và dung kháng $Z_C = 20\,\Omega$. Tổng trở $Z$ của đoạn mạch bằng:",
                r"$50\,\Omega$",
                r"$70\,\Omega$",
                r"$110\,\Omega$",
                r"$10\,\Omega$",
                "A",
                r"Áp dụng công thức tổng trở mạch $RLC$ nối tiếp: $$Z = \sqrt{R^2 + (Z_L - Z_C)^2} = \sqrt{30^2 + (60 - 20)^2} = \sqrt{900 + 1600} = 50\,\Omega$$",
                "medium"
            ),
            (
                "mcq",
                r"Câu 3 (Thông hiểu - Cảm ứng điện từ Faraday): Theo định luật Faraday - Lenz, biểu thức suất điện động cảm ứng $\mathcal{E}_c$ xuất hiện trong khung dây kín có từ thông $\Phi$ biến thiên là:",
                r"$\mathcal{E}_c = -\frac{\mathrm{d}\Phi}{\mathrm{d}t}$",
                r"$\mathcal{E}_c = B \cdot I \cdot \ell \sin\alpha$",
                r"$\mathcal{E}_c = \frac{1}{2} L I^2$",
                r"$\mathcal{E}_c = q \cdot E$",
                "A",
                r"Định luật Faraday: Độ lớn suất điện động cảm ứng tỉ lệ với tốc độ biến thiên từ thông, dấu trừ $(-)$ thể hiện định luật Lenz (dòng điện cảm ứng chống lại nguyên nhân sinh ra nó): $\mathcal{E}_c = -\frac{\mathrm{d}\Phi}{\mathrm{d}t}$.",
                "easy"
            ),
            (
                "mcq",
                r"Câu 4 (Vận dụng - Lượng tử ánh sáng): Giới hạn quang điện của kim loại đồng là $\lambda_0 = 0,30\,\mu\text{m}$. Chiếu bức xạ nào sau đây vào tấm đồng sẽ gây ra **hiện tượng quang điện ngoài**?",
                r"Tia tử ngoại có bước sóng $\lambda = 0,25\,\mu\text{m}$",
                r"Ánh sáng tím có bước sóng $\lambda = 0,40\,\mu\text{m}$",
                r"Ánh sáng lục có bước sóng $\lambda = 0,55\,\mu\text{m}$",
                r"Tia hồng ngoại có bước sóng $\lambda = 0,90\,\mu\text{m}$",
                "A",
                r"Điều kiện xảy ra hiện tượng quang điện ngoài là bước sóng ánh sáng kích thích phải nhỏ hơn hoặc bằng giới hạn quang điện: $\lambda \le \lambda_0 = 0,30\,\mu\text{m}$. Chỉ có $\lambda = 0,25\,\mu\text{m}$ thỏa mãn!",
                "hard"
            ),
            (
                "mcq",
                r"Câu 5 (Vận dụng cao - Thuyết tương đối hẹp Einstein): Một hạt chuyển động với tốc độ $v = 0,6c$ (với $c$ là tốc độ ánh sáng trong chân không). Tỉ số giữa khối lượng tương đối tính $m$ và khối lượng nghỉ $m_0$ của hạt là:",
                r"$1,25$",
                r"$0,80$",
                r"$1,67$",
                r"$0,64$",
                "A",
                r"Theo hệ thức tương đối tính Einstein: $$m = \frac{m_0}{\sqrt{1 - \frac{v^2}{c^2}}} \implies \frac{m}{m_0} = \frac{1}{\sqrt{1 - 0,6^2}} = \frac{1}{\sqrt{0,64}} = \frac{1}{0,8} = 1,25$$",
                "very_hard"
            ),
            (
                "true_false",
                r"Câu 6 (Thông hiểu - Cộng hưởng điện): Nhận định Đúng hay Sai: Khi mạch $RLC$ nối tiếp xảy ra cộng hưởng điện ($\omega = \frac{1}{\sqrt{LC}}$), hệ số công suất $\cos\varphi = 1$ và điện áp hai đầu mạch cùng pha với dòng điện.",
                "Đúng", "Sai", "", "", "A",
                r"Đúng! Khi $Z_L = Z_C \iff \omega = \frac{1}{\sqrt{LC}}$, ta có $\tan\varphi = \frac{Z_L - Z_C}{R} = 0 \Rightarrow \varphi = 0 \Rightarrow \cos\varphi = 1$, cường độ dòng điện đạt cực đại $I_{\max} = \frac{U}{R}$.",
                "medium"
            ),
            (
                "short_answer",
                r"Câu 7 (Vận dụng - Con lắc đơn): Tại nơi có gia tốc trọng trường $g = \pi^2 \approx 9,87\text{ m/s}^2$, một con lắc đơn có chiều dài $\ell = 1\text{ m}$ dao động điều hòa với chu kỳ $T = 2\pi\sqrt{\frac{\ell}{g}}$ bằng bao nhiêu giây?",
                "2", "", "", "", "2",
                r"Thay $\ell = 1\text{ m}$ và $\sqrt{g} = \pi$ vào công thức $T = 2\pi\sqrt{\frac{1}{\pi^2}} = 2\pi \cdot \frac{1}{\pi} = 2\text{ (s)}$.",
                "medium"
            ),
            (
                "essay",
                r"Câu 8 (Tự luận Vật lý): Phát biểu Nguyên lý I Nhiệt động lực học ($\Delta U = A + Q$), quy ước dấu của $A, Q$ và giải thích vì sao không thể chế tạo động cơ vĩnh cửu loại I.",
                "", "", "", "",
                r"Độ biến thiên nội năng ΔU = A + Q. Q > 0 nhận nhiệt, Q < 0 tỏa nhiệt; A > 0 nhận công, A < 0 sinh công. Động cơ vĩnh cửu loại I sinh công liên tục (A' > 0) mà không nhận năng lượng (Q = 0, ΔU = 0) vi phạm định luật bảo toàn năng lượng.",
                r"1) **Biểu thức:** $\Delta U = A + Q$ (Độ biến thiên nội năng bằng tổng công và nhiệt lượng hệ nhận được).\n2) **Quy ước dấu:** $Q > 0$ (nhận nhiệt), $Q < 0$ (truyền nhiệt); $A > 0$ (nhận công), $A < 0$ (thực hiện công).\n3) Chu trình kín có $\Delta U = 0 \Rightarrow Q = -A = A'$, nghĩa là muốn sinh công $A' > 0$ bắt buộc phải nhận nhiệt $Q > 0$ — không thể sinh công từ hư không.",
                "hard"
            ),
        ]
        for qt, qtext, oa, ob, oc, od, corr, expl, diff in phys_questions:
            c.execute("""
                INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty)
                VALUES (?, ?, ?, '', ?, ?, ?, ?, ?, ?, ?)
            """, (phys_id, qt, qtext, oa, ob, oc, od, corr, expl, diff))

        phys_fcs = [
            (r"Hệ thức độc lập thời gian trong Dao động điều hòa", r"$$A^2 = x^2 + \frac{v^2}{\omega^2}, \qquad \frac{v^2}{v_{\max}^2} + \frac{a^2}{a_{\max}^2} = 1$$ Với $v_{\max} = \omega A$ và $a_{\max} = \omega^2 A$.", "Vuông pha: tổng bình phương tỉ số = 1"),
            (r"Cộng hưởng mạch xoay chiều $RLC$ nối tiếp", r"Điều kiện: $Z_L = Z_C \iff \omega_0 = \frac{1}{\sqrt{LC}}$\nHệ quả: $Z_{\min} = R$, $I_{\max} = \frac{U}{R}$, $\cos\varphi = 1$, $P_{\max} = \frac{U^2}{R}$.", "ZL = ZC -> cos φ = 1"),
            (r"Công thức Anh-xtanh về Hiện tượng Quang điện", r"$$\varepsilon = h f = \frac{hc}{\lambda} = A + \frac{1}{2} m v_{0\max}^2$$ Trong đó $h = 6,625 \times 10^{-34}\text{ J}\cdot\text{s}$, $c = 3 \times 10^8\text{ m/s}$, $A = \frac{hc}{\lambda_0}$.", "Năng lượng photon = Công thoát + Động năng cực đại"),
        ]
        for fr, bk, hn in phys_fcs:
            c.execute("INSERT INTO flashcards (subject_id, front, back, hint, repetitions, interval_days, ease_factor, next_review) VALUES (?, ?, ?, ?, 0, 1, 2.5, ?)", (phys_id, fr, bk, hn, today_str))

    # =========================================================================
    # 4. SINH HỌC PHÂN TỬ & DI TRUYỀN HỌC (BIO101)
    # =========================================================================
    if "BIO101" not in existing_codes:
        c.execute("""
            INSERT INTO subjects (code, name, icon, category, description)
            VALUES ('BIO101', 'Sinh học Phân tử & Di truyền học', '🧬', 'Khoa học tự nhiên',
                    'Cơ chế di truyền cấp độ phân tử (ADN, ARN, Protein), quy luật Menđen - Moocgan, di truyền quần thể Hardy-Weinberg & tế bào học.')
        """)
        bio_id = c.lastrowid
        bio_questions = [
            (
                "mcq",
                r"Câu 1 (Nhận biết - Nhân đôi ADN): Trong quá trình nhân đôi $\text{ADN}$, enzim $\text{ADN polymerase}$ chỉ tổng hợp mạch mới theo chiều nào?",
                r"Chiều $5' \to 3'$ (trượt trên mạch khuôn chiều $3' \to 5'$)",
                r"Chiều $3' \to 5'$ trên cả hai mạch khuôn",
                r"Hai chiều ngẫu nhiên không phụ thuộc đầu $3'\text{-OH}$",
                r"Chỉ tổng hợp trên các đoạn intron",
                "A",
                r"Enzim $\text{ADN polymerase}$ chỉ có khả năng gắn nucleotit mới vào đầu $3'\text{-OH}$ tự do, do đó mạch mới **luôn luôn được tổng hợp theo chiều $5' \to 3'$** (mạch liên tục trên khuôn $3' \to 5'$, và từng đoạn Okazaki trên khuôn $5' \to 3'$).",
                "easy"
            ),
            (
                "mcq",
                r"Câu 2 (Thông hiểu - Cấu trúc ADN): Một phân tử $\text{ADN}$ mạch kép có tổng số $N = 3000$ nucleotit, trong đó số nucleotit loại Adenin ($A$) chiếm $20\%$. Số liên kết hiđrô $H = 2A + 3G$ của phân tử $\text{ADN}$ này là:",
                r"$3900$ liên kết",
                r"$3600$ liên kết",
                r"$3000$ liên kết",
                r"$4200$ liên kết",
                "A",
                r"Theo nguyên tắc bổ sung ($A = T$, $G = X$ và $\%A + \%G = 50\%$): \n- $\%A = 20\% \Rightarrow \%G = 30\%$.\n- $A = 0,2 \times 3000 = 600$; $G = 0,3 \times 3000 = 900$.\n- Số liên kết hiđrô: $H = 2A + 3G = 2(600) + 3(900) = 1200 + 2700 = 3900$.",
                "medium"
            ),
            (
                "mcq",
                r"Câu 3 (Vận dụng - Di truyền quần thể Hardy-Weinberg): Một quần thể ngẫu phối đạt trạng thái cân bằng di truyền có tần số alen lặn $a$ là $q = 0,4$ và alen trội $A$ là $p = 0,6$. Tỉ lệ kiểu gen dị hợp tử $Aa$ trong quần thể là:",
                r"$48\%$ ($0,48$)",
                r"$36\%$ ($0,36$)",
                r"$16\%$ ($0,16$)",
                r"$24\%$ ($0,24$)",
                "A",
                r"Theo định luật Hardy-Weinberg: $$p^2 (AA) + 2pq (Aa) + q^2 (aa) = 1$$ Tần số kiểu gen dị hợp $Aa$ là $2pq = 2 \times 0,6 \times 0,4 = 0,48 = 48\%$.",
                "hard"
            ),
            (
                "mcq",
                r"Câu 4 (Thông hiểu - Phiên mã & Dịch mã): Trên phân tử $\text{mARN}$, bộ ba mở đầu (start codon) quy định axit amin mở đầu là bộ ba nào?",
                r"$5'\text{-AUG-}3'$",
                r"$5'\text{-UAA-}3'$",
                r"$5'\text{-UAG-}3'$",
                r"$5'\text{-UGA-}3'$",
                "A",
                r"Bộ ba mở đầu trên $\text{mARN}$ là $5'\text{-AUG-}3'$ (mã hóa Methionine ở sinh vật nhân thực và Formyl-methionine ở sinh vật nhân sơ). Ba bộ ba $5'\text{-UAA-}3'$, $5'\text{-UAG-}3'$, $5'\text{-UGA-}3'$ là các bộ ba kết thúc (stop codons).",
                "easy"
            ),
            (
                "mcq",
                r"Câu 5 (Vận dụng cao - Quy luật Menđen): Cho phép lai $P: AaBbDd \times AabbDd$ (các gen phân li độc lập, trội hoàn toàn). Tỉ lệ đời con $F_1$ mang kiểu hình trội về cả 3 tính trạng ($A\text{-}B\text{-}D\text{-}$) là:",
                r"$\frac{9}{32}$",
                r"$\frac{27}{64}$",
                r"$\frac{3}{16}$",
                r"$\frac{9}{16}$",
                "A",
                r"Tách riêng từng cặp lai độc lập:\n- $Aa \times Aa \to \frac{3}{4} A\text{-}$\n- $Bb \times bb \to \frac{1}{2} B\text{-}$\n- $Dd \times Dd \to \frac{3}{4} D\text{-}$\nNhân xác suất: $P(A\text{-}B\text{-}D\text{-}) = \frac{3}{4} \times \frac{1}{2} \times \frac{3}{4} = \frac{9}{32}$.",
                "very_hard"
            ),
            (
                "true_false",
                r"Câu 6 (Thông hiểu - Hô hấp tế bào): Nhận định Đúng hay Sai: Phương trình tổng quát của hô hấp hiếu khí ở tế bào nhân thực là $\ce{C6H12O6 + 6O2 -> 6CO2 + 6H2O + Q (\text{ATP} + \text{nhiệt})}$, trong đó giai đoạn chuỗi truyền electron ở màng trong ti thể tạo ra nhiều $\text{ATP}$ nhất.",
                "Đúng", "Sai", "", "", "A",
                r"Đúng! Đường phân (bào tương) chỉ tạo $2\text{ ATP}$, chu trình Krebs tạo $2\text{ ATP}$, còn chuỗi truyền electron hô hấp ở màng trong ti thể tạo tới $26\text{--}34\text{ ATP}$.",
                "medium"
            ),
            (
                "short_answer",
                r"Câu 7 (Vận dụng - Nguyên phân): Một tế bào sinh dưỡng có bộ nhiễm sắc thể lưỡng bội $2n = 8$ tiến hành nguyên phân liên tiếp $3$ lần. Tổng số tế bào con được tạo ra sau $3$ lần nguyên phân là bao nhiêu?",
                "8", "", "", "", "8",
                r"Từ $1$ tế bào qua $k$ lần nguyên phân tạo ra $2^k$ tế bào con. Với $k = 3$, số tế bào con là $2^3 = 8$.",
                "medium"
            ),
        ]
        for qt, qtext, oa, ob, oc, od, corr, expl, diff in bio_questions:
            c.execute("""
                INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty)
                VALUES (?, ?, ?, '', ?, ?, ?, ?, ?, ?, ?)
            """, (bio_id, qt, qtext, oa, ob, oc, od, corr, expl, diff))

        bio_fcs = [
            (r"Học thuyết Trung tâm (Central Dogma) của Sinh học phân tử", r"$$\text{ADN} \xrightarrow{\text{Nhân đôi}} \text{ADN} \xrightarrow{\text{Phiên mã}} \text{mARN} \xrightarrow{\text{Dịch mã}} \text{Protein} \longrightarrow \text{Tính trạng}$$ (Ngoại lệ ở Retrovirus có enzim phiên mã ngược: $\text{ARN} \to \text{cADN}$).", "ADN -> mARN -> Protein"),
            (r"Công thức giải nhanh bài toán cấu trúc ADN mạch kép", r"- Tổng số nu: $N = 2A + 2G$ ($\Rightarrow A + G = \frac{N}{2}$)\n- Chiều dài gen: $L = \frac{N}{2} \times 3,4\,\text{\AA}$\n- Số liên kết hiđrô: $H = 2A + 3G$", "A=T (2 lk H) | G=X (3 lk H)"),
            (r"Định luật cân bằng di truyền Hardy-Weinberg", r"$$p^2 (AA) + 2pq (Aa) + q^2 (aa) = 1 \quad (p + q = 1)$$ Điều kiện nghiệm đúng: Quần thể kích thước lớn, ngẫu phối, không đột biến, không chọn lọc tự nhiên, không di - nhập gen.", "p + q = 1"),
        ]
        for fr, bk, hn in bio_fcs:
            c.execute("INSERT INTO flashcards (subject_id, front, back, hint, repetitions, interval_days, ease_factor, next_review) VALUES (?, ?, ?, ?, 0, 1, 2.5, ?)", (bio_id, fr, bk, hn, today_str))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    db.init_db()
    ensure_stem_and_math_upgraded()
    print("STEM & Math upgrade completed!")
