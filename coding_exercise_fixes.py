# -*- coding: utf-8 -*-
"""Vá dữ liệu 11 bài "Thực Hành Code" bị hỏng trong DB.

VÌ SAO CẦN FILE NÀY
===================
Script `seed_v15_comprehensive.py` sinh 10/20 bài bằng một vòng lặp
"cho có đủ số lượng", nội dung chỉ là:

    using System;
    public class Program { public static void Main() {
        Console.WriteLine("PHANSO_OK");   // <-- in ra một chuỗi HẰNG
    } }

và 5 test case có input "1", "2", "3", "4", "5" nhưng expected_output
LUÔN là đúng chuỗi hằng đó. Hệ quả:

  * Học viên mở bài "Nạp chồng toán tử" thì code mẫu đã "pass" sẵn
    (không học được gì).
  * Học viên viết code THẬT để giải bài (cộng phân số, Singleton, ...)
    thì lại TRƯỢT hết test, vì output không phải "PHANSO_OK".

Thêm nữa bài #47 (Python 05) bị lỗi sinh seed: dấu `\n` bị ghi thành
xuống dòng thật nằm ngay trong string literal:

    lines = sys.stdin.read().strip().split('
    ')

-> `SyntaxError: unterminated string literal`.

FILE NÀY chứa nội dung ĐÚNG cho 11 bài đó và được gọi tự động trong
`database.init_db()`, nên bản deploy trên cloud (đã có sẵn file DB) cũng
tự được vá, không phụ thuộc vào việc copy lại seed.
"""

FIXES_REV = "coding-exercises-rev-3"

SUBJECT_CSHARP = 5
SUBJECT_PYTHON = 22

# ---------------------------------------------------------------------------
# NỘI DUNG ĐÚNG CHO TỪNG BÀI
# Mỗi bài: key = (subject_id, tiền tố tiêu đề) để tìm được cả khi id khác nhau
# ---------------------------------------------------------------------------

_CS06 = r'''using System;

public class PhanSo {
    public int Tu { get; set; }
    public int Mau { get; set; }

    public PhanSo(int tu, int mau) {
        Tu = tu;
        Mau = (mau == 0) ? 1 : mau;
        RutGon();
    }

    private static int Ucln(int a, int b) {
        a = Math.Abs(a);
        b = Math.Abs(b);
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return (a == 0) ? 1 : a;
    }

    public void RutGon() {
        int g = Ucln(Tu, Mau);
        Tu /= g;
        Mau /= g;
        if (Mau < 0) { Tu = -Tu; Mau = -Mau; }
    }

    // Nạp chồng toán tử + : cộng hai phân số theo quy đồng mẫu
    public static PhanSo operator +(PhanSo a, PhanSo b) {
        return new PhanSo(a.Tu * b.Mau + b.Tu * a.Mau, a.Mau * b.Mau);
    }

    public override string ToString() {
        return Tu + "/" + Mau;
    }
}

public class Program {
    public static void Main() {
        string[] p = Console.ReadLine().Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        PhanSo f1 = new PhanSo(int.Parse(p[0]), int.Parse(p[1]));
        PhanSo f2 = new PhanSo(int.Parse(p[2]), int.Parse(p[3]));
        Console.WriteLine(f1 + f2);
    }
}'''

