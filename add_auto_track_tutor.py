import os

BASE_DIR = r"C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai"
os.chdir(BASE_DIR)

with open("static/app.js", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update source in askAiAboutCurrentExamQuestion
old_ask_exam = """  pinQuestionToTutor(q, {
    label: `Câu ${idx}`,
    user_answer: userAns,
    is_correct: isCorrect
  });"""
new_ask_exam = """  pinQuestionToTutor(q, {
    label: `Câu ${idx}`,
    user_answer: userAns,
    is_correct: isCorrect,
    source: 'exam'
  });"""

if old_ask_exam in text:
    text = text.replace(old_ask_exam, new_ask_exam)
    print("Added source: 'exam' to askAiAboutCurrentExamQuestion")

# 2. Update source in askAiAboutCurrentTimedQuestion
old_ask_timed = """  pinQuestionToTutor(q, {
    label: `Thi 60P - Câu ${idx}`,
    user_answer: userAns
  });"""
new_ask_timed = """  pinQuestionToTutor(q, {
    label: `Thi 60P - Câu ${idx}`,
    user_answer: userAns,
    source: 'timed_exam'
  });"""

if old_ask_timed in text:
    text = text.replace(old_ask_timed, new_ask_timed)
    print("Added source: 'timed_exam' to askAiAboutCurrentTimedQuestion")

# 3. Add auto-update in renderCurrentExamQuestion
target_render_q = "setText('current-q-num', STATE.exam.currentIndex + 1);"
auto_update_tutor_exam = """setText('current-q-num', STATE.exam.currentIndex + 1);
  if (typeof pinnedTutorQuestion !== 'undefined' && pinnedTutorQuestion && pinnedTutorQuestion.source === 'exam') {
    const parsedH = parseQuestionHeader(q.question_text || '');
    const cleanT = (parsedH.body || q.question_text || '').replace(/<[^>]+>/g, '').trim();
    pinnedTutorQuestion.id = q.id;
    pinnedTutorQuestion.shortTitle = `Câu ${STATE.exam.currentIndex + 1}`;
    pinnedTutorQuestion.fullTitle = cleanT;
    pinnedTutorQuestion.topic = parsedH.topic || '';
    pinnedTutorQuestion.code_snippet = q.code_snippet || '';
    pinnedTutorQuestion.option_a = q.option_a || '';
    pinnedTutorQuestion.option_b = q.option_b || '';
    pinnedTutorQuestion.option_c = q.option_c || '';
    pinnedTutorQuestion.option_d = q.option_d || '';
    pinnedTutorQuestion.correct_option = q._effectiveCorrect || '';
    pinnedTutorQuestion.explanation = q.explanation || '';
    pinnedTutorQuestion.user_answer = STATE.exam.answers[q.id] || '';
    setText('ft-pinned-q-title', `📌 Câu ${STATE.exam.currentIndex + 1} • ${pinnedTutorQuestion.topic || 'Kiến thức cốt lõi'}`);
    setText('ft-pinned-q-body', cleanT.substring(0, 110) + (cleanT.length > 110 ? '...' : ''));
    syncFloatingTutorSubjectContext();
  }"""

if "pinnedTutorQuestion.source === 'exam'" not in text and target_render_q in text:
    text = text.replace(target_render_q, auto_update_tutor_exam, 1)
    print("Added real-time tutor tracking to renderCurrentExamQuestion!")

# 4. Add auto-update in renderTimedExamQuestion
target_render_timed = "if (idxBadge) idxBadge.textContent = `Câu ${idx + 1} / ${window.TIMED_EXAM.questions.length}`;"
auto_update_tutor_timed = """if (idxBadge) idxBadge.textContent = `Câu ${idx + 1} / ${window.TIMED_EXAM.questions.length}`;
  if (typeof pinnedTutorQuestion !== 'undefined' && pinnedTutorQuestion && pinnedTutorQuestion.source === 'timed_exam') {
    const cleanTimedT = (q.question_text || '').replace(/<[^>]+>/g, '').trim();
    pinnedTutorQuestion.id = q.id;
    pinnedTutorQuestion.shortTitle = `Thi 60P - Câu ${idx + 1}`;
    pinnedTutorQuestion.fullTitle = cleanTimedT;
    pinnedTutorQuestion.topic = q.topic_tag || '';
    pinnedTutorQuestion.code_snippet = q.code_snippet || '';
    pinnedTutorQuestion.option_a = q.option_a || '';
    pinnedTutorQuestion.option_b = q.option_b || '';
    pinnedTutorQuestion.option_c = q.option_c || '';
    pinnedTutorQuestion.option_d = q.option_d || '';
    pinnedTutorQuestion.correct_option = q.correct_option || '';
    pinnedTutorQuestion.user_answer = window.TIMED_EXAM.answers[q.id] || '';
    setText('ft-pinned-q-title', `📌 Thi 60P - Câu ${idx + 1} • ${pinnedTutorQuestion.topic || 'Kiến thức cốt lõi'}`);
    setText('ft-pinned-q-body', cleanTimedT.substring(0, 110) + (cleanTimedT.length > 110 ? '...' : ''));
    syncFloatingTutorSubjectContext();
  }"""

if "pinnedTutorQuestion.source === 'timed_exam'" not in text and target_render_timed in text:
    text = text.replace(target_render_timed, auto_update_tutor_timed, 1)
    print("Added real-time tutor tracking to renderTimedExamQuestion!")

with open("static/app.js", "w", encoding="utf-8") as f:
    f.write(text)

print("add_auto_track_tutor.py completed successfully!")
