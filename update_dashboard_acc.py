app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

target = '''    grid.innerHTML = STATE.subjects
      .map((s, idx) => {'''

replacement = '''    const activeAcc = typeof getActiveAccount === 'function' ? getActiveAccount() : null;
    const enrolledIds = activeAcc && Array.isArray(activeAcc.enrolled_subjects) ? activeAcc.enrolled_subjects : [];

    let displaySubjects = [...STATE.subjects];
    if (enrolledIds.length > 0) {
      displaySubjects.sort((a, b) => {
        const aEn = enrolledIds.includes(a.id) ? 1 : 0;
        const bEn = enrolledIds.includes(b.id) ? 1 : 0;
        return bEn - aEn;
      });
    }

    grid.innerHTML = displaySubjects
      .map((s, idx) => {
        const isEnrolled = enrolledIds.includes(s.id);'''

if target in js:
    js = js.replace(target, replacement, 1)
    
    # Also add the enrolled badge inside the card
    card_badge_target = '${s.code === \'OOP_CSHARP\' ? \'<span class="badge-brand px-1.5 py-0.2 rounded text-[10px] font-extrabold">💻 CNTT Pro</span>\' : s.code === \'HOASINH_CTUMP\' ? \'<span class="badge-emerald px-1.5 py-0.2 rounded text-[10px] font-extrabold">🔬 Y Khoa</span>\' : s.question_count > 100 ? \'<span class="badge-amber px-1.5 py-0.2 rounded text-[10px] font-extrabold">⭐ Trọng Tâm</span>\' : \'\'}'
    card_badge_replacement = '${isEnrolled ? \'<span class="badge-brand px-1.5 py-0.2 rounded text-[10px] font-black border border-indigo-500/40">★ Môn Của Acc</span>\' : \'\'} ' + card_badge_target
    
    if card_badge_target in js:
        js = js.replace(card_badge_target, card_badge_replacement, 1)
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Updated renderDashboard with account subject prioritization!")
else:
    print("Target not found in renderDashboard")
