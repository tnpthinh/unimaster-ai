# apply_ai_and_system_optimizations.py
import re

print("Applying deep AI and system optimizations...")

# =========================================================================
# 1. OPTIMIZE ai_service.py
# =========================================================================
with open('ai_service.py', 'r', encoding='utf-8') as f:
    ai_code = f.read()

# Update GEMINI_MODELS
old_models = '''GEMINI_MODELS = [
    "gemini-3.5-flash-lite",  # Blazing fast (0.7s), instant response for tutor & mnemonics
    "gemini-3.5-flash",       # High quality reasoning (1.5s)
    "gemini-3-flash-preview"  # Reliable fallback
]'''

new_models = '''GEMINI_MODELS = [
    "gemini-3.5-flash-lite",  # Blazing fast (0.7s) - Tutor, hint, concept recall
    "gemini-3.5-flash",       # High quality reasoning (1.5s) - Code, essay, exams
    "gemini-3.6-flash",       # High performance fallback
    "gemini-3.7-flash"        # Deep reasoning fallback
]'''

if old_models in ai_code:
    ai_code = ai_code.replace(old_models, new_models)
    print("Updated GEMINI_MODELS in ai_service.py")

# Update _execute_gemini_payload to support contents
old_exec_start = '''async def _execute_gemini_payload(
    parts: list,
    system_instruction: str = "",
    max_tokens: int = 8192,
    thinking_budget: int = 384
) -> str:'''

new_exec_start = '''async def _execute_gemini_payload(
    parts: list = None,
    system_instruction: str = "",
    max_tokens: int = 8192,
    thinking_budget: int = 384,
    contents: list = None
) -> str:'''

if old_exec_start in ai_code:
    ai_code = ai_code.replace(old_exec_start, new_exec_start)
    print("Updated _execute_gemini_payload signature in ai_service.py")

# Support contents in payload construction
old_payload_construct = '''                payload = {
                    "contents": [{"role": "user", "parts": parts}],
                    "generationConfig": gen_cfg
                }'''

new_payload_construct = '''                payload_contents = contents if contents else [{"role": "user", "parts": parts or [{"text": ""}]}]
                payload = {
                    "contents": payload_contents,
                    "generationConfig": gen_cfg
                }'''

if old_payload_construct in ai_code:
    ai_code = ai_code.replace(old_payload_construct, new_payload_construct)
    print("Updated payload construction in _execute_gemini_payload")

# Update ai_chat_tutor to support conversation history
old_chat_tutor = '''async def ai_chat_tutor(subject_name: str, user_message: str, persona: str = "professor") -> str:
    persona_map = {
        "professor": "Phong cách Giáo sư Đại học uyên bác: phân tích cặn kẽ bản chất, công thức chuẩn xác và chỉ rõ bẫy đề thi.",
        "feynman": "Phong cách Richard Feynman siêu dễ hiểu: giải thích bằng hình ảnh đời thường sinh động để sinh viên mất gốc cũng hiểu ngay trong 1 phút.",
        "speed": "Phong cách Cao thủ Giải nhanh Trắc nghiệm: đi thẳng vào công thức bấm máy / loại trừ đáp án trong 10 giây.",
        "examiner": "Phong cách Giảng viên Vấn đáp: giải đáp ngắn gọn rồi đặt ngược lại 1 câu hỏi xoáy tình huống để kiểm tra độ hiểu sâu của sinh viên."
    }
    style_desc = persona_map.get(persona, persona_map["professor"])

    system_prompt = f"""Bạn là UniMaster AI — Gia sư ôn thi Đại học & THPT xuất sắc cho mọi khối ngành (Toán, Vật lý, Hóa học, Sinh học, CNTT, Kinh tế, Luật, Triết).
Môn học hiện tại: {subject_name}.
Chế độ giảng dạy: {style_desc}
{STEM_FORMAT_GUIDE}"""

    gemini_reply = await call_gemini(user_message, system_instruction=system_prompt, max_tokens=8192, thinking_budget=384)
    if gemini_reply:
        return gemini_reply'''

