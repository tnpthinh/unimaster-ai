# update_app_js_shortcuts.py

with open('static/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = '''const SUBJECT_SHORTCUTS = {
  OOP_CSHARP: [
    { icon: '⏱️', label: 'Thi Thử 60p (40 câu OOP)', action: 'startTimedExamForSubject(5, 60, 40)' },
    { icon: '💻', label: 'Chấm 20 Bài Code OOP & C++', action: "switchTab('exercises')" },
    { icon: '🧪', label: 'Unit Test Tự Động', action: "switchTab('exercises')" },
    { icon: '🗂️', label: 'Flashcard Đa Hình & Destructor', action: 'openSubjectFlashcards(5)' },
    { icon: '🤖', label: 'AI Review Rò Rỉ Bộ Nhớ', action: "switchTab('exercises')" }
  ],
  DISCRETE_MATH_ALGO: [
    { icon: '⚡', label: 'Thi Thử Giữa Kỳ 16/11 (40 câu)', action: 'startTimedExamForSubject(21, 60, 40)' },
    { icon: '📊', label: 'Mô Phỏng Thuật Toán Trực Quan', action: 'openAlgoVisualizerModal()' },
    { icon: '✍️', label: 'Trợ Giảng Chấm Tự Luận Thuật Toán', action: "switchTab('essay')" },
    { icon: '🎯', label: 'Săn Lỗi Thuật Toán 20s (Bug Hunter)', action: 'openBugHunterModal()' },
    { icon: '🗂️', label: 'Flashcard Bảng Độ Phức Tạp Big-O', action: 'openSubjectFlashcards(21)' }
  ],
  NNLT1: [
    { icon: '💻', label: 'Chấm 10 Bài Thực Hành C/C++', action: "switchTab('exercises'); selectExerciseBySubject(22);" },
    { icon: '🧪', label: 'Test Case Mảng, Chuỗi & Con Trỏ', action: "switchTab('exercises')" },
    { icon: '⏱️', label: 'Thi Thử 60p (40 câu Căn Bản)', action: 'startTimedExamForSubject(22, 60, 40)' },
    { icon: '🗂️', label: 'Flashcard Heap/Stack & Con Trỏ', action: 'openSubjectFlashcards(22)' }
  ],
  AVCB3: [
    { icon: '⏱️', label: 'Thi Thử 60 Phút (40 câu B1/B2)', action: 'startTimedExamForSubject(23, 60, 40)' },
    { icon: '📚', label: 'Ngân Hàng 200 Câu Ngữ Pháp', action: 'openSubjectBank(23)' },
    { icon: '🗂️', label: '30 Flashcard Từ Vựng Học Thuật', action: 'openSubjectFlashcards(23)' },
    { icon: '🤖', label: 'AI Gia Sư Luyện Câu B1/B2', action: "openFloatingTutorWithPrompt('Hãy giải thích cấu trúc Đảo ngữ và Câu điều kiện trong đề AVCB 3!')" }
  ],
  HOASINH_CTUMP: [
    { icon: '🩸', label: '200 câu Protid & Thận', action: 'quickStartBai2Protid()' },
    { icon: '🔬', label: 'Máy quang phổ Beer–Lambert', action: "switchTab('lab'); switchLabSubTab('spectro');" },
    { icon: '⏱️', label: 'Chạy trạm OSCE 6 trạm', action: "switchTab('lab'); switchLabSubTab('osce');" },
    { icon: '🩺', label: 'Bệnh nhân ảo lâm sàng', action: "switchTab('lab'); switchLabSubTab('patient');" },
    { icon: '💊', label: 'Hiệu chỉnh liều theo thận', action: "switchTab('lab'); switchLabSubTab('dosing');" }
  ],
  CS101: [
    { icon: '💻', label: 'Trắc nghiệm Cấu trúc dữ liệu', action: 'openSubjectExam(4)' },
    { icon: '🗂️', label: 'Flashcard Thuật toán & Độ phức tạp', action: 'openSubjectFlashcards(4)' },
    { icon: '🔍', label: 'Tra cứu Ngân hàng câu hỏi', action: 'openSubjectBank(4)' }
  ],
  MATH101: [
    { icon: '📐', label: 'Luyện thi Giải tích & Đại số', action: 'openSubjectExam(3)' },
    { icon: '🗂️', label: 'Flashcard Công thức Tích phân', action: 'openSubjectFlashcards(3)' }
  ]
};'''

replacement = '''const SUBJECT_SHORTCUTS = {
  OOP_CSHARP: [
    { icon: '⏱️', label: 'Thi Thử 60p (40 câu)', action: 'startTimedExamForSubject(5, 60, 40)' },
    { icon: '💻', label: 'Chấm Code OOP C#', action: "switchTab('exercises')" },
    { icon: '🧪', label: 'Unit Test Tự Động', action: "switchTab('exercises')" },
    { icon: '🗂️', label: 'Flashcard Đa Hình', action: 'openSubjectFlashcards(5)' },
    { icon: '🤖', label: 'AI Soi Rò Rỉ RAM', action: "switchTab('exercises')" }
  ],
  DISCRETE_MATH_ALGO: [
    { icon: '⚡', label: 'Đề Giữa Kỳ 16/11 (40 câu)', action: 'startTimedExamForSubject(21, 60, 40)' },
    { icon: '📊', label: 'Mô Phỏng Thuật Toán', action: 'openAlgoVisualizerModal()' },
    { icon: '✍️', label: 'Chấm Tự Luận Thuật Toán', action: "switchTab('essay')" },
    { icon: '🎯', label: 'Săn Lỗi 20s (Bug Hunter)', action: 'openBugHunterModal()' },
    { icon: '🗂️', label: 'Flashcard Big-O', action: 'openSubjectFlashcards(21)' }
  ],
  NNLT1: [
    { icon: '💻', label: 'Chấm Thực Hành Python', action: "switchTab('exercises'); selectExerciseBySubject(22);" },
    { icon: '🧪', label: 'Test Case Mảng & Chuỗi', action: "switchTab('exercises')" },
    { icon: '⏱️', label: 'Thi Thử 60p Căn Bản', action: 'startTimedExamForSubject(22, 60, 40)' },
    { icon: '🗂️', label: 'Flashcard Cấu Trúc Dữ Liệu', action: 'openSubjectFlashcards(22)' }
  ],
  AVCB3: [
    { icon: '⏱️', label: 'Thi Thử 60p (B1/B2)', action: 'startTimedExamForSubject(23, 60, 40)' },
    { icon: '📚', label: 'Ngân Hàng 200 Câu', action: 'openSubjectBank(23)' },
    { icon: '🗂️', label: 'Flashcard Từ Vựng', action: 'openSubjectFlashcards(23)' },
    { icon: '🤖', label: 'AI Luyện Ngữ Pháp', action: "openFloatingTutorWithPrompt('Hãy giải thích cấu trúc Đảo ngữ và Câu điều kiện trong đề AVCB 3!')" }
  ],
  HOASINH_CTUMP: [
    { icon: '🩸', label: '200 Câu Protid & Thận', action: 'quickStartBai2Protid()' },
    { icon: '🔬', label: 'Máy Quang Phổ', action: "switchTab('lab'); switchLabSubTab('spectro');" },
    { icon: '⏱️', label: 'Chạy Trạm OSCE', action: "switchTab('lab'); switchLabSubTab('osce');" },
    { icon: '🩺', label: 'Bệnh Nhân Ảo', action: "switchTab('lab'); switchLabSubTab('patient');" },
    { icon: '💊', label: 'Hiệu Chỉnh Liều', action: "switchTab('lab'); switchLabSubTab('dosing');" }
  ],
  CS101: [
    { icon: '💻', label: 'Trắc Nghiệm CTDL', action: 'openSubjectExam(4)' },
    { icon: '🗂️', label: 'Flashcard Thuật Toán', action: 'openSubjectFlashcards(4)' },
    { icon: '🔍', label: 'Ngân Hàng Câu Hỏi', action: 'openSubjectBank(4)' }
  ],
  MATH101: [
    { icon: '📐', label: 'Luyện Đề Giải Tích', action: 'openSubjectExam(3)' },
    { icon: '🗂️', label: 'Flashcard Tích Phân', action: 'openSubjectFlashcards(3)' }
  ]
};'''

if target in js:
    js = js.replace(target, replacement)
    print("Updated SUBJECT_SHORTCUTS with concise punchy labels.")
else:
    print("Target not found in static/app.js!")

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("static/app.js saved successfully.")
