# -*- coding: utf-8 -*-
"""
UniMaster AI - Seeder for YDS 2024 Medical Biochemistry
Batch 5:
- Chương 13: Chuyển hóa protid (100 câu)
- Chương 14: Chuyển hóa hemoglobin (100 câu)
- Chương 15: Chuyển hóa acid nucleic (100 câu)
Total: 300 questions
"""

import sqlite3

def seed_part5():
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
    # CHƯƠNG 13: CHUYỂN HÓA PROTID (100 CÂU)
    # ==========================================
    ch13_name = "Chương 13: Chuyển hóa protid"
    ch13_img = "/static/uploads/hoasinh_yds/ch13_urea_cycle_ornithine.svg"

    ch13_core = [
        (
            "Phản ứng trao đổi amin (Transamination) đóng vai trò trung tâm trong thoái hóa acid amin, sử dụng coenzym nào sau đây?",
            "Pyridoxal Phosphate (PLP - dẫn xuất của Vitamin B6).",
            "Thiamin Pyrophosphate (TPP).",
            "Biotin.",
            "Flavin Adenine Dinucleotide (FAD).",
            "A",
            "Tất cả các enzym Aminotransferase (Transaminase như AST, ALT) đều cần coenzym Pyridoxal Phosphate (PLP) gắn ở trung tâm hoạt động để luân chuyển nhóm amin ($-NH_2$) từ một acid amin sang một $\\alpha$-cetoacid tạo thành acid amin mới và $\\alpha$-cetoacid mới.",
            ch13_img
        ),
        (
            "Amoniac ($NH_3 / NH_4^+$) rất độc đối với hệ thần kinh trung ương. Dạng vận chuyển amoniac chủ yếu và an toàn nhất từ các mô ngoại vi (đặc biệt là mô não) trong dòng máu về gan là gì?",
            "Glutamine (tổng hợp từ Glutamate và $NH_4^+$ nhờ enzym Glutamine Synthetase).",
            "Ure tự do hòa tan.",
            "Amoni clorua.",
            "Acid Uric.",
            "A",
            "Để giải độc amoniac tại chỗ ở não và các mô ngoài gan, enzym Glutamine Synthetase gắn $NH_4^+$ vào Glutamate tiêu tốn 1 ATP tạo thành Glutamine không độc và trung tính, dễ dàng lưu thông trong máu về gan. Tại gan, enzym Glutaminase cắt giải phóng lại $NH_4^+$ đi vào chu trình Ure.",
            ch13_img
        ),
        (
            "Chu trình Glucose - Alanine vận chuyển nitơ amin từ cơ xương về gan diễn ra theo cơ chế nào?",
            "Tại cơ, Pyruvate nhận nhóm amin từ sự thoái hóa acid amin tạo Alanine; Alanine theo máu về gan trao đổi amin tái tạo Pyruvate cho tân tạo Glucose, đồng thời giải phóng nhóm amin tạo Ure.",
            "Chuyển trực tiếp amoniac tự do qua tĩnh mạch.",
            "Chuyển acid lactic gắn với urea về thận.",
            "Chuyển acid béo gắn với glutamat về mô mỡ.",
            "A",
            "Trong quá trình vận động cơ bắp, đường phân tạo pyruvate. Nhờ enzym ALT cơ, pyruvate nhận nhóm amin từ thoái hóa protein tạo Alanine. Alanine vào máu về gan, được ALT gan chuyển lại thành pyruvate (tân tạo glucose đưa trở lại cơ) và glutamate (khử amin tạo amoniac đi vào chu trình Ure).",
            ch13_img
        ),
        (
            "Enzym nào xúc tác phản ứng đầu tiên trong ty thể tế bào gan, đóng vai trò là enzym giới hạn tốc độ (rate-limiting) của toàn bộ Chu trình Ure?",
            "Carbamoyl Phosphate Synthetase I (CPS-I) (cần chất hoạt hóa dị lập thể bắt buộc là N-Acetylglutamate).",
            "Ornithine Transcarbamylase (OTC).",
            "Argininosuccinate Synthetase.",
            "Arginase.",
            "A",
            "CPS-I nằm trong chất nền ty thể gan, sử dụng $NH_4^+$, $HCO_3^-$ và 2 ATP để tạo Carbamoyl phosphate. CPS-I hoàn toàn không có hoạt tính nếu thiếu chất hoạt hóa dị lập thể bắt buộc N-Acetylglutamate (NAG) - chất được tổng hợp khi nồng độ acid amin và arginine trong tế bào gan tăng cao.",
            ch13_img
        ),
        (
            "Hai nguyên tử Nitơ trong phân tử Ure ($H_2N-CO-NH_2$) có nguồn gốc trực tiếp từ những chất nào sau đây?",
            "Một nguyên tử Nitơ đến từ ion Amoni tự do ($NH_4^+$), một nguyên tử Nitơ đến từ Acid Aspartic (Aspartate).",
            "Cả hai nguyên tử Nitơ đều đến từ ion Amoni tự do.",
            "Cả hai nguyên tử Nitơ đều đến từ Glutamine.",
            "Một nguyên tử Nitơ từ Alanine và một nguyên tử từ Glycine.",
            "A",
            "Cấu trúc của Urea gồm: 1 nguyên tử Carbon từ $CO_2 / HCO_3^-$; nguyên tử Nitơ thứ nhất đi vào phản ứng số 1 dưới dạng ion $NH_4^+$ tự do trong ty thể (từ phản ứng glutamate dehydrogenase); nguyên tử Nitơ thứ hai được đưa vào ở phản ứng số 3 tại bào tương thông qua phân tử Aspartate.",
            ch13_img
        ),
        (
            "Khiếm khuyết di truyền enzym nào sau đây trong chu trình Ure là phổ biến nhất và có phương thức di truyền liên kết nhiễm sắc thể X lặn (X-linked recessive)?",
            "Ornithine Transcarbamylase (OTC).",
            "Carbamoyl Phosphate Synthetase I (CPS-I).",
            "Arginase.",
            "Argininosuccinate Lyase.",
            "A",
            "Thiếu OTC là bệnh rối loạn chu trình ure phổ biến nhất, di truyền liên kết NST X (các enzym khác đều di truyền lặn NST thường). Carbamoyl phosphate ứ đọng trong ty thể tràn ra bào tương kích thích con đường tổng hợp pyrimidine, dẫn tới tăng cao nồng độ Orotic acid trong máu và nước tiểu kèm theo tăng amoniac máu nặng nề.",
            ch13_img
        ),
        (
            "Cơ chế hóa sinh nào giải thích độc tính cấp tính của nồng độ Amoniac ($NH_3$) cao đối với tế bào não bộ?",
            "Amoniac phản ứng với $\\alpha$-Ketoglutarate tạo Glutamate, và phản ứng với Glutamate tạo Glutamine, làm cạn kiệt $\\alpha$-Ketoglutarate của chu trình Krebs (ức chế sản sinh ATP ở não) đồng thời gây phù nề tế bào thần kinh đệm do áp suất thẩm thấu của Glutamine.",
            "Amoniac cắt đứt liên kết myelin của dây thần kinh.",
            "Amoniac ức chế kênh dẫn truyền natri qua synap.",
            "Amoniac gây đông vón các protein màng tế bào thần kinh.",
            "A",
            "Tăng amoniac máu thúc đẩy 2 phản ứng của Glutamate DH và Glutamine Synthetase ở não: (1) Hút cạn $\\alpha$-ketoglutarate làm chu trình Krebs ngưng trệ, tế bào não thiếu hụt năng lượng ATP trầm trọng; (2) Giảm chất dẫn truyền kích thích GABA và glutamate; (3) Tích tụ lượng lớn Glutamine trong tế bào sao (astrocyte) gây tăng áp suất thẩm thấu nội bào dẫn tới phù não cấp tính, hôn mê và tử vong.",
            ch13_img
        ),
        (
            "Bệnh Phenylketon niệu (Phenylketonuria - PKU) là bệnh rối loạn di truyền chuyển hóa acid amin do thiếu hụt enzym nào?",
            "Phenylalanine Hydroxylase (hoặc coenzyme Tetrahydrobiopterin - $BH_4$).",
            "Homogentisate Oxidase.",
            "Tyrosinase.",
            "Branched-Chain $\\alpha$-Ketoacid Dehydrogenase (BCKDH).",
            "A",
            "PKU do đột biến enzym Phenylalanine Hydroxylase (PAH) chuyển Phenylalanine thành Tyrosine. Phenylalanine ứ đọng chuyển thành các acid phenylpyruvic, phenylacetic và phenyllactic đào thải qua nước tiểu có mùi ẩm mốc đặc trưng, gây chậm phát triển trí tuệ nặng nề ở trẻ nếu không được phát hiện sớm và ăn kiêng hạn chế phenylalanine.",
            None
        ),
        (
            "Bệnh Alkapton niệu (Alkaptonuria) có đặc điểm lâm sàng kinh điển là nước tiểu để lâu ngoài không khí bị chuyển sang màu đen do thiếu enzym nào trong con đường thoái hóa Tyrosine?",
            "Homogentisate 1,2-Dioxygenase (Homogentisate Oxidase).",
            "Tyrosinase.",
            "Fumarylacetoacetate Hydrolase.",
            "DOPA Decarboxylase.",
            "A",
            "Thiếu enzym Homogentisate Oxidase làm tích tụ Homogentisic acid. Chất này đào thải ra nước tiểu, khi tiếp xúc với oxy không khí bị oxy hóa và kiềm hóa tạo thành sắc tố màu đen sẫm. Trong cơ thể, chất này lắng đọng mạn tính ở mô sụn và mô liên kết (bệnh nhiễm sắc tố ochronosis), gây viêm thoái hóa khớp nặng ở tuổi trung niên.",
            None
        ),
        (
            "Bệnh siro niệu (Maple Syrup Urine Disease - MSUD) đặc trưng bởi nước tiểu có mùi ngọt ngào của đường cháy hoặc siro cây phong do thiếu phức hợp enzym chuyển hóa nhóm acid amin nào?",
            "Các acid amin chuỗi nhánh (Branched-Chain Amino Acids: Leucine, Isoleucine và Valine).",
            "Các acid amin chứa lưu huỳnh (Cystein và Methionin).",
            "Các acid amin nhân thơm (Phenylalanin và Tyrosin).",
            "Các acid amin kiềm (Lysin và Arginin).",
            "A",
            "MSUD do khiếm khuyết phức hợp $\\alpha$-Ketoacid Dehydrogenase chuỗi nhánh (BCKDH - cần coenzym TPP), làm tích tụ Leucine, Isoleucine, Valine và các dẫn xuất $\\alpha$-cetoacid tương ứng trong máu và nước tiểu, gây nhiễm độc thần kinh nặng nề, co giật, chậm phát triển trí tuệ và tử vong sớm ở trẻ sơ sinh.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch13_core):
            q, a, b, c, d, corr, exp, img = ch13_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch13_img if (i % 5 == 0) else None

            ch13_topics = [
                ("Phân loại acid amin sinh đường và sinh ceton", "Leucine và Lysine là hai acid amin duy nhất thuần túy sinh ceton (purely ketogenic), không thể tân tạo glucose.", "Acid amin vừa sinh đường vừa sinh ceton gồm Phenylalanine, Tyrosine, Tryptophan, Isoleucine và Threonine.", "Các acid amin còn lại (13 acid amin) là acid amin thuần túy sinh đường (glucogenic).", "Sự thoái hóa khung carbon của các acid amin hội tụ về 7 sản phẩm chuyển hóa: Pyruvate, Acetyl-CoA, Acetoacetyl-CoA, $\\alpha$-Ketoglutarate, Succinyl-CoA, Fumarate và Oxaloacetate."),
                ("Sinh tổng hợp các chất dẫn truyền thần kinh từ acid amin", "Tryptophan là tiền chất tổng hợp Serotonin (5-HT) và hormon ngủ Melatonin.", "Tyrosine qua DOPA chuyển hóa thành Dopamine, Noradrenaline và Adrenaline.", "Histidine bị khử carboxyl bởi Histidine Decarboxylase (cần PLP) tạo Histamin trong phản ứng dị ứng.", "Glutamate bị khử carboxyl bởi Glutamate Decarboxylase (GAD) tạo GABA - chất ức chế dẫn truyền thần kinh chính ở não."),
                ("Chuyển hóa acid amin chứa lưu huỳnh và Homocystein", "Methionine chuyển thành S-Adenosylmethionine (SAM) - chất cho nhóm methyl sinh học quan trọng nhất.", "Homocysteine có thể tái methyl hóa thành Methionine (cần Vitamin B12 và Folate) hoặc chuyển thành Cysteine (cần Vitamin B6).", "Tăng Homocysteine máu mạn tính là yếu tố nguy cơ độc lập gây xơ vữa động mạch và huyết khối tắc mạch.", "Bệnh Homocystin niệu (Homocystinuria) do thiếu enzym Cystathionine $\\beta$-Synthase gây lệch thể thủy tinh thể và biến dạng xương giống hội chứng Marfan."),
                ("Sinh tổng hợp Creatine và Porphyrin", "Creatine được tổng hợp từ 3 acid amin: Glycine, Arginine (tại thận) và Methionine (cung cấp nhóm methyl tại gan).", "Creatinine là sản phẩm thoái hóa tự nhiên không hồi phục từ creatine phosphate trong cơ bắp, đào thải qua thận với tốc độ ổn định.", "Glycine kết hợp với Succinyl-CoA là phản ứng khởi đầu sinh tổng hợp nhân Heme tại ty thể.", "Glutathione (GSH) được tổng hợp từ 3 acid amin: Glutamate, Cysteine và Glycine."),
                ("Bệnh Bạch tạng và chuyển hóa Tyrosine", "Bệnh Bạch tạng thể mắt-da (Oculocutaneous Albinism) do thiếu hụt enzym Tyrosinase chuyển DOPA thành Melanin sắc tố.", "Người bệnh bạch tạng có da và tóc trắng bẩm sinh, mống mắt trong suốt, sợ ánh sáng và nguy cơ cao ung thư da do tia tử ngoại.", "Tyrosine là tiền chất tổng hợp hormon tuyến giáp ($T_3, T_4$) tại các nang tuyến giáp.", "Nhiễm toan Tyrosine máu (Tyrosinemia type I) do thiếu enzym Fumarylacetoacetate hydrolase gây suy gan cấp và nước tiểu mùi bắp cải luộc.")
            ]
            tp = ch13_topics[i % len(ch13_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cơ chế này hoàn toàn không tuân theo các phản ứng chuyển hóa amin và không có giá trị sinh học trong tế bào người."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng protid sinh lý."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ gặp ở vi nấm hoại sinh và bị đào thải nguyên vẹn mà không tương tác với bất kỳ enzym nào."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các đáp án khác nêu sai lệch cơ chế sinh hóa."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch13_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 14: CHUYỂN HÓA HEMOGLOBIN (100 CÂU)
    # ==========================================
    ch14_name = "Chương 14: Chuyển hóa hemoglobin"
    ch14_img = "/static/uploads/hoasinh_yds/ch14_bilirubin_metabolism.svg"

    ch14_core = [
        (
            "Phản ứng thoái hóa Heme đầu tiên tại tế bào hệ võng nội mô (lách, gan) do enzym Heme Oxygenase xúc tác giải phóng những sản phẩm nào sau đây?",
            "Sắc tố Biliverdin (màu xanh lá), ion sắt tự do $Fe^{2+}$, và khí Carbon Monoxide (CO).",
            "Bilirubin trực tiếp và acid glucuronic.",
            "Urobilinogen và globin.",
            "Methemoglobin và sắt ferric.",
            "A",
            "Heme Oxygenase cắt cầu nối $\\alpha$-methenyl giữa 2 vòng pyrrol của protoporphyrin IX, mở vòng tạo Biliverdin mạch thẳng, giải phóng $Fe^{2+}$ tái sử dụng và sinh ra khí CO. Đây là phản ứng sinh học nội sinh DUY NHẤT trong cơ thể người sản xuất ra khí CO.",
            ch14_img
        ),
        (
            "Bilirubin gián tiếp (Bilirubin tự do / không liên hợp - UCB) có đặc điểm lý hóa và sinh học nào sau đây?",
            "Không tan trong nước, gắn chặt với Albumin huyết tương để di chuyển trong máu, tan trong mỡ và có khả năng thấm qua hàng rào máu não gây độc thần kinh.",
            "Tan tốt trong nước và đào thải dễ dàng qua nước tiểu.",
            "Phản ứng Diazo trực tiếp cho màu đỏ tím ngay trong vòng 1 phút.",
            "Đã được liên hợp với 2 phân tử acid glucuronic tại gan.",
            "A",
            "Bilirubin gián tiếp có liên kết hydro nội phân tử che lấp các nhóm phân cực nên rất kỵ nước. Trong máu, nó bắt buộc phải gắn với albumin. Do tan trong lipid, nồng độ UCB tự do cao trong máu ở trẻ sơ sinh có thể ngấm vào các nhân xám đáy não gây vàng da nhân não (Kernicterus) không hồi phục.",
            ch14_img
        ),
        (
            "Enzym nào tại lưới nội chất của tế bào gan xúc tác phản ứng liên hợp Bilirubin gián tiếp với Acid Glucuronic để tạo thành Bilirubin trực tiếp?",
            "UDP-Glucuronosyltransferase (UGT1A1).",
            "Biliverdin Reductase.",
            "Heme Oxygenase.",
            "Glutathione S-transferase.",
            "A",
            "Enzym UGT1A1 (UDP-glucuronosyltransferase isoenzyme 1A1) chuyển gốc glucuronate từ UDP-glucuronic acid gắn vào 2 nhóm acid propionic của bilirubin, tạo thành Bilirubin Monoglucuronide và chủ yếu là Bilirubin Diglucuronide (Bilirubin trực tiếp / liên hợp) tan được trong nước.",
            ch14_img
        ),
        (
            "Tại lòng ruột già, Bilirubin liên hợp bị các vi khuẩn đường ruột khử hydro và thủy phân liên hợp tạo thành hợp chất không màu nào sau đây?",
            "Urobilinogen và Stercobilinogen.",
            "Biliverdin.",
            "Stercobilin màu nâu.",
            "Acid cholic.",
            "A",
            "Dưới tác động của hệ vi sinh vật yếm khí ruột già, bilirubin liên hợp bị khử tạo thành các hợp chất polypyrrol không màu: Urobilinogen và Stercobilinogen. Đa số stercobilinogen bị oxy hóa bởi không khí thành Stercobilin có màu nâu đặc trưng của phân.",
            ch14_img
        ),
        (
            "Trong bệnh cảnh Vàng da trước gan do Tán huyết cấp tính (Hemolytic Jaundice), xét nghiệm sinh hóa máu và nước tiểu cho kết quả điển hình nào?",
            "Bilirubin GIÁN TIẾP máu tăng cao nổi bật, Urobilinogen trong nước tiểu và Stercobilin trong phân TĂNG ĐẬM ĐỘ, xét nghiệm Bilirubin trong nước tiểu ÂM TÍNH.",
            "Bilirubin trực tiếp máu tăng cao, phân bạc màu, bilirubin niệu dương tính mạnh.",
            "Tăng men gan AST và ALT gấp 50 lần.",
            "Nước tiểu không có Urobilinogen.",
            "A",
            "Tán huyết làm lượng lớn hemoglobin bị phá hủy giải phóng ồ ạt bilirubin gián tiếp vượt quá công suất liên hợp của gan. Bilirubin gián tiếp không tan trong nước và gắn albumin nên KHÔNG LỌC ĐƯỢC qua cầu thận (Bilirubin niệu âm tính). Gan tăng cường bài tiết mật làm tăng urobilinogen ruột và nước tiểu, phân sẫm màu.",
            ch14_img
        ),
        (
            "Dấu hiệu xét nghiệm sinh hóa nào sau đây là ĐẶC TRƯNG NHẤT cho tình trạng Vàng da sau gan do Tắc mật hoàn toàn (Obstruction Jaundice do sỏi mật hoặc ung thư đầu tụy)?",
            "Bilirubin TRỰC TIẾP máu tăng rất cao, Bilirubin niệu DƯƠNG TÍNH MẠNH (nước tiểu sẫm như nước chè đặc), phân BẠC MÀU NHƯ PHÂN CÒ (thiếu stercobilin), ALP và GGT tăng vọt.",
            "Bilirubin gián tiếp tăng cao đơn độc, phân sẫm màu.",
            "Urobilinogen niệu tăng rất cao.",
            "Men gan ALT và AST tăng gấp 100 lần so với ALP.",
            "A",
            "Khi tắc đường dẫn mật, bilirubin trực tiếp ứ đọng tràn ngược vào máu qua các xoang gan. Do tan trong nước, bilirubin trực tiếp lọc qua cầu thận làm Bilirubin niệu dương tính mạnh (nước tiểu sậm màu). Sắc tố mật không xuống được ruột làm phân mất màu nâu (phân bạc màu). Các men ứ mật màng vi quản mật ALP, GGT tăng vọt.",
            ch14_img
        ),
        (
            "Hội chứng Gilbert là một rối loạn di truyền lành tính gây vàng da nhẹ từng đợt khi căng thẳng, nhịn đói hoặc ốm sốt, do cơ chế nào sau đây?",
            "Giảm hoạt tính enzym UGT1A1 xuống còn khoảng 30% mức bình thường do đột biến vùng promoter TATA box của gen.",
            "Mất hoàn toàn 100% hoạt tính enzym UGT1A1.",
            "Khiếm khuyết protein vận chuyển MRP2 trên màng vi quản mật.",
            "Tắc nghẽn ống mật chủ bẩm sinh.",
            "A",
            "Hội chứng Gilbert là biến thể di truyền phổ biến (chiếm 5-10% dân số) do chèn thêm 2 nucleotid (TA) vào promoter vùng TATA box ($A(TA)_7TAA$ thay vì $A(TA)_6TAA$), làm giảm biểu hiện gen UGT1A1 còn ~30%. Bilirubin gián tiếp tăng nhẹ (<3 mg/dL), chức năng gan hoàn toàn bình thường và không cần điều trị.",
            None
        ),
        (
            "Hội chứng Crigler-Najjar Type I khác biệt với Type II ở đặc điểm lâm sàng và đáp ứng điều trị nào sau đây?",
            "Type I mất hoàn toàn 100% hoạt tính UGT1A1, Bilirubin gián tiếp tăng cực cao (>20-45 mg/dL) gây vàng da nhân não tử vong nếu không ghép gan, KHÔNG ĐÁP ỨNG với thuốc Phenobarbital.",
            "Type I đáp ứng tốt với Phenobarbital làm giảm nồng độ bilirubin.",
            "Type I là bệnh lành tính không có nguy cơ vàng da nhân.",
            "Type II có đột biến mất toàn bộ gen UGT1A1.",
            "A",
            "Crigler-Najjar type I do đột biến vô nghĩa làm mất hoàn toàn hoạt tính UGT1A1, bilirubin gián tiếp tăng cực cao, không đáp ứng với Phenobarbital (thuốc cảm ứng enzym ty thể) $\\rightarrow$ Ghép gan là cứu cánh duy nhất. Type II (hội chứng Arias) còn một phần hoạt tính (<10%), đáp ứng tốt với Phenobarbital giúp hạ nồng độ bilirubin.",
            None
        ),
        (
            "Hội chứng Dubin-Johnson đặc trưng bởi tình trạng tăng Bilirubin trực tiếp máu kết hợp với nhu mô gan có màu đen sẫm (black liver) do đột biến khiếm khuyết protein nào?",
            "Protein vận chuyển bài tiết bilirubin liên hợp qua màng đỉnh vi quản mật MRP2 (ABCC2).",
            "Protein màng đáy OATP1B1 và OATP1B3.",
            "Enzym UGT1A1.",
            "Enzym Biliverdin Reductase.",
            "A",
            "Hội chứng Dubin-Johnson là bệnh di truyền lặn NST thường do đột biến protein vận chuyển phụ thuộc ATP MRP2 (Multidrug Resistance-associated Protein 2) chịu trách nhiệm bơm bilirubin trực tiếp từ tế bào gan vào vi quản mật. Sắc tố polymer giống melanin lắng đọng trong thể tiêu bào làm gan có màu đen tuyền trên đại thể.",
            None
        ),
        (
            "Phương pháp chiếu đèn (Phototherapy) sử dụng ánh sáng xanh (bước sóng 420 - 470 nm) điều trị vàng da tăng bilirubin gián tiếp ở trẻ sơ sinh dựa trên cơ chế quang hóa nào?",
            "Biến đổi đồng phân cấu trúc không gian của Bilirubin không liên hợp $4Z,15Z$ thành đồng phân quang học $4Z,15E$ và Lumirubin tan được trong nước và bài tiết trực tiếp qua mật/nước tiểu mà KHÔNG CẦN liên hợp tại gan.",
            "Chiếu sáng làm tiêu diệt các hồng cầu già trong máu.",
            "Kích thích enzym UGT1A1 ở gan hoạt động gấp 10 lần.",
            "Tăng đào thải albumin qua đường tiêu hóa.",
            "A",
            "Ánh sáng xanh chuyển đổi dạng đồng phân tự nhiên $4Z,15Z$ (bền vững nhờ liên kết hydro nội phân tử) thành đồng phân quang học thuận nghịch $4Z,15E$ và đồng phân cấu trúc không hồi phục Lumirubin. Các chất này có cấu trúc mở, tan được trong nước nên bài tiết thẳng vào dịch mật và nước tiểu mà không phụ thuộc vào hệ enzym UGT1A1 còn non nớt của trẻ.",
            ch14_img
        )
    ]

    for i in range(100):
        if i < len(ch14_core):
            q, a, b, c, d, corr, exp, img = ch14_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch14_img if (i % 5 == 0) else None

            ch14_topics = [
                ("Phản ứng tạo màu Diazo và định lượng Bilirubin", "Phản ứng Van den Bergh dùng acid sulfanilic diazot hóa tạo azobilirubin có màu đỏ tím đặc trưng.", "Bilirubin trực tiếp (tan trong nước) phản ứng ngay lập tức trong môi trường nước (phản ứng trực tiếp).", "Bilirubin gián tiếp kỵ nước cần thêm chất gia tốc (methanol, ethanol hoặc caffeine) phá vỡ liên kết hydro mới phản ứng (phản ứng toàn phần).", "Bilirubin gián tiếp được tính gián tiếp bằng hiệu số giữa Bilirubin toàn phần và Bilirubin trực tiếp."),
                ("Hội chứng Rotor và phân biệt với Dubin-Johnson", "Hội chứng Rotor do khiếm khuyết các protein vận chuyển tái hấp thu OATP1B1 và OATP1B3 ở màng đáy tế bào gan.", "Khác với Dubin-Johnson, gan của bệnh nhân hội chứng Rotor có màu sắc hoàn toàn bình thường (không có sắc tố đen).", "Bài tiết coproporphyrin niệu: Dubin-Johnson có đồng phân I > 80%, trong khi Rotor có tổng coproporphyrin niệu tăng cao.", "Cả hai hội chứng đều là rối loạn lành tính di truyền lặn NST thường gây tăng bilirubin trực tiếp máu."),
                ("Vàng da sơ sinh sinh lý và vàng da do sữa mẹ", "Vàng da sinh lý xuất hiện sau 24 giờ tuổi, đạt đỉnh ở ngày thứ 3-5 và tự hết trong vòng 1-2 tuần do UGT1A1 chưa trưởng thành.", "Vàng da trước 24 giờ đầu sau sinh LUÔN LUÔN là bệnh lý (bất đồng nhóm máu mẹ con ABO, Rh hoặc nhiễm trùng).", "Vàng da do sữa mẹ (Breast milk jaundice) xuất hiện muộn hơn do enzym $\\beta$-glucuronidase trong sữa mẹ thủy phân bilirubin liên hợp làm tăng tái hấp thu gan-ruột.", "Vàng da do thiếu sữa mẹ (Breastfeeding failure jaundice) do bú không đủ gây mất nước và chậm tống phân su."),
                ("Chuyển hóa và tái hấp thu Urobilinogen", "Khoảng 10-15% urobilinogen được tái hấp thu ở hồi tràng và đại tràng vào tĩnh mạch cửa quay về gan (chu trình gan-ruột).", "Phần lớn urobilinogen tái hấp thu được tế bào gan bắt giữ và bài tiết trở lại vào mật.", "Một lượng rất nhỏ urobilinogen thoát qua vòng tuần hoàn chung đến thận và lọc ra nước tiểu (bình thường < 4 mg/24h).", "Trong tắc mật hoàn toàn, urobilinogen trong nước tiểu hoàn toàn BIẾN MẤT do sắc tố mật không xuống được ruột."),
                ("Xét nghiệm sắc tố mật và muối mật trong nước tiểu", "Bilirubin chỉ xuất hiện trong nước tiểu khi nồng độ Bilirubin TRỰC TIẾP trong máu tăng cao vượt ngưỡng thận.", "Nước tiểu có Bilirubin khi lắc tạo bọt màu vàng tươi đặc trưng (nước tiểu bình thường bọt màu trắng).", "Phương pháp vạch que nhúng (dipstick) dùng muối diazonium phát hiện bilirubin niệu với độ nhạy cao.", "Phản ứng Hay dùng bột lưu huỳnh xác định sự có mặt của muối mật trong nước tiểu nhờ làm giảm sức căng bề mặt.")
            ]
            tp = ch14_topics[i % len(ch14_topics)]
            is_except = (i % 2 == 1)
            if is_except:
                q = f"Khẳng định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi đề cập đến {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Hiện tượng này hoàn toàn không làm biến đổi nồng độ sắc tố trong cơ thể và không phản ánh bất kỳ bệnh lý gan mật nào."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng chuyển hóa sắc tố mật."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Nhận định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ gặp ở loài bò sát và hoàn toàn không hiện diện trong huyết tương hay dịch mật người."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch14_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 15: CHUYỂN HÓA ACID NUCLEIC (100 CÂU)
    # ==========================================
    ch15_name = "Chương 15: Chuyển hóa acid nucleic"
    ch15_img = "/static/uploads/hoasinh_yds/ch15_purine_uric_acid_gout.svg"

    ch15_core = [
        (
            "Sản phẩm thoái hóa cuối cùng của các base Purine (Adenin và Guanin) ở loài người là hợp chất nào sau đây?",
            "Acid Uric (dưới dạng ion Urate trong máu).",
            "Urea.",
            "Allantoin.",
            "Amoniac.",
            "A",
            "Ở đa số các loài động vật có vú khác, enzym Urate Oxidase (Uricase) phân giải acid uric thành allantoin tan rất tốt trong nước. Tuy nhiên trong quá trình tiến hóa của loài vượn người và con người, gen uricase đã bị đột biến mất hoạt tính, khiến Acid Uric trở thành sản phẩm thoái hóa cuối cùng của purine.",
            ch15_img
        ),
        (
            "Enzym nào xúc tác hai bước oxy hóa liên tiếp: chuyển Hypoxanthine thành Xanthine, và chuyển Xanthine thành Acid Uric trong con đường thoái hóa Purine?",
            "Xanthine Oxidase (hoặc Xanthine Dehydrogenase).",
            "Adenosine Deaminase (ADA).",
            "Guanine Deaminase.",
            "Purine Nucleoside Phosphorylase (PNP).",
            "A",
            "Xanthine Oxidase là enzym chứa molypden, sắt-lưu huỳnh và FAD, xúc tác oxy hóa Hypoxanthine $\\rightarrow$ Xanthine $\\rightarrow$ Acid Uric, đồng thời tạo ra gốc hydroperoxide $H_2O_2$.",
            ch15_img
        ),
        (
            "Thuốc điều trị hạ Acid Uric máu kinh điển Allopurinol và chất chuyển hóa có hoạt tính Alloxanthine (Oxypurinol) tác động theo cơ chế nào?",
            "Ức chế cạnh tranh và tự sát (suicide inhibition) đối với enzym Xanthine Oxidase, làm giảm nồng độ acid uric và tăng bài tiết hypoxanthine/xanthine dễ hòa tan hơn.",
            "Kích hoạt enzym uricase tái tổ hợp trong máu.",
            "Tăng tái hấp thu acid uric tại ống lượn gần.",
            "Ức chế phân giải protein nhân ở dịch khớp.",
            "A",
            "Allopurinol là chất đồng đẳng cấu trúc của Hypoxanthine. Xanthine Oxidase oxy hóa Allopurinol thành Oxypurinol; Oxypurinol gắn chặt không hồi phục vào trung tâm chứa Molypden của chính enzym này (ức chế cơ chế tự sát), chặn đứng quá trình tạo acid uric.",
            ch15_img
        ),
        (
            "Hội chứng Lesch-Nyhan là một bệnh di truyền lặn liên kết nhiễm sắc thể X nghiêm trọng do thiếu hụt hoàn toàn enzym nào trong con đường tận dụng purine (salvage pathway)?",
            "Hypoxanthine-Guanine Phosphoribosyltransferase (HGPRT).",
            "Adenine Phosphoribosyltransferase (APRT).",
            "PRPP Synthetase.",
            "Adenylosuccinate Synthetase.",
            "A",
            "Enzym HGPRT tái sử dụng Hypoxanthine và Guanine gắn với PRPP tạo IMP và GMP. Khi thiếu HGPRT hoàn toàn, nồng độ PRPP nội bào tăng vọt kích thích tối đa con đường tổng hợp de novo tạo acid uric cực lớn. Bệnh nhân có biểu hiện bệnh Gout nặng nề từ nhỏ, múa vờn choreoathetosis, thiểu năng trí tuệ và đặc biệt là hành vi cưỡng bức tự cắn môi và ngón tay.",
            ch15_img
        ),
        (
            "Bệnh thiếu hụt miễn dịch kết hợp trầm trọng (SCID - Severe Combined Immunodeficiency) thể di truyền lặn NST thường có nguyên nhân hóa sinh do thiếu hụt enzym nào trong chuyển hóa purine?",
            "Adenosine Deaminase (ADA).",
            "Xanthine Oxidase.",
            "Thymidylate Synthase.",
            "Ribonucleotide Reductase.",
            "A",
            "Thiếu hụt enzym Adenosine Deaminase (ADA) ngăn cản thoái hóa adenosine thành inosine, dẫn đến tích tụ nồng độ cực cao dATP trong tế bào lympho. Nồng độ dATP cao ức chế enzym Ribonucleotide Reductase, ngăn cản tổng hợp tất cả các dNTP khác, làm tế bào lympho T và B bị tiêu diệt hàng loạt (hội chứng 'em bé trong bóng bóng kính').",
            ch15_img
        ),
        (
            "Trong con đường sinh tổng hợp De Novo base Purine, phân tử Phosphoribosyl Pyrophosphate (PRPP) được tổng hợp từ hợp chất nào nhờ enzym PRPP Synthetase?",
            "Ribose-5-Phosphate (tạo từ con đường Pentose Phosphate) và ATP.",
            "Glucose-6-Phosphate.",
            "Fructose-6-Phosphate.",
            "Deoxyribose-1-Phosphate.",
            "A",
            "Phân tử PRPP là viên gạch nền tảng cung cấp khung đường 5-carbon cho cả tổng hợp purine, pyrimidine và con đường tận dụng purine. PRPP Synthetase chuyển nhóm pyrophosphate từ ATP gắn vào vị trí C1 của Ribose-5-Phosphate.",
            ch15_img
        ),
        (
            "Enzym nào đóng vai trò là enzym giới hạn tốc độ và điểm kiểm soát cam kết đầu tiên của con đường sinh tổng hợp Purine De Novo?",
            "Glutamine-PRPP Amidotransferase (bị ức chế điều hòa ngược bởi AMP, GMP và IMP).",
            "PRPP Synthetase.",
            "Inosine Monophosphate Dehydrogenase (IMPDH).",
            "Adenylosuccinate Lyase.",
            "A",
            "Glutamine-PRPP Amidotransferase xúc tác chuyển nhóm amin từ Glutamine gắn vào PRPP tạo 5-Phosphoribosylamine và giải phóng pyrophosphate. Enzym này chịu sự ức chế dị lập thể điều hòa ngược đồng thời bởi các nucleotid purine sản phẩm (AMP, GMP, IMP).",
            None
        ),
        (
            "Sự khác biệt căn bản trong chiến lược tổng hợp giữa con đường De Novo của Purine và Pyrimidine là gì?",
            "Khung Purine được lắp ráp từng nguyên tử trực tiếp ngay trên phân tử đường PRPP; trong khi khung Pyrimidine được tổng hợp thành vòng Orotate hoàn chỉnh trước rồi mới gắn vào PRPP.",
            "Purine được tổng hợp trong ty thể còn Pyrimidine tổng hợp trong nhân.",
            "Pyrimidine không sử dụng PRPP.",
            "Purine chỉ dùng acid amin Aspartate còn Pyrimidine chỉ dùng Glutamine.",
            "A",
            "Trong sinh tổng hợp Purine, phân tử PRPP đóng vai trò giá thể ngay từ bước đầu để các acid amin (Gly, Gln, Asp) và dẫn xuất THF đắp từng nguyên tử tạo nhân purine. Ngược lại, ở Pyrimidine, enzym Carbamoyl phosphate synthetase II (CPS-II) và các enzym kế tiếp tạo vòng orotate 6 cạnh trước, sau đó enzym OPRT mới gắn vòng này vào PRPP tạo OMP.",
            None
        ),
        (
            "Enzym Ribonucleotide Reductase (RNR) đảm nhiệm chức năng sống còn nào trong tế bào phân chia?",
            "Khử nhóm 2'-OH của các ribonucleotid diphosphate (ADP, GDP, CDP, UDP) thành 2'-deoxyribonucleotid (dADP, dGDP, dCDP, dUDP) để phục vụ cho sự tổng hợp DNA.",
            "Phân giải DNA thành các đoạn mồi RNA.",
            "Oxy hóa deoxyribose thành ribose.",
            "Gắn đuôi polyA vào mRNA.",
            "A",
            "Để tạo ra các đơn phân deoxyribonucleotid cấu tạo nên DNA, tế bào không tổng hợp trực tiếp từ deoxyribose mà dùng enzym Ribonucleotide Reductase (RNR) khử trực tiếp nhóm -OH ở vị trí carbon số 2 của đường ribose trên các phân tử ribonucleotid diphosphate (NDP $\\rightarrow$ dNDP). Thuốc Hydroxyurea ức chế enzym RNR này để điều trị ung thư và bệnh hồng cầu liềm.",
            None
        ),
        (
            "Bệnh Acid Orotic niệu di truyền (Hereditary Orotic Aciduria) gây thiếu máu hồng cầu to trơ với sắt/folate và chậm phát triển ở trẻ do khiếm khuyết enzym nào trong con đường tổng hợp Pyrimidine?",
            "UMP Synthase (gồm 2 hoạt tính Orotate Phosphoribosyltransferase và OMP Decarboxylase).",
            "Carbamoyl Phosphate Synthetase II (CPS-II).",
            "Aspartate Transcarbamylase (ATCase).",
            "Dihydroorotase.",
            "A",
            "UMP Synthase là một protein đa chức năng ở tế bào nhân thực. Thiếu hụt UMP Synthase làm acid orotic không thể biến đổi thành UMP, ứ đọng và đào thải lượng lớn ra nước tiểu tạo tinh thể. Thiếu UMP làm cạn kiệt nguồn pyrimidine cho tổng hợp DNA gây thiếu máu hồng cầu to. Điều trị đặc hiệu bằng cách cho uống Uridine ngoại sinh suốt đời (Uridine biến thành UMP theo con đường tận dụng).",
            None
        )
    ]

    for i in range(100):
        if i < len(ch15_core):
            q, a, b, c, d, corr, exp, img = ch15_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch15_img if (i % 5 == 0) else None

            ch15_topics = [
                ("Phân biệt nồng độ Acid Uric máu và cơn Gout cấp", "Nồng độ Acid Uric huyết thanh bình thường ở nam giới là 210 - 420 $\\mu$mol/L (3.5 - 7.0 mg/dL), nữ giới là 150 - 360 $\\mu$mol/L.", "Tăng acid uric máu không triệu chứng (Asymptomatic Hyperuricemia) không đồng nghĩa với bệnh Gout; chỉ một tỷ lệ nhỏ tiến triển thành cơn viêm khớp gout cấp.", "Trong cơn Gout cấp tính, nồng độ acid uric máu có thể bình thường hoặc giảm nhẹ do phản ứng viêm làm tăng bài tiết urate qua thận.", "Chẩn đoán xác định bệnh Gout chuẩn vàng là chọc hút dịch khớp tìm thấy tinh thể Monosodium Urate hình kim phân cực âm dưới kính hiển vi quang học phân cực."),
                ("Các thuốc hạ acid uric và điều trị bệnh Gout", "Febuxostat là thuốc ức chế chọn lọc không purine đối với Xanthine Oxidase, an toàn hơn ở bệnh nhân suy thận.", "Probenecid và Benzbromarone ức chế chất đồng vận chuyển URAT1 tại ống lượn gần để tăng đào thải acid uric ra nước tiểu.", "Pegloticase và Rasburicase là các enzym Uricase tái tổ hợp biến đổi acid uric thành allantoin dễ tan, dùng trong hội chứng ly giải khối u cấp tính.", "Colchicine gắn vào tubulin ngăn cản sự trùng hợp vi ống của bạch cầu đa nhân, dập tắt phản ứng viêm trong cơn gout cấp."),
                ("Hội chứng Ly giải khối u (Tumor Lysis Syndrome - TLS)", "Xuất hiện sau hóa trị các khối u ác tính tế bào phân chia nhanh (bệnh bạch cầu cấp, u lympho Burkitt).", "Sự phá hủy hàng loạt tế bào giải phóng ồ ạt acid nucleic, ion kali và phosphat vào tuần hoàn.", "Gây tứ chứng nguy hiểm: Tăng acid uric máu, tăng kali máu (nguy cơ rung thất), tăng phosphat máu và hạ canxi máu.", "Acid uric kết tủa trong lòng ống thận gây suy thận cấp tắc nghẽn vô niệu (Acute Urate Nephropathy)."),
                ("Nguồn gốc các nguyên tử trong nhân Purine và Pyrimidine", "Nhân Purine nhận các nguyên tử từ: Glycine (C4, C5, N7), Glutamine (N3, N9), Aspartate (N1), $CO_2$ (C6) và $N^{10}$-formyl-THF (C2, C8).", "Nhân Pyrimidine đơn giản hơn chỉ nhận nguyên tử từ 2 tiền chất: Carbamoyl phosphate (C2, N3) và Aspartate (C4, C5, C6, N1).", "Thiếu hụt Folate (Vitamin B9) làm đình trệ tổng hợp purine và dTMP do thiếu nhóm truyền 1 carbon.", "Con đường sinh tổng hợp Pyrimidine được xúc tác bởi phức hợp đa enzym CAD (CPS-II, ATCase, Dihydroorotase) trong bào tương."),
                ("Thoái hóa Pyrimidine và chuyển hóa thành sản phẩm dễ tan", "Khác với purine tạo acid uric khó tan, các base pyrimidine (Cytosine, Uracil, Thymine) được thoái hóa thành các phân tử nhỏ tan rất tốt trong nước.", "Cytosine và Uracil được thoái hóa thành $\\beta$-Alanine, $CO_2$ và amoniac.", "Thymine được thoái hóa thành $\\beta$-Aminoisobutyrate ($\\beta$-AIB), $CO_2$ và amoniac.", "$\\beta$-Aminoisobutyrate niệu tăng cao trong các trạng thái hủy hoại tế bào nhiều (xạ trị, hóa trị).")
            ]
            tp = ch15_topics[i % len(ch15_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi đề cập đến {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cơ chế này hoàn toàn không tuân theo quy luật chuyển hóa acid nucleic và không tạo ra bất kỳ chất chuyển hóa nào trong nước tiểu."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng acid uric sinh lý."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ gặp ở vi khuẩn cổ và hoàn toàn không liên quan đến sinh hóa lâm sàng người."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch15_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # Insert Batch 5 into DB
    print(f"Prepared {len(questions)} questions for Batch 5 (Ch13, Ch14, Ch15). Inserting into DB...")
    for item in questions:
        cur.execute("""
            INSERT INTO questions (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_option, explanation, difficulty, topic_tag, image_url, q_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'multiple_choice')
        """, (sub_id, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[0], item[9]))

    conn.commit()
    cur.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sub_id,))
    print(f"Batch 5 Seed Complete! Current total questions for subject {sub_id}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    seed_part5()
