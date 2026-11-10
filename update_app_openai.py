import re

app_js_path = r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\static\app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Update checkApiKeyStatus
old_status_fn = """async function checkApiKeyStatus() {
  try {
    const res = await apiFetch('/api/settings');
    STATE.hasApiKey = Boolean(res.has_gemini_key);
    STATE.apiPool = res.pool || [];
    const count = STATE.apiPool.length || (STATE.hasApiKey ? 1 : 0);

    const pill = document.getElementById('api-status-pill');
    const mask = document.getElementById('api-current-mask');
    if (pill) {
      pill.className = `${STATE.hasApiKey ? 'badge-emerald' : 'badge-amber'} text-xs px-3 py-1 rounded-full font-bold`;
      pill.textContent = STATE.hasApiKey ? `🟢 Sẵn sàng ${count} Key luân phiên` : 'Chưa gắn Key';
    }
    if (mask) {
      mask.textContent = STATE.hasApiKey
        ? `Đang có ${count} khóa trong dàn luân phiên tự động (Ưu tiên: ${res.masked_key || STATE.apiPool[0]?.masked_key})`
        : 'Hãy thêm ít nhất 1 khóa Gemini API miễn phí bên dưới';
    }
    renderApiKeyPoolList();
  } catch (_) {}
}"""

new_status_fn = """async function checkApiKeyStatus() {
  try {
    const res = await apiFetch('/api/settings');
    STATE.hasApiKey = Boolean(res.has_gemini_key);
    STATE.apiPool = res.pool || [];
    STATE.openaiConfig = res.openai || {};
    const count = STATE.apiPool.length || (STATE.hasApiKey ? 1 : 0);

    // Sync OpenAI / ChatGPT UI
    const openAiPill = document.getElementById('openai-status-pill');
    const openAiMask = document.getElementById('openai-current-mask');
    const baseInp = document.getElementById('cfg-openai-base');
    const prioSel = document.getElementById('cfg-ai-priority');

    if (baseInp && !baseInp.value) {
      baseInp.value = STATE.openaiConfig.base_url || 'https://api.openai.com/v1';
    }
    if (prioSel) {
      prioSel.value = STATE.openaiConfig.priority || 'openai_first';
    }
    if (openAiMask) {
      openAiMask.textContent = STATE.openaiConfig.has_key
        ? `Khóa đang lưu: ${STATE.openaiConfig.masked_key} • Base: ${STATE.openaiConfig.base_url || 'api.openai.com'}`
        : 'Chưa gắn khóa ChatGPT. Hãy nhập mã sk-... bên dưới.';
    }
    if (openAiPill) {
      if (STATE.openaiConfig.priority === 'openai_first') {
        openAiPill.className = 'badge-emerald text-xs px-2.5 py-1 rounded-full font-bold';
        openAiPill.textContent = '🟢 Ưu tiên gọi trước';
      } else {
        openAiPill.className = 'badge-subtle text-xs px-2.5 py-1 rounded-full font-bold';
        openAiPill.textContent = '⚪ Chế độ dự phòng';
      }
    }

    const pill = document.getElementById('api-status-pill');
    const mask = document.getElementById('api-current-mask');
    if (pill) {
      pill.className = `${STATE.hasApiKey ? 'badge-emerald' : 'badge-amber'} text-xs px-3 py-1 rounded-full font-bold`;
      pill.textContent = STATE.hasApiKey ? `🟢 Sẵn sàng ${count} Key luân phiên` : 'Chưa gắn Key';
    }
    if (mask) {
      mask.textContent = STATE.hasApiKey
        ? `Đang có ${count} khóa trong dàn luân phiên tự động (Ưu tiên: ${res.masked_key || STATE.apiPool[0]?.masked_key})`
        : 'Hãy thêm ít nhất 1 khóa Gemini API miễn phí bên dưới';
    }
    renderApiKeyPoolList();
  } catch (_) {}
}"""

if old_status_fn in text:
    text = text.replace(old_status_fn, new_status_fn, 1)
    print("Updated checkApiKeyStatus")
else:
    print("old_status_fn not matched")

# Add OpenAI helper functions
openai_helpers = """
function togglePasswordVis(inputId) {
  const el = document.getElementById(inputId);
  if (!el) return;
  el.type = el.type === 'password' ? 'text' : 'password';
}

async function testOpenAiKeyUI() {
  const keyInp = document.getElementById('cfg-openai-key');
  const baseInp = document.getElementById('cfg-openai-base');
  const fb = document.getElementById('openai-test-feedback');
  if (!fb) return;

  const key = keyInp ? keyInp.value.trim() : '';
  const base_url = baseInp ? baseInp.value.trim() : '';

  fb.classList.remove('hidden');
  fb.className = 'text-xs p-3 rounded-xl font-bold badge-subtle';
  fb.textContent = '⏳ Đang gửi yêu cầu kiểm tra kết nối tới ChatGPT / OpenAI API...';

  try {
    const res = await apiFetch('/api/ai/test-openai', {
      method: 'POST',
      body: JSON.stringify({ key, base_url })
    });

    if (res.success) {
      fb.className = 'text-xs p-3 rounded-xl font-bold badge-emerald';
      fb.textContent = `✔ Kết nối thành công! Mô hình phản hồi tốt (${res.model || 'gpt-4o-mini'}) • Khóa: ${res.masked_key || ''}`;
      showToast('Khóa ChatGPT hoạt động xuất sắc!', 'success');
    } else {
      fb.className = 'text-xs p-3 rounded-xl font-bold badge-rose';
      fb.innerHTML = `✘ ${escapeHtml(res.message || 'Lỗi kết nối')}. <br/><span class="font-normal opacity-90 mt-1 block">Mẹo: Nếu bạn dùng Relay / Proxy API (như CloseAI, OneAPI, AiHubMix), hãy nhập chính xác đường dẫn Proxy vào ô Base URL (ví dụ: <code>https://api.yourproxy.com/v1</code>).</span>`;
      showToast('Kiểm tra ChatGPT: ' + (res.message || 'Lỗi'), 'warning');
    }
  } catch (err) {
    fb.className = 'text-xs p-3 rounded-xl font-bold badge-rose';
    fb.textContent = '✘ Lỗi kiểm tra: ' + err.message;
  }
}

async function saveOpenAiSettingsUI() {
  const keyInp = document.getElementById('cfg-openai-key');
  const baseInp = document.getElementById('cfg-openai-base');
  const prioSel = document.getElementById('cfg-ai-priority');

  const payload = {};
  if (keyInp && keyInp.value.trim()) {
    payload.openai_api_key = keyInp.value.trim();
    localStorage.setItem('unimaster_openai_key', keyInp.value.trim());
  }
  if (baseInp && baseInp.value.trim()) {
    payload.openai_base_url = baseInp.value.trim();
    localStorage.setItem('unimaster_openai_base', baseInp.value.trim());
  }
  if (prioSel) {
    payload.ai_provider_priority = prioSel.value;
  }

  const res = await apiFetch('/api/settings', {
    method: 'POST',
    body: JSON.stringify(payload)
  });

  if (res.success) {
    showToast('💾 Đã lưu cấu hình ChatGPT & Thứ tự ưu tiên AI thành công!', 'success');
    if (keyInp) keyInp.value = '';
    await checkApiKeyStatus();
  } else {
    showToast('Lỗi lưu cấu hình: ' + (res.error || 'Thử lại'), 'error');
  }
}
"""

if 'async function testOpenAiKeyUI' not in text:
    text += '\n' + openai_helpers
    print("Appended openai_helpers to app.js")

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Done updating app.js")
