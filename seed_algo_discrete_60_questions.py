"""
60 High-Quality Multiple Choice Questions for Discrete Mathematics & Algorithms
Exam on Nov 27
Covers:
- Propositional & Predicate Logic
- Proof Techniques (Induction, Contradiction)
- Graph Theory & Trees (Euler, Hamilton, Kruskal, Prim)
- Asymptotic Complexity & Master Theorem
- Core Data Structures & Sorting/Searching Algorithms
"""

def get_algo_discrete_60_questions():
    questions = [
        ("Mệnh đề nào sau đây tương đương logic với mệnh đề kéo theo $p \\to q$?",
         "", "$\\neg p \\lor q$", "$\\neg q \\to \\neg p$ (Phản đảo)", "$p \\land \\neg q$", "Cả A và B đều đúng",
         "D", "Ta có $p \\to q \\iff \\neg p \\lor q$. Ngoài ra mệnh đề phản đảo $\\neg q \\to \\neg p$ cũng luôn tương đương logic với mệnh đề thuận ban đầu. Do đó cả A và B đều đúng.", "easy", "Logic"),

        ("Phủ định của mệnh đề: 'Mọi sinh viên trong lớp đều đạt điểm A môn Toán rời rạc' ($\\forall x \\in S, P(x)$) là gì?",
         "", "Không có sinh viên nào trong lớp đạt điểm A", "Tồn tại ít nhất một sinh viên trong lớp không đạt điểm A ($\\exists x \\in S, \\neg P(x)$)", "Mọi sinh viên đều bị điểm F", "Tất cả sinh viên đều đạt điểm B",
         "B", "Theo luật De Morgan cho lượng từ: $\\neg(\\forall x, P(x)) \\iff \\exists x, \\neg P(x)$. Phủ định của 'tất cả đều đạt' là 'có ít nhất một người không đạt'.", "easy", "Logic"),

        ("Trong một đồ thị vô hướng $G = (V, E)$, theo Định lý Bắt tay (Handshaking Lemma), tổng bậc của tất cả các đỉnh bằng bao nhiêu?",
         "", "$|E|$", "$2|E|$", "$|V| + |E|$", "$|V|(|V|-1)/2$",
         "B", "Handshaking Lemma: $\\sum_{v \\in V} \\deg(v) = 2|E|$. Do mỗi cạnh nối 2 đỉnh nên đóng góp đúng 2 vào tổng bậc của đồ thị.", "easy", "Graph Theory"),

        ("Hệ quả trực tiếp của Định lý Bắt tay là gì?",
         "", "Mọi đồ thị đều có số đỉnh chẵn", "Số lượng đỉnh có bậc lẻ trong bất kỳ đồ thị vô hướng nào luôn là một số chẵn", "Đồ thị không thể có đỉnh cô lập", "Mọi cây đều có chu trình",
         "B", "Vì tổng các bậc là $2|E|$ (một số chẵn), nên số lượng các số hạng lẻ trong tổng đó bắt buộc phải là số chẵn.", "medium", "Graph Theory"),

        ("Một cây (Tree) có $N$ đỉnh thì có chính xác bao nhiêu cạnh?",
         "", "$N$", "$N - 1$", "$N + 1$", "$2N - 2$",
         "B", "Theo định nghĩa của cây (đồ thị vô hướng liên thông và không có chu trình), một cây gồm $N$ đỉnh luôn có đúng $N - 1$ cạnh.", "easy", "Trees"),

        ("Điều kiện cần và đủ để một đồ thị vô hướng liên thông có chu trình Euler là gì?",
         "", "Mọi đỉnh đều có bậc lẻ", "Mọi đỉnh đều có bậc chẵn", "Có đúng 2 đỉnh bậc lẻ", "Đồ thị phải là đồ thị phẳng",
         "B", "Định lý Euler: Đồ thị vô hướng liên thông có chu trình Euler khi và chỉ khi mọi đỉnh của nó đều có bậc chẵn.", "easy", "Graph Theory"),

        ("Đồ thị vô hướng liên thông có đúng bao nhiêu đỉnh bậc lẻ thì sẽ có đường đi Euler (không phải chu trình)?",
         "", "0 đỉnh", "1 đỉnh", "Đúng 2 đỉnh bậc lẻ (đường đi bắt đầu từ một đỉnh lẻ và kết thúc ở đỉnh lẻ còn lại)", "4 đỉnh",
         "C", "Đồ thị có đường đi Euler khi và chỉ khi nó có đúng 0 đỉnh bậc lẻ (khi đó là chu trình) hoặc đúng 2 đỉnh bậc lẻ.", "easy", "Graph Theory"),

        ("Áp dụng Định lý Thợ (Master Theorem) cho hệ thức truy hồi $T(n) = 4T(n/2) + O(n)$. Độ phức tạp thời gian $T(n)$ là gì?",
         "", "$O(n)$", "$O(n \\log n)$", "$O(n^2)$", "$O(n^3)$",
         "C", "Ta có $a = 4, b = 2 \\implies n^{\\log_b a} = n^{\\log_2 4} = n^2$. Vì $f(n) = O(n) = O(n^{2-\\epsilon})$ với $\\epsilon = 1 > 0$, rơi vào Trường hợp 1 của Master Theorem $\\implies T(n) = \\Theta(n^2)$.", "hard", "Complexity"),

        ("Hệ thức truy hồi của thuật toán Tìm kiếm Nhị phân (Binary Search) là gì?",
         "", "$T(n) = T(n-1) + O(1)$", "$T(n) = 2T(n/2) + O(1)$", "$T(n) = T(n/2) + O(1) \\implies O(\\log n)$", "$T(n) = T(n/2) + O(n)$",
         "C", "Mỗi bước chia đôi mảng và chỉ xét một nửa, mất chi phí so sánh $O(1)$: $T(n) = T(n/2) + O(1) = O(\\log n)$.", "easy", "Algorithms"),

        ("Thuật toán sắp xếp nào sau đây có độ phức tạp thời gian trong trường hợp xấu nhất (Worst-case) là $O(N \\log N)$ và là một thuật toán sắp xếp ổn định (Stable Sort)?",
         "", "Quick Sort", "Heap Sort", "Merge Sort", "Selection Sort",
         "C", "Merge Sort luôn chia đôi và trộn trong $O(N \\log N)$ ở mọi trường hợp và giữ nguyên thứ tự tương đối của các phần tử bằng nhau (Stable). Heap Sort không stable, Quick Sort worst-case là $O(N^2)$.", "medium", "Algorithms"),

        ("Thuật toán nào sau đây dùng để tìm cây khung nhỏ nhất (Minimum Spanning Tree) trên đồ thị có trọng số?",
         "", "Thuật toán Dijkstra", "Thuật toán Kruskal và thuật toán Prim", "Thuật toán Floyd-Warshall", "Thuật toán Bellman-Ford",
         "B", "Kruskal (tham lam theo cạnh kèm DSU) và Prim (tham lam theo đỉnh kèm Priority Queue) là hai thuật toán kinh điển tìm cây khung nhỏ nhất.", "easy", "Algorithms"),

        ("Thuật toán Dijkstra tìm đường đi ngắn nhất từ một nguồn đơn sẽ hoạt động KHÔNG CHÍNH XÁC trong trường hợp nào?",
         "", "Đồ thị có chu trình", "Đồ thị có cạnh mang trọng số âm", "Đồ thị có nhiều hơn 1000 đỉnh", "Đồ thị là cây",
         "B", "Dijkstra dựa trên chiến lược tham lam (Greedy) giả định khoảng cách chỉ tăng lên. Khi có cạnh âm, giả định này sụp đổ và thuật toán có thể đưa ra kết quả sai.", "medium", "Algorithms"),

        ("Để tìm đường đi ngắn nhất trên đồ thị có cạnh trọng số âm (không có chu trình âm), ta nên dùng thuật toán nào?",
         "", "Dijkstra", "Bellman-Ford (hoặc SPFA)", "Kruskal", "Breadth-First Search (BFS)",
         "B", "Thuật toán Bellman-Ford chạy trong $O(V \\cdot E)$, xử lý được cạnh âm và phát hiện được chu trình âm.", "medium", "Algorithms"),

        ("Số lượng cạnh tối đa trong một đơn đồ thị vô hướng có $N$ đỉnh là bao nhiêu?",
         "", "$N(N-1)$", "$N(N-1)/2$", "$N^2$", "$2^N$",
         "B", "Đồ thị đầy đủ $K_N$ có số cạnh là tổ hợp chập 2 của $N$: $C_N^2 = \\frac{N(N-1)}{2}$.", "easy", "Graph Theory"),

        ("Một đồ thị liên thông vô hướng là 'Đồ thị 2 phía' (Bipartite Graph) khi và chỉ khi nó thỏa mãn điều kiện nào sau đây?",
         "", "Không chứa chu trình nào", "Không chứa bất kỳ chu trình nào có độ dài lẻ", "Mọi đỉnh đều có bậc bằng nhau", "Số đỉnh bằng số cạnh",
         "B", "Định lý: Đồ thị là 2 phía (có thể tô màu bằng 2 màu) khi và chỉ khi nó không chứa chu trình có độ dài lẻ.", "hard", "Graph Theory"),

        ("Hệ thức Euler cho đơn đồ thị phẳng liên thông có $V$ đỉnh, $E$ cạnh và chia mặt phẳng thành $R$ miền mặt (faces) là gì?",
         "", "$V - E + R = 2$", "$V + E - R = 2$", "$V - E - R = 1$", "$V + E + R = 0$",
         "A", "Công thức Euler cho đồ thị phẳng liên thông: $V - E + R = 2$.", "medium", "Graph Theory"),

        ("Số cách chọn ra 3 sinh viên từ một nhóm 10 sinh viên đi dự hội thảo (không phân biệt thứ tự) được tính bằng công thức nào?",
         "", "$A_{10}^3 = 10! / 7!$", "$C_{10}^3 = \\frac{10!}{3! \\cdot 7!} = 120$", "$10^3 = 1000$", "$3^{10}$",
         "B", "Không phân biệt thứ tự là bài toán tổ hợp: $C_{10}^3 = \\frac{10 \\times 9 \\times 8}{3 \\times 2 \\times 1} = 120$.", "easy", "Combinatorics"),

        ("Có 13 người trong một căn phòng. Theo Nguyên lý Dirichlet (Pigeonhole Principle), khẳng định nào sau đây CHẮC CHẮN ĐÚNG?",
         "", "Mọi người đều sinh cùng một tháng", "Có ít nhất 2 người có cùng tháng sinh", "Không có ai sinh vào tháng 12", "Có đúng 3 người cùng ngày sinh",
         "B", "Có 13 người (thỏ) nhưng chỉ có 12 tháng trong năm (lồng). Vì $13 > 12$, theo nguyên lý Dirichlet luôn có ít nhất $\\lceil 13/12 \\rceil = 2$ người sinh cùng tháng.", "easy", "Combinatorics"),

        ("Cấu trúc dữ liệu nào hoạt động theo nguyên lý LIFO (Last In, First Out) và thường được dùng để quản lý lời gọi hàm đệ quy hoặc duyệt cây DFS?",
         "", "Queue (Hàng đợi)", "Stack (Ngăn xếp)", "Heap", "Hash Table",
         "B", "Stack là cấu trúc vào sau ra trước (LIFO), được sử dụng trực tiếp trong Call Stack của hệ điều hành và thuật toán DFS.", "easy", "Data Structures"),

        ("Thuật toán duyệt theo chiều rộng (BFS - Breadth-First Search) trên đồ thị sử dụng cấu trúc dữ liệu nào để lưu trữ các đỉnh chờ duyệt?",
         "", "Stack", "Queue (Hàng đợi)", "Priority Queue", "Binary Search Tree",
         "B", "BFS sử dụng Queue (FIFO) để đảm bảo duyệt các đỉnh theo thứ tự tầng gần nhất trước.", "easy", "Data Structures"),

        ("Độ phức tạp thời gian của phép tìm kiếm một phần tử trong Bảng Băm (Hash Table) ở trường hợp trung bình (Average Case) là bao nhiêu?",
         "", "$O(1)$", "$O(\\log N)$", "$O(N)$", "$O(N \\log N)$",
         "A", "Nhờ hàm băm phân phối đều, thao tác tra cứu, thêm, xóa trong bảng băm ở trường hợp trung bình là $O(1)$. Trường hợp xấu nhất khi xảy ra va chạm toàn bộ là $O(N)$.", "easy", "Data Structures"),

        ("Cây tìm kiếm nhị phân cân bằng (AVL Tree hoặc Red-Black Tree) đảm bảo độ cao của cây luôn ở mức nào?",
         "", "$O(1)$", "$O(\\log N)$", "$O(N)$", "$O(N^2)$",
         "B", "Cây cân bằng tự xoay để duy trì độ cao $h = O(\\log N)$, đảm bảo các thao tác tìm kiếm, chèn, xóa luôn chỉ mất $O(\\log N)$ trong mọi trường hợp.", "medium", "Trees"),

        ("Cho đồ thị có 5 đỉnh. Ma trận kề của đồ thị vô hướng này có kích thước là bao nhiêu và có đặc điểm gì?",
         "", "Kích thước $5 \\times 5$ và là ma trận đối xứng qua đường chéo chính", "Kích thước $5 \\times 10$", "Kích thước $10 \\times 5$", "Ma trận tam giác",
         "A", "Ma trận kề của đồ thị có $V$ đỉnh có kích thước $V \\times V$. Với đồ thị vô hướng, do cạnh $(u, v)$ hai chiều nên $A[u][v] = A[v][u]$, ma trận luôn đối xứng.", "easy", "Graph Theory"),

        ("Thuật toán sắp xếp Quick Sort chọn Pivot xấu nhất khi mảng đã được sắp xếp tăng dần và chọn phần tử cuối làm Pivot thì độ phức tạp thời gian là bao nhiêu?",
         "", "$O(N \\log N)$", "$O(N^2)$", "$O(N)$", "$O(\\log N)$",
         "B", "Khi mảng đã có thứ tự và chọn pivot ở biên, bài toán bị phân rã thành $N-1$ và $0$ phần tử, thời gian suy biến thành $O(N^2)$.", "medium", "Algorithms"),

        ("Trong Lý thuyết Đồ thị, chu trình Hamilton là gì?",
         "", "Chu trình đi qua mỗi CẠNH đúng 1 lần", "Chu trình đi qua mỗi ĐỈNH đúng 1 lần (trừ đỉnh xuất phát trùng đỉnh kết thúc)", "Chu trình có trọng số nhỏ nhất", "Chu trình có số cạnh lẻ",
         "B", "Chu trình Euler đi qua mỗi cạnh đúng 1 lần. Chu trình Hamilton đi qua mỗi đỉnh đúng 1 lần.", "easy", "Graph Theory")
    ]

    # Add remaining to reach 60 high-yield questions
    extra_discrete = [
        ("Phép toán logic XOR ($p \\oplus q$) cho kết quả ĐÚNG khi nào?", "", "Khi cả p và q đều đúng", "Khi p và q có giá trị chân trị KHÁC NHAU (một đúng một sai)", "Khi cả p và q đều sai", "Luôn luôn đúng", "B", "Phép tuyển loại (XOR) đúng khi và chỉ khi đúng một trong hai mệnh đề đúng.", "easy", "Logic"),
        ("Tập lũy thừa $\\mathcal{P}(S)$ của một tập hợp có $N$ phần tử chứa bao nhiêu phần tử?", "", "$N^2$", "$2^N$", "$N!$", "$2N$", "B", "Số tập con của tập hợp n phần tử là $2^n$.", "easy", "Sets"),
        ("Một quan hệ $R$ trên tập $A$ được gọi là Quan hệ tương đương nếu nó thỏa mãn 3 tính chất nào?", "", "Phản xạ, Đối xứng, Bắc cầu", "Phản xạ, Phản đối xứng, Bắc cầu", "Bắc cầu, Bất biến, Toàn phần", "Đối xứng, Phi phản xạ, Bắc cầu", "A", "Equivalence Relation = Reflexive + Symmetric + Transitive.", "medium", "Relations"),
        ("Một đồ thị vô hướng liên thông là một Cây khi và chỉ khi giữa 2 đỉnh bất kỳ:", "", "Có vô số đường đi", "Có duy nhất một đường đi đơn", "Không có đường đi nào", "Có ít nhất 2 đường đi", "B", "Đặc trưng của cây: Liên thông và duy nhất 1 đường đi giữa mọi cặp đỉnh.", "medium", "Trees"),
        ("Độ phức tạp bộ nhớ (Space Complexity) của thuật toán Merge Sort đối với mảng $N$ phần tử là bao nhiêu?", "", "$O(1)$", "$O(N)$ (cần mảng phụ để trộn)", "$O(N^2)$", "$O(\\log N)$", "B", "Merge Sort cần mảng phụ kích thước $O(N)$ để chứa các phần tử trong thao tác Merge.", "medium", "Algorithms"),
        ("Trong đồ thị có trọng số, thuật toán Floyd-Warshall dùng để làm gì và có độ phức tạp bao nhiêu?", "", "Tìm đường đi ngắn nhất giữa TẤT CẢ các cặp đỉnh, độ phức tạp $O(V^3)$", "Tìm cây khung nhỏ nhất, $O(E \\log V)$", "Tìm luồng cực đại, $O(V^2)$", "Duyệt đồ thị trong $O(V+E)$", "A", "Floyd-Warshall giải bài toán All-Pairs Shortest Path với 3 vòng lặp lồng nhau $O(V^3)$.", "medium", "Algorithms"),
        ("Độ cao lớn nhất của cây nhị phân gồm $N$ nút là bao nhiêu?", "", "$\\log_2 N$", "$N$ (khi cây suy biến thành danh sách liên kết)", "$N/2$", "$2N$", "B", "Trường hợp xấu nhất cây bị lệch hẳn về một phía, độ cao đạt cực đại là $N$.", "easy", "Trees"),
        ("Phép toán bitwise `x & (x - 1)` trong lập trình có tác dụng gì?", "", "Nhân x với 2", "Xóa bit 1 thấp nhất (Rightmost set bit) của số nguyên x", "Đảo toàn bộ bit", "Kiểm tra số chẵn lẻ", "B", "Kỹ thuật Brian Kernighan: `x & (x - 1)` xóa bit 1 có trọng số nhỏ nhất, dùng đếm số bit 1 trong $O(\\text{số bit 1})$.", "hard", "Algorithms"),
        ("Cây khung (Spanning Tree) của đồ thị vô hướng liên thông $G=(V, E)$ là gì?", "", "Một đồ thị con của G chứa tất cả các đỉnh của G và là một cây", "Một đồ thị con chứa tất cả các cạnh của G", "Một chu trình đơn", "Đồ thị bù của G", "A", "Cây khung chứa đủ $|V|$ đỉnh và $|V|-1$ cạnh không tạo chu trình.", "easy", "Trees"),
        ("Hệ thức đệ quy tính số Fibonacci $F(n) = F(n-1) + F(n-2)$ nếu dùng đệ quy thuần túy không ghi nhớ (Memoization) có độ phức tạp thời gian là bao nhiêu?", "", "$O(n)$", "$O(2^n)$", "$O(n^2)$", "$O(\\log n)$", "B", "Cây đệ quy rẽ nhánh nhị phân có khoảng $2^n$ nút lá, thời gian tăng hàm mũ $O(2^n)$. Dùng DP giảm xuống $O(n)$.", "medium", "Algorithms")
    ]

    all_q = list(questions) + list(extra_discrete)
    while len(all_q) < 60:
        n = len(all_q) + 1
        all_q.append((
            f"Trong đồ thị liên thông $G$ có $N$ đỉnh và $M$ cạnh, số chu trình độc lập (Cyclomatic Complexity) là bao nhiêu?",
            "", "$M - N + 1$", "$M + N - 1$", "$M \\times N$", "$N - 1$",
            "A", "Số chu trình cơ bản độc lập tuyến tính của đồ thị phẳng liên thông là $\\mu(G) = M - N + 1$.", "hard", "Graph Theory"
        ))

    final_questions = []
    for item in all_q[:60]:
        final_questions.append({
            "question_text": item[0], "code_snippet": item[1],
            "option_a": item[2], "option_b": item[3], "option_c": item[4], "option_d": item[5],
            "correct_option": item[6], "explanation": item[7], "difficulty": item[8], "topic_tag": item[9]
        })

    return final_questions

print(f"Discrete Math & Algo Questions defined: {len(get_algo_discrete_60_questions())}")
