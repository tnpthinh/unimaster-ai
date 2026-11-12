import sqlite3

def add_flashcards():
    conn = sqlite3.connect('unimaster.db')
    cur = conn.cursor()
    cur.execute("SELECT id FROM subjects WHERE code = 'HOASINH_YDS_2024'")
    sub_id = cur.fetchone()[0]

    fcs = [
        ("Chương 1: Hóa học Glucid - Khái niệm & Đồng phân",
         "• Monosacarid: D/L theo C bất đối xứng xa nhất; Epimer (C4: Glc-Gal, C2: Glc-Man).\n• Anomer (alpha/beta tại C1 bán acetal).\n• Maltose (alpha-1,4), Lactose (beta-1,4), Sucrose (alpha1, beta2 - không có tính khử).\n• Glycogen: alpha-1,4 và nhánh alpha-1,6.\n• Heparin: GAG sulfat hóa chống đông.",
         "Ghi nhớ các liên kết glycosid và tính khử của đường",
         "/static/uploads/hoasinh_yds/ch01_glucid_structures.svg"),

        ("Chương 2: Hóa học Lipid - Phân loại & Cấu trúc",
         "• Acid béo thiết yếu: Linoleic (Omega-6) và alpha-Linolenic (Omega-3).\n• Surfactant phổi: Dipalmitoylphosphatidylcholine (DPPC - Lecithin).\n• Cholesterol: 27C, nhân Steran; tiền chất acid mật, vit D3, hormon steroid.\n• Eicosanoid: từ Acid Arachidonic 20C (bị NSAID ức chế qua COX).\n• Lipoprotein: Chylomicron (TG ngoại sinh), VLDL (TG nội sinh), LDL (mảng xơ vữa), HDL (vận chuyển ngược bảo vệ).",
         "Các nhóm lipid phân cực và không phân cực",
         "/static/uploads/hoasinh_yds/ch02_lipid_classification.svg"),

        ("Chương 3: Hóa học Protid - Acid amin & Bậc cấu trúc",
         "• Glycin: không có C* duy nhất.\n• Cys, Met: chứa lưu huỳnh (-SH tạo cầu disulfid).\n• pI: pH tại đó điện tích thực = 0 (zwitterion).\n• Bậc 1: liên kết peptid; Bậc 2: xoắn alpha (H song song) & phiến gấp beta; Bậc 3: cuộn 3D; Bậc 4: nhiều tiểu đơn vị (Hb).\n• Albumin: tạo 75-80% áp suất keo huyết tương.",
         "20 acid amin chuẩn và cấu trúc bậc protein",
         "/static/uploads/hoasinh_yds/ch03_amino_acid_peptide.svg"),

        ("Chương 4: Hóa học Hemoglobin - Heme & Hiệu ứng Bohr",
         "• Heme: Protoporphyrin IX + Fe2+.\n• Tetramer: HbA1 (alpha2 beta2), HbF (alpha2 gamma2 - ái lực O2 cao hơn do gắn 2,3-BPG yếu).\n• Đường cong bão hòa: Sigmoid (tương tác hợp tác allosteric).\n• Hiệu ứng Bohr: pH giảm, pCO2 tăng, 2,3-BPG tăng, T tăng => Chuyển PHẢI (nhả O2).\n• HbS: Đột biến codon 6 chuỗi beta: Glu -> Val (hồng cầu hình liềm).",
         "Điều hòa ái lực oxy của hemoglobin",
         "/static/uploads/hoasinh_yds/ch04_hemoglobin_oxygen_curve.svg"),

        ("Chương 5: Nucleotid & Acid Nucleic - Cấu trúc DNA/RNA",
         "• Đơn phân: Base nitơ (Purin A,G; Pyrimidin C,T,U) + Pentose + Phosphat.\n• B-DNA: Xoắn kép ngược chiều, 10 bp/chu kỳ (3.4 nm), đường kính 2.0 nm.\n• Chargaff: A=T (2 liên kết H), G=C (3 liên kết H => Tm tỷ lệ thuận với %G-C).\n• Hiệu ứng tăng sắc A260 khi sợi đôi biến tính thành sợi đơn.\n• tRNA: đầu 3'-CCA gắn acid amin; mRNA có mũ 5'-cap m7G và đuôi polyA 3'.",
         "Quy tắc bổ sung Watson-Crick và các loại RNA",
         "/static/uploads/hoasinh_yds/ch05_dna_rna_structure.svg"),

        ("Chương 6: Vitamin & Coenzym Y học",
         "• B1 (Thiamin -> TPP): thiếu gây Beriberi, Wernicke-Korsakoff.\n• B3 (Niacin -> NAD/NADP): thiếu gây Pellagra (3D: Viêm da, Tiêu chảy, Sa sút trí tuệ).\n• B6 (PLP): trao đổi amin transaminase AST/ALT.\n• B9 (Folate) & B12: tạo máu hồng cầu to; thiếu B12 gây tổn thương tủy sống.\n• Tan trong dầu (A, D, E, K): D (1,25-(OH)2-D3 Calcitriol); K (gamma-carboxyl hóa II, VII, IX, X).",
         "Các bệnh thiếu hụt vitamin tương ứng",
         "/static/uploads/hoasinh_yds/ch06_vitamins_coenzymes.svg"),

        ("Chương 7: Enzym - Động học & Ức chế",
         "• Km: [S] tại đó v = Vmax/2 (Km tỷ lệ nghịch với ái lực).\n• Ức chế cạnh tranh: Km tăng, Vmax không đổi (vd Statin, Allopurinol).\n• Ức chế phi cạnh tranh: Km không đổi, Vmax giảm.\n• 6 lớp EC: 1.Oxidoreductase, 2.Transferase, 3.Hydrolase, 4.Lyase, 5.Isomerase, 6.Ligase.\n• Dấu ấn tim: CK-MB, Troponin I/T. Tắc mật: ALP, GGT.",
         "Đồ thị Lineweaver-Burk và các kiểu ức chế",
         "/static/uploads/hoasinh_yds/ch07_lineweaver_burk_inhibition.svg"),

        ("Chương 8: Hormon & Cơ chế truyền tín hiệu",
         "• Thụ thể nội bào (Steroid, T3/T4): gắn HRE trên DNA điều hòa phiên mã gen (tác dụng chậm).\n• Thụ thể màng GPCR: (1) Con đường cAMP (Glucagon, Adrenalin qua Gs -> PKA); (2) Con đường IP3/DAG (Gq -> PLC -> Ca2+ & PKC).\n• Thụ thể Tyrosine Kinase (Insulin): tự phosphoryl hóa, kích hoạt IRS-1 và GLUT4.\n• Thụ thể cGMP (NO, ANP): giãn cơ trơn mạch máu.",
         "Các hệ thống chất truyền tin thứ hai",
         "/static/uploads/hoasinh_yds/ch08_hormone_signal_transduction.svg"),

        ("Chương 9: Khái niệm về chuyển hóa các chất",
         "• Dị hóa: Phân giải sinh năng lượng (hội tụ về Acetyl-CoA và chu trình Krebs).\n• Đồng hóa: Tổng hợp tiêu tốn ATP và NADPH.\n• Hợp chất cao năng: PEP (-61.9 kJ/mol), 1,3-BPG (-49.3 kJ/mol), Phosphocreatine (-43.1 kJ/mol), ATP (-30.5 kJ/mol), Acetyl-CoA (liên kết thioester).\n• Ghép đôi năng lượng qua ATP kết nối phản ứng thu nhiệt với tỏa nhiệt.",
         "Năng lượng sinh học và dòng vật chất",
         "/static/uploads/hoasinh_yds/ch09_metabolic_pathways_overview.svg"),

        ("Chương 10: Chuyển hóa năng lượng - Chu trình Krebs & ETC",
         "• Krebs (8 phản ứng matrix ty thể): 1 Acetyl-CoA -> 2 CO2 + 3 NADH + 1 FADH2 + 1 GTP (~10 ATP).\n• Bước kiểm soát: Isocitrate Dehydrogenase.\n• Chuỗi ETC: Phức hợp I (bơm 4H+), II (FADH2, không bơm H+), III (bơm 4H+), IV (bơm 2H+, đích của Cyanide, CO).\n• Thuyết hóa thẩm Mitchell: Lực động proton dẫn động ATP Synthase (F0F1).\n• Phá ghép (DNP, Thermogenin): tiêu thụ O2 tăng nhưng chỉ sinh NHIỆT không tạo ATP.",
         "Chuỗi truyền điện tử và phosphoryl hóa oxy hóa",
         "/static/uploads/hoasinh_yds/ch10_krebs_cycle_tca.svg"),

        ("Chương 11: Chuyển hóa Glucid - Đường phân & Tân tạo",
         "• 3 enzym một chiều đường phân: Hexokinase/Glucokinase, PFK-1 (chất hoạt hóa mạnh F-2,6-BP), Pyruvate Kinase.\n• Kỵ khí: Pyruvate -> Lactate (LDH) tái tạo NAD+, thuần 2 ATP/Glucose.\n• Hiếu khí: tạo 30-32 ATP.\n• Tân tạo đường: 4 enzym (Pyruvate carboxylase, PEPCK, FBPase-1, G6Pase ở gan/thận).\n• G6PD: tạo NADPH bảo vệ hồng cầu; thiếu gây thiếu máu tán huyết cấp khi gặp chất oxy hóa.",
         "Đường phân, chu trình Cori và con đường Pentose Phosphate",
         "/static/uploads/hoasinh_yds/ch11_glycolysis_gluconeogenesis.svg"),

        ("Chương 12: Chuyển hóa Lipid - Beta-oxy hóa & Thể Ceton",
         "• Con thoi Carnitine (CPT-I): đưa acyl-CoA vào ty thể, bị Malonyl-CoA ức chế.\n• Beta-oxy hóa: 4 bước (Oxy hóa FAD -> Hợp nước -> Oxy hóa NAD+ -> Cắt Thiolase). Palmitate 16C thu 106 ATP thuần.\n• Thể Ceton: Acetoacetate, beta-hydroxybutyrate, Acetone. Gan tổng hợp nhưng KHÔNG dùng được do thiếu thiophorase.\n• Tổng hợp acid béo (bào tương): ACC chuyển Acetyl-CoA thành Malonyl-CoA (cần Biotin, CO2, ATP). Phức hợp FAS.\n• Statin: ức chế cạnh tranh HMG-CoA Reductase hạ cholesterol.",
         "Thoái hóa acid béo và sinh tổng hợp lipid",
         "/static/uploads/hoasinh_yds/ch12_fatty_acid_beta_oxidation.svg"),

        ("Chương 13: Chuyển hóa Protid - Chu trình Ure",
         "• Trao đổi amin (PLP) -> Khử amin oxy hóa (GDH giải phóng NH4+).\n• Chu trình Ure (gan): CPS-I (ty thể, cần N-acetylglutamate) -> OTC -> Citrulline (ra bào tương) -> Argininosuccinate -> Arginine -> Urea + Ornithine.\n• Nguồn gốc Nitơ ure: 1 từ NH4+ tự do, 1 từ Aspartate.\n• Thiếu OTC (di truyền lặn NST X): tăng amoniac máu, acid orotic niệu.\n• Rối loạn acid amin: PKU (thiếu PAH), Alkapton niệu (thiếu Homogentisate oxidase, nước tiểu đen), Siro niệu (thiếu BCKDH chuỗi nhánh).",
         "Đào thải amoniac và bệnh rối loạn acid amin",
         "/static/uploads/hoasinh_yds/ch13_urea_cycle_ornithine.svg"),

        ("Chương 14: Chuyển hóa Hemoglobin & Sắc tố mật",
         "• Heme -> Biliverdin + Fe2+ + CO (Heme oxygenase) -> Bilirubin gián tiếp (UCB, kỵ nước, gắn Albumin, độc thần kinh).\n• Gan liên hợp: UGT1A1 gắn 2 acid glucuronic -> Bilirubin trực tiếp (CB, tan trong nước, vào mật).\n• Ruột: khử thành Urobilinogen & Stercobilin (nâu phân).\n• Tắc mật: Bilirubin trực tiếp tăng vọt, nước tiểu sậm màu, phân bạc màu.\n• Tán huyết: Bilirubin gián tiếp tăng cao, bilirubin niệu âm tính.\n• Gilbert: giảm 70% UGT1A1 lành tính. Crigler-Najjar: thiếu nặng/mất hoàn toàn UGT1A1.",
         "Chuyển hóa Bilirubin và các dạng vàng da lâm sàng",
         "/static/uploads/hoasinh_yds/ch14_bilirubin_metabolism.svg"),

        ("Chương 15: Chuyển hóa Acid Nucleic & Bệnh Gout",
         "• Tổng hợp Purine de novo: từ PRPP, enzym giới hạn Glutamine-PRPP amidotransferase. Cần Gly, Gln, Asp, THF, CO2.\n• Thoái hóa Purine: Hypoxanthine -> Xanthine -> Acid Uric (Xanthine Oxidase).\n• Bệnh Gout: Acid Uric > 420 umol/L, lắng đọng tinh thể Monosodium Urate hình kim phân cực âm.\n• Allopurinol: ức chế tự sát Xanthine Oxidase.\n• Hội chứng Lesch-Nyhan: thiếu hoàn toàn HGPRT (tự cắn xé môi ngón tay, Gout nặng).",
         "Thoái hóa purine và cơ chế bệnh sinh của Gout",
         "/static/uploads/hoasinh_yds/ch15_purine_uric_acid_gout.svg"),

        ("Chương 16: Kỹ thuật PCR & Giải trình tự Acid Nucleic",
         "• PCR 3 pha: Biến tính (94-95°C) -> Bắt cặp mồi (50-65°C) -> Kéo dài (72°C nhờ Taq polymerase).\n• Real-time PCR: Giá trị Ct tỷ lệ nghịch với log số bản sao ban đầu. SYBR Green (xen kẽ phi đặc hiệu) vs Đầu dò TaqMan (FRET đặc hiệu nhờ 5'->3' exonuclease).\n• RT-PCR: dùng Reverse transcriptase phiên mã ngược RNA thành cDNA.\n• Sanger: kết thúc chuỗi bằng ddNTP thiếu 3'-OH.\n• NGS: Illumina (giải trình tự bằng tổng hợp SBS trên Flow cell), Nanopore (đo dòng điện qua lỗ nano).",
         "Các công nghệ sinh học phân tử hiện đại",
         "/static/uploads/hoasinh_yds/ch16_pcr_cycle_phases.svg"),

        ("Chương 17: Sinh tổng hợp Protein & Tác động kháng sinh",
         "• Mã di truyền: Bộ ba, thoái hóa, khởi đầu AUG (Met), kết thúc UAA, UAG, UGA.\n• Hoạt hóa tRNA: Aminoacyl-tRNA synthetase (tiêu 2 liên kết cao năng ATP).\n• Ribosome: Vi khuẩn 70S (30S+50S); Người 80S (40S+60S). Vị trí A (nhận codon), P (chuỗi peptid), E (thoát).\n• Peptidyl transferase: xúc tác bởi rRNA (Ribozyme).\n• Kháng sinh 30S: Aminoglycoside (đọc sai mã), Tetracycline (khóa vị trí A).\n• Kháng sinh 50S: Chloramphenicol (ức chế peptidyl transferase), Macrolide (ức chế translocation).",
         "Quá trình dịch mã và cơ chế chọn lọc kháng sinh",
         "/static/uploads/hoasinh_yds/ch17_translation_ribosome.svg"),

        ("Chương 18: Điều hòa chuyển hóa toàn thân",
         "• No (Insulin cao): tăng GLUT4, tổng hợp glycogen, lipid, protein.\n• Đói sớm (Glucagon cao, 12-24h): tiêu glycogen gan duy trì đường huyết, HSL ly giải mỡ.\n• Nhịn đói kéo dài (>3 ngày): não chuyển sang đốt Thể Ceton (thay thế 60-70% nhu cầu), gan/thận tân tạo đường từ acid amin/glycerol, tiết kiệm phân giải protein cơ.\n• Não: không dùng acid béo tự do. Hồng cầu: 100% đường phân kỵ khí.\n• Refeeding Syndrome: cho ăn đường ồ ạt kéo PO4, K, Mg vào nội bào gây hạ phosphat máu cấp tử vong.",
         "Cân bằng năng lượng giữa các cơ quan",
         "/static/uploads/hoasinh_yds/ch18_metabolic_regulation_hormones.svg")
    ]

    for title, back, hint, img in fcs:
        cur.execute("""
            INSERT INTO flashcards (subject_id, front, back, hint, image_url)
            VALUES (?, ?, ?, ?, ?)
        """, (sub_id, title, back, hint, img))

    conn.commit()
    cur.execute("SELECT count(*) FROM flashcards WHERE subject_id = ?", (sub_id,))
    print(f"Added {len(fcs)} flashcards! Total flashcards for subject {sub_id}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    add_flashcards()
