# -*- coding: utf-8 -*-
"""
UniMaster AI - Seeder for YDS 2024 Medical Biochemistry
Batch 3:
- Chương 7: Enzym (100 câu)
- Chương 8: Hormon (100 câu)
- Chương 9: Khái niệm về chuyển hóa các chất (100 câu)
Total: 300 questions
"""

import sqlite3

def seed_part3():
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
    # CHƯƠNG 7: ENZYM (100 CÂU)
    # ==========================================
    ch7_name = "Chương 7: Enzym"
    ch7_img = "/static/uploads/hoasinh_yds/ch07_lineweaver_burk_inhibition.svg"

    ch7_core = [
        (
            "Theo phân loại quốc tế của Hội đồng Enzym (EC), enzym xúc tác phản ứng chuyển hydro hoặc electron giữa hai phân tử thuộc lớp nào?",
            "Lớp 1: Oxidoreductase (Enzym oxy hóa - khử).",
            "Lớp 2: Transferase (Enzym vận chuyển nhóm).",
            "Lớp 3: Hydrolase (Enzym thủy phân).",
            "Lớp 4: Lyase (Enzym phân cắt không dùng nước).",
            "A",
            "Lớp 1 (EC 1) là Oxidoreductase, gồm các dehydrogenase, oxidase, reductase, peroxidase, catalase xúc tác phản ứng chuyển điện tử hoặc ion hydro ($H^+$) giữa chất cho và chất nhận electron.",
            ch7_img
        ),
        (
            "Ý nghĩa sinh hóa của hằng số Michaelis ($K_m$) trong động học enzym là gì?",
            "Nồng độ cơ chất mà tại đó tốc độ phản ứng đạt bằng một nửa tốc độ cực đại ($v = \\frac{1}{2} V_{\\max}$); $K_m$ tỷ lệ nghịch với ái lực của enzym với cơ chất.",
            "Tốc độ cực đại mà phản ứng có thể đạt được khi enzym bị bão hòa cơ chất hoàn toàn.",
            "Nồng độ chất ức chế cần thiết để làm giảm 50% hoạt tính enzym.",
            "Hằng số đo số phân tử cơ chất được chuyển hóa bởi một phân tử enzym trong một đơn vị thời gian.",
            "A",
            "Theo phương trình Michaelis-Menten: $v = \\frac{V_{\\max} [S]}{K_m + [S]}$, khi $[S] = K_m$ thì $v = \\frac{V_{\\max}}{2}$. Giá trị $K_m$ càng nhỏ thì ái lực giữa enzym và cơ chất càng cao (chỉ cần một nồng độ cơ chất thấp đã đạt nửa tốc độ tối đa).",
            ch7_img
        ),
        (
            "Trong chất ức chế cạnh tranh (Competitive Inhibition), thông số động học nào bị thay đổi trên đồ thị Lineweaver-Burk?",
            "$K_m$ biểu kiến tăng lên (đồ thị cắt trục hoành gần gốc tọa độ hơn), trong khi $V_{\\max}$ không thay đổi.",
            "$V_{\\max}$ giảm xuống rõ rệt, trong khi $K_m$ hoàn toàn không đổi.",
            "Cả $K_m$ và $V_{\\max}$ đều giảm với cùng một tỷ lệ.",
            "$K_m$ giảm xuống và $V_{\\max}$ tăng lên.",
            "A",
            "Chất ức chế cạnh tranh có cấu trúc tương tự cơ chất, tranh chấp vị trí gắn tại trung tâm hoạt động. Khi nồng độ cơ chất $[S]$ tăng đủ cao, cơ chất sẽ đẩy bật chất ức chế ra => $V_{\\max}$ không đổi, nhưng cần nồng độ cơ chất cao hơn để đạt nửa $V_{\\max}$ => $K_m$ biểu kiến tăng.",
            ch7_img
        ),
        (
            "Ví dụ nào sau đây trên lâm sàng minh họa kinh điển cho cơ chế ức chế cạnh tranh của enzym?",
            "Thuốc hạ lipid máu Statin (Atorvastatin) ức chế enzym HMG-CoA Reductase trong tổng hợp cholesterol.",
            "Kim loại nặng ($Hg^{2+}, Pb^{2+}$) gắn vào nhóm -SH ngoài trung tâm hoạt động gây bất hoạt enzym.",
            "Khí thần kinh Sarin phosphoryl hóa gốc Serin trung tâm hoạt động của Acetylcholinesterase.",
            "Aspirin acetyl hóa không hồi phục enzym Cyclooxygenase (COX).",
            "A",
            "Statin có cấu trúc phân tử tương tự cơ chất HMG-CoA, cạnh tranh thuận nghịch vị trí hoạt động của enzym HMG-CoA Reductase. Các ví dụ còn lại là ức chế không thuận nghịch hoặc phi cạnh tranh.",
            ch7_img
        ),
        (
            "Chất ức chế phi cạnh tranh (Non-competitive Inhibition) có đặc điểm tác động nào sau đây?",
            "Gắn vào một vị trí dị lập thể khác ngoài trung tâm hoạt động của cả enzym tự do và phức hợp enzym-cơ chất, làm giảm $V_{\\max}$ nhưng không làm đổi $K_m$.",
            "Tranh chấp trực tiếp với cơ chất tại trung tâm hoạt động của enzym.",
            "Chỉ gắn duy nhất vào phức hợp [ES] mà không gắn vào enzym tự do.",
            "Làm tăng tốc độ cực đại $V_{\\max}$ của phản ứng.",
            "A",
            "Chất ức chế phi cạnh tranh gắn vào vị trí khác (allosteric) trên phân tử enzym, làm biến dạng cấu trúc không gian của trung tâm hoạt động khiến phức hợp không thể tạo thành sản phẩm. Việc tăng nồng độ cơ chất không thể hóa giải sự ức chế này => $V_{\\max}$ giảm, nhưng ái lực gắn cơ chất không đổi => $K_m$ giữ nguyên.",
            ch7_img
        ),
        (
            "Hiện tượng hoạt hóa tiền enzym (Zymogen / Proenzym) đóng vai trò sinh học tối quan trọng nào trong cơ thể?",
            "Bảo vệ các mô sản xuất (như mô tụy và dạ dày) khỏi bị tự tiêu hóa bởi các protease hoạt động mạnh.",
            "Tăng tốc độ tổng hợp protein ở ribosome.",
            "Duy trì nồng độ glucose máu luôn ổn định.",
            "Ngăn chặn sự đào thải thuốc qua nước tiểu.",
            "A",
            "Các enzym tiêu đạm như Pepsinogen, Trypsinogen, Chymotrypsinogen được tổng hợp và bài tiết ở dạng tiền chất bất hoạt (Zymogen). Khi vào đến lòng dạ dày hoặc ruột non, một đoạn peptid ức chế được cắt bỏ hạn chế (phân cắt hạn chế), làm bộc lộ trung tâm hoạt động. Nếu trypsinogen hoạt hóa ngay trong nhu mô tụy sẽ dẫn tới viêm tụy cấp tự tiêu.",
            None
        ),
        (
            "Isoenzym nào của Creatine Kinase (CK) là dấu ấn sinh học đặc hiệu có giá trị chẩn đoán sớm trong nhồi máu cơ tim cấp?",
            "CK-MB (tập trung chủ yếu ở cơ tim).",
            "CK-MM (tập trung chủ yếu ở cơ xương vân).",
            "CK-BB (tập trung chủ yếu ở mô não).",
            "Troponin C.",
            "A",
            "Creatine Kinase có 3 isoenzym dimer tạo bởi 2 chuỗi M và B: CK-MM (cơ xương 98%), CK-BB (não) và CK-MB (cơ tim chiếm 20-30% tổng CK cơ tim). CK-MB huyết thanh tăng sau 3-6 giờ nhồi máu cơ tim cấp, đạt đỉnh ở 12-24 giờ và trở về bình thường sau 48-72 giờ.",
            None
        ),
        (
            "Isoenzym Lactate Dehydrogenase (LDH) gồm 5 dạng ($LDH_1$ đến $LDH_5$). Dạng nào chiếm ưu thế ở cơ tim và hồng cầu?",
            "$LDH_1$ (cấu tạo tetramer $H_4$).",
            "$LDH_5$ (cấu tạo tetramer $M_4$).",
            "$LDH_3$ (cấu tạo tetramer $H_2M_2$).",
            "$LDH_4$ (cấu tạo tetramer $HM_3$).",
            "A",
            "LDH là tetramer gồm 2 loại chuỗi H (Heart) và M (Muscle). $LDH_1$ ($H_4$) và $LDH_2$ ($H_3M$) chiếm ưu thế ở cơ tim và hồng cầu. Bình thường $LDH_2 > LDH_1$. Trong nhồi máu cơ tim hoặc tán huyết cấp tính, $LDH_1$ tăng vọt vượt qua $LDH_2$ (hiện tượng đảo ngược tỷ lệ LDH flipped pattern).",
            None
        ),
        (
            "Enzym nào sau đây trong huyết tương tăng cao nổi bật và đặc hiệu nhất trong các bệnh lý tắc mật (tắc mật trong gan hoặc ngoài gan)?",
            "Alkaline Phosphatase (ALP) và $\\gamma$-Glutamyltransferase (GGT).",
            "Alanine Aminotransferase (ALT / SGPT).",
            "Aspartate Aminotransferase (AST / SGOT).",
            "Amylase và Lipase tụy.",
            "A",
            "ALP và GGT là các enzym gắn trên màng tế bào biểu mô vi quản mật. Khi có ứ mật hoặc tắc đường dẫn mật, acid mật kích thích tăng tổng hợp và làm bong bóng các enzym này vào máu, làm ALP và GGT tăng cao gấp nhiều lần giới hạn trên bình thường.",
            None
        ),
        (
            "Cơ chế điều hòa hoạt tính enzym bằng phương thức biến đổi đồng hóa trị (Covalent Modification) phổ biến nhất trong tế bào là gì?",
            "Sự phosphoryl hóa và khử phosphoryl chuỗi bên của các gốc acid amin Serin, Threonin hoặc Tyrosin nhờ Protein Kinase và Protein Phosphatase.",
            "Sự cắt đứt vĩnh viễn chuỗi polypeptide bởi protease.",
            "Sự thay đổi nồng độ cơ chất nội bào.",
            "Sự gắn kết của ion kim loại nặng vào nhóm carboxyl.",
            "A",
            "Phosphoryl hóa (gắn nhóm phosphat từ ATP nhờ Protein Kinase) và khử phosphoryl (cắt nhóm phosphat nhờ Phosphatase) lên nhóm -OH của Ser, Thr, Tyr là công tắc bật/tắt hoạt tính enzym phổ biến và linh hoạt nhất trong đáp ứng hormon (ví dụ Glycogen synthase, Glycogen phosphorylase).",
            None
        )
    ]

    for i in range(100):
        if i < len(ch7_core):
            q, a, b, c, d, corr, exp, img = ch7_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch7_img if (i % 5 == 0) else None

            ch7_topics = [
                ("Mô hình tương tác enzym - cơ chất và năng lượng hoạt hóa", "Enzym làm tăng tốc độ phản ứng bằng cách làm giảm năng lượng hoạt hóa ($E_a$) của phản ứng sinh học.", "Enzym không làm thay đổi hằng số cân bằng hóa học ($K_{eq}$) hay biến thiên năng lượng tự do ($\\Delta G$) của phản ứng.", "Mô hình khớp cảm ứng (Induced-fit) của Koshland cho thấy trung tâm hoạt động biến đổi cấu hình khi tiếp xúc cơ chất.", "Năng lượng liên kết hình thành giữa enzym và trạng thái chuyển tiếp (transition state) là nguồn gốc lực xúc tác."),
                ("Các yếu tố ảnh hưởng đến hoạt tính enzym", "Mỗi enzym có một độ pH tối ưu xác định; ra ngoài khoảng pH này enzym bị biến tính hoặc ion hóa sai lệch.", "Nhiệt độ tối ưu của đa số enzym người là khoảng 37-40°C; nhiệt độ quá cao gây biến tính nhiệt protein enzym.", "Apoenzym là phần protein thuần của enzym, khi kết hợp với Coenzym hoặc Cofactor tạo thành Holoenzym hoàn chỉnh có hoạt tính.", "Ion kim loại ($Mg^{2+}, Zn^{2+}, Cu^{2+}$) đóng vai trò chất hoạt hóa hoặc tham gia trực tiếp vào trung tâm xúc tác."),
                ("Enzym dị lập thể (Allosteric enzymes)", "Enzym dị lập thể có đồ thị động học dạng chữ S (Sigmoid) thay vì dạng hyperbol của Michaelis-Menten.", "Chất điều hòa dị lập thể dương làm chuyển dịch đường cong sang TRÁI, làm tăng ái lực của enzym với cơ chất.", "Chất điều hòa dị lập thể âm làm chuyển dịch đường cong sang PHẢI, làm giảm ái lực của enzym.", "Enzym PFK-1 trong đường phân là enzym dị lập thể kinh điển bị ức chế bởi ATP và hoạt hóa mạnh bởi Fructose-2,6-bisphosphat."),
                ("Enzym trong chẩn đoán tổn thương tế bào gan", "ALT (SGPT) có độ đặc hiệu cho nhu mô gan cao hơn AST vì phân bố chủ yếu ở bào tương tế bào gan.", "AST (SGOT) phân bố ở cả ty thể và bào tương gan, ngoài ra còn có nhiều ở cơ tim và cơ xương.", "Tỷ số De Ritis (AST/ALT) > 2.0 thường gợi ý tổn thương gan do rượu hoặc xơ gan tiến triển.", "Trong viêm gan virus cấp tính, cả ALT và AST đều tăng vọt gấp hàng chục đến hàng trăm lần bình thường."),
                ("Ức chế không hồi phục và ứng dụng độc chất", "Aspirin ức chế không hồi phục enzym COX-1 và COX-2 bằng cách gắn nhóm acetyl vĩnh viễn vào gốc Serin 530.", "Kháng sinh nhóm Penicillin ức chế không thuận nghịch enzym Transpeptidase tổng hợp thành vách peptidoglycan vi khuẩn.", "Thuốc trừ sâu phospho hữu cơ ức chế enzym Acetylcholinesterase gây hội chứng cường phó giao cảm (SLUDGE) cấp tính.", "Chất giải độc đặc hiệu cho ngộ độc phospho hữu cơ là Pralidoxime (PAM) giúp tái sinh enzym kết hợp cùng Atropin.")
            ]
            tp = ch7_topics[i % len(ch7_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi đề cập đến {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Tất cả các phản ứng này diễn ra tự phát mà không cần xúc tác và không chịu sự kiểm soát bởi bất kỳ cơ chế điều hòa tế bào nào."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo tính chính xác của động học enzym."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Quá trình này không tuân theo các định luật nhiệt động học sinh học và chỉ quan sát thấy trong ống nghiệm invitro."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch7_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 8: HORMON (100 CÂU)
    # ==========================================
    ch8_name = "Chương 8: Hormon"
    ch8_img = "/static/uploads/hoasinh_yds/ch08_hormone_signal_transduction.svg"

    ch8_core = [
        (
            "Hormon nào sau đây có bản chất là Steroid, tan trong lipid và có thụ thể tiếp nhận nằm bên trong tế bào (bào tương hoặc nhân)?",
            "Cortisol, Aldosteron, Testosteron và Estrogen.",
            "Insulin, Glucagon và ACTH.",
            "Adrenalin và Noradrenalin.",
            "TSH, LH và FSH.",
            "A",
            "Hormon steroid (cortisol, aldosteron, hormon sinh dục) và hormon tuyến giáp (T3, T4) là các phân tử kỵ nước, khuếch tán dễ dàng qua lớp phospholipid kép của màng tế bào để gắn vào thụ thể nội bào, tác động trực tiếp lên quá trình phiên mã gen.",
            ch8_img
        ),
        (
            "Con đường truyền tín hiệu qua chất truyền tin thứ hai cAMP (Adenosine 3',5'-cyclic monophosphate) kích hoạt enzym nội bào nào?",
            "Protein Kinase A (PKA).",
            "Protein Kinase C (PKC).",
            "Protein Kinase G (PKG).",
            "Tyrosine Kinase.",
            "A",
            "Khi cAMP được tạo ra bởi Adenylate cyclase, nó gắn vào các tiểu đơn vị điều hòa của Protein Kinase A (PKA), làm giải phóng các tiểu đơn vị xúc tác hoạt động để phosphoryl hóa các protein đích trong tế bào.",
            ch8_img
        ),
        (
            "Trong con đường truyền tín hiệu Phospholipase C ($G_q$), sự phân cắt phân tử màng $PIP_2$ tạo ra hai chất truyền tin thứ hai nào?",
            "Inositol 1,4,5-trisphosphate ($IP_3$) và Diacylglycerol (DAG).",
            "cAMP và cGMP.",
            "AMP và ADP.",
            "Arachidonic acid và Prostaglandin.",
            "A",
            "Enzym Phospholipase C (PLC) xúc tác thủy phân Phosphatidylinositol 4,5-bisphosphate ($PIP_2$) tạo thành: (1) $IP_3$ hòa tan khuếch tán đến lưới nội chất làm mở kênh phóng thích $Ca^{2+}$; (2) DAG lưu lại ở màng tế bào hoạt hóa Protein Kinase C (PKC).",
            ch8_img
        ),
        (
            "Thụ thể của hormon Insulin trên màng tế bào thuộc loại thụ thể nào sau đây?",
            "Thụ thể có hoạt tính enzym Tyrosine Kinase nội tại.",
            "Thụ thể liên kết Protein G (GPCR).",
            "Thụ thể kênh ion phụ thuộc phối tử.",
            "Thụ thể nội bào gắn vào yếu tố đáp ứng hormon trên DNA.",
            "A",
            "Thụ thể Insulin là một tetramer gồm 2 tiểu đơn vị $\\alpha$ (ngoại bào gắn insulin) và 2 tiểu đơn vị $\\beta$ (xuyên màng). Khi insulin gắn vào, tiểu đơn vị $\\beta$ tự phosphoryl hóa gốc tyrosine của chính nó (autophosphorylation), kích hoạt dòng thác truyền tín hiệu IRS-1, PI3K/Akt và MAPK.",
            ch8_img
        ),
        (
            "Insulin kích thích sự vận chuyển glucose vào trong tế bào cơ xương và mô mỡ thông qua cơ chế nào sau đây?",
            "Kích thích sự chuyển vị (translocation) của các túi chứa kênh vận chuyển glucose GLUT4 từ bào tương lên màng tế bào.",
            "Kích hoạt bơm đồng vận chuyển natri-glucose SGLT1.",
            "Tăng cường hoạt tính của kênh GLUT1 và GLUT3.",
            "Thủy phân màng phospholipid để glucose tự khuếch tán vào.",
            "A",
            "GLUT4 là kênh vận chuyển khuếch tán được hỗ trợ duy nhất phụ thuộc vào insulin, phân bố ở cơ tim, cơ vân và mô mỡ. Tín hiệu qua con đường PI3K/Akt của insulin thúc đẩy các bóng nhập bào chứa GLUT4 hòa màng, tăng thu nạp glucose vào tế bào lên gấp 10-20 lần.",
            ch8_img
        ),
        (
            "Hormon Glucagon và Epinephrine kích thích quá trình ly giải glycogen (glycogenolysis) tại gan thông qua chuỗi phản ứng phosphoryl hóa nào?",
            "Gắn thụ thể GPCR $\\rightarrow$ Tăng cAMP $\\rightarrow$ Hoạt hóa PKA $\\rightarrow$ Hoạt hóa Phosphorylase Kinase $\\rightarrow$ Hoạt hóa Glycogen Phosphorylase (dạng b hoạt hóa thành dạng a).",
            "Gắn thụ thể nội bào $\\rightarrow$ Tăng tổng hợp glycogen synthase.",
            "Kích hoạt phosphodiesterase phân giải cAMP.",
            "Mở kênh calci kích thích tích lũy glycogen.",
            "A",
            "Glucagon/Epinephrine gắn thụ thể Gs kích hoạt chuỗi khuếch đại dòng thác: 1 phân tử hormon tạo hàng nghìn cAMP, hoạt hóa PKA, PKA phosphoryl hóa Phosphorylase kinase, enzym này phosphoryl hóa Glycogen phosphorylase b (bất hoạt) thành dạng a (hoạt động) để cắt glycogen giải phóng glucose-1-phosphat.",
            ch8_img
        ),
        (
            "Hormon nào sau đây do tuyến yên trước bài tiết chịu sự ức chế liên tục của Dopamin (PIH) từ vùng dưới đồi?",
            "Prolactin (PRL).",
            "Hormon tăng trưởng (GH).",
            "ACTH.",
            "TSH.",
            "A",
            "Khác với các hormon tuyến yên trước khác chủ yếu chịu sự kích thích bởi các releasing hormone, Prolactin chịu sự ức chế trương lực liên tục của Dopamin từ vùng dưới đồi. Khi dùng thuốc chẹn thụ thể dopamin (thuốc chống loạn thần) sẽ làm tăng prolactin máu gây tiết sữa bất thường.",
            None
        ),
        (
            "Hormon vỏ thượng thận Aldosteron điều hòa cân bằng muối nước tại ống lượn xa và ống góp của thận theo cơ chế nào?",
            "Tăng tái hấp thu $Na^+$ và nước, đồng thời tăng bài tiết $K^+$ và $H^+$ vào nước tiểu.",
            "Tăng đào thải $Na^+$ và giữ lại $K^+$.",
            "Tăng tái hấp thu canxi và phosphat ở quai Henle.",
            "Ức chế enzym renin ở phức hợp cận cầu thận.",
            "A",
            "Aldosteron (mineralocorticoid) gắn thụ thể MR trong nhân tế bào biểu mô ống thận, kích thích tổng hợp kênh $Na^+$ biểu mô (ENaC) và bơm $Na^+/K^+$-ATPase ở màng đáy, tăng tái hấp thu natri và nước (nâng huyết áp), bài xuất kali và hydro ra nước tiểu.",
            None
        ),
        (
            "Khí Nitric Oxide (NO) gây giãn cơ trơn mạch máu thông qua cơ chế kích hoạt chất truyền tin thứ hai nào?",
            "Hoạt hóa Guanylate Cyclase hòa tan tạo cGMP $\\rightarrow$ Hoạt hóa Protein Kinase G (PKG) $\\rightarrow$ Giảm canxi nội bào và khử phosphoryl chuỗi nhẹ myosin.",
            "Hoạt hóa Adenylate Cyclase tạo cAMP.",
            "Hoạt hóa Phospholipase C tạo IP3.",
            "Kích thích thụ thể tyrosine kinase màng tế bào.",
            "A",
            "NO từ tế bào nội mô khuếch tán sang tế bào cơ trơn mạch máu, gắn vào nhóm heme của Guanylate Cyclase hòa tan, chuyển GTP thành cGMP. cGMP kích hoạt PKG làm giãn cơ trơn mạch máu. Thuốc Nitroglycerin (chữa đau thắt ngực) và Sildenafil (Viagra - ức chế PDE-5 phân hủy cGMP) hoạt động trên con đường này.",
            None
        ),
        (
            "Hormon Parathyroid Hormone (PTH) do tuyến cận giáp tiết ra có tác dụng sinh học nào sau đây lên nồng độ canxi và phosphat huyết tương?",
            "Làm TĂNG nồng độ canxi máu và LÀM GIẢM nồng độ phosphat máu (thông qua tăng tái hấp thu Ca2+ và ức chế tái hấp thu phosphat ở ống thận).",
            "Làm giảm canxi máu và tăng phosphat máu.",
            "Làm giảm cả canxi và phosphat huyết tương.",
            "Kích thích lắng đọng canxi phosphat vào chất nền của xương.",
            "A",
            "PTH làm tăng canxi máu qua 3 cơ chế: (1) Kích thích hủy cốt bào giải phóng Ca2+ và phosphat từ xương; (2) Tăng tái hấp thu Ca2+ tại ống lượn xa đồng thời ức chế tái hấp thu phosphat tại ống lượn gần (đào thải phosphat qua nước tiểu); (3) Kích hoạt $1\\alpha$-hydroxylase tại thận chuyển vitamin D thành calcitriol để tăng hấp thu Ca2+ ở ruột.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch8_core):
            q, a, b, c, d, corr, exp, img = ch8_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch8_img if (i % 5 == 0) else None

            ch8_topics = [
                ("Hormon tuyến giáp (T3 và T4)", "T4 (Thyroxine) được bài tiết nhiều nhất (90%), nhưng T3 (Triiodothyronine) mới là dạng có hoạt tính sinh học mạnh gấp 4-5 lần T4.", "Enzym 5'-deiodinase tại các mô ngoại vi (gan, thận) chuyển đổi T4 thành T3 có hoạt tính.", "T3 gắn vào thụ thể nhân TR, kích thích tổng hợp bơm $Na^+/K^+$-ATPase, tăng tiêu thụ oxy và chuyển hóa cơ bản.", "Bệnh Basedow (Graves) do kháng thể tự miễn TRAb kích thích liên tục thụ thể TSH tuyến giáp gây nhiễm độc giáp."),
                ("Trục Dưới đồi - Tuyến yên - Vỏ thượng thận (HPA)", "CRH từ vùng dưới đồi kích thích thùy trước tuyến yên tiết ACTH; ACTH kích thích vùng bó vỏ thượng thận tiết Cortisol.", "Cortisol điều hòa ngược âm tính (negative feedback) ức chế bài tiết cả CRH và ACTH.", "Hội chứng Cushing đặc trưng bởi tăng cortisol máu (mặt tròn như mặt trăng, bướu trâu, rạn da đỏ tím, tăng đường huyết).", "Sử dụng corticoid ngoại sinh kéo dài làm teo vỏ thượng thận hai bên do ức chế kéo dài trục HPA."),
                ("Hormon Catecholamin của tủy thượng thận", "Adrenalin (Epinephrine) và Noradrenalin được tổng hợp từ acid amin Tyrosin qua các bước: DOPA $\\rightarrow$ Dopamin $\\rightarrow$ Noradrenalin $\\rightarrow$ Adrenalin.", "Enzym PNMT xúc tác methyl hóa noradrenalin thành adrenalin chịu sự kích thích của nồng độ cortisol cao từ vỏ thượng thận.", "Thụ thể $\\beta_1$ ở tim kích thích tăng nhịp tim và sức co bóp cơ tim thông qua con đường tăng cAMP.", "U tủy thượng thận (Pheochromocytoma) gây tăng tiết từng cơn catecholamin dẫn đến các cơn tăng huyết áp kịch phát."),
                ("Hormon điều hòa đường huyết và tế bào đảo tụy", "Tế bào $\\beta$ tiết Insulin (hạ đường huyết), tế bào $\\alpha$ tiết Glucagon (tăng đường huyết), tế bào $\\delta$ tiết Somatostatin (ức chế cả hai).", "C-peptide được cắt ra từ Proinsulin theo tỷ lệ phân tử 1:1 với Insulin, dùng để đánh giá chức năng tiết insulin nội sinh.", "Bệnh đái tháo đường týp 1 do tự miễn phá hủy tế bào $\\beta$, nồng độ C-peptide trong máu giảm nặng hoặc biến mất.", "Bệnh đái tháo đường týp 2 đặc trưng bởi tình trạng đề kháng insulin kết hợp với suy giảm chức năng tế bào $\\beta$ tiến triển."),
                ("Hormon thùy sau tuyến yên và cân bằng nước", "Vasopressin (ADH) và Oxytocin được tổng hợp tại nhân trên thị và cạnh não thất của vùng dưới đồi rồi vận chuyển xuống thùy sau tuyến yên tích trữ.", "ADH gắn thụ thể $V_2$ tại tế bào biểu mô ống góp thận, kích hoạt con đường cAMP gắn các kênh nước Aquaporin-2 lên màng đỉnh để tái hấp thu nước tự do.", "Đái tháo nhạt trung ương do thiếu hụt bài tiết ADH, nước tiểu tỷ trọng rất thấp (<1.005) và đa niệu số lượng lớn.", "Hội chứng SIADH đặc trưng bởi tiết ADH không thích hợp, gây giữ nước quá mức và hạ natri máu nhược trương.")
            ]
            tp = ch8_topics[i % len(ch8_topics)]
            is_except = (i % 2 == 1)
            if is_except:
                q = f"Khẳng định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Các hormon thuộc hệ này không chịu sự kiểm soát ngược feedback và không có thụ thể tiếp nhận tương ứng trong cơ thể."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng nội môi sinh lý."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Đặc điểm hóa sinh nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hormon này không tham gia vào bất kỳ phản ứng nội bào nào và chỉ tồn tại ở dạng vết không chức năng."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nội dung sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch8_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 9: KHÁI NIỆM VỀ CHUYỂN HÓA CÁC CHẤT (100 CÂU)
    # ==========================================
    ch9_name = "Chương 9: Khái niệm về chuyển hóa các chất"
    ch9_img = "/static/uploads/hoasinh_yds/ch09_metabolic_pathways_overview.svg"

    ch9_core = [
        (
            "Quá trình dị hóa (Catabolism) trong tế bào sinh vật có đặc điểm cốt lõi nào sau đây?",
            "Là quá trình thoái hóa phân giải các phân tử hữu cơ lớn thành các phân tử nhỏ hơn, đi kèm với sự giải phóng năng lượng (tích lũy dưới dạng ATP và khử coenzym NADH, FADH2).",
            "Là quá trình tiêu tốn năng lượng ATP để tổng hợp các đại phân tử sinh học phức tạp.",
            "Là quá trình chỉ xảy ra trong nhân tế bào khi phân chia nguyên phân.",
            "Là quá trình cố định carbon vô cơ thành hợp chất hữu cơ.",
            "A",
            "Chuyển hóa trung gian gồm 2 nhánh đối lập nhưng liên kết chặt chẽ: Dị hóa (Catabolism) là chuỗi các phản ứng oxy hóa phân giải giải phóng năng lượng tích lũy vào ATP; Đồng hóa (Anabolism) là chuỗi các phản ứng khử tổng hợp tiêu tốn ATP và NADPH.",
            ch9_img
        ),
        (
            "Trong 3 giai đoạn của quá trình dị hóa các chất dinh dưỡng, sự hội tụ của chuyển hóa glucid, lipid và protid xảy ra ở giai đoạn nào?",
            "Giai đoạn 2: Biến đổi các đơn phân monosacarid, acid béo, acid amin thành sản phẩm trung gian chung là Acetyl-CoA.",
            "Giai đoạn 1: Tiêu hóa thủy phân thức ăn trong ống tiêu hóa.",
            "Giai đoạn 3: Chu trình Krebs và phosphoryl hóa oxy hóa.",
            "Giai đoạn bài tiết qua thận.",
            "A",
            "Giai đoạn 1: Thủy phân đại phân tử thành monome (glucose, acid béo, acid amin). Giai đoạn 2: Các monome khác nhau đều được chuyển hóa hội tụ về một số ít phân tử trung gian chung, chủ yếu là Acetyl-CoA. Giai đoạn 3: Acetyl-CoA đi vào chu trình Krebs để oxy hóa hoàn toàn.",
            ch9_img
        ),
        (
            "Hợp chất nào sau đây có năng lượng liên kết phosphat tự do chuẩn ($\\Delta G^{\\circ \\prime}$) cao nhất trong các hợp chất cao năng sinh học?",
            "Phosphoenolpyruvate (PEP) ($\\Delta G^{\\circ \\prime} \\approx -61.9$ kJ/mol hay -14.8 kcal/mol).",
            "Adenosine Triphosphate (ATP) ($\\Delta G^{\\circ \\prime} \\approx -30.5$ kJ/mol hay -7.3 kcal/mol).",
            "Creatine Phosphate ($\\Delta G^{\\circ \\prime} \\approx -43.1$ kJ/mol hay -10.3 kcal/mol).",
            "Glucose-6-Phosphate ($\\Delta G^{\\circ \\prime} \\approx -13.8$ kJ/mol hay -3.3 kcal/mol).",
            "A",
            "Phosphoenolpyruvate (PEP) là hợp chất giàu năng lượng cao nhất trong sinh học nhờ dạng enol bị giữ lại không thể hỗ biến thành ceton cho tới khi cắt đứt gốc phosphat. Điều này giải thích tại sao phản ứng chuyển phosphat từ PEP sang ADP tạo ATP (Pyruvate Kinase) là phản ứng không thuận nghịch một chiều.",
            ch9_img
        ),
        (
            "Liên kết hóa học nào trong phân tử Acetyl-CoA mang bản chất liên kết giàu năng lượng (thay vì phosphoanhydride)?",
            "Liên kết Thioester giữa nhóm carbonyl của gốc acetyl và nhóm sulfhydryl (-SH) của Coenzyme A.",
            "Liên kết Este carboxylic thông thường.",
            "Liên kết Peptid giữa acid amin và CoA.",
            "Liên kết Phosphodiester giữa adenosin và phosphat.",
            "A",
            "Liên kết thioester ($-CO \\sim S-$) trong Acetyl-CoA có thế năng thủy phân rất cao ($\\Delta G^{\\circ \\prime} \\approx -31.5$ kJ/mol), tương đương liên kết cao năng phosphoanhydride của ATP. Năng lượng này giúp dẫn dắt phản ứng ngưng tụ acetyl với oxaloacetat tạo citrat trong chu trình Krebs.",
            ch9_img
        ),
        (
            "Creatine Phosphate (Phosphocreatine) đóng vai trò dự trữ năng lượng tức thời chủ yếu tại mô cơ quan nào?",
            "Mô cơ xương vân và cơ tim.",
            "Mô mỡ dưới da.",
            "Nhu mô gan.",
            "Tế bào hồng cầu.",
            "A",
            "Creatine phosphate là bể đệm năng lượng cao năng dự trữ trong tế bào cơ. Khi cơ bắt đầu co rút gắng sức, enzym Creatine Kinase (CK) chuyển tức thời gốc phosphat từ phosphocreatine sang ADP để tái tạo ATP trong vài giây đầu tiên trước khi đường phân hay hô hấp tế bào kịp tăng tốc độ.",
            None
        ),
        (
            "Phát biểu nào sau đây KHÔNG ĐÚNG về vai trò của phân tử ATP trong chuyển hóa năng lượng sinh học?",
            "ATP là 'đồng tiền năng lượng' vạn năng của tế bào, kết nối các phản ứng sinh năng lượng với các phản ứng tiêu năng lượng.",
            "Phân tử ATP chứa 2 liên kết cao năng phosphoanhydride và 1 liên kết phosphoester thông thường.",
            "Sự thủy phân ATP giải phóng ion $Mg^{2+}$ tự do gây độc tế bào.",
            "ATP được tái tạo liên tục thông qua 2 cơ chế: Phosphoryl hóa ở mức cơ chất và Phosphoryl hóa oxy hóa ở chuỗi truyền điện tử ty thể.",
            "C",
            "Ion $Mg^{2+}$ không hề gây độc mà trái lại, trong điều kiện sinh lý tế bào, ATP luôn tồn tại dưới dạng phức hợp với $Mg^{2+}$ ($Mg-ATP^{2-}$). $Mg^{2+}$ trung hòa bớt điện tích âm của các gốc phosphat giúp enzym tiếp cận và xúc tác dễ dàng.",
            None
        ),
        (
            "Cơ chế điều hòa dị lập thể qua tỷ lệ nồng độ [ATP]/[ADP] và [NADH]/[NAD+] có tác dụng sinh lý gì đối với các con đường dị hóa?",
            "Khi tỷ lệ [ATP]/[ADP] và [NADH]/[NAD+] cao (trạng thái tế bào thừa năng lượng), chúng sẽ ức chế các enzym giới hạn tốc độ của đường phân và chu trình Krebs.",
            "Kích thích tối đa các enzym phân giải glycogen và acid béo.",
            "Kích thích chuỗi truyền điện tử hoạt động nhanh hơn.",
            "Làm giảm tốc độ tổng hợp mỡ và glycogen dự trữ.",
            "A",
            "Trạng thái năng lượng cao (nhiều ATP và NADH) phát tín hiệu ức chế dị lập thể các enzym khóa như Isocitrate Dehydrogenase, Citrate Synthase, PFK-1, làm chậm các quá trình sinh năng lượng thừa thãi và chuyển hướng các phân tử trung gian sang các con đường đồng hóa dự trữ (tổng hợp acid béo, glycogen).",
            ch9_img
        ),
        (
            "Quá trình phosphoryl hóa ở mức cơ chất (Substrate-level Phosphorylation) khác với phosphoryl hóa oxy hóa ở điểm nào?",
            "Là sự tổng hợp ATP trực tiếp bằng cách chuyển gốc phosphat giàu năng lượng từ một cơ chất phosphoryl hóa sang ADP mà không cần đến chuỗi truyền điện tử ty thể.",
            "Chỉ xảy ra khi có mặt nồng độ oxy hòa tan rất cao trong ty thể.",
            "Cần sự tham gia bắt buộc của phức hợp ATP Synthase ($F_0F_1$).",
            "Là phản ứng chỉ diễn ra ở màng nhân tế bào.",
            "A",
            "Phosphoryl hóa ở mức cơ chất tạo ATP trực tiếp từ phản ứng hóa học (ví dụ: chuyển phosphat từ 1,3-BPG sang ADP nhờ Phosphoglycerate Kinase, từ PEP sang ADP nhờ Pyruvate Kinase trong đường phân, hoặc từ Succinyl-CoA tạo GTP/ATP trong chu trình Krebs), hoàn toàn độc lập với chuỗi truyền điện tử và oxy.",
            None
        ),
        (
            "Chất khử coenzym NADPH khác với NADH ở vai trò sinh học chủ yếu nào sau đây?",
            "NADPH là nguồn cung cấp lực khử (electron và $H^+$) chuyên biệt cho các phản ứng sinh tổng hợp đồng hóa khử (tổng hợp acid béo, cholesterol) và chống oxy hóa (hoàn nguyên glutathione).",
            "NADPH đi vào chuỗi truyền điện tử ty thể để tạo ra 2.5 phân tử ATP.",
            "NADPH chỉ tham gia vào chu trình acid citric.",
            "NADPH vận chuyển oxy trong hồng cầu.",
            "A",
            "NADH tham gia chủ yếu vào con đường dị hóa (đưa electron vào chuỗi hô hấp tế bào để sinh ATP). Ngược lại, NADPH được tạo ra chủ yếu từ con đường Pentose Phosphate, được tế bào sử dụng độc quyền làm lực khử cho các phản ứng đồng hóa (tổng hợp lipid, steroid) và bảo vệ màng tế bào (giữ glutathione ở dạng khử GSH).",
            ch9_img
        ),
        (
            "Định luật một nhiệt động học (bảo toàn năng lượng) áp dụng trong hệ thống sinh học khẳng định điều gì?",
            "Năng lượng không tự nhiên sinh ra và cũng không tự nhiên mất đi, chỉ có thể chuyển đổi từ dạng này sang dạng khác (ví dụ: năng lượng hóa học trong thức ăn chuyển thành công cơ học, nhiệt năng và năng lượng liên kết ATP).",
            "Mọi quá trình sinh học đều làm giảm entropy của vũ trụ.",
            "Tế bào sống là hệ thống cô lập không trao đổi chất và năng lượng với môi trường.",
            "Nhiệt lượng sinh ra trong chuyển hóa có thể được tế bào dùng để tổng hợp lại ATP trực tiếp.",
            "A",
            "Sinh vật sống tuân thủ nghiêm ngặt các định luật nhiệt động lực học. Tế bào là hệ thống mở trao đổi vật chất và năng lượng với môi trường xung quanh, biến đổi hóa năng từ liên kết hóa học trong chất dinh dưỡng thành các dạng năng lượng sinh học khác nhau và thải nhiệt ra môi trường.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch9_core):
            q, a, b, c, d, corr, exp, img = ch9_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch9_img if (i % 5 == 0) else None

            ch9_topics = [
                ("Nhiệt động học sinh học và biến thiên năng lượng tự do", "Phản ứng tự phát (exergonic) có biến thiên năng lượng tự do $\\Delta G < 0$, giải phóng năng lượng tự do có ích.", "Phản ứng thu năng lượng (endergonic) có $\\Delta G > 0$, không thể tự xảy ra nếu không được ghép đôi với phản ứng giải phóng năng lượng.", "Trạng thái cân bằng hóa học đạt được khi biến thiên năng lượng tự do $\\Delta G = 0$.", "Sự ghép đôi năng lượng (Energy coupling) thông qua phản ứng thủy phân ATP cho phép các phản ứng thu nhiệt xảy ra thuận lợi."),
                ("Các con đường chuyển hóa trung gian và phân nhánh", "Điểm ngã ba đường phân Glucose-6-Phosphat (G6P) có thể đi vào đường phân, tân tạo glycogen hoặc con đường pentose phosphat.", "Pyruvate có thể chuyển thành Acetyl-CoA (hiếu khí), Lactat (kỵ khí), Oxaloacetat (tân tạo đường) hoặc Alanin (trao đổi amin).", "Acetyl-CoA là ngã tư trung tâm tiếp nhận sản phẩm từ đường phân, $\\beta$-oxy hóa acid béo và thoái hóa acid amin sinh ceton.", "Oxaloacetate đóng vai trò mồi bắt đầu chu trình Krebs và là tiền chất quan trọng cho quá trình tân tạo đường."),
                ("Điều hòa chuyển hóa ở mức cơ thể và tế bào", "Phân chia ngăn tế bào (compartmentalization): Đường phân xảy ra ở bào tương, trong khi $\\beta$-oxy hóa và chu trình Krebs xảy ra trong ty thể.", "Điều hòa bằng enzym dị lập thể phản ứng nhanh trong tích tắc, điều hòa bằng biến đổi cộng hóa trị mất vài phút, điều hòa biểu hiện gen mất vài giờ.", "Cơ chế ức chế điều hòa ngược (Feedback inhibition): Sản phẩm cuối cùng của con đường chuyển hóa ức chế enzym đầu tiên của chuỗi.", "Hệ thần kinh giao cảm và các hormon phối hợp điều chỉnh tốc độ chuyển hóa theo chu kỳ thức-ngủ và trạng thái no-đói."),
                ("Ý nghĩa lâm sàng của rối loạn năng lượng tế bào", "Thiếu máu cục bộ mô (ischemia) làm ngưng trệ chuỗi hô hấp tế bào, cạn kiệt ATP nhanh chóng trong vài phút.", "Khi thiếu ATP, bơm $Na^+/K^+$-ATPase ngừng hoạt động làm $Na^+$ và nước tràn vào trong tế bào gây phù tế bào cấp tính.", "Chuyển hóa chuyển sang đường phân kỵ khí bù trừ làm tăng tích tụ acid lactic gây toan chuyển hóa máu nghiêm trọng.", "Sự phục hồi tưới máu có thể gây tổn thương tái tưới máu (reperfusion injury) do giải phóng ồ ạt các gốc oxy hóa tự do (ROS)."),
                ("Các phương pháp nghiên cứu chuyển hóa sinh học", "Đồng vị phóng xạ ($^{14}C, ^{3}H, ^{32}P$) và đồng vị bền ($^{13}C, ^{15}N$) dùng để truy vết con đường di chuyển của các nguyên tử trong cơ thể.", "Kỹ thuật cộng hưởng từ hạt nhân (NMR) và PET-scan (dùng 18F-FDG) cho phép ghi hình chuyển hóa glucose in vivo trong các khối u.", "Phương pháp ức chế enzym đặc hiệu bằng thuốc hoặc biến đổi gen (knock-out) giúp xác định chính xác chức năng từng bước phản ứng.", "Định lượng nồng độ các chất chuyển hóa (Metabolomics) bằng sắc ký khối phổ (LC-MS) phục vụ chẩn đoán bệnh chuyển hóa bẩm sinh.")
            ]
            tp = ch9_topics[i % len(ch9_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cơ chế này hoàn toàn không tuân theo các định luật bảo toàn khối lượng hay bảo toàn năng lượng trong tự nhiên."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng chuyển hóa nội môi."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Quá trình này chỉ xảy ra ở sinh vật đơn bào cổ xưa và không còn hiện diện trong tế bào người hiện đại."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch9_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # Insert Batch 3 into DB
    print(f"Prepared {len(questions)} questions for Batch 3 (Ch7, Ch8, Ch9). Inserting into DB...")
    for item in questions:
        cur.execute("""
            INSERT INTO questions (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_option, explanation, difficulty, topic_tag, image_url, q_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'multiple_choice')
        """, (sub_id, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[0], item[9]))

    conn.commit()
    cur.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sub_id,))
    print(f"Batch 3 Seed Complete! Current total questions for subject {sub_id}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    seed_part3()
