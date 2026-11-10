import os

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
INDEX_PATH = os.path.join(BASE_DIR, "static", "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

modal_bai4_html = """  <!-- ===================================================================
       MODAL: BÀI 4 HÓA SINH - 200 CÂU LIPID & NƯỚC TIỂU 10 THÔNG SỐ (CHIA 7 PHẦN)
       =================================================================== -->
  <div id="modal-bai4-parts" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/85 backdrop-blur-sm hidden animate-fade-in">
    <div class="uni-card w-full max-w-3xl max-h-[92vh] flex flex-col p-5 sm:p-6 space-y-4 shadow-2xl border border-rose-500/30 overflow-hidden">
      <!-- Modal Header -->
      <div class="flex items-center justify-between border-b pb-3.5" style="border-color: var(--border);">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-xl font-bold shadow-inner border border-rose-500/30">
            🫀
          </div>
          <div>
            <h3 class="text-base sm:text-lg font-black txt-main">Bài 4: 200 Câu Chuyển Hóa Lipid & Nước Tiểu 10 Thông Số</h3>
            <p class="text-xs txt-muted font-medium">Giáo trình Thực Hành Hóa Sinh CTUMP • Xóa bỏ thiên kiến độ dài (Anti-Length Bias 99%)</p>
          </div>
        </div>
        <button onclick="closeModal('modal-bai4-parts')" class="btn-soft p-2 text-xs rounded-xl"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>

      <!-- Quick Action: Luyện tất cả 200 câu -->
      <div class="p-3.5 sm:p-4 rounded-2xl bg-gradient-to-r from-rose-500/15 via-pink-500/10 to-transparent border border-rose-500/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-md">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="badge-brand text-[11px] font-bold px-2 py-0.5 rounded-full">Trọn Bộ 200 Câu</span>
            <span class="text-xs text-emerald-400 font-bold">✓ 50A : 50B : 50C : 50D cân bằng 25%</span>
          </div>
          <p class="text-xs txt-sub font-semibold">Luyện toàn diện 7 chuyên đề hoặc thi thử mô phỏng tính giờ 60 phút.</p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid();" class="btn-primary !bg-gradient-to-r !from-rose-500 !to-pink-600 px-4 py-2 text-xs font-bold shadow-lg hover:scale-105 transition-all">
            ⚡ Luyện Toàn Bộ 200 Câu
          </button>
          <button onclick="closeModal('modal-bai4-parts'); startTimedExamForBai4Lipid();" class="btn-soft px-3.5 py-2 text-xs font-bold border border-rose-500/40 hover:bg-rose-500/20">
            ⏱️ Thi Thử 60 Phút
          </button>
        </div>
      </div>

      <!-- Sub-Lessons List: 7 Parts -->
      <div class="overflow-y-auto pr-1 space-y-2.5 max-h-[52vh]">
        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-1">Chọn chuyên đề bài học để ôn riêng:</div>

        <!-- Part 1: Cholesterol -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 1: Định lượng Cholesterol toàn phần (CHE-CHO-POD)</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-rose-500/20 text-rose-300 border border-rose-500/30">30 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Cơ chế CHE, CHO, POD; phức Quinoneimine hồng 500nm; tuyến tính 750 mg/dL; pha loãng 1:2 nhân 3</p>
          </div>
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid(1);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 30 câu →
          </button>
        </div>

        <!-- Part 2: Triglycerid -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 2: Định lượng Triglycerid huyết thanh (LPL-GK-GPO-POD)</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-amber-500/20 text-amber-300 border border-amber-500/30">30 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Good's buffer pH 7.2; phức hồng 505nm; tuyến tính 1062 mg/dL; biến chứng viêm tụy cấp khi > 11 mmol/L</p>
          </div>
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid(2);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 30 câu →
          </button>
        </div>

        <!-- Part 3: HDL-C, LDL-C & Friedewald -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 3: Định lượng HDL-C, LDL-C & Công thức Friedewald</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">30 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">R1 (PVS/PEGME) đo xanh tím 578nm; Catalase tiêu H2O2; Công thức Friedewald LDL = TC - HDL - TG/5</p>
          </div>
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid(3);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 30 câu →
          </button>
        </div>

        <!-- Part 4: The Ceton nuoc tieu -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 4: Phản ứng tìm Thể Ceton nước tiểu (Legal / Rothera)</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-purple-500/20 text-purple-300 border border-purple-500/30">25 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Sodium nitroprussiat 10% tạo vòng tím với NH4OH đđ nghiêng 45°; 3 thể ceton; toan ceton ĐTĐ, nhịn đói</p>
          </div>
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid(4);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 25 câu →
          </button>
        </div>

        <!-- Part 5: Cybow 3 -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 5: Que nhúng nước tiểu 3 thông số (Cybow 3: pH, Glu, Pro)</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-blue-500/20 text-blue-300 border border-blue-500/30">25 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Nhúng 2s đọc sau 60s (sau 2p mất chính xác); âm tính giả Vitamin C; dương tính giả Javel/kiềm; bảo quản không để tủ lạnh</p>
          </div>
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid(5);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 25 câu →
          </button>
        </div>

        <!-- Part 6: May 10 thong so -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 6: Máy phân tích nước tiểu 10 thông số (Vận hành & Kỹ thuật)</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">30 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Quang phổ phản xạ 3 bóng đèn; quy trình 8 bước bấm nút xanh ngón tay trái; 10 giây; lỗi Strip problem-retest; không ly tâm</p>
          </div>
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid(6);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 30 câu →
          </button>
        </div>

        <!-- Part 7: Nguyen ly 10 thong so -->
        <div class="p-3.5 rounded-xl border bg-slate-900/60 hover:bg-slate-800/60 transition-all flex items-center justify-between gap-3" style="border-color: var(--border);">
          <div class="space-y-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-extrabold text-sm txt-main">Phần 7: Nguyên lý 10 thông số nước tiểu & Độ nhạy lâm sàng</span>
              <span class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-teal-500/20 text-teal-300 border border-teal-500/30">30 câu</span>
            </div>
            <p class="text-xs txt-muted truncate">Bạch cầu (esterase -> indoxyl tím 5-15 tb/µL); Nitrite (hồng đỏ vi khuẩn); Máu (peroxidase Hb); Bilirubin (diazotized)</p>
          </div>
          <button onclick="closeModal('modal-bai4-parts'); quickStartBai4Lipid(7);" class="btn-primary px-3.5 py-1.5 text-xs font-bold shrink-0">
            Luyện 30 câu →
          </button>
        </div>
      </div>

      <!-- Footer Info -->
      <div class="pt-2 border-t flex items-center justify-between text-[11px] txt-muted" style="border-color: var(--border);">
        <span>💡 Tỉ lệ đáp án dài nhất chỉ 1.0% — Triệt tiêu hoàn toàn thói quen đoán độ dài!</span>
        <button onclick="closeModal('modal-bai4-parts')" class="btn-soft px-3 py-1 text-xs">Đóng</button>
      </div>
    </div>
  </div>\n\n"""

target = "<!-- ===================================================================\n       ANTI-CHEAT FULLSCREEN LOCK OVERLAY"
target_crlf = "<!-- ===================================================================\r\n       ANTI-CHEAT FULLSCREEN LOCK OVERLAY"

if "modal-bai4-parts" not in content:
    if target in content:
        content = content.replace(target, modal_bai4_html + target)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("Injected modal-bai4-parts into index.html (LF target)")
    elif target_crlf in content:
        content = content.replace(target_crlf, modal_bai4_html + target_crlf)
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("Injected modal-bai4-parts into index.html (CRLF target)")
    else:
        print("Could not find target in index.html")
else:
    print("modal-bai4-parts already present")
