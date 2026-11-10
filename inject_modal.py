import os

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
INDEX_PATH = os.path.join(BASE_DIR, "static", "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target = "<!-- ===================================================================\n       ANTI-CHEAT FULLSCREEN LOCK OVERLAY"
target_crlf = "<!-- ===================================================================\r\n       ANTI-CHEAT FULLSCREEN LOCK OVERLAY"

modal_html = """  <!-- ===================================================================
       MODAL: BÀI 3 HÓA SINH - 200 CÂU GLUCID & ĐÁI THÁO ĐƯỜNG (CHIA 6 BÀI)
       =================================================================== -->
  <div id="modal-bai3-parts" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/85 backdrop-blur-sm hidden animate-fade-in">
    <div class="uni-card w-full max-w-3xl max-h-[92vh] flex flex-col p-5 sm:p-6 space-y-4 shadow-2xl border border-amber-500/30 overflow-hidden">
      <!-- Modal Header -->
      <div class="flex items-center justify-between border-b pb-3.5" style="border-color: var(--border);">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-xl font-bold shadow-inner border border-amber-500/30">
            🍬
          </div>
          <div>
            <h3 class="text-base sm:text-lg font-black txt-main">Bài 3: 200 Câu Glucid & Biện Luận Đái Tháo Đường</h3>
            <p class="text-xs txt-muted font-medium">Giáo trình Thực Hành Hóa Sinh CTUMP • Chuẩn hóa độ dài 4 đáp án (Anti-Length Bias)</p>
          </div>
        </div>
        <button onclick="closeModal('modal-bai3-parts')" class="btn-soft p-2 text-xs rounded-xl"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>

      <!-- Quick Action: Luyện tất cả 200 câu -->
      <div class="p-3.5 sm:p-4 rounded-2xl bg-gradient-to-r from-amber-500/15 via-orange-500/10 to-transparent border border-amber-500/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-md">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="badge-brand text-[11px] font-bold px-2 py-0.5 rounded-full">Trọn Bộ 200 Câu</span>
            <span class="text-xs text-emerald-400 font-bold">✓ 50A : 50B : 50C : 50D cân bằng 25%</span>
          </div>
          <p class="text-xs txt-sub font-semibold">Luyện toàn diện 6 chuyên đề hoặc thi thử mô phỏng 60 phút.</p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <button onclick="closeModal('modal-bai3-parts'); quickStartBai3Glucid();" class="btn-primary !bg-gradient-to-r !from-amber-500 !to-orange-500 px-4 py-2 text-xs font-bold shadow-lg hover:scale-105 transition-all">
            ⚡ Luyện Toàn Bộ 200 Câu
          </button>
          <button onclick="closeModal('modal-bai3-parts'); startTimedExamForBai3Glucid();" class="btn-soft px-3.5 py-2 text-xs font-bold border border-amber-500/40 hover:bg-amber-500/20">
            ⏱️ Thi Thử 60 Phút
          </button>
        </div>
      </div>

      <!-- Sub-Lessons List: 6 Parts -->
      <div class="overflow-y-auto pr-1 space-y-2.5 max-h-[52vh]">
        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-1">Chọn chuyên đề bài học để ôn riêng:</div>

        <!-- Part 1: Molish -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 1: Phản ứng Molish & Đại cương Glucid</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">25 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Cơ chế H2SO4 đđ tạo Furfural/HMF, vòng ngưng tụ α-naphtol tím, phân biệt chất hữu cơ/vô cơ</p>
          </div>
          <button onclick="closeModal('modal-bai3-parts'); quickStartBai3Glucid(1);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 25 câu →
          </button>
        </div>

        <!-- Part 2: Fehling -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 2: Phản ứng Fehling & Tính khử của đường</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-rose-500/20 text-rose-300 border border-rose-500/30">35 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Dạng enediol khử Cu2+ thành Cu2O đỏ gạch, Fehling A (CuSO4) & B (NaOH + Seignette), tính khử mono/disaccharid</p>
          </div>
          <button onclick="closeModal('modal-bai3-parts'); quickStartBai3Glucid(2);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 35 câu →
          </button>
        </div>

        <!-- Part 3: Polysaccharid & Iod -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 3: Phản ứng màu của Polysaccharid với Iod</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-blue-500/20 text-blue-300 border border-blue-500/30">25 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Cấu trúc xoắn helix amylose hấp phụ I2 xanh tím, đun nóng mất màu và để nguội hồi phục, màu đỏ nâu glycogen</p>
          </div>
          <button onclick="closeModal('modal-bai3-parts'); quickStartBai3Glucid(3);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 25 câu →
          </button>
        </div>

        <!-- Part 4: GOD-POD -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 4: Định lượng Glucose huyết tương (GOD-POD / Trinder)</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">45 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Kỹ thuật Trinder, bước sóng 500nm, chuẩn 11 mmol/L (180 mg/dL), ức chế đường phân NaF, nhiễu Bilirubin/Lipid</p>
          </div>
          <button onclick="closeModal('modal-bai3-parts'); quickStartBai3Glucid(4);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 45 câu →
          </button>
        </div>

        <!-- Part 5: Clinical OGTT -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 5: Biện luận Sinh hóa Đái tháo đường & Nghiệm pháp OGTT</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-amber-500/20 text-amber-300 border border-amber-500/30">35 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Trị số 75-115 mg/dL, tiêu chuẩn ADA chẩn đoán ĐTĐ đói ≥ 7.0 mmol/L, OGTT 75g (2h: 7.8-11.1), ngưỡng thận 180 mg/dL</p>
          </div>
          <button onclick="closeModal('modal-bai3-parts'); quickStartBai3Glucid(5);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 35 câu →
          </button>
        </div>

        <!-- Part 6: Benedict -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 6: Phản ứng Benedict & Tìm đường niệu bán định lượng</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-teal-500/20 text-teal-300 border border-teal-500/30">35 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Kiềm yếu Na2CO3 + Natri citrat, đun 1ml Benedict + 2 giọt nước tiểu 3 phút, thang bán định lượng (+ đến ++++)</p>
          </div>
          <button onclick="closeModal('modal-bai3-parts'); quickStartBai3Glucid(6);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 35 câu →
          </button>
        </div>
      </div>

      <!-- Footer Info -->
      <div class="pt-2 border-t flex items-center justify-between text-[11px] txt-muted" style="border-color: var(--border);">
        <span>💡 Tỉ lệ đáp án dài nhất chỉ 19% — Cân bằng tuyệt đối 50A : 50B : 50C : 50D!</span>
        <button onclick="closeModal('modal-bai3-parts')" class="btn-soft px-3 py-1 text-xs">Đóng</button>
      </div>
    </div>
  </div>\n\n"""

if "modal-bai3-parts" not in content:
    if target in content:
        content = content.replace(target, modal_html + target)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("Injected modal into index.html (LF target)")
    elif target_crlf in content:
        content = content.replace(target_crlf, modal_html + target_crlf)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("Injected modal into index.html (CRLF target)")
    else:
        print("Target anti-cheat not found!")
else:
    print("modal-bai3-parts already present in index.html")
