import sqlite3

def seed_midterm_algo():
    conn = sqlite3.connect('unimaster.db')
    c = conn.cursor()

    # Subject 21: Giải thuật & Toán rời rạc
    sid = 21

    questions = [
        # --- Chuyên đề 1: Độ phức tạp thời gian & Phân tích giải thuật (15 câu) ---
        (
            sid,
            "Độ phức tạp thời gian $O(g(n))$ của một thuật toán biểu diễn điều gì?",
            "Chặn trên (Upper Bound) tiệm cận của thời gian thực thi khi $n$ đủ lớn.",
            "Chặn dưới (Lower Bound) thời gian chạy tối thiểu.",
            "Thời gian chạy chính xác tuyệt đối đo bằng giây trên máy tính.",
            "Thời gian chạy trung bình của tất cả các trường hợp.",
            "A",
            "Ký hiệu Big-O biểu diễn chặn trên tiệm cận (Asymptotic Upper Bound), tức $f(n) \\leq c \\cdot g(n)$ với mọi $n \\geq n_0$."
        ),
        (
            sid,
            "Đoạn mã giả sau có độ phức tạp thời gian là bao nhiêu?\n```python\nfor i in range(n):\n    j = 1\n    while j < n:\n        j = j * 2\n```",
            "$O(n \\log n)$",
            "$O(n^2)$",
            "$O(n)$",
            "$O(\\log n)$",
            "A",
            "Vòng lặp ngoài chạy $n$ lần. Vòng lặp trong biến $j$ tăng gấp đôi mỗi lần nên chạy $\\approx \\log_2 n$ lần. Tổng số phép toán là $n \\times \\log_2 n = O(n \\log n)$."
        ),
        (
            sid,
            "Đoạn mã sau có độ phức tạp thời gian là bao nhiêu?\n```cpp\nfor (int i = 1; i <= n; i *= 2) {\n    cout << i << endl;\n}\n```",
            "$O(\\log n)$",
            "$O(n)$",
            "$O(n \\log n)$",
            "$O(1)$",
            "A",
            "Biến đếm $i$ nhân 2 sau mỗi bước: $1, 2, 4, 8, ..., 2^k \\leq n$. Số bước lặp là $k = \\lfloor \\log_2 n \\rfloor + 1$, do đó độ phức tạp là $O(\\log n)$."
        ),
        (
            sid,
            "Áp dụng Định lý Thợ (Master Theorem) cho hệ thức $T(n) = 2T(n/2) + O(n)$. Độ phức tạp của thuật toán là:",
            "$\\Theta(n \\log n)$",
            "$\\Theta(n)$",
            "$\\Theta(n^2)$",
            "$\\Theta(\\log n)$",
            "A",
            "Ở đây $a = 2, b = 2, f(n) = O(n)$. Ta có $n^{\\log_b a} = n^{\\log_2 2} = n^1$. Vì $f(n) = \\Theta(n^{\\log_b a})$, theo Trường hợp 2 của Master Theorem, nghiệm là $\\Theta(n \\log n)$ (chính là Merge Sort)."
        ),
        (
            sid,
            "Áp dụng Định lý Thợ cho hệ thức truy hồi $T(n) = 8T(n/2) + O(n^2)$. Độ phức tạp của $T(n)$ là:",
            "$\\Theta(n^3)$",
            "$\\Theta(n^2)$",
            "$\\Theta(n^2 \\log n)$",
            "$\\Theta(n^{\\log_2 3})$",
            "A",
            "$a = 8, b = 2 \\Rightarrow n^{\\log_b a} = n^{\\log_2 8} = n^3$. Vì $f(n) = O(n^2) = O(n^{3 - \\epsilon})$ với $\\epsilon = 1$, rơi vào Trường hợp 1 của Master Theorem: $T(n) = \\Theta(n^{\\log_b a}) = \\Theta(n^3)$."
        ),
        (
            sid,
            "Thuật toán có thời gian chạy $T(n) = T(n-1) + O(1)$ với $T(1) = 1$ có độ phức tạp là:",
            "$O(n)$",
            "$O(\\log n)$",
            "$O(n^2)$",
            "$O(2^n)$",
            "A",
            "Khai triển: $T(n) = T(n-1) + c = T(n-2) + 2c = ... = T(1) + (n-1)c = O(n)$."
        ),
        (
            sid,
            "Thuật toán đệ quy tính số Fibonacci theo định nghĩa: `F(n) = F(n-1) + F(n-2)` không dùng nhớ (memoization) có độ phức tạp là:",
            "$O(2^n)$ (chính xác là $O(1.618^n)$)",
            "$O(n^2)$",
            "$O(n)$",
            "$O(n \\log n)$",
            "A",
            "Cây đệ quy nhị phân có chiều cao $n$, mỗi tầng nhân đôi số lời gọi hàm, độ phức tạp thời gian tăng theo cấp số nhân $O(2^n)$."
        ),
        (
            sid,
            "Thứ tự tăng dần nào sau đây về tốc độ tăng của các hàm độ phức tạp khi $n \\to \\infty$ là ĐÚNG?",
            "$O(1) < O(\\log n) < O(\\sqrt{n}) < O(n) < O(n \\log n) < O(n^2) < O(2^n)$",
            "$O(1) < O(n) < O(\\log n) < O(n \\log n) < O(n^2) < O(2^n)$",
            "$O(1) < O(\\log n) < O(n) < O(\\sqrt{n}) < O(n^2) < O(2^n)$",
            "$O(\\log n) < O(1) < O(n) < O(n \\log n) < O(n^2) < O(2^n)$",
            "A",
            "Hằng số $O(1) < O(\\log n) < O(\\sqrt{n}) < O(n) < O(n \\log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)$."
        ),
        (
            sid,
            "Nếu một thuật toán chạy mất 1 giây với kích thước đầu vào $n = 1000$ và có độ phức tạp $O(n^2)$, thì với $n = 3000$, thời gian chạy ước tính là:",
            "9 giây",
            "3 giây",
            "6 giây",
            "27 giây",
            "A",
            "Vì độ phức tạp là $O(n^2)$, khi $n$ tăng gấp 3 lần ($3000/1000 = 3$), thời gian chạy sẽ tăng $3^2 = 9$ lần. $1 \\times 9 = 9$ giây."
        ),
        (
            sid,
            "Độ phức tạp không gian (Space Complexity) của thuật toán đệ quy duyệt cây nhị phân theo thứ tự trước (Pre-order) phụ thuộc vào yếu tố nào?",
            "Chiều cao của cây (chiều sâu của ngăn xếp Call Stack).",
            "Tổng số lá của cây.",
            "Số lượng nút con của nút gốc.",
            "Luôn luôn là $O(1)$.",
            "A",
            "Không gian bộ nhớ ngăn xếp đệ quy Call Stack tương ứng với độ sâu đường đi dài nhất từ gốc đến lá, tức là chiều cao của cây $O(h)$."
        ),

        # --- Chuyên đề 2: Thuật toán Sắp xếp (Sorting Algorithms) (15 câu) ---
        (
            sid,
            "Trong thuật toán Quick Sort, trường hợp xấu nhất (Worst-case) xảy ra khi nào và độ phức tạp lúc đó là bao nhiêu?",
            "Khi mảng đã có thứ tự và luôn chọn phần tử đầu/cuối làm chốt (Pivot); độ phức tạp $O(n^2)$.",
            "Khi mảng hoàn toàn ngẫu nhiên; độ phức tạp $O(n \\log n)$.",
            "Khi mảng có kích thước chẵn; độ phức tạp $O(n)$.",
            "Khi các phần tử bằng nhau; độ phức tạp $O(\\log n)$",
            "A",
            "Nếu pivot luôn là phần tử nhỏ nhất hoặc lớn nhất, mảng bị phân hoạch lệch thành 1 và $n-1$, dẫn đến thời gian $T(n) = T(n-1) + O(n) = O(n^2)$."
        ),
        (
            sid,
            "Thuật toán sắp xếp nào sau đây có độ phức tạp thời gian trong trường hợp xấu nhất vẫn đảm bảo $O(n \\log n)$ VÀ có tính ổn định (Stable)?",
            "Merge Sort (Sắp xếp trộn)",
            "Quick Sort (Sắp xếp nhanh)",
            "Heap Sort (Sắp xếp vun đống)",
            "Selection Sort (Sắp xếp chọn)",
            "A",
            "Merge Sort luôn có độ phức tạp $O(n \\log n)$ ở mọi trường hợp và giữ nguyên thứ tự tương đối của các phần tử có giá trị bằng nhau (ổn định)."
        ),
        (
            sid,
            "Heap Sort sử dụng cấu trúc dữ liệu Max-Heap để sắp xếp mảng tăng dần. Thời gian để xây dựng cây Max-Heap ban đầu từ mảng $n$ phần tử là:",
            "$O(n)$",
            "$O(n \\log n)$",
            "$O(n^2)$",
            "$O(\\log n)$",
            "A",
            "Bằng thuật toán vun đống từ dưới lên (Bottom-up Build-Heap), tổng số phép toán được chứng minh là $O(n)$, không phải $O(n \\log n)$."
        ),
        (
            sid,
            "Trong thuật toán Bubble Sort với cờ hiệu (flag swapped), trường hợp tốt nhất (Best-case) xảy ra khi mảng đã sắp xếp sẵn. Số phép so sánh và độ phức tạp lúc này là:",
            "$n - 1$ phép so sánh, độ phức tạp $O(n)$.",
            "$n(n-1)/2$ phép so sánh, độ phức tạp $O(n^2)$.",
            "$0$ phép so sánh, độ phức tạp $O(1)$.",
            "$\\log n$ phép so sánh, độ phức tạp $O(\\log n)$.",
            "A",
            "Sau lượt duyệt đầu tiên với $n-1$ phép so sánh, nếu không có cặp nào bị hoán đổi, cờ `swapped == false` và thuật toán kết thúc ngay với $O(n)$."
        ),
        (
            sid,
            "Thuật toán Insertion Sort (Sắp xếp chèn) hoạt động hiệu quả nhất trong trường hợp nào?",
            "Mảng gần như đã có thứ tự (Nearly Sorted).",
            "Mảng bị đảo ngược thứ tự hoàn toàn.",
            "Mảng có kích thước $n > 10^7$.",
            "Mảng chứa toàn số âm.",
            "A",
            "Khi mảng gần có thứ tự, mỗi phần tử chỉ cần dịch chuyển 1 hoặc 0 bước, thời gian chạy tiệm cận $O(n)$."
        ),
        (
            sid,
            "Đặc điểm nào sau đây là NHƯỢC ĐIỂM lớn nhất của Merge Sort so với Quick Sort khi cài đặt trên mảng?",
            "Tốn bộ nhớ phụ $O(n)$ để chứa mảng tạm thời khi trộn.",
            "Thời gian chạy trường hợp xấu nhất là $O(n^2)$.",
            "Không thể chạy trên dữ liệu danh sách liên kết.",
            "Không có tính ổn định (Unstable).",
            "A",
            "Merge Sort chuẩn cần mảng phụ kích thước $O(n)$ để trộn 2 nửa, trong khi Quick Sort là sắp xếp tại chỗ (In-place) chỉ tốn $O(\\log n)$ Call Stack."
        ),
        (
            sid,
            "Counting Sort và Radix Sort có thể đạt độ phức tạp tuyến tính $O(n)$ vì lý do gì?",
            "Chúng không sử dụng phép so sánh giữa các cặp phần tử (Non-comparison based).",
            "Chúng sử dụng thuật toán song song trên nhiều lõi CPU.",
            "Chúng chỉ áp dụng được cho mảng có độ dài dưới 100.",
            "Chúng bỏ qua các phần tử trùng lặp.",
            "A",
            "Các thuật toán so sánh đều có chặn dưới $\\Omega(n \\log n)$. Counting Sort dựa vào việc đếm tần số xuất hiện của giá trị trong một khoảng cố định nên đạt $O(n + k)$."
        ),

        # --- Chuyên đề 3: Tìm kiếm & Cây tìm kiếm nhị phân (BST) (15 câu) ---
        (
            sid,
            "Điều kiện TIÊN QUYẾT để áp dụng thuật toán Tìm kiếm Nhị phân (Binary Search) trên mảng là gì?",
            "Mảng phải được sắp xếp theo thứ tự (tăng dần hoặc giảm dần).",
            "Mảng không được chứa phần tử âm.",
            "Kích thước mảng $n$ phải là lũy thừa của 2.",
            "Mảng phải có độ dài lẻ.",
            "A",
            "Binary Search dựa vào tính chất thứ tự để loại bỏ một nửa không gian tìm kiếm ở mỗi bước. Nếu mảng chưa sắp xếp thì không thể áp dụng."
        ),
        (
            sid,
            "Trong mảng đã sắp xếp có $n = 1024$ phần tử, số lần so sánh tối đa của Tìm kiếm Nhị phân để tìm một khóa $X$ là:",
            "11 lần (tối đa $\\lfloor \\log_2 n \\rfloor + 1$)",
            "1024 lần",
            "512 lần",
            "1 lần",
            "A",
            "$\\log_2(1024) = 10$. Số lần so sánh tối đa khi không tìm thấy hoặc ở bước cuối cùng là $10 + 1 = 11$ lần."
        ),
        (
            sid,
            "Trong một Cây Tìm kiếm Nhị phân (BST), phép duyệt nào sau đây sẽ cho danh sách các khóa theo thứ tự TĂNG DẦN?",
            "Duyệt giữa (In-order Traversal: Left - Root - Right)",
            "Duyệt trước (Pre-order Traversal: Root - Left - Right)",
            "Duyệt sau (Post-order Traversal: Left - Right - Root)",
            "Duyệt theo mức (Level-order / BFS)",
            "A",
            "Trong BST, mọi nút ở cây con trái $< Root <$ mọi nút ở cây con phải. Duyệt In-order (Trái - Gốc - Phải) luôn cho dãy tăng dần."
        ),
        (
            sid,
            "Trường hợp xấu nhất khi tìm kiếm trên Cây Tìm kiếm Nhị phân (BST) không cân bằng xảy ra khi nào và độ phức tạp là bao nhiêu?",
            "Khi cây bị thoái hóa thành một đường thẳng (danh sách liên kết); độ phức tạp $O(n)$.",
            "Khi cây cân bằng hoàn hảo; độ phức tạp $O(\\log n)$.",
            "Khi cây có số nút là số chẵn; độ phức tạp $O(1)$.",
            "Khi các nút có giá trị âm; độ phức tạp $O(n \\log n)$.",
            "A",
            "Nếu thêm các phần tử theo thứ tự đã sắp xếp (ví dụ 1, 2, 3, 4, 5), BST thoái hóa thành một nhánh duy nhất, chiều cao $h = n$, dẫn đến tìm kiếm mất $O(n)$."
        ),
        (
            sid,
            "Cây AVL và Cây Đỏ - Đen (Red-Black Tree) giải quyết nhược điểm gì của Cây Tìm kiếm Nhị phân thông thường?",
            "Tự cân bằng (Self-balancing) để đảm bảo chiều cao luôn là $O(\\log n)$, ngăn chặn thoái hóa.",
            "Cho phép chứa các phần tử trùng khóa vô hạn.",
            "Giảm dung lượng bộ nhớ RAM về $O(1)$.",
            "Cho phép tìm kiếm mà không cần so sánh khóa.",
            "A",
            "Cây AVL và Red-Black Tree sử dụng các phép quay cây (Rotations) để duy trì sự cân bằng, bảo đảm các thao tác tìm kiếm, chèn, xóa luôn mất $O(\\log n)$."
        ),

        # --- Chuyên đề 4: Chia để trị, Quy hoạch động & Tham lam (15 câu) ---
        (
            sid,
            "Chiến lược thiết kế giải thuật 'Chia để trị' (Divide and Conquer) gồm 3 bước cơ bản nào?",
            "Chia (Divide) -> Trị (Conquer) -> Kết hợp (Combine)",
            "Khởi tạo -> Lặp -> Dừng",
            "Đoán -> Thử -> Sửa sai",
            "Chọn phần tử lớn nhất -> Loại bỏ -> Tiếp tục",
            "A",
            "Ba bước chuẩn: 1) Chia bài toán thành các bài toán con nhỏ hơn; 2) Trị bằng cách giải đệ quy; 3) Kết hợp lời giải các bài toán con thành lời giải bài toán ban đầu."
        ),
        (
            sid,
            "Sự khác biệt CỐT LÕI giữa Quy hoạch động (Dynamic Programming) và Chia để trị (Divide and Conquer) là gì?",
            "Quy hoạch động áp dụng cho bài toán có các bài toán con gối nhau (Overlapping Subproblems) và lưu lại kết quả.",
            "Chia để trị luôn có độ phức tạp thời gian nhanh hơn Quy hoạch động.",
            "Quy hoạch động không bao giờ dùng mảng hoặc bảng nhớ.",
            "Chia để trị chỉ áp dụng cho bài toán sắp xếp.",
            "A",
            "Trong Chia để trị, các bài toán con độc lập (như Merge Sort). Trong Quy hoạch động, các bài toán con lặp lại nhiều lần nên cần kỹ thuật lưu nhớ (Memoization / Tabulation) để không phải tính lại."
        ),
        (
            sid,
            "Thuật toán Tham lam (Greedy Algorithm) hoạt động dựa trên nguyên tắc nào?",
            "Tại mỗi bước, luôn đưa ra lựa chọn tối ưu cục bộ tốt nhất với hy vọng đạt được tối ưu toàn cục.",
            "Xem xét tất cả các phương án có thể rồi chọn phương án tốt nhất (vét cạn).",
            "Lùi lại bước trước nếu phát hiện phương án không khả thi (Quay lui Backtracking).",
            "Chia bài toán thành 2 nửa bằng nhau.",
            "A",
            "Đặc trưng của giải thuật tham lam: Greedy-choice property (lựa chọn tham lam) và Optimal substructure (cấu trúc con tối ưu)."
        ),
        (
            sid,
            "Bài toán 'Cái balo phân số' (Fractional Knapsack) cho phép chia nhỏ đồ vật có thể giải tối ưu bằng giải thuật nào?",
            "Thuật toán Tham lam (Greedy) dựa trên tỉ số giá trị / trọng lượng ($v_i / w_i$).",
            "Chỉ có thể giải bằng Vét cạn (Brute-force).",
            "Chỉ có thể giải bằng Cây khung nhỏ nhất Kruskal.",
            "Bắt buộc phải dùng thuật toán Dijkstra.",
            "A",
            "Fractional Knapsack có thể giải tối ưu bằng Greedy với độ phức tạp $O(n \\log n)$ nhờ việc sắp xếp theo đơn giá giảm dần."
        ),
        (
            sid,
            "Bài toán Balo 0-1 (0/1 Knapsack - mỗi đồ vật chỉ được chọn hoặc không chọn) KHÔNG THỂ giải tối ưu bằng thuật toán Tham lam vì lý do gì?",
            "Lựa chọn tham lam đồ vật có đơn giá cao nhất có thể làm lãng phí dung lượng balo, không đạt tối ưu toàn cục.",
            "Vì balo 0-1 không có nghiệm.",
            "Vì thuật toán tham lam chỉ chạy được trên số thực.",
            "Vì 0/1 Knapsack có số đồ vật vô hạn.",
            "A",
            "Ví dụ: Balo trọng lượng 5kg. Vật A (4kg, 28$), Vật B (3kg, 18$), Vật C (2kg, 12$). Tham lam chọn A (đơn giá 7$/kg) chỉ được 28$, trong khi chọn B + C (5kg) được 30$!"
        ),
        (
            sid,
            "Thuật toán Dijkstra tìm đường đi ngắn nhất thuộc nhóm phương pháp thiết kế nào?",
            "Thuật toán Tham lam (Greedy Algorithm)",
            "Chia để trị (Divide and Conquer)",
            "Nhánh cận (Branch and Bound)",
            "Ngẫu nhiên hóa (Randomized Algorithm)",
            "A",
            "Dijkstra luôn chọn đỉnh chưa thăm có khoảng cách tạm thời nhỏ nhất để nới lỏng (Relax) các cạnh kề, đây là bản chất của giải thuật Tham lam."
        )
    ]

    inserted = 0
    for q in questions:
        # Check if already exists
        c.execute("SELECT id FROM questions WHERE subject_id = ? AND question_text = ?", (q[0], q[1]))
        if not c.fetchone():
            c.execute("""
                INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, topic_tag, q_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'medium', 'Algorithms Midterm', 'mcq')
            """, q)
            inserted += 1

    conn.commit()
    print(f"Successfully seeded {inserted} new Midterm Algorithm questions for Subject 21!")
    
    # Check total questions for subject 21
    c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = 21")
    total = c.fetchone()[0]
    print(f"Total questions for Subject 21 (Giải thuật): {total}")
    conn.close()

if __name__ == '__main__':
    seed_midterm_algo()
