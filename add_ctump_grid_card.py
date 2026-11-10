with open('static/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

target = """  const grid = document.getElementById('exam-parts-grid');
  if (grid) {
    let html = '';
    const bai4Questions = allQs.filter((q) => q.topic_tag && q.topic_tag.startsWith('Bài 4'));"""

replacement = """  const grid = document.getElementById('exam-parts-grid');
  if (grid) {
    let html = '';
    const isCtump = (STATE.subjects.find((s) => s.id === sid)?.code || '') === 'HOASINH_CTUMP';
    if (isCtump) {
      html += `
        <div class="col-span-full p-3 rounded-2xl border border-indigo-500/40 bg-indigo-500/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-1 shadow-sm">
          <div class="flex items-center gap-2.5">
            <span class="text-2xl">🏛️</span>
            <div>
              <div class="font-black text-xs text-indigo-300 flex items-center gap-1.5">
                Trọn Bộ 322 Câu Hóa Sinh CTUMP Gốc (Chuẩn Giáo Trình)
              </div>
              <div class="text-[11px] txt-muted">Đã chia 5 phần: An toàn PTN, Protein/Biuret, Thận, Enzym/Lipid & Nước tiểu</div>
            </div>
          </div>
          <button type="button" onclick="openCtumpOriginalPartsModal()" class="btn-primary !bg-indigo-600 hover:!bg-indigo-700 px-3.5 py-1.5 text-xs font-black shadow-sm shrink-0">
            Xem 5 Phần Gốc ↗
          </button>
        </div>
      `;
    }
    const bai4Questions = allQs.filter((q) => q.topic_tag && q.topic_tag.startsWith('Bài 4'));"""

assert target in c, "target not found"
c = c.replace(target, replacement, 1)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("Added CTUMP 322 parts card to exam-parts-grid!")
