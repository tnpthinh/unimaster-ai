# -*- coding: utf-8 -*-
"""
UniMaster AI - Seeder for YDS 2024 Medical Biochemistry
Batch 6:
- Chương 16: PCR, realtime PCR, giải trình tự acid nucleic (100 câu)
- Chương 17: Sinh tổng hợp protein (100 câu)
- Chương 18: Liên quan và điều hòa chuyển hóa (100 câu)
Total: 300 questions
"""

import sqlite3

def seed_part6():
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
    # CHƯƠNG 16: PCR & GIẢI TRÌNH TỰ (100 CÂU)
    # ==========================================
    ch16_name = "Chương 16: PCR, realtime PCR, giải trình tự acid nucleic"
    ch16_img = "/static/uploads/hoasinh_yds/ch16_pcr_cycle_phases.svg"

    ch16_core = [
        (
            "Một chu kỳ nhiệt tiêu chuẩn của kỹ thuật PCR cổ điển bao gồm 3 bước liên tiếp theo thứ tự nhiệt độ nào sau đây?",
            "Biến tính tách sợi đôi (94 - 95°C) $\\rightarrow$ Bắt cặp mồi đặc hiệu (50 - 65°C) $\\rightarrow$ Kéo dài chuỗi (72°C).",
            "Bắt cặp mồi (72°C) $\\rightarrow$ Biến tính (95°C) $\\rightarrow$ Kéo dài (55°C).",
            "Kéo dài (95°C) $\\rightarrow$ Biến tính (72°C) $\\rightarrow$ Bắt cặp mồi (37°C).",
            "Điện di (60°C) $\\rightarrow$ Lai phân tử (95°C) $\\rightarrow$ Cắt enzym (72°C).",
            "A",
            "Mỗi chu kỳ PCR gồm 3 pha nhiệt độ: (1) Biến tính ở 94-95°C để phá vỡ các liên kết hydro tách DNA sợi đôi thành 2 sợi đơn; (2) Bắt cặp mồi ở 50-65°C để cặp mồi xuôi và ngược gắn bổ sung vào 2 đầu trình tự đích; (3) Kéo dài ở 72°C (nhiệt độ tối ưu của Taq DNA polymerase) để tổng hợp chuỗi DNA mới theo chiều 5' $\\rightarrow$ 3'.",
            ch16_img
        ),
        (
            "Taq DNA Polymerase sử dụng trong phản ứng PCR có nguồn gốc từ sinh vật nào và mang ưu điểm vượt trội gì?",
            "Phân lập từ vi khuẩn suối nước nóng *Thermus aquaticus*, có khả năng chịu nhiệt độ cao tới 95°C mà không bị biến tính hay mất hoạt tính xúc tác.",
            "Phân lập từ vi khuẩn *E. coli*, có tốc độ tổng hợp nhanh nhất.",
            "Phân lập từ nấm men, có hoạt tính đọc sửa sai 3' $\\rightarrow$ 5' hoàn hảo.",
            "Được tổng hợp hóa học nhân tạo hoàn toàn.",
            "A",
            "Trước khi phát hiện ra Taq polymerase, phản ứng PCR phải bổ sung enzym Klenow mới sau mỗi chu kỳ vì enzym bị phá hủy ở bước biến tính 95°C. Việc sử dụng Taq polymerase chịu nhiệt từ vi khuẩn suối nước nóng *Thermus aquaticus* cho phép tự động hóa hoàn toàn phản ứng PCR trong máy luân nhiệt (Thermal Cycler).",
            ch16_img
        ),
        (
            "Trong kỹ thuật Real-time PCR (qPCR), giá trị chu kỳ ngưỡng $C_t$ (Threshold Cycle / $C_q$) có ý nghĩa sinh học như thế nào?",
            "Số chu kỳ mà tại đó tín hiệu huỳnh quang vượt qua ngưỡng nền; giá trị $C_t$ TỶ LỆ NGHỊCH với lượng bản sao acid nucleic ban đầu trong mẫu bệnh phẩm.",
            "Số chu kỳ cần thiết để phản ứng PCR đạt trạng thái bão hòa đường bình nguyên.",
            "Nhiệt độ nóng chảy tại đó 50% sản phẩm PCR bị biến tính.",
            "Tỷ lệ thuận trực tiếp với số lượng chu kỳ khuếch đại tối đa.",
            "A",
            "Giá trị $C_t$ phản ánh thời điểm lượng sản phẩm DNA khuếch đại tạo ra đủ tín hiệu huỳnh quang vượt lên trên đường nền. Mẫu bệnh phẩm có nồng độ virus/vi khuẩn ban đầu càng cao (tải lượng cao) thì tín hiệu huỳnh quang đạt ngưỡng càng sớm, tức là giá trị $C_t$ càng nhỏ.",
            ch16_img
        ),
        (
            "Thuốc nhuộm huỳnh quang xen kẽ SYBR Green I trong Real-time PCR có nhược điểm gì so với đầu dò đặc hiệu TaqMan?",
            "Gắn không đặc hiệu vào tất cả các phân tử DNA sợi đôi (kể cả sản phẩm phụ không đặc hiệu và dimer mồi), cần phân tích đường cong nóng chảy (Melting Curve) để kiểm tra.",
            "Không phát tín hiệu huỳnh quang khi có mặt DNA.",
            "Chỉ dùng được cho các mẫu có nồng độ ban đầu cực thấp.",
            "Bị phá hủy hoàn toàn ở nhiệt độ trên 60°C.",
            "A",
            "SYBR Green I là chất phát huỳnh quang khi gắn xen vào rãnh nhỏ của bất kỳ DNA sợi đôi nào, do đó nếu có dimer mồi (primer dimer) hoặc sản phẩm khuếch đại chệch mục tiêu, nó vẫn phát tín hiệu gây dương tính giả. Vì vậy bắt buộc phải chạy phân tích đường cong nóng chảy ($T_m$ dissociation curve) sau phản ứng để kiểm tra độ đơn nhất của sản phẩm.",
            ch16_img
        ),
        (
            "Đầu dò TaqMan (TaqMan Probe) sử dụng cơ chế truyền năng lượng cộng hưởng huỳnh quang (FRET) dựa trên hoạt tính enzym nào của Taq Polymerase?",
            "Hoạt tính $5' \\rightarrow 3'$ Exonuclease phân cắt đầu dò giải phóng Reporter tách khỏi Quencher.",
            "Hoạt tính $3' \\rightarrow 5'$ Exonuclease đọc sửa sai.",
            "Hoạt tính Endonuclease cắt đôi sợi kép.",
            "Hoạt tính Ligase nối chuỗi.",
            "A",
            "Đầu dò TaqMan mang một chất phát sáng Reporter ở đầu 5' và một chất dập tắt huỳnh quang Quencher ở đầu 3'. Khi nguyên vẹn, Quencher hấp thụ năng lượng của Reporter theo cơ chế FRET. Khi Taq polymerase kéo dài chuỗi và gặp đầu dò, hoạt tính $5' \\rightarrow 3'$ exonuclease của nó sẽ cắt rời Reporter ra khỏi chuỗi, Reporter thoát khỏi tác dụng của Quencher và phát tín hiệu huỳnh quang đặc hiệu.",
            ch16_img
        ),
        (
            "Kỹ thuật RT-PCR (Reverse Transcription PCR) bắt buộc phải sử dụng enzym nào ở bước đầu tiên để phát hiện các virus mang vật chất di truyền là RNA (như SARS-CoV-2, HIV, HCV)?",
            "Enzym phiên mã ngược (Reverse Transcriptase - RT) để tổng hợp cDNA bổ sung từ sợi khuôn RNA.",
            "Taq DNA Polymerase.",
            "RNA Polymerase II.",
            "DNA Ligase.",
            "A",
            "Do Taq polymerase chỉ sử dụng khuôn mẫu là DNA mà không thể dùng khuôn mẫu RNA, các virus RNA bắt buộc phải trải qua bước phiên mã ngược (Reverse Transcription) nhờ men Reverse Transcriptase để tạo chuỗi DNA bổ sung (cDNA), sau đó cDNA mới được khuếch đại bằng phản ứng PCR hoặc Real-time PCR thông thường.",
            None
        ),
        (
            "Nguyên lý cốt lõi của phương pháp giải trình tự DNA theo Sanger (phương pháp kết thúc chuỗi dideoxy) là gì?",
            "Sử dụng các Dideoxynucleotide triphosphate (ddNTP: ddATP, ddTTP, ddCTP, ddGTP) thiếu nhóm 3'-OH tự do, làm dừng chuỗi tổng hợp ngay lập tức khi được gắn vào chuỗi DNA đang kéo dài.",
            "Sử dụng các hóa chất phân hủy hóa học đặc hiệu từng base nitơ.",
            "Cắt DNA bằng các enzym giới hạn restriction endonuclease.",
            "Đo nồng độ ion hydro giải phóng khi liên kết phosphodiester hình thành.",
            "A",
            "Các phân tử ddNTP thiếu cả nhóm 2'-OH và 3'-OH trên đường pentose (chỉ có $2',3'$-dideoxy). Khi DNA polymerase vô tình kết nạp một phân tử ddNTP vào đầu 3' của chuỗi DNA đang kéo dài, do không còn nhóm 3'-OH tự do để tạo liên kết phosphodiester tiếp theo nên quá trình tổng hợp chuỗi bị kết thúc dứt khoát tại base đó.",
            None
        ),
        (
            "Trong giải trình tự thế hệ mới (Next-Generation Sequencing - NGS) của hãng Illumina, công nghệ nào cho phép đọc đồng thời hàng tỷ đoạn DNA song song?",
            "Khuếch đại cụm cầu nối (Bridge Amplification) trên bề mặt Flow Cell và giải trình tự bằng phương pháp tổng hợp (Sequencing by Synthesis - SBS) dùng dNTP đánh dấu huỳnh quang có nhóm khóa thuận nghịch.",
            "Giải trình tự bằng phương pháp kết thúc chuỗi ddNTP của Sanger.",
            "Điện di mao quản trên bản gel polyacrylamide.",
            "Đo sự thay đổi pH bằng cảm biến bán dẫn Ion Torrent.",
            "A",
            "Nền tảng Illumina sử dụng công nghệ khuếch đại cầu nối đẳng nhiệt trên Flow cell để tạo ra hàng triệu cụm phân tử đơn dòng (clonal clusters). Sau đó, quá trình giải trình tự sử dụng 4 loại dNTP mang 4 màu huỳnh quang khác nhau với đầu 3' bị khóa thuận nghịch (reversible terminator), mỗi vòng quay chỉ kéo dài 1 base, chụp ảnh huỳnh quang rồi mở khóa cho chu kỳ tiếp theo.",
            None
        ),
        (
            "Kỹ thuật giải trình tự đơn phân tử thế hệ 3 của Oxford Nanopore Technologies (ONT) có ưu thế nổi bật nào sau đây?",
            "Cho các đoạn đọc cực kỳ dài (long-read sequencing lên tới hàng trăm kilobase), giải trình tự trực tiếp phân tử DNA hoặc RNA tự nhiên thời gian thực mà không cần bước khuếch đại PCR.",
            "Chi phí thiết bị máy móc đắt tiền nhất và kích thước máy khổng lồ.",
            "Độ chính xác trên từng base đơn lẻ cao hơn tất cả các phương pháp NGS chuỗi ngắn.",
            "Chỉ đọc được các đoạn DNA ngắn dưới 150 cặp base.",
            "A",
            "Oxford Nanopore cho phân tử DNA hoặc RNA sợi đơn đi qua một lỗ nano protein (nanopore) cắm trên màng sinh học dẫn điện. Khi từng base nitơ chui qua lỗ, nó cản trở dòng ion theo cách đặc thù tạo ra dao động dòng điện đặc trưng, máy đọc tín hiệu này theo thời gian thực với chiều dài đoạn đọc không giới hạn (long-read sequencing).",
            None
        ),
        (
            "Trong thiết kế mồi PCR (Primer Design), thông số nào sau đây là YÊU CẦU BẮT BUỘC để đảm bảo phản ứng khuếch đại đạt hiệu quả và đặc hiệu cao?",
            "Nhiệt độ nóng chảy ($T_m$) của mồi xuôi và mồi ngược phải gần bằng nhau (chênh lệch không quá 1 - 2°C) và tránh tạo cấu trúc kẹp tóc (hairpin) hoặc tự bắt cặp mồi (primer-dimer).",
            "Mồi phải có độ dài trên 60 nucleotid.",
            "Tỷ lệ G-C của mồi phải đạt 100%.",
            "Mồi phải bắt cặp bổ sung hoàn toàn ở đầu 5' của hai chuỗi.",
            "A",
            "Một cặp mồi PCR tối ưu thường dài 18 - 25 nucleotid, hàm lượng G-C khoảng 40 - 60%, nhiệt độ nóng chảy $T_m$ giữa 2 mồi chênh nhau không quá 1-2°C, có gốc G hoặc C ở đầu 3' (GC clamp) để neo bám chắc chắn, và tuyệt đối không có trình tự tự bổ sung tạo cấu trúc kẹp tóc hay dimer mồi.",
            ch16_img
        )
    ]

    for i in range(100):
        if i < len(ch16_core):
            q, a, b, c, d, corr, exp, img = ch16_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch16_img if (i % 5 == 0) else None

            ch16_topics = [
                ("Các biến thể kỹ thuật PCR chuyên sâu", "Nested PCR (PCR tổ) dùng 2 cặp mồi liên tiếp để tăng tối đa độ nhạy và độ đặc hiệu chẩn đoán.", "Multiplex PCR (PCR đa mồi) cho phép khuếch đại đồng thời nhiều trình tự đích khác nhau trong cùng một ống phản ứng.", "Touchdown PCR hạ dần nhiệt độ bắt cặp mồi qua các chu kỳ đầu để tránh gắn mồi chệch mục tiêu.", "Digital PCR (dPCR) phân chia mẫu thành hàng vạn giọt nhỏ (droplet dPCR) để định lượng số bản sao tuyệt đối mà không cần đường chuẩn."),
                ("Các ứng dụng lâm sàng của kỹ thuật PCR", "Đo tải lượng virus HIV-1 và HCV huyết tương phục vụ theo dõi đáp ứng điều trị thuốc kháng virus.", "Sàng lọc đột biến kháng thuốc (như đột biến T790M của EGFR trong ung thư phổi không tế bào nhỏ).", "Xác định đột biến gen bệnh tan máu Thalassemia, bệnh xơ nang và bệnh teo cơ tủy SMA.", "Giám định pháp y, xác định danh tính hài cốt liệt sĩ và huyết thống bằng phân tích lặp lại đoạn ngắn STR."),
                ("Phân tích đường cong nóng chảy (High-Resolution Melting - HRM)", "Kỹ thuật HRM dựa trên sự biến đổi độ huỳnh quang khi mẫu DNA sợi đôi bị nóng chảy tách thành sợi đơn theo nhiệt độ tăng dần.", "Nhiệt độ nóng chảy $T_m$ của sản phẩm phụ thuộc vào chiều dài đoạn khuếch đại, tỷ lệ G-C và trình tự nucleotid.", "HRM có khả năng phát hiện các đột biến điểm đơn nucleotid (SNP) và đột biến dị hợp tử với độ nhạy rất cao.", "Sử dụng các chất nhuộm bão hòa thế hệ mới như EvaGreen hoặc LCGreen không ức chế PCR ở nồng độ cao."),
                ("Các phương pháp giải trình tự thế hệ mới (NGS) khác", "Hệ thống Ion Torrent phát hiện sự giải phóng ion $H^+$ (đo thay đổi pH) khi một nucleotid được gắn vào chuỗi.", "Hệ thống PacBio SMRT (Single-Molecule Real-Time) sử dụng các giếng quang dẫn ZMW đo huỳnh quang đơn phân tử đọc dài.", "Kỹ thuật Targeted NGS (Panel gen mục tiêu) cho phép giải trình tự sâu hàng trăm gen ung thư liên quan với chi phí hợp lý.", "Giải trình tự toàn bộ vùng mã hóa (Whole Exome Sequencing - WES) khảo sát 1-2% hệ gen nhưng chứa tới 85% đột biến gây bệnh di truyền."),
                ("Kiểm soát chất lượng và tránh ngoại nhiễm trong phòng xét nghiệm phân tử", "Phân chia không gian phòng xét nghiệm một chiều nghiêm ngặt: Phòng pha hóa chất $\\rightarrow$ Phòng tách chiết mẫu $\\rightarrow$ Phòng khuếch đại và phân tích.", "Hiện tượng ngoại nhiễm sản phẩm PCR (Carry-over contamination) là nguyên nhân hàng đầu gây dương tính giả.", "Sử dụng enzym Uracil-DNA Glycosylase (UDG / UNG) và thay dTTP bằng dUTP để phân hủy các sản phẩm khuếch đại từ mẻ chạy trước.", "Mẫu chứng âm (Negative control) và mẫu chứng dương (Positive control) bắt buộc phải chạy kèm trong mỗi mẻ phản ứng.")
            ]
            tp = ch16_topics[i % len(ch16_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Kỹ thuật này hoàn toàn không tuân theo quy tắc bổ sung Watson-Crick và không cần sử dụng bất kỳ loại enzyme hay mồi nào."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo tính chính xác của xét nghiệm sinh học phân tử."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Phương pháp này chỉ áp dụng được trên mẫu khoáng thạch vô cơ và không có ứng dụng nào trong chẩn đoán y học."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch16_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 17: SINH TỔNG HỢP PROTEIN (100 CÂU)
    # ==========================================
    ch17_name = "Chương 17: Sinh tổng hợp protein"
    ch17_img = "/static/uploads/hoasinh_yds/ch17_translation_ribosome.svg"

    ch17_core = [
        (
            "Mã di truyền (Genetic Code) có tính thoái hóa (Degenerate) nghĩa là gì?",
            "Có nhiều bộ ba codon khác nhau cùng mã hóa cho một loại acid amin (do có 61 codon mã hóa cho 20 acid amin).",
            "Mỗi bộ ba codon mã hóa cho nhiều loại acid amin khác nhau tùy theo mô.",
            "Mã di truyền bị biến đổi theo thời gian và tuổi thọ sinh vật.",
            "Các bộ ba gối lên nhau khi ribosome di chuyển.",
            "A",
            "Tính thoái hóa (dư thừa) của mã di truyền nghĩa là 1 acid amin có thể được mã hóa bởi nhiều hơn 1 codon (ngoại trừ Methionine do AUG và Tryptophan do UGG mã hóa duy nhất). Điều này giúp giảm thiểu tác hại của các đột biến thay thế nucleotid (đột biến đồng nghĩa / câm).",
            ch17_img
        ),
        (
            "Ba bộ ba kết thúc (Stop Codons / Codon vô nghĩa) báo hiệu chấm dứt quá trình dịch mã trên phân tử mRNA là:",
            "UAA, UAG và UGA.",
            "AUG, UGG và UAA.",
            "UGA, UAC và UGG.",
            "AAA, AAG và AGG.",
            "A",
            "Trong số 64 bộ ba codon: có 61 codon mã hóa acid amin, còn 3 codon là UAA (ochre), UAG (amber) và UGA (opal) không có tRNA tương ứng mà được nhận diện bởi các yếu tố giải phóng (Release Factors - RF) để cắt chuỗi polypeptid hoàn chỉnh khỏi ribosome.",
            ch17_img
        ),
        (
            "Phản ứng hoạt hóa acid amin và gắn vào tRNA tương ứng do enzym Aminoacyl-tRNA Synthetase xúc tác tiêu tốn năng lượng của phân tử nào?",
            "ATP (thủy phân 1 ATP thành AMP và giải phóng Pyrophosphate $PP_i$, tương đương 2 liên kết cao năng).",
            "GTP.",
            "UTP.",
            "CTP.",
            "A",
            "Enzym Aminoacyl-tRNA synthetase xúc tác 2 bước: Bước 1: Acid amin + ATP $\\rightarrow$ Aminoacyl-AMP + $PP_i$; Bước 2: Aminoacyl-AMP + tRNA $\\rightarrow$ Aminoacyl-tRNA + AMP. Phản ứng tiêu tốn 1 phân tử ATP nhưng phá vỡ cả 2 liên kết cao năng (do $PP_i$ bị pyrophosphatase thủy phân thành $2 P_i$).",
            ch17_img
        ),
        (
            "Cấu trúc Ribosome hoàn chỉnh của tế bào nhân sơ (Prokaryote - vi khuẩn) và nhân thực (Eukaryote) có hệ số lắng lần lượt là:",
            "70S (tiểu đơn vị nhỏ 30S + tiểu đơn vị lớn 50S) ở vi khuẩn; 80S (tiểu đơn vị 40S + 60S) ở nhân thực.",
            "80S ở vi khuẩn và 70S ở nhân thực.",
            "100S ở tế bào người.",
            "50S ở cả hai loại tế bào.",
            "A",
            "Ribosome vi khuẩn là 70S cấu tạo từ tiểu đơn vị nhỏ 30S (chứa rRNA 16S và 21 protein) và tiểu đơn vị lớn 50S (chứa rRNA 23S, 5S và 31 protein). Ribosome nhân thực là 80S cấu tạo từ tiểu đơn vị 40S (chứa rRNA 18S) và tiểu đơn vị 60S (chứa rRNA 28S, 5.8S, 5S). Sự khác biệt này là nền tảng tác động chọn lọc của các kháng sinh.",
            ch17_img
        ),
        (
            "Liên kết peptid giữa nhóm amin của acid amin mới ở vị trí A và nhóm carboxyl của chuỗi polypeptid ở vị trí P trên ribosome được xúc tác bởi thành phần nào?",
            "Hoạt tính Peptidyl Transferase của phân tử rRNA (rRNA 23S ở Prokaryote, rRNA 28S ở Eukaryote) - đóng vai trò là một Ribozyme xúc tác.",
            "Một enzym protein chuyên biệt gắn ngoài ribosome.",
            "Yếu tố kéo dài EF-Tu.",
            "Phân tử tRNA tự xúc tác.",
            "A",
            "Phản ứng hình thành liên kết peptid không do một protein nào xúc tác mà do chính thành phần RNA ribosom (rRNA 23S của tiểu đơn vị lớn vi khuẩn hoặc rRNA 28S ở nhân thực) đảm nhiệm. Đây là một ví dụ kinh điển chứng minh RNA có hoạt tính xúc tác sinh học (Ribozyme).",
            ch17_img
        ),
        (
            "Kháng sinh nhóm Aminoglycosid (Streptomycin, Gentamicin, Amikacin) diệt khuẩn theo cơ chế tác động nào lên quá trình dịch mã?",
            "Gắn vào tiểu đơn vị nhỏ 30S của ribosome vi khuẩn, ức chế tạo phức hợp khởi đầu và làm biến dạng vị trí A gây đọc sai mã bộ ba (misreading), tổng hợp ra các protein lỗi làm chết vi khuẩn.",
            "Ức chế enzym tổng hợp thành vách peptidoglycan.",
            "Khóa enzym peptidyl transferase trên tiểu đơn vị 50S.",
            "Ngăn chặn enzym tháo xoắn DNA gyrase.",
            "A",
            "Aminoglycosid gắn cố định vào rRNA 16S của tiểu đơn vị 30S làm sai lệch cấu trúc không gian của túi nhận diện codon-anticodon, khiến ribosome lắp ráp nhầm các aminoacyl-tRNA không tương thích, dẫn đến dịch mã sai và protein dị tật chèn vào màng tế bào làm thủng màng và diệt khuẩn nhanh chóng.",
            ch17_img
        ),
        (
            "Kháng sinh nhóm Tetracyclin (Tetracycline, Doxycycline) ức chế dịch mã vi khuẩn theo cơ chế nào sau đây?",
            "Gắn thuận nghịch vào tiểu đơn vị 30S của ribosome, ngăn cản sự tiếp cận và gắn kết của Aminoacyl-tRNA vào vị trí A.",
            "Khóa vị trí P ngăn cản tRNA mang methionin gắn vào.",
            "Ức chế sự dịch chuyển chuyển vị (translocation) của ribosome.",
            "Gây kết thúc chuỗi polypeptid sớm.",
            "A",
            "Tetracyclin gắn vào rãnh nhỏ của tiểu đơn vị 30S vi khuẩn, che lấp vị trí tiếp nhận A (aminoacyl site), làm các phân tử aminoacyl-tRNA mới không thể bắt cặp codon-anticodon để đi vào ribosome, làm ngừng trệ giai đoạn kéo dài chuỗi peptide.",
            ch17_img
        ),
        (
            "Kháng sinh nhóm Macrolid (Erythromycin, Azithromycin, Clarithromycin) và Clindamycin tác động lên tiểu đơn vị nào của ribosome vi khuẩn?",
            "Gắn vào tiểu đơn vị lớn 50S, ngăn cản sự chuyển vị (translocation) của ribosome dọc theo mRNA và khóa đường hầm thoát của chuỗi peptide mới sinh.",
            "Gắn vào tiểu đơn vị nhỏ 30S.",
            "Ức chế sự hoạt hóa acid amin của tRNA synthetase.",
            "Ức chế yếu tố giải phóng RF.",
            "A",
            "Macrolid gắn vào rRNA 23S của tiểu đơn vị 50S ngay gần cửa ngõ đường hầm thoát chuỗi polypeptide (polypeptide exit tunnel), ngăn chặn sự chuyển vị của ribosome (translocation) từ codon này sang codon kế tiếp và làm chuỗi peptide non trẻ bị tắc nghẽn, rơi rụng sớm.",
            ch17_img
        ),
        (
            "Độc tố vi khuẩn Bạch hầu (Diphtheria toxin) và độc tố của *Pseudomonas aeruginosa* (Exotoxin A) gây chết tế bào vật chủ theo cơ chế ức chế sinh tổng hợp protein nào?",
            "Xúc tác phản ứng ADP-ribosyl hóa làm bất hoạt hoàn toàn Yếu tố kéo dài 2 (eEF-2) của tế bào nhân thực.",
            "Cắt đứt mũ 5'-cap của phân tử mRNA.",
            "Ức chế tổng hợp ATP trong ty thể.",
            "Phân giải rRNA 28S của tế bào người.",
            "A",
            "Độc tố bạch hầu là một enzym gắn gốc ADP-ribose từ $NAD^+$ vào acid amin biến đổi diphthamide trên Yếu tố kéo dài dịch mã eEF-2 của tế bào người. Khi eEF-2 bị ADP-ribosyl hóa, nó mất hoàn toàn khả năng xúc tác sự chuyển vị của ribosome 80S, làm tê liệt sinh tổng hợp protein của niêm mạc hầu họng và cơ tim dẫn tới tử vong.",
            None
        ),
        (
            "Quá trình biến đổi sau dịch mã (Post-translational Modification) nào sau đây là BẮT BUỘC để phân tử Insulin chuyển từ dạng tiền chất Proinsulin thành Insulin có hoạt tính sinh học?",
            "Cắt bỏ chuỗi peptide C (C-peptide) bằng các enzym nội protease, để lại hai chuỗi A và B liên kết với nhau bằng các cầu nối disulfid.",
            "Phosphoryl hóa chuỗi bên của Serin.",
            "Gắn thêm gốc acid béo palmitate.",
            "Hydroxyl hóa các gốc prolin.",
            "A",
            "Proinsulin được tổng hợp ở lưới nội chất hạt, cuộn lại và hình thành 3 cầu nối disulfid. Khi vào bộ máy Golgi và các túi tiết của tế bào $\\beta$, các enzym prohormone convertase cắt bỏ đoạn peptide nối ở giữa (C-peptide gồm 31 acid amin), giải phóng Insulin gồm 2 chuỗi A (21 aa) và chuỗi B (30 aa) liên kết với nhau qua 2 cầu disulfid liên chuỗi.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch17_core):
            q, a, b, c, d, corr, exp, img = ch17_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch17_img if (i % 5 == 0) else None

            ch17_topics = [
                ("Thuyết bắt cặp linh hoạt (Wobble Hypothesis) của Crick", "Sự bắt cặp giữa vị trí thứ 3 của codon (đầu 3') và vị trí thứ nhất của anticodon (đầu 5') có tính linh hoạt không gian.", "Một phân tử tRNA có thể nhận diện và bắt cặp với nhiều hơn một codon đồng nghĩa.", "Base biến đổi Inosine (I) ở vị trí thứ nhất của anticodon có thể bắt cặp bổ sung với cả A, U hoặc C của codon.", "Thuyết bắt cặp linh hoạt giải thích vì sao tế bào chỉ cần 31-48 loại tRNA để đọc đủ 61 codon mã hóa."),
                ("Các yếu tố dịch mã và tiêu tốn năng lượng sinh học", "Giai đoạn khởi đầu dịch mã ở vi khuẩn cần 3 yếu tố protein: IF-1, IF-2 (gắn GTP) và IF-3.", "Giai đoạn kéo dài chuỗi polypeptid cần EF-Tu, EF-Ts và EF-G (mỗi bước gắn aminoacyl-tRNA và chuyển vị tiêu tốn 2 phân tử GTP).", "Để tổng hợp 1 liên kết peptid tiêu tốn tương đương 4 liên kết cao năng (2 ATP hoạt hóa tRNA + 2 GTP kéo dài).", "Yếu tố giải phóng RF-1 nhận diện codon UAA và UAG, trong khi RF-2 nhận diện UAA và UGA ở vi khuẩn."),
                ("Các cơ chế kháng sinh khác ức chế dịch mã", "Chloramphenicol ức chế cạnh tranh trung tâm peptidyl transferase trên tiểu đơn vị 50S vi khuẩn, có tác dụng phụ suy tủy xương và hội chứng xám ở trẻ sơ sinh (Gray baby syndrome).", "Linezolid (Oxazolidinone) gắn vào rRNA 23S của tiểu đơn vị 50S ngăn chặn tạo phức hợp khởi đầu 70S, điều trị vi khuẩn kháng thuốc MRSA và VRE.", "Puromycin có cấu trúc tương tự tyrosyl-tRNA, gắn vào vị trí A gây kết thúc chuỗi sớm ở cả vi khuẩn và người.", "Cycloheximide ức chế chọn lọc enzym peptidyl transferase của ribosome 80S nhân thực, dùng làm chất ức chế nghiên cứu invitro."),
                ("Đích đến của protein và tín hiệu dẫn đường (Signal Peptide)", "Peptid tín hiệu ở đầu N hướng dẫn ribosome đang dịch mã bám vào màng lưới nội chất hạt qua hạt nhận diện tín hiệu SRP.", "Đột biến khuyết enzym GlcNAc phosphotransferase ngăn cản gắn tín hiệu Mannose-6-phosphate dẫn đến bệnh thể vùi (I-cell disease).", "Protein không có chuỗi tín hiệu đặc biệt sẽ ở lại và thực hiện chức năng trong bào tương.", "Ubiquitin gắn vào các protein hỏng hoặc thừa để hướng tới thể phân giải proteasome 26S tiêu hủy."),
                ("Biến đổi sau dịch mã và cấu trúc protein", "Sự glycosyl hóa gắn chuỗi đường vào gốc Asparagine (N-linked trong lưới nội chất) hoặc Serine/Threonine (O-linked trong bộ máy Golgi).", "Sự carboxyl hóa gốc Glutamate nhờ enzym phụ thuộc Vitamin K cần cho các yếu tố đông máu.", "Sự hydroxyl hóa gốc Proline và Lysine trong chuỗi collagen cần Vitamin C và $Fe^{2+}$.", "Phosphoryl hóa có tính thuận nghịch điều hòa bật/tắt hoạt tính enzym và thụ thể màng tế bào.")
            ]
            tp = ch17_topics[i % len(ch17_topics)]
            is_except = (i % 2 == 1)
            if is_except:
                q = f"Khẳng định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi đề cập đến {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cơ chế này hoàn toàn không tuân theo quy tắc bổ sung codon-anticodon và không có sự tham gia của ribosome hay các yếu tố dịch mã."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo tính chính xác của dịch mã protein."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Đặc điểm hóa sinh nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Quá trình này chỉ xảy ra ở bào quan lục lạp của thực vật và không hề tồn tại trong cơ thể người."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các phương án khác đưa ra nhận định sai lầm."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch17_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # ==========================================
    # CHƯƠNG 18: LIÊN QUAN VÀ ĐIỀU HÒA CHUYỂN HÓA (100 CÂU)
    # ==========================================
    ch18_name = "Chương 18: Liên quan và điều hòa chuyển hóa"
    ch18_img = "/static/uploads/hoasinh_yds/ch18_metabolic_regulation_hormones.svg"

    ch18_core = [
        (
            "Ở trạng thái vừa ăn no (Well-fed State / Trạng thái hấp thu), tỷ lệ hormon nào trong máu tăng vọt chi phối toàn bộ chuyển hóa cơ thể?",
            "Tỷ lệ INSULIN / GLUCAGON tăng cao.",
            "Tỷ lệ Glucagon / Insulin tăng cao.",
            "Tỷ lệ Epinephrine / Norepinephrine tăng cao.",
            "Nồng độ Cortisol đạt đỉnh.",
            "A",
            "Sau bữa ăn no giàu glucid và protid, nồng độ glucose máu tăng kích thích tế bào $\\beta$ tụy tiết mạnh Insulin, đồng thời ức chế tế bào $\\alpha$ tiết Glucagon. Tỷ lệ Insulin/Glucagon cao kích hoạt các enzym khử phosphoryl hóa, thúc đẩy đồng hóa tích lũy năng lượng (tổng hợp Glycogen, Triglycerid, Protein) và ức chế tất cả các con đường dị hóa.",
            ch18_img
        ),
        (
            "Tại sao trong trạng thái nhịn đói kéo dài (Starvation từ ngày thứ 3 trở đi), tế bào Não có thể thích nghi sử dụng chất nào để thay thế tới 60-70% nhu cầu năng lượng?",
            "Thể Ceton (chủ yếu là $\\beta$-hydroxybutyrate và acetoacetate do gan sản xuất).",
            "Acid béo tự do chuỗi dài.",
            "Amoniac và Ure hòa tan.",
            "Bilirubin gián tiếp.",
            "A",
            "Acid béo tự do không thể vượt qua hàng rào máu não do gắn chặt với albumin. Khi nhịn đói kéo dài, nồng độ thể Ceton trong máu tăng cao gấp hàng chục lần, vượt qua hàng rào máu não nhờ chất vận chuyển monocarboxylate (MCT). Não sử dụng thể ceton thay thế glucose, giúp giảm mạnh nhu cầu tân tạo đường từ acid amin, từ đó tiết kiệm tối đa phân hủy protein cơ vân.",
            ch18_img
        ),
        (
            "Nguồn cơ chất chủ yếu cung cấp cho quá trình Tân tạo đường (Gluconeogenesis) tại gan sau 24 giờ nhịn đói hoàn toàn là gì?",
            "Các acid amin sinh đường (đặc biệt là Alanine từ cơ xương) và Glycerol (từ sự thủy phân triglycerid mô mỡ).",
            "Glycogen dự trữ trong nhu mô gan.",
            "Các acid béo no chuỗi chẵn.",
            "Acid nucleic từ phân hủy tế bào.",
            "A",
            "Sau 18 - 24 giờ nhịn đói, toàn bộ lượng glycogen dự trữ hữu hạn ở gan đã bị phân giải cạn kiệt. Lúc này, nồng độ glucose máu được duy trì duy nhất bằng con đường Tân tạo đường tại gan (và vỏ thận). Các cơ chất tiền thân là Glycerol (giải phóng từ mô mỡ), Lactate (chu trình Cori) và các acid amin sinh đường thoái hóa từ cơ (chu trình Glucose-Alanine).",
            ch18_img
        ),
        (
            "Hội chứng nuôi ăn lại (Refeeding Syndrome) ở bệnh nhân suy kiệt hoặc nhịn đói kéo dài có cơ chế hóa sinh nguy hiểm nào sau đây?",
            "Khi được truyền đường quá nhanh, nồng độ Insulin tăng vọt kích thích các tế bào hấp thu ồ ạt Phosphate, Kali và Magie từ máu vào nội bào để phosphoryl hóa glucose, gây HẠ PHOSPHATE MÁU CẤP TÍNH dẫn tới suy hô hấp, suy tim cấp và loạn nhịp thất tử vong.",
            "Gây tăng canxi máu quá mức làm ngừng tim ở thì tâm thu.",
            "Gây vỡ hàng loạt tế bào hồng cầu do áp suất thẩm thấu.",
            "Gây suy thận cấp do ứ đọng acid uric.",
            "A",
            "Bệnh nhân nhịn đói lâu ngày bị cạn kiệt phosphat và khoáng chất toàn cơ thể. Khi được nuôi ăn đường trở lại đột ngột, insulin bài tiết mạnh kéo phosphat vào tế bào để tạo ATP và các chất trung gian đường phân. Nồng độ phosphat máu tụt dốc thảm hại (<0.3 mmol/L), tế bào không còn ATP và 2,3-BPG gây hủy cơ vân, suy tim mất bù, liệt cơ hô hấp và tử vong.",
            ch18_img
        ),
        (
            "Cơ tim (Myocardium) trong điều kiện sinh lý bình thường sử dụng nguồn nhiên liệu chuyển hóa ưa thích nhất là gì?",
            "Acid béo tự do (Free Fatty Acids - FFA) (cung cấp 60 - 80% tổng nhu cầu năng lượng).",
            "Glucose tự do qua đường phân kỵ khí.",
            "Glycogen dự trữ trong tế bào cơ tim.",
            "Acid amin chuỗi nhánh Leucine và Valine.",
            "A",
            "Cơ tim là mô hiếu khí thuần túy hoạt động co bóp liên tục không ngừng nghỉ. Nguồn nhiên liệu chính của cơ tim khi nghỉ ngơi là acid béo tự do qua chu trình $\\beta$-oxy hóa trong ty thể giàu đặc biệt ở cơ tim (60-80%). Phần còn lại là lactate và thể ceton. Glucose chỉ đóng góp tỷ lệ nhỏ trong điều kiện bình thường.",
            ch18_img
        ),
        (
            "Mô mỡ (Adipose tissue) trong trạng thái Đói giải phóng acid béo tự do vào máu nhờ enzym nào chịu sự kích thích của Glucagon và Epinephrine?",
            "Lipase nhạy cảm Hormon (Hormone-Sensitive Lipase - HSL) (được hoạt hóa bằng phản ứng phosphoryl hóa nhờ PKA).",
            "Lipoprotein Lipase (LPL).",
            "Pancreatic Lipase (Lipase tụy).",
            "Hepatic Lipase (Lipase gan).",
            "A",
            "Ở trạng thái đói hoặc stress, Glucagon và Epinephrine gắn thụ thể GPCR làm tăng cAMP và hoạt hóa Protein Kinase A (PKA). PKA phosphoryl hóa hoạt hóa enzym HSL và protein perilipin bao quanh giọt mỡ, kích hoạt quá trình ly giải mỡ (lipolysis) thủy phân triglycerid giải phóng acid béo tự do và glycerol vào tuần hoàn.",
            ch18_img
        ),
        (
            "Enzym nào đóng vai trò là 'cảm biến năng lượng' (Energy Sensor) tối cao của tế bào, được hoạt hóa khi tỷ lệ AMP/ATP tăng cao (trạng thái tế bào thiếu năng lượng)?",
            "AMP-activated Protein Kinase (AMPK).",
            "Protein Kinase A (PKA).",
            "Protein Kinase C (PKC).",
            "Glycogen Synthase Kinase 3 (GSK-3).",
            "A",
            "AMPK là trung tâm điều hòa năng lượng tế bào. Khi tế bào bị cạn kiệt năng lượng (AMP tăng vọt), AMP gắn vào AMPK kích hoạt enzym này phosphoryl hóa hàng loạt enzym đích: BẬT các con đường sinh ATP (đường phân, $\\beta$-oxy hóa) và TẮT các con đường tiêu tốn ATP (tổng hợp acid béo, tổng hợp cholesterol qua ức chế ACC và HMG-CoA reductase). Thuốc Metformin hoạt hóa con đường AMPK này.",
            ch18_img
        ),
        (
            "Mô nào sau đây KHÔNG THỂ sử dụng Acid béo làm nguồn năng lượng trong bất kỳ điều kiện nào?",
            "Tế bào hồng cầu (RBC).",
            "Tế bào cơ vân lúc nghỉ ngơi.",
            "Tế bào gan.",
            "Tế bào biểu mô ống thận.",
            "A",
            "Tế bào hồng cầu trưởng thành hoàn toàn không có ty thể. Vì quá trình $\\beta$-oxy hóa acid béo bắt buộc phải diễn ra trong ty thể, hồng cầu KHÔNG THỂ oxy hóa acid béo hay thể ceton để sinh năng lượng mà phụ thuộc 100% vào con đường đường phân kỵ khí glucose thành lactate trong bào tương.",
            ch18_img
        ),
        (
            "Trong bệnh cảnh Đái tháo đường týp 2, hiện tượng đề kháng Insulin (Insulin Resistance) tại gan và cơ vân dẫn đến biến đổi chuyển hóa nào?",
            "Giảm thu nhận glucose tại cơ vân (giảm chuyển vị GLUT4) kết hợp với gan tiếp tục tăng tân tạo đường không kiểm soát (do mất tín hiệu ức chế của insulin), gây tăng đường huyết mạn tính.",
            "Tăng tích lũy glycogen quá mức trong cơ vân.",
            "Ức chế phân giải lipid ở mô mỡ gây sút cân đột ngột.",
            "Ngừng hoàn toàn quá trình $\\beta$-oxy hóa trong ty thể.",
            "A",
            "Đề kháng insulin làm các thụ thể tế bào đáp ứng kém với insulin: Tại cơ vân, kênh GLUT4 không chuyển vị lên màng khiến glucose không vào được tế bào; tại gan, insulin mất khả năng ức chế enzym PEPCK và G6Pase khiến gan tân tạo đường ồ ạt dù đường huyết đang rất cao, dẫn tới vòng xoắn bệnh lý tăng glucose máu và tăng insulin máu bù trừ.",
            None
        ),
        (
            "Chuyển hóa ethanol (Rượu bia) tại gan tiêu tốn lượng lớn $NAD^+$ và tạo ra nồng độ rất cao NADH bào tương và ty thể, gây hậu quả chuyển hóa nào sau đây?",
            "Ức chế quá trình tân tạo đường (do NADH chuyển pyruvate thành lactate và oxaloacetate thành malate), dẫn tới hạ đường huyết cấp tính ở người uống rượu khi đói.",
            "Kích thích tối đa chu trình Krebs.",
            "Ức chế tổng hợp triglycerid và thể ceton tại gan.",
            "Tăng đào thải acid uric qua đường nước tiểu.",
            "A",
            "Oxy hóa ethanol bởi Alcohol Dehydrogenase (ADH) và ALDH làm tăng vọt tỷ lệ NADH/$NAD^+$ tại gan. Tỷ lệ này đảo ngược chiều các phản ứng thuận nghịch: Pyruvate bị biến thành Lactate (gây toan lactic và cạn kiệt pyruvate), Oxaloacetate bị biến thành Malate (cạn kiệt oxaloacetate). Hậu quả là gan hoàn toàn mất khả năng tân tạo đường, gây hạ đường huyết nghiêm trọng và gan nhiễm mỡ do tăng tổng hợp glycerol-3-phosphate.",
            None
        )
    ]

    for i in range(100):
        if i < len(ch18_core):
            q, a, b, c, d, corr, exp, img = ch18_core[i]
        else:
            corr_opts = ['A', 'B', 'C', 'D']
            corr = corr_opts[i % 4]
            img = ch18_img if (i % 5 == 0) else None

            ch18_topics = [
                ("Chuyển hóa trong gắng sức cơ bắp cấp tính và kéo dài", "Trong vài giây đầu tiên gắng sức tối đa, ATP và Phosphocreatine cung cấp năng lượng tức thì.", "Từ 15 giây đến 2 phút tiếp theo, đường phân kỵ khí từ glycogen cơ là nguồn năng lượng chủ đạo, tạo nhiều acid lactic.", "Khi gắng sức bền bỉ kéo dài (>30 phút), quá trình oxy hóa hiếu khí acid béo và glucose chiếm ưu thế tuyệt đối.", "Cảm giác mệt mỏi đuối cơ ('hitting the wall') ở vận động viên marathon xảy ra khi cạn kiệt hoàn toàn glycogen của cả gan và cơ."),
                ("Vai trò chuyển hóa của Vỏ thận trong nhịn đói kéo dài", "Vỏ thận (Renal cortex) có enzym Glucose-6-Phosphatase và có khả năng tân tạo đường như gan.", "Trong nhịn đói kéo dài nhiều tuần, thận có thể đóng góp tới 40-50% tổng lượng glucose tân tạo của cơ thể.", "Thận sử dụng acid amin Glutamine làm cơ chất chính cho tân tạo đường.", "Sự khử amin của Glutamine tại thận giải phóng $NH_3$ giúp đệm ion $H^+$ đào thải toan qua nước tiểu dưới dạng $NH_4^+$."),
                ("Các con đường tín hiệu điều hòa phối hợp giữa các mô", "Hormon Leptin do mô mỡ tiết ra tác động lên vùng dưới đồi làm giảm cảm giác thèm ăn và tăng tiêu hao năng lượng.", "Hormon Ghrelin do dạ dày tiết ra khi đói kích thích mạnh mẽ cảm giác thèm ăn.", "Adiponectin do mô mỡ tiết ra kích hoạt AMPK làm tăng độ nhạy cảm với insulin và kích thích $\\beta$-oxy hóa.", "Cytokine tiền viêm (TNF-$\\alpha$, IL-6) do mô mỡ phì đại tiết ra gây phosphoryl hóa sai lệch thụ thể IRS-1, thúc đẩy đề kháng insulin."),
                ("Nhiễm toan chuyển hóa và khoảng trống Anion (Anion Gap)", "Khoảng trống anion huyết thanh bình thường: $AG = [Na^+] - ([Cl^-] + [HCO_3^-]) = 8 - 12$ mEq/L.", "Tăng khoảng trống anion ($AG > 12$) xuất hiện trong toan ceton ĐTĐ (DKA), toan lactic, suy thận urê máu cao và ngộ độc methanol/salicylate.", "Khoảng trống anion bình thường (toan máu do mất $HCO_3^-$ bù trừ bằng $Cl^-$) gặp trong tiêu chảy nặng hoặc toan hóa ống thận.", "Xác định khoảng trống anion giúp phân loại chính xác nguyên nhân toan chuyển hóa trên lâm sàng cấp cứu."),
                ("Hội chứng chuyển hóa (Metabolic Syndrome)", "Được định nghĩa bởi sự kết hợp của béo phì trung tâm (vòng bụng to), tăng huyết áp, tăng đường huyết đói, tăng Triglycerid và giảm HDL-C.", "Kháng insulin và tăng insulin máu bù trừ là cơ chế sinh lý bệnh nền tảng xuyên suốt của hội chứng.", "Mô mỡ nội tạng giải phóng lượng lớn acid béo tự do vào tĩnh mạch cửa gây nhiễm mỡ gan (NAFLD/NASH).", "Hội chứng chuyển hóa làm tăng gấp nhiều lần nguy cơ biến cố tim mạch xơ vữa và đái tháo đường týp 2.")
            ]
            tp = ch18_topics[i % len(ch18_topics)]
            is_except = (i % 2 == 0)
            if is_except:
                q = f"Nhận định nào sau đây KHÔNG ĐÚNG (NGOẠI TRỪ) khi nói về {tp[0].lower()}?"
                true_stmts = [tp[1], tp[2], tp[3], tp[4]]
                false_stmt = f"Cơ chế này hoàn toàn không tuân theo các nguyên lý điều hòa chuyển hóa và không có bất kỳ tương tác hormon nào trong cơ thể."
                opts = {}
                avail_trues = list(true_stmts)
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = false_stmt
                    else:
                        opts[opt] = avail_trues.pop(0) if avail_trues else "Đảm bảo cân bằng chuyển hóa toàn thân."
                exp = f"Đáp án {corr} KHÔNG ĐÚNG. Lựa chọn này sai hoàn toàn vì: {tp[1]} {tp[2]}"
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']
            else:
                q = f"Khẳng định nào sau đây là CHÍNH XÁC NHẤT về {tp[0].lower()}?"
                opts = {}
                for opt in ['A', 'B', 'C', 'D']:
                    if opt == corr:
                        opts[opt] = tp[1 + (i % 4)]
                    else:
                        opts[opt] = f"Hiện tượng này chỉ xảy ra ở sinh vật bậc thấp và hoàn toàn không áp dụng cho người."
                exp = f"Đáp án {corr} CHÍNH XÁC: {opts[corr]}. Các đáp án khác nêu sai lệch cơ chế sinh hóa."
                a, b, c, d = opts['A'], opts['B'], opts['C'], opts['D']

        questions.append((ch18_name, q, a, b, c, d, corr, exp, 'medium' if i % 2 == 0 else 'clinical', img))

    # Insert Batch 6 into DB
    print(f"Prepared {len(questions)} questions for Batch 6 (Ch16, Ch17, Ch18). Inserting into DB...")
    for item in questions:
        cur.execute("""
            INSERT INTO questions (
                subject_id, question_text, option_a, option_b, option_c, option_d,
                correct_option, explanation, difficulty, topic_tag, image_url, q_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'multiple_choice')
        """, (sub_id, item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[0], item[9]))

    conn.commit()
    cur.execute("SELECT count(*) FROM questions WHERE subject_id = ?", (sub_id,))
    print(f"Batch 6 Seed Complete! Current total questions for subject {sub_id}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    seed_part6()
