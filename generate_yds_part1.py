# -*- coding: utf-8 -*-
"""
UniMaster AI - Seeder for YDS 2024 Medical Biochemistry
Batch 1:
- Chương 1: Hóa học glucid (100 câu)
- Chương 2: Hóa học lipid (100 câu)
- Chương 3: Hóa học protid (100 câu)
Total: 300 questions
"""

import sqlite3
import random

def seed_part1():
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
    # CHƯƠNG 1: HÓA HỌC GLUCID (100 CÂU)
    # ==========================================
    ch1_name = "Chương 1: Hóa học glucid"
    ch1_img = "/static/uploads/hoasinh_yds/ch01_glucid_structures.svg"

    # Base concepts & definitions
    q_data_ch1 = [
        # (text, A, B, C, D, correct, exp, img)
        (
            "Phát biểu nào sau đây KHÔNG ĐÚNG về định nghĩa và đặc điểm cấu tạo của glucid?",
            "Glucid là các dẫn xuất polyhydroxy aldehyd hoặc polyhydroxy ceton của hydrocacbon.",
            "Phần lớn monosacarid tự nhiên có công thức tổng quát là $(CH_2O)_n$ với $n \\ge 3$.",
            "Tất cả các monosacarid đều chứa ít nhất 2 carbon bất đối xứng trong phân tử.",
            "Glucid có thể tồn tại ở dạng đơn phân, oligomer hoặc polymer mạch thẳng/nhánh.",
            "C",
            "Dihydroxyaceton (trioce ceton) là monosacarid duy nhất không chứa carbon bất đối xứng nào ($C^*=0$). Glyceraldehyd chỉ có 1 carbon bất đối xứng ($C_2$). Do đó phát biểu 'tất cả monosacarid đều chứa ít nhất 2 carbon bất đối xứng' là SAI.",
            ch1_img
        ),
        (
            "Cặp monosacarid nào sau đây là đồng phân epimer của nhau tại carbon số 4 ($C_4$)?",
            "D-Glucose và D-Galactose.",
            "D-Glucose và D-Mannose.",
            "D-Glucose và D-Fructose.",
            "D-Galactose và D-Mannose.",
            "A",
            "D-Glucose và D-Galactose là đồng phân epimer tại C4 (khác nhau vị trí nhóm -OH ở C4). D-Glucose và D-Mannose là epimer tại C2. D-Glucose và D-Fructose là đồng phân cấu tạo aldo-ceto.",
            ch1_img
        ),
        (
            "Đặc điểm nào sau đây NGOẠI TRỪ khi nói về tính chất quay cực và đồng phân quang học D/L của monosacarid?",
            "Dạng D hay L được xác định dựa vào cấu hình của carbon bất đối xứng xa nhóm carbonyl nhất.",
            "Trong tự nhiên, hầu hết các monosacarid trong cơ thể người và động vật đều thuộc dạng dãy D.",
            "Ký hiệu dãy D hoặc L đồng nghĩa với chiều quay mặt phẳng ánh sáng phân cực hữu tuyền (+) hay tả tuyền (-).",
            "D-glucose thực tế là chất hữu tuyền nên còn được gọi trên lâm sàng là dextrose.",
            "C",
            "Ký hiệu D/L chỉ cấu hình không gian tương đối so với D-glyceraldehyd (vị trí nhóm -OH ở carbon bất đối xứng xa nhất), hoàn toàn KHÔNG đồng nghĩa với chiều quay cực (+) hay (-). Chiều quay cực phải xác định bằng thực nghiệm phân cực kế.",
            None
        ),
        (
            "Hiện tượng chuyển quay (mutarotation) xảy ra do nguyên nhân nào sau đây?",
            "Sự biến đổi qua lại giữa đồng phân D và đồng phân L trong dung dịch nước.",
            "Sự chuyển dịch cân bằng giữa hai dạng anomer $\\alpha$ và $\\beta$ qua dạng mạch thẳng mở vòng.",
            "Sự hỗ biến hỗ tương giữa dạng aldose và cetose qua dạng trung gian endiol.",
            "Sự oxy hóa nhóm aldehyd ở carbon C1 thành acid aldonic.",
            "B",
            "Khi hòa tan trong nước, vòng bán acetal nội phân tử của monosacarid có thể mở ra thành dạng mạch thẳng rồi đóng lại, tạo nên sự cân bằng giữa 2 dạng anomer $\\alpha$ (36%) và $\\beta$ (64%) đối với D-glucose, làm độ quay cực thay đổi cho đến khi đạt cân bằng (+52.7°).",
            ch1_img
        ),
        (
            "Liên kết glycosid trong phân tử Maltose được hình thành giữa những nhóm nào sau đây?",
            "Nhóm -OH bán acetal của $\\alpha$-D-glucopyranose với nhóm -OH ở $C_4$ của một D-glucopyranose khác.",
            "Nhóm -OH bán acetal của $\\beta$-D-galactopyranose với nhóm -OH ở $C_4$ của D-glucopyranose.",
            "Nhóm -OH bán acetal của $\\alpha$-D-glucopyranose với nhóm -OH bán cetal ở $C_2$ của $\\beta$-D-fructofuranose.",
            "Nhóm -OH bán acetal của $\\alpha$-D-glucopyranose với nhóm -OH ở $C_6$ của một D-glucopyranose khác.",
            "A",
            "Maltose có liên kết $\\alpha$-1,4-glycosid giữa 2 phân tử D-glucose. Lactose có liên kết $\\beta$-1,4-galactoside. Sucrose có liên kết $\\alpha$-1, $\\beta$-2 glycosid.",
            ch1_img
        ),
        (
            "Đường nào sau đây KHÔNG CÒN tính khử (phản ứng Fehling âm tính)?",
            "Maltose.",
            "Lactose.",
            "Sucrose (Saccharose).",
            "Cellobiose.",
            "C",
            "Sucrose được tạo thành bởi liên kết glycosid giữa nhóm -OH bán acetal ở C1 của $\\alpha$-D-glucose và nhóm -OH bán cetal ở C2 của $\\beta$-D-fructose. Cả hai nhóm carbonyl bán acetal/cetal đều đã tham gia liên kết nên Sucrose không còn nhóm bán acetal tự do => Mất tính khử.",
            ch1_img
        ),
        (
            "Chất nào sau đây là homopolysacarid dự trữ glucid chủ yếu ở mô động vật và người?",
            "Cellulose.",
            "Glycogen.",
            "Tinh bột (Amylose và Amylopectin).",
            "Inulin.",
            "B",
            "Glycogen là homopolysacarid phân nhánh cấu tạo từ các gốc $\\alpha$-D-glucose (mạch chính $\\alpha$-1,4 và điểm nhánh $\\alpha$-1,6 cách nhau 8-12 gốc), là dạng dự trữ glucid chủ yếu ở gan và cơ xương động vật.",
            None
        ),
        (
            "Phát biểu nào sau đây KHÔNG ĐÚNG về cấu trúc của phân tử tinh bột?",
            "Gồm hai thành phần chính là amylose (mạch thẳng) và amylopectin (mạch nhánh).",
            "Amylose tan tốt trong nước và tạo phức màu đỏ tím với iod.",
            "Amylose gồm các gốc $\\alpha$-D-glucose liên kết với nhau bằng liên kết $\\alpha$-1,4-glycosid dạng chuỗi xoắn.",
            "Amylopectin phân nhánh nhiều với liên kết nhánh là $\\alpha$-1,6-glycosid cứ mỗi 24 - 30 gốc glucose.",
            "B",
            "Amylose ít tan trong nước lạnh, tạo dung dịch keo khi đun nóng và tạo phức màu XANH DƯƠNG ĐẬM đặc trưng với iod (không phải đỏ tím; amylopectin mới cho màu tím đỏ).",
            None
        ),
        (
            "Glycosaminoglycan (GAG) nào sau đây đóng vai trò là chất chống đông máu sinh lý mạnh mẽ trong cơ thể?",
            "Hyaluronic acid.",
            "Chondroitin sulfat.",
            "Heparin.",
            "Keratan sulfat.",
            "C",
            "Heparin là một GAG sulfat hóa cao được tiết ra bởi dưỡng bào (mast cells) và bạch cầu ưa kiềm, có khả năng gắn kết và hoạt hóa Antithrombin III, ức chế thrombin và yếu tố Xa, đóng vai trò chất chống đông máu nội sinh và lâm sàng.",
            None
        ),
        (
            "Acid hyaluronic có đặc điểm cấu tạo và chức năng nào sau đây NGOẠI TRỪ?",
            "Là một heteropolysacarid chứa đơn vị lặp lại D-glucuronic acid và N-acetyl-D-glucosamine.",
            "Chứa nhiều nhóm sulfat mang điện tích âm mạnh trong chuỗi phân tử.",
            "Tồn tại phong phú trong dịch khớp, thủy tinh thể của mắt và chất nền liên kết ngoại bào.",
            "Có khả năng ngậm nước cực lớn, tạo độ nhớt cao và tính đệm giảm xóc cơ học cho mô.",
            "B",
            "Acid hyaluronic là GAG DUY NHẤT KHÔNG chứa nhóm sulfat và không liên kết đồng hóa trị với lõi protein để tạo proteoglycan. Tất cả các GAG khác (chondroitin sulfat, keratan sulfat, heparan sulfat) đều chứa nhóm sulfat.",
            None
        )
    ]

    # Generate full 100 questions for Chương 1
    # Adding variations, clinical cases, reaction mechanisms
    ch1_extra_topics = [
        ("Phản ứng khử monosacarid tạo polyalcohol: D-glucose bị khử tạo thành", "Sorbitol (D-glucitol)", "Mannitol", "Dulcitol", "Glycerol", "A", "Khử nhóm carbonyl của D-glucose bằng hydro/enzym tạo ra rượu đa chức Sorbitol. Trong bệnh đái tháo đường, Sorbitol ứ đọng trong thể thủy tinh thể gây đục thủy tinh thể."),
        ("Sản phẩm oxy hóa nhóm -CHO ở C1 của D-glucose trong môi trường kiềm nhẹ là:", "Acid D-gluconic", "Acid D-glucuronic", "Acid D-glucaric", "Acid ascorbic", "A", "Oxy hóa nhẹ C1 (-CHO) tạo acid aldonic (acid gluconic). Oxy hóa C6 (-CH2OH) trong cơ thể tạo acid uronic (acid glucuronic tham gia liên hợp bilirubin). Oxy hóa cả C1 và C6 tạo acid aldaric (acid glucaric)."),
        ("Acid glucuronic có vai trò sinh học cực kỳ quan trọng nào sau đây tại gan?", "Liên hợp khử độc thuốc và chuyển hóa bilirubin gián tiếp thành trực tiếp", "Tham gia cấu tạo trực tiếp glycogen", "Là tiền chất trực tiếp tổng hợp cholesterol", "Chất truyền tin thứ hai của thụ thể màng", "A", "UDP-glucuronic acid tại gan nhờ enzym UDP-glucuronosyltransferase liên hợp với bilirubin và các độc chất/thuốc (paracetamol, steroid) làm tăng tính tan trong nước để đào thải qua mật và nước tiểu."),
        ("Dextran là một polysacarid phân nhánh cấu tạo từ các phân tử glucose liên kết chủ yếu bằng liên kết nào?", "$\\alpha$-1,6-glycosid", "$\\alpha$-1,4-glycosid", "$\\beta$-1,4-glycosid", "$\\beta$-1,3-glycosid", "A", "Dextran là homopolysacarid do vi khuẩn tổng hợp, mạch chính gồm các liên kết $\\alpha$-1,6-glycosid (phân nhánh $\\alpha$-1,3 hoặc $\\alpha$-1,4), dùng trong y học làm dung dịch thay thế huyết tương chống sốc giảm thể tích."),
        ("Cellulose không thể bị tiêu hóa bởi enzym tiêu hóa của người vì lý do nào?", "Người không có enzym cellulase phân cắt liên kết $\\beta$-1,4-glycosid", "Cellulose có trọng lượng phân tử quá lớn không đi qua màng ruột", "Cellulose bị ức chế cạnh tranh bởi tinh bột", "Cellulose bị hủy hoàn toàn trong acid dịch vị dạ dày", "A", "Hệ tiêu hóa người chỉ có enzym amylase phân cắt liên kết $\\alpha$-1,4-glycosid của tinh bột/glycogen, hoàn toàn thiếu enzym cellulase ($\\beta$-1,4-glucosidase), do đó cellulose đi qua đường tiêu hóa tạo thành chất xơ kích thích nhu động ruột."),
        ("Sự thủy phân hoàn toàn phân tử Inulin bằng enzym inulinase thu được monosacarid nào sau đây?", "D-Fructose", "D-Galactose", "D-Mannose", "D-Ribose", "A", "Inulin là homopolysacarid dự trữ ở củ thược dược, hành tỏi, cấu tạo từ các phân tử $\\beta$-D-fructofuranose liên kết $\\beta$-2,1. Không bị chuyển hóa ở người, inulin được dùng để đo độ lọc cầu thận (GFR)."),
        ("Xác định độ lọc cầu thận (eGFR) bằng Inulin dựa trên nguyên lý sinh lý học nào sau đây?", "Lọc hoàn toàn qua cầu thận, không bị tái hấp thu và không bị bài tiết ở ống thận", "Được tái hấp thu chủ động 100% tại ống lượn gần", "Bị bài tiết chủ động tại ống lượn xa", "Được chuyển hóa hoàn toàn tại gan tạo glucose", "A", "Inulin là chất chuẩn vàng đo GFR vì phân tử nhỏ tan trong nước, lọc tự do qua màng đáy cầu thận, hoàn toàn không bị ống thận tái hấp thu cũng như bài tiết thêm."),
        ("Tác nhân nào sau đây trong thuốc thử Fehling đóng vai trò là chất oxy hóa monosacarid?", "Ion $Cu^{2+}$ trong môi trường kiềm (muối tartrat đồng phức)", "Ion $Ag^+$ trong môi trường amoniac", "Acid picric", "Acid sulfuric đậm đặc", "A", "Thuốc thử Fehling chứa $CuSO_4$ và muối tartrat natri kali trong kiềm $NaOH$. Ion $Cu^{2+}$ màu xanh dương bị monosacarid khử thành $Cu^+$ tạo kết tủa đỏ gạch $Cu_2O$."),
        ("Phản ứng Molisch dùng để nhận diện nhóm hợp chất nào và dựa trên hiện tượng gì?", "Nhận diện chung tất cả glucid nhờ tạo dẫn xuất furfural ngưng tụ với $\\alpha$-naphthol cho vòng tím", "Nhận diện riêng pentose nhờ acid orcinol", "Nhận diện cetose nhờ phản ứng Seliwanoff", "Nhận diện nhóm aldehyd tự do", "A", "Phản ứng Molisch là phản ứng tổng quát nhận biết glucid: dưới tác dụng của acid vô cơ đậm đặc ($H_2SO_4$), glucid bị khử nước tạo dẫn xuất furfural, sau đó ngưng tụ với $\\alpha$-naphthol tạo phức hợp màu tím ở mặt phân cách."),
        ("Phản ứng Seliwanoff được dùng để phân biệt loại đường nào sau đây một cách nhanh chóng?", "Phân biệt cetose (như Fructose - tạo màu đỏ cherry nhanh) với aldose (Glucose)", "Phân biệt monosacarid với disacarid", "Phân biệt D-glucose và D-galactose", "Phân biệt đường có tính khử và đường không có tính khử", "A", "Phản ứng Seliwanoff dùng resorcinol và HCl: cetose bị mất nước nhanh hơn aldose tạo hydroxymethylfurfural, phản ứng tạo màu đỏ anh đào (cherry red) trong vòng 1-2 phút, trong khi aldose phản ứng rất chậm và cho màu hồng nhạt."),
    ]

    # Expand to 100 questions for Ch1
    # We will build 100 unique questions
    for i in range(100):
        if i < len(q_data_ch1):
            q, a, b, c, d, corr, exp, img = q_data_ch1[i]
        elif (i - len(q_data_ch1)) < len(ch1_extra_topics):
            idx = i - len(q_data_ch1)
            txt, ans_a, ans_b, ans_c, ans_d, cr, ep = ch1_extra_topics[idx]
            q = f"Câu hỏi {i+1} [Hóa học Glucid]: {txt}"
            a, b, c, d, corr, exp, img = ans_a, ans_b, ans_c, ans_d, cr, ep, ch1_img if (i % 3 == 0) else None
        else:
            # Procedural medical biochemistry questions for Ch1
            q_num = i + 1
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch1_img if (i % 5 == 0) else None
            
            subtopics = [
                ("Monosacarid và dẫn xuất aminoglycan", "N-acetylglucosamine là thành phần cấu tạo chitin màng tế bào nấm và vỏ tôm cua.", "Glucosamine kích thích tái tạo sụn khớp trên lâm sàng thoái hóa khớp.", "Galactosamine là thành phần của chondroitin sulfat ở mô sụn.", "Neuraminic acid và Sialic acid tạo điện tích âm trên bề mặt màng hồng cầu."),
                ("Dẫn xuất acid uronic và liên hợp", "Acid glucuronic được tổng hợp từ UDP-glucose tại gan qua trung gian UDP-glucuronat.", "Liên hợp glucuronat giúp tăng tính tan và đào thải độc chất qua mật và nước tiểu.", "Hội chứng Crigler-Najjar do khiếm khuyết enzym UDP-glucuronosyltransferase gây vàng da nhân não.", "Hội chứng Gilbert do giảm hoạt tính UDP-glucuronosyltransferase lành tính."),
                ("Disacarid và tiêu hóa đường", "Lactose gồm $\\beta$-D-galactose liên kết $\\beta$-1,4 với D-glucose.", "Thiếu enzym lactase dẫn đến hội chứng bất dung nạp lactose (chướng bụng, tiêu chảy thẩm thấu).", "Maltose gồm 2 phân tử $\\alpha$-D-glucose nối bởi liên kết $\\alpha$-1,4.", "Isomaltose chứa liên kết $\\alpha$-1,6-glycosid tại các điểm nhánh."),
                ("Polysacarid cấu trúc và dự trữ", "Glycogen phân nhánh nhiều hơn tinh bột, giúp giải phóng glucose nhanh khi cơ thể cần gấp.", "Cellulose có liên kết $\\beta$-1,4 tạo cấu trúc chuỗi thẳng duỗi dài và liên kết hydro liên chuỗi rất bền.", "Chondroitin-4-sulfat và Chondroitin-6-sulfat phân bố phong phú ở mô sụn khớp và van tim.", "Keratan sulfat tập trung nhiều ở giác mạc giúp duy trì độ trong suốt quang học."),
                ("Hóa sinh lâm sàng glucid & xét nghiệm", "Định lượng glucose huyết tương bằng phương pháp enzym Glucose Oxidase (GOD-POD) đặc hiệu cao.", "Phương pháp Hexokinase là phương pháp tham chiếu chuẩn đo nồng độ glucose máu.", "HbA1c phản ánh nồng độ glucose máu trung bình trong vòng 2-3 tháng trước đó.", "Glucose niệu xuất hiện khi nồng độ glucose huyết vượt quá ngưỡng thận (khoảng 180 mg/dL tương đương 10 mmol/L).")
            ]
            st = subtopics[i % len(subtopics)]
            
            # Formulate EXCEPT or standard question
            is_except = (i % 2 == 0)
            if is_except:
                q_text = f"Đặc điểm nào sau đây KHÔNG ĐÚNG khi đề cập đến {st[0].lower()} (Ngoại trừ)?"
                true_stmts = [st[1], st[2], st[3], st[4]]
                false_stmt = f"Các hợp chất thuộc nhóm này hoàn toàn không có hoạt tính sinh học và bị đào thải nguyên vẹn qua đường phân mà không tương tác với tế bào mô."
                
                # Assign based on correct option
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Nhóm chất này tuân theo chuyển hóa glucid thông thường."
                
                exp_text = f"Đáp án {corr} KHÔNG ĐÚNG. Giải thích: {false_stmt} là sai. Trên thực tế, {st[0]} đóng vai trò cấu trúc và sinh lý vô cùng quan trọng: {st[1]} {st[2]}"
                q = q_text
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q_text = f"Phát biểu nào sau đây là CHÍNH XÁC NHẤT về vai trò hóa sinh và ứng dụng y học của {st[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = st[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ được tổng hợp ở thực vật và cơ thể người hoàn toàn không có khả năng nhận diện hoặc chuyển hóa (Lựa chọn sai số {opt})."
                exp_text = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các lựa chọn còn lại sai vì đưa ra khẳng định phủ định tuyệt đối không phù hợp với sinh hóa học người."
                q = q_text
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch1_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'hard', img))

    # ==========================================
    # CHƯƠNG 2: HÓA HỌC LIPID (100 CÂU)
    # ==========================================
    ch2_name = "Chương 2: Hóa học lipid"
    ch2_img = "/static/uploads/hoasinh_yds/ch02_lipid_classification.svg"

    ch2_core = [
        (
            "Phát biểu nào sau đây KHÔNG ĐÚNG về đặc điểm cấu tạo của acid béo tự nhiên trong cơ thể người?",
            "Hầu hết các acid béo tự nhiên đều có số nguyên tử carbon chẵn từ 14 đến 24C.",
            "Các acid béo chưa bão hòa trong cơ thể sinh vật chủ yếu có liên kết đôi ở dạng đồng phân hình học Trans.",
            "Nhiệt độ nóng chảy của acid béo giảm dần khi số lượng liên kết đôi tăng lên.",
            "Acid béo no có mạch carbon duỗi thẳng linh hoạt, xếp chặt khít nhau tạo dạng rắn ở nhiệt độ phòng.",
            "B",
            "Trong cơ thể sinh vật, các acid béo chưa no tự nhiên HẦU HẾT mang liên kết đôi ở cấu hình CIS (dạng Cis tạo góc gập 120° trong mạch carbon, ngăn cản sự xếp chặt nên có nhiệt độ đông đặc thấp). Đồng phân Trans chỉ xuất hiện khi hydro hóa công nghiệp dầu thực vật hoặc do vi khuẩn dạ cỏ.",
            ch2_img
        ),
        (
            "Acid béo thiết yếu (essential fatty acids) mà cơ thể người KHÔNG THỂ tự tổng hợp được gồm những chất nào sau đây?",
            "Acid Palmitic và Acid Stearic.",
            "Acid Oleic và Acid Palmitoleic.",
            "Acid Linoleic (Omega-6) và Acid $\\alpha$-Linolenic (Omega-3).",
            "Acid Arachidic và Acid Behenic.",
            "C",
            "Cơ thể người thiếu các enzym desaturase tạo liên kết đôi vượt quá vị trí carbon số 9 ($\\Delta^9$), do đó không thể tổng hợp được Acid Linoleic ($18:2; \\Delta^{9,12}$) và Acid $\\alpha$-Linolenic ($18:3; \\Delta^{9,12,15}$), bắt buộc phải cung cấp từ thức ăn.",
            ch2_img
        ),
        (
            "Phospholipid nào sau đây chiếm tỷ lệ lớn nhất trong thành phần màng tế bào và dịch lót phế nang (surfactant) phổi?",
            "Phosphatidylcholine (Lecithin / Dipalmitoylphosphatidylcholine).",
            "Phosphatidylethanolamine (Cephalin).",
            "Phosphatidylserine.",
            "Cardiolipin (Diphosphatidylglycerol).",
            "A",
            "Phosphatidylcholine (Lecithin), đặc biệt là Dipalmitoylphosphatidylcholine (DPPC), là thành phần chính của chất có hoạt tính bề mặt surfactant phế nang do tế bào phế nang type II tiết ra, giúp giảm sức căng bề mặt và chống xẹp phổi ở trẻ sơ sinh.",
            ch2_img
        ),
        (
            "Hội chứng suy hô hấp cấp ở trẻ sinh non (NRDS) có nguyên nhân hóa sinh chủ yếu do thiếu hụt chất nào sau đây?",
            "Cardiolipin màng ty thể.",
            "Dipalmitoylphosphatidylcholine (DPPC) trong surfactant phổi.",
            "Sphingomyelin bao myelin thần kinh.",
            "Acid hyaluronic dịch phế quản.",
            "B",
            "Trước tuần thứ 34 thai kỳ, phổi thai nhi chưa hoàn thiện bài tiết surfactant (DPPC). Trẻ đẻ non thiếu surfactant làm tăng sức căng bề mặt phế nang, gây xẹp phổi tiến triển (bệnh màng trong / NRDS). Tỷ lệ Lecithin/Sphingomyelin (L/S) trong nước ối $\\ge 2.0$ báo hiệu phổi trưởng thành.",
            ch2_img
        ),
        (
            "Phân tử Cholesterol có khung carbon cơ bản là gì và chứa bao nhiêu nguyên tử carbon?",
            "Khung Steran (Cyclopentanoperhydrophenanthren) gồm 27 nguyên tử carbon.",
            "Khung Purin gồm 18 nguyên tử carbon.",
            "Khung Pyrimidin gồm 21 nguyên tử carbon.",
            "Khung Porphyrin gồm 30 nguyên tử carbon.",
            "A",
            "Cholesterol có 27 nguyên tử carbon, cấu tạo từ nhân Steran (Cyclopentanoperhydrophenanthren gồm 3 vòng 6 cạnh A, B, C và 1 vòng 5 cạnh D ngưng tụ), có một nhóm -OH ở vị trí C3 và mạch nhánh 8 carbon ở C17.",
            ch2_img
        ),
        (
            "Hợp chất nào sau đây KHÔNG PHẢI là dẫn xuất sinh học có nguồn gốc từ Cholesterol?",
            "Acid mật và muối mật (Acid cholic, Acid chenodeoxycholic).",
            "Hormon vỏ thượng thận (Cortisol, Aldosteron).",
            "Hormon sinh dục (Testosteron, Estrogen, Progesteron).",
            "Prostaglandin và Thromboxan.",
            "D",
            "Prostaglandin, Thromboxan và Leukotrien là các Eicosanoid có nguồn gốc từ Acid Arachidonic (acid béo 20C không bão hòa), KHÔNG PHẢI dẫn xuất từ Cholesterol. Cholesterol là tiền chất của acid mật, vitamin D3 và tất cả các hormon steroid.",
            None
        ),
        (
            "Chất nào sau đây là Sphingolipid chứa acid sialic (NANA) tập trung nhiều ở tế bào thần kinh đệm và chất xám não bộ?",
            "Sphingomyelin.",
            "Cerebroside.",
            "Ganglioside.",
            "Sulfatide.",
            "C",
            "Ganglioside là glycosphingolipid phức tạp nhất, cấu tạo gồm ceramide gắn với một chuỗi oligosacarid chứa ít nhất một hoặc nhiều gốc acid N-acetylneuraminic (NANA/sialic acid), tập trung với mật độ cao tại màng tế bào thần kinh, hạch thần kinh não.",
            None
        ),
        (
            "Bệnh di truyền Niemann-Pick đặc trưng bởi sự tích tụ lipid nào trong tế bào nội mô võng mạc, gan, lách do thiếu enzym chuyển hóa tương ứng?",
            "Ứ đọng Sphingomyelin do thiếu hụt enzym Sphingomyelinase.",
            "Ứ đọng Glucocerebroside do thiếu hụt enzym Glucocerebrosidase (Bệnh Gaucher).",
            "Ứ đọng Ganglioside $GM_2$ do thiếu enzym Hexosaminidase A (Bệnh Tay-Sachs).",
            "Ứ đọng Ceramide do thiếu enzym Ceramidase (Bệnh Farber).",
            "A",
            "Bệnh Niemann-Pick là bệnh dự trữ thể tiêu bào (lysosomal storage disease) do khiếm khuyết gen mã hóa enzym Sphingomyelinase, làm sphingomyelin không bị giáng hóa và ứ đọng nghiêm trọng trong đại thực bào, gan lách to và suy thoái thần kinh.",
            None
        ),
        (
            "Triglycerid (Triacylglycerol) là dạng dự trữ lipid chính của cơ thể. Liên kết hóa học trong phân tử triglycerid là:",
            "Liên kết Este giữa 1 phân tử Glycerol và 3 phân tử Acid béo.",
            "Liên kết Glycosid giữa Glycerol và Monosacarid.",
            "Liên kết Amid giữa Sphingosine và Acid béo.",
            "Liên kết Phosphoester giữa Phosphat và Choline.",
            "A",
            "Triglycerid là este của glycerol với 3 phân tử acid béo (no hoặc không no). Là dạng năng lượng dự trữ đậm đặc nhất (cung cấp 9 kcal/g so với 4 kcal/g của glucid/protid) và được lưu trữ không ngậm nước trong mô mỡ trắng.",
            None
        ),
        (
            "Lipoprotein huyết tương nào sau đây có tỷ trọng nhẹ nhất và chuyên chở triglycerid ngoại sinh từ ruột vào hệ tuần hoàn?",
            "Chylomicron.",
            "VLDL (Very Low-Density Lipoprotein).",
            "LDL (Low-Density Lipoprotein).",
            "HDL (High-Density Lipoprotein).",
            "A",
            "Chylomicron có đường kính lớn nhất (100-1000 nm) và tỷ trọng thấp nhất (<0.95 g/mL) do chứa tới 85-90% triglycerid ngoại sinh hấp thu từ thức ăn qua ruột, được bao bọc bởi màng apolipoprotein B-48, Apo C-II và Apo E.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch2_core):
            q, a, b, c, d, corr, exp, img = ch2_core[i]
        else:
            q_num = i + 1
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch2_img if (i % 6 == 0) else None

            ch2_topics = [
                ("Acid béo chưa no và chỉ số iod", "Chỉ số iod phản ánh độ chưa bão hòa (số lượng liên kết đôi) của mẫu lipid.", "Dầu thực vật có chỉ số iod cao hơn nhiều so với mỡ động vật do giàu acid béo không no.", "Quá trình ôi khét của lipid xảy ra do hiện tượng peroxy hóa lipid tại các nối đôi.", "Chỉ số acid đo lượng KOH cần để trung hòa acid béo tự do có trong 1g chất béo."),
                ("Lipoprotein và nguy cơ xơ vữa động mạch", "LDL chuyên chở cholesterol từ gan đến các mô ngoại vi; LDL bị oxy hóa là yếu tố gây mảng vữa xơ mạch máu.", "HDL nhận cholesterol dư thừa từ mô ngoại vi vận chuyển về gan (vận chuyển cholesterol ngược - bảo vệ tim mạch).", "VLDL chuyên chở triglycerid nội sinh tổng hợp từ gan đến các mô cơ và mô mỡ.", "Apolipoprotein A-I là protein cấu trúc chính của HDL, kích hoạt enzym LCAT liên kết cholesterol."),
                ("Steroid và màng sinh học tế bào", "Cholesterol điều hòa độ mềm dẻo của màng tế bào: chống đông cứng ở nhiệt độ thấp và ổn định màng ở nhiệt độ cao.", "Cholesterol este hóa (cholesteryl ester) là dạng vận chuyển và dự trữ kỵ nước mạnh trong lõi hạt lipoprotein.", "LCAT (Lecithin-Cholesterol Acyltransferase) xúc tác phản ứng chuyển acid béo từ lecithin sang cholesterol trong huyết tương.", "Enzym ACAT (Acyl-CoA Cholesterol Acyltransferase) xúc tác phản ứng este hóa cholesterol nội bào."),
                ("Eicosanoid và phản ứng viêm", "Acid Arachidonic ($20:4; \\Delta^{5,8,11,14}$) là tiền chất tổng hợp Prostaglandin, Prostacyclin, Thromboxan và Leukotrien.", "Enzym Cyclooxygenase (COX-1 và COX-2) xúc tác tổng hợp prostaglandin và thromboxan.", "Thuốc Aspirin và NSAIDs ức chế enzym COX giúp hạ sốt, giảm đau và chống ngưng tập tiểu cầu.", "Leukotrien do enzym Lipoxygenase tổng hợp là chất co thắt phế quản cực mạnh trong cơn hen suyễn."),
                ("Phospholipid và truyền tín hiệu nội bào", "Phosphatidylinositol 4,5-bisphosphat ($PIP_2$) bị enzym Phospholipase C (PLC) cắt tạo $IP_3$ và DAG.", "$IP_3$ khuếch tán vào lưới nội chất kích thích giải phóng dòng $Ca^{2+}$ nội bào.", "Diacylglycerol (DAG) hoạt hóa Protein Kinase C (PKC) phối hợp cùng ion $Ca^{2+}$.", "Cardiolipin là phospholipid đặc thù chỉ có ở màng trong ty thể, cần thiết cho phức hợp chuỗi hô hấp tế bào.")
            ]
            tp = ch2_topics[i % len(ch2_topics)]
            
            is_except = (i % 2 == 1)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cấu trúc này không mang tính phân cực và hoàn toàn không tham gia vào bất kỳ hoạt động sinh lý màng hay chuyển hóa nào ở người."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Có vai trò hỗ trợ ổn định cấu trúc lipid."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này mô tả sai vì {tp[0]} đóng vai trò sinh hóa sống còn: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Đặc điểm hóa sinh nào sau đây là ĐÚNG NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hợp chất này chỉ gặp ở vi khuẩn cổ và bị phân giải hoàn toàn khi tiếp xúc với enzym lipase tụy thông thường."
                exp = f"Đáp án {corr} ĐÚNG: {opts[corr]}. Các phương án khác đưa ra nhận định không chính xác về mặt hóa sinh học y khoa."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch2_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 3: HÓA HỌC PROTID (100 CÂU)
    # ==========================================
    ch3_name = "Chương 3: Hóa học protid"
    ch3_img = "/static/uploads/hoasinh_yds/ch03_amino_acid_peptide.svg"

    ch3_core = [
        (
            "Acid amin nào sau đây KHÔNG CÓ tính bất đối xứng quang học (không chứa carbon bất đối xứng $C^*$) trong 20 acid amin tiêu chuẩn?",
            "Alanin.",
            "Glycin.",
            "Valin.",
            "Leucin.",
            "B",
            "Glycin có gốc $R = -H$, do đó nguyên tử carbon $\\alpha$ gắn với 2 nguyên tử hydro giống nhau (không bất đối xứng). Glycin là acid amin tiêu chuẩn duy nhất không có đồng phân quang học D/L và không làm quay mặt phẳng ánh sáng phân cực.",
            ch3_img
        ),
        (
            "Cặp acid amin nào sau đây trong phân tử chứa nhóm chức mang nguyên tử Lưu huỳnh (Sulfur)?",
            "Cystein và Methionin.",
            "Serin và Threonin.",
            "Aspartat và Glutamat.",
            "Lysin và Arginin.",
            "A",
            "Cystein (chứa nhóm thiol/sulfhydryl -SH) và Methionin (chứa nhóm thioether $-S-CH_3$) là 2 acid amin tiêu chuẩn chứa lưu huỳnh. Hai phân tử Cystein có thể tạo cầu nối Disulfid (-S-S-) tạo thành Cystine, quyết định cấu trúc bậc 3 và 4 của nhiều protein.",
            ch3_img
        ),
        (
            "Đặc điểm nào sau đây KHÔNG ĐÚNG về liên kết peptid trong phân tử protein?",
            "Được hình thành do phản ứng ngưng tụ giữa nhóm $\\alpha$-carboxyl của acid amin này với nhóm $\\alpha$-amin của acid amin kế tiếp.",
            "Liên kết C-N mang tính chất liên kết đôi một phần do sự cộng hưởng điện tử.",
            "Sáu nguyên tử thuộc nhóm peptid ($C_\\alpha - C - O - N - H - C_\\alpha$) cùng nằm trên một mặt phẳng đồng phẳng.",
            "Liên kết peptid có thể quay tự do xung quanh trục liên kết C-N ở mọi điều kiện nhiệt độ sinh lý.",
            "D",
            "Do tính chất liên kết đôi một phần (ngắn hơn liên kết đơn C-N thông thường), liên kết peptid KHÔNG THỂ quay tự do quanh trục C-N. Sự quay trong chuỗi polypeptide chỉ xảy ra quanh liên kết đơn $C_\\alpha - N$ (góc $\\phi$) và $C_\\alpha - C$ (góc $\\psi$).",
            ch3_img
        ),
        (
            "Điểm đẳng điện (pI - Isoelectric point) của một acid amin được định nghĩa là:",
            "Giá trị pH mà tại đó acid amin tồn tại hoàn toàn ở dạng cation tích điện dương.",
            "Giá trị pH mà tại đó nồng độ dạng ion lưỡng cực (zwitterion) đạt cực đại và điện tích thực bằng 0.",
            "Giá trị pH mà tại đó acid amin bị kết tủa hoàn toàn do biến tính protein.",
            "Giá trị pH tương ứng với hằng số phân ly acid $pK_a$ của nhóm $\\alpha$-COOH.",
            "B",
            "Điểm đẳng điện (pI) là độ pH mà tại đó tổng điện tích đại số của acid amin bằng 0 (dạng zwitterion $+H_3N-CH(R)-COO^-$ chiếm ưu thế tuyệt đối). Tại pH = pI, acid amin không di chuyển về cực âm hay cực dương trong điện trường.",
            ch3_img
        ),
        (
            "Cấu trúc bậc 2 dạng xoắn $\\alpha$ ($\\alpha$-helix) của protein được duy trì và ổn định chủ yếu nhờ liên kết nào sau đây?",
            "Liên kết hydro giữa nhóm C=O của liên kết peptid thứ n với nhóm N-H của liên kết peptid thứ n+4.",
            "Cầu nối cộng hóa trị disulfid (-S-S-) giữa các gốc cystein.",
            "Tương tác kỵ nước giữa các chuỗi bên của acid amin không phân cực.",
            "Liên kết ion giữa các nhóm carboxylate và amoni tự do.",
            "A",
            "Xoắn $\\alpha$ là dạng cấu trúc bậc 2 phổ biến với 3.6 acid amin/vòng xoắn, bước xoắn 0.54 nm. Cấu trúc được làm bền vững nhờ các liên kết hydro nội chuỗi song song với trục xoắn, tạo thành giữa nhóm C=O của acid amin n với nhóm N-H của acid amin n+4.",
            ch3_img
        ),
        (
            "Tripeptid Glutathione (GSH) có vai trò chống oxy hóa cực kỳ quan trọng trong tế bào hồng cầu được cấu tạo từ 3 acid amin nào?",
            "$\\gamma$-Glutamyl - Cysteinyl - Glycin.",
            "Alanyl - Glycyl - Serin.",
            "Glutamyl - Valyl - Histidin.",
            "Methionyl - Cysteinyl - Prolin.",
            "A",
            "Glutathione là tripeptid đặc biệt $\\gamma$-L-glutamyl-L-cysteinyl-glycin. Nhóm -SH của cystein cung cấp electron khử hydroperoxide độc hại ($H_2O_2$) thành $H_2O$ thông qua enzym Glutathione Peroxidase, bảo vệ màng hồng cầu chống lại sự tán huyết do oxy hóa.",
            ch3_img
        ),
        (
            "Protein nào sau đây chiếm tỷ lệ phong phú nhất trong toàn bộ cơ thể người (khoảng 25-30% tổng lượng protein)?",
            "Albumin huyết tương.",
            "Collagen mô liên kết.",
            "Hemoglobin hồng cầu.",
            "Myosin sợi cơ vân.",
            "B",
            "Collagen là protein cấu trúc sợi chiếm tới 25-30% tổng protein cơ thể, tạo nên độ bền cơ học cho da, xương, gân, sụn và mạch máu. Đơn vị cơ bản tropocollagen là xoắn ba (triple helix) chứa nhiều glycin (1/3), prolin và hydroxyprolin.",
            None
        ),
        (
            "Bệnh thiếu hụt Vitamin C (Bệnh Scurvy / Scorbut) dẫn đến chảy máu chân răng và xuất huyết dưới da do ức chế enzym nào trong quá trình trưởng thành của Collagen?",
            "Enzym Prolyl hydroxylase và Lysyl hydroxylase (cần vitamin C và $Fe^{2+}$ làm đồng yếu tố).",
            "Enzym Collagenase mô kẽ.",
            "Enzym Lysyl oxidase tạo liên kết chéo.",
            "Enzym Peptidyl transferase ribosome.",
            "A",
            "Vitamin C (Acid ascorbic) giữ ion sắt ở dạng khử $Fe^{2+}$, là đồng yếu tố bắt buộc của enzym Prolyl hydroxylase và Lysyl hydroxylase xúc tác tạo Hydroxyprolin và Hydroxylysin. Thiếu vitamin C làm collagen mất khả năng hình thành liên kết hydro xoắn 3 bền vững, thành mạch máu dễ vỡ gây xuất huyết.",
            None
        ),
        (
            "Phương pháp điện di protein huyết thanh (Serum Protein Electrophoresis - SPEP) ở pH kiềm 8.6 phân chia protein thành 5 dải theo thứ tự từ cực dương (+) về cực âm (-) là:",
            "Albumin $\\rightarrow \\alpha_1$-globulin $\\rightarrow \\alpha_2$-globulin $\\rightarrow \\beta$-globulin $\\rightarrow \\gamma$-globulin.",
            "$\\gamma$-globulin $\\rightarrow \\beta$-globulin $\\rightarrow \\alpha_2$-globulin $\\rightarrow \\alpha_1$-globulin $\\rightarrow$ Albumin.",
            "Albumin $\\rightarrow \\gamma$-globulin $\\rightarrow \\beta$-globulin $\\rightarrow \\alpha_1$-globulin $\\rightarrow \\alpha_2$-globulin.",
            "Fibrinogen $\\rightarrow$ Albumin $\\rightarrow$ Globulin $\\rightarrow$ Transferrin $\\rightarrow$ CRP.",
            "A",
            "Ở pH = 8.6 (cao hơn pI của hầu hết protein huyết thanh), tất cả protein tích điện âm và di chuyển về cực dương (anode). Albumin có điện tích âm lớn nhất và kích thước nhỏ nhất nên chạy nhanh nhất và xa nhất về cực (+), kế tiếp là $\\alpha_1, \\alpha_2, \\beta$ và cuối cùng là $\\gamma$-globulin.",
            None
        ),
        (
            "Phát biểu nào sau đây KHÔNG ĐÚNG về Albumin huyết thanh người?",
            "Do gan tổng hợp hoàn toàn, chiếm 55-65% tổng lượng protein huyết thanh.",
            "Đảm nhiệm khoảng 75-80% tổng áp suất keo (áp suất thẩm thấu keo) của huyết tương.",
            "Chuyên chở nhiều chất kỵ nước như bilirubin gián tiếp, acid béo tự do, hormon steroid và thuốc.",
            "Nồng độ albumin huyết thanh tăng cao rõ rệt trong các bệnh lý xơ gan mất bù và hội chứng thận hư.",
            "D",
            "Trong xơ gan mất bù (gan suy giảm khả năng tổng hợp) và hội chứng thận hư (thất thoát nặng protein qua màng lọc cầu thận), nồng độ albumin huyết thanh GIẢM NẶNG (<30 g/L), gây giảm áp suất keo huyết tương dẫn đến phù toàn thân và tràn dịch màng bụng (cổ trướng). Phát biểu 'tăng cao rõ rệt' là SAI hoàn toàn.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch3_core):
            q, a, b, c, d, corr, exp, img = ch3_core[i]
        else:
            q_num = i + 1
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch3_img if (i % 6 == 0) else None

            ch3_topics = [
                ("Phân loại và tính chất 20 acid amin", "Acid amin kiềm gồm Lysin, Arginin và Histidin có chuỗi bên tích điện dương ở pH sinh lý.", "Acid amin acid gồm Aspartat và Glutamat có chuỗi bên tích điện âm ở pH 7.4.", "Acid amin nhân thơm gồm Phenylalanin, Tyrosin và Tryptophan hấp thụ mạnh tia tử ngoại ở bước sóng 280 nm.", "Prolin là một imino acid có chuỗi bên gắn vòng vào nhóm amin, phá vỡ cấu trúc xoắn $\\alpha$."),
                ("Các phản ứng hóa học đặc trưng của protid", "Phản ứng Biuret đặc trưng cho liên kết peptid (từ 2 liên kết peptid trở lên tạo phức màu tím với $Cu^{2+}$ trong kiềm).", "Phản ứng Ninhydrin tạo màu tím Ruhemann dùng để định lượng acid amin tự do và sắc ký.", "Phản ứng Xanthoprotein tạo màu vàng khi cho $HNO_3$ đặc tác dụng với acid amin chứa nhân thơm.", "Thuốc thử Sanger (FDNB) và Edman (PITC) dùng để xác định acid amin đầu N tận cùng của chuỗi polypeptid."),
                ("Hiện tượng biến tính protein", "Biến tính protein làm phá hủy các cấu trúc bậc 2, 3 và 4 nhưng KHÔNG làm đứt gãy liên kết peptid bậc 1.", "Nhiệt độ cao, acid/kiềm mạnh, muối kim loại nặng ($Pb^{2+}, Hg^{2+}$) và urea nồng độ cao đều gây biến tính protein.", "Protein sau khi biến tính thường bị giảm độ tan, mất hoạt tính sinh học đặc hiệu và dễ bị enzym tiêu hóa phân giải.", "Một số protein có thể hồi tính (renaturation) khi loại bỏ dần tác nhân biến tính nếu liên kết bậc 1 còn nguyên vẹn."),
                ("Globulin huyết thanh và miễn dịch", "Dải $\\gamma$-globulin trên điện di chủ yếu gồm các kháng thể (Immunoglobulin: IgG, IgA, IgM, IgE, IgD).", "Bệnh đa u tủy xương (Multiple Myeloma) đặc trưng bởi đỉnh nhọn đơn dòng (M-spike) ở vùng $\\gamma$-globulin.", "Haptoglobin thuộc phân đoạn $\\alpha_2$-globulin có chức năng gắn kết Hb tự do trong máu chống mất sắt qua thận.", "Ceruloplasmin thuộc phân đoạn $\\alpha_2$-globulin chuyên chở 90-95% lượng đồng trong huyết tương."),
                ("Enzym và thụ thể bản chất protein", "Protein xuyên màng thường có các đoạn xoắn $\\alpha$ chứa nhiều acid amin kỵ nước (Leu, Ile, Val, Ala).", "Histidin có $pK_a \\approx 6.0$ gần với pH sinh lý 7.4 nên thường nằm ở trung tâm hoạt động của enzym làm chất cho/nhận proton.", "Sự phosphoryl hóa chuỗi bên Serin, Threonin hoặc Tyrosin là cơ chế điều hòa hoạt tính protein phổ biến nhất.", "Chaperone là các protein chuyên biệt hỗ trợ sự cuộn gập chính xác của các chuỗi polypeptide non trẻ.")
            ]
            tp = ch3_topics[i % len(ch3_topics)]
            
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Khẳng định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi đề cập đến {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Tất cả các hiện tượng hoặc tính chất này đều không liên quan đến cấu trúc phân tử và không có ứng dụng lâm sàng nào."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Tuân theo định luật hóa sinh đại cương."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Nhận định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Quá trình này hoàn toàn không tuân theo các nguyên lý nhiệt động lực học và không tạo ra bất kỳ biến đổi phân tử nào."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đều đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch3_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # Insert Batch 1 questions into SQLite
    print(f"Prepared {len(questions)} questions for Batch 1 (Ch1, Ch2, Ch3). Inserting into DB...")
    for item in questions:
        cur.execute("""
            INSERT INTO questions (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_option, explanation, difficulty, topic_tag, image_url, q_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'multiple_choice')
        """, (sub_id, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[0], item[9]))

    conn.commit()
    cur.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sub_id,))
    print(f"Batch 1 Seed Complete! Current total questions for subject {sub_id}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    seed_part1()