_CS07 = r'''using System;

public class NhanVien {
    public string Ten;
    public int LuongCoBan;

    public NhanVien(string ten, int luong) {
        Ten = ten;
        LuongCoBan = luong;
    }

    public virtual int TinhLuong() { return LuongCoBan; }
    public virtual string ChucVu() { return "Nhan vien"; }
}

public class TruongPhong : NhanVien {
    public TruongPhong(string ten, int luong) : base(ten, luong) {}
    public override int TinhLuong() { return LuongCoBan + LuongCoBan * 20 / 100; }
    public override string ChucVu() { return "Truong phong"; }
}

public class GiamDoc : TruongPhong {
    public GiamDoc(string ten, int luong) : base(ten, luong) {}
    public override int TinhLuong() { return LuongCoBan + LuongCoBan * 50 / 100; }
    public override string ChucVu() { return "Giam doc"; }
}

public class Program {
    public static void Main() {
        string[] p = Console.ReadLine().Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        string loai = p[0];
        int luong = int.Parse(p[1]);

        NhanVien nv;
        if (loai == "GD") {
            nv = new GiamDoc("GD", luong);
        } else if (loai == "TP") {
            nv = new TruongPhong("TP", luong);
        } else {
            nv = new NhanVien("NV", luong);
        }

        // Gọi qua kiểu cha -> đa hình: chạy đúng override của lớp con
        Console.WriteLine(nv.ChucVu() + " - " + nv.TinhLuong());
    }
}'''

_CS08 = r'''using System;

public class SoDuKhongDuException : Exception {
    public SoDuKhongDuException(string msg) : base(msg) {}
}

public class BankAccount {
    public int SoDu;

    public BankAccount(int soDu) { SoDu = soDu; }

    public void Rut(int soTien) {
        if (soTien > SoDu) {
            throw new SoDuKhongDuException("So du khong du");
        }
        SoDu -= soTien;
    }
}

public class Program {
    public static void Main() {
        string[] p = Console.ReadLine().Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        BankAccount tk = new BankAccount(int.Parse(p[0]));
        int rut = int.Parse(p[1]);

        try {
            tk.Rut(rut);
            Console.WriteLine("Con lai: " + tk.SoDu);
        } catch (SoDuKhongDuException) {
            Console.WriteLine("LOI: So du khong du");
        }
    }
}'''

_CS09 = r'''using System;
using System.Collections.Generic;

public interface IRepository<T> {
    void Add(T item);
    List<T> GetAll();
    int Count { get; }
}

public class ListRepository<T> : IRepository<T> {
    private List<T> _items = new List<T>();

    public void Add(T item) { _items.Add(item); }
    public List<T> GetAll() { return _items; }
    public int Count { get { return _items.Count; } }
}

public class Program {
    public static void Main() {
        int n = int.Parse(Console.ReadLine().Trim());
        IRepository<int> repo = new ListRepository<int>();

        if (n > 0) {
            string[] p = Console.ReadLine().Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            for (int i = 0; i < n && i < p.Length; i++) {
                repo.Add(int.Parse(p[i]));
            }
        }

        int sum = 0;
        foreach (int v in repo.GetAll()) { sum += v; }

        Console.WriteLine("Count: " + repo.Count);
        Console.WriteLine("Sum: " + sum);
    }
}'''

_CS10 = r'''using System;

public delegate void NhietDoCaoHandler(int nhietDo);

public class MayChu {
    public event NhietDoCaoHandler OnNhietDoCao;

    public void CapNhat(int nhietDo) {
        if (nhietDo > 80) {
            if (OnNhietDoCao != null) { OnNhietDoCao(nhietDo); }
        } else {
            Console.WriteLine("Binh thuong - " + nhietDo);
        }
    }
}

public class Program {
    public static void Main() {
        int t = int.Parse(Console.ReadLine().Trim());

        MayChu mc = new MayChu();
        mc.OnNhietDoCao += delegate(int nhietDo) {
            Console.WriteLine("CANH BAO: Nhiet do cao - " + nhietDo);
        };

        mc.CapNhat(t);
    }
}'''

_PY06 = r'''import sys


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    nums = [int(x) for x in data[1:1 + n]]
    # List comprehension: loc ra cac so nguyen to
    primes = [str(x) for x in nums if is_prime(x)]
    print(' '.join(primes))


if __name__ == '__main__':
    solve()'''

_PY07 = r'''import sys


def solve():
    lines = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    n = int(lines[0].strip())
    matrix = []
    for i in range(n):
        matrix.append([int(x) for x in lines[i + 1].split()])

    # zip(*matrix) chinh la phep chuyen vi (transpose)
    for row in zip(*matrix):
        print(' '.join(str(x) for x in row))


if __name__ == '__main__':
    solve()'''

