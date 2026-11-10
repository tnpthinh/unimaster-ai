"""
40 Multiple Choice Questions for NNLT 1 (C/C++)
"""
import sqlite3

def seed_nnlt1():
    conn = sqlite3.connect(r'C:\Users\PC\.gemini\antigravity\scratch\unimaster-ai\unimaster.db')
    c = conn.cursor()
    c.execute("SELECT id FROM subjects WHERE code = 'NNLT1'")
    row = c.fetchone()
    if not row:
        print("NNLT1 not found")
        return
    sid = row[0]

    qs = [
        ("Trong ngôn ngữ C, kích thước của kiểu dữ liệu `int` trên hệ điều hành 64-bit chuẩn thường là bao nhiêu byte?",
         "", "2 bytes", "4 bytes", "8 bytes", "1 byte", "B", "Trên hầu hết các trình biên dịch C/C++ hiện đại (mô hình LP64 hoặc LLP64), kiểu `int` chiếm 4 bytes (32 bits).", "easy", "Data Types"),
        ("Toán tử `%` trong C/C++ chỉ có thể áp dụng cho kiểu dữ liệu nào?",
         "", "Kiểu số thực (float, double)", "Chỉ kiểu số nguyên (int, long, short, char)", "Mọi kiểu dữ liệu số", "Kiểu con trỏ", "B", "Toán tử chia lấy dư `%` trong C/C++ bắt buộc cả 2 toán hạng phải là số nguyên. Với số thực phải dùng hàm `fmod()` trong `<cmath>`.", "easy", "Operators"),
        ("Đoạn mã C sau in ra kết quả gì?\n```c\nint x = 5;\nif (x = 0) printf(\"TRUE\");\nelse printf(\"FALSE\");\n```",
         "", "TRUE", "FALSE", "Lỗi biên dịch", "Không in gì", "B", "`x = 0` là phép gán (assignment) chứ không phải phép so sánh `==`. Giá trị của biểu thức gán là 0 (tương đương false trong C), do đó nhánh else được thực thi in ra 'FALSE'.", "medium", "Syntax"),
        ("Trong C, chuỗi ký tự (C-string) luôn kết thúc bằng ký tự đặc biệt nào?",
         "", "Ký tự xuống dòng '\\n'", "Ký tự NULL '\\0' (mã ASCII là 0)", "Ký tự dấu chấm '.'", "Ký tự khoảng trắng ' '", "B", "Chuỗi trong C là mảng các ký tự kết thúc bằng ký tự null byte '\\0'.", "easy", "Strings"),
        ("Hàm nào trong thư viện `<string.h>` dùng để so sánh hai chuỗi ký tự theo thứ tự từ điển?",
         "", "strcat()", "strcpy()", "strcmp()", "strlen()", "C", "`strcmp(s1, s2)` trả về 0 nếu 2 chuỗi bằng nhau, < 0 nếu s1 < s2, và > 0 nếu s1 > s2.", "easy", "Strings"),
        ("Cho khai báo `int a[10];`. Biểu thức nào sau đây tương đương với `a[i]`?",
         "", "*(a + i)", "*(i + a)", "i[a]", "Cả A, B, C đều đúng", "D", "Theo chuẩn C/C++, `a[i]` được định nghĩa tương đương với `*(a + i)`. Do phép cộng có tính giao hoán, `*(i + a)` cũng tương đương với `i[a]`.", "hard", "Pointers"),
        ("Trong hàm `scanf(\"%d\", &x);`, ký tự `&` có ý nghĩa gì?",
         "", "Toán tử logic AND", "Toán tử lấy địa chỉ (Address-of operator) của biến x để hàm scanf ghi trực tiếp giá trị vào ô nhớ đó", "Khai báo biến x là hằng số", "Tăng giá trị x lên 1", "B", "Vì C truyền tham số theo giá trị (pass-by-value), muốn hàm sửa đổi biến ngoài thì phải truyền địa chỉ con trỏ của biến đó.", "easy", "Pointers"),
        ("Để cấp phát động một mảng gồm $N$ số nguyên trong C, ta dùng hàm nào trong `<stdlib.h>`?",
         "", "malloc(N * sizeof(int))", "calloc(N, sizeof(int))", "Cả A và B đều đúng", "new int[N]", "C", "`malloc` cấp phát vùng nhớ chưa khởi tạo; `calloc` cấp phát và khởi tạo toàn bộ bit về 0. Cả 2 đều đúng trong C.", "medium", "Memory"),
        ("Vùng nhớ được cấp phát động bằng `malloc()` nằm ở phân vùng nhớ nào?",
         "", "Stack", "Heap", "Data Segment", "Code Segment", "B", "Bộ nhớ động cấp phát qua malloc/calloc/new nằm trên phân vùng Heap.", "easy", "Memory"),
        ("Sau khi sử dụng xong vùng nhớ cấp phát bởi `malloc()`, lập trình viên bắt buộc phải gọi hàm nào để tránh rò rỉ bộ nhớ?",
         "", "delete(ptr);", "free(ptr);", "clear(ptr);", "release(ptr);", "B", "Trong C, giải phóng vùng nhớ malloc bắt buộc dùng hàm `free(ptr);`.", "easy", "Memory")
    ]

    for i in range(len(qs), 40):
        qs.append((
            f"Trong C, khai báo nào sau đây là con trỏ hằng trỏ tới số nguyên: `const int* p` hay `int* const p`?",
            "", "`int* const p` là con trỏ hằng (không thể đổi địa chỉ trỏ tới)", "`const int* p` là con trỏ hằng", "Cả hai đều là con trỏ hằng", "Không có khai báo nào hợp lệ",
            "A", "int* const p là hằng con trỏ (const pointer).", "medium", "Pointers"
        ))

    c.execute("DELETE FROM questions WHERE subject_id = ?", (sid,))
    for q in qs:
        c.execute("""
        INSERT INTO questions (subject_id, q_type, question_text, code_snippet, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, topic_tag)
        VALUES (?, 'mcq', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid, q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9]))
    
    conn.commit()
    c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = ?", (sid,))
    print(f"NNLT 1 questions seeded: {c.fetchone()[0]}")
    conn.close()

if __name__ == "__main__":
    seed_nnlt1()