new_chat_tutor = '''async def ai_chat_tutor(subject_name: str, user_message: str, persona: str = "professor", history: list = None) -> str:
    persona_map = {
        "professor": "Phong cách Giáo sư Đại học uyên bác: phân tích cặn kẽ bản chất, công thức chuẩn xác và chỉ rõ bẫy đề thi.",
        "feynman": "Phong cách Richard Feynman siêu dễ hiểu: giải thích bằng hình ảnh đời thường sinh động để sinh viên mất gốc cũng hiểu ngay trong 1 phút.",
        "speed": "Phong cách Cao thủ Giải nhanh Trắc nghiệm: đi thẳng vào công thức bấm máy / loại trừ đáp án trong 10 giây.",
        "examiner": "Phong cách Giảng viên Vấn đáp: giải đáp ngắn gọn rồi đặt ngược lại 1 câu hỏi xoáy tình huống để kiểm tra độ hiểu sâu của sinh viên."
    }
    style_desc = persona_map.get(persona, persona_map["professor"])

    system_prompt = f"""Bạn là UniMaster AI — Gia sư ôn thi Đại học xuất sắc cho môn "{subject_name}".
Chế độ giảng dạy: {style_desc}
{STEM_FORMAT_GUIDE}"""

    # If history is provided, construct multi-turn dialogue
    if history and isinstance(history, list) and len(history) > 0:
        contents_list = []
        for turn in history[-8:]:
            role = "user" if turn.get("role") == "user" else "model"
            txt = str(turn.get("content") or turn.get("text") or "").strip()
            if txt:
                contents_list.append({"role": role, "parts": [{"text": txt}]})
        contents_list.append({"role": "user", "parts": [{"text": user_message}]})
        gemini_reply = await _execute_gemini_payload(contents=contents_list, system_instruction=system_prompt, max_tokens=4096, thinking_budget=256)
        if gemini_reply:
            return gemini_reply
    else:
        gemini_reply = await call_gemini(user_message, system_instruction=system_prompt, max_tokens=4096, thinking_budget=256)
        if gemini_reply:
            return gemini_reply'''

if old_chat_tutor in ai_code:
    ai_code = ai_code.replace(old_chat_tutor, new_chat_tutor)
    print("Updated ai_chat_tutor with multi-turn history support")

with open('ai_service.py', 'w', encoding='utf-8') as f:
    f.write(ai_code)
print("ai_service.py updated successfully.")


# =========================================================================
# 2. OPTIMIZE code_engine.py
# =========================================================================
with open('code_engine.py', 'r', encoding='utf-8') as f:
    ce_code = f.read()

# Update rubber_duck_critique to be professional and constructive
old_duck = '''async def rubber_duck_critique(code: str, language: str, error_trace: str = "") -> str:
    prompt = f"""Bạn là một Vịt Cao Su (Rubber Duck) - Trợ Giảng Lập Trình đại học CỰC KỲ KHÓ TÍNH, TOXIC, THÍCH CHÂM BIẾM VÀ JOKE.
Sinh viên vừa chạy code ({language}) và gặp lỗi (hoặc làm sai test case).

TỐI KỴ: TUYỆT ĐỐI KHÔNG ĐƯỢC VIẾT CODE GIẢI SẴN HOẶC CHỈ RÕ LỖI NẰM Ở DÒNG NÀO!
Hãy dùng giọng văn hài hước, châm biếm sâu cay (nhưng mang tính thúc đẩy sinh viên tự suy nghĩ) và ĐẶT 2-3 CÂU HỎI GỢI MỞ BẮT SINH VIÊN TỰ ĐỘNG NÃO!

Ví dụ phong cách:
- "Code thế này mà cũng đòi nộp thi à? Bạn có thấy cái vòng lặp for kia đang chạy vượt quá kích thước mảng không hả?"
- "Trong C++, class con kế thừa class cha thì phải dùng từ khóa gì hả thiên tài? Hay là muốn compiler tự bói?"

CODE CỦA SINH VIÊN:
```{language}
{code}
```

MÃ LỖI / STACK TRACE:
```
{error_trace}
```

Hãy đưa ra lời bình luận gay gắt và các câu hỏi gợi mở cho sinh viên:"""

    try:
        reply = await ai.call_gemini(prompt, max_tokens=1024, thinking_budget=0)
        if reply:
            return reply.strip()
    except Exception:
        pass

    return f"🦆 Vịt Cao Su: 'Bạn nghĩ code này biên dịch được à? Nhìn vào stack trace xem: {error_trace[:100]}... Hãy kiểm tra lại vòng lặp và kiểu dữ liệu trước khi bấm nộp bài tiếp!'"'''

