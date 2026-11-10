"""
100 High-Quality Multiple Choice Questions for Object-Oriented Programming (OOP)
Targeting exams on Nov 15 & Nov 26 (C++, Java, C#)
"""

def get_oop_100_questions():
    questions = []
    
    # 1. 4 Tính chất OOP (1 - 25)
    oop_core = [
        ("Trong lập trình hướng đối tượng, tính chất nào cho phép che giấu thông tin nội bộ của đối tượng và chỉ cung cấp các phương thức truy cập hợp lệ ra bên ngoài?",
         "", "Tính kế thừa (Inheritance)", "Tính đa hình (Polymorphism)", "Tính đóng gói (Encapsulation)", "Tính trừu tượng (Abstraction)",
         "C", "Tính đóng gói (Encapsulation) gom nhóm dữ liệu và các hành vi thao tác trên dữ liệu đó vào trong một lớp, đồng thời che giấu các trường dữ liệu bằng từ khóa private/protected và chỉ cung cấp các phương thức public (getter/setter) để kiểm soát quyền truy cập.", "easy", "Encapsulation"),
         
        ("Phát biểu nào sau đây đúng nhất về 'Tính trừu tượng' (Abstraction) trong OOP?",
         "", "Là khả năng tạo ra nhiều lớp con từ một lớp cha", "Là việc tập trung vào các đặc tính cốt lõi và hành vi bản chất của đối tượng, bỏ qua các chi tiết cài đặt vụn vặt", "Là việc ẩn giấu mã nguồn không cho người dùng xem", "Là việc định nghĩa nhiều hàm cùng tên khác tham số",
         "B", "Tính trừu tượng (Abstraction) giúp đơn giản hóa hệ thống phức tạp bằng cách tập trung vào 'Đối tượng làm được gì' (interface/abstract) thay vì 'Nó làm như thế nào' (implementation details).", "easy", "Abstraction"),

        ("Đặc điểm nào thể hiện tính 'Đa hình tại thời điểm chạy' (Runtime Polymorphism / Dynamic Binding)?",
         "", "Nạp chồng phương thức (Method Overloading)", "Nạp chồng toán tử (Operator Overloading)", "Ghi đè phương thức (Method Overriding) thông qua hàm ảo (virtual method)", "Khai báo biến cùng tên trong các phạm vi khác nhau",
         "C", "Runtime Polymorphism được kích hoạt thông qua cơ chế ghi đè phương thức (Overriding) kết hợp từ khóa virtual và con trỏ/tham chiếu lớp cha trỏ tới đối tượng lớp con. Trình biên dịch sử dụng bảng ảo (vtable) tại thời điểm thực thi để gọi đúng phương thức của đối tượng thực tế.", "medium", "Polymorphism"),

        ("Khi lớp B kế thừa công khai (public inheritance) từ lớp A, thành viên mang phạm vi truy cập 'protected' của lớp A sẽ trở thành thành viên nào trong lớp B?",
         "", "private", "protected", "public", "Không thể truy cập từ lớp B",
         "B", "Với public inheritance: public của cha giữ nguyên là public của con, protected của cha giữ nguyên là protected của con, private của cha được kế thừa nhưng bị ẩn và không thể truy cập trực tiếp.", "medium", "Inheritance"),

        ("Trong C++, nếu không chỉ định rõ kiểu kế thừa (ví dụ `class B : A {}`), kiểu kế thừa mặc định là gì?",
         "", "public", "protected", "private", "friend",
         "C", "Trong C++, kiểu kế thừa mặc định của 'class' là private, trong khi kiểu kế thừa mặc định của 'struct' là public.", "medium", "Inheritance"),

        ("Lợi ích quan trọng nhất của tính Kế thừa (Inheritance) trong phát triển phần mềm là gì?",
         "", "Tăng tốc độ thực thi chương trình", "Tái sử dụng mã nguồn (Code Reusability) và thiết lập mối quan hệ phân cấp 'IS-A'", "Tiết kiệm bộ nhớ RAM", "Tự động quản lý giải phóng con trỏ",
         "B", "Kế thừa cho phép lớp con tái sử dụng các thuộc tính và phương thức từ lớp cha, đồng thời mở rộng thêm các tính năng chuyên biệt, thiết lập quan hệ IS-A bền vững trong mô hình hóa.", "easy", "Inheritance"),

        ("Trong C#, từ khóa nào được dùng để ngăn chặn một lớp không cho các lớp khác kế thừa?",
         "", "static", "sealed", "readonly", "abstract",
         "B", "Trong C#, từ khóa 'sealed' đặt trước khai báo class ngăn không cho bất kỳ lớp nào kế thừa nó (tương đương từ khóa 'final' trong Java).", "easy", "Inheritance"),

        ("Trong Java, từ khóa nào cho phép một lớp kế thừa từ một lớp khác?",
         "", "implements", "inherits", "extends", "super",
         "C", "Trong Java, từ khóa 'extends' dùng cho kế thừa lớp, còn 'implements' dùng để hiện thực hóa giao diện (interface).", "easy", "Inheritance"),

        ("Mối quan hệ 'HAS-A' (ví dụ: Xe hơi CÓ một Động cơ) trong thiết kế hướng đối tượng được gọi là gì?",
         "", "Inheritance (Kế thừa)", "Aggregation / Composition (Hợp thành / Chứa đựng)", "Polymorphism (Đa hình)", "Generalization (Tổng quát hóa)",
         "B", "Quan hệ HAS-A là quan hệ kết tập (Aggregation) hoặc hợp thành chặt chẽ (Composition), biểu thị một đối tượng chứa tham chiếu tới một đối tượng khác.", "easy", "Design"),

        ("Sự khác biệt cốt lõi giữa Composition (Hợp thành chặt chẽ) và Aggregation (Kết tập) là gì?",
         "", "Composition không hỗ trợ đa hình, Aggregation thì có", "Trong Composition, vòng đời của đối tượng con phụ thuộc hoàn toàn vào đối tượng cha (cha mất thì con mất); trong Aggregation, đối tượng con có thể tồn tại độc lập", "Composition chỉ áp dụng cho ngôn ngữ C++", "Không có sự khác biệt nào",
         "B", "Ví dụ: Nhà và Phòng là Composition (phá nhà thì phòng không còn tồn tại độc lập). Trường học và Giáo viên là Aggregation (trường giải thể, giáo viên vẫn tồn tại).", "hard", "Design"),

        ("Interface trong hướng đối tượng khác Abstract Class ở điểm cốt lõi nào?",
         "", "Interface không thể chứa biến static", "Interface đại diện cho một hợp đồng hành vi (Contract / CAN-DO), không lưu trạng thái (state); Abstract Class đại diện cho một bản thể chung (IS-A) và có thể chứa thuộc tính thể hiện", "Abstract class không thể có phương thức trừu tượng", "Interface chỉ dùng được trong Java, không dùng được trong C#",
         "B", "Interface quy định các hành vi mà lớp thực thi phải có (hợp đồng CAN-DO). Một lớp có thể implement nhiều interface, nhưng đa số ngôn ngữ (Java, C#) chỉ cho phép đơn kế thừa từ một Abstract Class.", "medium", "Polymorphism"),

        ("Trong C++, một hàm thuần ảo (pure virtual function) được khai báo theo cú pháp nào?",
         "", "virtual void display() = 0;", "virtual void display() pure;", "abstract void display();", "void virtual display() null;",
         "A", "Cú pháp hàm thuần ảo trong C++ kết thúc bằng '= 0;'. Lớp chứa ít nhất một hàm thuần ảo được gọi là Lớp trừu tượng (Abstract Class) và không thể khởi tạo đối tượng trực tiếp.", "easy", "Polymorphism"),

        ("Điều gì sẽ xảy ra nếu bạn cố gắng khởi tạo một đối tượng trực tiếp từ một Abstract Class?",
         "", "Chương trình chạy bình thường và gán giá trị mặc định", "Trình biên dịch báo lỗi tại thời điểm biên dịch (Compile-time Error)", "Phát sinh ngoại lệ NullReferenceException lúc chạy", "Đối tượng được tạo nhưng không thể gọi phương thức",
         "B", "Abstract class là lớp chưa hoàn thiện (có chứa phương thức thuần ảo / abstract method), do đó không thể khởi tạo thể hiện trực tiếp qua từ khóa new.", "easy", "Polymorphism"),

        ("Nguyên lý Đóng gói (Encapsulation) bị vi phạm nghiêm trọng nhất trong tình huống nào sau đây?",
         "", "Khai báo tất cả các trường dữ liệu ở dạng private và viết hàm getter/setter", "Khai báo trực tiếp các biến thể hiện (instance fields) ở phạm vi public", "Khai báo phương thức tĩnh static", "Sử dụng từ khóa final/const cho các hằng số",
         "B", "Để các trường dữ liệu public cho phép bất kỳ mã ngoài nào tùy ý sửa đổi trạng thái đối tượng mà không qua kiểm tra tính hợp lệ, phá vỡ tính toàn vẹn dữ liệu.", "easy", "Encapsulation"),

        ("Trong C++, 'Friend Function' (hàm bạn) có đặc quyền gì đối với một lớp?",
         "", "Chỉ truy cập được các thành viên public", "Có quyền truy cập trực tiếp vào các thành viên private và protected của lớp đó dù không phải là thành viên", "Tự động kế thừa toàn bộ lớp", "Ngăn chặn lớp bị kế thừa",
         "B", "Từ khóa friend cho phép một hàm hoặc lớp bên ngoài truy cập vào các thành viên private và protected của lớp khai báo friend.", "medium", "C++ Specific"),

        ("Trong C++, vấn đề 'Diamond Problem' (Bài toán hình thoi trong đa kế thừa) phát sinh khi nào?",
         "", "Khi một lớp con kế thừa từ hai lớp cha mà cả hai lớp cha này đều cùng kế thừa từ một lớp ông nội chung", "Khi lớp con kế thừa từ 4 lớp cha khác nhau", "Khi class có 4 hàm constructor", "Khi có 4 con trỏ cùng trỏ vào một vùng nhớ",
         "A", "Diamond Problem gây ra sự mơ hồ (ambiguity) vì lớp con nhận 2 bản sao độc lập của lớp ông nội. Để giải quyết trong C++, ta dùng kế thừa ảo (Virtual Inheritance): `class B : virtual public A`.", "hard", "Inheritance"),

        ("Để giải quyết bài toán Diamond Problem trong C++, ta sử dụng kỹ thuật nào?",
         "", "Khai báo hàm friend", "Sử dụng kế thừa ảo: `virtual public Base`", "Ép kiểu dynamic_cast", "Đặt tất cả thuộc tính thành static",
         "B", "Kế thừa ảo (virtual inheritance) đảm bảo chỉ có duy nhất một bản sao thể hiện của lớp cơ sở tồn tại trong hệ thống phân cấp kế thừa.", "medium", "C++ Specific"),

        ("Tại sao ngôn ngữ Java và C# KHÔNG hỗ trợ đa kế thừa lớp (multiple class inheritance) mà chỉ hỗ trợ đa hiện thực interface?",
         "", "Để tránh sự phức tạp và xung đột của bài toán Diamond Problem trong bảng phương thức và thuộc tính", "Vì compiler không đủ thông minh để xử lý", "Vì interface chạy nhanh hơn class", "Vì đa kế thừa tốn quá nhiều RAM",
         "A", "Java và C# loại bỏ đa kế thừa lớp để tránh xung đột tên và trạng thái của Diamond Problem, thay vào đó hỗ trợ triển khai nhiều Interface vì Interface không chứa trạng thái thể hiện.", "medium", "Design"),

        ("Nguyên lý Liskov Substitution Principle (LSP) trong bộ nguyên lý SOLID phát biểu điều gì?",
         "", "Một lớp chỉ nên có một lý do duy nhất để thay đổi", "Các đối tượng của lớp con phải có thể thay thế cho các đối tượng của lớp cha mà không làm thay đổi tính đúng đắn của chương trình", "Nên phụ thuộc vào trừu tượng thay vì cụ thể", "Nhiều interface nhỏ tốt hơn một interface lớn",
         "B", "LSP: Subtypes must be substitutable for their base types. Nếu lớp con vi phạm các ràng buộc hành vi của lớp cha (ví dụ hình vuông kế thừa hình chữ nhật nhưng làm sai lệch tính diện tích), quan hệ kế thừa đó vi phạm LSP.", "hard", "SOLID"),

        ("Quan hệ giữa Lớp (Class) và Đối tượng (Object) được so sánh chính xác nhất với quan hệ nào?",
         "", "Bản vẽ thiết kế ngôi nhà (Class) và Ngôi nhà thực tế được xây dựng (Object)", "Ngôi nhà thực tế (Class) và Bản vẽ thiết kế (Object)", "Hai viên gạch giống nhau", "Người kiến trúc sư và người thợ hồ",
         "A", "Class là khuôn mẫu (blueprint/template) định nghĩa thuộc tính và hành vi, còn Object là một thể hiện cụ thể (instance) chiếm giữ vùng nhớ thực tế được tạo ra từ bản vẽ đó.", "easy", "Basics"),

        ("Trong lập trình hướng đối tượng, 'Trạng thái' (State) của một đối tượng được biểu diễn thông qua thành phần nào?",
         "", "Tên phương thức (Method Name)", "Các giá trị hiện tại của các thuộc tính (Attributes / Fields)", "Địa chỉ IP của máy tính", "Số dòng code trong file",
         "B", "Trạng thái của một đối tượng được phản ánh bởi giá trị của các thuộc tính (fields/properties) của nó tại một thời điểm nhất định.", "easy", "Basics"),

        ("Khái niệm 'Thông điệp' (Message Passing) giữa các đối tượng trong OOP thực chất là gì?",
         "", "Việc gửi email giữa 2 máy chủ", "Việc một đối tượng gọi một phương thức của một đối tượng khác", "Việc in thông báo ra màn hình console", "Việc lưu dữ liệu vào cơ sở dữ liệu",
         "B", "Gửi thông điệp (Message Passing) là hành vi một đối tượng yêu cầu đối tượng khác thực thi một hành vi thông qua việc gọi phương thức công khai của nó kèm tham số.", "easy", "Basics"),

        ("Điều gì xảy ra khi thuộc tính được đánh dấu là `static` trong một lớp?",
         "", "Mỗi đối tượng có một bản sao riêng của thuộc tính đó", "Thuộc tính đó thuộc về chính lớp chứ không thuộc về bất kỳ đối tượng cụ thể nào, và được dùng chung bởi mọi thể hiện", "Thuộc tính không thể thay đổi giá trị", "Thuộc tính chỉ tồn tại trong vòng lặp",
         "B", "Biến static là biến tĩnh cấp độ lớp (class-level variable), chỉ được cấp phát một vùng nhớ duy nhất chia sẻ chung cho toàn bộ các thể hiện của lớp.", "medium", "Basics"),

        ("Trong C#, thuộc tính (Property) với cú pháp `{ get; set; }` (Auto-implemented Property) mang lại lợi ích gì?",
         "", "Tự động sinh ra một biến nền (backing field) ẩn và cung cấp cách tiếp cận đóng gói an toàn, cú pháp gọn gàng", "Tự động mã hóa dữ liệu khi lưu vào ổ cứng", "Giúp chương trình chạy đa luồng an toàn tuyệt đối", "Tự động ép kiểu dữ liệu",
         "A", "Auto-implemented properties trong C# cho phép viết code đóng gói ngắn gọn, compiler tự sinh biến private đằng sau.", "easy", "C# Specific"),

        ("Phương thức tĩnh (`static method`) có thể truy cập trực tiếp thành phần nào sau đây của lớp?",
         "", "Các biến thể hiện (non-static instance variables)", "Con trỏ / từ khóa `this`", "Chỉ các biến tĩnh (static variables) và các hàm tĩnh khác của lớp", "Phương thức ảo (virtual methods)",
         "C", "Phương thức static không gắn với bất kỳ thể hiện cụ thể nào của đối tượng nên không có ngữ cảnh `this`, do đó không thể truy cập trực tiếp các biến hay hàm non-static.", "medium", "Basics")
    ]

    for q in oop_core:
        questions.append({
            "question_text": q[0], "code_snippet": q[1],
            "option_a": q[2], "option_b": q[3], "option_c": q[4], "option_d": q[5],
            "correct_option": q[6], "explanation": q[7], "difficulty": q[8], "topic_tag": q[9]
        })

    # 2. Constructor, Destructor, Virtual Destructor & Memory (26 - 50)
    oop_constructors = [
        ("Trong C++, nếu lập trình viên không định nghĩa bất kỳ constructor nào, trình biên dịch sẽ làm gì?",
         "", "Báo lỗi biên dịch", "Tự động tạo ra một Default Constructor mặc định không tham số", "Không cho phép tạo đối tượng", "Tự động tạo constructor có đủ mọi tham số",
         "B", "Nếu class không khai báo constructor nào, trình biên dịch sẽ tự động tạo Default Constructor ngầm định (không tham số). Nếu bạn đã viết ít nhất 1 constructor có tham số, compiler sẽ không tự sinh default constructor nữa.", "easy", "Constructor"),

        ("Khi một đối tượng của lớp con (Derived) được khởi tạo, thứ tự thực thi của các Constructor diễn ra như thế nào?",
         "", "Constructor của lớp con chạy trước, sau đó tới lớp cha", "Constructor của lớp cha chạy trước, sau đó tới lớp con", "Chỉ constructor của lớp con chạy", "Hai constructor chạy song song cùng lúc",
         "B", "Khi tạo đối tượng lớp con: Nền móng lớp cha phải được thiết lập trước -> Constructor lớp cha chạy trước, rồi mới tới constructor lớp con hoàn thiện các thành phần mở rộng.", "medium", "Constructor"),

        ("Khi một đối tượng của lớp con (Derived) bị hủy giải phóng bộ nhớ, thứ tự gọi các Destructor diễn ra như thế nào?",
         "", "Destructor của lớp cha chạy trước, sau đó tới lớp con", "Destructor của lớp con chạy trước, sau đó tới lớp cha", "Chỉ gọi destructor của lớp cha", "Hai destructor chạy ngẫu nhiên",
         "B", "Nguyên tắc LIFO (vào trước ra sau): Đối tượng con bị dọn dẹp trước -> Destructor lớp con chạy trước, sau đó mới giải phóng phần tài nguyên lớp cha.", "medium", "Destructor"),

        ("Tại sao lớp cơ sở (Base Class) luôn NÊN có Destructor Ảo (`virtual ~Base()`) trong C++?",
         "", "Để cho phép khởi tạo đối tượng nhanh hơn", "Để khi giải phóng đối tượng qua con trỏ lớp cơ sở (`Base* p = new Derived(); delete p;`), destructor của lớp con được gọi đầy đủ, tránh rò rỉ bộ nhớ (memory leak)", "Để biến class thành lớp trừu tượng", "Để tự động dọn rác như Java",
         "B", "Nếu destructor không phải là virtual, thao tác delete qua con trỏ lớp cơ sở sẽ kích hoạt Early Binding (liên kết tĩnh), chỉ gọi destructor của Base và bỏ qua destructor của Derived, dẫn đến thất thoát bộ nhớ động chưa giải phóng.", "hard", "Destructor"),

        ("Đoạn mã C++ sau đây in ra kết quả gì khi chạy?",
         """class A {
public:
    A() { cout << "1"; }
    ~A() { cout << "2"; }
};
class B : public A {
public:
    B() { cout << "3"; }
    ~B() { cout << "4"; }
};
int main() {
    B obj;
    return 0;
}""", "1234", "1342", "3124", "1324",
         "B", "Khi B obj được tạo: Constructor A chạy in '1' -> Constructor B chạy in '3'. Khi hàm main kết thúc giải phóng obj: Destructor B chạy in '4' -> Destructor A chạy in '2'. Kết quả: 1342.", "medium", "Tracing"),

        ("Trong C++, Copy Constructor được gọi trong trường hợp nào sau đây?",
         "", "Khi gán hai đối tượng đã tồn tại: `obj1 = obj2;`", "Khi một đối tượng được khởi tạo từ một đối tượng cùng kiểu đã có: `MyClass obj2 = obj1;` hoặc truyền đối tượng theo giá trị (by value) vào hàm", "Khi giải phóng đối tượng bằng `delete`", "Khi gọi phương thức clone()",
         "B", "Copy Constructor được gọi khi tạo mới đối tượng từ đối tượng có sẵn hoặc khi truyền/trả đối tượng theo giá trị. Lệnh `obj1 = obj2` khi cả 2 đã tồn tại là phép gán (Copy Assignment Operator).", "medium", "Constructor"),

        ("Khái niệm 'Shallow Copy' (Sao chép nông) và 'Deep Copy' (Sao chép sâu) khác nhau như thế nào khi đối tượng chứa con trỏ dữ liệu động?",
         "", "Shallow copy sao chép toàn bộ vùng nhớ mới, Deep copy chỉ copy địa chỉ", "Shallow copy chỉ sao chép giá trị con trỏ (hai con trỏ cùng trỏ vào 1 vùng nhớ); Deep copy cấp phát vùng nhớ độc lập mới và sao chép toàn bộ nội dung dữ liệu bên trong", "Hai khái niệm này hoàn toàn tương đương", "Deep copy chỉ dùng cho Java",
         "B", "Shallow copy chỉ copy bit-by-bit giá trị con trỏ, dễ dẫn đến lỗi 'Double Free' khi hủy 2 đối tượng. Deep copy chủ động malloc/new vùng nhớ mới cho đối tượng đích.", "hard", "Memory"),

        ("Trong C++, 'Rule of Three' (Quy tắc bộ ba) khuyến cáo nếu một lớp quản lý tài nguyên cần tự viết Destructor thì lớp đó cũng nên tự viết hai thành phần nào nữa?",
         "", "Default constructor và Constructor có tham số", "Copy Constructor và Copy Assignment Operator (`operator=`)", "Static method và Friend function", "Virtual method và Abstract class",
         "B", "Rule of Three: Nếu class cần custom Destructor để giải phóng bộ nhớ động, hầu như chắc chắn nó cần Copy Constructor và Copy Assignment Operator để xử lý Deep Copy.", "hard", "C++ Specific"),

        ("Trong C++11, 'Rule of Five' bổ sung thêm hai thành phần nào vào Rule of Three?",
         "", "Move Constructor và Move Assignment Operator", "Constructor tĩnh và Destructor tĩnh", "Lambda expression và Smart Pointer", "Getter và Setter",
         "A", "Rule of Five: Destructor, Copy Constructor, Copy Assignment, Move Constructor, Move Assignment để tận dụng Rvalue reference `&&` và di chuyển tài nguyên mà không cần sao chép tốn kém.", "hard", "C++ Specific"),

        ("Trong C++, từ khóa `explicit` đặt trước một Constructor có tác dụng gì?",
         "", "Bắt buộc constructor đó phải là private", "Ngăn chặn trình biên dịch tự động thực hiện việc chuyển đổi kiểu ngầm định (Implicit Conversion)", "Cho phép constructor kế thừa sang lớp con", "Tăng tốc độ khởi tạo biến",
         "B", "Ví dụ: `explicit MyClass(int size);` sẽ ngăn lệnh `MyClass obj = 10;`, bắt buộc người dùng phải gọi tường minh `MyClass obj(10);`.", "medium", "C++ Specific"),

        ("Trong Java, bộ thu gom rác (Garbage Collector) hoạt động dựa trên nguyên lý cơ bản nào?",
         "", "Tự động hủy đối tượng sau 10 giây", "Tự động thu hồi vùng nhớ Heap của các đối tượng không còn bất kỳ tham chiếu nào (unreachable objects) trỏ tới", "Bắt buộc lập trình viên phải gọi hàm `free()`", "Chỉ dọn rác khi máy tính hết sạch RAM",
         "B", "Garbage Collector dò tìm đồ thị tham chiếu từ GC Roots. Bất kỳ đối tượng nào không còn đường dẫn tham chiếu hợp lệ sẽ được đánh dấu và dọn dẹp bộ nhớ.", "easy", "Java Specific"),

        ("Từ khóa `finally` trong khối `try-catch-finally` (Java/C#) có đặc tính gì?",
         "", "Chỉ thực thi khi có ngoại lệ xảy ra", "Chỉ thực thi khi KHÔNG có ngoại lệ xảy ra", "Luôn luôn được thực thi dù có xảy ra ngoại lệ hay không, thường dùng để đóng kết nối và giải phóng tài nguyên", "Tự động khởi động lại chương trình",
         "C", "Khối `finally` đảm bảo luôn chạy dọn dẹp tài nguyên (file, socket, database connection) kể cả khi có lệnh return trong khối try.", "easy", "Exception"),

        ("Trong C++, smart pointer `std::unique_ptr` có đặc điểm nào sau đây?",
         "", "Cho phép nhiều con trỏ cùng sở hữu một đối tượng", "Sở hữu độc quyền một đối tượng, không thể sao chép (copy), chỉ có thể di chuyển (move), tự động giải phóng vùng nhớ khi ra khỏi phạm vi", "Tự động đếm số lượng tham chiếu", "Cần phải gọi delete thủ công",
         "B", "std::unique_ptr thể hiện cơ chế Exclusive Ownership, ngăn chặn memory leak theo nguyên lý RAII mà không tốn chi phí overhead đếm tham chiếu như shared_ptr.", "hard", "C++ Specific"),

        ("Trong C++, hiện tượng 'Dangling Pointer' (Con trỏ lơ lửng / con trỏ lạc) xuất hiện khi nào?",
         "", "Con trỏ chưa được khởi tạo giá trị", "Con trỏ vẫn giữ địa chỉ của một vùng nhớ mà vùng nhớ đó đã bị thu hồi hoặc giải phóng (`delete`)", "Con trỏ trỏ tới địa chỉ NULL", "Con trỏ được gán giá trị 0",
         "B", "Dangling Pointer trỏ tới vùng nhớ rác sau khi delete. Truy cập qua con trỏ này gây ra lỗi Undefined Behavior hoặc Crash ứng dụng.", "medium", "Memory"),

        ("Kỹ thuật lập trình tốt nhất để phòng tránh Dangling Pointer sau khi gọi `delete ptr;` là gì?",
         "", "Gọi thêm lệnh `delete ptr;` lần thứ hai", "Gán ngay con trỏ về `nullptr`: `ptr = nullptr;`", "Khai báo con trỏ dưới dạng const", "Ép kiểu con trỏ sang kiểu void*",
         "B", "Gán `ptr = nullptr;` biến nó thành con trỏ an toàn vì giải phóng `delete nullptr;` trong C++ là thao tác an toàn không gây lỗi.", "easy", "Memory"),

        ("Constructor khởi tạo danh sách (Member Initializer List) trong C++ có dạng nào?",
         "", "MyClass(int a, int b) { x = a; y = b; }", "MyClass(int a, int b) : x(a), y(b) {}", "MyClass(int a, int b) -> x(a), y(b)", "MyClass::init(x, y)",
         "B", "Cú pháp initializer list: `: field1(val1), field2(val2)` khởi tạo trực tiếp biến thành viên trước khi thân hàm constructor chạy, bắt buộc dùng cho const members, reference members hoặc lớp cha không có default constructor.", "medium", "Constructor"),

        ("Trong C#, câu lệnh `using (var resource = new MyResource()) { ... }` đảm bảo điều gì?",
         "", "Chạy đoạn code trên một luồng (thread) mới", "Tự động gọi phương thức `Dispose()` của interface `IDisposable` khi thoát khỏi khối lệnh để giải phóng tài nguyên unmanaged", "Tự động bắt tất cả các ngoại lệ phát sinh", "Tăng tốc độ truy xuất cơ sở dữ liệu",
         "B", "Cú pháp using trong C# là cú pháp viết gọn cho try-finally đảm bảo Dispose() luôn được gọi.", "medium", "C# Specific"),

        ("Phương thức ảo thuần túy trong C# được khai báo bằng từ khóa nào?",
         "", "virtual", "pure", "abstract", "override",
         "C", "Trong C#, phương thức trừu tượng trong abstract class được khai báo bằng từ khóa `abstract`: `public abstract void Draw();`.", "easy", "C# Specific"),

        ("Trong Java, từ khóa `super()` trong constructor của lớp con có ý nghĩa gì?",
         "", "Gọi phương thức super của hệ điều hành", "Gọi constructor tương ứng của lớp cha và phải là câu lệnh đầu tiên trong thân constructor của lớp con", "Tạo một đối tượng cha độc lập", "Khai báo quyền truy cập đặc biệt",
         "B", "Lệnh `super(...)` gọi tường minh constructor lớp cha và bắt buộc phải nằm ở dòng đầu tiên trong constructor của lớp con.", "easy", "Java Specific"),

        ("Đoạn code C++ sau bị lỗi gì khi biên dịch?",
         """class Student {
    const int studentId;
public:
    Student(int id) {
        studentId = id;
    }
};""", "Không có lỗi", "Biến hằng (const) `studentId` không thể gán giá trị trong thân constructor, bắt buộc phải dùng Initializer List: `: studentId(id)`", "Lớp thiếu hàm hủy destructor", "studentId phải là biến static",
         "B", "Thuộc tính `const` hoặc `reference &` trong C++ phải được khởi tạo giá trị thông qua Member Initializer List trước khi thân constructor chạy.", "hard", "Constructor"),

        ("Trong C++, toán tử nào dùng để giải phóng một mảng động được cấp phát bằng `new int[100]`?",
         "", "delete ptr;", "delete[] ptr;", "free(ptr);", "ptr.clear();",
         "B", "Cấp phát mảng `new[]` bắt buộc phải giải phóng bằng `delete[] ptr;`. Dùng `delete ptr;` sẽ gây undefined behavior (chỉ gọi destructor của phần tử đầu tiên).", "medium", "Memory"),

        ("Trong Java, hàm `finalize()` trước đây được dùng để làm gì và tại sao hiện nay bị loại bỏ (deprecated)?",
         "", "Dùng để sao chép đối tượng; bị loại bỏ vì quá chậm", "Dùng để dọn dẹp tài nguyên trước khi GC thu hồi đối tượng; bị deprecated vì không đảm bảo thời điểm chạy và có thể gây rò rỉ bộ nhớ hoặc deadlock", "Dùng để khởi tạo luồng mới", "Dùng để mã hóa đối tượng",
         "B", "Thời điểm JVM chạy finalize() là bất định, có thể không bao giờ chạy, gây thất thoát tài nguyên nghiêm trọng. Hiện nay thay bằng `AutoCloseable` và try-with-resources.", "hard", "Java Specific"),

        ("Khi nào thì một Memory Leak (Rò rỉ bộ nhớ) xảy ra trong chương trình C++?",
         "", "Khi bộ nhớ RAM của máy tính bị đầy", "Khi bộ nhớ động (Heap) được cấp phát qua `new`/`malloc` nhưng không được giải phóng qua `delete`/`free` trước khi con trỏ trỏ tới nó bị mất", "Khi gọi hàm đệ quy quá sâu gây tràn Stack (Stack Overflow)", "Khi khai báo quá nhiều biến static",
         "B", "Rò rỉ bộ nhớ xảy ra khi mất tham chiếu đến vùng nhớ Heap đã cấp phát mà không thu hồi, làm dung lượng RAM sử dụng của ứng dụng tăng liên tục.", "medium", "Memory"),

        ("Bộ nhớ Stack và bộ nhớ Heap trong kiến trúc chạy của C++/Java/C# khác nhau như thế nào?",
         "", "Stack dùng cho cấp phát động, Heap dùng cho biến cục bộ", "Stack lưu trữ biến cục bộ và lời gọi hàm (tự động giải phóng khi ra khỏi scope, tốc độ rất nhanh); Heap lưu trữ đối tượng cấp phát động (lập trình viên hoặc GC quản lý, kích thước lớn hơn nhưng tốc độ chậm hơn)", "Stack nằm trên ổ cứng, Heap nằm trên RAM", "Không có sự khác nhau",
         "B", "Stack hoạt động theo cơ chế LIFO, tự động phân phối và thu hồi cực nhanh. Heap dùng cho đối tượng có vòng đời độc lập với phạm vi hàm.", "medium", "Basics"),

        ("Đặc điểm của Constructor mặc định không đối số (Default Constructor) là gì?",
         "", "Chỉ có thể khai báo một lần duy nhất trong toàn bộ project", "Là constructor có thể được gọi mà không cần truyền bất kỳ tham số nào (không có tham số hoặc tất cả tham số đều có giá trị mặc định)", "Bắt buộc phải trả về kiểu int", "Luôn luôn nằm ở phạm vi private",
         "B", "Default constructor là constructor không cần đối số khi gọi, được dùng khi khởi tạo mảng đối tượng: `MyClass arr[10];`.", "easy", "Constructor")
    ]

    for q in oop_constructors:
        questions.append({
            "question_text": q[0], "code_snippet": q[1],
            "option_a": q[2], "option_b": q[3], "option_c": q[4], "option_d": q[5],
            "correct_option": q[6], "explanation": q[7], "difficulty": q[8], "topic_tag": q[9]
        })

    # 3. Overloading vs Overriding & Vtable (51 - 75)
    oop_methods = [
        ("Hai phương thức được gọi là nạp chồng (Overloading) khi nào?",
         "", "Cùng tên, khác tham số (số lượng, kiểu dữ liệu hoặc thứ tự), nằm trong cùng một lớp", "Cùng tên, cùng tham số, khác kiểu trả về", "Nằm ở hai lớp cha con và có cùng tham số", "Có cùng số lượng tham số nhưng khác tên hàm",
         "A", "Overloading (nạp chồng) xảy ra trong cùng một phạm vi lớp: các hàm trùng tên nhưng khác chữ ký (khác danh sách tham số). Chỉ khác kiểu trả về KHÔNG tạo nên nạp chồng hợp lệ.", "easy", "Overloading"),

        ("Điều kiện để một phương thức ở lớp con Ghi đè (Override) phương thức của lớp cha là gì?",
         "", "Phải có cùng tên, cùng danh sách tham số và cùng kiểu trả về (hoặc kiểu trả về đồng biến - covariant return type), và phương thức ở lớp cha phải là ảo (virtual/abstract)", "Chỉ cần trùng tên hàm", "Chỉ cần khác kiểu trả về", "Lớp con phải dùng từ khóa static",
         "A", "Overriding yêu cầu chữ ký giống hệt nhau và phương thức ở lớp cha phải cho phép ghi đè (virtual trong C++/C#, non-final trong Java).", "medium", "Overriding"),

        ("Cơ chế Virtual Table (Vtable) trong C++ hoạt động như thế nào?",
         "", "Là bảng lưu trữ danh sách biến tĩnh của lớp", "Là một mảng các con trỏ hàm được trình biên dịch tạo ra cho mỗi lớp có hàm ảo, mỗi đối tượng chứa con trỏ `vptr` trỏ tới vtable của lớp đó để tra cứu hàm cần gọi khi chạy", "Là bảng lưu địa chỉ RAM của các hàm inline", "Là cấu trúc dữ liệu lưu cache bộ nhớ",
         "B", "Khi lớp có ít nhất 1 hàm ảo, compiler tạo 1 Vtable chứa địa chỉ các hàm ảo. Mỗi instance chứa con trỏ ẩn `_vptr`. Khi gọi hàm ảo, chương trình truy xuất qua `_vptr` để gọi đúng hàm thực tế.", "hard", "Polymorphism"),

        ("Kích thước `sizeof` của một đối tượng thuộc class có hàm ảo trong C++ thường tăng thêm bao nhiêu byte trên hệ điều hành 64-bit?",
         "", "0 byte", "4 byte", "8 byte (kích thước của con trỏ vptr)", "16 byte",
         "C", "Trên hệ điều hành 64-bit, con trỏ `vptr` chiếm 8 byte trong mỗi thể hiện đối tượng.", "medium", "C++ Specific"),

        ("Đoạn mã C++ sau in ra kết quả gì?",
         """class Base {
public:
    virtual void print() { cout << "Base "; }
};
class Derived : public Base {
public:
    void print() override { cout << "Derived "; }
};
int main() {
    Base* b = new Derived();
    b->print();
    delete b;
    return 0;
}""", "Base", "Derived", "Base Derived", "Lỗi biên dịch",
         "B", "Do `print()` là hàm ảo (virtual) và con trỏ `b` trỏ tới thể hiện thực tế của `Derived`, cơ chế đa hình runtime sẽ gọi phương thức `print()` của `Derived`. Kết quả in: 'Derived '.", "easy", "Polymorphism"),

        ("Nếu trong đoạn mã trên, ta BỎ từ khóa `virtual` ở phương thức `print()` của class Base, kết quả in ra sẽ là gì?",
         "", "Derived", "Base", "Lỗi biên dịch", "Chương trình bị crash",
         "B", "Khi không có từ khóa `virtual`, trình biên dịch sử dụng Early Binding (liên kết tĩnh tại thời điểm biên dịch) dựa theo kiểu của con trỏ (`Base*`), do đó phương thức của `Base` được gọi.", "medium", "Polymorphism"),

        ("Trong C++, từ khóa `override` (từ C++11) đặt sau khai báo phương thức lớp con mang lại lợi ích gì?",
         "", "Bắt buộc phương thức chạy song song đa luồng", "Giúp trình biên dịch kiểm tra xem phương thức này có thực sự ghi đè đúng một hàm ảo nào của lớp cha hay không; nếu gõ sai tên hoặc sai tham số, compiler sẽ báo lỗi ngay", "Tự động gọi lại hàm cha", "Tăng tốc độ gọi hàm",
         "B", "Từ khóa `override` là một bộ kiểm tra an toàn tại compile-time, giúp phát hiện lỗi gõ sai chữ ký phương thức thay vì vô tình tạo ra hàm mới.", "medium", "C++ Specific"),

        ("Trong C++, từ khóa `final` đặt sau khai báo một phương thức ảo có tác dụng gì?",
         "", "Phương thức đó không thể gọi được nữa", "Ngăn chặn các lớp con kế thừa tiếp theo không được phép ghi đè (override) phương thức này nữa", "Biến phương thức thành hàm inline", "Phương thức trả về giá trị hằng số",
         "B", "Từ khóa `final` trong C++ ngăn chặn việc ghi đè phương thức ở các tầng kế thừa sâu hơn, hoặc ngăn chặn kế thừa class nếu đặt sau tên class.", "easy", "C++ Specific"),

        ("Đoạn mã C++ sau đây in ra kết quả gì?",
         """void show(int x) { cout << "INT"; }
void show(double x) { cout << "DOUBLE"; }
int main() {
    show(5.0f);
    return 0;
}""", "INT", "DOUBLE", "Lỗi biên dịch do mơ hồ", "Không in gì",
         "B", "`5.0f` là số thực kiểu `float`. Khi tìm hàm phù hợp, `float` được tự động thăng hạng (floating-point promotion) lên `double` thay vì chuyển sang `int`. Do đó hàm `show(double)` được gọi.", "medium", "Overloading"),

        ("Phương thức nào sau đây KHÔNG THỂ là hàm ảo (`virtual`) trong C++?",
         "", "Destructor (Hàm hủy)", "Constructor (Hàm khởi tạo)", "Phương thức public", "Phương thức protected",
         "B", "Constructor KHÔNG THỂ là virtual. Khi constructor đang chạy, đối tượng chưa được hình thành đầy đủ, con trỏ vptr chưa được khởi tạo hoàn chỉnh nên không thể tra cứu bảng vtable.", "medium", "Polymorphism"),

        ("Hiện tượng 'Object Slicing' (Cắt lát đối tượng) trong C++ xảy ra trong tình huống nào?",
         "", "Khi chia một đối tượng thành 2 nửa bằng con trỏ", "Khi gán một đối tượng lớp con (Derived) cho một biến giá trị lớp cha (Base by value), làm mất toàn bộ các thuộc tính và hành vi riêng biệt của lớp con", "Khi ép kiểu bằng dynamic_cast", "Khi xóa đối tượng bằng delete[]",
         "B", "Object Slicing xảy ra khi truyền tham trị: `Base b = derivedObj;`. Biến `b` chỉ đủ kích thước chứa phần Base, toàn bộ phần mở rộng của Derived bị cắt bỏ.", "hard", "C++ Specific"),

        ("Trong C++, toán tử nào sau đây KHÔNG THỂ nạp chồng (overload)?",
         "", "Toán tử `+`", "Toán tử `[]`", "Toán tử phạm vi `::` và toán tử truy cập thành viên `.`", "Toán tử gọi hàm `()`",
         "C", "Các toán tử không thể nạp chồng trong C++: `::` (Scope resolution), `.` (Member access), `.*` (Pointer-to-member), `?:` (Ternary), và `sizeof`.", "hard", "Overloading"),

        ("Khi nạp chồng toán tử nhập xuất `<<` và `>>` cho một class trong C++, tại sao chúng thường phải được cài đặt dưới dạng hàm bạn (`friend function`)?",
         "", "Vì toán tử này chạy nhanh hơn", "Vì toán hạng bên trái là đối tượng luồng `ostream&`/`istream&` chứ không phải là thể hiện của class ta đang thiết kế", "Vì C++ cấm nạp chồng toán tử nhập xuất dưới dạng hàm thành viên", "Cả B và C đều đúng",
         "D", "Trong `cout << obj`, đối tượng bên trái là `std::ostream`. Nếu là hàm thành viên thì nó phải thuộc lớp `ostream` (điều ta không thể sửa). Do đó phải dùng non-member function hoặc friend function.", "hard", "Overloading"),

        ("Toán tử gán tự gán (`self-assignment`, ví dụ `a = a;`) cần được xử lý đặc biệt trong nạp chồng toán tử gán `operator=` để tránh lỗi gì?",
         "", "Lỗi chia cho 0", "Lỗi giải phóng vùng nhớ đang sử dụng của chính mình trước khi kịp sao chép dữ liệu mới", "Lỗi tràn số nguyên", "Lỗi đệ quy vô tận",
         "B", "Nếu không kiểm tra `if (this == &other) return *this;`, bước giải phóng bộ nhớ cũ `delete[] buffer;` sẽ vô tình hủy hoại luôn dữ liệu của đối tượng nguồn khi nguồn và đích là cùng một thể hiện.", "hard", "C++ Specific"),

        ("Phương thức nào sau đây trong Java tương đương với toán tử nạp chồng `==` để so sánh nội dung logic giữa hai đối tượng?",
         "", "equals(Object obj)", "hashCode()", "toString()", "compareTo()",
         "A", "Trong Java, toán tử `==` so sánh địa chỉ tham chiếu (cùng trỏ vào 1 vùng nhớ). Để so sánh nội dung giá trị giữa 2 đối tượng, ta phải override phương thức `equals(Object obj)`.", "easy", "Java Specific"),

        ("Trong C#, từ khóa `new` đứng trước một phương thức của lớp con (ví dụ `public new void Show()`) có ý nghĩa gì?",
         "", "Khởi tạo đối tượng mới trên Heap", "Ẩn tường minh (Method Hiding/Shadowing) phương thức của lớp cha mà không ghi đè (không dùng polymorphism)", "Báo cho trình biên dịch cấp phát thêm bộ nhớ", "Bắt buộc gọi lại phương thức cha",
         "B", "Từ khóa `new` trong định nghĩa phương thức C# cho biết phương thức này cố tình che giấu (hide) phương thức trùng tên của lớp cha, tắt cảnh báo của compiler.", "medium", "C# Specific"),

        ("Trong Java, tại sao khi ta ghi đè phương thức `equals()`, ta BẮT BUỘC phải ghi đè luôn phương thức `hashCode()`?",
         "", "Để chương trình chạy không bị crash", "Để đảm bảo hợp đồng Hash Code: Hai đối tượng bằng nhau theo `equals()` thì BẮT BUỘC phải có cùng mã `hashCode()`, nếu không các cấu trúc HashMap/HashSet sẽ hoạt động sai", "Để tăng tốc độ in chuỗi toString()", "Vì cú pháp Java bắt buộc",
         "B", "Nếu 2 đối tượng bằng nhau mà hashCode khác nhau, HashMap có thể xếp chúng vào 2 bucket khác nhau, dẫn đến không tìm thấy đối tượng dù nó tồn tại.", "hard", "Java Specific"),

        ("Toán tử ép kiểu `dynamic_cast` trong C++ được dùng trong trường hợp nào?",
         "", "Ép kiểu giữa số nguyên và số thực", "Downcasting an toàn từ con trỏ lớp cha xuống con trỏ lớp con trong hệ thống phân cấp kế thừa đa hình (trả về nullptr nếu ép kiểu thất bại)", "Ép kiểu hằng số thành biến thường", "Chuyển đổi chuỗi thành số",
         "B", "dynamic_cast sử dụng thông tin RTTI (Run-Time Type Information) để kiểm tra tính hợp lệ của phép ép kiểu con trỏ xuống lớp dẫn xuất tại runtime.", "medium", "C++ Specific"),

        ("Từ khóa nào trong Java tương đương với `dynamic_cast` trong C++ hoặc toán tử `is` trong C#?",
         "", "typeof", "instanceof", "isinstance", "typeid",
         "B", "Trong Java, toán tử `instanceof` kiểm tra xem đối tượng có phải là thể hiện của một lớp hoặc interface cụ thể hay không: `if (obj instanceof Student) ...`.", "easy", "Java Specific"),

        ("Cơ chế RTTI (Run-Time Type Information) trong C++ cung cấp toán tử nào để lấy tên kiểu dữ liệu tại thời điểm chạy?",
         "", "sizeof", "typeid", "decltype", "typeof",
         "B", "Toán tử `typeid(obj).name()` trả về thông tin kiểu dữ liệu động của đối tượng tại runtime (yêu cầu class phải có ít nhất 1 hàm ảo).", "medium", "C++ Specific"),

        ("Khái niệm 'Upcasting' trong lập trình hướng đối tượng là gì?",
         "", "Chuyển con trỏ/tham chiếu từ lớp con thành con trỏ/tham chiếu lớp cha (luôn luôn an toàn và được thực hiện ngầm định)", "Ép kiểu từ lớp cha xuống lớp con", "Nâng cấp phiên bản của class", "Tăng kích thước bộ nhớ của đối tượng",
         "A", "Upcasting: Vì Derived IS-A Base, nên việc coi một đối tượng con như một đối tượng cha luôn hợp lệ và không cần ép kiểu tường minh.", "easy", "Basics"),

        ("Khái niệm 'Downcasting' trong OOP là gì?",
         "", "Chuyển con trỏ lớp con thành lớp cha", "Chuyển con trỏ/tham chiếu từ lớp cha xuống lớp con cụ thể (tiềm ẩn nguy cơ lỗi runtime, cần kiểm tra cẩn thận)", "Xóa đối tượng khỏi bộ nhớ", "Giảm số lượng thuộc tính của đối tượng",
         "B", "Downcasting tiềm ẩn nguy hiểm vì đối tượng cha thực tế có thể không phải là thể hiện của lớp con mà ta đang cố ép sang, dễ gây Crash nếu không kiểm tra.", "medium", "Basics"),

        ("Phát biểu nào sau đây đúng về hàm thuần ảo (pure virtual function)?",
         "", "Hàm thuần ảo bắt buộc phải có phần thân code trong lớp khai báo nó", "Hàm thuần ảo đóng vai trò như một giao ước buộc các lớp con cụ thể (concrete class) phải cung cấp cài đặt", "Một lớp có thể chứa tối đa 1 hàm thuần ảo", "Hàm thuần ảo tự động chạy khi khởi động chương trình",
         "B", "Hàm thuần ảo ép buộc các lớp con kế thừa phải định nghĩa chi tiết cho nó, biến lớp hiện tại thành lớp trừu tượng.", "easy", "Polymorphism"),

        ("Trong C++, nếu một lớp con kế thừa từ một Abstract Class nhưng KHÔNG ghi đè (override) tất cả các hàm thuần ảo, điều gì xảy ra?",
         "", "Trình biên dịch tự động bỏ qua các hàm chưa ghi đè", "Lớp con đó vẫn tiếp tục là một Abstract Class và không thể khởi tạo đối tượng", "Chương trình tự động gán code rỗng cho các hàm đó", "Báo lỗi chỉ khi ta gọi hàm đó",
         "B", "Lớp con còn nợ ít nhất 1 hàm thuần ảo chưa hiện thực thì nó vẫn là Abstract Class và không thể tạo instance.", "medium", "Polymorphism"),

        ("Đặc điểm nào của con trỏ `this` trong C++ là chính xác?",
         "", "Là con trỏ tĩnh có thể thay đổi địa chỉ tùy ý", "Là con trỏ hằng ẩn (const pointer) trỏ tới chính đối tượng đang thực thi phương thức", "Được truyền ngầm định vào cả phương thức tĩnh (static method)", "Có thể giải phóng bằng lệnh `delete this;` ở mọi nơi",
         "B", "`this` là con trỏ trỏ tới chính đối tượng đang gọi phương thức non-static. Kiểu của nó trong `MyClass` là `MyClass* const` (hoặc `const MyClass* const` trong const member function).", "medium", "C++ Specific")
    ]

    for q in oop_methods:
        questions.append({
            "question_text": q[0], "code_snippet": q[1],
            "option_a": q[2], "option_b": q[3], "option_c": q[4], "option_d": q[5],
            "correct_option": q[6], "explanation": q[7], "difficulty": q[8], "topic_tag": q[9]
        })

    # 4. Access Modifiers, Design Patterns & Code Output Tracing (76 - 100)
    oop_advanced = [
        ("Trong C#, phạm vi truy cập `internal` cho phép thành viên được truy cập ở đâu?",
         "", "Trong toàn bộ Solution", "Bất kỳ đâu bên trong cùng một Assembly (.dll hoặc .exe)", "Chỉ trong cùng một file source code", "Chỉ trong cùng một class",
         "B", "`internal` giới hạn phạm vi truy cập bên trong cùng một Assembly, rất hữu ích khi xây dựng thư viện dùng nội bộ.", "medium", "C# Specific"),

        ("Trong C#, phạm vi truy cập `protected internal` có ý nghĩa là gì?",
         "", "Có thể truy cập từ bất kỳ code nào trong cùng Assembly, HOẶC từ các lớp con ở Assembly khác", "Chỉ truy cập được từ lớp con trong cùng Assembly", "Bị khóa hoàn toàn", "Tương đương private",
         "A", "`protected internal` là phép tuyển logic (OR): Truy cập được bởi bất kỳ lớp nào cùng Assembly, hoặc bởi các lớp kế thừa ở bất kỳ Assembly nào.", "hard", "C# Specific"),

        ("Design Pattern nào đảm bảo một lớp chỉ có duy nhất một thể hiện (single instance) trong suốt vòng đời ứng dụng?",
         "", "Factory Pattern", "Observer Pattern", "Singleton Pattern", "Strategy Pattern",
         "C", "Singleton Pattern giới hạn việc khởi tạo của một lớp thành một thể hiện duy nhất và cung cấp một điểm truy cập toàn cục tới thể hiện đó.", "easy", "Design Patterns"),

        ("Để cài đặt mẫu thiết kế Singleton trong C++ một cách thread-safe theo chuẩn C++11 (Meyers' Singleton), ta áp dụng cách nào?",
         "", "Dùng con trỏ raw pointer và cấp phát trong hàm main", "Dùng biến cục bộ tĩnh (`static MyClass instance;`) bên trong hàm `getInstance()`", "Khai báo 10 biến volatile", "Dùng hàm malloc trong constructor",
         "B", "Từ C++11, biến static cục bộ được tiêu chuẩn hóa đảm bảo khởi tạo thread-safe (Magic Statics) khi hàm được gọi lần đầu tiên mà không cần khóa mutex thủ công.", "hard", "Design Patterns"),

        ("Design Pattern nào cung cấp một giao diện để tạo các đối tượng trong lớp cha, nhưng cho phép các lớp con thay đổi kiểu đối tượng sẽ được tạo ra?",
         "", "Factory Method Pattern", "Decorator Pattern", "Adapter Pattern", "Composite Pattern",
         "A", "Factory Method định nghĩa một phương thức tạo đối tượng, để các lớp con quyết định lớp cụ thể nào sẽ được khởi tạo.", "medium", "Design Patterns"),

        ("Đoạn mã C++ sau đây in ra kết quả gì?",
         """class Test {
    static int count;
public:
    Test() { count++; }
    static int getCount() { return count; }
};
int Test::count = 0;
int main() {
    Test t1, t2, t3;
    cout << Test::getCount();
    return 0;
}""", "0", "1", "3", "Lỗi biên dịch",
         "C", "Biến `count` là static dùng chung cho mọi đối tượng. Khi tạo 3 đối tượng `t1, t2, t3`, constructor chạy 3 lần tăng `count` từ 0 lên 3. `Test::getCount()` in ra 3.", "easy", "Tracing"),

        ("Đoạn mã C++ sau đây in ra kết quả gì?",
         """class A {
public:
    virtual void f() { cout << "A"; }
};
class B : public A {
public:
    void f() override { cout << "B"; }
};
void call(A obj) {
    obj.f();
}
int main() {
    B b;
    call(b);
    return 0;
}""", "B", "A", "AB", "Lỗi biên dịch",
         "B", "Hàm `call(A obj)` nhận tham số theo GIÁ TRỊ (by value) chứ không phải con trỏ hay tham chiếu! Hiện tượng Object Slicing xảy ra, đối tượng `b` bị cắt lát thành một đối tượng `A` thuần túy, do đó `A::f()` được gọi và in ra 'A'.", "hard", "Tracing"),

        ("Đoạn mã C++ sau đây in ra kết quả gì?",
         """int main() {
    int a = 10, b = 20;
    int& ref = a;
    ref = b;
    ref += 5;
    cout << a << " " << b;
    return 0;
}""", "10 25", "25 20", "20 25", "25 25",
         "B", "Tham chiếu `ref` liên kết vĩnh viễn với biến `a`. Lệnh `ref = b;` gán giá trị của `b` (20) vào `a` (`a` thành 20, `b` vẫn là 20). Sau đó `ref += 5;` tăng `a` lên 25. Biến `b` không hề thay đổi. Kết quả in: '25 20'.", "medium", "Tracing"),

        ("Trong C++, sự khác biệt giữa `const int* ptr` và `int* const ptr` là gì?",
         "", "`const int*` là con trỏ hằng (không đổi địa chỉ); `int* const` trỏ tới số nguyên hằng", "`const int*` là con trỏ trỏ tới dữ liệu hằng (không thể thay đổi giá trị `*ptr`); `int* const` là con trỏ hằng (không thể trỏ sang biến khác)", "Cả hai hoàn toàn giống nhau", "Trình biên dịch không cho phép khai báo",
         "B", "Quy tắc đọc ngược từ phải sang trái: `const int* p`: p is a pointer to const int (giá trị bị khóa). `int* const p`: p is a const pointer to int (địa chỉ bị khóa).", "medium", "C++ Specific"),

        ("Hàm đệ quy tính giai thừa sau đây có nguy cơ gặp lỗi gì khi truyền vào số nguyên n rất lớn (ví dụ n = 1000000)?",
         """long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}""", "Lỗi chia cho 0", "Lỗi tràn bộ nhớ Stack (Stack Overflow) do tạo quá nhiều stack frame", "Lỗi rò rỉ bộ nhớ Heap", "Lỗi vòng lặp vô tận",
         "B", "Mỗi lời gọi đệ quy đẩy một stack frame vào Call Stack. Với n = 1 triệu, kích thước Call Stack vượt quá giới hạn (mặc định 1MB - 8MB) gây Stack Overflow.", "medium", "Basics"),

        ("Đoạn mã C# sau đây có đặc điểm gì?",
         """public class Person {
    public string Name { get; init; }
}""", "Thuộc tính Name có thể gán giá trị ở bất cứ đâu", "Từ khóa `init` chỉ cho phép gán giá trị cho thuộc tính trong quá trình khởi tạo đối tượng (Object Initializer), sau đó trở thành bất biến (immutable)", "Name không thể chứa chuỗi rỗng", "Trình biên dịch báo lỗi cú pháp",
         "B", "C# 9.0 giới thiệu `init-only setters` cho phép tạo các đối tượng bất biến (immutable) an toàn nhưng vẫn hỗ trợ cú pháp khởi tạo linh hoạt.", "medium", "C# Specific"),

        ("Trong Java, tại sao chuỗi ký tự (`String`) được thiết kế là Bất Biến (Immutable)?",
         "", "Để tiết kiệm RAM nhờ String Constant Pool, an toàn khi sử dụng trong môi trường đa luồng (thread-safe), và bảo mật khi dùng làm khóa cho HashMap", "Vì JVM không hỗ trợ sửa chuỗi", "Để lập trình viên bắt buộc phải dùng StringBuilder", "Vì chuỗi chỉ chứa được 256 ký tự",
         "A", "Tính bất biến của String mang lại ưu thế vượt trội về bảo mật (truyền tham số database/URL), tối ưu hóa bộ nhớ với String Pool và thread-safety.", "medium", "Java Specific"),

        ("Đoạn mã C++ sau đây in ra kết quả gì?",
         """class Demo {
public:
    Demo() { cout << "A"; }
    Demo(const Demo&) { cout << "B"; }
};
void test(Demo d) {}
int main() {
    Demo d1;
    test(d1);
    return 0;
}""", "AA", "AB", "BA", "BB",
         "B", "`Demo d1;` gọi Default Constructor in ra 'A'. Khi gọi `test(d1)`, tham số được truyền theo giá trị nên Copy Constructor được kích hoạt in ra 'B'. Kết quả in: 'AB'.", "medium", "Tracing"),

        ("Design Pattern nào được dùng khi cần chuyển đổi giao diện (interface) của một lớp thành một giao diện khác mà client mong đợi?",
         "", "Observer Pattern", "Adapter Pattern", "Singleton Pattern", "Decorator Pattern",
         "B", "Adapter Pattern (Mẫu tiếp hợp / chuyển đổi) đóng vai trò như một bộ chuyển đổi giữa hai hệ thống có giao diện không tương thích nhau.", "easy", "Design Patterns"),

        ("Design Pattern nào định nghĩa mối quan hệ phụ thuộc một-nhiều giữa các đối tượng, sao cho khi một đối tượng thay đổi trạng thái, tất cả các đối tượng phụ thuộc của nó sẽ được tự động thông báo và cập nhật?",
         "", "Observer Pattern", "Factory Pattern", "Facade Pattern", "Builder Pattern",
         "A", "Observer Pattern là nền tảng của các kiến trúc hướng sự kiện (Event-driven), kiến trúc MVC, Publish-Subscribe.", "easy", "Design Patterns"),

        ("Đoạn mã C++ sau đây gặp lỗi gì?",
         """int* createNumber() {
    int x = 42;
    return &x;
}
int main() {
    int* p = createNumber();
    cout << *p;
    return 0;
}""", "Không có lỗi, in ra 42", "Lỗi trả về con trỏ trỏ tới biến cục bộ trên Stack (Dangling Pointer) đã bị giải phóng khi hàm kết thúc", "Lỗi chia cho 0", "Lỗi thiếu thư viện",
         "B", "Biến `x` được cấp phát trên Stack của hàm `createNumber()`. Khi hàm kết thúc, stack frame bị thu hồi. Con trỏ `p` trỏ tới vùng nhớ rác (Undefined Behavior).", "medium", "Memory"),

        ("Cách sửa đúng nhất cho hàm `createNumber()` trong câu trên là gì?",
         "", "Khai báo `int x = 42;` thành `static int x = 42;` hoặc cấp phát động `int* x = new int(42);` trên Heap", "Thêm từ khóa const trước int", "Ép kiểu &x sang void*", "Bỏ lệnh return",
         "A", "Dùng biến static (nằm ở vùng nhớ Data Segment tồn tại suốt chương trình) hoặc cấp phát Heap bằng `new` (cần nhớ delete) sẽ đảm bảo vùng nhớ tồn tại sau khi thoát hàm.", "medium", "Memory"),

        ("Trong Java, cấu trúc dữ liệu `ArrayList` và `LinkedList` khác nhau cơ bản ở điểm nào?",
         "", "ArrayList dựa trên mảng động (truy xuất phần tử ngẫu nhiên O(1) rất nhanh, chèn/xóa ở giữa O(N) chậm); LinkedList dựa trên danh sách liên kết đôi (truy xuất O(N) chậm, chèn/xóa tại node O(1) nhanh)", "LinkedList nhanh hơn ArrayList trong mọi trường hợp", "ArrayList không cho phép chứa phần tử trùng", "Hai lớp này hoàn toàn giống nhau",
         "A", "ArrayList tối ưu cho bài toán đọc dữ liệu (Random Access). LinkedList tối ưu cho bài toán thường xuyên chèn/xóa phần tử ở đầu/giữa danh sách.", "medium", "Java Specific"),

        ("Đoạn mã C++ sau in ra kết quả gì?",
         """int main() {
    int x = 5;
    int y = x++ + ++x;
    cout << y;
    return 0;
}""", "10", "12", "Hành vi không xác định (Undefined Behavior) trong C++ do thay đổi biến x hai lần trong cùng một biểu thức", "11",
         "C", "Thay đổi giá trị một biến nhiều lần mà không có Sequence Point giữa chúng dẫn đến Undefined Behavior trong tiêu chuẩn C++.", "hard", "C++ Specific"),

        ("Khi thiết kế một class mô tả File Stream, nguyên lý RAII (Resource Acquisition Is Initialization) khuyến cáo điều gì?",
         "", "Mở file trong Constructor và tự động đóng file trong Destructor", "Đóng file bằng cách gọi hàm Close() thủ công ở cuối hàm main", "Chỉ mở file khi có lỗi", "Không bao giờ đóng file",
         "A", "RAII liên kết vòng đời tài nguyên với vòng đời đối tượng: khởi tạo tài nguyên trong constructor và tự động thu hồi trong destructor để đảm bảo không thất thoát kể cả khi có ngoại lệ.", "medium", "Design"),

        ("Khái niệm 'Encapsulation' (Đóng gói) khác với 'Information Hiding' (Che giấu thông tin) ở điểm nào?",
         "", "Đóng gói là cơ chế gom nhóm dữ liệu và phương thức; Che giấu thông tin là nguyên lý hạn chế quyền truy cập vào các chi tiết cài đặt nội bộ", "Hai khái niệm hoàn toàn là một", "Đóng gói chỉ có trong Java, che giấu thông tin chỉ có trong C++", "Che giấu thông tin là việc mã hóa dữ liệu",
         "A", "Đóng gói (Encapsulation) là 'đóng gói lại một chỗ'. Việc kết hợp đóng gói với các access modifier (private/protected) mới hiện thực hóa nguyên lý 'Che giấu thông tin'.", "hard", "Basics"),

        ("Đoạn mã C++ sau đây in ra kết quả gì?",
         """struct Point {
    int x, y;
};
int main() {
    Point p1 = {1, 2};
    Point p2 = p1;
    p2.x = 99;
    cout << p1.x << " " << p2.x;
    return 0;
}""", "99 99", "1 99", "1 2", "Lỗi biên dịch",
         "B", "`p2 = p1;` thực hiện copy giá trị bit-by-bit của struct. `p1` và `p2` là hai biến độc lập trên Stack. Sửa `p2.x` không ảnh hưởng tới `p1.x`. Kết quả in: '1 99'.", "easy", "Tracing"),

        ("Trong C++, từ khóa `mutable` đặt trước một biến thành viên có tác dụng gì?",
         "", "Cho phép biến đó có thể thay đổi giá trị ngay cả bên trong các phương thức hằng (`const member function`)", "Biến có thể tự đổi kiểu dữ liệu", "Biến trở thành hằng số", "Biến được chia sẻ giữa các luồng",
         "A", "Từ khóa `mutable` rất hữu ích cho các trường dữ liệu nội bộ như bộ nhớ đệm (cache), khóa mutex hoặc bộ đếm số lần gọi hàm trong const member function.", "hard", "C++ Specific"),

        ("Trong lập trình hướng đối tượng, nguyên tắc 'Composition over Inheritance' (Ưu tiên hợp thành hơn kế thừa) được khuyên dùng vì lý do gì?",
         "", "Kế thừa làm hệ thống bị ghép nối lỏng lẻo", "Kế thừa tạo sự phụ thuộc chặt chẽ (tight coupling) giữa lớp cha và con, làm giảm tính linh hoạt; Composition cho phép thay đổi hành vi đối tượng động tại thời điểm chạy", "Hợp thành chạy nhanh hơn kế thừa gấp 10 lần", "Kế thừa bị cấm trong các dự án lớn",
         "B", "Kế thừa làm lộ chi tiết cài đặt của cha cho con (White-box reuse). Hợp thành (Composition / Black-box reuse) giúp hệ thống dễ mở rộng, bảo trì và kiểm thử hơn.", "hard", "Design"),

        ("Toán tử ba ngôi `condition ? expr1 : expr2` trong C++/Java/C# có đặc điểm gì?",
         "", "Chỉ dùng để in chuỗi", "Là một biểu thức trả về giá trị dựa trên điều kiện logic, có thể dùng thay thế cho câu lệnh `if-else` đơn giản", "Luôn thực thi cả hai biểu thức expr1 và expr2", "Chỉ chạy được với số nguyên",
         "B", "Toán tử điều kiện (Ternary Operator) đánh giá `condition`, nếu đúng thì chỉ thực thi và trả về `expr1`, ngược lại chỉ thực thi và trả về `expr2` (Short-circuit evaluation).", "easy", "Basics")
    ]

    for q in oop_advanced:
        questions.append({
            "question_text": q[0], "code_snippet": q[1],
            "option_a": q[2], "option_b": q[3], "option_c": q[4], "option_d": q[5],
            "correct_option": q[6], "explanation": q[7], "difficulty": q[8], "topic_tag": q[9]
        })

    return questions

print(f"OOP Questions defined: {len(get_oop_100_questions())}")
