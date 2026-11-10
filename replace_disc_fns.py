app_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

idx1 = js.find('function loadQuestionDiscussions(qid)')
idx2 = js.find('async function upvoteDiscussionComment(')

if idx1 != -1 and idx2 != -1:
    old_block = js[idx1:idx2]
    new_block = '''function toggleQuestionDiscussionBox(forceState = null) {
  const box = document.getElementById('q-community-discussion-box');
  if (!box) return;

  const willShow = forceState !== null ? forceState : box.classList.contains('hidden');
  if (willShow) {
    box.classList.remove('hidden');
    const q = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
    if (q) {
      loadQuestionDiscussions(q.id);
      setTimeout(() => document.getElementById('q-disc-content-input')?.focus(), 120);
    }
  } else {
    box.classList.add('hidden');
  }
}

async function loadQuestionDiscussions(qid) {
  const listEl = document.getElementById('q-discussion-list');
  const countEl = document.getElementById('q-discussion-count-badge');
  const toolbarCountEl = document.getElementById('q-toolbar-disc-count');
  if (!listEl || !qid) return;

  try {
    const res = await apiFetch(`/api/questions/${qid}/discussions`);
    const items = res.comments || res.discussions || [];
    STATE.discussionsCache[qid] = items;

    const countText = `${items.length} bình luận`;
    if (countEl) countEl.textContent = countText;
    if (toolbarCountEl) toolbarCountEl.textContent = items.length;

    if (!items.length) {
      const currentQ = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
      let seedTip = 'Chưa có bình luận nào cho câu này. Hãy là người đầu tiên chia sẻ mẹo nhớ!';
      if (currentQ) {
        const text = currentQ.question_text || '';
        if (text.includes('Cholesterol') || text.includes('Lipid')) {
          seedTip = '💡 Mẹo nhớ CTUMP: Công thức Friedewald: LDL-C = TC - HDL-C - (TG/5). Chỉ áp dụng khi TG < 400 mg/dL!';
        } else if (text.includes('Biuret') || text.includes('Protein')) {
          seedTip = '💡 Mẹo nhớ CTUMP: Phản ứng Biuret đặc trưng cho liên kết peptid (-CO-NH-), tạo phức màu tím sim với Cu2+ trong môi trường kiềm.';
        } else if (text.includes('Molish') || text.includes('Glucid')) {
          seedTip = '💡 Mẹo nhớ CTUMP: Thuốc thử Molish gồm alpha-naphthol trong cồn, tạo phức màu tím ở mặt phân cách giữa 2 lớp chất lỏng!';
        } else if (text.includes('class') || text.includes('virtual') || text.includes('override')) {
          seedTip = '💡 Mẹo nhớ OOP: Phương thức ở lớp cha phải có từ khóa "virtual" thì lớp con mới dùng "override" để ghi đè đa hình được!';
        }
      }
      listEl.innerHTML = `
        <div class="p-3 rounded-xl flex items-start gap-2.5 text-xs border border-indigo-500/30 bg-indigo-500/10 text-indigo-300">
          <span class="text-base">💡</span>
          <div>
            <div class="font-bold text-white">Gợi ý từ Trợ Giảng UniMaster AI:</div>
            <div>${seedTip}</div>
          </div>
        </div>
      `;
      return;
    }

    listEl.innerHTML = items
      .map(
        (c) => `
        <div class="p-3 rounded-xl flex items-start justify-between gap-3 text-xs" style="background-color: var(--bg-surface); border: 1px solid var(--border);">
          <div class="space-y-1">
            <div class="flex flex-wrap items-center gap-1.5">
              <span class="font-extrabold txt-main">👤 ${escapeHtml(c.author_name || 'Sinh viên')}</span>
              <span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">${escapeHtml(c.author_badge || '🎓 Sinh viên')}</span>
              ${c.is_verified ? `<span class="badge-emerald px-2 py-0.5 rounded text-[10px] font-bold">✔ Trợ giảng xác thực</span>` : ''}
            </div>
            <div class="txt-sub leading-relaxed">${formatRichText(c.content || '')}</div>
          </div>
          <button type="button" onclick="upvoteDiscussionComment(${c.id}, ${qid})" class="btn-soft px-2.5 py-1 text-xs font-bold shrink-0 flex items-center gap-1 text-amber-400">
            <span>👍</span> <span>${c.upvotes || 0}</span>
          </button>
        </div>
      `
      )
      .join('');
  } catch (err) {
    console.warn('Error loading discussions:', err);
  }
}

async function submitQuestionDiscussion() {
  const currentQ = (STATE.exam?.active && STATE.exam?.questions) ? STATE.exam.questions[STATE.exam.currentIndex] : null;
  if (!currentQ) return;

  const authorInp = document.getElementById('q-disc-author-input');
  const inp = document.getElementById('q-disc-content-input') || document.getElementById('q-discussion-input');
  const author = (authorInp?.value || '').trim() || 'Sinh viên UniMaster';
  const content = (inp?.value || '').trim();

  if (!content) {
    showToast('Vui lòng nhập nội dung bình luận!', 'warning');
    return;
  }

  // Instant Optimistic UI
  const listEl = document.getElementById('q-discussion-list');
  const countEl = document.getElementById('q-discussion-count-badge');
  const toolbarCountEl = document.getElementById('q-toolbar-disc-count');

  const tempCommentHtml = `
    <div class="p-3 rounded-xl flex items-start justify-between gap-3 text-xs animate-fade-in" style="background-color: var(--bg-surface); border: 1px solid var(--brand-border);">
      <div class="space-y-1">
        <div class="flex flex-wrap items-center gap-1.5">
          <span class="font-extrabold txt-main">👤 ${escapeHtml(author)}</span>
          <span class="badge-brand px-2 py-0.5 rounded text-[10px] font-bold">Vừa xong</span>
        </div>
        <div class="txt-sub text-xs leading-relaxed">${escapeHtml(content)}</div>
      </div>
      <span class="text-xs text-emerald-400 font-bold shrink-0">✓ Đã gửi</span>
    </div>
  `;
  if (listEl) {
    if (listEl.innerHTML.includes('Chưa có bình luận nào')) {
      listEl.innerHTML = tempCommentHtml;
    } else {
      listEl.innerHTML = tempCommentHtml + listEl.innerHTML;
    }
  }
  if (inp) inp.value = '';

  try {
    const res = await apiFetch(`/api/questions/${currentQ.id}/discussions`, {
      method: 'POST',
      body: JSON.stringify({
        author_name: author,
        author_badge: `⚡ Lv.${Math.floor(STATE.xp / 200) + 1}`,
        content: content
      })
    });
    if (res && res.success) {
      addXp(10);
      playSound('correct');
      showToast('💬 Đã đăng mẹo nhớ (+10 XP)!', 'success');
      const currCount = parseInt(toolbarCountEl?.textContent || '0', 10) + 1;
      if (toolbarCountEl) toolbarCountEl.textContent = currCount;
      if (countEl) countEl.textContent = `${currCount} bình luận`;
    }
  } catch (err) {
    showToast('Lỗi gửi bình luận: ' + err.message, 'warning');
  }
}

'''
    js = js[:idx1] + new_block + js[idx2:]
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced loadQuestionDiscussions & submitQuestionDiscussion successfully!")
else:
    print("Could not find targets:", idx1, idx2)
