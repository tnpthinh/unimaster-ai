import re

app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

v20_code = '''
// =========================================================================
// UNIMASTER v20: MULTI-ACCOUNT MANAGEMENT & SUBJECT ENROLLMENT PER ACCOUNT
// =========================================================================
const LOCAL_ACCOUNTS_KEY = 'unimaster_accounts_v2';
const LOCAL_ACTIVE_ACCOUNT_ID_KEY = 'unimaster_active_account_id_v2';

function getInitialAccounts() {
  return [
    {
      id: 'acc_y_khoa',
      name: 'Sinh Viên Y Khoa (CTUMP)',
      username: 'ykhoa_ctump',
      role: 'student',
      avatar: '🩺',
      enrolled_subjects: [10], // HOASINH_CTUMP
      theme: 'midnight',
      brand: '#7c3aed',
      created_at: '2026-11-01'
    },
    {
      id: 'acc_cntt',
      name: 'Sinh Viên CNTT & Lập Trình',
      username: 'cntt_dev',
      role: 'student',
      avatar: '💻',
      enrolled_subjects: [3, 4, 5, 8], // OOP, Python, Algorithms, Discrete Math
      theme: 'dark',
      brand: '#2563eb',
      created_at: '2026-11-02'
    },
    {
      id: 'acc_admin',
      name: 'Quản Trị Viên (Admin)',
      username: 'admin',
      role: 'admin',
      avatar: '👑',
      enrolled_subjects: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      theme: 'dark',
      brand: '#7c3aed',
      created_at: '2026-11-01'
    }
  ];
}

function getAllLocalAccounts() {
  try {
    const raw = localStorage.getItem(LOCAL_ACCOUNTS_KEY);
    if (!raw) {
      const init = getInitialAccounts();
      localStorage.setItem(LOCAL_ACCOUNTS_KEY, JSON.stringify(init));
      return init;
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : getInitialAccounts();
  } catch (_) {
    return getInitialAccounts();
  }
}

function saveAllLocalAccounts(list) {
  try {
    localStorage.setItem(LOCAL_ACCOUNTS_KEY, JSON.stringify(list || []));
  } catch (_) {}
}

function getActiveAccountId() {
  return localStorage.getItem(LOCAL_ACTIVE_ACCOUNT_ID_KEY) || 'acc_y_khoa';
}

function getActiveAccount() {
  const list = getAllLocalAccounts();
  const aid = getActiveAccountId();
  return list.find((a) => a.id === aid) || list[0];
}

function switchActiveAccount(accountId) {
  const list = getAllLocalAccounts();
  const acc = list.find((a) => a.id === accountId);
  if (!acc) return;

  localStorage.setItem(LOCAL_ACTIVE_ACCOUNT_ID_KEY, accountId);
  STATE.currentUser = acc;

  // Apply theme if stored
  if (acc.theme && typeof setThemeMode === 'function') {
    setThemeMode(acc.theme);
  }
  if (acc.brand && typeof setAccentPalette === 'function') {
    setAccentPalette(acc.brand, acc.brand);
  }

  updateHeaderUserPill();
  renderAccountsListUI();
  filterDashboardByEnrolledSubjects();

  // If user has enrolled subjects, set active subject to their first subject
  if (Array.isArray(acc.enrolled_subjects) && acc.enrolled_subjects.length > 0) {
    const sub = STATE.subjects.find((s) => s.id === acc.enrolled_subjects[0]);
    if (sub && typeof selectActiveSubject === 'function') {
      selectActiveSubject(sub.id);
    }
  }

  playSound('success');
  showToast(`🎉 Đã chuyển sang tài khoản: ${acc.name}!`, 'success');
}

function renderAccountsListUI() {
  const container = document.getElementById('acc-cards-container');
  if (!container) return;

  const list = getAllLocalAccounts();
  const activeId = getActiveAccountId();
  const activeAcc = getActiveAccount();

  // Update enrolled summary on card
  const summaryEl = document.getElementById('acc-active-enrolled-summary');
  if (summaryEl && activeAcc) {
    const enrolledIds = activeAcc.enrolled_subjects || [];
    if (!enrolledIds.length || enrolledIds.length === STATE.subjects.length) {
      summaryEl.textContent = 'Đang học: Toàn bộ 12 môn';
    } else {
      const names = STATE.subjects.filter((s) => enrolledIds.includes(s.id)).map((s) => s.name);
      summaryEl.textContent = `Đang học ${enrolledIds.length} môn: ${names.slice(0, 2).join(', ')}${names.length > 2 ? '...' : ''}`;
    }
  }

  container.innerHTML = list
    .map((acc) => {
      const isActive = acc.id === activeId;
      const enrolledIds = acc.enrolled_subjects || [];
      const subNames = STATE.subjects
        .filter((s) => enrolledIds.includes(s.id))
        .map((s) => `<span class="badge-subtle text-[10px] px-1.5 py-0.2 rounded font-sans font-bold">${s.icon || '📘'} ${escapeHtml(s.name.split('(')[0].trim())}</span>`)
        .slice(0, 3)
        .join(' ');

      return `
      <div class="acc-card ${isActive ? 'is-active' : ''} p-3.5 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl flex items-center justify-center text-xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 shrink-0">
            ${acc.avatar || '🎓'}
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-extrabold text-xs sm:text-sm txt-main">${escapeHtml(acc.name)}</span>
              ${isActive ? '<span class="badge-brand px-2 py-0.5 rounded-full text-[10px] font-bold">✓ Đang dùng</span>' : ''}
              ${acc.role === 'admin' ? '<span class="badge-rose px-1.5 py-0.2 rounded text-[10px] font-black">Admin</span>' : ''}
            </div>
            <div class="flex flex-wrap items-center gap-1 mt-1">
              ${subNames || '<span class="text-[10px] txt-muted italic">Chưa chọn môn học</span>'}
            </div>
          </div>
        </div>

        <div class="flex items-center gap-2 w-full sm:w-auto justify-end shrink-0">
          <button type="button" onclick="openAccountSubjectPickerModal('${acc.id}')" title="Chọn môn học cho tài khoản này" class="btn-soft px-2.5 py-1.5 text-xs font-bold text-indigo-400 hover:text-indigo-300">
            <span>📚</span> <span class="hidden sm:inline">Chọn môn</span>
          </button>
          ${!isActive ? `
            <button type="button" onclick="switchActiveAccount('${acc.id}')" class="btn-primary !bg-indigo-600 hover:!bg-indigo-500 px-3 py-1.5 text-xs font-black shadow-sm">
              Đổi sang Acc này
            </button>
          ` : `
            <span class="text-xs text-emerald-400 font-extrabold px-2">● Đang hoạt động</span>
          `}
        </div>
      </div>
    `;
    })
    .join('');
}

function promptCreateNewAccount() {
  const name = prompt('Nhập tên tài khoản học tập mới (VD: Sinh viên Y Dược, Ôn thi CNTT, Tài khoản 2...):');
  if (!name || !name.trim()) return;

  const list = getAllLocalAccounts();
  const emojis = ['🩺', '💻', '🔬', '📚', '⚡', '🦉', '🎨', '🚀', '🧠', '💊'];
  const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];

  const newAcc = {
    id: 'acc_' + Date.now(),
    name: name.trim(),
    username: name.trim().toLowerCase().replace(/[^a-z0-9]/g, '_').slice(0, 15) || 'user',
    role: 'student',
    avatar: randomEmoji,
    enrolled_subjects: [10], // Default to first CTUMP
    theme: 'midnight',
    brand: '#7c3aed',
    created_at: new Date().toISOString()
  };

  list.push(newAcc);
  saveAllLocalAccounts(list);
  switchActiveAccount(newAcc.id);

  // Immediately ask which subjects this account wants to study!
  setTimeout(() => {
    openAccountSubjectPickerModal(newAcc.id);
  }, 200);
}

// Target account being configured in Subject Enrollment Modal
let currentConfiguringAccountId = null;
let tempSelectedSubjectIds = new Set();

function openAccountSubjectPickerModal(accountId = null) {
  const targetId = accountId || getActiveAccountId();
  currentConfiguringAccountId = targetId;

  const list = getAllLocalAccounts();
  const acc = list.find((a) => a.id === targetId) || getActiveAccount();
  if (!acc) return;

  tempSelectedSubjectIds = new Set(acc.enrolled_subjects || []);
  setText('acc-subj-modal-user-name', acc.name);

  renderAccountSubjectCheckboxes();
  openModal('modal-account-subjects');
  playSound('click');
}

function renderAccountSubjectCheckboxes() {
  const grid = document.getElementById('acc-subjects-checkbox-grid');
  if (!grid) return;

  const allSubjects = STATE.subjects || [];
  setText('acc-subj-total-count', allSubjects.length);
  setText('acc-subj-selected-count', tempSelectedSubjectIds.size);

  grid.innerHTML = allSubjects
    .map((s) => {
      const isChecked = tempSelectedSubjectIds.has(s.id);
      return `
      <div onclick="toggleSubjectCheckbox(${s.id})" class="subj-checkbox-card ${isChecked ? 'selected' : ''} p-3 rounded-2xl flex items-center justify-between gap-3">
        <div class="flex items-center gap-2.5 overflow-hidden">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center text-lg bg-white/5 border border-white/10 shrink-0">
            ${s.icon || '📘'}
          </div>
          <div class="overflow-hidden">
            <div class="text-xs font-black txt-main truncate">${escapeHtml(s.name)}</div>
            <div class="text-[10px] txt-muted flex items-center gap-1.5 mt-0.5">
              <span class="badge-brand px-1.5 py-0.2 rounded font-mono">${s.question_count || 0} câu</span>
              <span>•</span>
              <span class="truncate">${escapeHtml(s.category || 'Học phần')}</span>
            </div>
          </div>
        </div>
        <div class="w-6 h-6 rounded-lg border-2 flex items-center justify-center shrink-0 transition-all ${isChecked ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-500 bg-transparent'}">
          ${isChecked ? '<span class="text-xs font-black">✓</span>' : ''}
        </div>
      </div>
    `;
    })
    .join('');
}

function toggleSubjectCheckbox(subjectId) {
  if (tempSelectedSubjectIds.has(subjectId)) {
    tempSelectedSubjectIds.delete(subjectId);
  } else {
    tempSelectedSubjectIds.add(subjectId);
  }
  renderAccountSubjectCheckboxes();
  playSound('click');
}

function selectSubjectPreset(presetType) {
  tempSelectedSubjectIds.clear();
  const all = STATE.subjects || [];

  if (presetType === 'medical') {
    all.filter((s) => s.code === 'HOASINH_CTUMP' || (s.category && s.category.includes('Y')) || s.name.includes('Hóa Sinh')).forEach((s) => tempSelectedSubjectIds.add(s.id));
  } else if (presetType === 'it') {
    all.filter((s) => ['OOP_CSHARP', 'NNLT1', 'CTDL_GT', 'TOAN_RR'].includes(s.code) || s.category === 'Công nghệ thông tin' || s.name.includes('Lập trình')).forEach((s) => tempSelectedSubjectIds.add(s.id));
  } else if (presetType === 'general') {
    all.filter((s) => ['MLN101', 'CNXHKH', 'AVCB3'].includes(s.code) || s.category === 'Lý luận chính trị' || s.category === 'Ngoại ngữ').forEach((s) => tempSelectedSubjectIds.add(s.id));
  }
  renderAccountSubjectCheckboxes();
  playSound('click');
}

function selectAllSubjects(shouldSelectAll) {
  tempSelectedSubjectIds.clear();
  if (shouldSelectAll) {
    (STATE.subjects || []).forEach((s) => tempSelectedSubjectIds.add(s.id));
  }
  renderAccountSubjectCheckboxes();
  playSound('click');
}

function saveAccountEnrolledSubjects() {
  if (!currentConfiguringAccountId) currentConfiguringAccountId = getActiveAccountId();
  const list = getAllLocalAccounts();
  const acc = list.find((a) => a.id === currentConfiguringAccountId);
  if (!acc) return;

  const chosen = Array.from(tempSelectedSubjectIds);
  if (!chosen.length) {
    showToast('Vui lòng chọn ít nhất 1 môn học cho tài khoản!', 'warning');
    return;
  }

  acc.enrolled_subjects = chosen;
  saveAllLocalAccounts(list);

  if (acc.id === getActiveAccountId()) {
    STATE.currentUser = acc;
    filterDashboardByEnrolledSubjects();
  }

  renderAccountsListUI();
  closeModal('modal-account-subjects');
  playSound('success');
  showToast(`✅ Đã lưu ${chosen.length} môn học cho tài khoản: ${acc.name}!`, 'success');
}

function filterDashboardByEnrolledSubjects() {
  const acc = getActiveAccount();
  if (!acc || !Array.isArray(acc.enrolled_subjects) || !acc.enrolled_subjects.length) return;

  // Highlight or sort enrolled subjects first in subject select and dashboard grid
  if (typeof renderDashboard === 'function') {
    renderDashboard();
  }
}

// =========================================================================
// DEEP COLOR CUSTOMIZER STUDIO & FULLSCREEN
// =========================================================================
function setCustomStageBg(colorHex) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.customBg = colorHex;
  const root = document.documentElement;
  
  if (colorHex) {
    root.style.setProperty('--bg-surface', colorHex);
    root.style.setProperty('--bg-card', colorHex);
    const lbl = document.getElementById('lbl-custom-bg');
    if (lbl) lbl.textContent = colorHex;
  }
  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function setOptionColorMode(mode) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.optColorMode = mode;
  const root = document.documentElement;

  ['rainbow', 'uniform', 'contrast'].forEach((m) => {
    const btn = document.getElementById(`opt-style-${m}`);
    if (btn) btn.classList.toggle('border-indigo-500/80', m === mode);
  });

  if (mode === 'rainbow') {
    root.style.setProperty('--opt-a-accent', '#8b5cf6');
    root.style.setProperty('--opt-b-accent', '#3b82f6');
    root.style.setProperty('--opt-c-accent', '#10b981');
    root.style.setProperty('--opt-d-accent', '#f59e0b');
  } else if (mode === 'uniform') {
    const brand = STATE.ui.brand || '#7c3aed';
    root.style.setProperty('--opt-a-accent', brand);
    root.style.setProperty('--opt-b-accent', brand);
    root.style.setProperty('--opt-c-accent', brand);
    root.style.setProperty('--opt-d-accent', brand);
  } else if (mode === 'contrast') {
    root.style.setProperty('--opt-a-accent', '#ffffff');
    root.style.setProperty('--opt-b-accent', '#ffffff');
    root.style.setProperty('--opt-c-accent', '#ffffff');
    root.style.setProperty('--opt-d-accent', '#ffffff');
  }

  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function setFeedbackCustomColor(type, hex) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  const root = document.documentElement;

  if (type === 'correct') {
    STATE.ui.correctColor = hex;
    root.style.setProperty('--emerald-border', hex);
    root.style.setProperty('--emerald-bg', hex + '22');
  } else if (type === 'wrong') {
    STATE.ui.wrongColor = hex;
    root.style.setProperty('--rose-border', hex);
    root.style.setProperty('--rose-bg', hex + '22');
  }

  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
}

function setQuestionTextColor(colorHex) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.customQTextColor = colorHex;
  const root = document.documentElement;

  root.style.setProperty('--custom-q-text-color', colorHex || 'var(--text-main)');
  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function setGlobalZoomScale(percent) {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  STATE.ui.zoomScale = percent;
  const root = document.documentElement;

  const basePx = (16 * (percent / 100)).toFixed(1);
  root.style.setProperty('--base-font-size', `${basePx}px`);

  document.querySelectorAll('.zoom-pill').forEach((el) => {
    el.classList.toggle('active', el.textContent.includes(`${percent}%`));
  });

  try {
    localStorage.setItem('unimaster_ui_prefs', JSON.stringify(STATE.ui));
  } catch (_) {}
  playSound('click');
}

function resetDeepColorCustomization() {
  if (!STATE.ui) STATE.ui = { ...DEFAULT_UI_PREFS };
  delete STATE.ui.customBg;
  delete STATE.ui.optColorMode;
  delete STATE.ui.correctColor;
  delete STATE.ui.wrongColor;
  delete STATE.ui.customQTextColor;
  delete STATE.ui.zoomScale;

  const root = document.documentElement;
  root.style.removeProperty('--bg-surface');
  root.style.removeProperty('--bg-card');
  root.style.removeProperty('--opt-a-accent');
  root.style.removeProperty('--opt-b-accent');
  root.style.removeProperty('--opt-c-accent');
  root.style.removeProperty('--opt-d-accent');
  root.style.removeProperty('--emerald-border');
  root.style.removeProperty('--emerald-bg');
  root.style.removeProperty('--rose-border');
  root.style.removeProperty('--rose-bg');
  root.style.removeProperty('--custom-q-text-color');
  root.style.removeProperty('--base-font-size');

  applyAllAppearancePrefs();
  playSound('success');
  showToast('Đã khôi phục cài đặt màu sắc & giao diện về mặc định!', 'info');
}

// =========================================================================
// FULLSCREEN DISTRACTION-FREE TOGGLE (TRÁNH VƯỚNG TAB TRÌNH DUYỆT)
// =========================================================================
function toggleAppFullscreen() {
  const isFs = Boolean(
    document.fullscreenElement ||
    document.webkitFullscreenElement ||
    document.mozFullScreenElement ||
    document.msFullscreenElement
  );

  if (!isFs) {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen().catch(() => {});
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    }
    document.body.classList.add('app-fullscreen-mode');
    updateFullscreenUI(true);
    showToast('📺 Đã bật Toàn Màn Hình (Không vướng tab trình duyệt)!', 'success');
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
    document.body.classList.remove('app-fullscreen-mode');
    updateFullscreenUI(false);
    showToast('🗗 Đã thu nhỏ màn hình.', 'info');
  }
}

function updateFullscreenUI(isFs) {
  const lbl = document.getElementById('header-fs-label');
  const heroLbl = document.getElementById('hero-fs-label');
  const heroIcon = document.getElementById('hero-fs-icon');
  const fsBtn = document.getElementById('header-fullscreen-btn');

  if (lbl) lbl.textContent = isFs ? 'Thu Nhỏ' : 'Toàn Màn Hình';
  if (heroLbl) heroLbl.textContent = isFs ? 'Thu Nhỏ Màn Hình' : 'Toàn Màn Hình Không Vướng Tab';
  if (heroIcon) heroIcon.textContent = isFs ? '🗗' : '⛶';
  if (fsBtn) fsBtn.classList.toggle('active', isFs);
}

document.addEventListener('fullscreenchange', () => {
  const isFs = Boolean(document.fullscreenElement);
  document.body.classList.toggle('app-fullscreen-mode', isFs);
  updateFullscreenUI(isFs);
});
document.addEventListener('webkitfullscreenchange', () => {
  const isFs = Boolean(document.webkitFullscreenElement);
  document.body.classList.toggle('app-fullscreen-mode', isFs);
  updateFullscreenUI(isFs);
});
'''

