import sqlite3

def seed_more():
    conn = sqlite3.connect('unimaster.db')
    c = conn.cursor()
    sid = 21

    more_qs = [
        (
            sid,
            "Cấu trúc dữ liệu Bảng băm (Hash Table) giải quyết xung đột (Collision) bằng phương pháp 'Dò tuyến tính' (Linear Probing) có nhược điểm lớn nhất là gì?",
            "Hiện tượng gom cụm sơ cấp (Primary Clustering), làm tăng số phép dò tìm.",
            "Không thể lưu trữ được chuỗi ký tự.",
            "Tốn bộ nhớ gấp đôi phương pháp Bảng băm liên kết (Chaining).",
            "Độ phức tạp trường hợp tốt nhất là $O(n^2)$.",
            "A",
            "Linear Probing $h(k, i) = (h'(k) + i) \\bmod m$ làm cho các khóa bị băm vào cùng một vùng tạo thành các khối ô bị chiếm liên tiếp, làm giảm hiệu suất tìm kiếm."
        ),
        (
            sid,
            "Để biểu diễn một đồ thị thưa (Sparse Graph - số cạnh $E \\ll V^2$), cấu trúc dữ liệu nào sau đây là TỐI ƯU NHẤT về mặt bộ nhớ?",
            "Danh sách kề (Adjacency List)",
            "Ma trận kề (Adjacency Matrix)",
            "Ma trận liên thuộc (Incidence Matrix)",
            "Mảng 2 chiều kích thước $V \\times V$",
            "A",
            "Danh sách kề tốn bộ nhớ $O(V + E)$, trong khi Ma trận kề luôn tốn $O(V^2)$ bất kể đồ thị có ít cạnh đến đâu."
        ),
        (
            sid,
            "Thuật toán sắp xếp Topo (Topological Sort) CHỈ CÓ THỂ áp dụng cho loại đồ thị nào sau đây?",
            "Đồ thị có hướng không có chu trình (DAG - Directed Acyclic Graph)",
            "Đồ thị vô hướng liên thông",
            "Mọi loại đồ thị có hướng (kể cả có chu trình)",
            "Đồ thị đầy đủ $K_n$",
            "A",
            "Topological Sort sắp xếp các đỉnh sao cho mọi cung $(u, v)$ thì $u$ đứng trước $v$. Nếu đồ thị có chu trình, sẽ có sự phụ thuộc vòng tròn và không thể sắp xếp được."
        ),
        (
            sid,
            "Thuật toán Kruskal tìm cây khung nhỏ nhất (MST) sử dụng cấu trúc dữ liệu nào để kiểm tra và hợp nhất hai tập hợp đỉnh mà không tạo chu trình?",
            "Cấu trúc các tập hợp rời nhau (Disjoint Set Union - DSU / Union-Find)",
            "Hàng đợi ưu tiên (Priority Queue / Heap)",
            "Ngăn xếp (Stack)",
            "Bảng băm (Hash Table)",
            "A",
            "DSU với hai thao tác `Find(u)` và `Union(u, v)` (kèm nén đường đi Path Compression và gộp theo hạng) giúp kiểm tra hai đỉnh có thuộc cùng thành phần liên thông hay không trong thời gian gần như $O(1)$ ($O(\\alpha(V))$)."
        ),
        (
            sid,
            "Độ phức tạp thời gian của thuật toán Kruskal trên đồ thị có $V$ đỉnh và $E$ cạnh là:",
            "$O(E \\log E)$ (hoặc $O(E \\log V)$)",
            "$O(V^2)$",
            "$O(V \\log V)$",
            "$O(V + E)$",
            "A",
            "Bước tốn thời gian nhất trong Kruskal là sắp xếp $E$ cạnh theo trọng số tăng dần: $O(E \\log E)$. Vì $E \\leq V^2$, nên $\\log E = O(\\log V)$, tổng thời gian là $O(E \\log V)$."
        ),
        (
            sid,
            "Thuật toán Prim tìm cây khung nhỏ nhất (MST) cài đặt bằng Hàng đợi ưu tiên (Min-Heap / Binary Heap) có độ phức tạp thời gian là:",
            "$O(E \\log V)$",
            "$O(V^2)$",
            "$O(V \\cdot E)$",
            "$O(E^2)$",
            "A",
            "Với Binary Heap, mỗi thao tác `Extract-Min` mất $O(\\log V)$ (chạy $V$ lần), và mỗi thao tác giảm khóa `Decrease-Key` mất $O(\\log V)$ (chạy tối đa $E$ lần), tổng cộng $O((V + E) \\log V) = O(E \\log V)$."
        ),
        (
            sid,
            "Thuật toán nào sau đây tìm đường đi ngắn nhất giữa TẤT CẢ các cặp đỉnh (All-Pairs Shortest Path) trên đồ thị có độ phức tạp $O(V^3)$?",
            "Thuật toán Floyd-Warshall (Quy hoạch động)",
            "Thuật toán Bellman-Ford",
            "Thuật toán Dijkstra",
            "Thuật toán Kruskal",
            "A",
            "Floyd-Warshall sử dụng quy hoạch động với 3 vòng lặp lồng nhau qua đỉnh trung gian $k$: $D[i][j] = \\min(D[i][j], D[i][k] + D[k][j])$, thời gian chạy là $\\Theta(V^3)$."
        ),
        (
            sid,
            "Hàng đợi ưu tiên (Priority Queue) hỗ trợ thao tác chèn phần tử `Insert` và lấy ra phần tử ưu tiên nhất `Extract-Min/Max` với độ phức tạp thời gian là bao nhiêu khi cài bằng Binary Heap?",
            "$O(\\log n)$ cho cả hai thao tác",
            "$O(1)$ cho cả hai thao tác",
            "$O(n)$ cho cả hai thao tác",
            "$O(1)$ cho chèn và $O(n)$ cho lấy ra",
            "A",
            "Binary Heap có cấu trúc cây nhị phân gần hoàn chỉnh, chiều cao $\\lfloor \\log_2 n \\rfloor$. Cả thao tác nổi lên (Percolate Up) khi chèn và chìm xuống (Percolate Down) khi xóa đều tốn thời gian tỉ lệ thuận với chiều cao $O(\\log n)$."
        ),
        (
            sid,
            "Thuật toán duyệt theo chiều sâu (DFS - Depth-First Search) có thể dùng để phát hiện chu trình trên đồ thị có hướng bằng cách phát hiện loại cạnh nào?",
            "Cạnh ngược (Back Edge - trỏ về một tổ tiên trên cây DFS)",
            "Cạnh tới (Forward Edge)",
            "Cạnh chéo (Cross Edge)",
            "Cạnh cây (Tree Edge)",
            "A",
            "Trong DFS trên đồ thị có hướng, các đỉnh được tô màu: Trắng (chưa thăm), Xám (đang duyệt trong stack), Đen (đã duyệt xong). Nếu gặp một cạnh trỏ đến đỉnh màu Xám, đó là Cạnh ngược (Back Edge) chứng tỏ đồ thị có chu trình."
        ),
        (
            sid,
            "Cho mảng $A = [5, 2, 8, 1, 9]$. Sau bước phân hoạch đầu tiên của Quick Sort chọn Pivot là phần tử cuối cùng (Pivot = 9), mảng sẽ có trạng thái nào?",
            "Tất cả các phần tử nhỏ hơn 9 nằm bên trái, 9 đứng ở vị trí cuối cùng.",
            "Mảng được sắp xếp hoàn toàn.",
            "Pivot 9 đứng ở vị trí đầu tiên.",
            "Mảng bị chia thành 2 nửa bằng nhau.",
            "A",
            "Vì 9 là phần tử lớn nhất trong mảng, tất cả các phần tử $5, 2, 8, 1$ đều nhỏ hơn 9 nên đều nằm bên trái của 9, vị trí của 9 sau phân hoạch chính là vị trí cuối cùng."
        ),
        (
            sid,
            "Thuật toán sắp xếp nào sau đây KHÔNG THỰC HIỆN việc so sánh giá trị giữa các phần tử trong mảng?",
            "Radix Sort (Sắp xếp theo cơ số)",
            "Quick Sort",
            "Merge Sort",
            "Heap Sort",
            "A",
            "Radix Sort phân phối các phần tử vào các xô (bucket) theo từng chữ số từ hàng đơn vị đến hàng cao nhất, không so sánh trực tiếp 2 phần tử."
        ),
        (
            sid,
            "Số phép so sánh trong trường hợp xấu nhất của thuật toán Sắp xếp Chọn (Selection Sort) trên mảng $n$ phần tử là:",
            "$\\frac{n(n-1)}{2}$ phép so sánh",
            "$n$ phép so sánh",
            "$n \\log n$ phép so sánh",
            "$n^3$ phép so sánh",
            "A",
            "Vòng lặp ngoài chạy $n-1$ lần, vòng trong tìm min từ $i+1$ đến $n$. Tổng số phép so sánh luôn là $(n-1) + (n-2) + ... + 1 = \\frac{n(n-1)}{2} = \\Theta(n^2)$ bất kể dữ liệu ban đầu."
        )
    ]

    inserted = 0
    for q in more_qs:
        c.execute("SELECT id FROM questions WHERE subject_id = ? AND question_text = ?", (q[0], q[1]))
        if not c.fetchone():
            c.execute("""
                INSERT INTO questions (subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, topic_tag, q_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'medium', 'Algorithms Midterm', 'mcq')
            """, q)
            inserted += 1

    conn.commit()
    print(f"Added {inserted} more high-yield Midterm Algorithm questions!")
    c.execute("SELECT COUNT(*) FROM questions WHERE subject_id = 21")
    print(f"Total questions for Subject 21 (Giải thuật & Toán rời rạc): {c.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    seed_more()