new_duck = '''async def rubber_duck_critique(code: str, language: str, error_trace: str = "") -> str:
    prompt = f"""Bạn là Cố Vấn Lập Trình AI & Trợ Giảng Cao Cấp (Senior Engineering Mentor) môn {language.upper()} (OOP, Thuật toán & Cấu trúc dữ liệu).
Sinh viên vừa chạy bài thi code và gặp lỗi biên dịch / ngoại lệ hoặc sai kết quả test case.

Nhiệm vụ:
1. **Chẩn đoán nguyên nhân gốc rễ (Root Cause):** Phân tích ngắn gọn lỗi này thực chất là gì (ví dụ: chia cho 0, trỏ null, vượt biên mảng, thiếu virtual destructor, vi phạm tính đóng gói).
2. **Gợi ý tư duy sửa lỗi (Actionable Hints):** 2-3 gạch đầu dòng hướng dẫn cách khắc phục cụ thể, súc tích.
3. **Mẹo tối ưu (Best Practice):** 1 lưu ý ngắn giúp code sạch và an toàn hơn.
Giữ phong cách sư phạm chuẩn mực, chuyên nghiệp, khích lệ và sâu sắc.

CODE CỦA SINH VIÊN:
```{language}
{code}
```

MÃ LỖI / STACK TRACE:
```
{error_trace}
```"""

    try:
        reply = await ai.call_gemini(prompt, max_tokens=1536, thinking_budget=128)
        if reply:
            return reply.strip()
    except Exception:
        pass

    return f"### 🤖 Phân Tích Lỗi & Gợi Ý Khắc Phục\\n- **Mã lỗi phát hiện:** `{error_trace[:120]}`\\n- **Hướng xử lý:** Kiểm tra lại điều kiện biên của vòng lặp, kiểm tra biến chưa khởi tạo hoặc con trỏ trỏ vào vùng nhớ không hợp lệ."'''

if old_duck in ce_code:
    ce_code = ce_code.replace(old_duck, new_duck)
    print("Updated rubber_duck_critique in code_engine.py")

# Fix encapsulation check in validate_csharp_oop_structure
old_encap = "has_encapsulation = bool(re.search(r'\\{\\s*get;\\s*private\\s+set;\\s*\\}', code)) or bool(re.search(r'\\bprivate\\s+[A-Za-z0-9_<>]+\\s+_[a-z]', code))"
new_encap = "has_encapsulation = bool(re.search(r'\\{\\s*(?:get;\\s*private\\s+set|private\\s+set;\\s*get)\\s*;?\\s*\\}', code)) or bool(re.search(r'\\bprivate\\s+[A-Za-z0-9_<>\\[\\]]+\\s+[A-Za-z0-9_]+', code))"

if old_encap in ce_code:
    ce_code = ce_code.replace(old_encap, new_encap)
    print("Fixed C# OOP encapsulation check in code_engine.py")

with open('code_engine.py', 'w', encoding='utf-8') as f:
    f.write(ce_code)
