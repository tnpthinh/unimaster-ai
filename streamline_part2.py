# streamline_part2.py
import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

loose_patterns = [
    (
        r'Cùng nhau ôn thi không cô đơn[\s\S]*?12 Huy hiệu danh giá\.',
        'Thách đấu 1v1 trực tiếp, phòng học Pomodoro 25/5 & bảng vinh danh'
    ),
    (
        r'Công thức tính điểm chuẩn eSports[\s\S]*?bùng nổ!',
        'Điểm số = Tốc độ trả lời + Chuỗi Combo liên tiếp.'
    ),
    (
        r'Hiệu ứng đồng hiện diện xã hội[\s\S]*?ngồi bàn học',
        'Chu kỳ tập trung 25 phút & 5 phút thư giãn'
    ),
    (
        r'Kết nối thời gian thực qua WebSocket[\s\S]*?màn hình chiếu!',
        'Nhập mã PIN để tham gia thi đối kháng trực tiếp'
    ),
    (
        r'Mô phỏng kỳ thi chạy trạm thực tế tại Bộ môn[\s\S]*?báo đổi trạm!',
        '6 trạm liên hoàn (Tiêu bản, Quang phổ, Xét nghiệm) • Chuông bấm giờ 60s/trạm'
    ),
    (
        r'Bấm nút "🔔 Bắt Đầu Vòng Chạy 6 Trạm"[\s\S]*?nếu làm xong sớm\.',
        'Bấm Bắt đầu để làm bài qua 6 trạm thi.'
    ),
    (
        r'Dùng Camera Điện thoại / iPad chụp trực tiếp[\s\S]*?chấm điểm chi tiết\.',
        'Chụp ảnh vở bài tập hoặc giấy nháp tính toán để AI chấm điểm từng bước.'
    ),
    (
        r'Hãy bấm "📷 Chụp Ảnh / Chọn Ảnh Bài Làm"[\s\S]*?bắt đầu chấm điểm!',
        'Chụp ảnh bài làm hoặc chọn bài mẫu để AI chấm.'
    ),
    (
        r'Bấm vào bất kỳ nút chuyên đề nào[\s\S]*?bài kiểm tra liên quan\.',
        'Chạm vào nút chuyên đề để xem công thức và luyện tập.'
    ),
    (
        r'Tra cứu nomogram hiệu chỉnh liều[\s\S]*?cho bệnh nhân suy thận',
        'Hiệu chỉnh liều kháng sinh & thuốc theo thanh thải Creatinin'
    ),
    (
        r'Nhập số liệu nghiên cứu dịch tễ & y sinh[\s\S]*?và bảng 2x2',
        'Tính độ nhạy (Se), độ đặc hiệu (Sp), Odds Ratio (OR) & Relative Risk (RR)'
    ),
    (
        r'Chuyển đổi toàn bộ ngân hàng câu hỏi trắc nghiệm[\s\S]*?học thuộc lòng!',
        'Xuất bộ thẻ Anki (.txt) hoặc đề thi Word A4 in giấy'
    ),
    (
        r'Định dạng chuẩn Anki UTF-8[\s\S]*?trên điện thoại\.',
        'Chuẩn UTF-8 nhập 1-click vào Anki Mobile / AnkiDroid.'
    ),
    (
        r'Định dạng văn bản Word A4 chuẩn[\s\S]*?sẵn sàng in ra giấy\.',
        'Chuẩn đề in A4 (2 cột rõ đẹp, bảng đáp án cuối trang).'
    ),
    (
        r'Điện thoại và máy tính bắt cùng mạng Wi-Fi[\s\S]*?thời gian thực\.',
        'Quét mã để học ngay trên điện thoại hoặc iPad.'
    ),
    (
        r'Hệ thống đã tích hợp Direct Browser-to-Gemini Cloud Engine[\s\S]*?chấm điểm AI độc lập!',
        'Chế độ đám mây độc lập: sử dụng trọn vẹn ngay cả khi tắt PC.'
    ),
    (
        r'Mỗi câu sai cần trả lời đúng liên tiếp 3 lần[\s\S]*?sổ câu sai\.',
        'Quy tắc 3 lần đúng liên tiếp (3/3 ✨) để hoàn thành.'
    ),
    (
        r'Chọn môn học để hệ thống tự động lọc đề thi[\s\S]*?công cụ thực hành của môn đó:',
        'Chọn môn học cần ôn tập:'
    ),
    (
        r'Hệ thống phát hiện bạn đã chuyển đổi tab[\s\S]*?ghi nhận vi phạm\.',
        'Bạn đã rời tab quá 3 lần. Bài thi đã được tự động nộp.'
    )
]

applied = 0
for pat, rep in loose_patterns:
    if re.search(pat, html):
        html = re.sub(pat, rep, html)
        applied += 1
        print(f"Matched and replaced pattern: {pat[:40]}...")
    else:
        print(f"Pattern not found: {pat[:40]}...")

print(f"\nApplied: {applied} / {len(loose_patterns)}")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("static/index.html updated successfully.")
