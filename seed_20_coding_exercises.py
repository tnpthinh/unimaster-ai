"""
20 Practical Coding Exercises for OOP & NNLT 1 (C++/Java/Python/C#)
Each exercise contains:
- title, problem statement
- specifications (specs)
- boilerplate sample code
- unit test cases (input, expected_output, is_hidden)
- reference solution
- language
"""

EXERCISES = [
    # -------------------------------------------------------------
    # NNLT 1: MẢNG, CHUỖI, CON TRỎ, STRUCT, THUẬT TOÁN
    # -------------------------------------------------------------
    {
        "code_tag": "NNLT1_01",
        "subject_code": "NNLT1",
        "title": "Bài 1 (NNLT1): Tìm Phần Tử Lớn Thứ Nhì Trong Mảng",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Cho mảng số nguyên $A$ gồm $N$ phần tử ($2 \\le N \\le 10^5$). Hãy tìm giá trị lớn thứ nhì (khác giá trị lớn nhất) trong mảng. Nếu tất cả các phần tử đều bằng nhau, in ra `-1`.",
        "specs": [
            "Đầu vào: Dòng 1 chứa số nguyên N. Dòng 2 chứa N số nguyên cách nhau bởi khoảng trắng.",
            "Đầu ra: In ra một số nguyên duy nhất là giá trị lớn thứ nhì, hoặc -1 nếu không tồn tại.",
            "Độ phức tạp thời gian tối ưu: O(N), bộ nhớ O(1)."
        ],
        "sample_code": """#include <iostream>
#include <vector>
#include <climits>
using namespace std;

int findSecondLargest(const vector<int>& arr) {
    // TODO: Cài đặt thuật toán tìm phần tử lớn thứ nhì trong O(N)
    return -1;
}

int main() {
    int n;
    if (!(cin >> n) || n < 2) {
        cout << -1 << endl;
        return 0;
    }
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) cin >> arr[i];
    cout << findSecondLargest(arr) << endl;
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <vector>
#include <climits>
using namespace std;

int findSecondLargest(const vector<int>& arr) {
    long long first = LLONG_MIN, second = LLONG_MIN;
    for (int x : arr) {
        if (x > first) {
            second = first;
            first = x;
        } else if (x < first && x > second) {
            second = x;
        }
    }
    return (second == LLONG_MIN) ? -1 : (int)second;
}

int main() {
    int n;
    if (!(cin >> n) || n < 2) {
        cout << -1 << endl;
        return 0;
    }
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) cin >> arr[i];
    cout << findSecondLargest(arr) << endl;
    return 0;
}
""",
        "test_cases": [
            {"input": "5\n12 35 1 10 34", "expected_output": "34", "is_hidden": False},
            {"input": "4\n10 10 10 10", "expected_output": "-1", "is_hidden": False},
            {"input": "6\n5 2 9 1 9 7", "expected_output": "7", "is_hidden": False},
            {"input": "2\n100 50", "expected_output": "50", "is_hidden": True},
            {"input": "7\n-5 -2 -9 -1 -9 -7 -3", "expected_output": "-2", "is_hidden": True}
        ]
    },
    {
        "code_tag": "NNLT1_02",
        "subject_code": "NNLT1",
        "title": "Bài 2 (NNLT1): Chuẩn Hóa Chuỗi Họ Tên Tiếng Việt",
        "difficulty": "easy",
        "language": "cpp",
        "problem": "Cho một chuỗi ký tự chứa họ và tên bị lỗi định dạng (thừa khoảng trắng đầu, cuối, giữa các từ, chữ hoa chữ thường lộn xộn). Hãy chuẩn hóa chuỗi: xóa khoảng trắng thừa, viết hoa chữ cái đầu mỗi từ và viết thường các chữ cái còn lại.",
        "specs": [
            "Đầu vào: Chuỗi ký tự S bất kỳ (chiều dài tối đa 1000 ký tự).",
            "Đầu ra: Chuỗi đã được chuẩn hóa đúng quy tắc danh xưng.",
            "Ví dụ: '  nGUYeN   vAN    a  ' -> 'Nguyen Van A'"
        ],
        "sample_code": """#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cctype>
using namespace std;

string normalizeName(const string& s) {
    // TODO: Viết code chuẩn hóa họ tên
    return "";
}

int main() {
    string s;
    if (getline(cin, s)) {
        cout << normalizeName(s) << endl;
    }
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cctype>
using namespace std;

string normalizeName(const string& s) {
    stringstream ss(s);
    string word, result = "";
    while (ss >> word) {
        if (!word.empty()) {
            word[0] = toupper((unsigned char)word[0]);
            for (size_t i = 1; i < word.length(); ++i) {
                word[i] = tolower((unsigned char)word[i]);
            }
            if (!result.empty()) result += " ";
            result += word;
        }
    }
    return result;
}

int main() {
    string s;
    if (getline(cin, s)) {
        cout << normalizeName(s) << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "  nGUYeN   vAN    a  ", "expected_output": "Nguyen Van A", "is_hidden": False},
            {"input": "tRAn   tHi    mAipHuONG", "expected_output": "Tran Thi Maiphuong", "is_hidden": False},
            {"input": "LE", "expected_output": "Le", "is_hidden": False},
            {"input": "   pHam   dInH   kHOI   nGuyen   ", "expected_output": "Pham Dinh Khoi Nguyen", "is_hidden": True}
        ]
    },
    {
        "code_tag": "NNLT1_03",
        "subject_code": "NNLT1",
        "title": "Bài 3 (NNLT1): Kiểm Tra Chuỗi Đối Xứng (Palindrome)",
        "difficulty": "easy",
        "language": "cpp",
        "problem": "Kiểm tra xem một chuỗi có phải là chuỗi đối xứng (Palindrome) hay không, sau khi đã loại bỏ toàn bộ khoảng trắng, ký tự đặc biệt và không phân biệt hoa thường. In ra `YES` nếu đối xứng, ngược lại in ra `NO`.",
        "specs": [
            "Đầu vào: Chuỗi ký tự S.",
            "Đầu ra: 'YES' hoặc 'NO'.",
            "Ví dụ: 'A man, a plan, a canal: Panama' -> 'YES'"
        ],
        "sample_code": """#include <iostream>
#include <string>
#include <cctype>
using namespace std;

bool isPalindrome(const string& s) {
    // TODO: Viết hàm kiểm tra palindrome
    return false;
}

int main() {
    string s;
    if (getline(cin, s)) {
        cout << (isPalindrome(s) ? "YES" : "NO") << endl;
    }
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <string>
#include <cctype>
using namespace std;

bool isPalindrome(const string& s) {
    int left = 0, right = (int)s.length() - 1;
    while (left < right) {
        while (left < right && !isalnum((unsigned char)s[left])) left++;
        while (left < right && !isalnum((unsigned char)s[right])) right--;
        if (tolower((unsigned char)s[left]) != tolower((unsigned char)s[right])) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}

int main() {
    string s;
    if (getline(cin, s)) {
        cout << (isPalindrome(s) ? "YES" : "NO") << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "A man, a plan, a canal: Panama", "expected_output": "YES", "is_hidden": False},
            {"input": "race a car", "expected_output": "NO", "is_hidden": False},
            {"input": "Was it a car or a cat I saw?", "expected_output": "YES", "is_hidden": False},
            {"input": "Madam, in Eden, I'm Adam", "expected_output": "YES", "is_hidden": True}
        ]
    },
    {
        "code_tag": "NNLT1_04",
        "subject_code": "NNLT1",
        "title": "Bài 4 (NNLT1): Đếm Tần Suất & Tìm Phần Tử Đa Số (Majority)",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Cho mảng số nguyên $A$ kích thước $N$. Phần tử đa số là phần tử xuất hiện nhiều hơn $\\lfloor N/2 \\rfloor$ lần. Hãy tìm phần tử này. Nếu không có phần tử đa số, in ra `NO`.",
        "specs": [
            "Đầu vào: Dòng 1 chứa N. Dòng 2 chứa N số nguyên.",
            "Đầu ra: In ra phần tử đa số hoặc 'NO'.",
            "Thuật toán tối ưu: Boyer-Moore Voting Algorithm O(N) thời gian, O(1) bộ nhớ."
        ],
        "sample_code": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n) || n <= 0) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    
    // TODO: Cài đặt tìm phần tử đa số
    cout << "NO" << endl;
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n) || n <= 0) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    // Boyer-Moore Voting Algorithm
    int candidate = a[0], count = 1;
    for (int i = 1; i < n; ++i) {
        if (a[i] == candidate) {
            count++;
        } else {
            count--;
            if (count == 0) {
                candidate = a[i];
                count = 1;
            }
        }
    }

    // Xác minh lại
    int freq = 0;
    for (int x : a) {
        if (x == candidate) freq++;
    }

    if (freq > n / 2) {
        cout << candidate << endl;
    } else {
        cout << "NO" << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "7\n2 2 1 1 1 2 2", "expected_output": "2", "is_hidden": False},
            {"input": "6\n1 2 3 4 5 6", "expected_output": "NO", "is_hidden": False},
            {"input": "5\n3 3 4 2 4", "expected_output": "NO", "is_hidden": False},
            {"input": "9\n7 7 5 7 5 1 5 7 7", "expected_output": "7", "is_hidden": True}
        ]
    },
    {
        "code_tag": "NNLT1_05",
        "subject_code": "NNLT1",
        "title": "Bài 5 (NNLT1): Xóa Phần Tử Trùng Trong Mảng Đã Sắp Xếp",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Cho mảng số nguyên đã sắp xếp theo thứ tự không giảm. Hãy loại bỏ các phần tử trùng lặp tại chỗ (in-place) sao cho mỗi phần tử duy nhất chỉ xuất hiện 1 lần. In ra độ dài mảng mới và các phần tử đó.",
        "specs": [
            "Đầu vào: Dòng 1: N. Dòng 2: N số nguyên tăng dần.",
            "Đầu ra: Dòng 1 in ra K (số lượng phần tử duy nhất). Dòng 2 in ra K phần tử cách nhau khoảng trắng.",
            "Độ phức tạp O(N), không dùng mảng phụ O(1) space."
        ],
        "sample_code": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n) || n <= 0) {
        cout << "0\\n\\n";
        return 0;
    }
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    // TODO: Xóa phần tử trùng tại chỗ
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n) || n <= 0) {
        cout << "0\\n\\n";
        return 0;
    }
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    int k = 1;
    for (int i = 1; i < n; ++i) {
        if (a[i] != a[k - 1]) {
            a[k] = a[i];
            k++;
        }
    }

    cout << k << "\\n";
    for (int i = 0; i < k; ++i) {
        cout << a[i] << (i + 1 == k ? "" : " ");
    }
    cout << "\\n";
    return 0;
}
""",
        "test_cases": [
            {"input": "6\n1 1 2 2 3 4", "expected_output": "4\n1 2 3 4", "is_hidden": False},
            {"input": "5\n0 0 1 1 1", "expected_output": "2\n0 1", "is_hidden": False},
            {"input": "3\n5 5 5", "expected_output": "1\n5", "is_hidden": True}
        ]
    },
    {
        "code_tag": "NNLT1_06",
        "subject_code": "NNLT1",
        "title": "Bài 6 (NNLT1): Thao Tác Con Trỏ & Đảo Chuỗi Bằng Con Trỏ",
        "difficulty": "easy",
        "language": "cpp",
        "problem": "Sử dụng con trỏ (pointer) trong C/C++ để đảo ngược một chuỗi ký tự mà không dùng hàm đảo ngược thư viện sẵn. Đảm bảo thao tác trực tiếp trên bộ nhớ qua hai con trỏ `start` và `end`.",
        "specs": [
            "Đầu vào: Chuỗi ký tự S.",
            "Đầu ra: Chuỗi S sau khi đã đảo ngược.",
            "Yêu cầu: Viết hàm `void reverseString(char* s)` sử dụng con trỏ."
        ],
        "sample_code": """#include <iostream>
