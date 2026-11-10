import os

html_path = r'static/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject survival-predictor-widget into view-dashboard right before "<!-- 4 Colorful Stat Cards -->"
survival_widget_html = '''
      <!-- ===================================================================
           UNIMASTER v15.0: SURVIVAL PREDICTOR & PANIC COUNTDOWN WIDGET
           =================================================================== -->
      <div id="survival-predictor-widget" class="uni-card p-5 relative overflow-hidden border-2 border-rose-500/50 bg-gradient-to-r from-rose-950/40 via-purple-950/30 to-slate-900/80 shadow-2xl">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div class="space-y-1.5">
            <div class="flex items-center gap-2">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-black uppercase tracking-wider bg-rose-500/20 text-rose-300 border border-rose-500/50 animate-pulse">
                <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                🚨 BÁO ĐỘNG ĐỎ KỲ THI
              </span>
              <span id="survival-quota-badge" class="badge-amber text-xs font-mono font-bold px-2.5 py-0.5 rounded-md">Quota hôm nay: 0 / 40 câu</span>
            </div>
            <h3 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
              <span>⏰</span> <span id="survival-urgent-title">OOP Thực Hành C# (15/11): Còn đúng 6 ngày!</span>
            </h3>
            <p class="text-xs text-slate-300 max-w-xl">
              Panic Meter tính toán áp lực rớt môn cho 5 mốc thi: OOP Thực hành (15/11), OOP Trắc nghiệm (26/11), Toán Rời Rạc (27/11), NNLT1 (1/12), AVCB 3 (4/12).
            </p>
          </div>

          <!-- Quick Action Buttons -->
          <div class="flex flex-wrap items-center gap-2 shrink-0">
            <button onclick="switchTab('exercises'); activateAntiCheat(true);" class="btn-primary !bg-gradient-to-r !from-rose-600 !to-amber-600 px-3.5 py-2 text-xs font-bold flex items-center gap-1.5 shadow-lg hover:scale-105 transition-all">
              <span>💻</span> Thi Code 60m (15/11)
            </button>
            <button onclick="switchTab('essay')" class="btn-soft px-3.5 py-2 text-xs font-bold flex items-center gap-1.5">
              <span>📝</span> Tự Luận Toán Rời Rạc
            </button>
            <button onclick="openBugHunterModal()" class="btn-soft px-3 py-2 text-xs font-bold flex items-center gap-1">
              <span>🎯</span> Săn Lỗi (20s)
            </button>
            <button onclick="openAlgoVisualizerModal()" class="btn-soft px-3 py-2 text-xs font-bold flex items-center gap-1">
              <span>📊</span> Mô Phỏng Thuật Toán
            </button>
            <button onclick="openBoilerplateTrainerModal()" class="btn-soft px-3 py-2 text-xs font-bold flex items-center gap-1">
              <span>⌨️</span> Gõ Class C# (&lt;2m)
            </button>
            <button onclick="openCheatSheetModal()" class="btn-soft px-3 py-2 text-xs font-bold flex items-center gap-1">
              <span>🖨️</span> Phao A4
            </button>
          </div>
        </div>

        <!-- 5-Exam Urgent Countdown Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5 pt-4 mt-3 border-t border-white/10 text-xs">
          <div class="p-2.5 rounded-xl border border-rose-500/40 bg-rose-500/15 space-y-0.5">
            <div class="flex items-center justify-between text-[10px] text-rose-300 font-bold">
              <span>15/11/2026</span>
              <span class="px-1.5 py-0.2 rounded bg-rose-500 text-white font-mono font-black">CỰC GẤP</span>
            </div>
            <div class="font-extrabold text-white text-xs truncate">OOP Thực hành C#</div>
            <div id="countdown-15-11" class="font-mono text-rose-400 font-black text-sm">6 ngày nữa</div>
          </div>

          <div class="p-2.5 rounded-xl border border-amber-500/30 bg-amber-500/10 space-y-0.5">
            <div class="flex items-center justify-between text-[10px] text-amber-300 font-bold">
              <span>26/11/2026</span>
              <span class="px-1.5 py-0.2 rounded bg-amber-500/30 text-amber-300 font-mono font-bold">17 NGÀY</span>
            </div>
            <div class="font-extrabold text-white text-xs truncate">OOP Trắc nghiệm & TH</div>
            <div id="countdown-26-11" class="font-mono text-amber-300 font-black text-sm">17 ngày nữa</div>
          </div>

          <div class="p-2.5 rounded-xl border border-indigo-500/30 bg-indigo-500/10 space-y-0.5">
            <div class="flex items-center justify-between text-[10px] text-indigo-300 font-bold">
              <span>27/11/2026</span>
              <span class="px-1.5 py-0.2 rounded bg-indigo-500/30 text-indigo-300 font-mono font-bold">18 NGÀY</span>
            </div>
            <div class="font-extrabold text-white text-xs truncate">Toán Rời Rạc & Giải Thuật</div>
            <div id="countdown-27-11" class="font-mono text-indigo-300 font-black text-sm">18 ngày nữa</div>
          </div>

          <div class="p-2.5 rounded-xl border border-cyan-500/30 bg-cyan-500/10 space-y-0.5">
            <div class="flex items-center justify-between text-[10px] text-cyan-300 font-bold">
              <span>01/12/2026</span>
              <span class="px-1.5 py-0.2 rounded bg-cyan-500/30 text-cyan-300 font-mono font-bold">22 NGÀY</span>
            </div>
            <div class="font-extrabold text-white text-xs truncate">NNLT 1 (Python)</div>
            <div id="countdown-01-12" class="font-mono text-cyan-300 font-black text-sm">22 ngày nữa</div>
          </div>

          <div class="p-2.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 space-y-0.5">
            <div class="flex items-center justify-between text-[10px] text-emerald-300 font-bold">
              <span>04/12/2026</span>
              <span class="px-1.5 py-0.2 rounded bg-emerald-500/30 text-emerald-300 font-mono font-bold">25 NGÀY</span>
            </div>
            <div class="font-extrabold text-white text-xs truncate">Anh Văn Cơ Bản 3</div>
            <div id="countdown-04-12" class="font-mono text-emerald-300 font-black text-sm">25 ngày nữa</div>
          </div>
        </div>
      </div>
'''

