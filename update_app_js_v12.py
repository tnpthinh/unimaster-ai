# -*- coding: utf-8 -*-
"""
UniMaster AI Pro v12.0 — Update static/app.js:
1. Define renderAcademicText and renderInlineMathAndCode (fixes Spectro, OSCE, and Handwritten grader errors).
2. Fix switchLabSubTab to correctly initialize Spectro cuvettes and OSCE stations.
3. Add multi-account authentication, profile sync, and admin user management functions.
4. Add global Active Subject Selector and contextual subject-centric filtering across the entire app.
"""

import os
import re

APP_JS_PATH = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js"

with open(APP_JS_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add definitions for renderAcademicText and renderInlineMathAndCode near formatRichText
render_funcs = """
// Academic Text & Math rendering helpers
function renderAcademicText(text) {
  if (!text) return '';
  if (typeof renderMarkdown === 'function') return renderMarkdown(text);
  if (typeof formatRichText === 'function') return formatRichText(text);
  return escapeHtml(String(text));
}

function renderInlineMathAndCode(text) {
  if (!text) return '';
  if (typeof formatRichText === 'function') return formatRichText(text);
  if (typeof renderMarkdown === 'function') return renderMarkdown(text);
  return escapeHtml(String(text));
}
"""

if "function renderAcademicText" not in code:
    code = render_funcs + "\n" + code

# 2. Update switchLabSubTab
old_switch_lab = """function switchLabSubTab(subKey) {
  const subs = ['spectro', 'osce', 'handwritten', 'graph', 'calc', 'patient', 'dosing', 'biostat', 'export'];
  subs.forEach((k) => {
    document.getElementById(`lab-sub-${k}`)?.classList.toggle('hidden', k !== subKey);
  });
  document.querySelectorAll('[data-labtab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-labtab') === subKey);
  });
  if (subKey === 'graph') renderInteractiveKnowledgeGraph();
  if (subKey === 'calc') runClinicalCalculators();
  if (subKey === 'patient') initVirtualPatientView();
  if (subKey === 'dosing') runRenalDoseCalculation();
  if (subKey === 'biostat') runBiostatCalculations();
  if (subKey === 'export') initExportView();
  playSound('click');
}"""

new_switch_lab = """function switchLabSubTab(subKey) {
  const subs = ['spectro', 'osce', 'handwritten', 'graph', 'calc', 'patient', 'dosing', 'biostat', 'export'];
  subs.forEach((k) => {
    document.getElementById(`lab-sub-${k}`)?.classList.toggle('hidden', k !== subKey);
  });
  document.querySelectorAll('[data-labtab]').forEach((btn) => {
    btn.classList.toggle('active', btn.getAttribute('data-labtab') === subKey);
  });
  if (subKey === 'spectro') {
    if (!currentSpectroState.initialized) {
      currentSpectroState.initialized = true;
      randomizeSpectroCase();
    } else {
      updateSpectroDisplay();
    }
  }
  if (subKey === 'osce') {
    renderOsceStationStrip();
    if (osceState.active) {
      renderOsceStation();
    }
  }
  if (subKey === 'graph') renderInteractiveKnowledgeGraph();
  if (subKey === 'calc') runClinicalCalculators();
  if (subKey === 'patient') initVirtualPatientView();
  if (subKey === 'dosing') runRenalDoseCalculation();
  if (subKey === 'biostat') runBiostatCalculations();
  if (subKey === 'export') initExportView();
  playSound('click');
}"""

code = code.replace(old_switch_lab, new_switch_lab)

# 3. Fix submitHandwrittenForGrading null-safety
old_hw_submit = """async function submitHandwrittenForGrading() {
  if (!currentHandwrittenDataUrl) {
    showToast('Vui lòng chụp ảnh hoặc bấm Tạo phiếu bài làm viết tay mẫu trước!', 'warning');
    return;
  }
  const box = document.getElementById('hw-grading-result');
  const btn = document.getElementById('hw-grade-btn');
  if (btn) btn.disabled = true;
  if (box) {
    box.innerHTML = `<div class="py-10 text-center txt-brand font-extrabold animate-pulse">🔍 Gemini Vision đang đọc chữ viết tay, kiểm tra từng phép tính và đơn vị đo...</div>`;
  }

  const sub = STATE.subjects.find((s) => String(s.id) === String(STATE.examConfig.subjectId)) || STATE.subjects[0];
  const qText = document.getElementById('hw-question-context')?.value || 'Chấm bài giải tự luận / phiếu thực hành viết tay';
  const note = document.getElementById('hw-student-note')?.value || '';

  const res = await apiFetch('/api/ai/grade-handwritten', {
    method: 'POST',
    body: JSON.stringify({
      subject_name: sub?.name || 'Thực Hành Hóa Sinh',
      question_text: qText,
      student_note: note,
      image_base64: currentHandwrittenDataUrl,
      mime_type: currentHandwrittenMime
    })
  });
  if (btn) btn.disabled = false;

  const g = res.grading || {"""

new_hw_submit = """async function submitHandwrittenForGrading() {
  if (!currentHandwrittenDataUrl) {
    showToast('Vui lòng chụp ảnh hoặc bấm Tạo phiếu bài làm viết tay mẫu trước!', 'warning');
    return;
  }
  const box = document.getElementById('hw-grading-result');
  const btn = document.getElementById('hw-grade-btn');
  if (btn) btn.disabled = true;
  if (box) {
    box.innerHTML = `<div class="py-10 text-center txt-brand font-extrabold animate-pulse">🔍 Gemini Vision đang đọc chữ viết tay, kiểm tra từng phép tính và đơn vị đo...</div>`;
  }

  const sub = STATE.subjects.find((s) => String(s.id) === String(STATE.examConfig.subjectId)) || STATE.subjects[0];
  const qText = document.getElementById('hw-question-context')?.value || 'Chấm bài giải tự luận / phiếu thực hành viết tay';
  const note = document.getElementById('hw-student-note')?.value || '';

  let res = null;
  try {
    res = await apiFetch('/api/ai/grade-handwritten', {
      method: 'POST',
      body: JSON.stringify({
        subject_name: sub?.name || 'Thực Hành Hóa Sinh',
        question_text: qText,
        student_note: note,
        image_base64: currentHandwrittenDataUrl,
        mime_type: currentHandwrittenMime
      })
    });
  } catch (e) {
    console.warn('Lỗi gọi API grade-handwritten:', e);
  }

  if (btn) btn.disabled = false;

  const g = (res && res.grading) ? res.grading : {"""

code = code.replace(old_hw_submit, new_hw_submit)

# 4. Append v12.0 Client Engine: Active Subject Bar + Multi-account System + History Sync
v12_extension = """
// ============================================================================
// UNIMASTER AI PRO v12.0 — SUBJECT-CENTRIC FLOW & USER ACCOUNT SYSTEM
// ============================================================================

STATE.currentUser = null;
STATE.activeSubjectId = null;

// --- 1. USER ACCOUNT & AUTH STATUS ---
async function fetchCurrentUserProfile() {
  try {
    const res = await apiFetch('/api/auth/me');
    if (res && res.success && res.user) {
      STATE.currentUser = res.user;
      updateHeaderUserPill();
      // If user has preferred subject in state, load it
      await syncUserStateFromServer();
    }
  } catch (err) {
    console.warn('Chưa đăng nhập hoặc chạy nội bộ:', err);
  }
}

function updateHeaderUserPill() {
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
  if (avatar) {
    avatar.textContent = (user.full_name || user.username || 'U')[0].toUpperCase();
  }
}

function openAccountModal() {
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
}

function switchAccountTab(tab) {
  document.getElementById('acc-panel-profile')?.classList.toggle('hidden', tab !== 'profile');
  document.getElementById('acc-panel-admin')?.classList.toggle('hidden', tab !== 'admin');
  document.getElementById('acc-tab-profile-btn')?.classList.toggle('active', tab === 'profile');
  document.getElementById('acc-tab-admin-btn')?.classList.toggle('active', tab === 'admin');

  if (tab === 'admin') loadAdminUsersList();
}

async function loadAdminUsersList() {
  const listEl = document.getElementById('acc-admin-users-list');
  if (!listEl) return;
  listEl.innerHTML = '<div class="py-6 text-center txt-muted text-xs">Đang tải danh sách tài khoản...</div>';

  try {
    const res = await apiFetch('/api/admin/users');
    if (res && res.success && res.users) {
      if (res.users.length === 0) {
        listEl.innerHTML = '<div class="py-6 text-center txt-muted text-xs">Chưa có tài khoản sinh viên nào đăng ký.</div>';
        return;
      }

      listEl.innerHTML = res.users.map(u => `
        <div class="uni-card p-3.5 flex items-center justify-between text-xs">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-black ${u.role === 'admin' ? 'bg-rose-500/20 text-rose-400' : 'bg-emerald-500/20 text-emerald-400'}">
              ${(u.full_name || u.username)[0].toUpperCase()}
            </div>
            <div>
              <div class="font-extrabold txt-main flex items-center gap-1.5">
                <span>${escapeHtml(u.full_name || u.username)}</span>
                <span class="${u.role === 'admin' ? 'badge-rose' : 'badge-soft'} px-1.5 py-0.2 rounded text-[10px]">${u.role}</span>
              </div>
              <div class="text-[11px] txt-muted font-mono">@${u.username} • Đã thi ${u.exam_count || 0} bài • Điểm TB: ${u.avg_score ? Number(u.avg_score).toFixed(1) : '--'}</div>
            </div>
          </div>
          <div>
            ${u.role !== 'admin' ? `
              <button type="button" onclick="deleteUserAccount(${u.id}, '${escapeHtml(u.username)}')" class="btn-soft px-2.5 py-1 text-rose-400 hover:bg-rose-500/20 text-[11px] font-bold">
                Xóa
              </button>
            ` : '<span class="text-[11px] text-amber-400 font-bold">Chủ sở hữu</span>'}
          </div>
        </div>
      `).join('');
    } else {
      listEl.innerHTML = `<div class="py-4 text-center text-rose-400 text-xs">${res?.error || 'Không thể tải danh sách'}</div>`;
    }
  } catch (err) {
    listEl.innerHTML = `<div class="py-4 text-center text-rose-400 text-xs">Lỗi: ${err.message}</div>`;
  }
}

async function deleteUserAccount(uid, uname) {
  if (!confirm(`Bạn có chắc chắn muốn xóa tài khoản sinh viên "@${uname}" không? Mọi dữ liệu làm bài của sinh viên này sẽ bị xóa vĩnh viễn.`)) return;

  try {
    const res = await apiFetch(`/api/admin/users/${uid}`, { method: 'DELETE' });
    if (res && res.success) {
      showToast(`Đã xóa tài khoản @${uname}!`, 'success');
      loadAdminUsersList();
    } else {
      showToast(res?.error || 'Không thể xóa', 'error');
    }
  } catch (err) {
    showToast('Lỗi xóa: ' + err.message, 'error');
  }
}

async function handleLogout() {
  try {
    await fetch('/api/auth/logout', { method: 'POST' });
  } catch (_) {}
  showToast('Đang đăng xuất...', 'info');
  setTimeout(() => { window.location.href = '/login'; }, 300);
}


// --- 2. ACTIVE SUBJECT SELECTOR & CONTEXTUAL FILTERING ---
function initActiveSubjectBar() {
  const preferred =
    STATE.subjects.find((s) => s.code === 'HOASINH_CTUMP') ||
    STATE.subjects.find((s) => s.code === 'OOP_CSHARP') ||
    STATE.subjects[0];

  const savedSubId = localStorage.getItem('unimaster_active_subject_id');
  const matched = STATE.subjects.find((s) => String(s.id) === String(savedSubId));
  const active = matched || preferred;

  if (active) {
    selectActiveSubject(active.id, false);
  }
}

function openSubjectPickerModal() {
  const listEl = document.getElementById('subj-picker-list');
  if (!listEl) return;

  listEl.innerHTML = STATE.subjects.map((s) => {
    const isAct = String(s.id) === String(STATE.activeSubjectId);
    return `
      <div onclick="selectActiveSubject(${s.id}, true)" 
        class="uni-card p-4 flex items-center justify-between cursor-pointer transition-all hover:border-violet-500 ${isAct ? 'border-2 border-indigo-500 bg-indigo-500/10' : ''}">
        <div class="flex items-center gap-3">
          <div class="text-2xl">${s.icon || '📚'}</div>
          <div>
            <div class="font-extrabold text-sm txt-main flex items-center gap-2">
              <span>${escapeHtml(s.name)}</span>
              ${isAct ? '<span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">Đang chọn</span>' : ''}
            </div>
            <div class="text-xs txt-muted mt-0.5">${escapeHtml(s.description || s.category || '')}</div>
          </div>
        </div>
        <div class="text-right">
          <span class="badge-soft font-mono font-bold text-xs px-2.5 py-1 rounded-lg">${s.question_count || 0} câu</span>
        </div>
      </div>
    `;
  }).join('');

  openModal('modal-subject-picker');
  playSound('click');
}

function selectActiveSubject(subjectId, notify = true) {
  const sub = STATE.subjects.find((s) => String(s.id) === String(subjectId));
  if (!sub) return;

  STATE.activeSubjectId = sub.id;
  STATE.examConfig.subjectId = sub.id;
  localStorage.setItem('unimaster_active_subject_id', String(sub.id));

  // Update Top Bar & Header Elements
  const iconEl = document.getElementById('active-subj-icon');
  const nameEl = document.getElementById('active-subj-name');
  const badgeEl = document.getElementById('active-subj-badge');

  if (iconEl) iconEl.textContent = sub.icon || '📚';
  if (nameEl) nameEl.textContent = sub.name;
  if (badgeEl) badgeEl.textContent = `${sub.question_count || 0} câu`;

  // Sync all select dropdowns across tabs
  const ids = [
    'exam-subject-select',
    'exercise-subject-select',
    'fc-subject-select',
    'bank-subject-select',
    'tutor-subject-select',
    'gen-subject-select',
    'add-q-subject',
    'roadmap-subject-select',
    'battle-subject-select',
    'export-subject-select',
    'live-host-subject'
  ];
  ids.forEach((id) => {
    const sel = document.getElementById(id);
    if (sel && sel.value !== String(sub.id)) {
      sel.value = String(sub.id);
    }
  });

  closeModal('modal-subject-picker');

  // Context-aware refresh based on active tab
  if (STATE.currentTab === 'dashboard') renderDashboard();
  if (STATE.currentTab === 'exam') onExamSubjectChange();
  if (STATE.currentTab === 'flashcards') loadFlashcardsView();
  if (STATE.currentTab === 'search') filterQuestionBank();
  if (STATE.currentTab === 'exercises') loadExercisesView();

  if (notify) {
    showToast(`🎯 Đã chọn môn: ${sub.name}`, 'success');
    playSound('click');
  }
}
"""

if "fetchCurrentUserProfile" not in code:
    code += "\n" + v12_extension

# 5. Call fetchCurrentUserProfile and initActiveSubjectBar in loadSubjectsAndStats
old_load_sub = """    populateAllSubjectSelects();
    renderDashboard();
    await onExamSubjectChange();"""

new_load_sub = """    populateAllSubjectSelects();
    initActiveSubjectBar();
    await fetchCurrentUserProfile();
    renderDashboard();
    await onExamSubjectChange();"""

code = code.replace(old_load_sub, new_load_sub)

with open(APP_JS_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated static/app.js v12.0 successfully! Total characters:", len(code))