#include <cstring>
using namespace std;

void reverseWithPointer(char* s) {
    // TODO: Dùng 2 con trỏ start, end để đảo chuỗi
}

int main() {
    char s[1005];
    if (cin.getline(s, 1005)) {
        reverseWithPointer(s);
        cout << s << endl;
    }
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <cstring>
using namespace std;

void reverseWithPointer(char* s) {
    if (!s) return;
    char* start = s;
    char* end = s + strlen(s) - 1;
    while (start < end) {
        char temp = *start;
        *start = *end;
        *end = temp;
        start++;
        end--;
    }
}

int main() {
    char s[1005];
    if (cin.getline(s, 1005)) {
        reverseWithPointer(s);
        cout << s << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "hello world", "expected_output": "dlrow olleh", "is_hidden": False},
            {"input": "UniMaster AI", "expected_output": "IA retsaMinU", "is_hidden": False},
            {"input": "a", "expected_output": "a", "is_hidden": True}
        ]
    },
    {
        "code_tag": "NNLT1_07",
        "subject_code": "NNLT1",
        "title": "Bài 7 (NNLT1): Cộng Hai Ma Trận & Kiểm Tra Đối Xứng",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Cho hai ma trận vuông $A$ và $B$ cấp $N \\times N$. Tính ma trận tổng $C = A + B$. Sau đó kiểm tra xem ma trận $C$ có phải là ma trận đối xứng (nghĩa là $C[i][j] == C[j][i]$ với mọi $i, j$) hay không. In ra `SYMMETRIC` hoặc `NOT_SYMMETRIC`.",
        "specs": [
            "Đầu vào: Dòng 1: N. N dòng tiếp theo là ma trận A. N dòng tiếp theo là ma trận B.",
            "Đầu ra: Dòng 1 in ra ma trận C. Dòng tiếp theo in ra 'SYMMETRIC' hoặc 'NOT_SYMMETRIC'."
        ],
        "sample_code": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    // TODO: Nhập A, B, tính C = A + B và kiểm tra tính đối xứng
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<vector<int>> A(n, vector<int>(n));
    vector<vector<int>> B(n, vector<int>(n));
    vector<vector<int>> C(n, vector<int>(n));

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) cin >> A[i][j];

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) cin >> B[i][j];

    bool sym = true;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = A[i][j] + B[i][j];
            cout << C[i][j] << (j + 1 == n ? "" : " ");
        }
        cout << "\\n";
    }

    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (C[i][j] != C[j][i]) {
                sym = false;
                break;
            }
        }
        if (!sym) break;
    }

    cout << (sym ? "SYMMETRIC" : "NOT_SYMMETRIC") << "\\n";
    return 0;
}
""",
        "test_cases": [
            {
                "input": "2\n1 2\n3 4\n1 1\n0 1",
                "expected_output": "2 3\n3 5\nSYMMETRIC",
                "is_hidden": False
            },
            {
                "input": "2\n1 0\n0 1\n0 2\n1 0",
                "expected_output": "1 2\n1 1\nNOT_SYMMETRIC",
                "is_hidden": False
            }
        ]
    },
    {
        "code_tag": "NNLT1_08",
        "subject_code": "NNLT1",
        "title": "Bài 8 (NNLT1): Quản Lý Sinh Viên Bằng Struct & Tìm Thủ Khoa",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Định nghĩa struct `Student` gồm: mã sinh viên (string), họ tên (string), điểm GPA (float). Nhập danh sách $N$ sinh viên, tìm và in ra thông tin của sinh viên có GPA cao nhất.",
        "specs": [
            "Đầu vào: Dòng 1: N. N dòng tiếp theo, mỗi dòng chứa: MãSV HọTên GPA (cách nhau bởi dấu phẩy hoặc tab).",
            "Đầu ra: In thông tin thủ khoa theo mẫu: 'TOP: [MãSV] - [HọTên] - [GPA]'."
        ],
        "sample_code": """#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