if 'id="survival-predictor-widget"' not in html:
    target_str = '<!-- 4 Colorful Stat Cards -->'
    if target_str in html:
        html = html.replace(target_str, survival_widget_html + '\n\n      ' + target_str)
        print("Injected survival-predictor-widget into Dashboard.")
    else:
        print("Target <!-- 4 Colorful Stat Cards --> not found!")
else:
    print("survival-predictor-widget already exists in HTML.")

# 2. Inject modal-boilerplate-trainer right before "<!-- ==================================================================="
boilerplate_modal_html = '''
  <!-- ===================================================================
       UNIMASTER v15.0: OOP BOILERPLATE SPEED TRAINER MODAL (< 2 PHÚT)
       =================================================================== -->
  <div id="modal-boilerplate-trainer" class="fixed inset-0 z-50 flex items-center justify-center p-3 bg-black/80 backdrop-blur-sm hidden animate-fade-in">
    <div class="uni-card w-full max-w-2xl max-h-[92vh] flex flex-col p-5 sm:p-6 space-y-4 shadow-2xl border border-violet-500/40">
      <div class="flex items-center justify-between border-b pb-3" style="border-color: var(--border);">
        <div class="flex items-center gap-2">
          <span class="text-xl">⌨️</span>
          <div>
            <h3 class="text-base font-extrabold text-white">OOP Boilerplate Speed Trainer (Luyện Gõ C# &lt; 2 Phút)</h3>
            <p class="text-xs text-slate-400">Rèn phản xạ gõ khung Class C#, Encapsulation, Constructor, Property</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span id="boilerplate-timer" class="px-3 py-1 rounded-lg font-mono font-black text-sm bg-amber-500/20 text-amber-400 border border-amber-500/40">120s</span>
          <button onclick="closeBoilerplateTrainerModal()" class="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-white/10 text-slate-400 hover:text-white">✕</button>
        </div>
      </div>

      <div class="space-y-2">
        <div class="p-3 rounded-xl bg-violet-950/30 border border-violet-500/30 text-xs text-slate-200">
          <div class="font-bold text-violet-300 mb-1">📋 Đề Bài Luyện Tốc Độ:</div>
          <div id="boilerplate-prompt-text" class="font-mono text-xs">
            Hãy khai báo một class `Student` có thuộc tính `Id` (int, getter/private setter), `FullName` (string, getter/setter), constructor nhận vào 2 tham số, và một phương thức `public void DisplayInfo()` in ra màn hình.
          </div>
        </div>

        <div class="flex items-center justify-between text-xs font-mono font-bold text-slate-400 px-1">
          <span id="boilerplate-wpm">Tốc độ: 0 WPM</span>
          <span id="boilerplate-accuracy">Trạng thái cú pháp: Đang chờ</span>
        </div>

        <textarea id="boilerplate-editor" oninput="onBoilerplateInput()"
          rows="10" placeholder="// Bắt đầu gõ code C# tại đây...
public class Student {
    public int Id { get; private set; }
    public string FullName { get; set; }
    public Student(int id, string fullName) {
        Id = id;
        FullName = fullName;
    }
    public void DisplayInfo() {
        Console.WriteLine($&quot;{Id} - {FullName}&quot;);
    }
}"
          class="uni-input w-full p-3 font-mono text-xs bg-slate-950 text-cyan-300 leading-relaxed border border-slate-700 rounded-xl focus:border-cyan-400"></textarea>

        <div id="boilerplate-feedback-box" class="hidden p-3 rounded-xl text-xs font-mono"></div>
      </div>

      <div class="flex items-center justify-between pt-2 border-t" style="border-color: var(--border);">
        <button onclick="startNewBoilerplateDrill()" class="btn-soft px-3 py-1.5 text-xs font-bold">🔄 Đổi Bài Mới</button>
        <div class="flex items-center gap-2">
          <button onclick="validateBoilerplateCode()" class="btn-primary px-4 py-2 text-xs font-bold shadow-md">
            <span>⚡</span> Kiểm Tra Cú Pháp & WPM
          </button>
        </div>
      </div>
    </div>
  </div>
'''

