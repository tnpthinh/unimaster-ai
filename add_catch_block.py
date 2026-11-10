with open('static/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

target = """  renderPaletteGrid();
  refreshIcons();
  renderAllMathOnPage();
}

function renderQuestionAnswerArea(q) {"""

replacement = """  renderPaletteGrid();
  refreshIcons();
  renderAllMathOnPage();
  } catch (err) {
    console.error('Critical renderCurrentExamQuestion failure:', err);
    try {
      const q = STATE.exam?.questions?.[STATE.exam?.currentIndex];
      const pEl = document.getElementById('q-prompt-text');
      const aEl = document.getElementById('q-answer-area');
      if (pEl && q) pEl.textContent = q.question_text || 'Câu hỏi';
      if (aEl && q && (q.option_a || q.option_b)) {
        aEl.innerHTML = [
          q.option_a ? `<div class="option-row opt-A" onclick="selectExamOption('A')"><strong>A:</strong> ${escapeHtml(q.option_a)}</div>` : '',
          q.option_b ? `<div class="option-row opt-B" onclick="selectExamOption('B')"><strong>B:</strong> ${escapeHtml(q.option_b)}</div>` : '',
          q.option_c ? `<div class="option-row opt-C" onclick="selectExamOption('C')"><strong>C:</strong> ${escapeHtml(q.option_c)}</div>` : '',
          q.option_d ? `<div class="option-row opt-D" onclick="selectExamOption('D')"><strong>D:</strong> ${escapeHtml(q.option_d)}</div>` : ''
        ].join('');
      }
    } catch (_) {}
  }
}

function renderQuestionAnswerArea(q) {"""

assert target in c, "target not found"
c = c.replace(target, replacement, 1)

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("Added catch block cleanly!")
