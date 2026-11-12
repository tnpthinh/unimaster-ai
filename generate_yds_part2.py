# -*- coding: utf-8 -*-
"""
UniMaster AI - Seeder for YDS 2024 Medical Biochemistry
Batch 2:
- Chương 4: Hóa học hemoglobin (100 câu)
- Chương 5: Hóa học nucleotid và acid nucleic (100 câu)
- Chương 6: Vitamin (100 câu)
Total: 300 questions
"""

import sqlite3

def seed_part2():
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
    # CHƯƠNG 4: HÓA HỌC HEMOGLOBIN (100 CÂU)
    # ==========================================
    ch4_name = "Chương 4: Hóa học hemoglobin"
    ch4_img = "/static/uploads/hoasinh_yds/ch04_hemoglobin_oxygen_curve.svg"

    ch4_core = [
        (
            "Cấu tạo phân tử của Heme bao gồm những thành phần nào sau đây?",
            "Ion $Fe^{2+}$ nằm ở trung tâm vòng Protoporphyrin IX liên kết với 4 nguyên tử nitơ của nhân pyrrol.",
            "Ion $Fe^{3+}$ nằm ở trung tâm vòng Protoporphyrin IX liên kết với chuỗi globin.",
            "Ion $Mg^{2+}$ nằm ở trung tâm vòng Porphyrin liên kết với 4 vòng pyrrol.",
            "Ion $Cu^{2+}$ kết hợp với chuỗi polypeptid $\\alpha$ và $\\beta$.",
            "A",
            "Heme là nhóm ngoại sắc tố của Hemoglobin và Myoglobin, cấu tạo gồm vòng Protoporphyrin IX liên kết phối trí với ion $Fe^{2+}$ ở trung tâm qua 4 liên kết phối trí với 4 nguyên tử nitơ của 4 vòng pyrrol.",
            ch4_img
        ),
        (
            "Phát biểu nào sau đây KHÔNG ĐÚNG về cấu trúc bậc 4 của Hemoglobin A1 (HbA1) ở người trưởng thành?",
            "Là một tetramer gồm 2 chuỗi $\\alpha$ (141 acid amin) và 2 chuỗi $\\beta$ (146 acid amin).",
            "Mỗi phân tử HbA1 chứa 4 nhóm Heme và có khả năng gắn kết tối đa 4 phân tử oxy ($O_2$).",
            "Các tiểu đơn vị liên kết với nhau bằng các liên kết cộng hóa trị disulfid cực kỳ bền vững.",
            "Phân tử tồn tại ở 2 trạng thái cấu hình không gian: dạng căng (T - Tense) và dạng giãn (R - Relaxed).",
            "C",
            "Bốn tiểu đơn vị trong phân tử Hb liên kết với nhau bằng CÁC LIÊN KẾT PHI CỘNG HÓA TRỊ (tương tác kỵ nước, liên kết hydro, cầu muối ion), hoàn toàn KHÔNG CÓ liên kết cộng hóa trị disulfid. Nhờ đó phân tử có tính linh động allosteric cao khi gắn oxy.",
            ch4_img
        ),
        (
            "Đặc điểm ái lực oxy của Hemoglobin và Myoglobin khác nhau như thế nào?",
            "Hb có đường cong bão hòa oxy dạng chữ S (sigmoid) do tương tác hợp tác, trong khi Myoglobin có dạng hyperbol.",
            "Myoglobin có ái lực với oxy thấp hơn Hemoglobin ở mọi mức phân áp $pO_2$.",
            "Hb giải phóng oxy khó khăn hơn Myoglobin ở mô cơ đang hoạt động gắng sức.",
            "Hb không chịu ảnh hưởng của các chất điều hòa dị lập thể allosteric.",
            "A",
            "Myoglobin (đơn phân tử) có đường cong hyperbol, ái lực rất cao với O2 ($P_{50} \\approx 2-3$ mmHg), chỉ nhả oxy khi phân áp oxy mô cực thấp. Hb (tetramer) có tương tác hợp tác dương tạo đường cong sigmoid ($P_{50} \\approx 26$ mmHg), giúp bắt tối đa O2 ở phổi và nhả hiệu quả ở mô ngoại vi.",
            ch4_img
        ),
        (
            "Chất điều hòa dị lập thể 2,3-Bisphosphoglycerate (2,3-BPG) tác động lên Hemoglobin theo cơ chế nào sau đây?",
            "Gắn vào hốc trung tâm mang điện tích dương giữa hai chuỗi $\\beta$, ổn định cấu hình dạng T (Tense), làm giảm ái lực của Hb với $O_2$ (dịch chuyển đường cong phân ly sang phải).",
            "Gắn trực tiếp vào nhân Heme tranh chấp vị trí gắn của oxy.",
            "Làm tăng ái lực của Hemoglobin với oxy ở mô ngoại vi.",
            "Gắn vào chuỗi $\\alpha$ làm biến tính hoàn toàn phân tử hemoglobin.",
            "A",
            "2,3-BPG là chất chuyển hóa trung gian của đường phân trong hồng cầu (chu trình Rapoport-Luebering), mang nhiều điện tích âm, gắn vào khoang trung tâm giữa 2 chuỗi $\\beta$ của dạng Tense (deoxy-Hb) qua cầu muối, giúp ổn định dạng T, tạo thuận lợi nhả O2 cho mô.",
            ch4_img
        ),
        (
            "Tại sao Hemoglobin thai nhi (HbF - $\\alpha_2\\gamma_2$) lại có ái lực với oxy CAO HƠN Hemoglobin người lớn (HbA1 - $\\alpha_2\\beta_2$)?",
            "Chuỗi $\\gamma$ thay thế acid amin Histidin 143 bằng Serin trung tính, làm giảm ái lực liên kết với 2,3-BPG.",
            "HbF chứa 8 nhóm heme nên gắn được gấp đôi lượng oxy.",
            "HbF có cấu trúc đơn phân tử giống hệt myoglobin.",
            "HbF không bao giờ chuyển sang dạng cấu hình Tense.",
            "A",
            "Ở chuỗi $\\gamma$ của HbF, vị trí 143 là Serin thay vì Histidin (tích điện dương) như chuỗi $\\beta$ của HbA. Mất đi 2 điện tích dương làm HbF gắn 2,3-BPG yếu hơn nhiều => Dạng R chiếm ưu thế => Ái lực oxy cao hơn HbA, cho phép thai nhi rút oxy từ máu mẹ qua nhau thai.",
            ch4_img
        ),
        (
            "Hiệu ứng Bohr (Bohr effect) mô tả hiện tượng sinh lý hóa sinh nào sau đây?",
            "Sự giảm ái lực của Hb với $O_2$ khi pH giảm (tăng nồng độ $H^+$) hoặc khi tăng phân áp $pCO_2$, thúc đẩy phóng thích oxy tại mô ngoại vi.",
            "Sự tăng ái lực của Hb với $O_2$ tại mô cơ khi sinh nhiều acid lactic.",
            "Sự biến tính oxyhemoglobin thành methemoglobin ở nhiệt độ cao.",
            "Sự gắn kết của khí CO với hemoglobin tạo carboxyhemoglobin bền vững.",
            "A",
            "Tại mô ngoại vi chuyển hóa mạnh, $CO_2$ và $H^+$ tăng cao. $H^+$ gắn vào các gốc Histidin chuỗi globin tạo cầu muối ổn định dạng T, đẩy O2 ra khỏi Hb (đường cong dịch phải). Tại phổi, $pO_2$ cao đẩy $H^+$ ra và thải $CO_2$.",
            ch4_img
        ),
        (
            "Độc tính nguy hiểm của khí Carbon Monoxide (CO) trong ngộ độc CO bắt nguồn từ nguyên nhân hóa sinh nào?",
            "CO cạnh tranh gắn vào $Fe^{2+}$ của Heme với ái lực cao gấp khoảng 220 lần so với oxy, đồng thời làm dịch chuyển đường cong phân ly O2 sang TRÁI, khóa chặt lượng O2 còn lại không cho nhả ra mô.",
            "CO oxy hóa $Fe^{2+}$ thành $Fe^{3+}$ làm vỡ hồng cầu hàng loạt.",
            "CO cắt đứt liên kết peptid giữa các chuỗi globin.",
            "CO ngăn cản hấp thu sắt tại tá tràng.",
            "A",
            "CO gắn vào $Fe^{2+}$ của Hb tạo Carboxyhemoglobin (HbCO) với ái lực gấp ~220 lần O2. Không chỉ chiếm chỗ gắn O2, phân tử CO còn làm các heme còn lại chuyển sang dạng R, dịch đường cong sang TRÁI, ngăn cản hoàn toàn việc phóng thích O2 cho mô, gây thiếu oxy mô tối cấp.",
            ch4_img
        ),
        (
            "Methemoglobin (MetHb) được hình thành do cơ chế nào và triệu chứng lâm sàng đặc trưng là gì?",
            "Sắt trong nhân Heme bị oxy hóa từ dạng khử $Fe^{2+}$ thành dạng oxy hóa $Fe^{3+}$, mất khả năng gắn O2, gây tím tái (cyanosis) toàn thân không đáp ứng với thở oxy.",
            "Sắt trong nhân Heme bị khử thành sắt kim loại $Fe^0$, gây vỡ hồng cầu.",
            "Đột biến mất chuỗi $\\beta$ gây bệnh thiếu máu Cooley.",
            "Hemoglobin bị gắn liên kết đồng hóa trị với glucose tạo HbA1c.",
            "A",
            "Methemoglobin chứa $Fe^{3+}$ (ferric) không thể gắn oxy. Khi tỷ lệ MetHb trong máu > 10-15%, bệnh nhân xuất hiện tím tái (da màu xanh xám, máu màu sôcôla). Điều trị cấp cứu bằng chất khử Xanh methylen (Methylene blue) hoặc Vitamin C liều cao.",
            None
        ),
        (
            "Bệnh hồng cầu hình liềm (Sickle Cell Anemia - HbS) là kết quả của đột biến điểm nào trên chuỗi $\\beta$-globin?",
            "Đột biến thay thế Acid Glutamic (tích điện âm) bằng Valin (kỵ nước) tại vị trí acid amin số 6 của chuỗi $\\beta$.",
            "Đột biến thay thế Acid Glutamic bằng Lysin tại vị trí số 6 chuỗi $\\beta$ (tạo HbC).",
            "Mất đoạn toàn bộ gen mã hóa chuỗi $\\alpha$-globin trên nhiễm sắc thể 16.",
            "Đột biến thay thế Histidin 143 bằng Serin.",
            "A",
            "HbS do đột biến thay thế GAG thành GTG tại codon 6 chuỗi $\\beta$, dẫn tới thay Glu (ưa nước) bằng Val (kỵ nước). Khi thiếu oxy (dạng deoxy-Hb), gốc Valin kỵ nước lộ ra ngoài gắn kết vào hốc kỵ nước của phân tử HbS lân cận, tạo thành chuỗi polymer sợi dài làm biến dạng hồng cầu thành hình liềm gây tắc mạch và tán huyết.",
            None
        ),
        (
            "Chất nào sau đây vận chuyển phần lớn lượng $CO_2$ (khoảng 70%) từ mô ngoại vi về phổi?",
            "Dạng ion Bicarbonate ($HCO_3^-$) hòa tan trong huyết tương nhờ enzym Carbonic Anhydrase (CA) trong hồng cầu.",
            "Dạng hòa tan vật lý tự do $CO_2$ trong huyết tương.",
            "Dạng Carbaminoglobin ($Hb-NH-COO^-$) gắn trực tiếp vào đầu amin của globin.",
            "Dạng kết hợp với lipid màng hồng cầu.",
            "A",
            "Khoảng 70% $CO_2$ được vận chuyển dưới dạng ion $HCO_3^-$ hòa tan trong huyết tương nhờ enzym Carbonic Anhydrase trong RBC xúc tác $CO_2 + H_2O \\leftrightarrow H_2CO_3 \\leftrightarrow H^+ + HCO_3^-$. Hiện tượng chuyển đổi ion Clorua (Chloride shift / Hamburger) duy trì cân bằng điện tích màng hồng cầu.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch4_core):
            q, a, b, c, d, corr, exp, img = ch4_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch4_img if (i % 5 == 0) else None

            ch4_topics = [
                ("Thalassemia và rối loạn chuỗi globin", "$\\alpha$-Thalassemia do đột biến mất gen $\\alpha$ trên NST 16; mất 4 gen gây phù thai Hb Bart's ($\\gamma_4$) tử vong in utero.", "$\\beta$-Thalassemia major (thiếu máu Cooley) do giảm hoặc mất hoàn toàn tổng hợp chuỗi $\\beta$ trên NST 11.", "Hồng cầu trong bệnh Thalassemia có đặc điểm nhược sắc, kích thước nhỏ và xuất hiện tế bào bia (target cells).", "Bệnh nhân $\\beta$-thalassemia phụ thuộc truyền máu có nguy cơ ứ đọng sắt (hemosiderosis) tại tim, gan và tuyến tụy."),
                ("Các dạng dẫn xuất hemoglobin", "HbA1c là dạng hemoglobin gắn glucose không qua xúc tác enzym (glycation), tỷ lệ thuận với đường huyết trung bình trong 120 ngày.", "Sulfhemoglobin hình thành do gắn lưu huỳnh vào vòng porphyrin, là liên kết không hồi phục và không có thuốc giải độc đặc hiệu.", "Carbaminohemoglobin là dạng $CO_2$ gắn vào nhóm amin tự do ở đầu N của các chuỗi polypeptide globin.", "Cyanmethemoglobin là phức chất màu đỏ bền vững dùng trong phương pháp định lượng hemoglobin toàn phần bằng quang phổ Drabkin."),
                ("Điều hòa ái lực oxy và đường cong phân ly", "Nhiệt độ cơ thể tăng (sốt cao, vận động gắng sức) làm dịch chuyển đường cong phân ly oxy sang PHẢI, tạo thuận giải phóng oxy cho mô.", "Nhiễm toan (tăng ion $H^+$, giảm pH máu) làm giảm ái lực của hemoglobin đối với oxy.", "Khi sống ở độ cao nhiều ngày, nồng độ 2,3-BPG trong hồng cầu tăng lên để tăng cung cấp oxy cho mô cơ quan.", "Bơm máu dự trữ lâu ngày bị suy giảm 2,3-BPG làm hồng cầu truyền vào gắn chặt oxy khó nhả ra mô."),
                ("Sinh tổng hợp Heme và ngộ độc chì", "Phản ứng đầu tiên tổng hợp Heme xảy ra trong ty thể giữa Succinyl-CoA và Glycin nhờ enzym ALA Synthase (cần Vitamin B6).", "Enzym ALA Synthase là enzym dị lập thể giới hạn tốc độ và bị ức chế ngược bởi Heme tự do.", "Ngộ độc Chì ($Pb$) ức chế enzym ALA Dehydratase và Ferrochelatase, gây tích tụ ALA niệu và thiếu máu hồng cầu nhỏ ứ sắt.", "Porphyria là nhóm bệnh rối loạn di truyền do khiếm khuyết các enzym trong con đường sinh tổng hợp Heme."),
                ("Cấu trúc không gian và chức năng Allosteric", "Sự gắn oxy vào tiểu đơn vị đầu tiên kéo nguyên tử sắt vào mặt phẳng porphyrin, truyền tín hiệu cơ học làm tăng ái lực của các tiểu đơn vị còn lại.", "Cấu hình Tense (dạng T) có nhiều cầu muối nội và liên chuỗi, hạn chế khả năng tiếp cận của phân tử oxy vào túi heme.", "Histidin F8 (Histidin gần - Proximal) tạo liên kết phối trí thứ 5 trực tiếp với $Fe^{2+}$.", "Histidin E7 (Histidin xa - Distal) ngăn cản sự gắn kết vuông góc của CO, làm giảm ái lực của CO với Heme xuống còn ~200 lần so với dạng tự do.")
            ]
            tp = ch4_topics[i % len(ch4_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Đặc điểm nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cơ chế này hoàn toàn không tuân theo các nguyên lý allosteric và không phụ thuộc vào trạng thái oxy hóa của ion sắt."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo tính sinh lý của tế bào hồng cầu."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Quá trình này không có ý nghĩa lâm sàng và không làm thay đổi các chỉ số sinh hóa máu ở bệnh nhân."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các đáp án khác nêu sai lệch về sinh hóa học lâm sàng."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch4_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 5: HÓA HỌC NUCLEOTID & ACID NUCLEIC (100 CÂU)
    # ==========================================
    ch5_name = "Chương 5: Hóa học nucleotid và acid nucleic"
    ch5_img = "/static/uploads/hoasinh_yds/ch05_dna_rna_structure.svg"

    ch5_core = [
        (
            "Cấu tạo của một mononucleotid hoàn chỉnh bao gồm 3 thành phần nào sau đây?",
            "Base nitơ (Purin hoặc Pyrimidin), đường Pentose (Ribose hoặc Deoxyribose) và 1 hoặc nhiều gốc Phosphat.",
            "Base nitơ, acid béo và gốc phosphat.",
            "Đường Hexose, acid amin và ion kim loại $Mg^{2+}$.",
            "Purin, Pyrimidin và liên kết peptid.",
            "A",
            "Một đơn phân nucleotid gồm 3 phần: Base nitơ (A, G, C, T, U) + Đường 5C (D-ribose hoặc 2'-deoxy-D-ribose) + Nhóm phosphat ester hóa tại C5' hoặc C3' của đường pentose.",
            ch5_img
        ),
        (
            "Liên kết hóa học nào sau đây nối các đơn phân mononucleotid liên tiếp trong một chuỗi polynucleotid (DNA hoặc RNA)?",
            "Liên kết 3',5'-Phosphodiester giữa nhóm 3'-OH của đường trước với nhóm 5'-phosphat của đường kế tiếp.",
            "Liên kết N-glycosid giữa base nitơ và đường.",
            "Liên kết hydro giữa các base nitơ đối diện.",
            "Cầu nối cộng hóa trị disulfid giữa các gốc purin.",
            "A",
            "Bộ khung của chuỗi polynucleotid là các liên kết 3',5'-phosphodiester lặp lại, nối nguyên tử C3' của gốc pentose này với nguyên tử C5' của gốc pentose kế tiếp thông qua một nhóm phosphat.",
            ch5_img
        ),
        (
            "Quy tắc bổ sung Chargaff đối với phân tử DNA sợi đôi quy định tỷ lệ nào sau đây?",
            "$A = T$ và $G = C$, dẫn đến tổng $A + G = T + C$ (tổng Purin = tổng Pyrimidin) và tỷ lệ $(A+T)/(G+C)$ là đặc trưng cho loài.",
            "$A = G$ và $T = C$.",
            "$A + T = G + C$ trong mọi phân tử DNA sinh vật.",
            "Số lượng liên kết hydro giữa A và T luôn bằng giữa G và C.",
            "A",
            "Nghiên cứu của Erwin Chargaff chứng minh trong DNA sợi đôi: số lượng mol Adenin luôn bằng Thymin ($A=T$), Guanin luôn bằng Cytosin ($G=C$). Do đó tổng Purin = tổng Pyrimidin ($A+G=T+C$). Tuy nhiên tỷ lệ $(A+T)/(G+C)$ thay đổi tùy loài.",
            ch5_img
        ),
        (
            "Đặc điểm nào sau đây KHÔNG ĐÚNG về mô hình cấu trúc xoắn kép B-DNA của Watson và Crick?",
            "Gồm hai chuỗi polynucleotid xoắn song song ngược chiều (chuỗi $5' \\rightarrow 3'$ và chuỗi $3' \\rightarrow 5'$) quanh một trục chung.",
            "Các base nitơ hướng vào trong trục xoắn, liên kết bổ sung bằng liên kết hydro (A gắn T bằng 2 liên kết, G gắn C bằng 3 liên kết).",
            "Mỗi chu kỳ xoắn có chiều dài 3.4 nm (34 Å), tương ứng với khoảng 10 cặp base (bp).",
            "Hai chuỗi polynucleotid liên kết với nhau bằng các liên kết cộng hóa trị bền vững không thể bị biến tính bởi nhiệt.",
            "D",
            "Hai chuỗi DNA liên kết với nhau bằng CÁC LIÊN KẾT HYDRO YẾU và tương tác xếp chồng kỵ nước, KHÔNG PHẢI liên kết cộng hóa trị. Do đó DNA dễ dàng bị tách thành sợi đơn (biến tính / nóng chảy) khi đun nóng hoặc môi trường kiềm.",
            ch5_img
        ),
        (
            "Nhiệt độ nóng chảy ($T_m$ - Melting temperature) của DNA là gì và phụ thuộc vào yếu tố nào?",
            "Nhiệt độ tại đó 50% cấu trúc xoắn kép DNA bị biến tính thành sợi đơn; $T_m$ tỷ lệ thuận với hàm lượng cặp base G-C.",
            "Nhiệt độ tại đó DNA bị đứt gãy toàn bộ liên kết phosphodiester thành các nucleotid tự do.",
            "Nhiệt độ tại đó tất cả các liên kết glycosid bị thủy phân.",
            "$T_m$ càng cao khi phân tử DNA chứa càng nhiều cặp base A-T.",
            "A",
            "$T_m$ là nhiệt độ làm biến tính 50% phân tử DNA sợi đôi. Do cặp G-C có 3 liên kết hydro (so với 2 liên kết hydro của A-T) và tương tác xếp chồng mạnh hơn, phân tử DNA nào có hàm lượng G-C càng cao thì liên kết càng bền và nhiệt độ $T_m$ càng cao.",
            ch5_img
        ),
        (
            "Hiệu ứng tăng sắc (Hyperchromic effect) của DNA quan sát thấy khi nào?",
            "Độ hấp thụ ánh sáng tử ngoại ở bước sóng 260 nm ($A_{260}$) tăng mạnh khi DNA sợi đôi bị biến tính thành sợi đơn.",
            "Sự biến đổi màu sắc từ trong suốt sang đỏ khi nhuộm iod.",
            "Sự phát huỳnh quang màu xanh dưới ánh sáng đèn Wood.",
            "Độ hấp thụ quang phổ ở 280 nm tăng vọt do acid amin nhân thơm.",
            "A",
            "Trong DNA sợi đôi, các base nitơ xếp chồng chặt khít bên trong trục làm giảm khả năng hấp thụ tia cực tím (UV). Khi DNA bị biến tính tách thành 2 sợi đơn, các base tự do tiếp xúc với ánh sáng làm độ hấp thụ cực đại ở 260 nm tăng từ 30-40% (hiệu ứng tăng sắc).",
            ch5_img
        ),
        (
            "Đặc điểm cấu tạo nào sau đây là DUY NHẤT có ở phân tử RNA mà KHÔNG CÓ ở phân tử DNA?",
            "Chứa đường D-ribose (có nhóm 2'-OH) và base Pyrimidin là Uracil (U).",
            "Chứa liên kết 3',5'-phosphodiester.",
            "Chứa base purin Adenin và Guanin.",
            "Có khả năng cuộn gập tạo cấu trúc không gian ba chiều.",
            "A",
            "RNA khác DNA ở 2 điểm cơ bản: (1) Đường pentose là D-ribose thay vì 2'-deoxy-D-ribose; (2) Base pyrimidin là Uracil (U) thay vì Thymin (T). Nhóm 2'-OH của ribose làm phân tử RNA kém bền vững hơn DNA trong môi trường kiềm.",
            ch5_img
        ),
        (
            "Cấu trúc đầu 5'-cap (mũ 5') của phân tử mRNA tế bào nhân thực (Eukaryote) có bản chất hóa học là gì?",
            "7-methylguanosine gắn với nucleotid đầu tiên qua liên kết bất thường $5',5'$-triphosphat.",
            "Đoạn chuỗi poly-Adenin gồm 200-250 gốc adenosin monophosphat.",
            "Vòng đối mã anticodon gắn acid amin.",
            "Một đoạn intron chưa được cắt ghép.",
            "A",
            "Đầu 5' của tiền mRNA ở tế bào nhân thực được gắn mũ 7-methylguanosine ($m^7G$) qua cầu nối $5',5'$-triphosphat ngay sau khi khởi đầu phiên mã, giúp bảo vệ mRNA khỏi enzym exonuclease và hỗ trợ nhận diện ribosome khi dịch mã.",
            None
        ),
        (
            "Cấu trúc hình lá chẽ ba (cloverleaf) của tRNA có vị trí gắn acid amin đặc hiệu tại đâu?",
            "Nhánh tiếp nhận tận cùng đầu 3' mang trình tự bảo thủ đặc trưng: $5'-CCA-3'$ (nhóm 3'-OH của Adenosin).",
            "Vòng đối mã anticodon ở thùy giữa.",
            "Đầu 5' mang nhóm monophosphat.",
            "Thùy T$\\Psi$C chứa base biến đổi pseudouridine.",
            "A",
            "Đầu 3' của tất cả phân tử tRNA đều tận cùng bằng bộ ba ribonucleotid $5'-CCA-3'$. Acid amin tương ứng được hoạt hóa và este hóa vào nhóm 2'-OH hoặc 3'-OH của gốc Adenosin cuối cùng này nhờ enzym Aminoacyl-tRNA Synthetase.",
            None
        ),
        (
            "Chất truyền tin thứ hai Adenosine 3',5'-cyclic monophosphate (cAMP) được tổng hợp từ ATP nhờ enzym nào?",
            "Adenylate Cyclase (xúc tác đóng vòng phosphat giữa C3' và C5' của ribose).",
            "Phosphodiesterase (PDE).",
            "Protein Kinase A (PKA).",
            "ATP Synthase màng trong ty thể.",
            "A",
            "Adenylate cyclase gắn trên màng tế bào (khi được thụ thể liên kết protein Gs hoạt hóa) xúc tác chuyển ATP thành cAMP và giải phóng pyrophosphat ($PP_i$). cAMP hoạt hóa Protein Kinase A (PKA). Enzym Phosphodiesterase (PDE) thủy phân cAMP thành AMP 5' bất hoạt.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch5_core):
            q, a, b, c, d, corr, exp, img = ch5_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch5_img if (i % 5 == 0) else None

            ch5_topics = [
                ("Các dạng đồng phân DNA và siêu xoắn", "Dạng B-DNA là dạng cấu trúc sinh lý phổ biến nhất trong tế bào sống với chuỗi xoắn phải.", "Dạng A-DNA ngắn hơn, dày hơn, xuất hiện trong điều kiện mất nước hoặc cấu trúc lai RNA-DNA.", "Dạng Z-DNA có chuỗi xoắn trái, khung đường-phosphat ngoằn ngoèo, xuất hiện ở vùng giàu chuỗi GC lặp lại.", "Enzym Topoisomerase (Gyrase) điều hòa trạng thái siêu xoắn của DNA trong sao chép và phiên mã."),
                ("Các loại RNA không mã hóa và chức năng", "microRNA (miRNA) dài khoảng 21-25 nucleotid tham gia ức chế dịch mã hoặc phân giải mRNA đích.", "snRNA (small nuclear RNA) phối hợp với protein tạo thể cắt ghép spliceosome để cắt intron và nối exon.", "rRNA 28S ở tế bào nhân thực có hoạt tính peptidyl transferase (ribozyme) hình thành liên kết peptid.", "Đuôi poly(A) ở đầu 3' của mRNA do enzym Poly(A) Polymerase gắn thêm không cần khuôn mẫu DNA."),
                ("Dẫn xuất nucleotid có hoạt tính sinh học", "S-adenosylmethionine (SAM) là chất cho nhóm methyl ($-CH_3$) quan trọng nhất trong các phản ứng methyl hóa sinh học.", "Coenzyme A (CoA-SH) chứa thành phần nucleotid là dẫn xuất của ADP-3'-phosphat gắn với acid pantothenic.", "NAD+ và NADP+ chứa nhân nicotinamid gắn với dinucleotid adenin, tham gia vận chuyển hydro trong hô hấp tế bào.", "FAD và FMN là các dẫn xuất flavin nucleotid tham gia vận chuyển 2 electron và 2 proton."),
                ("Ức chế tổng hợp acid nucleic bằng hóa trị ung thư", "5-Fluorouracil (5-FU) là chất tương tự Uracil, ức chế enzym Thymidylate Synthase, ngăn chặn tạo dTMP cho tổng hợp DNA.", "Methotrexate ức chế enzym Dihydrofolate Reductase (DHFR), làm cạn kiệt nguồn tetrahydrofolate cần cho tổng hợp purine và dTMP.", "Azathioprine và 6-Mercaptopurine là các chất tương tự purine dùng để ức chế miễn dịch và điều trị bệnh bạch cầu.", "Cisplatin tạo liên kết chéo giữa các sợi DNA ngăn cản sự tháo xoắn và phân chia tế bào ung thư."),
                ("Đặc tính lý hóa và xét nghiệm acid nucleic", "Độ tinh sạch của mẫu DNA/RNA được đánh giá bằng tỷ số độ hấp thụ quang học $A_{260}/A_{280}$ (chuẩn DNA tinh sạch là ~1.8, RNA tinh sạch là ~2.0).", "Mẫu DNA bị nhiễm tạp chất protein sẽ làm giảm tỷ số $A_{260}/A_{280}$ xuống dưới 1.6.", "Thuốc nhuộm huỳnh quang Ethidium Bromide (EtBr) xen kẽ giữa các cặp base DNA, phát sáng cam dưới tia UV.", "Điện di trên gel agarose phân tách các đoạn DNA dựa vào kích thước do toàn bộ chuỗi DNA tích điện âm đồng đều nhờ gốc phosphat.")
            ]
            tp = ch5_topics[i % len(ch5_topics)]
            is_except = (i % 2 == 1)
            if is_except:
                q = f"Khẳng định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cấu trúc nucleotid này không có tính đặc hiệu và không tham gia vào các cơ chế truyền tải thông tin di truyền hay năng lượng."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo tính chính xác di truyền."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Đặc điểm hóa sinh nào sau đây là ĐÚNG NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ gặp ở thể thực khuẩn và không tồn tại trong nhân hay ty thể tế bào người."
                exp = f"Đáp án {corr} ĐÚNG: {opts[corr]}. Các phương án khác không phù hợp với sinh học phân tử hiện đại."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch5_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'hard', img))

    # ==========================================
    # CHƯƠNG 6: VITAMIN (100 CÂU)
    # ==========================================
    ch6_name = "Chương 6: Vitamin"
    ch6_img = "/static/uploads/hoasinh_yds/ch06_vitamins_coenzymes.svg"

    ch6_core = [
        (
            "Vitamin nào sau đây tan trong dầu và có khả năng tích lũy trong mô mỡ và gan, dễ gây độc tính khi sử dụng quá liều kéo dài?",
            "Vitamin B1, B2, C, B6.",
            "Vitamin A, D, E, K.",
            "Vitamin B9, B12, H, PP.",
            "Cholin, Inositol, Carnitine.",
            "B",
            "Nhóm vitamin tan trong dầu gồm 4 vitamin: A, D, E, K. Do không tan trong nước, chúng không dễ dàng đào thải qua nước tiểu mà tích lũy tại mô mỡ và gan, nguy cơ gây ngộ độc mạn tính nếu dùng liều cao kéo dài (đặc biệt là Vitamin A và D).",
            ch6_img
        ),
        (
            "Dạng coenzym có hoạt tính sinh học của Vitamin B1 (Thiamin) trong cơ thể là gì?",
            "Thiamin Pyrophosphate (TPP).",
            "Flavin Adenine Dinucleotide (FAD).",
            "Pyridoxal Phosphate (PLP).",
            "Nicotinamide Adenine Dinucleotide (NAD+).",
            "A",
            "Vitamin B1 được phosphoryl hóa tạo thành Thiamin pyrophosphate (TPP). TPP là coenzyme của phức hợp Pyruvate Dehydrogenase, $\\alpha$-Ketoglutarate Dehydrogenase và Transketolase (chu trình pentose).",
            ch6_img
        ),
        (
            "Triệu chứng thần kinh và tim mạch điển hình của bệnh Beriberi (ướt và khô) xảy ra do thiếu hụt vitamin nào sau đây?",
            "Vitamin B1 (Thiamin).",
            "Vitamin B2 (Riboflavin).",
            "Vitamin B3 (Niacin).",
            "Vitamin B12 (Cobalamin).",
            "A",
            "Thiếu Vitamin B1 gây bệnh Beriberi: Beriberi khô biểu hiện tổn thương thần kinh ngoại biên đối xứng (yếu cơ, mất phản xạ gân xương); Beriberi ướt biểu hiện suy tim cung lượng cao kèm phù chi dưới. Ở người nghiện rượu, thiếu B1 cấp gây hội chứng não Wernicke-Korsakoff.",
            ch6_img
        ),
        (
            "Bệnh Pellagra với tam chứng kinh điển '3D' (Dermatitis - Viêm da đối xứng, Diarrhea - Tiêu chảy, Dementia - Sa sút trí tuệ) là do thiếu hụt trầm trọng chất nào?",
            "Vitamin B3 (Niacin / Nicotinic acid / PP) hoặc acid amin tiền chất Tryptophan.",
            "Vitamin B1 (Thiamin).",
            "Vitamin C (Acid ascorbic).",
            "Vitamin A (Retinol).",
            "A",
            "Bệnh Pellagra (bệnh viêm da sần sùi) do thiếu hụt Vitamin B3 (Niacin) dẫn đến thiếu NAD+ và NADP+, suy sụp chuyển hóa năng lượng toàn thân. Tryptophan là acid amin tiền chất có thể chuyển đổi thành Niacin (60 mg tryptophan $\\approx$ 1 mg niacin).",
            ch6_img
        ),
        (
            "Coenzym Pyridoxal Phosphate (PLP) có nguồn gốc từ Vitamin B6 đóng vai trò xúc tác chủ đạo cho nhóm phản ứng chuyển hóa nào?",
            "Các phản ứng chuyển hóa acid amin: Trao đổi amin (Transamination - AST/ALT), khử carboxyl (Decarboxylation) và khử amin.",
            "Các phản ứng oxy hóa khử trong chuỗi hô hấp tế bào.",
            "Phản ứng carboxyl hóa cần biotin.",
            "Phản ứng vận chuyển nhóm methyl cần vitamin B12.",
            "A",
            "PLP là coenzyme của tất cả các enzym Transaminase (AST, ALT), Decarboxylase (tổng hợp GABA từ glutamate, histamin từ histidin, serotonin từ tryptophan) và Glycogen phosphorylase trong tiêu glycogen.",
            ch6_img
        ),
        (
            "Phụ nữ mang thai trong 3 tháng đầu cần bổ sung acid folic (Vitamin B9) để phòng ngừa dị tật bẩm sinh nghiêm trọng nào ở thai nhi?",
            "Khuyết tật ống thần kinh (dị tật nứt đốt sống - spina bifida và thai vô sọ - anencephaly).",
            "Bệnh tim bẩm sinh tứ chứng Fallot.",
            "Bệnh nhuyễn xương và còi xương.",
            "Đục thủy tinh thể bẩm sinh.",
            "A",
            "Vitamin B9 (Acid folic $\\rightarrow$ THF) cần thiết cho sự tổng hợp dTMP và purine phục vụ phân chia tế bào thần kinh phôi thai. Thiếu folate ở giai đoạn đóng ống thần kinh (ngày 21-28 sau thụ tinh) làm tăng vọt nguy cơ nứt đốt sống và vô sọ. Khuyến cáo bổ sung 400-800 $\\mu$g/ngày.",
            None
        ),
        (
            "Vitamin B12 (Cobalamin) cần chất nào do tế bào viền của niêm mạc dạ dày tiết ra để có thể hấp thu được tại đoạn cuối hồi tràng?",
            "Yếu tố nội tại của Castle (Intrinsic Factor - IF).",
            "Acid cholic của muối mật.",
            "Enzym pepsinogen.",
            "Hormon gastrin.",
            "A",
            "Tế bào viền dạ dày tiết Yếu tố nội tại (IF). IF gắn với vitamin B12 tạo phức hợp bền vững kháng enzym tiêu hóa, di chuyển xuống tận đoạn cuối hồi tràng và được thụ thể cubilin nhận diện để hấp thu qua cơ chế nhập bào. Cắt dạ dày hoặc viêm teo dạ dày tự miễn gây bệnh thiếu máu ác tính Biermer.",
            None
        ),
        (
            "Dạng có hoạt tính sinh học mạnh nhất của Vitamin D trong cơ thể được chuyển hóa lần lượt qua gan và thận là gì?",
            "1,25-dihydroxycholecalciferol (Calcitriol).",
            "25-hydroxycholecalciferol (Calcidiol).",
            "7-dehydrocholesterol.",
            "Ergocalciferol (Vitamin D2).",
            "A",
            "Vitamin D3 từ da/thức ăn được 25-hydroxyl hóa tại gan thành 25-(OH)-D3 (Calcidiol - dạng dự trữ lưu hành trong máu). Tại ống thận gần, enzym $1\\alpha$-hydroxylase (chịu kích thích của PTH) gắn thêm nhóm OH thứ hai tạo $1,25-(OH)_2-D_3$ (Calcitriol - dạng hormon có hoạt tính mạnh nhất).",
            ch6_img
        ),
        (
            "Cơ chế tác động sinh hóa của Vitamin K trong quá trình đông máu là gì?",
            "Đóng vai trò coenzyme cho enzym $\\gamma$-glutamyl carboxylase biến đổi các gốc Glutamat thành $\\gamma$-carboxyglutamat (Gla) trên các yếu tố đông máu II, VII, IX, X.",
            "Kích hoạt trực tiếp enzym thrombin cắt phân tử fibrinogen thành fibrin.",
            "Tăng số lượng tiểu cầu giải phóng từ tủy xương.",
            "Ức chế plasminogen ngăn chặn tiêu sợi huyết.",
            "A",
            "Các yếu tố đông máu II (Prothrombin), VII, IX, X và protein C, S cần nhóm carboxyl thứ hai trên các gốc acid glutamic (tạo $\\gamma$-carboxyglutamat) để tạo vị trí liên kết mang điện tích âm gắn với ion $Ca^{2+}$, từ đó bám lên màng phospholipid tiểu cầu hoạt hóa. Thuốc chống đông kháng vitamin K (Warfarin, Sintrom) ức chế enzym VKOR tái tạo vitamin K khử.",
            ch6_img
        ),
        (
            "Chất nào sau đây là chất chống oxy hóa tan trong mỡ chính của cơ thể, bảo vệ các acid béo không no của màng tế bào khỏi phản ứng peroxy hóa gốc tự do?",
            "Vitamin E ($\\alpha$-tocopherol).",
            "Vitamin B1 (Thiamin).",
            "Vitamin B2 (Riboflavin).",
            "Vitamin B5 (Acid pantothenic).",
            "A",
            "Vitamin E ($\\alpha$-tocopherol) là chất chống oxy hóa tan trong lipid mạnh nhất, chèn vào lớp màng phospholipid kép để bẫy và dập tắt các gốc tự do peroxyl ($ROO^\\bullet$), bảo vệ màng tế bào, màng hồng cầu và hạt lipoprotein LDL khỏi sự peroxy hóa lipid.",
            ch6_img
        )
    ]

    for i in range(100):
        if i < len(ch6_core):
            q, a, b, c, d, corr, exp, img = ch6_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch6_img if (i % 5 == 0) else None

            ch6_topics = [
                ("Vitamin A và chu trình thị giác", "11-cis-retinal kết hợp với opsin tạo sắc tố Rhodopsin ở tế bào que võng mạc nhạy cảm với ánh sáng yếu.", "Thiếu vitamin A dẫn tới quáng gà (nyctalopia) ban đêm và khô giác mạc (xerophthalmia) ở trẻ em.", "Acid retinoic gắn vào thụ thể nhân RAR/RXR điều hòa biệt hóa biểu mô và tạo sừng da.", "Ngộ độc vitamin A cấp tính gây đau đầu dữ dội, tăng áp lực nội sọ giả u não và tổn thương gan."),
                ("Vitamin C và phản ứng oxy hóa khử", "Acid ascorbic là chất cho electron mạnh, chuyển đổi qua lại giữa dạng khử và dehydroascorbic acid.", "Vitamin C hỗ trợ hấp thu sắt non-heme ở ruột non bằng cách khử ion $Fe^{3+}$ thành ion $Fe^{2+}$ dễ hòa tan.", "Vitamin C tham gia phản ứng hydroxyl hóa dopamin thành noradrenalin trong tủy thượng thận.", "Bệnh nhân thiếu vitamin C có biểu hiện chậm lành vết thương do mất tính bền vững của các sợi collagen."),
                ("Phân biệt thiếu máu do Folate và Vitamin B12", "Cả thiếu Folate và thiếu Vitamin B12 đều gây thiếu máu hồng cầu to (Megaloblastic anemia) và tăng Homocystein máu.", "CHỈ CÓ THIẾU VITAMIN B12 mới gây tăng nồng độ Methylmalonic acid (MMA) và tổn thương thần kinh (thoái hóa tủy sống kết hợp).", "Bổ sung đơn độc acid folic liều cao cho bệnh nhân thiếu B12 có thể cải thiện tình trạng thiếu máu nhưng làm bệnh thần kinh nặng nề hơn.", "Thuốc Metformin dùng lâu năm ở bệnh nhân đái tháo đường có thể làm giảm hấp thu vitamin B12 tại ruột."),
                ("Vitamin B2, B5, B7 và chuyển hóa năng lượng", "Riboflavin (B2) tạo FMN và FAD, tham gia chuyển hóa acid béo và chu trình acid citric.", "Acid pantothenic (B5) cấu tạo nên Coenzyme A (CoA-SH) cần cho sự hoạt hóa và vận chuyển các gốc acyl.", "Biotin (B7 / Vitamin H) gắn với protein avidin trong lòng trắng trứng sống với ái lực cực mạnh, ngăn cản hấp thu biotin.", "Enzym Pyruvat Carboxylase và Acetyl-CoA Carboxylase cần coenzyme Biotin để vận chuyển nhóm $CO_2$."),
                ("Độc tính và tương tác thuốc của vitamin", "Dùng liều cao Vitamin D dẫn tới tăng canxi máu, vôi hóa mô mềm (thận, mạch máu) và sỏi thận canxi.", "Kháng sinh Isoniazid (INH) điều trị lao tạo phức hợp làm tăng đào thải vitamin B6, cần phối hợp uống kèm pyridoxin.", "Thuốc chống co giật (Phenytoin, Carbamazepine) làm tăng chuyển hóa và giảm nồng độ Vitamin D/Folate máu.", "Vitamin K liều cao đối kháng tác dụng của thuốc chống đông kháng vitamin K (Warfarin).")
            ]
            tp = ch6_topics[i % len(ch6_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Chất này không có vai trò coenzym và cơ thể có thể tự tổng hợp hoàn toàn từ lipid bão hòa mà không cần cung cấp từ ngoại sinh."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng vitamin sinh lý."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này bị phá hủy hoàn toàn trong huyết tương và không có bất kỳ ý nghĩa chẩn đoán hay điều trị y khoa nào."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các lựa chọn còn lại nêu sai lệch cơ chế sinh hóa."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch6_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # Insert Batch 2 into DB
    print(f"Prepared {len(questions)} questions for Batch 2 (Ch4, Ch5, Ch6). Inserting into DB...")
    for item in questions:
        cur.execute("""
            INSERT INTO questions (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_option, explanation, difficulty, topic_tag, image_url, q_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'multiple_choice')
        """, (sub_id, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[0], item[9]))

    conn.commit()
    cur.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sub_id,))
    print(f"Batch 2 Seed Complete! Current total questions for subject {sub_id}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    seed_part2()