# 1. Update openAccountModal to default to 'switch' tab
open_acc_old = '''function openAccountModal() {
  const modal = document.getElementById('modal-account-profile');
  if (!modal) return;
  
  const user = STATE.currentUser || { id: 1, full_name: 'Quản Trị Viên (Admin)', username: 'admin', role: 'admin' };
  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

  setEl('acc-modal-fullname', user.full_name || user.username);
  setEl('acc-modal-username', `@${user.username}`);
  setEl('acc-modal-role', user.role === 'admin' ? '👑 Quản Trị Viên Tối Cao' : '🎓 Sinh Viên');
  setEl('acc-modal-exams-count', `${STATE.stats?.total_exams || 0} bài`);
  setEl('acc-modal-mistakes-count', `${STATE.mistakes?.length || 0} câu`);
  setEl('acc-modal-streak', `${STATE.streak || 1} ngày 🔥`);

  // Show/Hide Admin Tab based on role
  const adminTabBtn = document.getElementById('acc-tab-admin-btn');
  if (adminTabBtn) {
    adminTabBtn.classList.toggle('hidden', user.role !== 'admin');
  }

  switchAccountTab('profile');
  openModal('modal-account-profile');
  playSound('click');
}'''

open_acc_new = '''function openAccountModal() {
  const modal = document.getElementById('modal-account-profile');
  if (!modal) return;

  const activeAcc = getActiveAccount();
  STATE.currentUser = activeAcc;

  const user = activeAcc || { id: 1, name: 'Quản Trị Viên (Admin)', username: 'admin', role: 'admin' };
  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

  setEl('acc-modal-fullname', user.name || user.full_name || user.username);
  setEl('acc-modal-username', `@${user.username}`);
  setEl('acc-modal-role', user.role === 'admin' ? '👑 Quản Trị Viên Tối Cao' : '🎓 Sinh Viên');
  setEl('acc-modal-exams-count', `${STATE.stats?.total_exams || 0} bài`);
  setEl('acc-modal-mistakes-count', `${STATE.mistakes?.length || 0} câu`);
  setEl('acc-modal-streak', `${STATE.streak || 1} ngày 🔥`);

  const adminTabBtn = document.getElementById('acc-tab-admin-btn');
  if (adminTabBtn) {
    adminTabBtn.classList.toggle('hidden', user.role !== 'admin');
  }

  switchAccountTab('switch');
  renderAccountsListUI();
  openModal('modal-account-profile');
  playSound('click');
}'''