_PY08 = r'''import sys
import io


def solve():
    text = sys.stdin.read().strip()
    # Context manager: tu dong dong (giai phong) bo nho khi ra khoi khoi with
    with io.StringIO() as f:
        f.write(text)
        f.seek(0)
        data = f.read()
    print(data.upper())


if __name__ == '__main__':
    solve()'''

_PY09 = r'''import sys


class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            return None
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def size(self):
        return len(self._items)


def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    st = Stack()
    for x in data[1:1 + n]:
        st.push(int(x))

    st.pop()
    st.pop()

    top = st.peek()
    print('Top: ' + ('None' if top is None else str(top)))
    print('Size: ' + str(st.size()))


if __name__ == '__main__':
    solve()'''

_PY10 = r'''import sys


class ScoreOutOfRangeException(Exception):
    pass


def kiem_tra_diem(diem):
    if diem < 0 or diem > 10:
        raise ScoreOutOfRangeException('Diem khong hop le')
    return diem


def solve():
    raw = sys.stdin.read().strip()
    if not raw:
        return
    diem = float(raw)
    try:
        kiem_tra_diem(diem)
        if diem == int(diem):
            print('Diem: ' + str(int(diem)))
        else:
            print('Diem: ' + str(diem))
    except ScoreOutOfRangeException:
        print('LOI: Diem khong hop le')


if __name__ == '__main__':
    solve()'''

# Bai #47 (Python 05): sua loi xuong dong lot trong string literal
_PY05 = r'''import sys


def search_insert(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return low


if __name__ == '__main__':
    # Dung split() thay cho split('\n') de tranh loi escape khi sinh seed
    data = sys.stdin.read().split()
    if len(data) >= 2:
        target = int(data[0])
        nums = [int(x) for x in data[1:]]
        print(search_insert(nums, target))'''


def _tc(input_text, expected, hidden=False):
    return {"input": input_text, "expected_output": expected, "is_hidden": hidden}