print("code_engine.py updated successfully.")


# =========================================================================
# 3. OPTIMIZE server.py
# =========================================================================
with open('server.py', 'r', encoding='utf-8') as f:
    srv_code = f.read()

old_ai_chat = '''async def ai_chat(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "")
        if not subject_name and data.get("subject_id"):
            subs = db.get_all_subjects()
            found = next((s for s in subs if s["id"] == int(data["subject_id"])), None)
            subject_name = found["name"] if found else "Đại học tổng hợp"
        message = data.get("message", "")
        persona = data.get("persona", "professor")
        reply = await ai.ai_chat_tutor(subject_name or "Đại học tổng hợp", message, persona=persona)
        return json_resp({"success": True, "reply": reply})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)'''

new_ai_chat = '''async def ai_chat(request):
    try:
        data = await safe_get_json(request)
        subject_name = data.get("subject_name", "")
        if not subject_name and data.get("subject_id"):
            subs = db.get_all_subjects()
            found = next((s for s in subs if s["id"] == int(data["subject_id"])), None)
            subject_name = found["name"] if found else "Đại học tổng hợp"
        message = data.get("message", "")
        persona = data.get("persona", "professor")
        history = data.get("history", [])
        reply = await ai.ai_chat_tutor(subject_name or "Đại học tổng hợp", message, persona=persona, history=history)
        return json_resp({"success": True, "reply": reply})
    except Exception as e:
        return json_resp({"success": False, "error": str(e)}, 500)'''

if old_ai_chat in srv_code:
    srv_code = srv_code.replace(old_ai_chat, new_ai_chat)
    print("Updated ai_chat endpoint in server.py")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(srv_code)
print("server.py updated successfully.")


