"""
Import 100 OOP C# questions, 10 OOP Exercises, plus True/False, Short Answer, and Essay questions into UniMaster AI
"""
import json
import re
from database import init_db, add_subject, add_question, add_exercise, add_flashcard, get_all_subjects, get_connection

# Dữ liệu 100 câu trắc nghiệm khách quan OOP C# từ file người dùng
compressedBank = [
  [
    "Câu 1 (Lý thuyết - Khái niệm OOP): Trong lập trình hướng đối tượng, tính chất nào cho phép che giấu thông tin cài đặt bên trong và chỉ cung cấp các phương thức/thuộc tính công khai để truy cập?",
    1,
    "Inheritance (Kế thừa)",
    "Encapsulation (Đóng gói)",
    "Polymorphism (Đa hình)",
    "Abstraction (Trừu tượng)",
    "Tính đóng gói (Encapsulation) giấu dữ liệu bằng access modifier private và cung cấp giao diện truy cập công khai qua public methods/properties."
  ],
  [
    "Câu 2 (Đọc hiểu mã - Khai báo Lớp & Properties): Cho đoạn mã lệnh C# sau:\n```csharp\nclass SanPham\n{\n    private double gia;\n    public double Gia\n    {\n        get { return gia; }\n        set { gia = value > 0 ? value : 0; }\n    }\n}\n// Trong hàm Main:\nSanPham sp = new SanPham { Gia = -150 };\nConsole.WriteLine(sp.Gia);\n```",
    1,
    "-150",
    "0",
    "Lỗi biên dịch",
    "Ngoại lệ ArgumentOutOfRangeException khi chạy",
    "Khối set kiểm tra value > 0. Do -150 < 0 nên gia nhận giá trị 0. Console in ra 0."
  ],
  [
    "Câu 3 (Lý thuyết - Khởi tạo đối tượng): Khi tạo một đối tượng mới bằng từ khóa `new` trong C#, vùng nhớ của đối tượng đó được cấp phát ở đâu trong hệ thống?",
    1,
    "Vùng nhớ Stack",
    "Vùng nhớ Heap",
    "Vùng nhớ ROM",
    "Vùng nhớ Register",
    "Trong C#, các kiểu tham chiếu (Reference Types) như Lớp (Class) được cấp phát vùng nhớ trên Heap."
  ],
  [
    "Câu 4 (Đọc hiểu mã - Khai báo & Khởi tạo đối tượng): Cho đoạn mã C# sau:\n```csharp\nclass SinhVien\n{\n    public string Ten { get; set; }\n    public int Tuoi { get; set; } = 18;\n}\n// Trong hàm Main:\nSinhVien sv = new SinhVien();\nConsole.WriteLine($\"{sv.Ten}_{sv.Tuoi}\");\n```",
    0,
    "_18",
    "null_18",
    "_0",
    "Lỗi biên dịch do chưa gán Ten",
    "Ten thuộc kiểu string nhận giá trị mặc định là null (in ra chuỗi rỗng), Tuoi gán mặc định 18. Ký tự xuất ra là '_18'."
  ],
  [
    "Câu 5 (Lý thuyết - Access Modifiers): Thành viên của một lớp được khai báo với từ khóa `protected` có thể được truy cập ở những đâu?",
    0,
    "Trong chính lớp đó và các lớp kế thừa từ nó",
    "Từ bất kỳ đâu trong toàn bộ solution",
    "Chỉ duy nhất trong chính lớp đó",
    "Chỉ trong các lớp nằm cùng tập tin nguồn",
    "Từ khóa protected giới hạn phạm vi truy cập bên trong nội bộ lớp khai báo và các lớp dẫn xuất (kế thừa) từ nó."
  ],
  [
    "Câu 6 (Đọc hiểu mã - Property validation): Cho đoạn mã C# sau:\n```csharp\nclass TaiKhoan\n{\n    private double soDu;\n    public double SoDu\n    {\n        get => soDu;\n        set => soDu = (value >= 100) ? value : 100;\n    }\n}\n// Trong hàm Main:\nTaiKhoan tk = new TaiKhoan();\ntk.SoDu = 50;\nConsole.WriteLine(tk.SoDu);\n```",
    1,
    "50",
    "100",
    "0",
    "Lỗi biên dịch",
    "Giá trị gán là 50 (< 100) nên biểu thức điều kiện trả về 100. Thuộc tính SoDu nhận giá trị 100."
  ],
  [
    "Câu 7 (Lý thuyết - Khái niệm Class vs Object): Mối quan hệ giữa Lớp (Class) và Đối tượng (Object) trong lập trình OOP được phát biểu đúng nhất là:",
    1,
    "Lớp là một thể hiện cụ thể chạy trong bộ nhớ của Đối tượng",
    "Lớp là khuôn mẫu (blueprint) định nghĩa thuộc tính và hành vi, còn Đối tượng là một thể hiện cụ thể (instance) của Lớp",
    "Lớp và Đối tượng là hai thuật ngữ hoàn toàn đồng nghĩa",
    "Một Lớp chỉ có thể tạo ra duy nhất một Đối tượng",
    "Lớp đóng vai trò như bản thiết kế khuôn mẫu, còn đối tượng là thực thể cụ thể được sinh ra từ khuôn mẫu đó."
  ],
  [
    "Câu 8 (Đọc hiểu mã - Auto-implemented Property): Cho đoạn mã C# sau:\n```csharp\nclass NhanVien\n{\n    public string MaNV { get; private set; }\n    public NhanVien(string ma) { MaNV = ma; }\n}\n// Trong hàm Main:\nNhanVien nv = new NhanVien(\"NV01\");\n//nv.MaNV = \"NV02\";\nConsole.WriteLine(nv.MaNV);\n```",
    0,
    "NV01",
    "NV02",
    "Lỗi biên dịch ở câu lệnh in",
    "Lỗi Runtime",
    "MaNV có set là private nên được gán hợp lệ qua Constructor ('NV01'). Dòng gán ngoài bị comment nên Console in ra 'NV01'."
  ],
  [
    "Câu 9 (Lý thuyết - Encapsulation): Tại sao các trường dữ liệu (fields) trong một lớp nên được khai báo là `private` thay vì `public`?",
    1,
    "Để chương trình chạy nhanh hơn",
    "Để ngăn chặn việc thay đổi dữ liệu tùy tiện từ bên ngoài và bảo vệ tính hợp lệ của đối tượng",
    "Để cho phép lớp khác kế thừa dữ liệu đó",
    "Vì C# bắt buộc mọi field phải là private",
    "Khai báo private bảo vệ dữ liệu nội bộ (Encapsulation), tránh việc mã bên ngoài can thiệp làm hỏng trạng thái đối tượng."
  ],
  [
    "Câu 10 (Đọc hiểu mã - Khởi tạo đối tượng): Cho đoạn mã C# sau:\n```csharp\nclass HinhTron\n{\n    public double BanKinh { get; set; } = 1.0;\n    public double TinhDienTich() => Math.PI * BanKinh * BanKinh;\n}\n// Trong hàm Main:\nHinhTron ht = new HinhTron { BanKinh = 2.0 };\nConsole.WriteLine(ht.TinhDienTich() > 12 ? \"Lon\" : \"Nho\");\n```",
    0,
    "Lon",
    "Nho",
    "12.56",
    "Lỗi biên dịch",
    "Dien tich = PI * 2 * 2 ≈ 12.566. Do 12.566 > 12 là Đúng, màn hình in ra 'Lon'."
  ],
  [
    "Câu 12 (Đọc hiểu mã - Object Initializer Syntax): Cho đoạn mã C# sau:\n```csharp\nclass Sach\n{\n    public string TieuDe { get; set; }\n    public double Gia { get; set; }\n}\n// Trong hàm Main:\nSach s = new Sach { TieuDe = \"C# OOP\", Gia = 50000 };\nConsole.WriteLine($\"{s.TieuDe}: {s.Gia}\");\n```",
    0,
    "C# OOP: 50000",
    "C#: 50000",
    "Lỗi biên dịch do thiếu Constructor",
    "null: 0",
    "Cú pháp Object Initializer gán giá trị trực tiếp cho các thuộc tính TieuDe và Gia. Kết quả in ra 'C# OOP: 50000'."
  ],
  [
    "Câu 14 (Đọc hiểu mã - Default Values): Cho đoạn mã C# sau:\n```csharp\nclass KhachHang\n{\n    public string Ten;\n    public bool LaVIP;\n    public int DiemTichLuy;\n}\n// Trong hàm Main:\nKhachHang kh = new KhachHang();\nConsole.WriteLine($\"{kh.Ten == null}_{kh.LaVIP}_{kh.DiemTichLuy}\");\n```",
    0,
    "True_False_0",
    "False_True_0",
    "True_True_1",
    "Lỗi biên dịch",
    "Giá trị mặc định các trường: string (null -> kh.Ten == null là True), bool (False), int (0). Kết quả 'True_False_0'."
  ],
  [
    "Câu 16 (Đọc hiểu mã - Property Chaining): Cho đoạn mã C# sau:\n```csharp\nclass LopHoc\n{\n    private int siSo = 30;\n    public int SiSo\n    {\n        get => siSo;\n        set => siSo = value > 0 ? value : siSo;\n    }\n}\n// Trong hàm Main:\nLopHoc lh = new LopHoc();\nlh.SiSo = -5;\nConsole.WriteLine(lh.SiSo);\n```",
    1,
    "-5",
    "30",
    "0",
    "Lỗi biên dịch",
    "Gán -5 (< 0) nên siSo giữ nguyên giá trị ban đầu là 30. Console in ra 30."
  ],
  [
    "Câu 17 (Lý thuyết - Partial Class): Từ khóa `partial` áp dụng trước khai báo `class` trong C# nhằm mục đích gì?",
    0,
    "Cho phép chia định nghĩa của một lớp thành nhiều tệp mã nguồn (.cs) khác nhau",
    "Ngăn không cho lớp bị kế thừa",
    "Biến lớp đó thành lớp trừu tượng",
    "Cho phép tạo đối tượng mà không cần dùng new",
    "Partial class cho phép người lập trình tách nội dung của cùng một lớp ra nhiều file .cs riêng biệt."
  ],
  [
    "Câu 18 (Đọc hiểu mã - Method Invocations): Cho đoạn mã C# sau:\n```csharp\nclass MayTinh\n{\n    public int Cong(int a, int b) => a + b;\n    public double Cong(double a, double b) => a + b + 0.5;\n}\n// Trong hàm Main:\nMayTinh mt = new MayTinh();\nConsole.WriteLine(mt.Cong(2, 3));\n```",
    0,
    "5",
    "5.5",
    "5.0",
    "Lỗi biên dịch",
    "2 và 3 là hai số nguyên (int), C# ưu tiên gọi hàm Cong(int, int) trả về 2 + 3 = 5."
  ],
  [
    "Câu 19 (Lý thuyết - Constructor Overloading): Thế nào là hiện tượng Nạp chồng phương thức khởi tạo (Constructor Overloading)?",
    0,
    "Một lớp có nhiều Constructor cùng tên nhưng khác nhau về danh sách tham số truyền vào",
    "Constructor của lớp con đè lên Constructor của lớp cha",
    "Khởi tạo một đối tượng nhiều lần trong bộ nhớ",
    "Lớp con gọi Constructor của lớp cha qua base",
    "Constructor Overloading xảy ra khi trong cùng một lớp định nghĩa nhiều Constructor có tên trùng tên lớp nhưng khác tham số."
  ],
  [
    "Câu 20 (Đọc hiểu mã - Private Setter): Cho đoạn mã C# sau:\n```csharp\nclass SanPham\n{\n    public string Ten { get; }\n    public SanPham(string ten) { Ten = ten; }\n}\n// Trong hàm Main:\nSanPham sp = new SanPham(\"Laptop\");\nConsole.WriteLine(sp.Ten);\n```",
    0,
    "Laptop",
    "null",
    "Lỗi biên dịch",
    "Lỗi Runtime",
    "Getter-only auto-property cho phép gán giá trị hợp lệ bên trong Constructor. Màn hình xuất 'Laptop'."
  ],
  [
    "Câu 21 (Lý thuyết - Phương thức & Tham số): Điểm khác biệt căn bản giữa hai từ khóa `ref` và `out` khi truyền tham số cho phương thức trong C# là gì?",
    0,
    "Biến truyền vào ref bắt buộc phải khởi tạo giá trị trước, còn out không bắt buộc nhưng phương thức phải gán giá trị cho nó trước khi thoát",
    "ref truyền theo tham trị, out truyền theo tham chiếu",
    "out chỉ áp dụng cho kiểu tham chiếu",
    "ref không thay đổi giá trị của biến gốc sau khi thoát hàm",
    "ref yêu cầu khởi tạo biến trước khi gọi hàm; out bắt buộc phương thức nhận tham số phải gán giá trị cho biến trước khi return."
  ],
  [
    "Câu 22 (Đọc hiểu mã - Phương thức & Từ khóa ref/out): Cho đoạn mã C# sau:\n```csharp\nclass Program\n{\n    static void ThayDoi(ref int a, out int b)\n    {\n        a += 10;\n        b = a * 2;\n    }\n    static void Main()\n    {\n        int x = 5, y;\n        ThayDoi(ref x, out y);\n        Console.WriteLine($\"x={x}, y={y}\");\n    }\n}\n```",
    1,
    "x=5, y=10",
    "x=15, y=30",
    "x=15, y=10",
    "Lỗi biên dịch",
    "a = 5 + 10 = 15 (x thành 15). b = 15 * 2 = 30 (y thành 30). In ra 'x=15, y=30'."
  ],
  [
    "Câu 23 (Lý thuyết - Nạp chồng phương thức Method Overloading): Yếu tố nào sau đây KHÔNG THỂ dùng để phân biệt các phương thức nạp chồng (Overloading) trong cùng một lớp?",
    2,
    "Số lượng tham số",
    "Kiểu dữ liệu của các tham số",
    "Kiểu trả về của phương thức (Return type)",
    "Thứ tự các kiểu dữ liệu tham số",
    "C# không cho phép nạp chồng hai phương thức chỉ khác nhau mỗi kiểu trả về (Return type)."
  ],
  [
    "Câu 24 (Đọc hiểu mã - Method Overloading Call): Cho đoạn mã C# sau:\n```csharp\nclass InAn\n{\n    public void Xuat(int x) => Console.Write(\"Int \");\n    public void Xuat(double x) => Console.Write(\"Double \");\n}\n// Trong hàm Main:\nInAn ia = new InAn();\nia.Xuat(5);\nia.Xuat(5.0);\n```",
    2,
    "Int Int",
    "Double Double",
    "Int Double",
    "Double Int",
    "5 là int gọi Xuat(int) -> 'Int '. 5.0 là double gọi Xuat(double) -> 'Double '. Kết quả: 'Int Double '."
  ],
  [
    "Câu 25 (Lý thuyết - Optional Parameters): Trong C#, tham số tùy chọn (Optional Parameter) có giá trị mặc định phải được khai báo ở vị trí nào trong danh sách tham số của phương thức?",
    0,
    "Đứng ở cuối danh sách tham số",
    "Đứng ở đầu danh sách tham số",
    "Ở bất kỳ vị trí nào tùy ý",
    "Bắt buộc phải đứng giữa các tham số ref",
    "Các tham số tùy chọn có gán giá trị mặc định bắt buộc phải đứng sau tất cả các tham số bắt buộc."
  ],
  [
    "Câu 26 (Đọc hiểu mã - Optional Parameters): Cho đoạn mã C# sau:\n```csharp\nclass Program\n{\n    static int TinhTien(int gia, int soLuong = 1, double giamGia = 0)\n    {\n        return (int)(gia * soLuong * (1 - giamGia));\n    }\n    static void Main()\n    {\n        Console.WriteLine(TinhTien(100, 2));\n    }\n}\n```",
    1,
    "100",
    "200",
    "0",
    "Lỗi biên dịch",
    "gia = 100, soLuong = 2, giamGia nhận giá trị mặc định 0. Kết quả 100 * 2 * 1 = 200."
  ],
  [
    "Câu 27 (Lý thuyết - Named Arguments): Kỹ thuật truyền tham số theo tên (Named Arguments) trong C# giúp mang lại lợi ích gì?",
    0,
    "Cho phép truyền tham số không cần theo đúng thứ tự khai báo trong định nghĩa phương thức",
    "Giúp tăng tốc độ thực thi phương thức",
    "Bắt buộc tham số đó phải là kiểu string",
    "Tự động chuyển đổi kiểu dữ liệu tham số",
    "Named Arguments (VD: Tinh(b: 2, a: 1)) cho phép chỉ định rõ tên tham số nên không bị ràng buộc bởi vị trí."
  ],
  [
    "Câu 28 (Đọc hiểu mã - Named Arguments): Cho đoạn mã C# sau:\n```csharp\nclass Program\n{\n    static void HienThi(int x, string y)\n    {\n        Console.Write($\"{y}:{x}\");\n    }\n    static void Main()\n    {\n        HienThi(y: \"Code\", x: 10);\n    }\n}\n```",
    0,
    "Code:10",
    "10:Code",
    "Lỗi biên dịch",
    "Code:x",
    "Tham số x nhận 10, y nhận 'Code'. Chuỗi định dạng $\"{y}:{x}\" xuất ra 'Code:10'."
  ],
  [
    "Câu 29 (Lý thuyết - Keyword `params`): Từ khóa `params` khai báo trước một mảng trong danh sách tham số của phương thức cho phép điều gì?",
    0,
    "Truyền số lượng tham số biến đổi (hoặc danh sách phân cách bởi dấu phẩy) vào phương thức",
    "Bắt buộc mảng truyền vào phải được khởi tạo sẵn",
    "Giới hạn mảng tối đa 5 phần tử",
    "Biến mảng thành mảng 2 chiều",
    "Từ khóa params cho phép truyền số lượng đối số tùy ý rời rạc hoặc truyền trực tiếp một mảng vào hàm."
  ],
  [
    "Câu 30 (Đọc hiểu mã - Keyword `params`): Cho đoạn mã C# sau:\n```csharp\nclass Program\n{\n    static int Tong(params int[] numbers)\n    {\n        int s = 0;\n        foreach (int n in numbers) s += n;\n        return s;\n    }\n    static void Main()\n    {\n        Console.WriteLine(Tong(1, 2, 3, 4));\n    }\n}\n```",
    0,
    "10",
    "4",
    "Lỗi biên dịch",
    "0",
    "Hàm Tong tính tổng mảng numbers [1, 2, 3, 4]. Kết quả 1 + 2 + 3 + 4 = 10."
  ],
  [
    "Câu 31 (Lý thuyết - Passing Value Types by Reference): Khi truyền một biến kiểu giá trị (Value Type như `int`, `double`) vào phương thức kèm từ khóa `ref`, điều gì xảy ra?",
    0,
    "Phương thức thao tác trực tiếp trên vùng nhớ của biến gốc, thay đổi bên trong hàm sẽ làm thay đổi biến gốc",
    "Phương thức tạo ra một bản sao mới độc lập",
    "Giá trị biến gốc bị xóa về 0",
    "Phương thức không thể sửa giá trị biến",
    "Từ khóa ref biến tham số kiểu giá trị thành tham chiếu đến chính địa chỉ ô nhớ của biến gốc."
  ],
  [
    "Câu 32 (Đọc hiểu mã - Pass by value vs ref): Cho đoạn mã C# sau:\n```csharp\nclass Program\n{\n    static void Tang(int a, ref int b)\n    {\n        a += 5;\n        b += 5;\n    }\n    static void Main()\n    {\n        int x = 10, y = 10;\n        Tang(x, ref y);\n        Console.WriteLine($\"{x}_{y}\");\n    }\n}\n```",
    0,
    "10_15",
    "15_15",
    "10_10",
    "15_10",
    "x truyền tham trị nên giữ nguyên 10. y truyền ref nên tăng thành 15. In ra '10_15'."
  ],
  [
    "Câu 33 (Lý thuyết - Method Expression Body): Cú pháp Expression-bodied member trong C# (ví dụ: `public int Tinh() => x * 2;`) dùng ký hiệu nào để nối định nghĩa hàm?",
    0,
    "=>",
    "->",
    "::",
    "=",
    "Cú pháp Expression-bodied viết ngắn gọn phương thức trả về kết quả bằng toán tử lambda/mũi tên '=>'."
  ],
  [
    "Câu 34 (Đọc hiểu mã - Expression-bodied method): Cho đoạn mã C# sau:\n```csharp\nclass HinhVuong\n{\n    public double Canh { get; set; }\n    public double ChuVi => Canh * 4;\n}\n// Trong hàm Main:\nHinhVuong hv = new HinhVuong { Canh = 3.5 };\nConsole.WriteLine(hv.ChuVi);\n```",
    0,
    "14",
    "12.25",
    "3.5",
    "Lỗi biên dịch",
    "ChuVi là getter-only expression-bodied property = 3.5 * 4 = 14."
  ],
  [
    "Câu 35 (Lý thuyết - Recursion): Đặc điểm cơ bản của một phương thức đệ quy (Recursive Method) là gì?",
    0,
    "Phương thức tự gọi lại chính nó bên trong thân hàm và có điều kiện dừng",
    "Phương thức gọi một phương thức tĩnh khác",
    "Phương thức không có giá trị trả về",
    "Phương thức chỉ chứa vòng lặp for",
    "Phương thức đệ quy gọi lại chính nó và bắt buộc phải có điểm dừng để tránh tràn bộ nhớ Stack."
  ],
  [
    "Câu 36 (Đọc hiểu mã - Recursion): Cho đoạn mã C# đệ quy sau:\n```csharp\nclass Program\n{\n    static int GiaiThua(int n)\n    {\n        if (n <= 1) return 1;\n        return n * GiaiThua(n - 1);\n    }\n    static void Main()\n    {\n        Console.WriteLine(GiaiThua(4));\n    }\n}\n```",
    0,
    "24",
    "12",
    "4",
    "1",
    "GiaiThua(4) = 4 * 3 * 2 * 1 = 24."
  ],
  [
    "Câu 39 (Lý thuyết - Pass Reference Type by Value): Mặc định, khi truyền một đối tượng (Reference Type) vào phương thức không có `ref/out`, điều gì được truyền đi?",
    0,
    "Bản sao của địa chỉ tham chiếu (pointer/reference) đến đối tượng trên Heap",
    "Bản sao toàn bộ dữ liệu của đối tượng",
    "Bản sao địa chỉ biến trên Stack",
    "Đối tượng bị khóa không thể sửa thuộc tính",
    "Đối tượng truyền mặc định là truyền bản sao của địa chỉ tham chiếu, cả 2 cùng trỏ đến 1 vùng nhớ đối tượng trên Heap."
  ],
  [
    "Câu 40 (Đọc hiểu mã - Modifying Object inside Method): Cho đoạn mã C# sau:\n```csharp\nclass SanPham { public double Gia { get; set; } }\nclass Program\n{\n    static void GiamGia(SanPham sp)\n    {\n        sp.Gia -= 10;\n    }\n    static void Main()\n    {\n        SanPham p = new SanPham { Gia = 50 };\n        GiamGia(p);\n        Console.WriteLine(p.Gia);\n    }\n}\n```",
    0,
    "40",
    "50",
    "0",
    "Lỗi biên dịch",
    "Tham số sp cùng tham chiếu tới đối tượng p trên Heap. Sửa sp.Gia làm p.Gia giảm từ 50 xuống 40."
  ],
  [
    "Câu 41 (Lý thuyết - Constructor & Kế thừa): Khi một đối tượng của lớp con được khởi tạo trong C#, thứ tự chạy các phương thức khởi tạo (Constructor) diễn ra như thế nào?",
    0,
    "Constructor của lớp cha chạy trước, sau đó mới đến Constructor của lớp con",
    "Constructor của lớp con chạy trước, sau đó đến Constructor của lớp cha",
    "Chỉ có Constructor của lớp con chạy",
    "Hai Constructor chạy song song",
    "Khi khởi tạo lớp con, C# tự động gọi Constructor của lớp cha trước để đảm bảo phần kế thừa được khởi tạo hoàn chỉnh."
  ],
  [
    "Câu 42 (Đọc hiểu mã - Constructor & Kế thừa): Cho đoạn mã C# sau:\n```csharp\nclass Cha\n{\n    public Cha() { Console.Write(\"A \"); }\n    public Cha(int x) { Console.Write(\"B \"); }\n}\nclass Con : Cha\n{\n    public Con() : base(5) { Console.Write(\"C \"); }\n}\n// Trong hàm Main:\nCon obj = new Con();\n```",
    1,
    "A C",
    "B C",
    "C",
    "A B C",
    "Con() gọi : base(5) làm Cha(int x) chạy trước in 'B ', sau đó thân Con() chạy in 'C '. Kết quả: 'B C'."
  ],
  [
    "Câu 43 (Lý thuyết - Polymorphism `virtual`/`override`): Để cho phép một phương thức của lớp cha có thể được ghi đè (override) ở lớp con, phương thức ở lớp cha phải khai báo từ khóa nào?",
    0,
    "virtual",
    "override",
    "new",
    "abstract",
    "Từ khóa virtual ở lớp cha cho phép và đánh dấu phương thức đó có thể được ghi đè (override) ở lớp con."
  ],
  [
    "Câu 44 (Đọc hiểu mã - Đa hình `virtual`/`override`): Cho đoạn mã C# sau:\n```csharp\nclass DongVat\n{\n    public virtual void Keu() { Console.Write(\"DongVat \"); }\n}\nclass Cho : DongVat\n{\n    public override void Keu() { Console.Write(\"GauGau \"); }\n}\n// Trong hàm Main:\nDongVat dv = new Cho();\ndv.Keu();\n```",
    1,
    "DongVat",
    "GauGau",
    "DongVat GauGau",
    "Lỗi biên dịch",
    "Biến kiểu DongVat nhưng trỏ đến instance Cho. Nhờ override, phương thức Keu() của Cho được gọi -> 'GauGau'."
  ],
  [
    "Câu 45 (Lý thuyết - Che giấu phương thức với `new`): Từ khóa `new` khi dùng trước khai báo một phương thức ở lớp con (Method Hiding) có tác dụng gì?",
    0,
    "Che giấu phương thức trùng tên của lớp cha thay vì ghi đè đa hình",
    "Ghi đè phương thức ảo của lớp cha",
    "Bắt buộc lớp con phải gọi hàm cha qua base",
    "Khởi tạo đối tượng mới",
    "Từ khóa new ngắt liên kết đa hình, định nghĩa một phương thức mới che giấu phương thức trùng tên của lớp cha."
  ],
  [
    "Câu 46 (Đọc hiểu mã - Method Hiding (`new`)): Cho đoạn mã C# sau:\n```csharp\nclass A\n{\n    public void HienThi() { Console.Write(\"A\"); }\n}\nclass B : A\n{\n    public new void HienThi() { Console.Write(\"B\"); }\n}\n// Trong hàm Main:\nA obj = new B();\nobj.HienThi();\n```",
    0,
    "A",
    "B",
    "A B",
    "Lỗi biên dịch",
    "Vì dùng new nên không có cơ chế đa hình. Biến kiểu A gọi A.HienThi() xuất ra 'A'."
  ],
  [
    "Câu 47 (Lý thuyết - Abstract Class & Method): Đặc điểm nào sau đây là ĐÚNG đối với lớp trừu tượng (`abstract class`) trong C#?",
    0,
    "Không thể khởi tạo đối tượng trực tiếp bằng toán tử new",
    "Chỉ được chứa phương thức trừu tượng, không được chứa phương thức có thân hàm",
    "Có thể khởi tạo đối tượng bằng new nếu không có tham số",
    "Lớp con không cần ghi đè các phương thức abstract",
    "Lớp trừu tượng (abstract class) là bản thiết kế dở dang, không thể được khởi tạo trực tiếp qua toán tử new."
  ],
  [
    "Câu 48 (Đọc hiểu mã - Abstract Class Implementation): Cho đoạn mã C# sau:\n```csharp\nabstract class Hinh\n{\n    public abstract double TinhDienTich();\n}\nclass HinhVuong : Hinh\n{\n    public double Canh { get; set; } = 3;\n    public override double TinhDienTich() => Canh * Canh;\n}\n// Trong hàm Main:\nHinh h = new HinhVuong();\nConsole.WriteLine(h.TinhDienTich());\n```",
    0,
    "9",
    "3",
    "Lỗi biên dịch do h là Hinh",
    "0",
    "HinhVuong ghi đè TinhDienTich() = 3 * 3 = 9. Biến cha Hinh gọi phương thức đa hình in ra 9."
  ],
  [
    "Câu 49 (Lý thuyết - Operator Overloading syntax): Quy tắc khai báo nào sau đây là BẮT BUỘC khi định nghĩa phương thức nạp chồng toán tử (Operator Overloading)?",
    0,
    "Phương thức phải được khai báo với từ khóa public static",
    "Phương thức phải được khai báo private",
    "Phải trả về kiểu bool",
    "Không thể nhận tham số truyền vào",
    "Nạp chồng toán tử trong C# bắt buộc khai báo là public static operator <toán_tử>(...)."
  ],
  [
    "Câu 50 (Đọc hiểu mã - Operator Overloading `+`): Cho đoạn mã C# sau:\n```csharp\nclass Diem\n{\n    public int X { get; set; }\n    public int Y { get; set; }\n    public static Diem operator +(Diem d1, Diem d2)\n    {\n        return new Diem { X = d1.X + d2.X, Y = d1.Y + d2.Y };\n    }\n}\n// Trong hàm Main:\nDiem p1 = new Diem { X = 2, Y = 3 };\nDiem p2 = new Diem { X = 4, Y = 1 };\nDiem p3 = p1 + p2;\nConsole.WriteLine($\"{p3.X}_{p3.Y}\");\n```",
    0,
    "6_4",
    "2_3",
    "4_1",
    "Lỗi biên dịch",
    "X = 2 + 4 = 6, Y = 3 + 1 = 4. Kết quả p3.X_p3.Y là '6_4'."
  ]
]

