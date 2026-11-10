"""
5 University-Level Essay Exam Prompts for Discrete Mathematics & Algorithms
Each prompt contains:
- title, topic, subject_code
- problem description (with LaTeX math)
- scoring rubric breakdown (Thang 10: Logic, Base case, Induction, Edge case, Complexity)
- model solution (10/10)
"""

ESSAY_PROMPTS = [
    {
        "id": "ESSAY_01",
        "subject_code": "DISCRETE_MATH_ALGO",
        "topic": "Logic Mệnh Đề & Suy Diễn Hợp Lý",
        "title": "Đề 1: Chứng Minh Tương Đương Logic & Quy Tắc Suy Diễn",
        "question_text": r"""Cho các mệnh đề logic $p, q, r$.
1. Hãy chứng minh bằng các luật tương đương logic (không dùng bảng chân trị) rằng:
$$(p \to r) \land (q \to r) \iff (p \lor q) \to r$$
2. Phân tích tính hợp lệ của lập luận sau bằng quy tắc suy diễn:
- Tiền đề 1: Nếu trời mưa ($p$), thì đường trơn ($q$).
- Tiền đề 2: Đường trơn ($q$) hoặc xe buýt chạy đúng giờ ($r$).
- Tiền đề 3: Xe buýt không chạy đúng giờ ($\neg r$).
- Kết luận: Vậy trời mưa ($p$).
Hãy chỉ ra lập luận trên đúng hay ngụy biện (nêu tên lỗi ngụy biện nếu có).""",
        "rubric": {
            "max_score": 10.0,
            "criteria": [
                {"item": "Biến đổi tương đương logic bước 1 (p -> r = ~p v r)", "points": 2.0},
                {"item": "Áp dụng luật phân phối/kết hợp chính xác", "points": 2.0},
                {"item": "Chuyển về dạng (~p ^ ~q) v r = ~(p v q) v r = (p v q) -> r", "points": 1.0},
                {"item": "Phân tích tiền đề 2 và 3 dẫn đến q (Modus Tollendo Ponens)", "points": 2.5},
                {"item": "Chỉ ra khẳng định hệ quả là ngụy biện (Fallacy of Affirming the Consequent)", "points": 2.5}
            ]
        },
        "model_solution": r"""### PHẦN 1: CHỨNG MINH TƯƠNG ĐƯƠNG LOGIC
Ta biến đổi vế trái (VT):
$$VT = (p \to r) \land (q \to r)$$
- Áp dụng luật kéo theo ($A \to B \iff \neg A \lor B$):
$$VT \iff (\neg p \lor r) \land (\neg q \lor r)$$
- Áp dụng luật phân phối của phép hội đối với phép tuyển:
$$VT \iff (\neg p \land \neg q) \lor r$$
- Áp dụng luật De Morgan ($\neg p \land \neg q \iff \neg(p \lor q)$):
$$VT \iff \neg(p \lor q) \lor r$$
- Áp dụng ngược lại luật kéo theo:
$$VT \iff (p \lor q) \to r = VP \quad (\text{đpcm})$$

### PHẦN 2: PHÂN TÍCH LẬP LUẬN
- Từ Tiền đề 2 ($q \lor r$) và Tiền đề 3 ($\neg r$), theo quy tắc tam đoạn luận tuyển (Disjunctive Syllogism):
  Ta suy ra được: $q$ (Đường trơn là ĐÚNG).
- Tiếp theo, xét Tiền đề 1: $p \to q$ (Nếu trời mưa thì đường trơn).
  Ta đã biết $q$ đúng, từ đó người lập luận kết luận rằng $p$ đúng (Trời mưa).
- **Kết luận:** Lập luận trên là **NGỤY BIỆN KHẲNG ĐỊNH HỆ QUẢ (Fallacy of Affirming the Consequent)**.
  Đường có thể trơn do xe tưới nước rửa đường, tuyết tan, hoặc dầu loang chứ không nhất thiết do trời mưa ($q$ đúng không đảm bảo $p$ phải đúng)."""
    },
    {
        "id": "ESSAY_02",
        "subject_code": "DISCRETE_MATH_ALGO",
        "topic": "Quy Nạp Toán Học & Nguyên Lý Dirichlet",
        "title": "Đề 2: Chứng Minh Quy Nạp & Ứng Dụng Nguyên Lý Dirichlet",
        "question_text": r"""1. Bằng phương pháp quy nạp toán học, hãy chứng minh rằng với mọi số nguyên dương $n \ge 1$:
$$1^2 + 2^2 + 3^2 + \dots + n^2 = \frac{n(n + 1)(2n + 1)}{6}$$
2. Cho một tập hợp $S$ gồm $n + 1$ số nguyên dương phân biệt thuộc đoạn $[1, 2n]$. Hãy dùng nguyên lý Dirichlet (Pigeonhole Principle) để chứng minh rằng: luôn tồn tại ít nhất hai số $a, b \in S$ sao cho $a$ chia hết cho $b$ (hoặc $b$ chia hết cho $a$).""",
        "rubric": {
            "max_score": 10.0,
            "criteria": [
                {"item": "Bước cơ sở (Base Case) với n = 1", "points": 1.5},
                {"item": "Giả thiết quy nạp (Inductive Hypothesis) với n = k", "points": 1.5},
                {"item": "Bước quy nạp: Biến đổi tổng k + 1 và rút gọn đại số chính xác", "points": 3.0},
                {"item": "Biểu diễn mỗi số nguyên dương dưới dạng 2^k * m (m lẻ)", "points": 2.0},
                {"item": "Áp dụng nguyên lý Dirichlet xác định số lồng và số thỏ suy ra đpcm", "points": 2.0}
            ]
        },
        "model_solution": r"""### PHẦN 1: CHỨNG MINH QUY NẠP TOÁN HỌC
Đặt mệnh đề cần chứng minh là $P(n): \sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6}$.
- **Bước cơ sở ($n = 1$):**
  - $VT = 1^2 = 1$.
  - $VP = \frac{1(1+1)(2\cdot 1 + 1)}{6} = \frac{1 \cdot 2 \cdot 3}{6} = 1$.
  - Do $VT = VP$, $P(1)$ đúng.
- **Giả thiết quy nạp:** Giả sử $P(k)$ đúng với $k \ge 1$, nghĩa là:
  $$\sum_{i=1}^k i^2 = \frac{k(k+1)(2k+1)}{6}$$
- **Bước quy nạp:** Ta cần chứng minh $P(k+1)$ đúng, tức là:
  $$\sum_{i=1}^{k+1} i^2 = \frac{(k+1)(k+2)(2(k+1)+1)}{6} = \frac{(k+1)(k+2)(2k+3)}{6}$$
  Thật vậy:
  $$\sum_{i=1}^{k+1} i^2 = \left(\sum_{i=1}^k i^2\right) + (k+1)^2 = \frac{k(k+1)(2k+1)}{6} + (k+1)^2$$
  Đặt nhân tử chung $(k+1)$:
  $$= (k+1) \left[\frac{k(2k+1) + 6(k+1)}{6}\right] = (k+1) \left[\frac{2k^2 + 7k + 6}{6}\right]$$
  Phân tích tam thức bậc hai $2k^2 + 7k + 6 = (k+2)(2k+3)$:
  $$= \frac{(k+1)(k+2)(2k+3)}{6} \quad (\text{đpcm})$$
  Theo nguyên lý quy nạp toán học, công thức đúng với mọi $n \ge 1$.

### PHẦN 2: ỨNG DỤNG NGUYÊN LÝ DIRICHLET
- Mọi số nguyên dương $x \in S$ đều có thể biểu diễn duy nhất dưới dạng:
  $$x = 2^k \cdot m$$
  Trong đó $k \ge 0$ là số mũ tự nhiên và $m$ là một số nguyên lẻ.
- Vì $x \in [1, 2n]$, nên ước lẻ $m$ cũng nằm trong khoảng $[1, 2n]$.
- Số lượng số lẻ trong khoảng $[1, 2n]$ đúng bằng $n$ (đó là $1, 3, 5, \dots, 2n-1$).
- Tập $S$ có $n + 1$ phần tử (tương ứng với $n + 1$ chú thỏ), nhưng chỉ có tối đa $n$ giá trị lẻ $m$ khả dĩ (tương ứng với $n$ chiếc chuồng).
- Theo nguyên lý Dirichlet, tồn tại ít nhất 2 số phân biệt $a, b \in S$ có cùng giá trị phần lẻ $m$:
  $$a = 2^i \cdot m, \quad b = 2^j \cdot m \quad (i \neq j)$$
- Không mất tính tổng quát, giả sử $i > j$, khi đó:
  $$\frac{a}{b} = \frac{2^i \cdot m}{2^j \cdot m} = 2^{i-j} \in \mathbb{Z}^+$$
  Nghĩa là $a$ chia hết cho $b$ ($\text{đpcm}$)."""
    },
    {
        "id": "ESSAY_03",
        "subject_code": "DISCRETE_MATH_ALGO",
        "topic": "Lý Thuyết Đồ Thị & Cây Khung Nhỏ Nhất",
        "title": "Đề 3: Thuật Toán Kruskal, Prim & Chu Trình Euler",
        "question_text": r"""1. Phát biểu Định lý Euler về điều kiện cần và đủ để một đồ thị vô hướng liên thông $G = (V, E)$ có chu trình Euler và đường đi Euler. Chứng minh chiều thuận: Nếu đồ thị có chu trình Euler thì mọi đỉnh đều có bậc chẵn.
2. So sánh nguyên lý hoạt động của hai thuật toán tìm cây khung nhỏ nhất (MST): Thuật toán Kruskal và Thuật toán Prim:
- Cấu trúc dữ liệu tối ưu thường dùng cho từng thuật toán (Disjoint Set Union vs Min-Heap/Priority Queue).
- Đánh giá độ phức tạp thời gian của cả hai thuật toán và cho biết trường hợp nào nên ưu tiên dùng Kruskal, trường hợp nào nên dùng Prim.""",
        "rubric": {
            "max_score": 10.0,
            "criteria": [
                {"item": "Phát biểu chính xác điều kiện Euler cho chu trình và đường đi", "points": 2.0},
                {"item": "Chứng minh chiều thuận bậc chẵn bằng tính chất 'vào - ra' tại mỗi đỉnh", "points": 2.5},
                {"item": "Phân tích nguyên lý Kruskal (Greedy theo cạnh) & Prim (Greedy theo đỉnh)", "points": 2.5},
                {"item": "Cấu trúc dữ liệu DSU, Priority Queue và độ phức tạp O(E log V)", "points": 1.5},
                {"item": "So sánh đồ thị thưa (Sparse Graph) vs đồ thị dày (Dense Graph)", "points": 1.5}
            ]
        },
        "model_solution": r"""### PHẦN 1: ĐỊNH LÝ EULER
- **Định lý:**
  - Một đồ thị vô hướng liên thông $G$ có chu trình Euler khi và chỉ khi mọi đỉnh của nó đều có bậc chẵn ($\deg(v) \equiv 0 \pmod 2, \forall v \in V$).
  - Đồ thị có đường đi Euler khi và chỉ khi nó có đúng 0 hoặc 2 đỉnh bậc lẻ.
- **Chứng minh chiều thuận:**
  - Giả sử $G$ có chu trình Euler $C = v_0 e_1 v_1 e_2 \dots e_m v_0$.
  - Khi đi dọc theo chu trình $C$, mỗi lần chu trình đi qua một đỉnh $v$: nó đi vào $v$ qua một cạnh và rời khỏi $v$ qua một cạnh khác. Mỗi lần đi qua như vậy đóng góp đúng $2$ vào bậc của $v$.
  - Đối với đỉnh xuất phát $v_0$, chu trình bắt đầu bằng một cạnh đi ra và kết thúc bằng một cạnh đi vào, tổng cộng cũng đóng góp $2$.
  - Do mỗi cạnh trong $E$ được đi qua đúng 1 lần duy nhất, tổng số cạnh liên thuộc với mỗi đỉnh $v$ phải là một số chẵn: $\deg(v)$ chẵn với mọi $v \in V$ ($\text{đpcm}$).

### PHẦN 2: SO SÁNH THUẬT TOÁN KRUSKAL VÀ PRIM
| Tiêu chí | Thuật toán Kruskal | Thuật toán Prim |
| :--- | :--- | :--- |
| **Tư tưởng giải thuật** | Chọn cạnh có trọng số nhỏ nhất không tạo thành chu trình (Edge-centric). | Phát triển cây từ một đỉnh gốc, luôn chọn cạnh nối cây với đỉnh ngoài có trọng số nhỏ nhất (Vertex-centric). |
| **Cấu trúc dữ liệu** | **Disjoint Set Union (DSU)** với kỹ thuật Path Compression & Union by Rank. | **Hàng đợi ưu tiên (Min-Heap / Fibonacci Heap)** để lấy đỉnh có khoảng cách nhỏ nhất. |
| **Độ phức tạp** | $O(E \log E) = O(E \log V)$ (do thao tác sắp xếp cạnh chiếm ưu thế). | $O(E \log V)$ với Binary Heap, hoặc $O(E + V \log V)$ với Fibonacci Heap. |
| **Ứng dụng tối ưu** | Rất hiệu quả cho **đồ thị thưa (Sparse Graph)** khi $E \approx V$. | Rất hiệu quả cho **đồ thị dày (Dense Graph)** khi $E \approx V^2$ (đặc biệt khi dùng ma trận kề $O(V^2)$). |"""
    },
    {
        "id": "ESSAY_04",
        "subject_code": "DISCRETE_MATH_ALGO",
        "topic": "Thuật Toán Sắp Xếp & Bất Biến Vòng Lặp",
        "title": "Đề 4: Merge Sort, Bất Biến Vòng Lặp & Định Lý Thợ (Master Theorem)",
        "question_text": r"""1. Viết mã giả (Pseudocode) cho thuật toán sắp xếp trộn (Merge Sort) bao gồm hàm `MergeSort(A, p, r)` và hàm `Merge(A, p, q, r)`.
2. Chứng minh tính đúng đắn của hàm `Merge` bằng phương pháp Bất biến vòng lặp (Loop Invariant):
- Khởi tạo (Initialization).
- Duy trì (Maintenance).
- Kết thúc (Termination).
3. Thiết lập hệ thức truy hồi thời gian chạy của Merge Sort và dùng Định lý Thợ (Master Theorem) để chứng minh độ phức tạp thời gian trong mọi trường hợp là $\Theta(n \log n)$.""",
        "rubric": {
            "max_score": 10.0,
            "criteria": [
                {"item": "Mã giả MergeSort và Merge rõ ràng, đúng chuẩn", "points": 2.5},
                {"item": "Phát biểu chính xác bất biến vòng lặp trong hàm Merge", "points": 1.5},
                {"item": "Chứng minh đủ 3 bước: Khởi tạo, Duy trì, Kết thúc", "points": 3.0},
                {"item": "Thiết lập hệ thức truy hồi T(n) = 2T(n/2) + O(n)", "points": 1.5},
                {"item": "Áp dụng đúng trường hợp 2 của Master Theorem ra Theta(n log n)", "points": 1.5}
            ]
        },
        "model_solution": r"""### PHẦN 1: MÃ GIẢ MERGE SORT
```text
Algorithm Merge(A, p, q, r):
    n1 = q - p + 1
    n2 = r - q
    create arrays L[0..n1-1] and R[0..n2-1]
    for i = 0 to n1-1: L[i] = A[p + i]
    for j = 0 to n2-1: R[j] = A[q + 1 + j]
    
    i = 0, j = 0, k = p
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            A[k] = L[i]
            i = i + 1
        else:
            A[k] = R[j]
            j = j + 1
        k = k + 1
    while i < n1:
        A[k] = L[i]; i = i + 1; k = k + 1
    while j < n2:
        A[k] = R[j]; j = j + 1; k = k + 1

Algorithm MergeSort(A, p, r):
    if p < r:
        q = floor((p + r) / 2)
        MergeSort(A, p, q)
        MergeSort(A, q + 1, r)
        Merge(A, p, q, r)
```

### PHẦN 2: CHỨNG MINH BẰNG BẤT BIẾN VÒNG LẶP (LOOP INVARIANT)
- **Phát biểu bất biến:** Tại đầu mỗi vòng lặp `while`, mảng con $A[p \dots k-1]$ chứa $k-p$ phần tử nhỏ nhất của $L[0 \dots n_1-1]$ và $R[0 \dots n_2-1]$ theo thứ tự đã sắp xếp. Ngoài ra, $L[i]$ và $R[j]$ là các phần tử nhỏ nhất chưa được sao chép trở lại vào mảng $A$.
- **Khởi tạo (Initialization):** Trước vòng lặp đầu tiên, $k = p$, mảng con $A[p \dots p-1]$ rỗng (0 phần tử), hiển nhiên thỏa mãn tính sắp xếp. $i = 0, j = 0$, $L[0]$ và $R[0]$ là phần tử nhỏ nhất của $L$ và $R$.
- **Duy trì (Maintenance):** Giả sử bất biến đúng ở bước $k$. Nếu $L[i] \le R[j]$, thì $L[i]$ là phần tử nhỏ nhất chưa vào $A$. Vì $A[p \dots k-1]$ đã chứa các phần tử nhỏ hơn, gán $A[k] = L[i]$ sẽ mở rộng mảng $A[p \dots k]$ vẫn giữ nguyên thứ tự sắp xếp. Sau đó tăng $i$ và $k$, bất biến được bảo toàn cho vòng lặp kế tiếp. Trường hợp $R[j] < L[i]$ chứng minh tương tự.
- **Kết thúc (Termination):** Vòng lặp dừng khi $i = n_1$ hoặc $j = n_2$. Hai vòng lặp phụ sao chép các phần tử còn lại (vốn đã lớn hơn tất cả phần tử trong $A[p \dots k-1]$). Khi đó toàn bộ mảng con $A[p \dots r]$ được sắp xếp hoàn chỉnh.

### PHẦN 3: PHÂN TÍCH ĐỘ PHỨC TẠP BẰNG MASTER THEOREM
- Hệ thức truy hồi của Merge Sort:
  $$T(n) = 2T(n/2) + \Theta(n)$$
  Trong đó:
  - $a = 2$: Số bài toán con.
  - $b = 2$: Tỷ lệ chia kích thước dữ liệu đầu vào.
  - $f(n) = \Theta(n)$: Chi phí của hàm `Merge`.
- Ta có $n^{\log_b a} = n^{\log_2 2} = n^1 = n$.
- So sánh $f(n)$ với $n^{\log_b a}$: Ta thấy $f(n) = \Theta(n^{\log_b a}) = \Theta(n)$.
- Áp dụng **Trường hợp 2 của Định lý Thợ (Master Theorem Case 2)**:
  $$T(n) = \Theta(n^{\log_b a} \log n) = \Theta(n \log n)$$
- Do không phụ thuộc vào trạng thái dữ liệu đầu vào (tốt nhất, xấu nhất hay trung bình), độ phức tạp thời gian luôn là $\Theta(n \log n)$."""
    },
    {
        "id": "ESSAY_05",
        "subject_code": "DISCRETE_MATH_ALGO",
        "topic": "Đường Đi Ngắn Nhất & Thuật Toán Dijkstra",
        "title": "Đề 5: Thuật Toán Dijkstra, Truy Vết & Bài Toán Cạnh Trọng Số Âm",
        "question_text": r"""1. Trình bày thuật toán Dijkstra tìm đường đi ngắn nhất từ một đỉnh nguồn $s$ đến tất cả các đỉnh còn lại trên đồ thị có trọng số không âm $G = (V, E, w)$:
- Nêu cấu trúc dữ liệu mảng khoảng cách `dist[]` và mảng truy vết `parent[]`.
- Trình bày thao tác thư giãn cạnh (Relaxation).
2. Cho đồ thị có 3 đỉnh $A, B, C$ với các cạnh có trọng số:
- $w(A, B) = 3$
- $w(A, C) = 5$
- $w(B, C) = -4$
Hãy chạy mô phỏng thuật toán Dijkstra xuất phát từ đỉnh $A$ và giải thích tại sao thuật toán cho kết quả SAI khi đồ thị tồn tại cạnh có trọng số âm.
3. Đề xuất thuật toán thay thế có khả năng xử lý cạnh trọng số âm và phát hiện chu trình âm (Negative Cycle).""",
        "rubric": {
            "max_score": 10.0,
            "criteria": [
                {"item": "Trình bày thuật toán Dijkstra và thao tác Relaxation dist[v] > dist[u] + w(u,v)", "points": 3.0},
                {"item": "Mô phỏng chính xác các bước trên đồ thị mẫu A, B, C", "points": 2.5},
                {"item": "Giải thích nguyên nhân cốt lõi (Greedy chọn đỉnh cố định không bao giờ cập nhật lại)", "points": 2.5},
                {"item": "Đề xuất thuật toán Bellman-Ford O(V*E) và thuật toán SPFA", "points": 2.0}
            ]
        },
        "model_solution": r"""### PHẦN 1: THUẬT TOÁN DIJKSTRA
- **Khởi tạo:**
  - `dist[s] = 0`, `dist[v] = +infinity` với mọi $v \neq s$.
  - `parent[v] = null` với mọi $v$.
  - Tập đỉnh đã chốt khoảng cách tối ưu $S = \emptyset$.
- **Thao tác Thư giãn (Relaxation):** Với cạnh $(u, v)$ có trọng số $w(u, v)$:
  $$\text{Nếu } dist[u] + w(u, v) < dist[v] \implies dist[v] = dist[u] + w(u, v); \quad parent[v] = u$$
- **Vòng lặp:** Tại mỗi bước, chọn đỉnh $u \notin S$ có `dist[u]` nhỏ nhất, đưa $u$ vào $S$, sau đó tiến hành thư giãn tất cả các cạnh đi ra từ $u$. Lặp lại cho đến khi mọi đỉnh đều thuộc $S$.

### PHẦN 2: MÔ PHỎNG VÀ NGUYÊN NHÂN DIJKSTRA THẤT BẠI VỚI CẠNH ÂM
- Xét đồ thị: Cạnh $(A, B) = 3$, $(A, C) = 5$, $(B, C) = -4$. Đỉnh nguồn $s = A$.
- **Bước 1:** Khởi tạo `dist[A] = 0`, `dist[B] = \infty`, `dist[C] = \infty`.
- **Bước 2:** Chọn đỉnh có khoảng cách nhỏ nhất chưa chốt là $A$. Chốt $A$ vào $S$. Thư giãn các đỉnh kề:
  - `dist[B] = 0 + 3 = 3`.
  - `dist[C] = 0 + 5 = 5`.
- **Bước 3:** Trong các đỉnh chưa chốt $\{B, C\}$, đỉnh $B$ có `dist[B] = 3 < dist[C] = 5`. Dijkstra chọn chốt $B$ vào $S$. Thư giãn kề của $B$:
  - Cạnh $(B, C) = -4$: `dist[C] = min(5, dist[B] - 4) = min(5, 3 - 4) = -1`.
- **Bây giờ xét tình huống:** Nếu đỉnh $C$ vốn đã được chốt trước (hoặc giả sử đồ thị có thêm cạnh từ $C$ quay lại ảnh hưởng đến $B$):
  - **Bản chất sai lầm của Dijkstra:** Thuật toán dựa trên chiến lược tham lam (**Greedy**). Dijkstra mặc định rằng một khi đỉnh $u$ được chốt vào tập $S$, thì khoảng cách `dist[u]` đã là tối ưu toàn cục và **không bao giờ có thể giảm bớt được nữa**. Giả định này chỉ đúng khi mọi trọng số cạnh $w \ge 0$.
  - Khi có cạnh trọng số âm, một đường đi qua nhiều cạnh hơn lại có thể có tổng trọng số nhỏ hơn một cạnh đơn, phá vỡ tính chất đơn điệu tăng dần của khoảng cách, khiến Dijkstra cho kết quả sai lầm hoặc rơi vào vòng lặp vô tận nếu có chu trình âm.

### PHẦN 3: THUẬT TOÁN THAY THẾ
- Để giải quyết đồ thị có cạnh trọng số âm, ta sử dụng **Thuật toán Bellman-Ford**:
  - Thư giãn tất cả $|E|$ cạnh liên tục qua $|V| - 1$ vòng lặp. Độ phức tạp $O(V \cdot E)$.
  - Vòng lặp thứ $|V|$ nếu vẫn còn cạnh thư giãn được thì kết luận đồ thị chứa **Chu trình trọng số âm (Negative Cycle)**.
- Ngoài ra có thể dùng **SPFA (Shortest Path Faster Algorithm)** cải tiến bằng hàng đợi Queue để tăng tốc trong thực tế."""
    }
]

print(f"Loaded {len(ESSAY_PROMPTS)} essay exam prompts.")
