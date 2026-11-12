import os

os.makedirs('static/uploads/hoasinh_yds', exist_ok=True)

svg_defs = {
    'ch03_amino_acid_peptide.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#38bdf8" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">HÓA HỌC PROTID: ACID AMIN, ĐIỂM ĐẲNG ĐIỆN &amp; LIÊN KẾT PEPTID</text>
  <g transform="translate(50, 65)">
    <rect width="210" height="260" fill="#1e293b" rx="12" stroke="#38bdf8" stroke-width="2"/>
    <text x="105" y="30" fill="#7dd3fc" font-size="14" font-weight="bold" text-anchor="middle" font-family="sans-serif">Dạng Lưỡng Cực (Zwitterion)</text>
    <text x="105" y="70" fill="#f8fafc" font-size="14" text-anchor="middle" font-family="monospace">+H3N — CH(R) — COO-</text>
    <rect x="20" y="100" width="170" height="70" fill="#334155" rx="8"/>
    <text x="105" y="122" fill="#fef08a" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">pH = pI (Điểm đẳng điện)</text>
    <text x="105" y="145" fill="#e2e8f0" font-size="11" text-anchor="middle" font-family="sans-serif">Điện tích thực = 0</text>
    <text x="105" y="160" fill="#fca5a5" font-size="11" text-anchor="middle" font-family="sans-serif">Không di chuyển trong điện di</text>
    <text x="105" y="205" fill="#93c5fd" font-size="11" text-anchor="middle" font-family="sans-serif">pH &lt; pI: Tích điện (+) (Cation)</text>
    <text x="105" y="230" fill="#f472b6" font-size="11" text-anchor="middle" font-family="sans-serif">pH &gt; pI: Tích điện (-) (Anion)</text>
  </g>
  <g transform="translate(295, 65)">
    <rect width="210" height="260" fill="#1e293b" rx="12" stroke="#a855f7" stroke-width="2"/>
    <text x="105" y="30" fill="#c084fc" font-size="14" font-weight="bold" text-anchor="middle" font-family="sans-serif">Cấu Trúc Liên Kết Peptid</text>
    <text x="105" y="75" fill="#f8fafc" font-size="15" text-anchor="middle" font-family="monospace">— CO — NH —</text>
    <rect x="20" y="100" width="170" height="140" fill="#334155" rx="8"/>
    <text x="105" y="125" fill="#6ee7b7" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Tính Chất Bền Vững</text>
    <text x="105" y="150" fill="#e2e8f0" font-size="11" text-anchor="middle" font-family="sans-serif">• Đồng phẳng, lai hóa sp2</text>
    <text x="105" y="175" fill="#e2e8f0" font-size="11" text-anchor="middle" font-family="sans-serif">• Bản chất liên kết đôi một phần</text>
    <text x="105" y="200" fill="#fef08a" font-size="11" text-anchor="middle" font-family="sans-serif">• Cấu hình Trans bền hơn Cis</text>
    <text x="105" y="225" fill="#cbd5e1" font-size="11" text-anchor="middle" font-family="sans-serif">• Bị thủy phân bởi protease</text>
  </g>
  <g transform="translate(540, 65)">
    <rect width="210" height="260" fill="#1e293b" rx="12" stroke="#10b981" stroke-width="2"/>
    <text x="105" y="30" fill="#34d399" font-size="14" font-weight="bold" text-anchor="middle" font-family="sans-serif">Bậc Cấu Trúc Protein</text>
    <rect x="15" y="55" width="180" height="40" fill="#064e3b" rx="6"/>
    <text x="105" y="80" fill="#a7f3d0" font-size="11" font-weight="bold" text-anchor="middle" font-family="sans-serif">Bậc 1: Chuỗi polypeptide</text>
    <rect x="15" y="105" width="180" height="40" fill="#047857" rx="6"/>
    <text x="105" y="130" fill="#ecfdf5" font-size="11" font-weight="bold" text-anchor="middle" font-family="sans-serif">Bậc 2: Xoắn α &amp; Gấp nếp β</text>
    <rect x="15" y="155" width="180" height="40" fill="#059669" rx="6"/>
    <text x="105" y="180" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle" font-family="sans-serif">Bậc 3: Không gian 3D cuộn</text>
    <rect x="15" y="205" width="180" height="40" fill="#10b981" rx="6"/>
    <text x="105" y="230" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="middle" font-family="sans-serif">Bậc 4: Nhiều tiểu đơn vị (Hb)</text>
  </g>
</svg>''',

    'ch04_hemoglobin_oxygen_curve.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#f87171" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">HÓA HỌC HEMOGLOBIN: ĐƯỜNG CONG Phân Ly O2 &amp; HIỆU ỨNG BOHR</text>
  <g transform="translate(60, 65)">
    <rect width="380" height="260" fill="#1e293b" rx="12" stroke="#ef4444" stroke-width="1.5"/>
    <line x1="50" y1="220" x2="340" y2="220" stroke="#94a3b8" stroke-width="2"/>
    <line x1="50" y1="220" x2="50" y2="40" stroke="#94a3b8" stroke-width="2"/>
    <text x="345" y="225" fill="#cbd5e1" font-size="11" font-family="sans-serif">pO2 (mmHg)</text>
    <text x="50" y="30" fill="#cbd5e1" font-size="11" font-family="sans-serif">Độ bão hòa O2 (%)</text>
    <path d="M 50,220 Q 70,60 330,55" fill="none" stroke="#38bdf8" stroke-width="3" stroke-dasharray="4,4"/>
    <text x="210" y="75" fill="#38bdf8" font-size="12" font-weight="bold">Myoglobin (Hyperbol)</text>
    <path d="M 50,220 C 120,215 150,110 330,65" fill="none" stroke="#ef4444" stroke-width="3.5"/>
    <text x="220" y="130" fill="#f87171" font-size="12" font-weight="bold">Hemoglobin (Sigmoid - Chữ S)</text>
    <path d="M 50,220 C 150,220 180,140 330,85" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3,3"/>
    <text x="210" y="180" fill="#f59e0b" font-size="11">Chuyển Phải: Tăng H+, CO2, 2,3-BPG, T°</text>
  </g>
  <g transform="translate(460, 65)">
    <rect width="280" height="260" fill="#1e293b" rx="12" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="140" y="30" fill="#fbbf24" font-size="14" font-weight="bold" text-anchor="middle" font-family="sans-serif">Hiệu Ứng Bohr &amp; Điều Hòa</text>
    <rect x="15" y="50" width="250" height="55" fill="#334155" rx="8"/>
    <text x="140" y="72" fill="#ef4444" font-size="12" font-weight="bold" text-anchor="middle">Tại Mô Ngoại Vi (Chuyển Phải)</text>
    <text x="140" y="92" fill="#fecaca" font-size="11" text-anchor="middle">Tăng pCO2, tăng H+ (giảm pH) =&gt; Nhả O2</text>
    <rect x="15" y="115" width="250" height="55" fill="#334155" rx="8"/>
    <text x="140" y="137" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Tại Phổi (Chuyển Trái)</text>
    <text x="140" y="157" fill="#bae6fd" font-size="11" text-anchor="middle">Giảm pCO2, kiềm hóa =&gt; Tăng bắt O2</text>
    <rect x="15" y="180" width="250" height="65" fill="#334155" rx="8"/>
    <text x="140" y="202" fill="#a855f7" font-size="12" font-weight="bold" text-anchor="middle">HbF so với HbA (Người lớn)</text>
    <text x="140" y="222" fill="#e9d5ff" font-size="10.5" text-anchor="middle">HbF (α2γ2) ái lực 2,3-BPG yếu hơn</text>
    <text x="140" y="237" fill="#e9d5ff" font-size="10.5" text-anchor="middle">=&gt; Ái lực O2 CAO HƠN HbA (bắt O2 từ mẹ)</text>
  </g>
</svg>''',

    'ch05_dna_rna_structure.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#38bdf8" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">HÓA HỌC NUCLEOTID &amp; CẤU TRÚC XOẮN KÉP ACID NUCLEIC</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="165" y="30" fill="#7dd3fc" font-size="14" font-weight="bold" text-anchor="middle">Thành Phần Đơn Phân (Nucleotid)</text>
    <rect x="20" y="55" width="290" height="55" fill="#334155" rx="8"/>
    <text x="165" y="78" fill="#fef08a" font-size="12" font-weight="bold" text-anchor="middle">1. Base Nitơ: Purine &amp; Pyrimidine</text>
    <text x="165" y="98" fill="#e2e8f0" font-size="11" text-anchor="middle">Purine: Adenin (A), Guanin (G) (2 vòng)</text>
    <rect x="20" y="120" width="290" height="55" fill="#334155" rx="8"/>
    <text x="165" y="143" fill="#f472b6" font-size="12" font-weight="bold" text-anchor="middle">2. Đường Pentose (5 Carbon)</text>
    <text x="165" y="163" fill="#e2e8f0" font-size="11" text-anchor="middle">DNA: 2\'-deoxy-D-ribose | RNA: D-ribose</text>
    <rect x="20" y="185" width="290" height="55" fill="#334155" rx="8"/>
    <text x="165" y="208" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">3. Gốc Phosphat (H3PO4)</text>
    <text x="165" y="228" fill="#e2e8f0" font-size="11" text-anchor="middle">Liên kết Phosphodiester 3\'-5\' nối các monome</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#8b5cf6" stroke-width="1.5"/>
    <text x="170" y="30" fill="#c084fc" font-size="14" font-weight="bold" text-anchor="middle">Quy Tắc Chargaff &amp; Watson-Crick</text>
    <rect x="20" y="55" width="300" height="60" fill="#334155" rx="8"/>
    <text x="170" y="80" fill="#38bdf8" font-size="13" font-weight="bold" text-anchor="middle">A = T (2 liên kết Hydro)</text>
    <text x="170" y="102" fill="#f87171" font-size="13" font-weight="bold" text-anchor="middle">G ≡ C (3 liên kết Hydro - Bền hơn)</text>
    <rect x="20" y="125" width="300" height="115" fill="#334155" rx="8"/>
    <text x="170" y="148" fill="#fef08a" font-size="12" font-weight="bold" text-anchor="middle">Đặc Điểm Mô Hình B-DNA</text>
    <text x="170" y="170" fill="#e2e8f0" font-size="11" text-anchor="middle">• 2 chuỗi song song ngược chiều (5\'→3\' &amp; 3\'→5\')</text>
    <text x="170" y="190" fill="#e2e8f0" font-size="11" text-anchor="middle">• Chu kỳ xoắn: 3,4 nm = 10 cặp base (bp)</text>
    <text x="170" y="210" fill="#e2e8f0" font-size="11" text-anchor="middle">• Đường kính xoắn: 2,0 nm (20 Å)</text>
    <text x="170" y="230" fill="#6ee7b7" font-size="11" text-anchor="middle">• Rãnh lớn (Major groove) &amp; Rãnh nhỏ</text>
  </g>
</svg>''',

    'ch06_vitamins_coenzymes.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#f59e0b" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">VITAMIN &amp; CÁC COENZYM TƯƠNG ỨNG TRONG Y HỌC</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="165" y="30" fill="#fbbf24" font-size="14" font-weight="bold" text-anchor="middle">Nhóm Vitamin Tan Trong Nước (B, C)</text>
    <rect x="15" y="50" width="300" height="45" fill="#334155" rx="6"/>
    <text x="165" y="70" fill="#f8fafc" font-size="11" text-anchor="middle"><tspan fill="#fbbf24" font-weight="bold">B1 (Thiamin):</tspan> Coenzym TPP (Khử carboxyl α-cetoacid)</text>
    <text x="165" y="85" fill="#fca5a5" font-size="10" text-anchor="middle">Thiếu: Bệnh Beriberi, hội chứng Wernicke-Korsakoff</text>
    <rect x="15" y="102" width="300" height="45" fill="#334155" rx="6"/>
    <text x="165" y="122" fill="#f8fafc" font-size="11" text-anchor="middle"><tspan fill="#38bdf8" font-weight="bold">B2 (Riboflavin):</tspan> Coenzym FMN, FAD (Oxy hóa khử)</text>
    <rect x="15" y="154" width="300" height="45" fill="#334155" rx="6"/>
    <text x="165" y="174" fill="#f8fafc" font-size="11" text-anchor="middle"><tspan fill="#34d399" font-weight="bold">B3 (PP / Niacin):</tspan> Coenzym NAD+, NADP+</text>
    <text x="165" y="189" fill="#fca5a5" font-size="10" text-anchor="middle">Thiếu: Bệnh Pellagra (3D: Viêm da, Tiêu chảy, Sa sút)</text>
    <rect x="15" y="206" width="300" height="45" fill="#334155" rx="6"/>
    <text x="165" y="226" fill="#f8fafc" font-size="11" text-anchor="middle"><tspan fill="#c084fc" font-weight="bold">B6 (Pyridoxine):</tspan> PLP (Trao đổi amin Transaminase)</text>
    <text x="165" y="241" fill="#fca5a5" font-size="10" text-anchor="middle">B9 (Folate) &amp; B12: Tạo máu, tổng hợp thymidylate</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#10b981" stroke-width="1.5"/>
    <text x="170" y="30" fill="#34d399" font-size="14" font-weight="bold" text-anchor="middle">Nhóm Vitamin Tan Trong Dầu (A, D, E, K)</text>
    <rect x="15" y="50" width="310" height="45" fill="#334155" rx="6"/>
    <text x="170" y="70" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Vitamin A (Retinol, Retinal, Retinoic acid)</text>
    <text x="170" y="85" fill="#cbd5e1" font-size="10" text-anchor="middle">Thị giác (Rhodopsin que), biểu mô. Thiếu: Quáng gà, khô mắt</text>
    <rect x="15" y="102" width="310" height="45" fill="#334155" rx="6"/>
    <text x="170" y="122" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">Vitamin D (Calcitriol - 1,25-(OH)2-D3)</text>
    <text x="170" y="137" fill="#cbd5e1" font-size="10" text-anchor="middle">Hấp thu Ca/P ở ruột, khoáng hóa xương. Còi xương, nhuyễn xương</text>
    <rect x="15" y="154" width="310" height="45" fill="#334155" rx="6"/>
    <text x="170" y="174" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Vitamin E (Tocopherol)</text>
    <text x="170" y="189" fill="#cbd5e1" font-size="10" text-anchor="middle">Chống oxy hóa tan trong mỡ, bảo vệ màng tế bào &amp; RBC</text>
    <rect x="15" y="206" width="310" height="45" fill="#334155" rx="6"/>
    <text x="170" y="226" fill="#4ade80" font-size="11" font-weight="bold" text-anchor="middle">Vitamin K (Phylloquinone, Menaquinone)</text>
    <text x="170" y="241" fill="#cbd5e1" font-size="10" text-anchor="middle">γ-carboxyl hóa yếu tố đông máu II, VII, IX, X tại gan</text>
  </g>
</svg>''',

    'ch08_hormone_signal_transduction.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#f472b6" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">CƠ CHẾ TRUYỀN TÍN HIỆU HORMON &amp; CHẤT TRUYỀN TIN THỨ HAI</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#ec4899" stroke-width="1.5"/>
    <text x="165" y="30" fill="#f472b6" font-size="14" font-weight="bold" text-anchor="middle">Hormon Màng Tế Bào (Peptid/Catecholamin)</text>
    <rect x="15" y="50" width="300" height="90" fill="#334155" rx="8"/>
    <text x="165" y="72" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">1. Con Đường cAMP (Gs / Gi)</text>
    <text x="165" y="92" fill="#e2e8f0" font-size="11" text-anchor="middle">Hormon + GPCR =&gt; Adenylate Cyclase</text>
    <text x="165" y="110" fill="#fef08a" font-size="11" text-anchor="middle">ATP =&gt; cAMP =&gt; Hoạt hóa Protein Kinase A (PKA)</text>
    <text x="165" y="128" fill="#94a3b8" font-size="10" text-anchor="middle">Glucagon, Adrenalin, TSH, ACTH, PTH...</text>
    <rect x="15" y="150" width="300" height="95" fill="#334155" rx="8"/>
    <text x="165" y="172" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">2. Con Đường Phospholipase C (Gq)</text>
    <text x="165" y="192" fill="#e2e8f0" font-size="11" text-anchor="middle">PLC phân cắt PIP2 =&gt; IP3 + DAG</text>
    <text x="165" y="210" fill="#fef08a" font-size="11" text-anchor="middle">IP3 phóng thích Ca2+ nội bào | DAG hoạt hóa PKC</text>
    <text x="165" y="228" fill="#94a3b8" font-size="10" text-anchor="middle">Oxytocin, Vasopressin (V1), Angiotensin II...</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#a855f7" stroke-width="1.5"/>
    <text x="170" y="30" fill="#c084fc" font-size="14" font-weight="bold" text-anchor="middle">Hormon Thấm Qua Màng (Steroid &amp; Tuyến Giáp)</text>
    <rect x="15" y="50" width="310" height="90" fill="#334155" rx="8"/>
    <text x="170" y="72" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">Thụ Thể Nội Bào (Bào tương / Nhân)</text>
    <text x="170" y="92" fill="#e2e8f0" font-size="11" text-anchor="middle">Hormon khuếch tán qua màng phospholipid kép</text>
    <text x="170" y="110" fill="#fef08a" font-size="11" text-anchor="middle">Gắn thụ thể =&gt; Phức hợp Hormon-Thụ thể</text>
    <text x="170" y="128" fill="#94a3b8" font-size="10" text-anchor="middle">Cortisol, Aldosteron, Estrogen, Testosterone, T3/T4</text>
    <rect x="15" y="150" width="310" height="95" fill="#334155" rx="8"/>
    <text x="170" y="172" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Cơ Chế Tác Dụng: Biểu Hiện Gen</text>
    <text x="170" y="192" fill="#e2e8f0" font-size="11" text-anchor="middle">Phức hợp gắn lên yếu tố đáp ứng Hormon (HRE)</text>
    <text x="170" y="210" fill="#6ee7b7" font-size="11" text-anchor="middle">Điều hòa phiên mã gen đích =&gt; Tổng hợp mRNA mới</text>
    <text x="170" y="228" fill="#fca5a5" font-size="10" text-anchor="middle">Thời gian tác dụng chậm (vài giờ - vài ngày)</text>
  </g>
</svg>''',

    'ch09_metabolic_pathways_overview.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#38bdf8" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">KHÁI NIỆM VỀ CHUYỂN HÓA CÁC CHẤT &amp; DÒNG NĂNG LƯỢNG</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="165" y="30" fill="#7dd3fc" font-size="14" font-weight="bold" text-anchor="middle">Dị Hóa (Catabolism - Phân giải)</text>
    <rect x="20" y="55" width="290" height="45" fill="#334155" rx="6"/>
    <text x="165" y="78" fill="#f8fafc" font-size="12" text-anchor="middle">Đại phân tử: Glucid, Lipid, Protein</text>
    <text x="165" y="120" fill="#38bdf8" font-size="20" text-anchor="middle">⬇</text>
    <rect x="20" y="135" width="290" height="45" fill="#334155" rx="6"/>
    <text x="165" y="158" fill="#fef08a" font-size="12" font-weight="bold" text-anchor="middle">Acetyl-CoA &amp; Các Sản Phẩm Trung Gian</text>
    <text x="165" y="200" fill="#38bdf8" font-size="20" text-anchor="middle">⬇</text>
    <rect x="20" y="215" width="290" height="45" fill="#064e3b" rx="6"/>
    <text x="165" y="238" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">Giải phóng Năng lượng (ATP, NADH, FADH2)</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="170" y="30" fill="#fbbf24" font-size="14" font-weight="bold" text-anchor="middle">Đồng Hóa (Anabolism - Tổng hợp)</text>
    <rect x="20" y="55" width="300" height="45" fill="#334155" rx="6"/>
    <text x="170" y="78" fill="#f8fafc" font-size="12" text-anchor="middle">Tiền chất nhỏ: Acid amin, Acid béo, Monosacarid</text>
    <text x="170" y="120" fill="#f59e0b" font-size="20" text-anchor="middle">⬇ + Tiêu tốn ATP &amp; NADPH</text>
    <rect x="20" y="135" width="300" height="45" fill="#334155" rx="6"/>
    <text x="170" y="158" fill="#f472b6" font-size="12" font-weight="bold" text-anchor="middle">Đại Phân Tử Sinh Học (Glycogen, TG, Protein)</text>
    <rect x="20" y="195" width="300" height="55" fill="#334155" rx="6"/>
    <text x="170" y="215" fill="#e2e8f0" font-size="11" text-anchor="middle"><tspan fill="#fbbf24" font-weight="bold">Ý nghĩa:</tspan> Xây dựng cấu trúc tế bào, mô,</text>
    <text x="170" y="235" fill="#e2e8f0" font-size="11" text-anchor="middle">dự trữ năng lượng và các chất hoạt tính sinh học</text>
  </g>
</svg>''',

    'ch11_glycolysis_gluconeogenesis.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#38bdf8" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">CHUYỂN HÓA GLUCID: ĐƯỜNG PHÂN (GLYCOLYSIS) &amp; TÂN TẠO ĐƯỜNG</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="165" y="30" fill="#7dd3fc" font-size="14" font-weight="bold" text-anchor="middle">3 Phản Ứng Một Chiều (Khóa Đường Phân)</text>
    <rect x="15" y="50" width="300" height="60" fill="#334155" rx="6"/>
    <text x="165" y="72" fill="#fef08a" font-size="11" font-weight="bold" text-anchor="middle">1. Glucose =&gt; G6P (Hexokinase / Glucokinase)</text>
    <text x="165" y="92" fill="#cbd5e1" font-size="10" text-anchor="middle">Glucokinase (Gan/Tụy): Km cao, không bị G6P ức chế</text>
    <rect x="15" y="118" width="300" height="60" fill="#334155" rx="6"/>
    <text x="165" y="140" fill="#f87171" font-size="11" font-weight="bold" text-anchor="middle">2. F6P =&gt; F1,6-BP (PFK-1 - Enzym Giới Hạn Tốc Độ)</text>
    <text x="165" y="160" fill="#cbd5e1" font-size="10" text-anchor="middle">Hoạt hóa mạnh bởi F2,6-BP, AMP | Ức chế bởi ATP, Citrat</text>
    <rect x="15" y="186" width="300" height="60" fill="#334155" rx="6"/>
    <text x="165" y="208" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">3. PEP =&gt; Pyruvat (Pyruvat Kinase)</text>
    <text x="165" y="228" fill="#cbd5e1" font-size="10" text-anchor="middle">Tạo ATP ở mức cơ chất | Hoạt hóa bởi F1,6-BP</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#10b981" stroke-width="1.5"/>
    <text x="170" y="30" fill="#34d399" font-size="14" font-weight="bold" text-anchor="middle">Tân Tạo Đường (Gluconeogenesis)</text>
    <rect x="15" y="50" width="310" height="80" fill="#334155" rx="6"/>
    <text x="170" y="72" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">4 Enzym Vượt Cửa Ải Một Chiều</text>
    <text x="170" y="92" fill="#e2e8f0" font-size="10.5" text-anchor="middle">• Pyruvat carboxylase (Ty thể, cần Biotin)</text>
    <text x="170" y="108" fill="#e2e8f0" font-size="10.5" text-anchor="middle">• PEPCK (Phosphoenolpyruvat carboxykinase)</text>
    <text x="170" y="124" fill="#e2e8f0" font-size="10.5" text-anchor="middle">• Fructose-1,6-bisphosphatase &amp; Glucose-6-phosphatase</text>
    <rect x="15" y="138" width="310" height="108" fill="#334155" rx="6"/>
    <text x="170" y="160" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Hiệu Suất Năng Lượng Đường Phân</text>
    <text x="170" y="182" fill="#f8fafc" font-size="11" text-anchor="middle">Hiếu khí: 1 Glucose =&gt; 2 Pyruvat + 2 ATP + 2 NADH (~30-32 ATP)</text>
    <text x="170" y="204" fill="#fca5a5" font-size="11" text-anchor="middle">Kỵ khí (RBC, cơ co rút): 1 Glucose =&gt; 2 Lactat + 2 ATP thuần</text>
    <text x="170" y="226" fill="#fef08a" font-size="10.5" text-anchor="middle">Hồng cầu không có ty thể =&gt; bắt buộc chuyển hóa kỵ khí!</text>
  </g>
</svg>''',

    'ch12_fatty_acid_beta_oxidation.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#fbbf24" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">CHUYỂN HÓA LIPID: β-OXY HÓA ACID BÉO &amp; TỔNG HỢP THỂ CETON</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="165" y="30" fill="#fbbf24" font-size="14" font-weight="bold" text-anchor="middle">Con Thoi Carnitine &amp; Chu Trình β-Oxy Hóa</text>
    <rect x="15" y="50" width="300" height="60" fill="#334155" rx="6"/>
    <text x="165" y="72" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">CPT-I (Carnitine Palmitoyltransferase-1)</text>
    <text x="165" y="92" fill="#cbd5e1" font-size="10.5" text-anchor="middle">Đưa acyl-CoA vào ty thể | Bị ức chế bởi Malonyl-CoA</text>
    <rect x="15" y="118" width="300" height="75" fill="#334155" rx="6"/>
    <text x="165" y="138" fill="#4ade80" font-size="12" font-weight="bold" text-anchor="middle">4 Bước Chu Trình β-Oxy Hóa</text>
    <text x="165" y="156" fill="#e2e8f0" font-size="10.5" text-anchor="middle">1. Oxy hóa (FAD) -&gt; 2. Hợp nước (Hydrat hóa)</text>
    <text x="165" y="172" fill="#e2e8f0" font-size="10.5" text-anchor="middle">3. Oxy hóa (NAD+) -&gt; 4. Phân cắt Thiolase (CoA-SH)</text>
    <text x="165" y="188" fill="#fef08a" font-size="10" text-anchor="middle">Cắt 2C giải phóng: 1 Acetyl-CoA + 1 FADH2 + 1 NADH</text>
    <rect x="15" y="200" width="300" height="45" fill="#064e3b" rx="6"/>
    <text x="165" y="225" fill="#a7f3d0" font-size="11" font-weight="bold" text-anchor="middle">Hiệu suất Palmitat (16C): Thuần 106 ATP!</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#ec4899" stroke-width="1.5"/>
    <text x="170" y="30" fill="#f472b6" font-size="14" font-weight="bold" text-anchor="middle">Thể Ceton (Ketone Bodies) Tại Gan</text>
    <rect x="15" y="50" width="310" height="80" fill="#334155" rx="6"/>
    <text x="170" y="72" fill="#fca5a5" font-size="12" font-weight="bold" text-anchor="middle">3 Loại Thể Ceton</text>
    <text x="170" y="92" fill="#e2e8f0" font-size="11" text-anchor="middle">1. Acetoacetat (dạng đầu tiên hình thành)</text>
    <text x="170" y="110" fill="#e2e8f0" font-size="11" text-anchor="middle">2. β-hydroxybutyrat (dạng ưu thế trong máu)</text>
    <text x="170" y="126" fill="#e2e8f0" font-size="11" text-anchor="middle">3. Aceton (khí thở mùi trái cây chín)</text>
    <rect x="15" y="138" width="310" height="108" fill="#334155" rx="6"/>
    <text x="170" y="160" fill="#fef08a" font-size="12" font-weight="bold" text-anchor="middle">Cơ Chế &amp; Ý Nghĩa Lâm Sàng</text>
    <text x="170" y="180" fill="#e2e8f0" font-size="10.5" text-anchor="middle">• Gan tạo ra nhưng KHÔNG sử dụng được do thiếu thiophorase</text>
    <text x="170" y="200" fill="#e2e8f0" font-size="10.5" text-anchor="middle">• Mô ngoại vi (não khi nhịn đói, cơ, tim) đốt ceton thành năng lượng</text>
    <text x="170" y="225" fill="#f87171" font-size="10.5" font-weight="bold" text-anchor="middle">Nhiễm toan ceton ĐTĐ týp 1 (DKA): Thiếu Insulin tuyệt đối</text>
  </g>
</svg>''',

    'ch13_urea_cycle_ornithine.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#34d399" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">CHUYỂN HÓA PROTID: CHU TRÌNH URE &amp; ĐÀO THẢI AMONIAC</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#10b981" stroke-width="1.5"/>
    <text x="165" y="30" fill="#6ee7b7" font-size="14" font-weight="bold" text-anchor="middle">5 Phản Ứng Chu Trình Ure (Gan)</text>
    <rect x="15" y="50" width="300" height="55" fill="#064e3b" rx="6"/>
    <text x="165" y="72" fill="#fef08a" font-size="11" font-weight="bold" text-anchor="middle">1. CPS-I (Trong Ty Thể - Bước Giới Hạn Tốc Độ)</text>
    <text x="165" y="92" fill="#e2e8f0" font-size="10" text-anchor="middle">NH4+ + HCO3- + 2 ATP =&gt; Carbamoyl phosphat (N-acetylglutamat hoạt hóa)</text>
    <rect x="15" y="112" width="300" height="45" fill="#064e3b" rx="6"/>
    <text x="165" y="132" fill="#a7f3d0" font-size="11" font-weight="bold" text-anchor="middle">2. OTC: Ornithin + Carbamoyl-P =&gt; Citrullin (Ra bào tương)</text>
    <rect x="15" y="164" width="300" height="85" fill="#334155" rx="6"/>
    <text x="165" y="184" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">3-5. Phản ứng tại Bào tương</text>
    <text x="165" y="202" fill="#cbd5e1" font-size="10.5" text-anchor="middle">3. Citrullin + Aspartat =&gt; Argininosuccinat</text>
    <text x="165" y="220" fill="#cbd5e1" font-size="10.5" text-anchor="middle">4. Phân cắt ra Fumarat (nối vào chu trình Krebs)</text>
    <text x="165" y="238" fill="#fef08a" font-size="10.5" font-weight="bold" text-anchor="middle">5. Arginase: Arginin =&gt; Ure + Ornithin tái tạo</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#ef4444" stroke-width="1.5"/>
    <text x="170" y="30" fill="#f87171" font-size="14" font-weight="bold" text-anchor="middle">Nguồn Gốc 2 Nguyên Tử Nitơ Của Ure</text>
    <rect x="20" y="50" width="300" height="70" fill="#334155" rx="8"/>
    <text x="170" y="75" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Nitơ thứ nhất: Đến từ NH4+ tự do</text>
    <text x="170" y="98" fill="#f472b6" font-size="12" font-weight="bold" text-anchor="middle">Nitơ thứ hai: Đến từ Acid Aspartic (Aspartat)</text>
    <rect x="20" y="130" width="300" height="115" fill="#334155" rx="8"/>
    <text x="170" y="152" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">Tăng Amoniac Máu (Hyperammonemia)</text>
    <text x="170" y="172" fill="#e2e8f0" font-size="10.5" text-anchor="middle">• Bệnh não gan do xơ gan, suy gan cấp</text>
    <text x="170" y="190" fill="#e2e8f0" font-size="10.5" text-anchor="middle">• Đột biến enzym OTC (di truyền lặn NST X phổ biến nhất)</text>
    <text x="170" y="210" fill="#fca5a5" font-size="10.5" text-anchor="middle">• Độc tính thần kinh: NH3 cạn kiệt α-ketoglutarat &amp; Glutamat</text>
    <text x="170" y="230" fill="#fca5a5" font-size="10.5" text-anchor="middle">=&gt; Ức chế chu trình Krebs &amp; phù não cấp tính</text>
  </g>
</svg>''',

    'ch15_purine_uric_acid_gout.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#a855f7" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">THOÁI HÓA PURINE, ACID URIC &amp; CƠ CHẾ BỆNH GOUT</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#a855f7" stroke-width="1.5"/>
    <text x="165" y="30" fill="#c084fc" font-size="14" font-weight="bold" text-anchor="middle">Con Đường Thoái Hóa Purine</text>
    <rect x="15" y="50" width="300" height="45" fill="#334155" rx="6"/>
    <text x="165" y="75" fill="#e2e8f0" font-size="11" text-anchor="middle">AMP =&gt; Adenosine =&gt; Inosine =&gt; <tspan fill="#fef08a" font-weight="bold">Hypoxanthine</tspan></text>
    <text x="165" y="110" fill="#a855f7" font-size="16" text-anchor="middle">⬇ Xanthine Oxidase</text>
    <rect x="15" y="120" width="300" height="45" fill="#334155" rx="6"/>
    <text x="165" y="145" fill="#fef08a" font-size="13" font-weight="bold" text-anchor="middle">Xanthine</text>
    <text x="165" y="180" fill="#a855f7" font-size="16" text-anchor="middle">⬇ Xanthine Oxidase (Ức chế bởi Allopurinol / Febuxostat)</text>
    <rect x="15" y="190" width="300" height="55" fill="#581c87" rx="6"/>
    <text x="165" y="215" fill="#f87171" font-size="14" font-weight="bold" text-anchor="middle">ACID URIC (Sản phẩm thoái hóa cuối)</text>
    <text x="165" y="235" fill="#e9d5ff" font-size="10" text-anchor="middle">Con người thiếu men Uricase (Urate oxidase) =&gt; Không tan dễ dàng</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#ef4444" stroke-width="1.5"/>
    <text x="170" y="30" fill="#f87171" font-size="14" font-weight="bold" text-anchor="middle">Bệnh Khớp Gout &amp; Đột Biến HGPRT</text>
    <rect x="15" y="50" width="310" height="80" fill="#334155" rx="8"/>
    <text x="170" y="72" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">Cơ Chế Viêm Khớp Cấp Tính</text>
    <text x="170" y="92" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• Nồng độ Acid uric máu &gt; 420 µmol/L (7.0 mg/dL)</text>
    <text x="170" y="108" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• Lắng đọng tinh thể Monosodium Urate hình kim</text>
    <text x="170" y="124" fill="#fca5a5" font-size="10.5" text-anchor="middle">• Đại thực bào thực bào tinh thể =&gt; Phản ứng viêm dữ dội</text>
    <rect x="15" y="138" width="310" height="108" fill="#334155" rx="6"/>
    <text x="170" y="160" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Hội Chứng Lesch-Nyhan</text>
    <text x="170" y="180" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• Thiếu hụt hoàn toàn enzym cứu cánh HGPRT</text>
    <text x="170" y="198" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• Tăng vọt tổng hợp purine De Novo =&gt; Acid uric máu cực cao</text>
    <text x="170" y="216" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• Lâm sàng: Bệnh Gout trẻ em, múa vờn, thiểu năng trí tuệ</text>
    <text x="170" y="234" fill="#fca5a5" font-size="10.5" font-weight="bold" text-anchor="middle">Đặc trưng: Hành vi tự cắn xé môi và ngón tay!</text>
  </g>
</svg>''',

    'ch17_translation_ribosome.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#38bdf8" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">SINH TỔNG HỢP PROTEIN: RIBOSOME &amp; TÁC ĐỘNG KHÁNG SINH</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="165" y="30" fill="#7dd3fc" font-size="14" font-weight="bold" text-anchor="middle">3 Vị Trí Của Ribosome (A - P - E)</text>
    <rect x="15" y="50" width="90" height="80" fill="#047857" rx="6"/>
    <text x="60" y="80" fill="#6ee7b7" font-size="16" font-weight="bold" text-anchor="middle">Vị trí A</text>
    <text x="60" y="105" fill="#ecfdf5" font-size="10" text-anchor="middle">Aminoacyl-tRNA</text>
    <text x="60" y="120" fill="#ecfdf5" font-size="9" text-anchor="middle">Bắt codon mới</text>
    <rect x="120" y="50" width="90" height="80" fill="#1d4ed8" rx="6"/>
    <text x="165" y="80" fill="#93c5fd" font-size="16" font-weight="bold" text-anchor="middle">Vị trí P</text>
    <text x="165" y="105" fill="#eff6ff" font-size="10" text-anchor="middle">Peptidyl-tRNA</text>
    <text x="165" y="120" fill="#eff6ff" font-size="9" text-anchor="middle">Mang chuỗi peptid</text>
    <rect x="225" y="50" width="90" height="80" fill="#b91c1c" rx="6"/>
    <text x="270" y="80" fill="#fca5a5" font-size="16" font-weight="bold" text-anchor="middle">Vị trí E</text>
    <text x="270" y="105" fill="#fef2f2" font-size="10" text-anchor="middle">Exit site</text>
    <text x="270" y="120" fill="#fef2f2" font-size="9" text-anchor="middle">tRNA rời khỏi</text>
    <rect x="15" y="145" width="300" height="100" fill="#334155" rx="8"/>
    <text x="165" y="170" fill="#fef08a" font-size="12" font-weight="bold" text-anchor="middle">3 Giai Đoạn Dịch Mã</text>
    <text x="165" y="192" fill="#e2e8f0" font-size="11" text-anchor="middle">1. Khởi đầu: Codon AUG mã hóa Methionin (fMet)</text>
    <text x="165" y="212" fill="#e2e8f0" font-size="11" text-anchor="middle">2. Kéo dài: Peptidyl transferase hình thành liên kết peptid</text>
    <text x="165" y="232" fill="#e2e8f0" font-size="11" text-anchor="middle">3. Kết thúc: Mã kết thúc UAA, UAG, UGA (RF giải phóng)</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="170" y="30" fill="#fbbf24" font-size="14" font-weight="bold" text-anchor="middle">Cơ Chế Tác Động Của Kháng Sinh Lên Ribosome</text>
    <rect x="15" y="50" width="310" height="90" fill="#334155" rx="6"/>
    <text x="170" y="72" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">Ức Chế Tiểu Đơn Vị 30S Vi Khuẩn</text>
    <text x="170" y="92" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• <tspan fill="#7dd3fc" font-weight="bold">Aminoglycosid (Gentamicin, Streptomycin):</tspan> Đọc sai mã</text>
    <text x="170" y="110" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• <tspan fill="#7dd3fc" font-weight="bold">Tetracyclin (Doxycycline):</tspan> Khóa gắn aminoacyl-tRNA vào vị trí A</text>
    <text x="170" y="128" fill="#94a3b8" font-size="10" text-anchor="middle">Chọn lọc vi khuẩn, ít ảnh hưởng tế bào người (Ribosome 40S/60S)</text>
    <rect x="15" y="150" width="310" height="95" fill="#334155" rx="6"/>
    <text x="170" y="172" fill="#f472b6" font-size="12" font-weight="bold" text-anchor="middle">Ức Chế Tiểu Đơn Vị 50S Vi Khuẩn</text>
    <text x="170" y="192" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• <tspan fill="#f9a8d4" font-weight="bold">Chloramphenicol:</tspan> Ức chế Peptidyl transferase</text>
    <text x="170" y="210" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• <tspan fill="#f9a8d4" font-weight="bold">Macrolid (Erythromycin, Azithromycin):</tspan> Ngăn cản chuyển vị translocation</text>
    <text x="170" y="228" fill="#cbd5e1" font-size="10.5" text-anchor="middle">• <tspan fill="#f9a8d4" font-weight="bold">Clindamycin:</tspan> Ngăn tạo phức hợp khởi đầu chuỗi</text>
  </g>
</svg>''',

    'ch18_metabolic_regulation_hormones.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="100%" height="100%">
  <rect width="800" height="360" fill="#0f172a" rx="16"/>
  <text x="400" y="36" fill="#f59e0b" font-size="20" font-weight="bold" text-anchor="middle" font-family="sans-serif">ĐIỀU HÒA CHUYỂN HÓA: TRẠNG THÁI NO vs ĐÓI (INSULIN / GLUCAGON)</text>
  <g transform="translate(50, 65)">
    <rect width="330" height="260" fill="#1e293b" rx="12" stroke="#10b981" stroke-width="1.5"/>
    <text x="165" y="30" fill="#34d399" font-size="14" font-weight="bold" text-anchor="middle">Trạng Thái No (Well-Fed State)</text>
    <rect x="15" y="50" width="300" height="45" fill="#064e3b" rx="6"/>
    <text x="165" y="72" fill="#fef08a" font-size="13" font-weight="bold" text-anchor="middle">Tỷ lệ INSULIN / GLUCAGON Tăng Vọt</text>
    <rect x="15" y="105" width="300" height="140" fill="#334155" rx="8"/>
    <text x="165" y="128" fill="#6ee7b7" font-size="12" font-weight="bold" text-anchor="middle">Tăng Cường Các Con Đường Đồng Hóa</text>
    <text x="165" y="150" fill="#e2e8f0" font-size="11" text-anchor="middle">• Tăng thu nạp glucose vào cơ &amp; mô mỡ (GLUT4)</text>
    <text x="165" y="172" fill="#e2e8f0" font-size="11" text-anchor="middle">• Kích thích tổng hợp Glycogen (Glycogen synthase)</text>
    <text x="165" y="194" fill="#e2e8f0" font-size="11" text-anchor="middle">• Kích thích tổng hợp Triglycerid (Lipogenesis)</text>
    <text x="165" y="216" fill="#e2e8f0" font-size="11" text-anchor="middle">• Kích thích tổng hợp Protein &amp; Đường phân</text>
    <text x="165" y="235" fill="#fca5a5" font-size="10" text-anchor="middle">Ức chế: Tiêu glycogen, Tân tạo đường, β-oxy hóa</text>
  </g>
  <g transform="translate(410, 65)">
    <rect width="340" height="260" fill="#1e293b" rx="12" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="170" y="30" fill="#fbbf24" font-size="14" font-weight="bold" text-anchor="middle">Trạng Thái Đói &amp; Nhịn Đói Kéo Dài</text>
    <rect x="15" y="50" width="310" height="45" fill="#451a03" rx="6"/>
    <text x="170" y="72" fill="#f87171" font-size="13" font-weight="bold" text-anchor="middle">GLUCAGON &amp; EPINEPHRINE Chiếm Ưu Thế</text>
    <rect x="15" y="105" width="310" height="140" fill="#334155" rx="8"/>
    <text x="170" y="128" fill="#fde047" font-size="12" font-weight="bold" text-anchor="middle">Huy Động Năng Lượng Tối Đa</text>
    <text x="170" y="150" fill="#e2e8f0" font-size="11" text-anchor="middle">• Giai đoạn đầu (&lt;24h): Tiêu glycogen gan duy trì glucose</text>
    <text x="170" y="172" fill="#e2e8f0" font-size="11" text-anchor="middle">• Giai đoạn sau: Tân tạo đường (từ Alanin, Lactat, Glycerol)</text>
    <text x="170" y="194" fill="#e2e8f0" font-size="11" text-anchor="middle">• Ly giải mỡ (HSL): Phóng thích Acid béo tự do</text>
    <text x="170" y="216" fill="#e2e8f0" font-size="11" text-anchor="middle">• Tăng tạo Thể Ceton tại gan nuôi dưỡng Não &amp; Cơ</text>
    <text x="170" y="235" fill="#6ee7b7" font-size="10" text-anchor="middle">Tiết kiệm protein cơ tối đa trong nhịn đói kéo dài!</text>
  </g>
</svg>'''
}

for fname, content in svg_defs.items():
    p = os.path.join('static/uploads/hoasinh_yds', fname)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
print(f'Successfully wrote {len(svg_defs)} SVGs!')
