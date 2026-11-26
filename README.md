---
title: UniMaster AI Pro
emoji: 🎓
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# UniMaster AI Pro v7.0
Nền tảng Ôn Thi & Gia Sư AI Tương Tác Sư Phạm (Feynman, Socratic, Gen Z, Mẹo 5s).

## Triển khai Cloud 24/7 Miễn Phí (Tắt PC vẫn dùng online)

### Cách 1: Hugging Face Spaces (Khuyên dùng - 100% Free 24/7 vĩnh viễn)
1. Đăng nhập [huggingface.co](https://huggingface.co) -> bấm **New Space**.
2. Đặt tên Space (ví dụ: `unimaster-ai`), chọn License: **MIT**.
3. Chọn Space SDK: **Docker** -> **Blank**.
4. Chọn Hardware: **CPU basic • 2 vCPU • 16GB RAM • Free**.
5. Nhập biến môi trường (Secrets / Variables):
   - `APP_PASSWORD`: Mật khẩu đăng nhập của bạn.
   - `GEMINI_API_KEYS`: Danh sách API key Google AI Studio (cách nhau dấu phẩy).
   - `REQUIRE_AUTH`: `1` (hoặc `0` nếu không cần mật khẩu).
6. Kết nối trực tiếp với repo GitHub `tnpthinh/unimaster-ai` hoặc push code lên.

### Cách 2: Koyeb (Có cụm máy chủ Singapore tốc độ cao)
1. Đăng ký tài khoản tại [koyeb.com](https://www.koyeb.com).
2. Tạo Service mới -> Chọn **GitHub**.
3. Chọn repo `tnpthinh/unimaster-ai` -> Builder: **Dockerfile**.
4. Chọn vùng: **Singapore (sin)** để đạt tốc độ cao nhất từ Việt Nam.
5. Thiết lập Environment Variables tương tự như trên.