# 10 bài tập lớn OOP C# kèm giải mẫu
oopExercises = [
  {
    "id": 1,
    "title": "BÀI TẬP 1: QUẢN LÝ DỊCH VỤ PHÒNG KHÁCH SẠN (HOTEL MANAGEMENT)",
    "problem": "Một khách sạn quản lý 02 loại phòng lưu trú chính: Phòng Tiêu chuẩn (StandardRoom) và Phòng Cao cấp (VIPRoom). Mỗi loại phòng có đơn giá ngày, phụ dịch vụ ăn uống, chính sách phục vụ đặc biệt và công thức tính tổng chi phí thanh toán hoàn toàn khác nhau.",
    "specs": [
      "A. Lớp cơ sở trừu tượng Phong: Thuộc tính MaPhong (string), TenKhachHang (string), GiaPhongNgay (double >= 0), SoNgayThue (int >= 1). Constructor mặc định & đầy đủ tham số. Phương thức: public abstract double TinhTienPhong(), public virtual void NhapThongTin(), public virtual void InThongTin().",
      "B1. Lớp StandardRoom (Kế thừa Phong): Bổ sung TienDichVuAnUong (double >= 0). TinhTienPhong() = (GiaPhongNgay * SoNgayThue) + TienDichVuAnUong.",
      "B2. Lớp VIPRoom (Kế thừa Phong): Bổ sung PhiPhucVuVIP (double). TinhTienPhong() = (GiaPhongNgay * SoNgayThue) * 0.95 + PhiPhucVuVIP (giảm 5% giá phòng).",
      "C. Hàm Main: Tạo 01 StandardRoom và 01 VIPRoom. Đưa vào List<Phong>, duyệt gọi InThongTin() chứng minh đa hình, tính tổng doanh thu và tìm phòng có chi phí cao nhất."
    ],
    "sampleCode": """using System;
using System.Collections.Generic;

abstract class Phong
{
    public string MaPhong { get; set; }
    public string TenKhachHang { get; set; }
    private double giaPhongNgay;
    public double GiaPhongNgay { get => giaPhongNgay; set => giaPhongNgay = value >= 0 ? value : 0; }
    private int soNgayThue = 1;
    public int SoNgayThue { get => soNgayThue; set => soNgayThue = value >= 1 ? value : 1; }

    public Phong() { }
    public Phong(string ma, string ten, double gia, int soNgay)
    {
        MaPhong = ma; TenKhachHang = ten; GiaPhongNgay = gia; SoNgayThue = soNgay;
    }

    public abstract double TinhTienPhong();
    public virtual void InThongTin()
    {
        Console.WriteLine($"[Phòng {MaPhong}] Khách: {TenKhachHang} | Giá/ngày: {GiaPhongNgay:N0} | Ngày: {SoNgayThue} | Tổng tiền: {TinhTienPhong():N0} VND");
    }
}

class StandardRoom : Phong
{
    public double TienDichVuAnUong { get; set; }
    public StandardRoom(string ma, string ten, double gia, int soNgay, double tienAn)
        : base(ma, ten, gia, soNgay) { TienDichVuAnUong = tienAn >= 0 ? tienAn : 0; }

    public override double TinhTienPhong() => (GiaPhongNgay * SoNgayThue) + TienDichVuAnUong;
}

class VIPRoom : Phong
{
    public double PhiPhucVuVIP { get; set; }
    public VIPRoom(string ma, string ten, double gia, int soNgay, double phiVip)
        : base(ma, ten, gia, soNgay) { PhiPhucVuVIP = phiVip; }

    public override double TinhTienPhong() => (GiaPhongNgay * SoNgayThue) * 0.95 + PhiPhucVuVIP;
}"""
  },
  {
    "id": 2,
    "title": "BÀI TẬP 2: QUẢN LÝ PHƯƠNG TIỆN GIAO THÔNG VÀ PHÍ ĐĂNG KIỂM (VEHICLE MANAGEMENT)",
    "problem": "Trung tâm đăng kiểm xe cơ giới quản lý 02 loại phương tiện phổ biến: Xe ô tô con (Car) và Xe tải vận tải (Truck).",
    "specs": [
      "A. Lớp cơ sở trừu tượng PhuongTien: BiSoXe, HangSanXuat, NamSanXuat, GiaTriXe. Phương thức: TinhPhiDangKiem().",
      "B1. Lớp Car: Bổ sung SoChoNgoi. TinhPhiDangKiem() = 340,000 + (SoChoNgoi > 5 ? 100,000 : 50,000) VND.",
      "B2. Lớp Truck: Bổ sung TaiTrongTan. TinhPhiDangKiem() = 500,000 + (TaiTrongTan * 80,000) VND."
    ],
    "sampleCode": """abstract class PhuongTien
{
    public string BiSoXe { get; set; }
    public string HangSanXuat { get; set; }
    public abstract double TinhPhiDangKiem();
}

class Car : PhuongTien
{
    public int SoChoNgoi { get; set; }
    public override double TinhPhiDangKiem() => 340000 + (SoChoNgoi > 5 ? 100000 : 50000);
}

class Truck : PhuongTien
{
    public double TaiTrongTan { get; set; }
    public override double TinhPhiDangKiem() => 500000 + (TaiTrongTan * 80000);
}"""
  }
]

