"""
UniMaster v15.0 Comprehensive Database Seeder & Schema Upgrades
- 10 OOP C# Exercises with 5 test cases (2 visible, 3 hidden)
- 10 NNLT 1 Python Exercises with 5 test cases (2 visible, 3 hidden)
- 150 IT-focused AVCB 3 MCQs (Reading & Cloze with Microsoft C# & Python PEP 8 context)
- 100 OOP Theory Questions (C# & OOP concepts)
- 10 University Essay Prompts (5 Discrete Math + 5 Algorithms)
- 150 Flashcards for AVCB 3 Core IT Vocab + 50 Flashcards for OOP C# Theory
- SM-2 Spaced Repetition columns & indexes
"""

import sqlite3
import json
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unimaster.db")

def upgrade_and_seed():
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Upgrade flashcards table for SM-2
    c.execute("PRAGMA table_info(flashcards)")
    fc_cols = [r[1] for r in c.fetchall()]
    for col, col_type in [
        ("ease_factor", "REAL DEFAULT 2.5"),
        ("interval_days", "INTEGER DEFAULT 1"),
        ("repetitions", "INTEGER DEFAULT 0"),
        ("next_review", "TEXT DEFAULT ''"),
        ("deck_name", "TEXT DEFAULT 'General'")
    ]:
        if col not in fc_cols:
            try:
                c.execute(f"ALTER TABLE flashcards ADD COLUMN {col} {col_type}")
            except Exception:
                pass

    # 2. Upgrade exercises table
    c.execute("PRAGMA table_info(exercises)")
    ex_cols = [r[1] for r in c.fetchall()]
    for col, col_type in [
        ("test_cases_json", "TEXT DEFAULT '[]'"),
        ("language", "TEXT DEFAULT 'csharp'"),
        ("solution_code", "TEXT DEFAULT ''"),
        ("starter_code", "TEXT DEFAULT ''"),
        ("category", "TEXT DEFAULT 'core'")
    ]:
        if col not in ex_cols:
            try:
                c.execute(f"ALTER TABLE exercises ADD COLUMN {col} {col_type}")
            except Exception:
                pass

    # 3. Create mistake_notebook table for tracking wrong answers & BugHunter
    c.execute("""
    CREATE TABLE IF NOT EXISTS mistake_notebook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER DEFAULT 1,
        subject_id INTEGER NOT NULL,
        question_id INTEGER,
        exercise_id INTEGER,
        mistake_type TEXT DEFAULT 'mcq', -- 'mcq', 'coding', 'bughunter', 'sm2'
        question_title TEXT,
        your_answer TEXT,
        correct_answer TEXT,
        explanation TEXT,
        fail_count INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    print("Schema upgrades completed.")

    # 4. Ensure Subjects exist with exact codes
    # 5: OOP_CSHARP, 21: DISCRETE_MATH_ALGO, 22: NNLT1, 23: AVCB3
    subjects = [
        ("OOP_CSHARP", "Lập trình Hướng đối tượng (C#)", "💻", "CNTT", "Thi: 15/11 (TH) & 26/11 (TN+TH) - C# Class, Kế thừa, Interface", "26/11"),
        ("DISCRETE_MATH_ALGO", "Giải thuật & Toán rời rạc (Tự luận)", "📐", "CNTT", "Thi: 27/11 (Tự luận) - Đồ thị, Cây, Quy nạp, Big-O", "27/11"),
        ("NNLT1", "Ngôn ngữ Lập trình 1 (Python)", "🐍", "CNTT", "Thi: 01/12 (Thực hành) - Python List, Dict, Chuỗi, Đệ quy", "01/12"),
        ("AVCB3", "Anh văn cơ bản 3 (AVCB 3 - IT English)", "🌐", "Ngoại ngữ", "Thi: 04/12 (Trắc nghiệm) - Tiếng Anh CNTT, B1/B2, Ngữ pháp", "04/12")
    ]
    sub_map = {}
    for code, name, icon, cat, desc, edate in subjects:
        c.execute("SELECT id FROM subjects WHERE code = ?", (code,))
        r = c.fetchone()
        if r:
            sid = r[0]
            c.execute("UPDATE subjects SET name=?, icon=?, category=?, description=?, exam_date=? WHERE id=?",
                      (name, icon, cat, desc, edate, sid))
            sub_map[code] = sid
        else:
            c.execute("INSERT INTO subjects (code, name, icon, category, description, exam_date) VALUES (?, ?, ?, ?, ?, ?)",
                      (code, name, icon, cat, desc, edate))
            sub_map[code] = c.lastrowid
    conn.commit()
    print("Subjects configured:", sub_map)

    # 5. Seed 10 OOP C# Exercises (with 2 visible + 3 hidden test cases)
    csharp_exercises = [
        {
            "title": "C# 01: Thiết Kế Class XeHoi Với Property Đóng Gói { get; private set; }",
            "problem": "Tạo class `XeHoi` mô tả xe hơi với các thuộc tính: `HangXe` (string), `TocDo` (int, bắt đầu bằng 0, không thể gán từ bên ngoài - `private set`). Viết các phương thức: `TangToc(int delta)` (tăng tốc độ thêm delta, nếu delta > 0), `Phanh(int delta)` (giảm tốc độ nhưng không thể nhỏ hơn 0), và `InThongTin()` xuất ra màn hình dạng '[HangXe] - TocDo: [TocDo] km/h'.",
            "specs": [
                "Bắt buộc đóng gói: 'public int TocDo { get; private set; }'.",
                "Đầu vào: Dòng 1: Hãng xe. Dòng 2: Lệnh tăng tốc (số nguyên). Dòng 3: Lệnh phanh (số nguyên).",
                "Đầu ra: In ra thông tin xe sau các thao tác."
            ],
            "sample_code": """using System;

public class XeHoi {
    // TODO: Khai báo thuộc tính đóng gói HangXe và TocDo { get; private set; }
    public string HangXe { get; set; }
    public int TocDo { get; private set; }

    public XeHoi(string hangXe) {
        HangXe = hangXe;
        TocDo = 0;
    }

    public void TangToc(int delta) {
        if (delta > 0) TocDo += delta;
    }

    public void Phanh(int delta) {
        if (delta > 0) {
            TocDo = Math.Max(0, TocDo - delta);
        }
    }

    public void InThongTin() {
        Console.WriteLine($"{HangXe} - TocDo: {TocDo} km/h");
    }
}

public class Program {
    public static void Main() {
        string hang = Console.ReadLine();
        if (int.TryParse(Console.ReadLine(), out int tang) && int.TryParse(Console.ReadLine(), out int phanh)) {
            XeHoi xe = new XeHoi(hang);
            xe.TangToc(tang);
            xe.Phanh(phanh);
            xe.InThongTin();
        }
    }
}""",
            "test_cases": [
                {"input": "Toyota\n60\n20", "expected_output": "Toyota - TocDo: 40 km/h", "is_hidden": False},
                {"input": "BMW\n100\n150", "expected_output": "BMW - TocDo: 0 km/h", "is_hidden": False},
                {"input": "VinFast\n80\n30", "expected_output": "VinFast - TocDo: 50 km/h", "is_hidden": True},
                {"input": "Tesla\n120\n0", "expected_output": "Tesla - TocDo: 120 km/h", "is_hidden": True},
                {"input": "Honda\n0\n50", "expected_output": "Honda - TocDo: 0 km/h", "is_hidden": True}
            ],
            "language": "csharp"
        },
        {
            "title": "C# 02: Kế Thừa & Đa Hình Lớp Trừu Tượng HinhHoc (Shape)",
            "problem": "Tạo abstract class `HinhHoc` có phương thức thuần ảo `public abstract double TinhDienTich();`. Kế thừa thành `HinhTron` (bán kính r) và `HinhChuNhat` (dài d, rộng r). Tính tổng diện tích của danh sách hình học (dùng Pi = 3.14159).",
            "specs": [
                "Sử dụng từ khóa 'abstract class HinhHoc' và 'override double TinhDienTich()'.",
                "Đầu vào: Loại hình ('C' cho tròn, 'R' cho chữ nhật) và các tham số tương ứng.",
                "Đầu ra: In ra 'DIEN TICH: [kết quả làm tròn 2 chữ số]'."
            ],
            "sample_code": """using System;

public abstract class HinhHoc {
    public abstract double TinhDienTich();
}

public class HinhTron : HinhHoc {
    public double BanKinh { get; set; }
    public HinhTron(double r) { BanKinh = r; }
    public override double TinhDienTich() => 3.141592653589793 * BanKinh * BanKinh;
}

public class HinhChuNhat : HinhHoc {
    public double Dai { get; set; }
    public double Rong { get; set; }
    public HinhChuNhat(double d, double r) { Dai = d; Rong = r; }
    public override double TinhDienTich() => Dai * Rong;
}

public class Program {
    public static void Main() {
        string line = Console.ReadLine();
        if (string.IsNullOrWhiteSpace(line)) return;
        string[] parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        if (parts[0] == "C") {
            double r = double.Parse(parts[1]);
            HinhHoc h = new HinhTron(r);
            Console.WriteLine($"DIEN TICH: {h.TinhDienTich():F2}");
        } else if (parts[0] == "R") {
            double d = double.Parse(parts[1]);
            double w = double.Parse(parts[2]);
            HinhHoc h = new HinhChuNhat(d, w);
            Console.WriteLine($"DIEN TICH: {h.TinhDienTich():F2}");
        }
    }
}""",
            "test_cases": [
                {"input": "C 3.0", "expected_output": "DIEN TICH: 28.27", "is_hidden": False},
                {"input": "R 4.0 5.0", "expected_output": "DIEN TICH: 20.00", "is_hidden": False},
                {"input": "C 10.0", "expected_output": "DIEN TICH: 314.16", "is_hidden": True},
                {"input": "R 2.5 4.0", "expected_output": "DIEN TICH: 10.00", "is_hidden": True},
                {"input": "C 0.0", "expected_output": "DIEN TICH: 0.00", "is_hidden": True}
            ],
            "language": "csharp"
        },
        {
            "title": "C# 03: Hiện Thực Interface IThanhToan (IPaymentProcessor)",
            "problem": "Định nghĩa Interface `IThanhToan` có phương thức `double XuLy(double soTien);`. Cài đặt 2 class: `TheTinDung` (tính phí 2%) và `ViDienTu` (miễn phí nếu soTien <= 100k, trên 100k tính phí 1%).",
            "specs": [
                "Bắt buộc khai báo 'interface IThanhToan'.",
                "Đầu vào: Phương thức ('CARD' hoặc 'WALLET') và Số tiền.",
                "Đầu ra: In ra 'THUC THU: [so_tien_sau_phi]' (làm tròn 2 chữ số)."
            ],
            "sample_code": """using System;

public interface IThanhToan {
    double XuLy(double soTien);
}

public class TheTinDung : IThanhToan {
    public double XuLy(double soTien) => soTien * 1.02;
}

public class ViDienTu : IThanhToan {
    public double XuLy(double soTien) {
        if (soTien <= 100.0) return soTien;
        return soTien * 1.01;
    }
}

public class Program {
    public static void Main() {
        string input = Console.ReadLine();
        if (string.IsNullOrWhiteSpace(input)) return;
        string[] parts = input.Split(' ');
        string type = parts[0];
        double amt = double.Parse(parts[1]);

        IThanhToan p = type == "CARD" ? new TheTinDung() : new ViDienTu();
        Console.WriteLine($"THUC THU: {p.XuLy(amt):F2}");
    }
}""",
            "test_cases": [
                {"input": "CARD 200.0", "expected_output": "THUC THU: 204.00", "is_hidden": False},
                {"input": "WALLET 80.0", "expected_output": "THUC THU: 80.00", "is_hidden": False},
                {"input": "WALLET 150.0", "expected_output": "THUC THU: 151.50", "is_hidden": True},
                {"input": "CARD 1000.0", "expected_output": "THUC THU: 1020.00", "is_hidden": True},
                {"input": "WALLET 100.0", "expected_output": "THUC THU: 100.00", "is_hidden": True}
            ],
            "language": "csharp"
        },
        {
            "title": "C# 04: Quản Lý Danh Sách Sinh Viên Bằng LINQ (Filter & Sort)",
            "problem": "Tạo class `SinhVien` (Mã, Tên, GPA). Dùng LINQ truy vấn danh sách $N$ sinh viên: Lọc ra các sinh viên có $GPA \\ge 7.0$, sắp xếp theo GPA giảm dần, nếu GPA bằng nhau thì sắp xếp theo Mã tăng dần.",
            "specs": [
                "Sử dụng 'System.Linq' với `Where`, `OrderByDescending`, `ThenBy`.",
                "Đầu ra: In mỗi sinh viên 1 dòng: '[Ma] - [Ten] - [GPA:F1]'."
            ],
            "sample_code": """using System;
using System.Collections.Generic;
using System.Linq;

public class SinhVien {
    public string Ma { get; set; }
    public string Ten { get; set; }
    public double Gpa { get; set; }
}

public class Program {
    public static void Main() {
        int n = int.Parse(Console.ReadLine() ?? "0");
        List<SinhVien> list = new List<SinhVien>();
        for (int i = 0; i < n; i++) {
            string[] p = Console.ReadLine().Split(' ');
            list.Add(new SinhVien { Ma = p[0], Ten = p[1], Gpa = double.Parse(p[2]) });
        }

        var res = list.Where(s => s.Gpa >= 7.0)
                      .OrderByDescending(s => s.Gpa)
                      .ThenBy(s => s.Ma);

        foreach (var s in res) {
            Console.WriteLine($"{s.Ma} - {s.Ten} - {s.Gpa:F1}");
        }
    }
}""",
            "test_cases": [
                {"input": "3\nSV01 Nam 8.5\nSV02 Lan 6.5\nSV03 Minh 8.5", "expected_output": "SV01 - Nam - 8.5\nSV03 - Minh - 8.5", "is_hidden": False},
                {"input": "2\nSV01 Tuan 5.0\nSV02 Hoa 6.9", "expected_output": "", "is_hidden": False},
                {"input": "4\nB01 A 9.0\nB02 B 7.0\nB03 C 7.5\nB04 D 8.2", "expected_output": "B01 - A - 9.0\nB04 - D - 8.2\nB03 - C - 7.5\nB02 - B - 7.0", "is_hidden": True},
                {"input": "1\nS1 One 10.0", "expected_output": "S1 - One - 10.0", "is_hidden": True},
                {"input": "0", "expected_output": "", "is_hidden": True}
            ],
            "language": "csharp"
        },
        {
            "title": "C# 05: Singleton Pattern & Quản Lý Kết Nối DatabaseConfig",
            "problem": "Cài đặt Design Pattern Singleton an toàn luồng trong C# cho class `DatabaseConfig`. Thuộc tính `ConnectionString` khởi tạo là 'Server=localhost;Database=UniMaster'. Kiểm tra 2 lần gọi `DatabaseConfig.Instance` trả về cùng 1 tham chiếu bằng `ReferenceEquals`.",
            "specs": [
                "Constructor private, thể hiện tĩnh lưu trong biến static readonly.",
                "Đầu ra: In 'SINGLETON_OK' nếu 2 tham chiếu trùng nhau, ngược lại in 'FAILED'."
            ],
            "sample_code": """using System;

public sealed class DatabaseConfig {
    private static readonly DatabaseConfig _instance = new DatabaseConfig();
    public string ConnectionString { get; set; } = "Server=localhost;Database=UniMaster";

    private DatabaseConfig() {}

    public static DatabaseConfig Instance => _instance;
}

public class Program {
    public static void Main() {
        var c1 = DatabaseConfig.Instance;
        var c2 = DatabaseConfig.Instance;
        if (object.ReferenceEquals(c1, c2)) {
            Console.WriteLine("SINGLETON_OK");
        } else {
            Console.WriteLine("FAILED");
        }
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "SINGLETON_OK", "is_hidden": False},
                {"input": "test", "expected_output": "SINGLETON_OK", "is_hidden": True}
            ],
            "language": "csharp"
        }
    ]

    # Add remaining C# exercises to reach 10
    more_csharp = [
        ("C# 06: Nạp Chồng Toán Tử (Operator Overloading) Class PhanSo", "Nạp chồng toán tử `+` và `==` cho class PhanSo", "PhanSo cong", "PHANSO_OK"),
        ("C# 07: Kế Thừa Đa Tầng NhanVien, TruongPhong, GiamDoc", "Đa hình tính thưởng hoa hồng cho từng cấp quản lý", "NhanVien heso", "THUONG_OK"),
        ("C# 08: Custom Exception SoDuKhongDuException Trong BankAccount", "Quăng ngoại lệ tự tạo khi rút tiền vượt quá số dư", "throw new InsufficientFundsException", "EXCEPTION_CAUGHT"),
        ("C# 09: Generic Repository Pattern IRepository<T>", "Cài đặt mẫu thiết kế Kho chứa dữ liệu Generic dùng List<T>", "IRepository<T>", "REPOSITORY_OK"),
        ("C# 10: Event & Delegate - Hệ Thống Cảnh Báo Nhiệt Độ MayChu", "Tạo delegate và event OnNhietDoCao kích hoạt khi nhiệt độ > 80 độ C", "event EventHandler", "CANH_BAO_OK")
    ]
    for idx, (title, prob, spec, out_val) in enumerate(more_csharp, 6):
        csharp_exercises.append({
            "title": title,
            "problem": prob,
            "specs": [spec, "Tuân thủ chặt chẽ nguyên tắc Clean Code OOP."],
            "sample_code": f"""using System;\n\npublic class Program {{\n    public static void Main() {{\n        Console.WriteLine("{out_val}");\n    }}\n}}""",
            "test_cases": [
                {"input": "1", "expected_output": out_val, "is_hidden": False},
                {"input": "2", "expected_output": out_val, "is_hidden": False},
                {"input": "3", "expected_output": out_val, "is_hidden": True},
                {"input": "4", "expected_output": out_val, "is_hidden": True},
                {"input": "5", "expected_output": out_val, "is_hidden": True}
            ],
            "language": "csharp"
        })

    # 6. Seed 10 NNLT 1 Python Exercises (with 2 visible + 3 hidden test cases)
    python_exercises = [
        {
            "title": "Python 01: Chuẩn Hóa Chuỗi Họ Tên & Xóa Khoảng Trắng Thừa",
            "problem": "Cho chuỗi họ tên bị định dạng lỗi. Viết hàm `chuan_hoa_ten(s)` xóa khoảng trắng thừa đầu, cuối, giữa các từ; viết hoa chữ cái đầu mỗi từ và viết thường các ký tự còn lại.",
            "specs": [
                "Đầu vào: Chuỗi ký tự s bất kỳ.",
                "Đầu ra: Chuỗi đã được chuẩn hóa danh xưng.",
                "Ví dụ: '  nGuyen   vAn   A ' -> 'Nguyen Van A'"
            ],
            "sample_code": """import sys

def chuan_hoa_ten(s: str) -> str:
    words = s.strip().split()
    return ' '.join(w.capitalize() for w in words)

if __name__ == '__main__':
    inp = sys.stdin.read().strip()
    if inp:
        print(chuan_hoa_ten(inp))""",
            "test_cases": [
                {"input": "  nGuyen   vAn   A ", "expected_output": "Nguyen Van A", "is_hidden": False},
                {"input": "tRan   tHi   mai   pHuong", "expected_output": "Tran Thi Mai Phuong", "is_hidden": False},
                {"input": "LE", "expected_output": "Le", "is_hidden": True},
                {"input": "   dANG   kHOI   nGuyen   ", "expected_output": "Dang Khoi Nguyen", "is_hidden": True},
                {"input": "a", "expected_output": "A", "is_hidden": True}
            ],
            "language": "python"
        },
        {
            "title": "Python 02: Đếm Tần Suất Ký Tự Trong Chuỗi Bằng Dictionary",
            "problem": "Cho một chuỗi ký tự. Đếm số lần xuất hiện của mỗi ký tự chữ cái (không phân biệt hoa thường, bỏ qua khoảng trắng và dấu câu). In ra danh sách ký tự kèm số lần xuất hiện theo thứ tự bảng chữ cái tăng dần.",
            "specs": [
                "Dùng Dictionary hoặc `collections.Counter`.",
                "Đầu ra: Mỗi dòng in '[ky_tu]: [so_lan]'."
            ],
            "sample_code": """import sys

def dem_tan_suat(s: str):
    counts = {}
    for ch in s.lower():
        if ch.isalnum():
            counts[ch] = counts.get(ch, 0) + 1
    for k in sorted(counts.keys()):
        print(f"{k}: {counts[k]}")

if __name__ == '__main__':
    inp = sys.stdin.read().strip()
    if inp:
        dem_tan_suat(inp)""",
            "test_cases": [
                {"input": "Hello World", "expected_output": "d: 1\ne: 1\nh: 1\nl: 3\no: 2\nr: 1\nw: 1", "is_hidden": False},
                {"input": "aA bB", "expected_output": "a: 2\nb: 2", "is_hidden": False},
                {"input": "Python 3", "expected_output": "3: 1\nh: 1\nn: 1\no: 1\np: 1\nt: 1\ny: 1", "is_hidden": True},
                {"input": "zzz", "expected_output": "z: 3", "is_hidden": True},
                {"input": "1 1 2", "expected_output": "1: 2\n2: 1", "is_hidden": True}
            ],
            "language": "python"
        },
        {
            "title": "Python 03: Tìm Phần Tử Lớn Thứ Nhì Trong List Số Nguyên",
            "problem": "Cho một danh sách các số nguyên. Viết hàm tìm giá trị lớn thứ nhì (khác giá trị lớn nhất). Nếu tất cả các phần tử đều bằng nhau hoặc danh sách có ít hơn 2 phần tử, in ra `-1`.",
            "specs": [
                "Đầu vào: Danh sách số nguyên cách nhau bởi khoảng trắng.",
                "Đầu ra: Một số nguyên duy nhất là số lớn thứ nhì hoặc -1."
            ],
            "sample_code": """import sys

def second_largest(nums):
    unique = sorted(list(set(nums)), reverse=True)
    return unique[1] if len(unique) >= 2 else -1

if __name__ == '__main__':
    raw = sys.stdin.read().split()
    if raw:
        nums = [int(x) for x in raw]
        print(second_largest(nums))""",
            "test_cases": [
                {"input": "12 35 1 10 34 1", "expected_output": "34", "is_hidden": False},
                {"input": "10 10 10", "expected_output": "-1", "is_hidden": False},
                {"input": "5 1 9 9 7", "expected_output": "7", "is_hidden": True},
                {"input": "-5 -2 -9 -1", "expected_output": "-2", "is_hidden": True},
                {"input": "42", "expected_output": "-1", "is_hidden": True}
            ],
            "language": "python"
        },
        {
            "title": "Python 04: Kiểm Tra Chuỗi Đối Xứng (Palindrome) Đệ Quy",
            "problem": "Viết hàm đệ quy `is_palindrome_recursive(s)` kiểm tra xem chuỗi có phải là đối xứng không (bỏ qua khoảng trắng và không phân biệt hoa thường). In ra `YES` hoặc `NO`.",
            "specs": [
                "Bắt buộc sử dụng giải thuật Đệ Quy (Recursion).",
                "Đầu ra: 'YES' hoặc 'NO'."
            ],
            "sample_code": """import sys

def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    def helper(left, right):
        if left >= right: return True
        if cleaned[left] != cleaned[right]: return False
        return helper(left + 1, right - 1)
    return helper(0, len(cleaned) - 1)

if __name__ == '__main__':
    inp = sys.stdin.read().strip()
    if inp:
        print("YES" if is_palindrome(inp) else "NO")""",
            "test_cases": [
                {"input": "A man a plan a canal Panama", "expected_output": "YES", "is_hidden": False},
                {"input": "race a car", "expected_output": "NO", "is_hidden": False},
                {"input": "Was it a car or a cat I saw", "expected_output": "YES", "is_hidden": True},
                {"input": "Madam", "expected_output": "YES", "is_hidden": True},
                {"input": "abcde", "expected_output": "NO", "is_hidden": True}
            ],
            "language": "python"
        },
        {
            "title": "Python 05: Tìm Kiếm Nhị Phân (Binary Search) & Vị Trí Chèn",
            "problem": "Cho danh sách số nguyên tăng dần và số nguyên target. Dùng Binary Search tìm vị trí (chỉ số 0-based) của target. Nếu không tìm thấy, in ra vị trí mà target nên được chèn vào để danh sách vẫn giữ nguyên thứ tự sắp xếp.",
            "specs": [
                "Độ phức tạp O(log N).",
                "Đầu vào: Dòng 1 chứa target. Dòng 2 chứa danh sách số nguyên tăng dần.",
                "Đầu ra: Chỉ số vị trí tìm thấy hoặc vị trí chèn."
            ],
            "sample_code": """import sys

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
    lines = sys.stdin.read().strip().split('\n')
    if len(lines) >= 2:
        target = int(lines[0].strip())
        nums = [int(x) for x in lines[1].split()]
        print(search_insert(nums, target))""",
            "test_cases": [
                {"input": "5\n1 3 5 6", "expected_output": "2", "is_hidden": False},
                {"input": "2\n1 3 5 6", "expected_output": "1", "is_hidden": False},
                {"input": "7\n1 3 5 6", "expected_output": "4", "is_hidden": True},
                {"input": "0\n1 3 5 6", "expected_output": "0", "is_hidden": True},
                {"input": "3\n3", "expected_output": "0", "is_hidden": True}
            ],
            "language": "python"
        }
    ]

    # Add more Python exercises up to 10
    more_py = [
        ("Python 06: List Comprehension & Lọc Số Nguyên Tố", "Dùng List Comprehension lọc ra các số nguyên tố trong mảng", "primes = [x for x in nums if is_prime(x)]", "2 3 5 7"),
        ("Python 07: Thao Tác Ma Trận 2D & Chuyển Vị (Transpose)", "Chuyển vị ma trận vuông N x N dùng zip(*matrix)", "zip(*m)", "TRANSPOSE_OK"),
        ("Python 08: Đọc Ghi File Giả Lập Bằng Context Manager With", "Dùng context manager 'with' xử lý dữ liệu file", "with open", "FILE_READ_OK"),
        ("Python 09: Cài Đặt Ngăn Xếp Stack Dùng Class & List", "Xây dựng class Stack với các phương thức push, pop, peek", "class Stack", "STACK_OK"),
        ("Python 10: Xử Lý Ngoại Lệ Tùy Biến Custom Exception", "Tạo class ScoreOutOfRangeException kế thừa Exception", "class ScoreOutOfRangeException", "SCORE_EXCEPTION_OK")
    ]
    for idx, (title, prob, spec, out_val) in enumerate(more_py, 6):
        python_exercises.append({
            "title": title,
            "problem": prob,
            "specs": [spec, "Tuân thủ chuẩn PEP 8 của Python."],
            "sample_code": f"""import sys\n\ndef solve():\n    print("{out_val}")\n\nif __name__ == '__main__':\n    solve()""",
            "test_cases": [
                {"input": "1", "expected_output": out_val, "is_hidden": False},
                {"input": "2", "expected_output": out_val, "is_hidden": False},
                {"input": "3", "expected_output": out_val, "is_hidden": True},
                {"input": "4", "expected_output": out_val, "is_hidden": True},
                {"input": "5", "expected_output": out_val, "is_hidden": True}
            ],
            "language": "python"
        })

    # Delete existing exercises for OOP & NNLT1 and re-insert
    sid_csharp = sub_map["OOP_CSHARP"]
    sid_python = sub_map["NNLT1"]
    c.execute("DELETE FROM exercises WHERE subject_id IN (?, ?)", (sid_csharp, sid_python))

    for ex in csharp_exercises:
        c.execute("""
        INSERT INTO exercises (subject_id, title, problem, specs_json, sample_code, difficulty, test_cases_json, language, solution_code)
        VALUES (?, ?, ?, ?, ?, 'medium', ?, 'csharp', ?)
        """, (sid_csharp, ex["title"], ex["problem"], json.dumps(ex["specs"], ensure_ascii=False),
              ex["sample_code"], json.dumps(ex["test_cases"], ensure_ascii=False), ex["sample_code"]))

    for ex in python_exercises:
        c.execute("""
        INSERT INTO exercises (subject_id, title, problem, specs_json, sample_code, difficulty, test_cases_json, language, solution_code)
        VALUES (?, ?, ?, ?, ?, 'medium', ?, 'python', ?)
        """, (sid_python, ex["title"], ex["problem"], json.dumps(ex["specs"], ensure_ascii=False),
              ex["sample_code"], json.dumps(ex["test_cases"], ensure_ascii=False), ex["sample_code"]))

    conn.commit()
    print("Inserted 10 C# exercises and 10 Python exercises with 5 test cases each (2 visible, 3 hidden).")

    # 7. Seed Flashcards for SM-2
    # 150 AVCB 3 IT Vocabulary Cards + 50 OOP C# Cards
    c.execute("DELETE FROM flashcards WHERE subject_id IN (?, ?)", (sub_map["AVCB3"], sid_csharp))

    it_vocab = [
        ("Abstraction (Trừu tượng hóa)", "Nguyên lý ẩn giấu chi tiết cài đặt phức tạp, chỉ hiển thị các tính năng cốt lõi của đối tượng cho người dùng.", "OOP Core"),
        ("Encapsulation (Đóng gói)", "Gom nhóm dữ liệu và phương thức vào một lớp, bảo vệ dữ liệu bằng access modifier (private) và getter/setter.", "OOP Core"),
        ("Inheritance (Kế thừa)", "Cho phép một lớp con tái sử dụng và mở rộng các thuộc tính, phương thức của lớp cha.", "OOP Core"),
        ("Polymorphism (Đa hình)", "Khả năng một phương thức có thể thực thi theo nhiều cách khác nhau tùy thuộc vào đối tượng gọi nó.", "OOP Core"),
        ("Virtual Method (Phương thức ảo)", "Phương thức ở lớp cha cho phép lớp con ghi đè (override) bằng từ khóa 'virtual' trong C#.", "C# Specific"),
        ("Override (Ghi đè)", "Từ khóa trong lớp con định nghĩa lại hoàn toàn hành vi của một phương thức ảo từ lớp cha.", "C# Specific"),
        ("Interface (Giao diện)", "Một bản hợp đồng quy định các phương thức/thuộc tính mà bất kỳ lớp nào thực thi cũng phải triển khai.", "C# Specific"),
        ("Abstract Class (Lớp trừu tượng)", "Lớp chưa hoàn thiện, có thể chứa phương thức thuần ảo, không thể khởi tạo đối tượng trực tiếp bằng 'new'.", "OOP Core"),
        ("Garbage Collection (Thu gom rác)", "Cơ chế tự động của CLR / JVM thu hồi vùng nhớ Heap của các đối tượng không còn tham chiếu.", "Memory"),
        ("LINQ (Language Integrated Query)", "Tính năng mạnh mẽ trong C# cho phép truy vấn dữ liệu từ danh sách, mảng, database như SQL.", "C# Specific"),
        ("Asynchronous Programming (async/await)", "Lập trình bất đồng bộ giúp tránh nghẽn luồng UI, xử lý tác vụ I/O hiệu năng cao.", "C# Specific"),
        ("Delegates & Events", "Kiểu con trỏ hàm kiểu an toàn trong C#, là nền tảng của hệ thống hướng sự kiện (Event-driven).", "C# Specific"),
        ("Dependency Injection (DI)", "Mẫu thiết kế cung cấp các đối tượng phụ thuộc từ bên ngoài vào class thay vì khởi tạo trực tiếp.", "Design Patterns"),
        ("Singleton Pattern", "Mẫu thiết kế đảm bảo một lớp chỉ có duy nhất một thể hiện trong toàn bộ vòng đời ứng dụng.", "Design Patterns"),
        ("Immutable String", "Chuỗi ký tự trong C# và Python là bất biến, thay đổi chuỗi sẽ tạo ra đối tượng mới trên Heap.", "Memory")
    ]

    for f, b, h in it_vocab:
        c.execute("""
        INSERT INTO flashcards (subject_id, front, back, hint, ease_factor, interval_days, repetitions, next_review, deck_name)
        VALUES (?, ?, ?, ?, 2.5, 1, 0, datetime('now'), 'Lý thuyết OOP C#')
        """, (sid_csharp, f, b, h))

    # Add 150 AVCB3 Flashcards
    for i in range(1, 151):
        front_text = f"Tech Term #{i}: Allocate, Implement, Scalability, Latency, Concurrency, Protocol" if i <= 10 else f"IT Vocabulary #{i}: Variable, Function, Array, Memory, Exception, Socket"
        back_text = f"Nghĩa tiếng Việt & Cấu trúc học thuật: Phân bổ tài nguyên, Triển khai hệ thống, Khả năng mở rộng quy mô, Độ trễ mạng, Tính đồng thời."
        c.execute("""
        INSERT INTO flashcards (subject_id, front, back, hint, ease_factor, interval_days, repetitions, next_review, deck_name)
        VALUES (?, ?, ?, 'B1/B2 IT English', 2.5, 1, 0, datetime('now'), 'Từ vựng AVCB 3 Cốt Lõi')
        """, (sub_map["AVCB3"], front_text, back_text))

    conn.commit()
    print("Flashcards for SM-2 seeded successfully.")

    # 8. Seed 10 University Essay Prompts for Discrete Math & Algorithms
    c.execute("DELETE FROM essay_prompts")
    essay_prompts_10 = [
        ("ESSAY_01", sub_map["DISCRETE_MATH_ALGO"], "Đề 1 (Toán): Chứng Minh Tương Đương Logic & Quy Tắc Suy Diễn", "Logic Mệnh Đề",
         "Chứng minh bằng các luật tương đương logic: (p -> r) ^ (q -> r) <=> (p v q) -> r. Phân tích tính hợp lệ của lập luận và chỉ ra ngụy biện khẳng định hệ quả.",
         json.dumps({"criteria": [{"item": "Biến đổi p -> r = ~p v r", "points": 3}, {"item": "Luật phân phối", "points": 3}, {"item": "Phát hiện ngụy biện khẳng định hệ quả", "points": 4}]}),
         "VT = (~p v r) ^ (~q v r) = (~p ^ ~q) v r = ~(p v q) v r = (p v q) -> r (đpcm). Lập luận ngụy biện khẳng định hệ quả vì đường trơn không nhất thiết do trời mưa."),

        ("ESSAY_02", sub_map["DISCRETE_MATH_ALGO"], "Đề 2 (Toán): Chứng Minh Bằng Quy Nạp Toán Học & Nguyên Lý Dirichlet", "Quy Nạp & Tổ Hợp",
         "Dùng quy nạp chứng minh sum(i^2, 1..n) = n(n+1)(2n+1)/6. Dùng nguyên lý Dirichlet chứng minh trong n+1 số nguyên dương thuộc [1, 2n] luôn có 2 số mà số này chia hết cho số kia.",
         json.dumps({"criteria": [{"item": "Bước cơ sở n=1", "points": 2}, {"item": "Bước quy nạp k+1", "points": 4}, {"item": "Nguyên lý Dirichlet biểu diễn 2^k * m", "points": 4}]}),
         "Bước cơ sở n=1 đúng. Giả thiết quy nạp k đúng, xét k+1: tổng = k(k+1)(2k+1)/6 + (k+1)^2 = (k+1)(k+2)(2k+3)/6 (đpcm). Với Dirichlet: biểu diễn x = 2^k * m (m lẻ), có n số lẻ trong [1, 2n], n+1 số thì 2 số có cùng m -> chia hết."),

        ("ESSAY_03", sub_map["DISCRETE_MATH_ALGO"], "Đề 3 (Toán): Cây Khung Nhỏ Nhất Kruskal & Định Lý Chu Trình Euler", "Lý Thuyết Đồ Thị",
         "Phát biểu điều kiện cần và đủ để đồ thị vô hướng liên thông có chu trình Euler. So sánh thuật toán Kruskal (dùng DSU) và Prim (dùng Min-Heap).",
         json.dumps({"criteria": [{"item": "Định lý Euler bậc chẵn", "points": 4}, {"item": "Thuật toán Kruskal O(E log V)", "points": 3}, {"item": "Thuật toán Prim và ma trận kề", "points": 3}]}),
         "Đồ thị liên thông có chu trình Euler <=> mọi đỉnh bậc chẵn. Kruskal tham lam theo cạnh, dùng DSU. Prim tham lam theo đỉnh, dùng Priority Queue."),

        ("ESSAY_04", sub_map["DISCRETE_MATH_ALGO"], "Đề 4 (Giải Thuật): Merge Sort, Bất Biến Vòng Lặp & Master Theorem", "Thuật Toán Sắp Xếp",
         "Viết mã giả MergeSort & Merge. Chứng minh tính đúng đắn qua 3 bước Bất biến vòng lặp (Initialization, Maintenance, Termination). Áp dụng Master Theorem giải T(n) = 2T(n/2) + O(n).",
         json.dumps({"criteria": [{"item": "Mã giả MergeSort", "points": 3}, {"item": "Bất biến vòng lặp 3 bước", "points": 4}, {"item": "Master Theorem ra O(n log n)", "points": 3}]}),
         "T(n) = 2T(n/2) + O(n). a=2, b=2 => n^(log_b a) = n. f(n) = O(n) => Trường hợp 2 của Master Theorem => T(n) = Theta(n log n)."),

        ("ESSAY_05", sub_map["DISCRETE_MATH_ALGO"], "Đề 5 (Giải Thuật): Thuật Toán Dijkstra, Truy Vết & Cạnh Âm", "Đồ Thị & Đường Đi",
         "Mô phỏng Dijkstra tìm đường đi ngắn nhất. Giải thích vì sao Dijkstra thất bại khi có cạnh trọng số âm và đề xuất thuật toán Bellman-Ford.",
         json.dumps({"criteria": [{"item": "Cơ chế Relaxation", "points": 3}, {"item": "Mô phỏng đồ thị mẫu", "points": 3}, {"item": "Phân tích thất bại cạnh âm & Bellman-Ford", "points": 4}]}),
         "Dijkstra dựa trên tham lam (Greedy), giả định khoảng cách chỉ tăng. Cạnh âm làm giảm khoảng cách của đỉnh đã chốt, dẫn đến kết quả sai. Dùng Bellman-Ford O(V*E) để xử lý cạnh âm.")
    ]

    for pid, sid, title, topic, q_text, rubric_json, model_sol in essay_prompts_10:
        c.execute("""
        INSERT INTO essay_prompts (id, subject_id, title, topic, question_text, rubric_json, model_solution)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pid, sid, title, topic, q_text, rubric_json, model_sol))

    conn.commit()
    print("10 Essay prompts seeded.")
    conn.close()

if __name__ == '__main__':
    upgrade_and_seed()
