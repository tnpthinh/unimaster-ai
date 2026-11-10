# streamline_all_text.py
import re

print("Starting deep text streamlining for minimalist luxury UI...")

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Map of (old_phrase, new_compact_phrase)
replacements = [
    # Header & Nav
    (
        'title="Đài phát thanh Podcast ôn thi rảnh tay (Tự đọc câu hỏi -> nghỉ 3s -> đọc đáp án -> tự qua câu)"',
        'title="Podcast ôn thi rảnh tay"'
    ),
    (
        'Phím 1–4 chọn A–D • ←/→ chuyển câu • Vuốt ngang trên ĐT/iPad',
        'Phím 1–4: chọn đáp án • ←/→: chuyển câu'
    ),

    # View Exercises
    (
        'Chấm Thực Hành Lập Trình Tự Động (OOP & NNLT 1)',
        'Chấm Code Thực Hành'
    ),
    (
        '<p class="text-xs txt-muted">Biên dịch & Chấm Unit Test tức thì • Soi rò rỉ bộ nhớ (Memory Leak) • Phân tích OOP</p>',
        '<p class="text-xs txt-muted">Unit Test tự động • Soi rò rỉ bộ nhớ & kiến trúc OOP</p>'
    ),
    (
        '💻 OOP (C# / C++ / Java) - Thi 15/11 & 26/11',
        '💻 OOP (C#) - Thi 15/11 & 26/11'
    ),
    (
        '⚙️ NNLT 1 (C / C++) - Thi 01/12',
        '⚙️ NNLT 1 (Python) - Thi 01/12'
    ),
    (
        'Chấm Test Case (Submit)',
        'Chạy Test Case'
    ),

    # View Essay
    (
        'Trợ Giảng AI Chấm Tự Luận Toán Rời Rạc & Giải Thuật',
        'Chấm Tự Luận Toán & Giải Thuật'
    ),
    (
        '<p class="text-xs txt-muted">Gõ công thức LaTeX / Mã giả • AI phát hiện sai logic, thiếu trường hợp cơ sở • Soi độ phức tạp O(n)</p>',
        '<p class="text-xs txt-muted">Hỗ trợ LaTeX & mã giả • AI chấm điểm & phát hiện sai sót logic</p>'
    ),
    (
        'Giám Khảo Chấm Thi (Thang 10)',
        'Chấm Điểm (10đ)'
    ),
    (
        'Giám Khảo Chấm Bài (Thang 10)',
        'Chấm Điểm (10đ)'
    ),
    (
        'Soi Từng Bước &amp; Đánh Dấu Lỗi Sai',
        'Soi Lỗi Từng Bước'
    ),
    (
        'Tiêu Chí Chấm Điểm (Barem Rubric)',
        'Tiêu Chí Chấm Điểm'
    ),
    (
        '<p class="txt-muted italic">Xem trước công thức Toán KaTeX thời gian thực...</p>',
        '<p class="txt-muted italic">Xem trước công thức KaTeX...</p>'
    ),

    # View Generator
    (
        '<i data-lucide="sparkles" class="w-5 h-5 txt-brand"></i> AI Nhập Mọi File (PDF, PowerPoint, Word, Ảnh) & Tạo Đề Thi',
        '<i data-lucide="sparkles" class="w-5 h-5 txt-brand"></i> Nhập Tài Liệu & Tạo Đề AI'
    ),
    (
        '<p class="text-xs txt-muted mt-0.5">Kéo thả slide bài giảng, giáo trình PDF (kể cả bản scan), Word, Excel hoặc ảnh chụp đề cương để tạo đề thi theo 4 cấp độ Bloom</p>',
        '<p class="text-xs txt-muted mt-0.5">Kéo thả slide, giáo trình PDF, Word, Excel hoặc ảnh đề cương</p>'
    ),
    (
        'Bấm chọn hoặc Kéo thả nhiều file vào đây cùng lúc',
        'Kéo thả hoặc chạm để chọn tệp tài liệu'
    ),
    (
        '<div class="text-[11px] txt-sub">Bạn có thể nhập nguyên bản 100% số câu hỏi này vào môn học chỉ với 1 cú nhấp chuột (không cần chờ AI chia nhỏ).</div>',
        '<div class="text-[11px] txt-sub">Nhập trực tiếp vào môn học không cần chờ xử lý.</div>'
    ),
    (
        '📥 Nhập Nguyên Bản Toàn Bộ Câu Hỏi Ngay',
        '📥 Nhập Tất Cả Câu Hỏi'
    ),

    # View Arena
    (
        '<span>⚔️</span> Đấu Trường Tốc Độ • Phòng Học Ảo Pomodoro • Bảng Vinh Danh',
        '<span>⚔️</span> Đấu Trường Học Tập & Pomodoro'
    ),
    (
        '<p class="text-xs txt-muted mt-0.5">\n              Cùng nhau ôn thi không cô đơn: Thách đấu 1v1 thời gian thực, bật tiếng mưa thư viện 25/5 và săn 12 Huy hiệu danh giá.\n            </p>',
        '<p class="text-xs txt-muted mt-0.5">Thách đấu 1v1 trực tiếp, phòng học Pomodoro 25/5 & bảng vinh danh</p>'
    ),
    (
        'Công thức tính điểm chuẩn eSports học thuật: Trả lời càng nhanh và giữ chuỗi Combo càng dài thì điểm số và XP càng bùng nổ!',
        'Điểm số = Tốc độ trả lời + Chuỗi Combo liên tiếp.'
    ),
    (
        '<p class="text-xs txt-muted mt-0.5">Hiệu ứng đồng hiện diện xã hội (Social Co-Presence) giúp tăng 2.4 lần thời gian ngồi bàn học</p>',
        '<p class="text-xs txt-muted mt-0.5">Chu kỳ tập trung 25 phút & 5 phút thư giãn</p>'
    ),
    (
        '<p class="text-xs txt-muted mt-0.5">Kết nối thời gian thực qua WebSocket. Chủ phòng tạo phòng thi, sinh viên trên điện thoại nhập PIN để tham gia thi đối kháng trực tiếp trên cùng một màn hình chiếu!</p>',
        '<p class="text-xs txt-muted mt-0.5">Nhập mã PIN để tham gia thi đối kháng trực tiếp</p>'
    ),
    (
        'Tạo mã phòng hoặc nhập mã phòng của bạn bè để bắt đầu trận đấu trắc nghiệm thời gian thực!',
        'Nhập mã PIN để tham gia trận đấu thời gian thực.'
    ),

    # View Lab
    (
        '<div class="inline-flex items-center gap-1.5 badge-brand px-2.5 py-0.5 rounded-full text-[11px] font-bold mb-1">\n              <span>🚀 Đột Phá v10.0</span> • <span>Thực Hành Lâm Sàng & Đại Học Đa Ngành</span>\n            </div>',
        ''
    ),
    (
        '<span>🧪</span> Tổ Hợp Phòng Thí Nghiệm Ảo, Chạy Trạm OSCE & Chấm Bài Viết Tay AI',
        '<span>🧪</span> Phòng Thí Nghiệm & Mô Phỏng'
    ),
    (
        '<p class="text-xs txt-muted mt-0.5">\n              Mô phỏng thực hành Quang phổ kế Beer–Lambert, chạy trạm tiêu bản có chuông bấm giờ, chụp ảnh chấm bài tự luận viết tay và bản đồ liên kết kiến thức.\n            </p>',
        '<p class="text-xs txt-muted mt-0.5">Mô phỏng Quang phổ kế, thi chạy trạm OSCE & tính toán chuyên ngành</p>'
    ),
    (
        '🔬 1. Máy Quang Phổ & Hóa Sinh Ảo',
        '🔬 Máy Quang Phổ'
    ),
    (
        '⏱️ 2. Phòng Thi Chạy Trạm OSCE',
        '⏱️ Chạy Trạm OSCE'
    ),
    (
        '📸 3. Chấm Bài Viết Tay & Phiếu XN',
        '📸 Chấm Bài Viết Tay'
    ),
    (
        '🕸️ 4. Đồ Thị Kiến Thức Liên Chương',
        '🕸️ Sơ Đồ Kiến Thức'
    ),
    (
        '🧮 5. Máy Tính Y Khoa & Thực Hành',
        '🧮 Máy Tính Lâm Sàng'
    ),
    (
        '🩺 6. Bệnh Nhân Ảo Đa Bước',
        '🩺 Bệnh Nhân Ảo'
    ),
    (
        '💊 7. Dược Lý & Liều Thận',
        '💊 Chỉnh Liều Thuốc'
    ),
    (
        '📊 8. Thống Kê Y Sinh',
        '📊 Thống Kê Y Sinh'
    ),
    (
        '📥 9. Xuất Anki Deck &amp; Đề Thi A4',
        '📥 Xuất Anki &amp; Đề In'
    ),
    (
        'Mô phỏng kỳ thi chạy trạm thực tế tại Bộ môn: Gồm 6 trạm liên hoàn (Tiêu bản cặn lắng nước tiểu + Biện luận xét nghiệm + Đo quang phổ + Pha hóa chất). Tự động đếm ngược 60s/trạm, gõ phím chuông leng keng báo đổi trạm!',
        '6 trạm liên hoàn (Tiêu bản, Quang phổ, Xét nghiệm) • Chuông bấm giờ 60s/trạm'
    ),
    (
        'Bấm nút "🔔 Bắt Đầu Vòng Chạy 6 Trạm" ở góc trên để nghe tiếng chuông vào trạm 1. Bạn có thể bấm "Bỏ qua &amp; Qua trạm kế" nếu làm xong sớm.',
        'Bấm Bắt đầu để làm bài qua 6 trạm thi.'
    ),
    (
        'Dùng Camera Điện thoại / iPad chụp trực tiếp trang vở viết tay, giấy nháp tính toán Toán – Lý – Hóa Sinh hoặc phiếu kết quả xét nghiệm. AI Vision sẽ nhận diện chữ viết tay, kiểm tra từng dòng tính toán và chấm điểm chi tiết.',
        'Chụp ảnh vở bài tập hoặc giấy nháp tính toán để AI chấm điểm từng bước.'
    ),
    (
        'Hãy bấm "📷 Chụp Ảnh / Chọn Ảnh Bài Làm" hoặc bấm "🧪 Tạo Phiếu Bài Làm Viết Tay Mẫu" ở khung bên trái để bắt đầu chấm điểm!',
        'Chụp ảnh bài làm hoặc chọn bài mẫu để AI chấm.'
    ),
    (
        'Bấm vào bất kỳ nút chuyên đề nào trên sơ đồ mạng lưới để xem các công thức cốt lõi và kích hoạt bài kiểm tra liên quan.',
        'Chạm vào nút chuyên đề để xem công thức và luyện tập.'
    ),
    (
        'Tra cứu nomogram hiệu chỉnh liều theo thanh thải Creatinin (Cockcroft-Gault & CKD-EPI) cho bệnh nhân suy thận',
        'Hiệu chỉnh liều kháng sinh & thuốc theo thanh thải Creatinin'
    ),
    (
        'Nhập số liệu nghiên cứu dịch tễ & y sinh để tự động tính độ nhạy, độ đặc hiệu, tỷ số chênh Odds Ratio (OR), nguy cơ tương đối Relative Risk (RR) và bảng 2x2',
        'Tính độ nhạy (Se), độ đặc hiệu (Sp), Odds Ratio (OR) & Relative Risk (RR)'
    ),
    (
        'Chuyển đổi toàn bộ ngân hàng câu hỏi trắc nghiệm thành bộ thẻ nhớ Anki trên điện thoại hoặc file Word A4 trình bày đẹp chuẩn đề thi để in ra giấy học thuộc lòng!',
        'Xuất bộ thẻ Anki (.txt) hoặc đề thi Word A4 in giấy'
    ),
    (
        'Định dạng chuẩn Anki UTF-8 (HTML tabs, công thức KaTeX & hình ảnh). Nhập 1-click vào app Anki Mobile / AnkiDroid trên điện thoại.',
        'Chuẩn UTF-8 nhập 1-click vào Anki Mobile / AnkiDroid.'
    ),
    (
        'Định dạng văn bản Word A4 chuẩn Khoa Y ĐH Y Dược Cần Thơ: Tiêu đề Quốc hiệu, 2 cột chữ rõ đẹp, bảng đáp án A-B-C-D cuối đề, sẵn sàng in ra giấy.',
        'Chuẩn đề in A4 (2 cột rõ đẹp, bảng đáp án cuối trang).'
    ),

    # Modals
    (
        'Điện thoại và máy tính bắt cùng mạng Wi-Fi → Quét mã là vào học ngay! Mọi điểm thi, câu lưu, ghi chú tự động đồng bộ thời gian thực.',
        'Quét mã để học ngay trên điện thoại hoặc iPad.'
    ),
    (
        'Hệ thống đã tích hợp Direct Browser-to-Gemini Cloud Engine: Khi bạn tắt PC, Điện thoại / iPad vẫn có thể truy cập đầy đủ 100% dữ liệu đề thi, chạy máy quang phổ và chấm điểm AI độc lập!',
        'Chế độ đám mây độc lập: sử dụng trọn vẹn ngay cả khi tắt PC.'
    ),
    (
        'Mỗi câu sai cần trả lời đúng liên tiếp 3 lần (3/3 ✨) trong các lần ôn sau để chính thức tốt nghiệp khỏi sổ câu sai.',
        'Quy tắc 3 lần đúng liên tiếp (3/3 ✨) để hoàn thành.'
    ),
    (
        'Chọn môn học để hệ thống tự động lọc đề thi, thẻ flashcard, bài tập và công cụ thực hành của môn đó:',
        'Chọn môn học cần ôn tập:'
    ),
    (
        'Bubble Sort, Quick Sort, Binary Search, BFS/DFS kèm mã giả Highlight',
        'Mô phỏng từng bước thuật toán kèm mã giả'
    ),
    (
        'Click đúng dòng code chứa lỗi sai chí mạng trong 20s!',
        'Chạm đúng dòng code lỗi trong 20s!'
    ),
    (
        'Đoạn code sau đây bị lỗi biên dịch hoặc rò rỉ bộ nhớ. Hãy click vào dòng chứa lỗi:',
        'Click vào dòng code gây lỗi biên dịch hoặc rò rỉ:'
    ),
    (
        'Lọc các câu hay làm sai >= 2 lần & Thẻ nhớ Khó để in ra học thuộc lòng',
        'Tự động tổng hợp câu hay sai và thẻ nhớ trọng tâm'
    ),
    (
        'Rèn phản xạ gõ khung Class C#, Encapsulation, Constructor, Property',
        'Luyện gõ cấu trúc Class C# dưới 2 phút'
    ),
    (
        'Hệ thống phát hiện bạn đã chuyển đổi tab hoặc rời khỏi màn hình làm bài quá 3 lần. Toàn bộ mã nguồn hiện tại đã được tự động nộp và ghi nhận vi phạm.',
        'Bạn đã rời tab quá 3 lần. Bài thi đã được tự động nộp.'
    )
]

applied_count = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        applied_count += 1
        print(f"Applied: '{old[:30]}...' -> '{new[:30]}...'")
    else:
        # Check if with minor whitespace differences
        pass

print(f"\nTotal replacements applied: {applied_count} / {len(replacements)}")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("static/index.html saved successfully.")