if open_acc_old in js:
    js = js.replace(open_acc_old, open_acc_new, 1)
    print("1. Updated openAccountModal to default to switch tab")

# 2. Update switchAccountTab to support 'switch' tab
switch_acc_old = '''function switchAccountTab(tab) {
  document.getElementById('acc-panel-profile')?.classList.toggle('hidden', tab !== 'profile');
  document.getElementById('acc-panel-admin')?.classList.toggle('hidden', tab !== 'admin');
  document.getElementById('acc-tab-profile-btn')?.classList.toggle('active', tab === 'profile');
  document.getElementById('acc-tab-admin-btn')?.classList.toggle('active', tab === 'admin');

  if (tab === 'admin') loadAdminUsersList();
}'''

switch_acc_new = '''function switchAccountTab(tab) {
  document.getElementById('acc-panel-switch')?.classList.toggle('hidden', tab !== 'switch');
  document.getElementById('acc-panel-profile')?.classList.toggle('hidden', tab !== 'profile');
  document.getElementById('acc-panel-admin')?.classList.toggle('hidden', tab !== 'admin');

  document.getElementById('acc-tab-switch-btn')?.classList.toggle('active', tab === 'switch');
  document.getElementById('acc-tab-profile-btn')?.classList.toggle('active', tab === 'profile');
  document.getElementById('acc-tab-admin-btn')?.classList.toggle('active', tab === 'admin');

  if (tab === 'switch') renderAccountsListUI();
  if (tab === 'admin') loadAdminUsersList();
}'''

