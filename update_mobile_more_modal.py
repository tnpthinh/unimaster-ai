with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_grid = '''      <div class="grid grid-cols-2 gap-2.5">
        <button onclick="switchTab('arena'); closeModal('modal-mobile-more');" class="btn-soft p-3.5 rounded-xl flex flex-col items-center justify-center gap-1.5 text-center">
          <span class="text-2xl">🏆</span>
          <span class="text-xs font-bold txt-main">Đấu Trường</span>
          <span class="text-[10px] txt-muted">Quiz Battle Live</span>
        </button>'''

enhanced_grid = '''      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 max-h-[70vh] overflow-y-auto pr-1">
        <button onclick="switchTab('exercises'); closeModal('modal-mobile-more'); activateAntiCheat(true);" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center border-rose-500/30 hover:border-rose-500">
          <span class="text-xl">💻</span>
          <span class="text-xs font-extrabold text-rose-300">Thi Code 60m</span>
          <span class="text-[10px] txt-muted">OOP C# &amp; Python</span>
        </button>
        <button onclick="switchTab('essay'); closeModal('modal-mobile-more');" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center border-amber-500/30 hover:border-amber-500">
          <span class="text-xl">📝</span>
          <span class="text-xs font-extrabold text-amber-300">Bảng Tự Luận</span>
          <span class="text-[10px] txt-muted">Toán Rời Rạc &amp; GT</span>
        </button>
        <button onclick="openBugHunterModal(); closeModal('modal-mobile-more');" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center border-violet-500/30 hover:border-violet-500">
          <span class="text-xl">🎯</span>
          <span class="text-xs font-extrabold text-violet-300">Săn Lỗi (20s)</span>
          <span class="text-[10px] txt-muted">Minigame Bắt Bug</span>
        </button>
        <button onclick="openAlgoVisualizerModal(); closeModal('modal-mobile-more');" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center border-cyan-500/30 hover:border-cyan-500">
          <span class="text-xl">📊</span>
          <span class="text-xs font-extrabold text-cyan-300">Mô Phỏng GT</span>
          <span class="text-[10px] txt-muted">Sort &amp; Search Visual</span>
        </button>
        <button onclick="openBoilerplateTrainerModal(); closeModal('modal-mobile-more');" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center border-emerald-500/30 hover:border-emerald-500">
          <span class="text-xl">⌨️</span>
          <span class="text-xs font-extrabold text-emerald-300">Gõ Class C#</span>
          <span class="text-[10px] txt-muted">&lt; 2 Phút + WPM</span>
        </button>
        <button onclick="openCheatSheetModal(); closeModal('modal-mobile-more');" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center border-indigo-500/30 hover:border-indigo-500">
          <span class="text-xl">🖨️</span>
          <span class="text-xs font-extrabold text-indigo-300">Phao In A4</span>
          <span class="text-[10px] txt-muted">Tổng Ôn Phút Chót</span>
        </button>
        <button onclick="switchTab('arena'); closeModal('modal-mobile-more');" class="btn-soft p-3 rounded-xl flex flex-col items-center justify-center gap-1 text-center">
          <span class="text-xl">🏆</span>
          <span class="text-xs font-bold txt-main">Đấu Trường</span>
          <span class="text-[10px] txt-muted">Quiz Battle Live</span>
        </button>'''

if target_grid in html:
    html = html.replace(target_grid, enhanced_grid, 1)
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Enhanced modal-mobile-more with all 6 quick exam tools.")
else:
    print("Target grid not found in index.html.")