using namespace std;

struct Student {
    string id;
    string name;
    float gpa;
};

int main() {
    int n;
    if (!(cin >> n)) return 0;
    string dummy;
    getline(cin, dummy);
    // TODO: Nhập và tìm sinh viên có GPA lớn nhất
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
using namespace std;

struct Student {
    string id;
    string name;
    float gpa;
};

int main() {
    int n;
    if (!(cin >> n)) return 0;
    string dummy;
    getline(cin, dummy);

    vector<Student> list;
    int topIdx = 0;
    float maxGpa = -1.0f;

    for (int i = 0; i < n; ++i) {
        string line;
        if (!getline(cin, line)) break;
        stringstream ss(line);
        Student s;
        ss >> s.id;
        string temp;
        vector<string> nameParts;
        float g;
        while (ss >> temp) {
            try {
                size_t idx;
                g = stof(temp, &idx);
                if (idx == temp.length()) {
                    s.gpa = g;
                    break;
                } else {
                    nameParts.push_back(temp);
                }
            } catch (...) {
                nameParts.push_back(temp);
            }
        }
        string full = "";
        for (size_t k = 0; k < nameParts.size(); ++k) {
            if (k > 0) full += " ";
            full += nameParts[k];
        }
        s.name = full;
        if (s.gpa > maxGpa) {
            maxGpa = s.gpa;
            topIdx = i;
        }
        list.push_back(s);
    }

    if (!list.empty()) {
        cout << "TOP: " << list[topIdx].id << " - " << list[topIdx].name << " - " 
             << fixed << setprecision(2) << list[topIdx].gpa << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {
                "input": "3\nSV01 Nguyen Van A 3.8\nSV02 Tran Thi B 3.95\nSV03 Le Van C 3.6",
                "expected_output": "TOP: SV02 - Tran Thi B - 3.95",
                "is_hidden": False
            }
        ]
    },
    {
        "code_tag": "NNLT1_09",
        "subject_code": "NNLT1",
        "title": "Bài 9 (NNLT1): Tìm Kiếm Nhị Phân (Binary Search)",
        "difficulty": "easy",
        "language": "cpp",
        "problem": "Cho mảng đã sắp xếp gồm $N$ số nguyên tăng dần và một giá trị $X$. Dùng thuật toán tìm kiếm nhị phân để tìm vị trí (chỉ số 0-based) của $X$. Nếu không tìm thấy, in ra `-1`.",
        "specs": [
            "Đầu vào: Dòng 1: N và X. Dòng 2: N số nguyên tăng dần.",
            "Đầu ra: Vị trí của X hoặc -1.",
            "Thời gian: O(log N)."
        ],
        "sample_code": """#include <iostream>
#include <vector>
using namespace std;

int binarySearch(const vector<int>& a, int x) {
    // TODO: Viết tìm kiếm nhị phân
    return -1;
}

int main() {
    int n, x;
    if (!(cin >> n >> x)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    cout << binarySearch(a, x) << endl;
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <vector>
using namespace std;

int binarySearch(const vector<int>& a, int x) {
    int low = 0, high = (int)a.size() - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (a[mid] == x) return mid;
        if (a[mid] < x) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main() {
    int n, x;
    if (!(cin >> n >> x)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    cout << binarySearch(a, x) << endl;
    return 0;
}
""",
        "test_cases": [
            {"input": "5 7\n1 3 5 7 9", "expected_output": "3", "is_hidden": False},
            {"input": "5 4\n1 3 5 7 9", "expected_output": "-1", "is_hidden": False},
            {"input": "1 10\n10", "expected_output": "0", "is_hidden": True}
        ]
    },
    {
        "code_tag": "NNLT1_10",
        "subject_code": "NNLT1",
        "title": "Bài 10 (NNLT1): Chuyển Đổi Số Thập Phân Sang Nhị Phân",
        "difficulty": "easy",
        "language": "cpp",
        "problem": "Cho số nguyên dương $N$ ($0 \\le N \\le 10^9$). Hãy chuyển đổi $N$ sang biểu diễn nhị phân tương ứng và in ra màn hình.",
        "specs": [
            "Đầu vào: Số nguyên N.",
            "Đầu ra: Chuỗi nhị phân tương ứng (ví dụ: 13 -> 1101, 0 -> 0)."
        ],
        "sample_code": """#include <iostream>
#include <string>
using namespace std;

string toBinary(long long n) {
    // TODO: Chuyển đổi n sang nhị phân
    return "";
}

int main() {
    long long n;
    if (cin >> n) {
        cout << toBinary(n) << endl;
    }
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

string toBinary(long long n) {
    if (n == 0) return "0";
    string res = "";
    while (n > 0) {
        res += (n % 2 == 0 ? '0' : '1');
        n /= 2;
    }
    reverse(res.begin(), res.end());
    return res;
}

int main() {
    long long n;
    if (cin >> n) {
        cout << toBinary(n) << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "13", "expected_output": "1101", "is_hidden": False},
            {"input": "0", "expected_output": "0", "is_hidden": False},
            {"input": "255", "expected_output": "11111111", "is_hidden": False},
            {"input": "1024", "expected_output": "10000000000", "is_hidden": True}
        ]
    },

    # -------------------------------------------------------------
    # OOP: CLASS, KẾ THỪA, ĐA HÌNH, TRỪU TƯỢNG, VIRTUAL, PATTERNS
    # -------------------------------------------------------------
    {
        "code_tag": "OOP_01",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 11 (OOP): Thiết Kế Class Phân Số (Fraction) & Rút Gọn",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Thiết kế class `PhanSo` với hai thuộc tính `tuSo` và `mauSo`. Cài đặt phương thức khởi tạo, phương thức rút gọn (dùng GCD), và phương thức cộng hai phân số. Nếu mẫu số âm, đưa dấu âm lên tử số.",
        "specs": [
            "Đầu vào: 4 số nguyên: tu1 mau1 tu2 mau2.",
            "Đầu ra: In phân số tổng ở dạng tối giản 'tu/mau' (nếu mẫu số = 1 thì chỉ in tu).",
            "Ví dụ: 1 2 1 3 -> 5/6 ; 1 2 1 2 -> 1"
        ],
        "sample_code": """#include <iostream>
#include <numeric>
using namespace std;

class PhanSo {
private:
    long long tu, mau;
public:
    PhanSo(long long t = 0, long long m = 1) : tu(t), mau(m) {
        rutGon();
    }
    
    void rutGon() {
        // TODO: Rút gọn phân số theo GCD và chuẩn hóa mẫu dương
    }
    
    PhanSo cong(const PhanSo& other) const {
        // TODO: Cộng hai phân số
        return PhanSo();
    }
    
    void xuat() const {
        if (mau == 1) cout << tu << endl;
        else cout << tu << "/" << mau << endl;
    }
};

int main() {
    long long t1, m1, t2, m2;
    if (cin >> t1 >> m1 >> t2 >> m2) {
        PhanSo p1(t1, m1), p2(t2, m2);
        PhanSo sum = p1.cong(p2);
        sum.xuat();
    }
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <cstdlib>
using namespace std;

long long gcd(long long a, long long b) {
    a = llabs(a); b = llabs(b);
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

class PhanSo {
private:
    long long tu, mau;
public:
    PhanSo(long long t = 0, long long m = 1) : tu(t), mau(m) {
        rutGon();
    }
    
    void rutGon() {
        if (mau < 0) {
            tu = -tu;
            mau = -mau;
        }
        long long g = gcd(tu, mau);
        if (g > 0) {
            tu /= g;
            mau /= g;
        }
    }
    
    PhanSo cong(const PhanSo& other) const {
        long long newTu = tu * other.mau + other.tu * mau;
        long long newMau = mau * other.mau;
        return PhanSo(newTu, newMau);
    }
    
    void xuat() const {
        if (mau == 1) cout << tu << endl;
        else cout << tu << "/" << mau << endl;
    }
};

int main() {
    long long t1, m1, t2, m2;
    if (cin >> t1 >> m1 >> t2 >> m2) {
        PhanSo p1(t1, m1), p2(t2, m2);
        PhanSo sum = p1.cong(p2);
        sum.xuat();
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "1 2 1 3", "expected_output": "5/6", "is_hidden": False},
            {"input": "1 2 1 2", "expected_output": "1", "is_hidden": False},
            {"input": "2 4 -1 2", "expected_output": "0", "is_hidden": False},
            {"input": "3 -6 5 10", "expected_output": "0", "is_hidden": True}
        ]
    },
    {
        "code_tag": "OOP_02",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 12 (OOP): Đóng Gói (Encapsulation) - Class BankAccount",
        "difficulty": "easy",
        "language": "cpp",
        "problem": "Thiết kế class `BankAccount` tuân thủ tính đóng gói: thuộc tính `balance` ở dạng `private`. Các phương thức: `deposit(amount)`, `withdraw(amount)` (trả về false nếu không đủ tiền hoặc amount <= 0), `getBalance()`. Mô phỏng chuỗi giao dịch nạp/rút tiền.",
        "specs": [
            "Đầu vào: Số dư ban đầu. Tiếp theo là các lệnh: 'D [amount]' (Deposit) hoặc 'W [amount]' (Withdraw) cho đến khi gặp lệnh 'E' (End).",
            "Đầu ra: Với mỗi lệnh W không hợp lệ, in ra 'FAILED'. Cuối cùng in ra 'BALANCE: [số dư cuối]'."
        ],
        "sample_code": """#include <iostream>
#include <string>
using namespace std;

class BankAccount {
private:
    double balance;
public:
    BankAccount(double init = 0) : balance(init) {}
    // TODO: Viết deposit, withdraw, getBalance
};

int main() {
    double init;
    if (!(cin >> init)) return 0;
    BankAccount acc(init);
    char cmd;
    while (cin >> cmd && cmd != 'E') {
        double amt;
        cin >> amt;
        // TODO: Xử lý giao dịch
    }
    // TODO: In kết quả
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

class BankAccount {
private:
    double balance;
public:
    BankAccount(double init = 0) : balance(init >= 0 ? init : 0) {}

    void deposit(double amount) {
        if (amount > 0) balance += amount;
    }

    bool withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            return true;
        }
        return false;
    }

    double getBalance() const {
        return balance;
    }
};

int main() {
    double init;
    if (!(cin >> init)) return 0;
    BankAccount acc(init);
    char cmd;
    while (cin >> cmd && cmd != 'E') {
        double amt;
        cin >> amt;
        if (cmd == 'D') {
            acc.deposit(amt);
        } else if (cmd == 'W') {
            if (!acc.withdraw(amt)) {
                cout << "FAILED\\n";
            }
        }
    }
    cout << "BALANCE: " << fixed << setprecision(2) << acc.getBalance() << endl;
    return 0;
}
""",
        "test_cases": [
            {
                "input": "100.0\nD 50.0\nW 30.0\nW 200.0\nE",
                "expected_output": "FAILED\nBALANCE: 120.00",
                "is_hidden": False
            },
            {
                "input": "500.0\nW 500.0\nE",
                "expected_output": "BALANCE: 0.00",
                "is_hidden": False
            }
        ]
    },
    {
        "code_tag": "OOP_03",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 13 (OOP): Đa Hình Trừu Tượng - Hệ Thống Hình Học (Shape)",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Xây dựng lớp trừu tượng `Shape` với phương thức thuần ảo `virtual double getArea() const = 0` và `virtual string getName() const = 0`. Kế thừa thành `Circle(radius)` và `Rectangle(width, height)`. Tính tổng diện tích của danh sách các hình hình học.",
        "specs": [
            "Sử dụng $\\pi = 3.14159$.",
            "Đầu vào: N hình. Tiếp theo là các hình: 'C [radius]' hoặc 'R [width] [height]'.",
            "Đầu ra: In ra tổng diện tích làm tròn 2 chữ số thập phân."
        ],
        "sample_code": """#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
using namespace std;

class Shape {
public:
    virtual ~Shape() {}
    virtual double getArea() const = 0;
};

// TODO: Lớp Circle và Rectangle

int main() {
    int n;
    if (!(cin >> n)) return 0;
    // TODO: Quản lý con trỏ Shape* và tính tổng diện tích
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
using namespace std;

const double PI = 3.141592653589793;

class Shape {
public:
    virtual ~Shape() {}
    virtual double getArea() const = 0;
};

class Circle : public Shape {
private:
    double radius;
public:
    Circle(double r) : radius(r) {}
    double getArea() const override {
        return PI * radius * radius;
    }
};

class Rectangle : public Shape {
private:
    double width, height;
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    double getArea() const override {
        return width * height;
    }
};

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<Shape*> shapes;
    for (int i = 0; i < n; ++i) {
        char type;
        cin >> type;
        if (type == 'C') {
            double r; cin >> r;
            shapes.push_back(new Circle(r));
        } else if (type == 'R') {
            double w, h; cin >> w >> h;
            shapes.push_back(new Rectangle(w, h));
        }
    }

    double total = 0;
    for (Shape* s : shapes) {
        total += s->getArea();
        delete s; // Dọn dẹp tránh memory leak
    }

    cout << "TOTAL AREA: " << fixed << setprecision(2) << total << endl;
    return 0;
}
""",
        "test_cases": [
            {
                "input": "2\nC 2.0\nR 3.0 4.0",
                "expected_output": "TOTAL AREA: 24.57",
                "is_hidden": False
            },
            {
                "input": "1\nR 5.0 10.0",
                "expected_output": "TOTAL AREA: 50.00",
                "is_hidden": False
            }
        ]
    },
    {
        "code_tag": "OOP_04",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 14 (OOP): Kế Thừa Quản Lý Nhân Sự & Đa Hình Tính Lương",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Tạo lớp cơ sở `NhanVien` với các thuộc tính: mã, họ tên, lương cơ bản. Lớp con `NhanVienVanPhong` có thêm hệ số chuyên cần (Lương = Lương cơ bản * hệ số + 500k phụ cấp). Lớp con `NhanVienSanXuat` có thêm số lượng sản phẩm (Lương = Lương cơ bản + số sản phẩm * 20k). Đa hình tính lương.",
        "specs": [
            "Đầu vào: N. Mỗi dòng tiếp theo là thông tin nhân viên: 'VP [Mã] [Tên] [LuongCB] [HeSo]' hoặc 'SX [Mã] [Tên] [LuongCB] [SoSP]'.",
            "Đầu ra: In mã nhân viên và lương tính được, cuối cùng in tổng quỹ lương."
        ],
        "sample_code": """#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
using namespace std;

// TODO: Thiết kế class NhanVien, NhanVienVanPhong, NhanVienSanXuat
int main() {
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
using namespace std;

class NhanVien {
protected:
    string id, name;
    double luongCB;
public:
    NhanVien(string id, string name, double luongCB) : id(id), name(name), luongCB(luongCB) {}
    virtual ~NhanVien() {}
    virtual double tinhLuong() const = 0;
    string getId() const { return id; }
};

class NhanVienVanPhong : public NhanVien {
private:
    double heSo;
public:
    NhanVienVanPhong(string id, string name, double lcb, double hs) : NhanVien(id, name, lcb), heSo(hs) {}
    double tinhLuong() const override {
        return luongCB * heSo + 500.0;
    }
};

class NhanVienSanXuat : public NhanVien {
private:
    int soSP;
public:
    NhanVienSanXuat(string id, string name, double lcb, int sp) : NhanVien(id, name, lcb), soSP(sp) {}
    double tinhLuong() const override {
        return luongCB + soSP * 20.0;
    }
};

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<NhanVien*> staff;
    for (int i = 0; i < n; ++i) {
        string type, id, name;
        double lcb;
        cin >> type >> id >> name >> lcb;
        if (type == "VP") {
            double hs; cin >> hs;
            staff.push_back(new NhanVienVanPhong(id, name, lcb, hs));
        } else if (type == "SX") {
            int sp; cin >> sp;
            staff.push_back(new NhanVienSanXuat(id, name, lcb, sp));
        }
    }

    double total = 0;
    for (NhanVien* nv : staff) {
        double salary = nv->tinhLuong();
        total += salary;
        cout << nv->getId() << ": " << fixed << setprecision(1) << salary << endl;
        delete nv;
    }
    cout << "TOTAL: " << fixed << setprecision(1) << total << endl;
    return 0;
}
""",
        "test_cases": [
            {
                "input": "2\nVP NV01 Lan 5000.0 1.2\nSX NV02 Hung 4000.0 50",
                "expected_output": "NV01: 6500.0\nNV02: 5000.0\nTOTAL: 11500.0",
                "is_hidden": False
            }
        ]
    },
    {
        "code_tag": "OOP_05",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 15 (OOP): Interface Thanh Toán (IPaymentProcessor)",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Cài đặt kiến trúc thanh toán Interface: `IPaymentProcessor` với hàm `processPayment(amount)`. Cài đặt 2 cổng thanh toán `CreditCardPayment` (phí 2% trên số tiền) và `VNPayPayment` (phí cố định 5.0). In ra số tiền thực thu.",
        "specs": [
            "Đầu vào: Loại cổng ('CC' hoặc 'VNPAY') và số tiền.",
            "Đầu ra: In ra 'PROCESSED: [Tổng tiền gồm phí]'."
        ],
        "sample_code": """#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

// TODO: Cài đặt IPaymentProcessor
int main() {
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

class IPaymentProcessor {
public:
    virtual ~IPaymentProcessor() {}
    virtual double processPayment(double amount) = 0;
};

class CreditCardPayment : public IPaymentProcessor {
public:
    double processPayment(double amount) override {
        return amount * 1.02; // Phí 2%
    }
};

class VNPayPayment : public IPaymentProcessor {
public:
    double processPayment(double amount) override {
        return amount + 5.0; // Phí cố định 5.0
    }
};

int main() {
    string method;
    double amount;
    if (cin >> method >> amount) {
        IPaymentProcessor* p = nullptr;
        if (method == "CC") p = new CreditCardPayment();
        else p = new VNPayPayment();
        
        cout << "PROCESSED: " << fixed << setprecision(2) << p->processPayment(amount) << endl;
        delete p;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "CC 100.0", "expected_output": "PROCESSED: 102.00", "is_hidden": False},
            {"input": "VNPAY 100.0", "expected_output": "PROCESSED: 105.00", "is_hidden": False}
        ]
    },
    {
        "code_tag": "OOP_06",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 16 (OOP): Virtual Destructor & Ngăn Chặn Rò Rỉ Bộ Nhớ",
        "difficulty": "hard",
        "language": "cpp",
        "problem": "Khi giải phóng đối tượng của lớp con qua con trỏ lớp cha `Base* ptr = new Derived(); delete ptr;`, nếu lớp cha không có destructor ảo (`virtual ~Base()`), destructor của lớp con sẽ KHÔNG được gọi, dẫn đến rò rỉ bộ nhớ. Hãy sửa lỗi code mẫu để destructor của cả hai lớp được gọi tuần tự chính xác.",
        "specs": [
            "Đầu vào: Không có đầu vào.",
            "Đầu ra đúng thứ tự giải phóng: 'Derived destroyed' rồi đến 'Base destroyed'."
        ],
        "sample_code": """#include <iostream>
using namespace std;

class Base {
public:
    // TODO: Khắc phục lỗi rò rỉ bộ nhớ ở đây bằng virtual destructor
    ~Base() {
        cout << "Base destroyed" << endl;
    }
};

class Derived : public Base {
private:
    int* buffer;
public:
    Derived() { buffer = new int[100]; }
    ~Derived() {
        delete[] buffer;
        cout << "Derived destroyed" << endl;
    }
};

int main() {
    Base* obj = new Derived();
    delete obj;
    return 0;
}
""",
        "solution_code": """#include <iostream>
using namespace std;

class Base {
public:
    virtual ~Base() {
        cout << "Base destroyed" << endl;
    }
};

class Derived : public Base {
private:
    int* buffer;
public:
    Derived() { buffer = new int[100]; }
    ~Derived() override {
        delete[] buffer;
        cout << "Derived destroyed" << endl;
    }
};

int main() {
    Base* obj = new Derived();
    delete obj;
    return 0;
}
""",
        "test_cases": [
            {"input": "", "expected_output": "Derived destroyed\nBase destroyed", "is_hidden": False}
        ]
    },
    {
        "code_tag": "OOP_07",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 17 (OOP): Nạp Chồng Toán Tử (Operator Overloading) Vector2D",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Định nghĩa class `Vector2D` gồm hai tọa độ x, y (số thực). Cài đặt nạp chồng toán tử cộng `+` (cộng hai vector) và toán tử tích vô hướng `*` (dot product) trả về số thực.",
        "specs": [
            "Đầu vào: x1 y1 x2 y2.",
            "Đầu ra: Dòng 1 in vector tổng '(x, y)', dòng 2 in tích vô hướng làm tròn 2 chữ số."
        ],
        "sample_code": """#include <iostream>
#include <iomanip>
using namespace std;

class Vector2D {
public:
    double x, y;
    Vector2D(double x = 0, double y = 0) : x(x), y(y) {}
    // TODO: Nạp chồng operator + và operator *
};

int main() {
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <iomanip>
using namespace std;

class Vector2D {
public:
    double x, y;
    Vector2D(double x = 0, double y = 0) : x(x), y(y) {}

    Vector2D operator+(const Vector2D& other) const {
        return Vector2D(x + other.x, y + other.y);
    }

    double operator*(const Vector2D& other) const {
        return x * other.x + y * other.y;
    }
};

int main() {
    double x1, y1, x2, y2;
    if (cin >> x1 >> y1 >> x2 >> y2) {
        Vector2D v1(x1, y1), v2(x2, y2);
        Vector2D sum = v1 + v2;
        double dot = v1 * v2;
        cout << "(" << fixed << setprecision(1) << sum.x << ", " << sum.y << ")\\n";
        cout << fixed << setprecision(2) << dot << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "1.0 2.0 3.0 4.0", "expected_output": "(4.0, 6.0)\n11.00", "is_hidden": False},
            {"input": "0.0 5.0 5.0 0.0", "expected_output": "(5.0, 5.0)\n0.00", "is_hidden": False}
        ]
    },
    {
        "code_tag": "OOP_08",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 18 (OOP): Quản Lý Danh Sách Đối Tượng & Lọc GPA Giỏi",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Thiết kế lớp `SinhVien` và lớp `LopHoc`. `LopHoc` chứa danh sách sinh viên, có phương thức `tinhDiemTrungBinh()` của cả lớp và phương thức đếm số lượng sinh viên đạt loại Giỏi ($GPA \\ge 8.0$).",
        "specs": [
            "Đầu vào: N. N dòng tiếp theo chứa: MãSV HọTên GPA.",
            "Đầu ra: Dòng 1 in: 'GPA TB: [điểm]', dòng 2 in: 'SO SV GIOI: [số lượng]'."
        ],
        "sample_code": """#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
using namespace std;

// TODO: Cài đặt SinhVien và LopHoc
int main() {
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
using namespace std;

class SinhVien {
private:
    string id, name;
    double gpa;
public:
    SinhVien(string id, string name, double gpa) : id(id), name(name), gpa(gpa) {}
    double getGpa() const { return gpa; }
};

class LopHoc {
private:
    vector<SinhVien> ds;
public:
    void themSV(const SinhVien& sv) { ds.push_back(sv); }

    double tinhDiemTB() const {
        if (ds.empty()) return 0;
        double sum = 0;
        for (const auto& s : ds) sum += s.getGpa();
        return sum / ds.size();
    }

    int demGioi() const {
        int cnt = 0;
        for (const auto& s : ds) {
            if (s.getGpa() >= 8.0) cnt++;
        }
        return cnt;
    }
};

int main() {
    int n;
    if (!(cin >> n)) return 0;
    LopHoc lop;
    for (int i = 0; i < n; ++i) {
        string id, name;
        double gpa;
        cin >> id >> name >> gpa;
        lop.themSV(SinhVien(id, name, gpa));
    }
    cout << "GPA TB: " << fixed << setprecision(2) << lop.tinhDiemTB() << "\\n";
    cout << "SO SV GIOI: " << lop.demGioi() << endl;
    return 0;
}
""",
        "test_cases": [
            {
                "input": "3\nB21 Nam 8.5\nB22 Mai 7.5\nB23 Dung 9.0",
                "expected_output": "GPA TB: 8.33\nSO SV GIOI: 2",
                "is_hidden": False
            }
        ]
    },
    {
        "code_tag": "OOP_09",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 19 (OOP): Design Pattern Singleton (AppConfig)",
        "difficulty": "hard",
        "language": "cpp",
        "problem": "Cài đặt mẫu thiết kế Singleton (Meyers' Singleton) cho class `AppConfig`. Đảm bảo constructor là private, không thể sao chép (copy constructor deleted) và hàm `getInstance()` luôn trả về cùng một thể hiện duy nhất trong bộ nhớ.",
        "specs": [
            "Đầu vào: Không có đầu vào.",
            "Đầu ra: In ra 'SAME_INSTANCE' khi kiểm tra địa chỉ bộ nhớ của 2 lần gọi getInstance()."
        ],
        "sample_code": """#include <iostream>
using namespace std;

class AppConfig {
    // TODO: Cài đặt Singleton Pattern
};

int main() {
    // TODO: Kiểm tra singleton
    return 0;
}
""",
        "solution_code": """#include <iostream>
using namespace std;

class AppConfig {
private:
    string appName;
    AppConfig() : appName("UniMaster AI") {}
    AppConfig(const AppConfig&) = delete;
    AppConfig& operator=(const AppConfig&) = delete;
public:
    static AppConfig& getInstance() {
        static AppConfig instance;
        return instance;
    }
    string getAppName() const { return appName; }
};

int main() {
    AppConfig& c1 = AppConfig::getInstance();
    AppConfig& c2 = AppConfig::getInstance();
    if (&c1 == &c2) {
        cout << "SAME_INSTANCE" << endl;
    } else {
        cout << "DIFFERENT_INSTANCE" << endl;
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "", "expected_output": "SAME_INSTANCE", "is_hidden": False}
        ]
    },
    {
        "code_tag": "OOP_10",
        "subject_code": "OOP_CSHARP",
        "title": "Bài 20 (OOP): Ngoại Lệ Tùy Biến (Custom Exception Handling)",
        "difficulty": "medium",
        "language": "cpp",
        "problem": "Tạo ngoại lệ tùy biến `InvalidAgeException` kế thừa từ `std::exception`. Khi khởi tạo người dùng `User(age)`, nếu $age < 0$ hoặc $age > 150$, quăng ra ngoại lệ này kèm thông điệp 'Invalid age range'. Bắt và xử lý ngoại lệ trong hàm `main()`.",
        "specs": [
            "Đầu vào: Số nguyên age.",
            "Đầu ra: Nếu hợp lệ in ra 'USER_CREATED: [age]'. Nếu quăng ngoại lệ in ra 'CAUGHT: Invalid age range'."
        ],
        "sample_code": """#include <iostream>
#include <exception>
#include <string>
using namespace std;

// TODO: Tạo InvalidAgeException và User
int main() {
    int age;
    if (cin >> age) {
        // TODO: Try catch
    }
    return 0;
}
""",
        "solution_code": """#include <iostream>
#include <exception>
#include <string>
using namespace std;

class InvalidAgeException : public exception {
public:
    const char* what() const noexcept override {
        return "Invalid age range";
    }
};

class User {
private:
    int age;
public:
    User(int a) : age(a) {
        if (a < 0 || a > 150) {
            throw InvalidAgeException();
        }
    }
    int getAge() const { return age; }
};

int main() {
    int age;
    if (cin >> age) {
        try {
            User u(age);
            cout << "USER_CREATED: " << u.getAge() << endl;
        } catch (const InvalidAgeException& e) {
            cout << "CAUGHT: " << e.what() << endl;
        }
    }
    return 0;
}
""",
        "test_cases": [
            {"input": "20", "expected_output": "USER_CREATED: 20", "is_hidden": False},
            {"input": "-5", "expected_output": "CAUGHT: Invalid age range", "is_hidden": False},
            {"input": "160", "expected_output": "CAUGHT: Invalid age range", "is_hidden": False}
        ]
    }
]

print(f"Loaded {len(EXERCISES)} practical exercises.")