if switch_acc_old in js:
    js = js.replace(switch_acc_old, switch_acc_new, 1)
    print("2. Updated switchAccountTab to support 'switch' tab")

# 3. Update updateHeaderUserPill to reflect active account avatar and name
update_pill_old = '''function updateHeaderUserPill() {
  const pill = document.getElementById('header-user-btn');
  const avatar = document.getElementById('header-user-avatar');
  const nameEl = document.getElementById('header-user-name');
  const roleEl = document.getElementById('header-user-role');

  if (!pill) return;
  const user = STATE.currentUser || { full_name: 'Quản Trị Viên', role: 'admin', username: 'admin' };
  
  if (nameEl) nameEl.textContent = user.full_name || user.username;
  if (roleEl) {
    if (user.role === 'admin') {
      roleEl.textContent = '👑 Quản Trị';
      roleEl.className = 'badge-rose px-1.5 py-0.5 rounded text-[10px] font-black';
    } else {
      roleEl.textContent = '🎓 Sinh Viên';
      roleEl.className = 'badge-brand px-1.5 py-0.5 rounded text-[10px] font-black text-emerald-400';
    }
  }
}'''

update_pill_new = '''function updateHeaderUserPill() {
  const pill = document.getElementById('header-user-btn');
  const avatar = document.getElementById('header-user-avatar');
  const nameEl = document.getElementById('header-user-name');
  const roleEl = document.getElementById('header-user-role');

  if (!pill) return;
  const user = getActiveAccount() || STATE.currentUser || { name: 'Quản Trị Viên', role: 'admin', username: 'admin' };

  if (nameEl) nameEl.textContent = user.name || user.full_name || user.username;
  if (avatar && user.avatar) avatar.textContent = user.avatar;
  if (roleEl) {
    if (user.role === 'admin') {
      roleEl.textContent = '👑 Quản Trị';
      roleEl.className = 'badge-rose px-1.5 py-0.5 rounded text-[10px] font-black';
    } else {
      roleEl.textContent = '🎓 Sinh Viên';
      roleEl.className = 'badge-brand px-1.5 py-0.5 rounded text-[10px] font-black text-emerald-400';
    }
  }
}'''