EXERCISE_FIXES = [
    # ------------------------------ C# (môn 5) ------------------------------
    {
        "subject_id": SUBJECT_CSHARP,
        "title_prefix": "C# 06",
        "title": "C# 06: Nạp Chồng Toán Tử (Operator Overloading) Class PhanSo",
        "problem": (
            "Cài đặt class `PhanSo` có hai thuộc tính `Tu` (tử) và `Mau` (mẫu). "
            "Nạp chồng toán tử `+` để cộng hai phân số, sau đó tự động rút gọn kết quả "
            "bằng ước chung lớn nhất (UCLN).\n\n"
            "Đầu vào: một dòng 4 số nguyên `a b c d` tương ứng hai phân số a/b và c/d.\n"
            "Đầu ra: phân số tổng đã rút gọn, định dạng `tu/mau`. Nếu mẫu âm thì đưa dấu âm lên tử."
        ),
        "specs": [
            "Cài đặt `public static PhanSo operator +(PhanSo a, PhanSo b)`.",
            "Viết hàm `Ucln(int a, int b)` bằng thuật toán Euclid để rút gọn phân số.",
            "Đầu ra luôn ở dạng tối giản, ví dụ '1 2 1 2' -> '1/1'."
        ],
        "language": "csharp",
        "sample_code": _CS06,
        "test_cases": [
            _tc("1 2 1 3", "5/6"),
            _tc("1 2 1 2", "1/1"),
            _tc("1 3 2 3", "1/1", True),
            _tc("3 4 1 4", "1/1", True),
            _tc("1 6 1 3", "1/2", True),
        ],
    },
    {
        "subject_id": SUBJECT_CSHARP,
        "title_prefix": "C# 07",
        "title": "C# 07: Kế Thừa Đa Tầng NhanVien, TruongPhong, GiamDoc",
        "problem": (
            "Xây dựng ba lớp kế thừa nhau: `NhanVien` (lớp cha), `TruongPhong` kế thừa "
            "`NhanVien`, `GiamDoc` kế thừa `TruongPhong`.\n\n"
            "Mỗi lớp ghi đè `TinhLuong()` và `ChucVu()`:\n"
            "- NhanVien: lương = lương cơ bản, chức vụ 'Nhan vien'\n"
            "- TruongPhong: lương = cơ bản + 20% cơ bản, chức vụ 'Truong phong'\n"
            "- GiamDoc: lương = cơ bản + 50% cơ bản, chức vụ 'Giam doc'\n\n"
            "Đầu vào: một dòng gồm mã loại (`NV`, `TP`, `GD`) và lương cơ bản.\n"
            "Đầu ra: `ChucVu - Luong`, ví dụ 'TP 10000000' -> 'Truong phong - 12000000'."
        ),
        "specs": [
            "Dùng `virtual` ở lớp cha và `override` ở lớp con (đa hình).",
            "Tính lương bằng số nguyên để tránh sai số dấu phẩy động.",
            "Gọi `TinhLuong()` qua biến kiểu `NhanVien` để chứng minh đa hình hoạt động."
        ],
        "language": "csharp",
        "sample_code": _CS07,
        "test_cases": [
            _tc("NV 10000000", "Nhan vien - 10000000"),
            _tc("TP 10000000", "Truong phong - 12000000"),
            _tc("GD 10000000", "Giam doc - 15000000", True),
            _tc("TP 20000000", "Truong phong - 24000000", True),
            _tc("GD 20000000", "Giam doc - 30000000", True),
        ],
    },
    {
        "subject_id": SUBJECT_CSHARP,
        "title_prefix": "C# 08",
        "title": "C# 08: Custom Exception SoDuKhongDuException Trong BankAccount",
        "problem": (
            "Tạo lớp ngoại lệ tự định nghĩa `SoDuKhongDuException` kế thừa `Exception`. "
            "Class `BankAccount` có phương thức `Rut(int soTien)`: nếu số tiền rút lớn hơn "
            "số dư thì `throw new SoDuKhongDuException(...)`.\n\n"
            "Đầu vào: một dòng gồm `soDu` và `soTienRut`.\n"
            "Đầu ra: nếu rút thành công in `Con lai: X`, nếu không đủ tiền in "
            "`LOI: So du khong du` (bắt bằng `catch`)."
        ),
        "specs": [
            "Khai báo `public class SoDuKhongDuException : Exception` có constructor nhận message.",
            "Kiểm tra `soTien > SoDu` TRƯỚC khi trừ tiền.",
            "Bắt ngoại lệ bằng `catch (SoDuKhongDuException)` — không dùng catch-all."
        ],
        "language": "csharp",
        "sample_code": _CS08,
        "test_cases": [
            _tc("1000 500", "Con lai: 500"),
            _tc("1000 2000", "LOI: So du khong du"),
            _tc("0 1", "LOI: So du khong du", True),
            _tc("500 500", "Con lai: 0", True),
            _tc("10000 9999", "Con lai: 1", True),
        ],
    },
    {
        "subject_id": SUBJECT_CSHARP,
        "title_prefix": "C# 09",
        "title": "C# 09: Generic Repository Pattern IRepository<T>",
        "problem": (
            "Cài đặt mẫu thiết kế Repository dùng Generic: interface `IRepository<T>` gồm "
            "`Add(T item)`, `GetAll()`, `Count`. Lớp `ListRepository<T>` hiện thực bằng `List<T>`.\n\n"
            "Đầu vào: dòng 1 là số nguyên `n`, dòng 2 gồm `n` số nguyên.\n"
            "Đầu ra: hai dòng `Count: <số phần tử>` và `Sum: <tổng các phần tử>`."
        ),
        "specs": [
            "Interface phải khai báo generic `<T>`, không dùng kiểu cụ thể.",
            "Không dùng LINQ `.Sum()` — duyệt `foreach` để thể hiện hiểu `GetAll()`.",
            "Với n = 0 vẫn in `Count: 0` và `Sum: 0`."
        ],
        "language": "csharp",
        "sample_code": _CS09,
        "test_cases": [
            _tc("3\n1 2 3", "Count: 3\nSum: 6"),
            _tc("0", "Count: 0\nSum: 0"),
            _tc("5\n10 20 30 40 50", "Count: 5\nSum: 150", True),
            _tc("1\n7", "Count: 1\nSum: 7", True),
            _tc("2\n-5 5", "Count: 2\nSum: 0", True),
        ],
    },
    {
        "subject_id": SUBJECT_CSHARP,
        "title_prefix": "C# 10",
        "title": "C# 10: Event & Delegate - Hệ Thống Cảnh Báo Nhiệt Độ MayChu",
        "problem": (
            "Tạo `delegate void NhietDoCaoHandler(int nhietDo)` và event `OnNhietDoCao` "
            "trong class `MayChu`. Khi nhiệt độ > 80 thì kích hoạt event.\n\n"
            "Đầu vào: một số nguyên là nhiệt độ hiện tại.\n"
            "Đầu ra: nếu > 80 in `CANH BAO: Nhiet do cao - X`, ngược lại in `Binh thuong - X`."
        ),
        "specs": [
            "Khai báo `public event NhietDoCaoHandler OnNhietDoCao;`.",
            "Luôn kiểm tra `if (OnNhietDoCao != null)` trước khi gọi event (tránh NullReferenceException).",
            "Đăng ký handler bằng `+=` với anonymous method hoặc lambda."
        ],
        "language": "csharp",
        "sample_code": _CS10,
        "test_cases": [
            _tc("90", "CANH BAO: Nhiet do cao - 90"),
            _tc("80", "Binh thuong - 80"),
            _tc("100", "CANH BAO: Nhiet do cao - 100", True),
            _tc("25", "Binh thuong - 25", True),
            _tc("81", "CANH BAO: Nhiet do cao - 81", True),
        ],
    },
    # ----------------------------- Python (môn 22) -----------------------------
    {
        "subject_id": SUBJECT_PYTHON,
        "title_prefix": "Python 05",
        "title": "Python 05: Tìm Kiếm Nhị Phân (Binary Search) & Vị Trí Chèn",
        "problem": (
            "Cho danh sách số nguyên tăng dần và số nguyên target. Dùng Binary Search tìm vị trí "
            "(chỉ số 0-based) của target. Nếu không tìm thấy, in ra vị trí mà target nên được chèn "
            "vào để danh sách vẫn giữ nguyên thứ tự sắp xếp.\n\n"
            "Đầu vào: dòng 1 chứa target. Dòng 2 chứa danh sách số nguyên tăng dần.\n"
            "Đầu ra: chỉ số vị trí tìm thấy hoặc vị trí chèn."
        ),
        "specs": [
            "Độ phức tạp O(log N) — không dùng `in` hay `list.index()`.",
            "Đầu vào: dòng 1 chứa target, dòng 2 chứa danh sách số nguyên tăng dần.",
            "Đầu ra: chỉ số vị trí tìm thấy hoặc vị trí chèn."
        ],
        "language": "python",
        "sample_code": _PY05,
        "test_cases": [
            _tc("5\n1 3 5 6", "2"),
            _tc("2\n1 3 5 6", "1"),
            _tc("7\n1 3 5 6", "4", True),
            _tc("0\n1 3 5 6", "0", True),
            _tc("3\n3", "0", True),
        ],
    },
    {
        "subject_id": SUBJECT_PYTHON,
        "title_prefix": "Python 06",
        "title": "Python 06: List Comprehension & Lọc Số Nguyên Tố",
        "problem": (
            "Cho `n` số nguyên. Hãy dùng **list comprehension** để lọc ra các số nguyên tố "
            "và in chúng trên một dòng, cách nhau bởi dấu cách.\n\n"
            "Đầu vào: dòng 1 là số lượng `n`, dòng 2 gồm `n` số nguyên.\n"
            "Đầu ra: các số nguyên tố theo đúng thứ tự xuất hiện; nếu không có số nào thì in dòng trống."
        ),
        "specs": [
            "Viết hàm `is_prime(n)` xử lý đúng cả số < 2.",
            "Bắt buộc dùng list comprehension: `[x for x in nums if is_prime(x)]`.",
            "In bằng `' '.join(...)` — không in dấu cách thừa ở cuối."
        ],
        "language": "python",
        "sample_code": _PY06,
        "test_cases": [
            _tc("5\n1 2 3 4 5", "2 3 5"),
            _tc("4\n4 6 8 9", ""),
            _tc("6\n7 11 13 17 19 23", "7 11 13 17 19 23", True),
            _tc("1\n2", "2", True),
            _tc("3\n1 1 1", "", True),
        ],
    },
    {
        "subject_id": SUBJECT_PYTHON,
        "title_prefix": "Python 07",
        "title": "Python 07: Thao Tác Ma Trận 2D & Chuyển Vị (Transpose)",
        "problem": (
            "Cho ma trận vuông kích thước `N x N`. Hãy in ra ma trận chuyển vị (transpose) "
            "bằng cách dùng `zip(*matrix)`.\n\n"
            "Đầu vào: dòng 1 là `N`, `N` dòng tiếp theo mỗi dòng gồm `N` số nguyên.\n"
            "Đầu ra: `N` dòng của ma trận chuyển vị, các số cách nhau bởi dấu cách."
        ),
        "specs": [
            "Dùng `zip(*matrix)` để chuyển vị, không viết vòng lặp hai chiều thủ công.",
            "Đọc input bằng `sys.stdin.read().splitlines()` và bỏ qua dòng trống.",
            "Mỗi dòng output có đúng `N` số."
        ],
        "language": "python",
        "sample_code": _PY07,
        "test_cases": [
            _tc("2\n1 2\n3 4", "1 3\n2 4"),
            _tc("3\n1 2 3\n4 5 6\n7 8 9", "1 4 7\n2 5 8\n3 6 9"),
            _tc("1\n5", "5", True),
            _tc("2\n1 1\n2 2", "1 2\n1 2", True),
            _tc("3\n1 2 3\n1 2 3\n1 2 3", "1 1 1\n2 2 2\n3 3 3", True),
        ],
    },
    {
        "subject_id": SUBJECT_PYTHON,
        "title_prefix": "Python 08",
        "title": "Python 08: Đọc Ghi File Giả Lập Bằng Context Manager With",
        "problem": (
            "Dùng context manager `with` để ghi một chuỗi vào bộ nhớ đệm (`io.StringIO`), "
            "đưa con trỏ về đầu (`seek(0)`), đọc lại và in ra chữ IN HOA.\n\n"
            "Đầu vào: một dòng văn bản.\n"
            "Đầu ra: nội dung đó ở dạng chữ in hoa."
        ),
        "specs": [
            "Bắt buộc dùng `with io.StringIO() as f:` — không đóng file thủ công.",
            "Phải gọi `f.seek(0)` trước khi đọc lại, nếu không sẽ đọc được chuỗi rỗng.",
            "In bằng `print(data.upper())`."
        ],
        "language": "python",
        "sample_code": _PY08,
        "test_cases": [
            _tc("hello", "HELLO"),
            _tc("UniMaster", "UNIMASTER"),
            _tc("abc def", "ABC DEF", True),
            _tc("123", "123", True),
            _tc("python", "PYTHON", True),
        ],
    },
    {
        "subject_id": SUBJECT_PYTHON,
        "title_prefix": "Python 09",
        "title": "Python 09: Cài Đặt Ngăn Xếp Stack Dùng Class & List",
        "problem": (
            "Xây dựng class `Stack` (LIFO) với các phương thức `push`, `pop`, `peek`, `size`, "
            "dùng `list` bên trong.\n\n"
            "Đầu vào: dòng 1 là `n`, dòng 2 gồm `n` số nguyên lần lượt được push vào stack.\n"
            "Sau đó **pop hai lần**, rồi in ra:\n"
            "- `Top: <giá trị đỉnh>` (in `None` nếu stack rỗng)\n"
            "- `Size: <số phần tử còn lại>`"
        ),
        "specs": [
            "`pop()` trên stack rỗng phải trả về `None`, KHÔNG được ném IndexError.",
            "`peek()` trả về `None` khi stack rỗng.",
            "Dùng `self._items` (có gạch dưới) để thể hiện đóng gói."
        ],
        "language": "python",
        "sample_code": _PY09,
        "test_cases": [
            _tc("3\n1 2 3", "Top: 1\nSize: 1"),
            _tc("1\n5", "Top: None\nSize: 0"),
            _tc("5\n10 20 30 40 50", "Top: 30\nSize: 3", True),
            _tc("0", "Top: None\nSize: 0", True),
            _tc("2\n7 8", "Top: None\nSize: 0", True),
        ],
    },
    {
        "subject_id": SUBJECT_PYTHON,
        "title_prefix": "Python 10",
        "title": "Python 10: Xử Lý Ngoại Lệ Tùy Biến Custom Exception",
        "problem": (
            "Tạo class `ScoreOutOfRangeException` kế thừa `Exception`. Viết hàm "
            "`kiem_tra_diem(diem)` ném ngoại lệ này khi điểm < 0 hoặc > 10.\n\n"
            "Đầu vào: một số thực là điểm.\n"
            "Đầu ra: nếu hợp lệ in `Diem: X`, nếu không in `LOI: Diem khong hop le`."
        ),
        "specs": [
            "Khai báo `class ScoreOutOfRangeException(Exception): pass`.",
            "Điều kiện biên: điểm 0 và 10 là HỢP LỆ, chỉ < 0 hoặc > 10 mới lỗi.",
            "In số nguyên khi điểm là số nguyên (8.0 -> '8'), giữ 1 dấu thập phân khi lẻ."
        ],
        "language": "python",
        "sample_code": _PY10,
        "test_cases": [
            _tc("8", "Diem: 8"),
            _tc("15", "LOI: Diem khong hop le"),
            _tc("-1", "LOI: Diem khong hop le", True),
            _tc("10", "Diem: 10", True),
            _tc("7.5", "Diem: 7.5", True),
        ],
    },
]


