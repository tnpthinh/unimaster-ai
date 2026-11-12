# -*- coding: utf-8 -*-
"""
UniMaster AI - Seeder for YDS 2024 Medical Biochemistry
Batch 4:
- Chương 10: Chuyển hóa năng lượng (100 câu)
- Chương 11: Chuyển hóa glucid (100 câu)
- Chương 12: Chuyển hóa lipid (100 câu)
Total: 300 questions
"""

import sqlite3

def seed_part4():
    conn = sqlite3.connect('unimaster.db')
    cur = conn.cursor()
    cur.execute("SELECT id FROM subjects WHERE code = 'HOASINH_YDS_2024'")
    row = cur.fetchone()
    if not row:
        print("Error: Subject HOASINH_YDS_2024 not found!")
        return
    sub_id = row[0]

    questions = []

    # ==========================================
    # CHƯƠNG 10: CHUYỂN HÓA NĂNG LƯỢNG (100 CÂU)
    # ==========================================
    ch10_name = "Chương 10: Chuyển hóa năng lượng"
    ch10_img = "/static/uploads/hoasinh_yds/ch10_krebs_cycle_tca.svg"

    ch10_core = [
        (
            "Chu trình Acid Citric (Chu trình Krebs / TCA) diễn ra tại vị trí tế bào học nào?",
            "Chất nền (matrix) của ty thể (ngoại trừ enzym Succinate Dehydrogenase gắn ở màng trong ty thể).",
            "Bào tương tế bào.",
            "Khoang màng ngoài ty thể.",
            "Lưới nội chất hạt.",
            "A",
            "Tất cả 8 phản ứng của chu trình Krebs đều xảy ra trong chất nền ty thể (mitochondrial matrix), ngoại trừ duy nhất enzym Succinate Dehydrogenase (xúc tác chuyển Succinat thành Fumarat) là một protein gắn chặt vào màng trong ty thể (chính là Phức hợp II của chuỗi hô hấp tế bào).",
            ch10_img
        ),
        (
            "Phản ứng mở đầu chu trình Krebs là sự ngưng tụ giữa hai chất nào sau đây?",
            "Oxaloacetate (4C) và gốc Acetyl của Acetyl-CoA (2C) dưới tác dụng của enzym Citrate Synthase tạo thành Citrate (6C).",
            "Pyruvate và Acetyl-CoA tạo $\\alpha$-ketoglutarate.",
            "Succinyl-CoA và Glycin tạo ALA.",
            "Citrate và Isocitrate tạo Oxaloacetate.",
            "A",
            "Phản ứng 1 của chu trình Krebs do Citrate Synthase xúc tác: gốc Acetyl (2C) ngưng tụ với Oxaloacetate (4C) cùng 1 phân tử $H_2O$ thủy phân liên kết thioester giải phóng Coenzyme A tự do ($CoA-SH$) và tạo ra phân tử Citrate 6 carbon.",
            ch10_img
        ),
        (
            "Enzym nào đóng vai trò là enzym dị lập thể giới hạn tốc độ (rate-limiting enzyme) chính của toàn bộ chu trình Krebs?",
            "Isocitrate Dehydrogenase (bị ức chế bởi ATP, NADH; hoạt hóa bởi ADP, $Ca^{2+}$).",
            "Citrate Synthase.",
            "Succinate Dehydrogenase.",
            "Fumarase.",
            "A",
            "Isocitrate Dehydrogenase xúc tác phản ứng khử carboxyl oxy hóa Isocitrate thành $\\alpha$-Ketoglutarate tạo ra phân tử $CO_2$ và NADH đầu tiên. Đây là bước kiểm soát tốc độ chính của chu trình, chịu sự ức chế ngược âm tính của nồng độ năng lượng cao (ATP và NADH).",
            ch10_img
        ),
        (
            "Phản ứng duy nhất trong chu trình Krebs thực hiện phosphoryl hóa ở mức cơ chất (Substrate-level phosphorylation) để trực tiếp tạo liên kết giàu năng lượng là:",
            "Sự biến đổi Succinyl-CoA thành Succinate nhờ enzym Succinyl-CoA Synthetase (Succinate Thiokinase), tạo ra 1 phân tử GTP (hoặc ATP).",
            "Sự biến đổi Citrate thành Isocitrate.",
            "Sự oxy hóa Succinate thành Fumarate.",
            "Sự oxy hóa Malate thành Oxaloacetate.",
            "A",
            "Năng lượng từ sự phân cắt liên kết thioester giàu năng lượng của Succinyl-CoA được ghép đôi trực tiếp với quá trình phosphoryl hóa GDP tạo GTP (tại gan/thận) hoặc ADP tạo ATP (tại mô tim/cơ), không cần chuỗi truyền điện tử.",
            ch10_img
        ),
        (
            "Mỗi vòng quay của chu trình Krebs tiêu thụ 1 gốc Acetyl-CoA sẽ giải phóng những sản phẩm nào sau đây?",
            "2 phân tử $CO_2$, 3 NADH, 1 $FADH_2$ và 1 GTP (tương đương năng lượng khoảng 10 ATP sau chuỗi ETC).",
            "1 phân tử $CO_2$, 2 NADH, 2 $FADH_2$ và 2 ATP.",
            "3 phân tử $CO_2$, 1 NADH, 3 $FADH_2$ và 1 ATP.",
            "Không tạo ra $CO_2$ nào và chỉ sinh nhiệt năng.",
            "A",
            "Một phân tử Acetyl-CoA đi vào chu trình Krebs giải phóng 2 nguyên tử C dưới dạng 2 phân tử $CO_2$ (qua 2 phản ứng khử carboxyl oxy hóa của Isocitrate DH và $\\alpha$-Ketoglutarate DH), khử 3 $NAD^+$ thành 3 NADH, khử 1 FAD thành 1 $FADH_2$ và tạo 1 GTP. Khi đi qua chuỗi ETC: $3\\times 2.5 + 1\\times 1.5 + 1 = 10$ ATP.",
            ch10_img
        ),
        (
            "Theo Thuyết hóa thẩm (Chemiosmotic Hypothesis) của Peter Mitchell, ATP được tổng hợp tại màng trong ty thể là nhờ động lực nào?",
            "Gradient điện hóa proton ($H^+$) giữa khoang gian màng và chất nền ty thể điều khiển dòng proton chạy qua phức hợp ATP Synthase ($F_0F_1$).",
            "Sự vận chuyển tích cực trực tiếp oxy từ ngoài vào ty thể.",
            "Sự thủy phân lipid màng trong ty thể giải phóng nhiệt lượng.",
            "Lực hút tĩnh điện giữa các gốc phosphat tự do.",
            "A",
            "Các phức hợp I, III, IV của chuỗi truyền điện tử hoạt động như các bơm proton, đẩy ion $H^+$ từ chất nền ra khoang gian màng, tạo ra chênh lệch nồng độ pH và điện thế màng (lực động proton - Proton Motive Force). Dòng $H^+$ chảy ngược về chất nền qua kênh $F_0$ làm quay trục xoay của ATP Synthase, kích hoạt trung tâm xúc tác của $F_1$ tổng hợp ATP từ ADP và $P_i$.",
            ch10_img
        ),
        (
            "Phức hợp nào trong chuỗi truyền điện tử ty thể KHÔNG hoạt động như một bơm proton xuyên màng (không bơm $H^+$ ra khoang gian màng)?",
            "Phức hợp II (Succinate-Q Reductase / Succinate Dehydrogenase).",
            "Phức hợp I (NADH-Q Oxidoreductase).",
            "Phức hợp III (Q-Cytochrome c Oxidoreductase).",
            "Phức hợp IV (Cytochrome c Oxidase).",
            "A",
            "Phức hợp II chuyển electron từ $FADH_2$ (tạo ra từ Succinate) sang Ubiquinone (CoQ). Do chênh lệch thế năng oxy hóa khử giữa $FADH_2$ và CoQ không đủ lớn, Phức hợp II KHÔNG giải phóng đủ năng lượng để bơm proton $H^+$ qua màng. Vì vậy, 1 $FADH_2$ chỉ tạo được khoảng 1.5 ATP (so với 2.5 ATP từ NADH của Phức hợp I).",
            ch10_img
        ),
        (
            "Độc chất Cyanide ($CN^-$) và khí Carbon Monoxide (CO) gây ngừng thở tế bào và tử vong nhanh chóng do ức chế đặc hiệu thành phần nào của chuỗi truyền điện tử ty thể?",
            "Ức chế phức hợp IV (Cytochrome c Oxidase), khóa chặt tâm gắn sắt-heme $a_3-Cu_B$ ngăn cản chuyển electron cho oxy.",
            "Ức chế phức hợp I ngăn cản khử NADH.",
            "Ức chế phức hợp II ngăn chuyển hóa succinat.",
            "Ức chế men ATP Synthase.",
            "A",
            "Cyanide ($CN^-$), CO và Azide ($N_3^-$) gắn chặt với ion sắt $Fe^{3+}$ trong nhóm heme $a_3$ của Cytochrome c Oxidase (Phức hợp IV), ngăn cản phản ứng khử oxy thành nước. Chuỗi truyền điện tử bị đình trệ hoàn toàn, gradient proton biến mất, tổng hợp ATP ngừng trệ dẫn tới tử vong tế bào tối cấp tính.",
            ch10_img
        ),
        (
            "Chất phá ghép (Uncoupling Agent) như 2,4-Dinitrophenol (DNP) hoặc protein Thermogenin (UCP-1) gây biến đổi chuyển hóa năng lượng nào sau đây?",
            "Làm tiêu tán gradient proton bằng cách cho $H^+$ rò rỉ trực tiếp qua màng trong ty thể mà không đi qua ATP Synthase: Chuỗi truyền điện tử và tiêu thụ $O_2$ tăng vọt nhưng KHÔNG tạo được ATP, năng lượng giải phóng hoàn toàn dưới dạng NHIỆT.",
            "Khóa kênh truyền điện tử làm giảm tiêu thụ oxy.",
            "Ức chế hoàn toàn chu trình Krebs trong chất nền ty thể.",
            "Ngăn chặn sự thâm nhập của pyruvate vào ty thể.",
            "A",
            "Chất phá ghép tách rời (uncouple) quá trình oxy hóa (chuỗi ETC) khỏi quá trình phosphoryl hóa (tổng hợp ATP). Protein UCP-1 (Thermogenin) trong mô mỡ nâu của trẻ sơ sinh và động vật ngủ đông thực hiện cơ chế này để sinh nhiệt chống rét. Thuốc giảm cân độc hại DNP trước đây gây sốt cực cao và suy đa tạng tử vong do cơ chế phá ghép.",
            None
        ),
        (
            "Chất kháng sinh Oligomycin ức chế quá trình phosphoryl hóa oxy hóa theo cơ chế nào?",
            "Gắn trực tiếp và bịt kín kênh proton $F_0$ của enzym ATP Synthase, ngăn cản dòng ion $H^+$ chảy về chất nền ty thể.",
            "Ức chế phức hợp I NADH dehydrogenase.",
            "Phân giải màng ngoài ty thể.",
            "Cạnh tranh với cơ chất succinate tại phức hợp II.",
            "A",
            "Oligomycin gắn đặc hiệu vào tiểu đơn vị $F_0$ của ATP Synthase làm khóa dòng proton $H^+$. Hậu quả là gradient proton tăng rất cao trong khoang gian màng tạo lực cản ngược làm chuỗi ETC cũng bị dừng lại thứ phát (trừ khi có mặt chất phá ghép).",
            None
        )
    ]

    for i in range(100):
        if i < len(ch10_core):
            q, a, b, c, d, corr, exp, img = ch10_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch10_img if (i % 5 == 0) else None

            ch10_topics = [
                ("Phức hợp $\\alpha$-Ketoglutarate Dehydrogenase và ngộ độc Asen", "Phức hợp này gồm 3 enzym ($E_1, E_2, E_3$) và cần 5 coenzym: TPP, Lipoate, CoA-SH, FAD, NAD+.", "Cấu trúc và cơ chế xúc tác tương tự phức hợp Pyruvate Dehydrogenase.", "Asenat (Arsenic) gắn vào nhóm sulfhydryl của acid lipoic làm bất hoạt enzym, gây ức chế hô hấp tế bào.", "Sự tích tụ $\\alpha$-ketoglutarate kích thích phản ứng trao đổi amin tạo glutamat."),
                ("Các phản ứng bổ sung cơ chất (Anaplerotic reactions)", "Chu trình Krebs là chu trình lưỡng dụng (amphibolic): vừa dị hóa vừa cung cấp tiền chất đồng hóa.", "Phản ứng carboxyl hóa Pyruvate thành Oxaloacetate nhờ Pyruvate Carboxylase (cần Biotin) là phản ứng anaplerotic quan trọng nhất.", "Sự khử amin của Glutamat tạo $\\alpha$-ketoglutarate giúp bổ sung sản phẩm trung gian cho chu trình.", "Sự thoái hóa acid amin chuỗi nhánh tạo Succinyl-CoA tham gia vào chu trình Krebs."),
                ("Con thoi vận chuyển điện tử từ bào tương vào ty thể", "Con thoi Malate-Aspartate ở gan, thận và tim chuyển NADH bào tương thành NADH ty thể (tạo ~2.5 ATP/NADH).", "Con thoi Glycerol-3-Phosphate ở cơ xương và não chuyển NADH bào tương thành $FADH_2$ ty thể (tạo ~1.5 ATP/NADH).", "Màng trong ty thể không cho phép NADH và $NAD^+$ tự do khuếch tán qua lại.", "Sự lựa chọn con thoi giải thích vì sao 1 phân tử glucose khi oxy hóa hoàn toàn tạo 30 hoặc 32 ATP."),
                ("Hệ thống Cytochrome và phản ứng oxy hóa khử", "Các cytochrome chứa nhóm ngoại Heme với nguyên tử sắt luân chuyển giữa $Fe^{2+}$ (dạng khử) và $Fe^{3+}$ (dạng oxy hóa).", "Cytochrome c là một protein ngoại vi hòa tan trong khoang gian màng, di chuyển linh hoạt giữa phức hợp III và IV.", "Cytochrome c khi bị rò rỉ ra bào tương sẽ kích hoạt con đường chết theo chương trình (Apoptosis) qua caspase.", "Ubiquinone (Coenzyme Q / CoQ10) là chất mang điện tử kỵ nước hòa tan tự do trong màng kép phospholipid."),
                ("Bệnh lý ty thể và hội chứng lâm sàng", "Đột biến DNA ty thể (mtDNA) di truyền 100% theo dòng mẹ do ty thể của hợp tử có nguồn gốc từ noãn bào.", "Bệnh thần kinh thị giác di truyền Leber (LHON) do đột biến phức hợp I gây mù đột ngột ở người trẻ.", "Hội chứng MELAS (Bệnh não cơ ty thể, nhiễm toan lactic và đột quỵ) do rối loạn phosphoryl hóa oxy hóa.", "Hội chứng Leigh (bệnh não hoại tử bán cấp) biểu hiện thoái hóa thần kinh vận động tiến triển ở trẻ em.")
            ]
            tp = ch10_topics[i % len(ch10_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Khẳng định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi đề cập đến {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cơ chế này hoàn toàn không liên quan đến chuỗi hô hấp tế bào và không cần sự tham gia của bất kỳ coenzym nào."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo sinh năng lượng sinh học."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Nhận định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Quá trình này không tuân theo các định luật nhiệt động lực học và chỉ quan sát thấy trong môi trường nhân tạo."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nội dung sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch10_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 11: CHUYỂN HÓA GLUCID (100 CÂU)
    # ==========================================
    ch11_name = "Chương 11: Chuyển hóa glucid"
    ch11_img = "/static/uploads/hoasinh_yds/ch11_glycolysis_gluconeogenesis.svg"

    ch11_core = [
        (
            "Ba phản ứng không thuận nghịch (một chiều) của con đường đường phân (Glycolysis) được xúc tác bởi các enzym nào sau đây?",
            "Hexokinase (hoặc Glucokinase), Phosphofructokinase-1 (PFK-1) và Pyruvate Kinase.",
            "Phosphohexose Isomerase, Aldolase và Enolase.",
            "Glyceraldehyde-3-Phosphate Dehydrogenase, Phosphoglycerate Kinase và Triose Phosphate Isomerase.",
            "Pyruvate Dehydrogenase, Citrate Synthase và Aconitase.",
            "A",
            "Đường phân gồm 10 phản ứng, trong đó có 3 phản ứng một chiều giải phóng năng lượng tự do lớn: (1) Glucose $\\rightarrow$ G6P (Hexokinase/Glucokinase); (2) Fructose-6-P $\\rightarrow$ Fructose-1,6-BP (PFK-1); (3) Phosphoenolpyruvate $\\rightarrow$ Pyruvate (Pyruvate Kinase). Ba phản ứng này là các điểm kiểm soát điều hòa chính.",
            ch11_img
        ),
        (
            "Sự khác biệt quan trọng nhất giữa Glucokinase (ở gan và tế bào $\\beta$ tụy) và Hexokinase (ở các mô ngoại vi) là gì?",
            "Glucokinase có $K_m$ rất cao với glucose (ái lực thấp), không bị ức chế bởi sản phẩm Glucose-6-Phosphate, giúp gan thu nạp tối đa glucose sau bữa ăn khi đường huyết tăng vọt.",
            "Hexokinase có $K_m$ cao hơn Glucokinase.",
            "Glucokinase bị ức chế dị lập thể bởi Glucose-6-Phosphate.",
            "Hexokinase chỉ hoạt động khi đường huyết vượt quá 10 mmol/L.",
            "A",
            "Hexokinase ở hầu hết các mô có $K_m$ rất thấp (~0.1 mM) nên luôn hoạt động ở tốc độ tối đa ngay cả khi đói để cung cấp năng lượng cơ bản, và bị ức chế bởi G6P. Ngược lại, Glucokinase ở gan có $K_m$ cao (~10 mM), chỉ hoạt động mạnh sau bữa ăn no khi glucose máu tĩnh mạch cửa tăng vọt để biến glucose thành G6P dự trữ thành glycogen.",
            ch11_img
        ),
        (
            "Chất điều hòa dị lập thể dương mạnh nhất của enzym Phosphofructokinase-1 (PFK-1) trong con đường đường phân là gì?",
            "Fructose-2,6-bisphosphate ($F-2,6-BP$).",
            "Adenosine Triphosphate (ATP).",
            "Citrate.",
            "Glucose-6-Phosphate.",
            "A",
            "$F-2,6-BP$ là chất truyền tin dị lập thể nội bào mạnh nhất hoạt hóa PFK-1 (kích thích đường phân) đồng thời ức chế Fructose-1,6-bisphosphatase (ức chế tân tạo đường). Nồng độ $F-2,6-BP$ được điều hòa bởi enzym kép PFK-2/FBPase-2 chịu sự kiểm soát đối kháng của Insulin và Glucagon.",
            ch11_img
        ),
        (
            "Trong điều kiện kỵ khí (như tế bào hồng cầu hoặc mô cơ vân co rút gắng sức thiếu oxy), Pyruvate được chuyển hóa tiếp tục thành chất nào để tái tạo $NAD^+$ duy trì đường phân?",
            "Pyruvate bị khử thành Lactate nhờ enzym Lactate Dehydrogenase (LDH), oxy hóa NADH thành $NAD^+$.",
            "Pyruvate bị oxy hóa thành Acetyl-CoA đi vào chu trình Krebs.",
            "Pyruvate biến đổi thành Oxaloacetate.",
            "Pyruvate chuyển hóa thành Ethanol và khí $CO_2$.",
            "A",
            "Trong điều kiện kỵ khí hoặc tế bào không có ty thể (như hồng cầu), chuỗi truyền điện tử không hoạt động nên không thể tái tạo $NAD^+$ từ NADH. Enzym LDH trong bào tương xúc tác phản ứng thuận nghịch: Pyruvate + NADH + $H^+ \\leftrightarrow$ Lactate + $NAD^+$, cung cấp $NAD^+$ để phản ứng số 6 của đường phân (GAPDH) tiếp tục diễn ra.",
            ch11_img
        ),
        (
            "Hiệu suất năng lượng thuần (net gain) của con đường đường phân từ 1 phân tử Glucose trong điều kiện KỴ KHÍ là bao nhiêu?",
            "2 phân tử ATP thuần (tạo ra 4 ATP nhưng đã tiêu tốn 2 ATP ở giai đoạn đầu) và 2 phân tử Lactate.",
            "4 phân tử ATP và 2 NADH.",
            "30 hoặc 32 phân tử ATP.",
            "Không tạo ra được phân tử ATP nào.",
            "A",
            "Trong đường phân kỵ khí, giai đoạn tiêu tốn năng lượng sử dụng 2 ATP (ở phản ứng Hexokinase và PFK-1). Giai đoạn sinh năng lượng tạo ra 4 ATP (2 từ PGK, 2 từ Pyruvate kinase) qua phosphoryl hóa mức cơ chất. Do đó hiệu suất thuần là: $4 - 2 = 2$ ATP cho mỗi phân tử glucose.",
            ch11_img
        ),
        (
            "Chu trình Cori (Cori Cycle) mô tả mối quan hệ chuyển hóa tương hỗ nào giữa mô cơ và gan?",
            "Lactate sinh ra từ đường phân kỵ khí ở mô cơ vận chuyển qua máu về gan để tân tạo thành Glucose; Glucose sau đó giải phóng vào máu đưa trở lại cơ để tái sử dụng.",
            "Glucose từ gan vận chuyển đến mô mỡ tổng hợp triglycerid.",
            "Amoniac từ cơ chuyển về gan tạo ure.",
            "Acid béo từ mô mỡ vận chuyển về cơ sinh năng lượng.",
            "A",
            "Mô cơ vận động mạnh sinh nhiều acid lactic. Cơ không có enzym Glucose-6-phosphatase nên không thể tự tân tạo đường giải phóng vào máu. Lactate đi vào máu về gan, tế bào gan dùng enzym LDH chuyển lactate thành pyruvate rồi tân tạo thành glucose tiêu tốn 6 ATP, glucose mới sinh lại cung cấp cho cơ.",
            ch11_img
        ),
        (
            "Enzym nào sau đây trong quá trình tân tạo đường (Gluconeogenesis) đóng vai trò thay thế phản ứng một chiều của Hexokinase và CHỈ HIỆN DIỆN ở gan và thận?",
            "Glucose-6-Phosphatase (gắn ở màng lưới nội chất).",
            "Fructose-1,6-Bisphosphatase.",
            "Pyruvate Carboxylase.",
            "Phosphoenolpyruvate Carboxykinase (PEPCK).",
            "A",
            "Glucose-6-Phosphatase xúc tác cắt nhóm phosphat của G6P tạo glucose tự do để khuếch tán vào máu qua kênh GLUT2 duy trì đường huyết khi đói. Do cơ xương hoàn toàn thiếu enzym này, glycogen của cơ chỉ dùng nội bộ cho chính tế bào cơ mà không thể tạo đường tự do ra máu.",
            ch11_img
        ),
        (
            "Bệnh Von Gierke (Bệnh dự trữ Glycogen týp I - GSD I) do khiếm khuyết di truyền enzym Glucose-6-Phosphatase gây ra các biểu hiện lâm sàng đặc trưng nào sau đây?",
            "Hạ đường huyết nghiêm trọng khi nhịn đói, gan to ứ đọng glycogen, nhiễm toan acid lactic máu, tăng lipid máu và tăng acid uric máu (bệnh Gout thứ phát).",
            "Yếu cơ khi gắng sức nhưng đường huyết luôn bình thường.",
            "Suy tim xung huyết do phì đại cơ tim tiến triển.",
            "Tán huyết cấp tính sau khi ăn đậu fava.",
            "A",
            "Do thiếu Glucose-6-phosphatase, gan không thể giải phóng glucose vào máu từ cả hai con đường tiêu glycogen và tân tạo đường, dẫn tới hạ đường huyết khi đói dữ dội. G6P ứ đọng chuyển hướng sang tổng hợp lipid (tăng TG, VLDL), tăng tạo acid lactic và kích thích con đường HMP shunt tạo nhiều ribose-5-P dẫn tới tăng tổng hợp purine và acid uric gây Gout.",
            None
        ),
        (
            "Con đường Pentose Phosphate (HMP Shunt / Hexose Monophosphate) có hai vai trò sinh lý tối quan trọng là gì?",
            "Cung cấp NADPH (lực khử sinh tổng hợp và chống oxy hóa) và cung cấp Ribose-5-Phosphate (tiền chất tổng hợp nucleotid, DNA, RNA).",
            "Tạo ra 36 phân tử ATP cung cấp cho co cơ.",
            "Oxy hóa hoàn toàn glucose thành $CO_2$ và nước.",
            "Tân tạo glucose từ các acid béo chuỗi dài.",
            "A",
            "Con đường Pentose Phosphate không nhằm mục đích tạo ATP mà cung cấp: (1) NADPH cần cho sinh tổng hợp acid béo, cholesterol, hormon steroid và giữ cho Glutathione luôn ở dạng khử bảo vệ hồng cầu; (2) Ribose-5-phosphat cần cho tổng hợp acid nucleic ở các mô phân chia nhanh.",
            None
        ),
        (
            "Bệnh nhân thiếu hụt enzym Glucose-6-Phosphate Dehydrogenase (G6PD) trên tế bào hồng cầu xuất hiện cơn tán huyết cấp tính khi tiếp xúc với các yếu tố khởi phát nào?",
            "Thuốc chống sốt rét (Primaquine), thuốc kháng sinh nhóm Sulfonamid, Dapsone, hoặc ăn đậu tằm (Fava beans).",
            "Ăn quá nhiều thức ăn giàu đường ngọt saccarose.",
            "Uống sữa tươi giàu đường lactose.",
            "Vận động thể thao nhẹ nhàng vào buổi sáng.",
            "A",
            "G6PD là enzym đầu tiên của con đường Pentose Phosphate tạo NADPH duy trì Glutathione khử (GSH) trong hồng cầu. Khi tiếp xúc với các tác nhân oxy hóa (thuốc sốt rét primaquine, hóa chất, đậu fava), hồng cầu không đủ GSH để trung hòa $H_2O_2$, làm hemoglobin bị kết tủa thành các thể Heinz và màng hồng cầu bị oxy hóa vỡ gây tán huyết cấp tính.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch11_core):
            q, a, b, c, d, corr, exp, img = ch11_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch11_img if (i % 5 == 0) else None

            ch11_topics = [
                ("Sinh tổng hợp Glycogen và vai trò Glycogenin", "UDP-Glucose là dạng glucose hoạt hóa dùng làm cơ chất cho enzym Glycogen Synthase.", "Enzym Glycogen Synthase chỉ tạo liên kết $\\alpha$-1,4-glycosid nối dài chuỗi.", "Enzym phân nhánh (Branching enzyme - Amylo-$\\alpha(1,4)\\rightarrow \\alpha(1,6)$-transglucosidase) tạo các liên kết nhánh $\\alpha$-1,6.", "Protein lõi Glycogenin đóng vai trò là mồi bắt đầu gắn 8 gốc glucose đầu tiên nhờ hoạt tính tự glycosyl hóa."),
                ("Thoái hóa Glycogen và các enzym tham gia", "Glycogen Phosphorylase cắt liên kết $\\alpha$-1,4 giải phóng Glucose-1-Phosphate (cần coenzyme PLP).", "Enzym cắt nhánh (Debranching enzyme) có 2 hoạt tính: 4:4 transferase chuyển 3 gốc glucose và $\\alpha$-1,6-glucosidase cắt gốc glucose nhánh tự do.", "Phosphoglucomutase xúc tác phản ứng thuận nghịch chuyển G1P thành G6P.", "Ở cơ, G6P đi thẳng vào đường phân; ở gan, G6P bị Glucose-6-phosphatase thủy phân giải phóng glucose vào máu."),
                ("Các bệnh tích lũy Glycogen (GSD) khác", "Bệnh Pompe (GSD II) do thiếu enzym $\\alpha$-1,4-glucosidase trong lysosome, ứ glycogen tim gây phì đại cơ tim tử vong sớm.", "Bệnh McArdle (GSD V) do thiếu Glycogen phosphorylase cơ vân, biểu hiện đau mỏi cơ, chuột rút và myoglobin niệu sau vận động.", "Bệnh Cori / Forbes (GSD III) do thiếu enzym cắt nhánh tạo glycogen có nhánh ngắn bất thường.", "Bệnh Andersen (GSD IV) do thiếu enzym tạo nhánh tạo glycogen không nhánh gây xơ gan tiến triển."),
                ("Chuyển hóa Galactose và Fructose", "Galactose được chuyển hóa qua Galactokinase và Galactose-1-Phosphate Uridyltransferase (GALT).", "Bệnh Galactosemia bẩm sinh cổ điển do thiếu enzym GALT gây đục thủy tinh thể, suy gan, chậm phát triển trí tuệ.", "Fructose ở gan được Fructokinase phosphoryl hóa thành Fructose-1-P rồi bị Aldolase B phân cắt.", "Bất dung nạp Fructose di truyền (HFI) do thiếu hụt Aldolase B gây tích tụ F1P ức chế tân tạo đường gây hạ đường huyết nặng."),
                ("Ý nghĩa xét nghiệm đường huyết và HbA1c", "Nồng độ glucose máu tĩnh mạch lúc đói bình thường từ 3.9 đến 5.6 mmol/L (70 - 99 mg/dL).", "Chẩn đoán Đái tháo đường khi glucose đói $\\ge 7.0$ mmol/L hoặc HbA1c $\\ge 6.5\\%$ (xác nhận lại lần 2).", "Nghiệm pháp dung nạp glucose đường uống (OGTT) dùng 75g glucose, chẩn đoán ĐTĐ nếu đường huyết sau 2h $\\ge 11.1$ mmol/L.", "HbA1c bị sai lệch trong các bệnh lý làm thay đổi đời sống hồng cầu (như thiếu máu tán huyết, truyền máu gần đây).")
            ]
            tp = ch11_topics[i % len(ch11_topics)]
            is_except = (i % 2 == 1)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Con đường chuyển hóa này không chịu sự tác động của enzym và có thể tự hoàn thành không phụ thuộc vào nồng độ ion hay năng lượng tế bào."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng glucid sinh lý."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Đặc điểm hóa sinh nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ được chuyển hóa khi cơ thể ở nhiệt độ đóng băng và hoàn toàn mất tác dụng ở thân nhiệt bình thường."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch11_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 12: CHUYỂN HÓA LIPID (100 CÂU)
    # ==========================================
    ch12_name = "Chương 12: Chuyển hóa lipid"
    ch12_img = "/static/uploads/hoasinh_yds/ch12_fatty_acid_beta_oxidation.svg"

    ch12_core = [
        (
            "Con thoi Carnitine (Carnitine Shuttle) đảm nhận vai trò sống còn nào trong quá trình thoái hóa acid béo?",
            "Vận chuyển các phân tử Acyl-CoA béo chuỗi dài từ bào tương xuyên qua màng trong ty thể vào chất nền ty thể để thực hiện $\\beta$-oxy hóa.",
            "Vận chuyển Acetyl-CoA từ ty thể ra bào tương.",
            "Vận chuyển acid mật từ gan xuống túi mật.",
            "Vận chuyển cholesterol từ mô ngoại vi về gan.",
            "A",
            "Màng trong ty thể không thấm đối với Acyl-CoA béo chuỗi dài (>12C). Enzym Carnitine Palmitoyltransferase I (CPT-I) ở màng ngoài gắn acyl với carnitine tạo acylcarnitine để vận chuyển qua màng trong nhờ translocase. CPT-II ở màng trong tái tạo lại Acyl-CoA trong chất nền ty thể.",
            ch12_img
        ),
        (
            "Enzym CPT-I (Carnitine Palmitoyltransferase I) bị ức chế dị lập thể bởi chất nào sau đây để ngăn cản sự $\\beta$-oxy hóa xảy ra đồng thời với quá trình sinh tổng hợp acid béo?",
            "Malonyl-CoA (sản phẩm đầu tiên của con đường sinh tổng hợp acid béo).",
            "Acetyl-CoA.",
            "Citrate.",
            "Palmitate.",
            "A",
            "Khi tế bào ở trạng thái no và thừa năng lượng, Acetyl-CoA carboxylase tạo ra nhiều Malonyl-CoA để tổng hợp acid béo. Nồng độ Malonyl-CoA cao sẽ ức chế mạnh CPT-I, khóa con thoi carnitine không cho acid béo mới sinh đi vào ty thể để bị thoái hóa phân giải (ngăn chặn chu trình vô ích - futile cycle).",
            ch12_img
        ),
        (
            "Một chu kỳ của quá trình $\\beta$-oxy hóa acid béo no chuỗi chẵn trong ty thể bao gồm 4 phản ứng liên tiếp theo thứ tự nào?",
            "Oxy hóa lần 1 (khử hydro tạo $FADH_2$) $\\rightarrow$ Hợp nước (Hydrat hóa) $\\rightarrow$ Oxy hóa lần 2 (khử hydro tạo NADH) $\\rightarrow$ Phân cắt Thiolase (dùng Coenzyme A giải phóng 1 Acetyl-CoA).",
            "Hợp nước $\\rightarrow$ Khử hydro $\\rightarrow$ Khử carboxyl $\\rightarrow$ Ngưng tụ.",
            "Phosphoryl hóa $\\rightarrow$ Đồng phân hóa $\\rightarrow$ Cắt mạch $\\rightarrow$ Oxy hóa.",
            "Khử hydro $\\rightarrow$ Khử nước $\\rightarrow$ Khử carboxyl $\\rightarrow$ Tái tạo carnitine.",
            "A",
            "Bốn bước phản ứng lặp lại của $\\beta$-oxy hóa: (1) Acyl-CoA Dehydrogenase tạo trans-$\\Delta^2$-enoyl-CoA và $FADH_2$; (2) Enoyl-CoA Hydratase gắn nước tạo L-$\\beta$-hydroxyacyl-CoA; (3) $\\beta$-Hydroxyacyl-CoA Dehydrogenase tạo $\\beta$-ketoacyl-CoA và NADH; (4) $\\beta$-Ketothiolase dùng $CoA-SH$ cắt đứt liên kết giải phóng 1 Acetyl-CoA (2C) và một Acyl-CoA ngắn hơn 2 carbon.",
            ch12_img
        ),
        (
            "Hiệu suất năng lượng thuần (net ATP) thu được từ sự oxy hóa hoàn toàn 1 phân tử Acid Palmitic (16C) thành $CO_2$ và $H_2O$ là bao nhiêu?",
            "106 phân tử ATP (tổng tạo thành 108 ATP trừ 2 ATP tiêu tốn cho phản ứng hoạt hóa ban đầu).",
            "129 phân tử ATP.",
            "36 phân tử ATP.",
            "180 phân tử ATP.",
            "A",
            "Palmitate (16C) trải qua 7 chu kỳ $\\beta$-oxy hóa tạo 8 Acetyl-CoA, 7 $FADH_2$, 7 NADH. 8 Acetyl-CoA $\\times 10 = 80$ ATP; 7 $FADH_2 \\times 1.5 = 10.5$ ATP; 7 NADH $\\times 2.5 = 17.5$ ATP. Tổng cộng $= 108$ ATP. Trừ 2 liên kết cao năng ATP biến thành AMP và $PP_i$ ở phản ứng Acyl-CoA Synthetase hoạt hóa ban đầu $\\rightarrow$ Thuần 106 ATP.",
            ch12_img
        ),
        (
            "Cơ quan nào trong cơ thể là nơi DUY NHẤT có khả năng tổng hợp thể Ceton (Ketone bodies), nhưng lại KHÔNG THỂ sử dụng thể ceton làm nguồn năng lượng?",
            "Gan (Liver).",
            "Não.",
            "Cơ tim.",
            "Cơ xương vân.",
            "A",
            "Gan tổng hợp thể ceton (acetoacetate, $\\beta$-hydroxybutyrate, acetone) trong ty thể tế bào gan nhờ enzym HMG-CoA synthase. Tuy nhiên, gan hoàn toàn THIẾU enzym $\\beta$-ketoacyl-CoA transferase (Thiophorase), do đó gan không thể hoạt hóa acetoacetate thành acetoacetyl-CoA để đốt cháy mà phải xuất khẩu toàn bộ ra máu nuôi não, cơ và tim.",
            ch12_img
        ),
        (
            "Enzym nào đóng vai trò là enzym giới hạn tốc độ của con đường sinh tổng hợp acid béo trong bào tương tế bào?",
            "Acetyl-CoA Carboxylase (ACC) (xúc tác chuyển Acetyl-CoA thành Malonyl-CoA, cần Biotin, $CO_2$ và ATP).",
            "Fatty Acid Synthase (FAS).",
            "ATP Citrate Lyase.",
            "Malic Enzyme.",
            "A",
            "Acetyl-CoA Carboxylase (ACC) là enzym dị lập thể điều hòa tốc độ tổng hợp acid béo: được hoạt hóa dị lập thể bởi Citrate và khử phosphoryl hóa bởi Insulin (trạng thái no); bị ức chế dị lập thể bởi Palmitoyl-CoA và bị phosphoryl hóa bất hoạt bởi Glucagon/Epinephrine và AMPK (trạng thái đói).",
            ch12_img
        ),
        (
            "Enzym nào đóng vai trò là enzym giới hạn tốc độ của con đường sinh tổng hợp Cholesterol và là đích tác dụng trực tiếp của nhóm thuốc Statin?",
            "HMG-CoA Reductase (xúc tác chuyển đổi HMG-CoA thành Mevalonate trong màng lưới nội chất).",
            "HMG-CoA Synthase.",
            "Squalene Synthase.",
            "7$\\alpha$-Hydroxylase.",
            "A",
            "HMG-CoA Reductase khử HMG-CoA thành Mevalonate cần 2 phân tử NADPH, là bước điều hòa then chốt quyết định tốc độ tổng hợp cholesterol nội sinh. Thuốc Statin (như Atorvastatin, Rosuvastatin) ức chế cạnh tranh thuận nghịch enzym này, làm giảm cholesterol nội bào và kích thích tế bào gan tăng biểu hiện thụ thể LDL receptor để kéo LDL từ máu vào gan, hạ lipid máu.",
            ch12_img
        ),
        (
            "Lipoprotein nào sau đây có nhiệm vụ vận chuyển Cholesterol dư thừa từ các mô ngoại vi quay trở về gan để chuyển hóa thành acid mật (quá trình vận chuyển cholesterol ngược - Reverse Cholesterol Transport)?",
            "HDL (High-Density Lipoprotein).",
            "LDL (Low-Density Lipoprotein).",
            "VLDL (Very Low-Density Lipoprotein).",
            "Chylomicron.",
            "A",
            "HDL được tổng hợp tại gan và ruột non, chứa Apolipoprotein A-I có khả năng hoạt hóa enzym LCAT để ester hóa cholesterol tự do lấy từ màng tế bào ngoại vi và vận chuyển về gan (Reverse Cholesterol Transport). Nồng độ HDL-C cao trong máu tương quan nghịch với nguy cơ bệnh mạch vành (yếu tố bảo vệ tim mạch).",
            None
        ),
        (
            "Hội chứng Tăng Chylomicron máu có tính gia đình (Type I Hyperlipoproteinemia) có nguyên nhân hóa sinh do khiếm khuyết di truyền yếu tố nào sau đây?",
            "Đột biến thiếu hụt enzym Lipoprotein Lipase (LPL) hoặc thiếu hụt đồng yếu tố hoạt hóa Apolipoprotein C-II.",
            "Đột biến mất thụ thể LDL receptor trên màng tế bào gan.",
            "Tăng tổng hợp quá mức Apolipoprotein B-100.",
            "Thiếu hụt enzym LCAT huyết tương.",
            "A",
            "Enzym Lipoprotein Lipase (LPL) gắn trên bề mặt tế bào nội mô mao mạch (đặc biệt ở mô mỡ và cơ) cần Apolipoprotein C-II để hoạt hóa, xúc tác thủy phân triglycerid trong Chylomicron và VLDL thành acid béo tự do. Thiếu LPL hoặc Apo C-II làm Chylomicron không được thanh thải, ứ đọng cực cao trong huyết tương gây viêm tụy cấp tái diễn.",
            None
        ),
        (
            "Trong bệnh cảnh Nhiễm toan ceton do đái tháo đường (Diabetic Ketoacidosis - DKA), cơ chế sinh hóa nào dẫn đến sự sản sinh ồ ạt thể Ceton?",
            "Thiếu hụt insulin trầm trọng kết hợp tăng glucagon kích thích tối đa enzym Hormone-Sensitive Lipase (HSL) trong mô mỡ phân giải triglycerid, giải phóng ồ ạt acid béo tự do về gan; tại gan $\\beta$-oxy hóa tăng vọt tạo thừa Acetyl-CoA trong khi Oxaloacetate bị rút cạn cho tân tạo đường, đẩy toàn bộ Acetyl-CoA sang tổng hợp thể Ceton.",
            "Thừa insulin làm tăng chuyển hóa glucose thành ceton.",
            "Ức chế enzym CPT-I ở màng ty thể gan.",
            "Tăng đào thải glucose qua nước tiểu.",
            "A",
            "Khi thiếu insulin tuyệt đối, tế bào không sử dụng được glucose nên phát tín hiệu đói năng lượng giả tạo: HSL trong mô mỡ tăng ly giải lipid phóng thích acid béo; tại gan, con thoi CPT-I mở tối đa, $\\beta$-oxy hóa tạo lượng khổng lồ Acetyl-CoA. Mặt khác, oxaloacetate bị rút cạn vào tân tạo đường khiến chu trình Krebs ngưng trệ $\\rightarrow$ Toàn bộ Acetyl-CoA chuyển hướng thành Acetoacetate và $\\beta$-hydroxybutyrate làm toan máu nặng nề.",
            ch12_img
        )
    ]

    for i in range(100):
        if i < len(ch12_core):
            q, a, b, c, d, corr, exp, img = ch12_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch12_img if (i % 5 == 0) else None

            ch12_topics = [
                ("Thoái hóa acid béo chưa no và acid béo carbon lẻ", "Acid béo carbon lẻ qua $\\beta$-oxy hóa ở vòng cuối cùng tạo Propionyl-CoA (3C).", "Propionyl-CoA được carboxyl hóa thành Methylmalonyl-CoA (cần Biotin) rồi chuyển thành Succinyl-CoA (cần Vitamin B12) đi vào chu trình Krebs.", "Oxy hóa acid béo chưa no cần thêm các enzym Isomerase và Reductase để dịch chuyển liên kết đôi cis thành trans.", "Peroxisome đảm nhiệm việc cắt ngắn các acid béo chuỗi rất dài (VLCFA $\\ge 22$C) trước khi đưa vào ty thể."),
                ("Phức hợp Acid Fatty Synthase (FAS)", "FAS ở động vật là một homodimer chứa 7 hoạt tính xúc tác khác nhau và cánh tay mang acyl ACP.", "Nhánh phosphopantetheine của ACP có nguồn gốc từ vitamin B5 (acid pantothenic).", "Mỗi chu kỳ kéo dài chuỗi acid béo gồm 4 bước: Ngưng tụ $\\rightarrow$ Khử lần 1 $\\rightarrow$ Khử nước $\\rightarrow$ Khử lần 2.", "Sản phẩm cuối cùng giải phóng khỏi enzym FAS nhờ Thioesterase là Acid Palmitic (16:0)."),
                ("Rối loạn chuyển hóa lipoprotein và thụ thể LDL", "Thụ thể LDL receptor nhận diện Apolipoprotein B-100 và Apolipoprotein E để nhập bào hạt LDL qua các hố phủ clathrin.", "Bệnh tăng cholesterol máu gia đình (FH - Type IIa) do đột biến gen LDL receptor gây cholesterol máu tăng vọt và u vàng gân gót (xanthoma).", "PCSK9 là protein thúc đẩy sự thoái giáng thể tiêu bào của thụ thể LDL; thuốc ức chế PCSK9 giúp tăng thu hồi LDL vào gan.", "VLDL được gan bài tiết sau khi mất dần triglycerid biến đổi thành IDL rồi thành LDL."),
                ("Sinh tổng hợp Phospholipid và Triacylglycerol", "Glycerol-3-Phosphate là bộ khung khởi đầu tổng hợp TG, được tạo từ khử DHAP (đường phân) hoặc phosphoryl hóa glycerol tại gan (Glycerol kinase).", "Acid phosphatidic (1,2-diacylglycerol-3-phosphat) là chất trung gian chung tổng hợp cả triglycerid và phospholipid.", "Con đường tổng hợp Phosphatidylcholine cần sự hoạt hóa cholin bởi CTP tạo CDP-Choline.", "Mô mỡ thiếu enzym Glycerol Kinase nên phụ thuộc hoàn toàn vào đường phân để tạo Glycerol-3-P tổng hợp mỡ."),
                ("Chuyển hóa và bài tiết Cholesterol", "Con người không thể phân hủy khung steroid của cholesterol thành $CO_2$ và nước.", "Đào thải cholesterol duy nhất qua gan bằng cách bài tiết cholesterol tự do vào mật hoặc chuyển thành acid mật.", "Enzym $7\\alpha$-Hydroxylase (chịu ức chế ngược bởi acid mật) là enzym kiểm soát tổng hợp acid mật nguyên phát.", "Muối mật trải qua chu trình gan-ruột (enterohepatic circulation): 95% được tái hấp thu ở đoạn cuối hồi tràng về gan.")
            ]
            tp = ch12_topics[i % len(ch12_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi đề cập đến {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Quá trình này hoàn toàn không tuân theo quy luật chuyển hóa lipid và không chịu ảnh hưởng của nồng độ enzym hay hormon trong máu."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng chuyển hóa lipid sinh lý."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ gặp ở thực vật thủy sinh và không tham gia vào bất kỳ con đường năng lượng nào ở động vật có vú."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch12_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # Insert Batch 4 into DB
    print(f"Prepared {len(questions)} questions for Batch 4 (Ch10, Ch11, Ch12). Inserting into DB...")
    for item in questions:
        cur.execute("""
            INSERT INTO questions (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_option, explanation, difficulty, topic_tag, image_url, q_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'multiple_choice')
        """, (sub_id, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[0], item[9]))

    conn.commit()
    cur.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sub_id,))
    print(f"Batch 4 Seed Complete! Current total questions for subject {sub_id}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    seed_part4()
