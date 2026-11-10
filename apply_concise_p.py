# apply_concise_p.py
import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    (
        'Cùng nhau ôn thi không cô đơn: Thách đấu 1v1 thời gian thực, bật tiếng mưa thư viện 25/5 và săn 12 Huy hiệu Danh giá',
        'Thách đấu 1v1 thời gian thực, phòng học Pomodoro 25/5 & bảng vinh danh'
    ),
    (
        'Công thức tính điểm chuẩn eSports học thuật: Trả lời càng nhanh và giữ chuỗi Combo càng dài, điểm mỗi câu nhân tới 2.0x!',
        'Điểm = Tốc độ + Chuỗi Combo liên tiếp (x2.0)'
    ),
    (
        'Kết nối thời gian thực qua WebSocket. Chủ phòng tạo phòng thi, sinh viên trên điện thoại nhập PIN để cùng đua top tức thì!',
        'Nhập mã PIN để tham gia thi đối kháng trực tiếp'
    ),
    (
        'Áp dụng định luật Beer–Lambert: Cthử = (ODthử / ODchuẩn) × Cchuẩn để tính nồng độ mẫu bệnh nhân và chọn nhận định lâm sàng.',
        'Định luật Beer–Lambert: C(thử) = [OD(thử) / OD(chuẩn)] × C(chuẩn)'
    ),
    (
        'Mô phỏng kỳ thi chạy trạm thực tế tại Bộ môn: Gồm 6 trạm liên hoàn (Tiêu bản cặn lắng nước tiểu + Biện luận Hóa sinh lâm sàng). Khi hết giờ mỗi trạm, chuông 🔔 sẽ vang lên và tự động chuyển sang trạm kế tiếp!',
        '6 trạm liên hoàn (Tiêu bản & Biện luận) • Chuông báo 60s/trạm'
    ),
    (
        'Bấm nút "🔔 Bắt Đầu Vòng Chạy 6 Trạm" ở góc trên để nghe tiếng chuông vào trạm 1. Bạn có thể tự chuyển trạm sớm hoặc đợi chuông báo hết giờ!',
        'Bấm Bắt đầu để làm bài qua 6 trạm thi'
    ),
    (
        'Dùng Camera Điện thoại / iPad chụp trực tiếp trang vở viết tay, giấy nháp tính toán Toán – Lý – Hóa – Sinh hoặc phiếu trả kết quả thực hành. AI sẽ đọc chữ viết tay, chấm điểm thang 10 và chỉ ra từng bước đúng/sai!',
        'Chụp ảnh vở bài tập hoặc giấy nháp để AI chấm điểm từng bước'
    ),
    (
        'Hãy bấm "📷 Chụp Ảnh / Chọn Ảnh Bài Làm" hoặc bấm "🧪 Tạo Phiếu Bài Làm Viết Tay Mẫu" ở khung bên trái để xem AI đọc chữ và chấm điểm!',
        'Chụp ảnh bài làm hoặc chọn bài mẫu để AI chấm'
    ),
    (
        'Bấm vào bất kỳ nút chuyên đề nào trên sơ đồ mạng lưới để xem các công thức cốt lõi và kích hoạt bài luyện tập mục tiêu ngay lập tức.',
        'Chạm chuyên đề để xem công thức và luyện tập'
    ),
    (
        'Tính thể tích nước tiểu phút V = V24h (mL) / 1440 và hệ số thanh thải mL/phút',
        'Thể tích phút: V = V24h / 1440 (mL/phút)'
    ),
    (
        'LDL-C = CholesterolTP - HDL-C - (Triglycerid / 2.2) (Áp dụng khi TG &lt; 4.5 mmol/L)',
        'Friedewald: LDL-C = TC - HDL - (TG / 2.2) (khi TG &lt; 4.5 mmol/L)'
    ),
    (
        'Tra cứu nomogram hiệu chỉnh liều theo thanh thải Creatinin (Cockcroft-Gault & CKD-EPI) cho bệnh nhân suy giảm chức năng thận.',
        'Hiệu chỉnh liều thuốc theo Cockcroft-Gault & CKD-EPI'
    ),
    (
        'Nhập số liệu nghiên cứu dịch tễ & y sinh để tự động tính độ nhạy, độ đặc hiệu, tỷ số chênh Odds Ratio (95% CI) và Chi-Square.',
        'Tính độ nhạy (Se), độ đặc hiệu (Sp), Odds Ratio & Relative Risk'
    ),
    (
        'Chuyển đổi toàn bộ ngân hàng câu hỏi trắc nghiệm thành bộ thẻ nhớ Anki trên điện thoại hoặc file Word in ấn chuẩn Bộ GD.',
        'Xuất thẻ Anki (.txt) hoặc tài liệu in A4'
    ),
    (
        'Định dạng chuẩn Anki UTF-8 (HTML tabs, công thức KaTeX & hình ảnh). Nhập 1-click vào app Anki Mobile (iOS/Android) hoặc Anki PC.',
        'Chuẩn Anki UTF-8 (HTML tabs, KaTeX & hình ảnh)'
    ),
    (
        'Định dạng văn bản Word A4 chuẩn Khoa Y ĐH Y Dược Cần Thơ: Tiêu đề Quốc hiệu, 2 cột chữ rõ đẹp, bảng đáp án riêng ở trang cuối.',
        'Chuẩn đề in A4 (2 cột rõ đẹp, bảng đáp án cuối trang)'
    ),
    (
        'Điện thoại và máy tính bắt cùng mạng Wi-Fi → Quét mã là vào học ngay! Mọi điểm thi, câu lưu sao, câu sai và ghi chú tự động đồng bộ qua lại tức thì.',
        'Quét mã để học ngay trên điện thoại hoặc iPad (đồng bộ tức thì)'
    ),
    (
        'Hệ thống đã tích hợp Direct Browser-to-Gemini Cloud Engine: Khi bạn tắt PC, Điện thoại / iPad tự động dùng dữ liệu 467 câu hỏi + 16 ảnh tiêu bản đã lưu trong máy và gọi thẳng lên máy chủ Google Gemini qua 4G/Wi-Fi của điện thoại mà không cần đi qua PC!',
        'Chế độ đám mây: Học độc lập trên điện thoại/iPad không cần mở PC'
    ),
    (
        'Mỗi câu sai cần trả lời đúng liên tiếp 3 lần (3/3 ✨) trong các lần ôn sau để chính thức tốt nghiệp khỏi Sổ tay',
        'Quy tắc 3 lần đúng liên tiếp (3/3 ✨) để hoàn thành'
    ),
    (
        'Chọn môn học để hệ thống tự động lọc đề thi, thẻ flashcard, bài tập và công cụ thực hành chuyên biệt cho môn đó.',
        'Chọn môn học cần ôn tập'
    ),
    (
        'Hệ thống phát hiện bạn đã chuyển đổi tab hoặc rời khỏi màn hình làm bài quá 3 lần. Toàn bộ quyền thao tác đã bị đóng băng để đảm bảo tính minh bạch.',
        'Bạn đã rời tab quá 3 lần. Bài thi đã được tự động nộp.'
    )
]

applied = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        applied += 1
        print(f"Applied: '{old[:35]}...' -> '{new[:35]}...'")
    else:
        print(f"NOT FOUND: '{old[:35]}...'")

print(f"\nTotal applied: {applied} / {len(replacements)}")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("static/index.html saved successfully.")