# =========================================================================
# 4. OPTIMIZE static/app.js
# =========================================================================
with open('static/app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Update sendTutorMessage with history & math rendering
old_send_tutor = '''async function sendTutorMessage() {
  const inp = document.getElementById('tutor-input');
  const box = document.getElementById('tutor-chat-box');
  if (!inp || !box || !inp.value.trim()) return;
  const msg = inp.value.trim();
  inp.value = '';

  const sub = STATE.subjects.find((s) => String(s.id) === String(document.getElementById('tutor-subject-select')?.value));
  const uDiv = document.createElement('div');
  uDiv.className = 'ml-auto max-w-xl p-3.5 rounded-2xl text-sm font-semibold text-white';
  uDiv.style.background = 'linear-gradient(135deg, var(--brand), var(--brand-2))';
  uDiv.textContent = msg;
  box.appendChild(uDiv);

  const aDiv = document.createElement('div');
  aDiv.className = 'ai-callout max-w-3xl text-sm markdown-body';
  aDiv.innerHTML = `<div class="skeleton-shimmer h-14 w-full"></div>`;
  box.appendChild(aDiv);
  box.scrollTop = box.scrollHeight;

  const res = await apiFetch('/api/ai/chat', {
    method: 'POST',
    body: JSON.stringify({
      subject_id: sub?.id || 5,
      subject_name: sub?.name || 'Đại học',
      persona: STATE.tutorPersona || 'professor',
      message: msg
    })
  });
  aDiv.innerHTML = renderMarkdown(res.reply || '');
  box.scrollTop = box.scrollHeight;
}'''

new_send_tutor = '''window.TUTOR_CHAT_HISTORY = window.TUTOR_CHAT_HISTORY || [];

async function sendTutorMessage() {
  const inp = document.getElementById('tutor-input');
  const box = document.getElementById('tutor-chat-box');
  if (!inp || !box || !inp.value.trim()) return;
  const msg = inp.value.trim();
  inp.value = '';

  const sub = STATE.subjects.find((s) => String(s.id) === String(document.getElementById('tutor-subject-select')?.value));
  const uDiv = document.createElement('div');
  uDiv.className = 'ml-auto max-w-xl p-3.5 rounded-2xl text-sm font-semibold text-white';
  uDiv.style.background = 'linear-gradient(135deg, var(--brand), var(--brand-2))';
  uDiv.textContent = msg;
  box.appendChild(uDiv);

  const aDiv = document.createElement('div');
  aDiv.className = 'ai-callout max-w-3xl text-sm markdown-body';
  aDiv.innerHTML = `<div class="skeleton-shimmer h-14 w-full"></div>`;
  box.appendChild(aDiv);
  box.scrollTop = box.scrollHeight;

  window.TUTOR_CHAT_HISTORY.push({ role: 'user', content: msg });

  try {
    const res = await apiFetch('/api/ai/chat', {
      method: 'POST',
      body: JSON.stringify({
        subject_id: sub?.id || 5,
        subject_name: sub?.name || 'Đại học',
        persona: STATE.tutorPersona || 'professor',
        message: msg,
        history: window.TUTOR_CHAT_HISTORY
      })
    });
    const replyText = res.reply || 'Xin lỗi, tôi chưa thể trả lời lúc này.';
    window.TUTOR_CHAT_HISTORY.push({ role: 'model', content: replyText });
    aDiv.innerHTML = renderMarkdown(replyText);
    renderAllMathOnPage(aDiv);
  } catch (err) {
    aDiv.innerHTML = `<p class="txt-rose">Lỗi kết nối AI: ${escapeHtml(err.message)}</p>`;
  }
  box.scrollTop = box.scrollHeight;
}'''

if old_send_tutor in app_code:
    app_code = app_code.replace(old_send_tutor, new_send_tutor)
    print("Updated sendTutorMessage in static/app.js")

# Update rubber duck UI in app.js
old_duck_ui = '''    if (duckEl) {
      duckEl.innerHTML = `
        <div class="space-y-2">
          <div class="flex items-center gap-2 font-bold text-amber-400">
            <span>🦆 Vịt Cao Su Trợ Giảng (Toxic Mode):</span>
          </div>
          <div class="txt-sub leading-relaxed text-xs italic">${formatRichText(res.reply || 'Viết code cẩn thận lại xem!')}</div>
        </div>
      `;
      playSound('click');
    }'''

new_duck_ui = '''    if (duckEl) {
      duckEl.innerHTML = `
        <div class="space-y-2">
          <div class="flex items-center gap-2 font-bold text-cyan-400">
            <span>🤖 Cố Vấn Lập Trình AI:</span>
          </div>
          <div class="txt-main leading-relaxed text-xs markdown-body">${renderMarkdown(res.reply || 'Vui lòng kiểm tra lại điều kiện biên và kiểu dữ liệu.')}</div>
        </div>
      `;
      renderAllMathOnPage(duckEl);
      playSound('click');
    }'''

if old_duck_ui in app_code:
    app_code = app_code.replace(old_duck_ui, new_duck_ui)
    print("Updated Rubber Duck UI rendering in static/app.js")

# Update step-by-step validator formatting in app.js
app_code = app_code.replace(
    '<p class="text-xs text-amber-200 italic max-w-sm text-right">${escapeHtml(val.overall_verdict || \'\')}</p>',
    '<div class="text-xs text-amber-200 max-w-sm text-right leading-relaxed">${formatRichText(val.overall_verdict || \'\')}</div>'
)

app_code = app_code.replace(
    '<div class="text-slate-100 font-bold">${escapeHtml(st.text || \'\')}</div>',
    '<div class="text-slate-100 font-bold">${formatRichText(st.text || \'\')}</div>'
)

app_code = app_code.replace(
    '<div class="text-[11px] opacity-90 font-sans italic">→ ${escapeHtml(st.feedback || \'\')}</div>',
    '<div class="text-[11px] opacity-90 font-sans">→ ${formatRichText(st.feedback || \'\')}</div>'
)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(app_code)
print("static/app.js updated successfully.")