def repair_coding_exercises(conn) -> int:
    """Vá 11 bài hỏng. Trả về số bài đã cập nhật.

    Chạy mỗi lần khởi động app nhưng chỉ UPDATE thật khi `FIXES_REV` thay đổi,
    nên gần như không tốn thời gian.
    """
    import json as _json

    cur = conn.cursor()
    try:
        row = cur.execute(
            "SELECT value FROM settings WHERE key = 'coding_exercises_rev'"
        ).fetchone()
        current_rev = row[0] if row else None
        if current_rev == FIXES_REV:
            return 0
    except Exception:
        current_rev = None

    updated = 0
    for item in EXERCISE_FIXES:
        try:
            cur.execute(
                """
                UPDATE exercises
                   SET title = ?, problem = ?, specs_json = ?, sample_code = ?,
                       solution_code = ?, test_cases_json = ?, language = ?,
                       difficulty = 'medium'
                 WHERE subject_id = ? AND title LIKE ?
                """,
                (
                    item["title"],
                    item["problem"],
                    _json.dumps(item["specs"], ensure_ascii=False),
                    item["sample_code"],
                    item["sample_code"],
                    _json.dumps(item["test_cases"], ensure_ascii=False),
                    item["language"],
                    item["subject_id"],
                    item["title_prefix"] + "%",
                ),
            )
            updated += cur.rowcount or 0
        except Exception:
            continue

    try:
        cur.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            ("coding_exercises_rev", FIXES_REV),
        )
    except Exception:
        pass

    try:
        conn.commit()
    except Exception:
        pass

    return updated