if update_pill_old in js:
    js = js.replace(update_pill_old, update_pill_new, 1)
    print("3. Updated updateHeaderUserPill to reflect active account")

# 4. Update applyAllAppearancePrefs to support customBg, optColorMode, customQTextColor
apply_prefs_target = '''  root.style.setProperty('--card-radius', `${u.cardRadiusPx || 18}px`);'''
apply_prefs_expansion = '''  root.style.setProperty('--card-radius', `${u.cardRadiusPx || 18}px`);

  // Deep Color Customization application
  if (u.customBg) {
    root.style.setProperty('--bg-surface', u.customBg);
    root.style.setProperty('--bg-card', u.customBg);
  }
  if (u.customQTextColor) {
    root.style.setProperty('--custom-q-text-color', u.customQTextColor);
  }
  if (u.optColorMode) {
    setOptionColorMode(u.optColorMode);
  }
  if (u.correctColor) {
    root.style.setProperty('--emerald-border', u.correctColor);
    root.style.setProperty('--emerald-bg', u.correctColor + '22');
  }
  if (u.wrongColor) {
    root.style.setProperty('--rose-border', u.wrongColor);
    root.style.setProperty('--rose-bg', u.wrongColor + '22');
  }
  if (u.zoomScale) {
    const basePx = (16 * (u.zoomScale / 100)).toFixed(1);
    root.style.setProperty('--base-font-size', `${basePx}px`);
  }'''

if apply_prefs_target in js and 'Deep Color Customization application' not in js:
    js = js.replace(apply_prefs_target, apply_prefs_expansion, 1)
    print("4. Added Deep Color hooks to applyAllAppearancePrefs")

# Append v20_code
if 'UNIMASTER v20: MULTI-ACCOUNT' not in js:
    js += '\n' + v20_code
    print("5. Appended v20 multi-account and deep customizer functions")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Done updating static/app.js for v20!")