if 'id="modal-boilerplate-trainer"' not in html:
    target_lock = '<!-- ===================================================================\n       ANTI-CHEAT FULLSCREEN LOCK OVERLAY'
    if target_lock in html:
        html = html.replace(target_lock, boilerplate_modal_html + '\n  ' + target_lock)
        print("Injected modal-boilerplate-trainer before Anti-Cheat overlay.")
    else:
        # try without exact indentation
        idx = html.find('id="anti-cheat-lock-overlay"')
        if idx != -1:
            div_start = html.rfind('<div', 0, idx)
            html = html[:div_start] + boilerplate_modal_html + '\n  ' + html[div_start:]
            print("Injected modal-boilerplate-trainer before anti-cheat-lock-overlay.")
else:
    print("modal-boilerplate-trainer already exists.")

# 3. Upgrade Flashcards Rating Buttons to 4 SM-2 buttons if needed
fc_3_buttons = '''        <div class="grid grid-cols-3 gap-3">
          <button onclick="rateFlashcard(1)" class="uni-card uni-card-interactive p-3 text-center">
            <div class="text-xs font-extrabold txt-rose">1. Chưa thuộc</div>
          </button>
          <button onclick="rateFlashcard(2)" class="uni-card uni-card-interactive p-3 text-center">
            <div class="text-xs font-extrabold txt-amber">2. Tạm nhớ</div>
          </button>
          <button onclick="rateFlashcard(3)" class="uni-card uni-card-interactive p-3 text-center">
            <div class="text-xs font-extrabold txt-emerald">3. Thuộc lòng</div>
          </button>
        </div>'''

fc_sm2_buttons = '''        <!-- SM-2 4 Spaced Repetition Buttons -->
        <div id="fc-sm2-meta-stats" class="text-center font-mono text-[11px] text-slate-400">Ease: 2.50 • Khoảng cách: 1 ngày • Lặp lại: 0 lần</div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <button onclick="rateFlashcardSM2('again')" class="uni-card uni-card-interactive p-3 text-center border border-rose-500/30 hover:border-rose-500 bg-rose-500/10">
            <div class="text-xs font-black text-rose-400">1. Quên (Again)</div>
            <div class="text-[10px] text-slate-400 font-mono mt-0.5">&lt; 1 ngày • Reset</div>
          </button>
          <button onclick="rateFlashcardSM2('hard')" class="uni-card uni-card-interactive p-3 text-center border border-amber-500/30 hover:border-amber-500 bg-amber-500/10">
            <div class="text-xs font-black text-amber-400">2. Khó (Hard)</div>
            <div class="text-[10px] text-slate-400 font-mono mt-0.5">Khoảng cách × 1.2</div>
          </button>
          <button onclick="rateFlashcardSM2('good')" class="uni-card uni-card-interactive p-3 text-center border border-emerald-500/30 hover:border-emerald-500 bg-emerald-500/10">
            <div class="text-xs font-black text-emerald-400">3. Tốt (Good)</div>
            <div class="text-[10px] text-slate-400 font-mono mt-0.5">Khoảng cách chuẩn</div>
          </button>
          <button onclick="rateFlashcardSM2('easy')" class="uni-card uni-card-interactive p-3 text-center border border-cyan-500/30 hover:border-cyan-500 bg-cyan-500/10">
            <div class="text-xs font-black text-cyan-400">4. Dễ (Easy)</div>
            <div class="text-[10px] text-slate-400 font-mono mt-0.5">Khoảng cách × Ease</div>
          </button>
        </div>'''

if fc_3_buttons in html:
    html = html.replace(fc_3_buttons, fc_sm2_buttons)
    print("Replaced 3 flashcard buttons with 4 SM-2 buttons.")
else:
    print("Flashcard 3 buttons target not found or already replaced.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated static/index.html successfully.")