def seed_rich_data():
    init_db()
    
    # 1. Thêm hoặc lấy môn Lập trình OOP C#
    oop_sid = add_subject(
        code="OOP_CSHARP",
        name="Lập trình Hướng đối tượng C# (.NET)",
        icon="💻",
        category="Công nghệ thông tin",
        description="Kho bài tập và 100 câu hỏi trắc nghiệm khách quan chuẩn cấu trúc đề thi OOP C# (.NET)."
    )

    print(f"Adding OOP C# questions to subject id {oop_sid}...")
    
    # Nạp 100 câu trắc nghiệm
    for item in compressedBank:
        raw_text = item[0]
        correct_idx = item[1]
        opt_a = item[2]
        opt_b = item[3]
        opt_c = item[4] if len(item) > 4 else ""
        opt_d = item[5] if len(item) > 5 else ""
        expl = item[6] if len(item) > 6 else ""
        
        # Tách code snippet nếu có
        code_part = ""
        q_text = raw_text
        match = re.search(r'```csharp\n([\s\S]*?)```', raw_text)
        if match:
            code_part = match.group(1).strip()
            q_text = raw_text.replace(match.group(0), '').strip()
            
        correct_letter = ["A", "B", "C", "D"][correct_idx]
        
        add_question(
            subject_id=oop_sid,
            question_text=q_text,
            option_a=opt_a,
            option_b=opt_b,
            option_c=opt_c,
            option_d=opt_d,
            correct_option=correct_letter,
            explanation=expl,
            difficulty='medium',
            q_type='mcq',
            code_snippet=code_part
        )

    # Nạp các câu hỏi ĐÚNG / SAI (True/False)
    tf_questions = [
      ("Trong C#, một lớp con có thể kế thừa từ nhiều lớp cha cùng một lúc (Đa kế thừa lớp).", "False", "C# chỉ hỗ trợ đơn kế thừa lớp (Single Inheritance), nhưng hỗ trợ đa thực thi interface.", oop_sid),
      ("Interface trong C# có thể chứa các trường dữ liệu thực thể (instance fields).", "False", "Interface không thể chứa biến thực thể (instance fields) mà chỉ chứa định nghĩa phương thức, thuộc tính, sự kiện.", oop_sid),
      ("Từ khóa `sealed` khi khai báo trước một class sẽ ngăn không cho bất kỳ class nào khác kế thừa từ nó.", "True", "Lớp sealed (bị phong ấn) không thể bị kế thừa.", oop_sid),
      ("Toán tử `is` trong C# trả về giá trị kiểu bool để kiểm tra tính tương thích kiểu dữ liệu lúc runtime.", "True", "Toán tử `is` trả về true nếu đối tượng tương thích với kiểu dữ liệu kiểm tra.", oop_sid)
    ]
    for q_t, ans, exp, s_id in tf_questions:
        add_question(
            subject_id=s_id,
            question_text=q_t,
            option_a="Đúng (True)",
            option_b="Sai (False)",
            correct_option="A" if ans == "True" else "B",
            explanation=exp,
            q_type='true_false'
        )

    # Nạp các câu hỏi TRẢ LỜI NGẮN (Short answer / Predict Output)
    sa_questions = [
      ("Cho đoạn mã C# sau, màn hình console sẽ in ra kết quả gì?\n```csharp\nint x = 5;\nvoid Tang(ref int a) { a += 10; }\nTang(ref x);\nConsole.WriteLine(x);\n```", "15", "x được truyền bằng từ khóa `ref` nên giá trị trong ô nhớ bị thay đổi từ 5 thành 15.", oop_sid),
      ("Cho đoạn mã C# sau, kết quả in ra là gì?\n```csharp\nint a = 4, b = 2;\nConsole.WriteLine(a / b * 3);\n```", "6", "Thứ tự thực hiện từ trái sang phải: 4 / 2 = 2; 2 * 3 = 6.", oop_sid)
    ]
    for q_t, ans, exp, s_id in sa_questions:
        add_question(
            subject_id=s_id,
            question_text=q_t,
            correct_option=ans,
            explanation=exp,
            q_type='short_answer'
        )

    # Nạp 10 bài tập lớn OOP C# vào bảng exercises
    for ex in oopExercises:
        add_exercise(
            subject_id=oop_sid,
            title=ex["title"],
            problem=ex["problem"],
            specs=ex["specs"],
            sample_code=ex["sampleCode"]
        )

    print("All rich questions and exercises imported successfully!")

if __name__ == "__main__":
    seed_rich_data()
