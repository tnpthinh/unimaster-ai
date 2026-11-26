# -*- coding: utf-8 -*-
"""
Script xây dựng và kiểm tra 100 câu trắc nghiệm C# OOP chuẩn đại học.
Đảm bảo:
1. len(correct_option) <= max(wrong_options) cho TẤT CẢ các câu.
2. Không chứa các cụm "theo như tài liệu", "theo tài liệu".
3. Kiến thức chuẩn mực C# OOP đại học: CLR, CTS, Memory (Stack/Heap), 4 tính chất, SOLID, C# 8/9/10/11 features.
4. Giải thích cực kỳ chi tiết, bản chất sâu sắc để sinh viên học và hiểu tận gốc.
"""

questions_part1 = [
    # 1
    {
        "q": "Trong C#, sự khác biệt cốt lõi về mặt quản lý bộ nhớ giữa 'class' và 'struct' là gì?",
        "A": "Class là kiểu tham chiếu cấp phát trên Heap; struct là kiểu giá trị cấp phát trên Stack (hoặc inline)",
        "B": "Class là kiểu giá trị cấp phát trên Stack; struct là kiểu tham chiếu cấp phát trên vùng nhớ Managed Heap",
        "C": "Class luôn được thu gom bởi Garbage Collector ngay lập tức; struct không bao giờ bị thu hồi bộ nhớ RAM",
        "D": "Class hỗ trợ đa kế thừa trực tiếp từ nhiều class khác; struct chỉ kế thừa được từ một class cha duy nhất",
        "corr": "A",
        "exp": "Trong hệ thống kiểu CTS của .NET, class là Reference Type nên thực thể của nó được lưu trên Managed Heap và được quản lý bởi Garbage Collector (GC). Ngược lại, struct là Value Type, giá trị được lưu trữ trực tiếp trên Stack (hoặc nằm nội tuyến bên trong đối tượng chứa nó), giúp tối ưu hiệu năng và không chịu sự quản lý trực tiếp của GC.",
        "diff": "medium", "tag": "Memory Management"
    },
    # 2
    {
        "q": "Từ khóa access modifier nào trong C# cho phép thành viên chỉ được truy cập bên trong cùng một Assembly (project/dll)?",
        "A": "private protected (chỉ cho phép trong lớp và các lớp con nằm trong cùng Assembly)",
        "B": "protected internal (cho phép trong cùng Assembly hoặc lớp con ở Assembly khác)",
        "C": "internal (chỉ cho phép truy cập từ bất kỳ đoạn mã nào nằm trong cùng Assembly)",
        "D": "protected (chỉ cho phép truy cập bên trong nội bộ lớp cha và các lớp con kế thừa)",
        "corr": "C",
        "exp": "Từ khóa 'internal' giới hạn phạm vi truy cập của kiểu dữ liệu hoặc thành viên chỉ trong cùng một Assembly (.dll hoặc .exe). 'protected' chỉ cho phép trong lớp và các lớp con; 'protected internal' cho phép truy cập từ cùng Assembly HOẶC từ lớp con ở Assembly khác; 'private protected' chỉ cho phép lớp con nằm CÙNG Assembly.",
        "diff": "easy", "tag": "Access Modifiers"
    },
    # 3
    {
        "q": "Từ khóa 'init' trong khai báo thuộc tính (Property) của C# 9.0+ có vai trò gì?",
        "A": "Cho phép gán giá trị bất kỳ lúc nào nhưng bắt buộc phải thông qua phương thức khởi tạo tĩnh",
        "B": "Chỉ cho phép gán lúc khởi tạo đối tượng, sau đó biến đối tượng thành bất biến (immutable)",
        "C": "Bắt buộc thuộc tính phải có giá trị mặc định là null trước khi gọi hàm khởi tạo có tham số",
        "D": "Tự động sinh ra một biến cục bộ tạm thời để lưu trữ dữ liệu trên Stack thay vì Managed Heap",
        "corr": "B",
        "exp": "Bộ truy cập 'init' (Init-only setters) cho phép thuộc tính được thiết lập giá trị trong quá trình khởi tạo đối tượng (qua Constructor hoặc cú pháp Object Initializer { Prop = val }), nhưng sau khi đối tượng đã khởi tạo xong, thuộc tính này hoàn toàn chỉ đọc (read-only), giúp thiết kế đối tượng bất biến an toàn và ngắn gọn.",
        "diff": "medium", "tag": "Properties"
    },
    # 4
    {
        "q": "Sự khác biệt căn bản giữa hai từ khóa 'const' và 'readonly' trong C# là gì?",
        "A": "'const' là hằng số compile-time; 'readonly' là hằng số run-time có thể gán trong Constructor",
        "B": "'const' chỉ dùng được trong phạm vi hàm; 'readonly' chỉ dùng cho biến toàn cục của lớp tĩnh",
        "C": "'const' có thể thay đổi giá trị trong Constructor; 'readonly' không thể thay đổi sau biên dịch",
        "D": "'const' được cấp phát trên Heap; 'readonly' luôn luôn được cấp phát tĩnh trên bộ nhớ Stack",
        "corr": "A",
        "exp": "'const' được đánh giá tại thời điểm biên dịch (Compile-time constant), bắt buộc phải gán giá trị cố định ngay khi khai báo và giá trị này được nhúng trực tiếp vào mã IL. Trong khi đó, 'readonly' là hằng số thời điểm chạy (Runtime constant), cho phép tính toán và gán giá trị tại lúc khai báo hoặc bên trong Constructor của lớp.",
        "diff": "medium", "tag": "Keywords"
    },
    # 5
    {
        "q": "Trong C#, phạm vi truy cập 'protected internal' mang ý nghĩa nào sau đây?",
        "A": "Chỉ các lớp con nằm trong cùng Assembly mới có thể truy cập được dữ liệu thành viên này",
        "B": "Chỉ các lớp nằm ngoài Assembly và đồng thời là lớp con mới truy cập được trường dữ liệu",
        "C": "Truy cập được từ bất kỳ code nào trong cùng Assembly HOẶC từ các lớp con ở Assembly khác",
        "D": "Hoàn toàn tương đương với phạm vi truy cập public trong toàn bộ các project của giải pháp",
        "corr": "C",
        "exp": "'protected internal' là phép hợp logic (OR): thành viên có thể được truy cập bởi bất kỳ đoạn mã nào nằm trong cùng một Assembly, HOẶC bởi bất kỳ lớp dẫn xuất (lớp con) nào dù lớp dẫn xuất đó nằm ở một Assembly hoàn toàn khác.",
        "diff": "hard", "tag": "Access Modifiers"
    },
    # 6
    {
        "q": "Phạm vi truy cập 'private protected' (từ C# 7.2) có ý nghĩa như thế nào?",
        "A": "Chỉ có các lớp con nằm trong cùng một Assembly mới được phép truy cập",
        "B": "Bất kỳ lớp nào trong cùng Assembly đều truy cập được mà không cần kế thừa",
        "C": "Chỉ lớp cha truy cập được, tất cả các lớp con ở mọi nơi đều bị từ chối",
        "D": "Cho phép truy cập công khai trong Assembly nhưng chặn truy cập ngoài Assembly",
        "corr": "A",
        "exp": "'private protected' là phép giao logic (AND): thành viên chỉ có thể được truy cập bởi các lớp con (derived classes) VÀ đồng thời lớp con đó phải nằm CÙNG một Assembly với lớp cha khai báo nó.",
        "diff": "hard", "tag": "Access Modifiers"
    },
    # 7
    {
        "q": "Lớp (class) nào là lớp gốc tối cao mà mọi kiểu dữ liệu trong C# (kể cả int, bool, struct) đều trực tiếp hoặc gián tiếp kế thừa?",
        "A": "System.Type (lớp biểu diễn thông tin phản chiếu kiểu dữ liệu tại thời điểm chạy thực tế)",
        "B": "System.ValueType (lớp cơ sở riêng dành cho các kiểu dữ liệu giá trị)",
        "C": "System.Object (lớp gốc tối cao của toàn bộ hệ thống kiểu CTS trong .NET)",
        "D": "System.Component (lớp cơ sở cho các thành phần giao diện người dùng)",
        "corr": "C",
        "exp": "Trong Common Type System (CTS) của .NET, class System.Object (alias là object trong C#) là gốc của toàn bộ cây phả hệ kiểu dữ liệu. Tất cả các kiểu tham chiếu và kiểu giá trị (thông qua System.ValueType kế thừa Object) đều thừa hưởng các phương thức cơ bản như ToString(), Equals(), GetHashCode(), GetType().",
        "diff": "easy", "tag": "Type System"
    },
    # 8
    {
        "q": "Đoạn mã sau vi phạm nguyên tắc nào trong C#?\nstruct Diem { public int X; public Diem() { } } (trước C# 10)",
        "A": "struct không được phép chứa các trường dữ liệu mang kiểu nguyên thủy như kiểu int",
        "B": "Trước C# 10, struct không được phép khai báo hàm khởi tạo không tham số tường minh",
        "C": "struct bắt buộc phải kế thừa tường minh từ một struct khác trước khi tạo constructor",
        "D": "struct chỉ được phép chứa các phương thức tĩnh chứ không thể chứa phương thức thực thể",
        "corr": "B",
        "exp": "Trước phiên bản C# 10, ngôn ngữ cấm tuyệt đối việc định nghĩa Constructor không tham số tường minh (parameterless constructor) cho struct, vì runtime luôn khởi tạo struct bằng cách xóa sạch vùng nhớ về bit 0 (default value). Từ C# 10 quy định này mới được nới lỏng.",
        "diff": "medium", "tag": "Structs"
    },
    # 9
    {
        "q": "Khi truyền một biến kiểu tham chiếu (đối tượng class) vào một hàm không có từ khóa ref/out, điều gì thực sự được sao chép?",
        "A": "Toàn bộ vùng nhớ chứa các trường của đối tượng trên Managed Heap được nhân bản thành bản sao mới hoàn toàn",
        "B": "Địa chỉ tham chiếu trỏ đến đối tượng được truyền theo cơ chế truyền giá trị (pass-by-value)",
        "C": "Đối tượng bị chuyển đổi tức thì thành một struct tạm thời trên ngăn xếp Stack hệ thống",
        "D": "Hàm sẽ tạo ra một luồng xử lý mới để cô lập đối tượng ban đầu với lời gọi bên ngoài",
        "corr": "B",
        "exp": "Mặc định trong C#, mọi tham số đều truyền theo giá trị (pass-by-value). Với kiểu tham chiếu, giá trị được truyền và sao chép chính là 'con trỏ tham chiếu' (pointer/reference). Do đó cả hai biến tham chiếu cùng trỏ tới một vùng nhớ trên Heap; sửa đổi thuộc tính đối tượng sẽ ảnh hưởng ra ngoài, nhưng nếu gán biến đó = new MyClass() thì bên ngoài không đổi.",
        "diff": "hard", "tag": "Memory Management"
    },
    # 10
    {
        "q": "Từ khóa 'static' đặt trước định nghĩa một lớp (static class) trong C# dẫn đến ràng buộc nào?",
        "A": "Lớp chỉ được chứa thành viên tĩnh, không thể tạo instance bằng từ khóa new và bị sealed",
        "B": "Lớp có thể kế thừa từ một class thông thường nhưng không được phép cài đặt bất kỳ interface nào",
        "C": "Lớp bắt buộc phải có ít nhất một constructor công khai nhận tham số kiểu chuỗi ký tự",
        "D": "Lớp có thể được nhân bản thành nhiều đối tượng độc lập trong các thread khác nhau",
        "corr": "A",
        "exp": "Một static class trong C# được trình biên dịch gắn cờ 'abstract sealed' trong mã IL. Điều này đồng nghĩa với việc: không thể khởi tạo đối tượng (new), không thể kế thừa, và tất cả thành viên bên trong nó (hàm, biến, property) bắt buộc phải mang từ khóa static.",
        "diff": "easy", "tag": "Static Class"
    },
    # 11
    {
        "q": "Điều gì xảy ra khi gán giá trị của một biến kiểu struct sang một biến struct khác (struct B = A;)?",
        "A": "Biến B sẽ trỏ chung vùng nhớ với biến A trên Managed Heap và dùng chung bộ nhớ",
        "B": "Toàn bộ giá trị các trường dữ liệu của A được sao chép theo từng bit sang biến B",
        "C": "Phép gán thất bại ở thời điểm biên dịch vì struct bắt buộc phải dùng hàm Clone()",
        "D": "CLR sẽ tự động sinh ra một con trỏ trung gian để liên kết hai biến với nhau",
        "corr": "B",
        "exp": "Vì struct là Value Type, phép gán giữa hai biến struct là phép sao chép sâu theo giá trị (value copy / bitwise copy). Toàn bộ dữ liệu của biến A được copy độc lập sang ô nhớ của biến B, do đó thay đổi trường dữ liệu của B hoàn toàn không tác động đến A.",
        "diff": "medium", "tag": "Structs"
    },
    # 12
    {
        "q": "Toán tử 'nameof' trong C# mang lại lợi ích kỹ thuật quan trọng nhất nào?",
        "A": "Tự động ép kiểu dữ liệu chuỗi về tên biến tại thời điểm thực thi của chương trình thông qua Reflection",
        "B": "Lấy chuỗi tên định danh tại compile-time, giúp an toàn khi tái cấu trúc mã (Refactoring)",
        "C": "Chuyển đổi một đối tượng phức tạp thành chuỗi JSON chứa toàn bộ dữ liệu của lớp",
        "D": "Định danh địa chỉ ô nhớ vật lý của biến để phục vụ việc debug con trỏ không an toàn",
        "corr": "B",
        "exp": "Toán tử 'nameof' nhận vào một biểu thức (tên biến, tên hàm, tên thuộc tính, tên lớp) và trả về một chuỗi ký tự chứa tên định danh đó ngay tại thời điểm biên dịch. Nhờ đó, nếu chúng ta đổi tên biến bằng công cụ Refactor của IDE, chuỗi tên cũng tự động cập nhật, tránh lỗi runtime gõ sai chính tả chuỗi.",
        "diff": "easy", "tag": "Keywords"
    },
    # 13
    {
        "q": "Phát biểu nào sau đây là ĐÚNG về bộ nhớ cấp phát cho một biến mang kiểu 'string' trong C#?",
        "A": "Biến tham chiếu nằm trên Stack, đối tượng chuỗi ký tự thực tế nằm trên Managed Heap",
        "B": "Cả biến tham chiếu lẫn nội dung mảng ký tự đều luôn luôn được lưu trữ trực tiếp trên vùng nhớ Stack",
        "C": "Nội dung chuỗi ký tự được lưu trữ trực tiếp trong thanh ghi CPU của tiến trình",
        "D": "Chuỗi ký tự trong C# là kiểu giá trị Value Type nên hành xử giống hệt như struct",
        "corr": "A",
        "exp": "Trong C#, 'string' (System.String) là một kiểu tham chiếu (Reference Type) đặc biệt: nó có tính bất biến (immutable). Khi khai báo biến cục bộ string s = 'abc', biến s (con trỏ tham chiếu 4 hoặc 8 bytes) nằm trên Stack, còn đối tượng String thực tế chứa mảng ký tự được cấp phát trên Managed Heap.",
        "diff": "medium", "tag": "Type System"
    },
    # 14
    {
        "q": "Đặc điểm nào sau đây là ĐÚNG về hàm khởi tạo tĩnh (Static Constructor) trong C#?",
        "A": "Có thể có tham số và có phạm vi truy cập public hoặc private tùy ý lập trình viên cấu hình",
        "B": "Không tham số, không access modifier, tự động chạy một lần duy nhất trước khi dùng lớp",
        "C": "Chạy lặp đi lặp lại mỗi khi một đối tượng mới của lớp được tạo ra bằng từ khóa new",
        "D": "Được triệu gọi trực tiếp thông qua cú pháp tên_lớp.Constructor_Tinh() trong mã nguồn",
        "corr": "B",
        "exp": "Static Constructor trong C# không nhận tham số, không có bất kỳ access modifier nào (kể cả public/private). Nó được CLR tự động triệu gọi đúng một lần duy nhất khi lớp được nạp vào bộ nhớ (trước khi tạo thực thể đầu tiên hoặc trước khi truy cập bất kỳ thành viên tĩnh nào của lớp).",
        "diff": "medium", "tag": "Constructors"
    },
    # 15
    {
        "q": "Cơ chế gọi Constructor cha từ Constructor con (Constructor Chaining) trong C# sử dụng từ khóa nào?",
        "A": "this(...) (chỉ dùng để gọi hàm khởi tạo khác trong cùng một lớp hiện tại)",
        "B": "parent(...) (từ khóa đại diện cho lớp cha trong một số ngôn ngữ kịch bản)",
        "C": "super(...) (từ khóa gọi hàm khởi tạo của lớp cha trong ngôn ngữ Java)",
        "D": "base(...) (từ khóa chuẩn trong C# để gọi hàm khởi tạo của lớp cơ sở)",
        "corr": "D",
        "exp": "Trong C#, để chuyển tiếp lời gọi từ hàm khởi tạo của lớp dẫn xuất lên hàm khởi tạo của lớp cơ sở, lập trình viên sử dụng cú pháp `: base(...)`. Để gọi chéo giữa các hàm khởi tạo trong cùng một lớp, lập trình viên sử dụng cú pháp `: this(...)`. (Lưu ý: Java dùng super, C# dùng base).",
        "diff": "easy", "tag": "Constructors"
    },
    # 16
    {
        "q": "Quá trình 'Boxing' trong C# được định nghĩa chính xác là gì?",
        "A": "Chuyển đổi kiểu dữ liệu tham chiếu trên Heap thành kiểu giá trị lưu trên ngăn xếp Stack bộ nhớ",
        "B": "Đóng gói kiểu giá trị (Value Type) thành kiểu tham chiếu (Reference Type) trên Heap",
        "C": "Giải phóng vùng nhớ của đối tượng không còn sử dụng về hệ điều hành quản lý",
        "D": "Nén dữ liệu của một mảng nhiều chiều thành một danh sách liên kết đơn trong RAM",
        "corr": "B",
        "exp": "Boxing là quá trình ngầm định chuyển đổi một biến kiểu giá trị (Value Type - lưu trên Stack) thành kiểu tham chiếu object hoặc interface được cấp phát trên Managed Heap. Quá trình này tốn chi phí CPU để cấp phát bộ nhớ mới trên Heap và sao chép dữ liệu.",
        "diff": "medium", "tag": "Boxing/Unboxing"
    },
    # 17
    {
        "q": "Đoạn mã sau thực hiện thao tác gì và có rủi ro gì?\nobject obj = 123;\nint x = (int)obj;",
        "A": "Dòng 1 là Unboxing, Dòng 2 là Boxing; không có bất kỳ rủi ro nào xảy ra trong chương trình",
        "B": "Dòng 1 là Boxing, Dòng 2 là Unboxing; nếu ép sai kiểu sẽ ném ngoại lệ InvalidCastException",
        "C": "Cả hai dòng đều là Upcasting thuần túy không ảnh hưởng đến hiệu năng của bộ nhớ RAM",
        "D": "Dòng 2 là Downcasting con trỏ thô, có nguy cơ gây tràn bộ nhớ Stack nếu giá trị x quá lớn",
        "corr": "B",
        "exp": "Dòng 1 đưa số nguyên 123 (Value Type) vào hộp object trên Heap -> Boxing. Dòng 2 trích xuất giá trị nguyên từ hộp object ra lại Stack -> Unboxing. Unboxing yêu cầu ép kiểu tường minh. Nếu kiểu được ép không khớp chính xác với kiểu gốc đã đóng hộp (ví dụ ép sang double thay vì int), runtime sẽ ném ra ngoại lệ InvalidCastException.",
        "diff": "medium", "tag": "Boxing/Unboxing"
    },
    # 18
    {
        "q": "Mô hình bộ thu gom rác Garbage Collector (GC) của .NET phân chia các đối tượng thành mấy thế hệ (Generations)?",
        "A": "2 thế hệ: Short-lived (ngắn hạn) và Long-lived (dài hạn) phân chia trên RAM",
        "B": "3 thế hệ: Thế hệ 0 (Gen 0), Thế hệ 1 (Gen 1), và Thế hệ 2 (Gen 2)",
        "C": "4 thế hệ: Stack, Heap, Static và Large Object Heap phân cấp theo kích cỡ đối tượng",
        "D": "5 thế hệ tương ứng với 5 mức độ ưu tiên của luồng đang chạy trong tiến trình",
        "corr": "B",
        "exp": "GC của .NET tổ chức bộ nhớ Heap thành 3 thế hệ (Generations): Gen 0 (chứa các đối tượng ngắn hạn mới tạo), Gen 1 (vùng đệm chứa đối tượng sống sót sau đợt dọn rác ở Gen 0), và Gen 2 (chứa các đối tượng dài hạn và Large Object Heap - LOH). Cách phân chia này dựa trên giả thuyết: đối tượng càng mới thì tỉ lệ chết càng nhanh.",
        "diff": "hard", "tag": "Garbage Collection"
    },
    # 19
    {
        "q": "Mục đích cốt lõi của giao diện IDisposable và phương thức Dispose() trong C# là gì?",
        "A": "Để Garbage Collector biết đối tượng nào cần được nhân bản sang phân vùng Gen 2 của bộ nhớ",
        "B": "Giải phóng kịp thời tài nguyên không quản lý (Unmanaged Resources) như file, socket, DB",
        "C": "Xóa sạch toàn bộ biến tĩnh trong chương trình để chống rò rỉ bộ nhớ khi người dùng tắt app",
        "D": "Bắt buộc hệ điều hành phải dừng toàn bộ các luồng nền đang truy cập vào CPU hiện tại",
        "corr": "B",
        "exp": "Garbage Collector chỉ tự động quản lý bộ nhớ được quản lý (Managed Memory). Với các tài nguyên không được quản lý (Unmanaged Resources như handle file, kết nối DB, socket mạng, con trỏ OS), lập trình viên phải cài đặt IDisposable.Dispose() để người dùng giải phóng chủ động ngay khi dùng xong mà không phải đợi GC kích hoạt Finalizer.",
        "diff": "medium", "tag": "IDisposable"
    },
    # 20
    {
        "q": "Câu lệnh 'using (var stream = new FileStream(...)) { ... }' trong C# tương đương với khối lệnh nào sau đây?",
        "A": "Khối lệnh `try { ... } catch (Exception) { ... }`",
        "B": "Khối lệnh `try { ... } finally { stream?.Dispose(); }`",
        "C": "Khối lệnh đồng bộ khóa luồng `lock (stream) { ... }`",
        "D": "Khối lệnh ghim địa chỉ con trỏ `fixed (stream) { ... }`",
        "corr": "B",
        "exp": "Câu lệnh 'using' là cú pháp đường (syntactic sugar) của khối 'try ... finally'. Khi khối using kết thúc (dù chạy bình thường hay phát sinh ngoại lệ đột ngột), phương thức Dispose() của đối tượng cài đặt IDisposable luôn được đảm bảo gọi trong nhánh finally.",
        "diff": "medium", "tag": "IDisposable"
    },
    # 21
    {
        "q": "Destructor (Finalizer) trong C# có cú pháp và cơ chế hoạt động như thế nào?",
        "A": "Cú pháp `~TenLop()`, do Garbage Collector tự động gọi ngầm định trước khi dọn dẹp",
        "B": "Cú pháp `!TenLop()`, được lập trình viên chủ động gọi thông qua toán tử delete",
        "C": "Cú pháp `delete TenLop()`, chạy đồng bộ ngay khi đối tượng ra khỏi tầm vực biến",
        "D": "Cú pháp `void Finalize()`, bắt buộc phải được khai báo với phạm vi truy cập public",
        "corr": "A",
        "exp": "Trong C#, Destructor được viết dưới dạng `~ClassName()`. Lập trình viên không thể gọi trực tiếp hàm này. Trình biên dịch sẽ chuyển đổi nó thành phương thức Finalize() được ghi đè, và nó sẽ được GC triệu gọi trong một luồng riêng biệt (Finalizer Thread) khi đối tượng bị dọn rác.",
        "diff": "medium", "tag": "Destructor"
    },
    # 22
    {
        "q": "Tại sao các chuyên gia khuyến cáo NÊN HẠN CHẾ viết Finalizer (~ClassName) nếu không thật sự cần thiết?",
        "A": "Finalizer làm đối tượng sống qua ít nhất một chu kỳ GC, làm trì hoãn giải phóng bộ nhớ",
        "B": "Finalizer sẽ khiến chương trình bị crash ngay lập tức khi chạy trên hệ điều hành 64-bit",
        "C": "Khi có Finalizer thì lớp đó không thể khai báo bất kỳ thuộc tính hoặc hàm khởi tạo nào khác",
        "D": "Finalizer ép buộc mọi biến thành viên trong lớp phải được lưu trực tiếp trên ngăn xếp Stack",
        "corr": "A",
        "exp": "Khi một đối tượng có Finalizer, GC không thể thu hồi bộ nhớ của nó ngay trong chu kỳ đầu tiên. Đối tượng sẽ được đưa vào hàng đợi Finalization Queue, sống sót và bị đẩy lên thế hệ cao hơn (Gen 1 hoặc Gen 2). Điều này làm tăng áp lực bộ nhớ và làm chậm tiến trình dọn rác.",
        "diff": "hard", "tag": "Garbage Collection"
    },
    # 23
    {
        "q": "Phương thức `GC.SuppressFinalize(this)` thường được gọi ở đâu và nhằm mục đích gì?",
        "A": "Được gọi trong Constructor để ngăn GC không cho phép thu gom đối tượng này trong tương lai",
        "B": "Gọi trong Dispose() để báo GC bỏ qua Finalizer vì tài nguyên đã giải phóng chủ động",
        "C": "Được gọi trong hàm Main để tăng tốc độ khởi động của toàn bộ ứng dụng phần mềm máy tính",
        "D": "Được gọi trước mỗi phép toán Boxing để ngăn việc cấp phát vùng nhớ mới trên bộ nhớ Heap",
        "corr": "B",
        "exp": "Trong mẫu thiết kế chuẩn Dispose Pattern, khi người dùng đã chủ động gọi Dispose() để dọn sạch tài nguyên, việc gọi `GC.SuppressFinalize(this)` sẽ thông báo cho CLR không cần đưa đối tượng vào Finalization Queue nữa. Nhờ vậy, đối tượng có thể được giải phóng ngay ở chu kỳ GC tiếp theo, tối ưu tài nguyên tối đa.",
        "diff": "hard", "tag": "IDisposable"
    },
    # 24
    {
        "q": "Trong C#, nếu một lớp có nhiều Constructor, làm thế nào để một Constructor tái sử dụng mã nguồn của Constructor khác trong cùng lớp?",
        "A": "Tự động gọi lại tên hàm Init() bên trong thân của từng hàm khởi tạo của lớp",
        "B": "Sử dụng cú pháp `: this(...)` ngay sau phần khai báo danh sách tham số Constructor",
        "C": "Dùng từ khóa new để tạo một thực thể tạm thời rồi sao chép toàn bộ dữ liệu của đối tượng sang",
        "D": "Sử dụng từ khóa self.Constructor(...) trong dòng đầu tiên của thân hàm khởi tạo",
        "corr": "B",
        "exp": "Kỹ thuật gọi chéo hàm khởi tạo trong cùng một lớp được gọi là Constructor Chaining. Cú pháp chuẩn của C# là đặt dấu hai chấm kèm theo `: this(các_tham_số)` trước khi mở dấu ngoặc nhọn `{` của thân Constructor.",
        "diff": "easy", "tag": "Constructors"
    },
    # 25
    {
        "q": "Điều gì xảy ra nếu lập trình viên không khai báo bất kỳ Constructor nào cho một class?",
        "A": "Báo lỗi biên dịch nghiêm trọng vì mọi class đều bắt buộc phải có ít nhất một Constructor do người viết",
        "B": "Trình biên dịch tự động cung cấp Constructor mặc định công khai không tham số",
        "C": "Lớp đó sẽ trở thành static class và không thể tạo instance bằng từ khóa new được nữa",
        "D": "Tất cả các trường dữ liệu của lớp đó sẽ không bao giờ được cấp phát bộ nhớ trong RAM",
        "corr": "B",
        "exp": "Nếu một class không có bất kỳ constructor nào do lập trình viên định nghĩa, C# compiler sẽ tự động chèn một constructor mặc định public không tham số, trong đó các trường dữ liệu được khởi tạo về giá trị mặc định của kiểu (0, false, null).",
        "diff": "easy", "tag": "Constructors"
    },
    # 26
    {
        "q": "Nếu đã định nghĩa một Constructor có tham số, ví dụ `public SinhVien(string ma, string ten)`, muốn dùng `new SinhVien()` thì phải làm gì?",
        "A": "Khai báo tường minh thêm một Constructor không tham số `public SinhVien() { }`",
        "B": "Không cần làm gì cả vì trình biên dịch vẫn luôn giữ lại Constructor mặc định ẩn cho lớp",
        "C": "Chỉ cần đánh dấu từ khóa virtual trước Constructor có tham số đã khai báo trước đó",
        "D": "Phải ép kiểu đối tượng về kiểu System.Object trước khi thực hiện gọi lệnh new khởi tạo",
        "corr": "A",
        "exp": "Quy tắc của C#: một khi lập trình viên đã viết bất kỳ Constructor nào (dù có tham số hay không), trình biên dịch sẽ KHÔNG tự động sinh ra Constructor mặc định nữa. Do đó, nếu muốn sử dụng Constructor không tham số, lập trình viên buộc phải tự tay khai báo nó.",
        "diff": "easy", "tag": "Constructors"
    },
    # 27
    {
        "q": "Lợi ích chính của việc sử dụng Property (Thuộc tính) thay vì trường công khai (public field) trong C# là gì?",
        "A": "Kiểm soát logic đọc/ghi, kiểm tra tính hợp lệ dữ liệu và duy trì tính đóng gói",
        "B": "Tăng tốc độ truy xuất dữ liệu lên gấp đôi do bỏ qua việc cấp phát vùng nhớ trên Managed Heap",
        "C": "Cho phép biến dữ liệu có thể được truy cập trực tiếp từ các tiến trình ngoài hệ điều hành",
        "D": "Ngăn không cho các lớp con kế thừa trường dữ liệu này trong toàn bộ dự án phần mềm",
        "corr": "A",
        "exp": "Property cung cấp cơ chế getter/setter linh hoạt, cho phép ta cài đặt các logic kiểm tra dữ liệu đầu vào (validation), tính toán giá trị động, đặt phạm vi truy cập khác nhau cho đọc và ghi (ví dụ `public int Id { get; private set; }`), bảo vệ tính toàn vẹn trạng thái nội bộ của đối tượng.",
        "diff": "easy", "tag": "Encapsulation"
    },
    # 28
    {
        "q": "Trong C# 9.0+, kiểu dữ liệu 'record' (hoặc 'record class') chủ yếu được thiết kế nhằm mục đích gì?",
        "A": "Mô hình hóa dữ liệu bất biến với cơ chế so sánh theo giá trị (value-based equality)",
        "B": "Thay thế hoàn toàn cấu trúc struct để tăng tốc độ thực thi cho các phép tính số thực lớn",
        "C": "Tự động đồng bộ hóa dữ liệu giữa bộ nhớ RAM và cơ sở dữ liệu quan hệ SQL Server từ xa",
        "D": "Cung cấp khả năng đa kế thừa từ nhiều lớp cha khác nhau mà không thông qua giao diện interface",
        "corr": "A",
        "exp": "Record trong C# mang lại 2 đặc trưng quan trọng: tính bất biến (Immutability) khi kết hợp với positional parameters/init properties, và cơ chế so sánh giá trị (Value Equality) tự động: 2 thực thể record có các trường bằng nhau sẽ được coi là bằng nhau (khác với class thông thường so sánh theo tham chiếu địa chỉ).",
        "diff": "medium", "tag": "Record"
    },
    # 29
    {
        "q": "Cú pháp nào sau đây thể hiện đột biến không phá hủy (non-destructive mutation) trên một record trong C#?",
        "A": "var p2 = p1 with { Age = 25 }; (sử dụng biểu thức with để tạo bản sao cập nhật)",
        "B": "var p2 = clone(p1) { Age = 25 }; (sử dụng hàm clone của đối tượng để sao chép)",
        "C": "var p2 = p1.Copy().SetAge(25); (sử dụng chuỗi phương thức sao chép truyền thống)",
        "D": "var p2 = new p1(Age: 25); (sử dụng hàm khởi tạo đặc biệt với tham số đặt tên)",
        "corr": "A",
        "exp": "Biểu thức `with` (With-expression) cho phép tạo ra một bản sao mới của đối tượng record hiện có nhưng có thể thay đổi một vài thuộc tính chỉ định, trong khi đối tượng gốc vẫn giữ nguyên trạng thái bất biến của nó.",
        "diff": "medium", "tag": "Record"
    },
    # 30
    {
        "q": "Indexer trong C# cho phép một đối tượng hoạt động giống như cấu trúc nào sau đây?",
        "A": "Giống như một hàm bất đồng bộ có thể await ở bất kỳ đâu trong chu trình thực thi",
        "B": "Giống như một con trỏ hàm trong C++ để gọi hàm callback phản hồi sự kiện hệ thống",
        "C": "Giống một mảng, cho phép truy cập phần tử qua toán tử chỉ mục ngoặc vuông `[]`",
        "D": "Giống như một khối lệnh try-catch để tự động bắt lỗi cú pháp tại thời điểm biên dịch",
        "corr": "C",
        "exp": "Indexer cho phép các thực thể của một lớp hoặc cấu trúc có thể được truy xuất theo chỉ mục tương tự như mảng thông qua cú pháp `this[...]`. Cú pháp khai báo phổ biến: `public T this[int index] { get { ... } set { ... } }`.",
        "diff": "easy", "tag": "Indexers"
    },
    # 31
    {
        "q": "Phát biểu nào sau đây là ĐÚNG về so sánh bằng nhau giữa hai đối tượng `record` trong C#?",
        "A": "Hai đối tượng record chỉ bằng nhau khi chúng trỏ tới cùng một địa chỉ ô nhớ trên Heap",
        "B": "Hai record bằng nhau nếu cùng kiểu và tất cả thuộc tính tương ứng bằng nhau về giá trị",
        "C": "Không thể sử dụng toán tử `==` để so sánh hai record mà bắt buộc phải dùng hàm ReferenceEquals",
        "D": "Phép so sánh hai record luôn trả về false nếu chúng được khởi tạo từ hai dòng mã khác nhau",
        "corr": "B",
        "exp": "Trình biên dịch tự động sinh mã ghi đè phương thức Equals() và nạp chồng toán tử `==` cho kiểu record dựa trên giá trị của các trường (Value-based equality), thay vì so sánh địa chỉ tham chiếu (Reference equality) như class thông thường.",
        "diff": "medium", "tag": "Record"
    },
    # 32
    {
        "q": "Auto-implemented Property `public string Name { get; }` (chỉ có get, không có set) có thể được gán giá trị ở đâu?",
        "A": "Ở bất kỳ phương thức nào bên trong lớp nhưng phải thông qua từ khóa this để định danh",
        "B": "Chỉ tại nơi khai báo thuộc tính hoặc bên trong Constructor của lớp đó",
        "C": "Ở bất kỳ đâu kể cả bên ngoài lớp nếu truyền tham số qua con trỏ tham chiếu ref",
        "D": "Chỉ có thể được gán tự động bởi Garbage Collector khi nạp đối tượng vào bộ nhớ Heap",
        "corr": "B",
        "exp": "Một read-only auto-property (chỉ có getter) được bảo vệ chặt chẽ: nó chỉ có thể nhận giá trị khởi tạo ngay tại dòng khai báo hoặc bên trong Constructor của chính lớp đó. Sau khi constructor hoàn tất, giá trị không thể thay đổi.",
        "diff": "easy", "tag": "Properties"
    },
    # 33
    {
        "q": "Trong C#, backing field của một Auto-implemented Property là gì?",
        "A": "Trường biến private ẩn do trình biên dịch tự động tạo ra để lưu trữ giá trị property",
        "B": "File cấu hình XML lưu trữ trạng thái của lớp trên ổ đĩa cứng của hệ điều hành máy tính",
        "C": "Biến toàn cục được chia sẻ chung cho tất cả các luồng trong ứng dụng đang chạy hiện hành",
        "D": "Hằng số được nhúng trực tiếp vào bảng biểu tượng thời điểm biên dịch mã trung gian MSIL",
        "corr": "A",
        "exp": "Khi ta khai báo Auto-Property như `public int Age { get; set; }`, trình biên dịch C# sẽ tự động sinh ra một trường biến private ẩn mang tên dạng `<Age>k__BackingField` trong mã MSIL để lưu trữ dữ liệu thực sự cho thuộc tính đó.",
        "diff": "medium", "tag": "Properties"
    },
    # 34
    {
        "q": "Khi nào lập trình viên BẮT BUỘC phải dùng Full Property (có backing field tường minh) thay vì Auto-Property?",
        "A": "Khi muốn thuộc tính có phạm vi truy cập là public cho cả việc đọc và ghi dữ liệu ra vào",
        "B": "Khi cần bổ sung logic kiểm tra (validation), logging hoặc tính toán trong get/set",
        "C": "Khi lớp đó kế thừa từ một interface có chứa khai báo thuộc tính tương ứng của giao diện",
        "D": "Khi muốn đối tượng được cấp phát trên bộ nhớ Stack thay vì vùng nhớ Managed Heap",
        "corr": "B",
        "exp": "Auto-property chỉ đơn thuần lưu và đọc giá trị. Khi cần thêm logic tùy biến như kiểm tra dữ liệu đầu vào (ví dụ: `if (value < 0) throw new ArgumentException()`), kích hoạt sự kiện thông báo thay đổi (INotifyPropertyChanged), hay tính toán giá trị lười (lazy loading), ta bắt buộc phải dùng Full Property với backing field tường minh.",
        "diff": "easy", "tag": "Properties"
    },
    # 35
    {
        "q": "Đoạn mã sau mang ý nghĩa gì trong C#?\n`public string Title { get; set; } = \"Chưa đặt tên\";`",
        "A": "Gán giá trị khởi tạo mặc định cho property ngay tại thời điểm khởi tạo đối tượng",
        "B": "Ép buộc mọi lớp con phải ghi đè thuộc tính này với giá trị là Chưa đặt tên khi kế thừa",
        "C": "Khởi tạo một biến hằng số tĩnh không thể thay đổi trong suốt vòng đời của ứng dụng phần mềm",
        "D": "Tự động chuyển đổi thuộc tính này thành kiểu struct để tối ưu hóa bộ nhớ ngăn xếp Stack",
        "corr": "A",
        "exp": "Đây là cú pháp Property Initializer (giới thiệu từ C# 6.0), cho phép gán giá trị khởi tạo mặc định cho Auto-Property trực tiếp ngay tại vị trí khai báo, giúp mã nguồn gọn gàng mà không cần viết tường minh trong constructor.",
        "diff": "easy", "tag": "Properties"
    },
    # 36
    {
        "q": "Kiểu dữ liệu 'record struct' (từ C# 10) khác với 'record class' ở điểm cơ bản nào?",
        "A": "record struct là kiểu giá trị lưu trên Stack, còn record class là kiểu tham chiếu trên Heap",
        "B": "record struct không hỗ trợ biểu thức with, còn record class thì hỗ trợ đầy đủ cú pháp bất biến này",
        "C": "record struct không hỗ trợ cơ chế so sánh bằng nhau dựa trên giá trị các trường dữ liệu",
        "D": "record struct có thể kế thừa từ nhiều struct khác còn record class thì không thể kế thừa",
        "corr": "A",
        "exp": "C# 10 bổ sung `record struct`: nó kết hợp các ưu điểm của struct (Value Type, cấp phát bộ nhớ nhanh trên Stack, không sinh rác cho GC) với các tiện ích của record (tự sinh ToString(), so sánh giá trị, hỗ trợ with-expression). Trong khi đó `record` mặc định (hoặc `record class`) là Reference Type trên Heap.",
        "diff": "hard", "tag": "Record"
    },
    # 37
    {
        "q": "Từ khóa 'required' (từ C# 11) trước một property có tác dụng gì khi khởi tạo đối tượng?",
        "A": "Bắt buộc người tạo đối tượng phải gán giá trị cho nó qua Constructor hoặc Initializer",
        "B": "Bắt buộc thuộc tính đó không bao giờ được phép mang giá trị rỗng hoặc khoảng trắng vô nghĩa",
        "C": "Bắt buộc Garbage Collector phải giải phóng thuộc tính đó ngay khi đối tượng ra khỏi scope",
        "D": "Bắt buộc thuộc tính phải được bảo vệ bởi khóa lock để đảm bảo an toàn đa luồng tuyệt đối",
        "corr": "A",
        "exp": "Modifier 'required' (C# 11) đảm bảo tính toàn vẹn dữ liệu: buộc người gọi khi tạo đối tượng bằng cú pháp Object Initializer `{ Prop = val }` hoặc qua constructor phải cung cấp giá trị cho thuộc tính đó, nếu quên trình biên dịch sẽ báo lỗi ngay lập tức.",
        "diff": "medium", "tag": "Properties"
    },
    # 38
    {
        "q": "Thuộc tính chỉ có get `public double DienTich => Dai * Rong;` sử dụng cú pháp gì trong C#?",
        "A": "Lambda Expression cho hàm khởi tạo mặc định của lớp",
        "B": "Expression-bodied Property (thuộc tính dạng biểu thức)",
        "C": "Hàm nạp chồng toán tử nhân hai số thực trên bộ nhớ Stack",
        "D": "Khối lệnh đồng bộ hóa dữ liệu đa luồng một cách tự động",
        "corr": "B",
        "exp": "Cú pháp `=>` (Expression-bodied member) cho phép viết các thuộc tính chỉ đọc (read-only getter) hoặc các phương thức đơn giản trên một dòng biểu thức duy nhất, giúp code trực quan, súc tích và dễ đọc.",
        "diff": "easy", "tag": "Properties"
    },
    # 39
    {
        "q": "C# hỗ trợ hình thức đa kế thừa (Multiple Inheritance) nào sau đây đối với class?",
        "A": "Cho phép một class kế thừa trực tiếp từ nhiều class cha cùng một lúc trong khai báo",
        "B": "Chỉ đơn kế thừa một class cha, nhưng có thể cài đặt nhiều interface cùng lúc",
        "C": "Không hỗ trợ kế thừa bất kỳ hình thức nào để đảm bảo tính toàn vẹn an toàn dữ liệu",
        "D": "Cho phép một struct kế thừa từ một class và nhiều struct cha khác cùng một thời điểm",
        "corr": "B",
        "exp": "C# tuân thủ nguyên lý Đơn kế thừa (Single Inheritance) đối với lớp để loại trừ bài toán kim cương (Diamond Problem). Một lớp con chỉ được có duy nhất một lớp cha trực tiếp, nhưng được phép triển khai (implement) đồng thời không giới hạn số lượng giao diện (interfaces).",
        "diff": "easy", "tag": "Inheritance"
    },
    # 40
    {
        "q": "Toán tử 'as' trong C# thực hiện việc ép kiểu tham chiếu như thế nào khi quá trình ép kiểu thất bại?",
        "A": "Ném ra ngoại lệ InvalidCastException làm ngắt quãng chu trình chạy của ứng dụng",
        "B": "Trả về giá trị null mà không gây phát sinh ngoại lệ đột ngột trong chương trình",
        "C": "Khởi tạo một đối tượng rỗng mặc định của kiểu đích trên phân vùng Managed Heap",
        "D": "Tự động ép kiểu cưỡng bức các bit dữ liệu thô về giá trị 0 trên bộ nhớ hệ thống",
        "corr": "B",
        "exp": "Toán tử 'as' dùng để ép kiểu an toàn giữa các kiểu tham chiếu hoặc nullable. Nếu việc ép kiểu không tương thích, thay vì văng ngoại lệ InvalidCastException làm đổ vỡ chương trình như cách ép kiểu truyền thống `(Type)obj`, toán tử 'as' sẽ trả về null một cách êm đẹp.",
        "diff": "medium", "tag": "Type Casting"
    },
    # 41
    {
        "q": "Cú pháp Pattern Matching `if (obj is SinhVien sv)` trong C# 7.0+ thực hiện những hành động nào?",
        "A": "Kiểm tra xem obj có phải SinhVien không; nếu đúng thì gán vào biến mới sv và trả về true",
        "B": "Chỉ kiểm tra kiểu của obj nhưng không thể khai báo thêm biến mới trong câu lệnh điều kiện if",
        "C": "Ép kiểu cưỡng bức obj về SinhVien; nếu sai kiểu sẽ tự ném ra ngoại lệ SystemException",
        "D": "Chuyển đổi kiểu dữ liệu của biến obj từ Reference Type thành Value Type trên vùng nhớ Stack",
        "corr": "A",
        "exp": "Cú pháp Pattern Matching kết hợp toán tử 'is' vừa kiểm tra tính tương thích kiểu dữ liệu (tương tự như `obj is SinhVien`), vừa tự động ép kiểu và gán đối tượng vào một biến cục bộ mới `sv` trong phạm vi của khối lệnh nếu điều kiện thỏa mãn, loại bỏ nhu cầu ép kiểu thủ công dòng tiếp theo.",
        "diff": "medium", "tag": "Type Casting"
    },
    # 42
    {
        "q": "Khái niệm 'Upcasting' (ép kiểu ngược lên) trong hệ thống phân cấp kế thừa C# có đặc điểm gì?",
        "A": "Chuyển tham chiếu lớp con về kiểu lớp cha, luôn luôn an toàn và diễn ra ngầm định",
        "B": "Chuyển tham chiếu từ lớp cha xuống lớp con, tiềm ẩn rủi ro ném lỗi InvalidCastException",
        "C": "Bắt buộc phải sử dụng toán tử ép kiểu tường minh `(ChildClass)parentObj` trong mã nguồn",
        "D": "Chỉ thực hiện được khi hai lớp có chung một biến static mang kiểu dữ liệu nguyên thủy",
        "corr": "A",
        "exp": "Upcasting là việc gán tham chiếu của một đối tượng thuộc lớp con cho biến thuộc kiểu lớp cha (ví dụ `Animal a = new Dog();`). Phép chuyển đổi này luôn an toàn và hợp lệ vì con luôn có đầy đủ đặc tính của cha (quan hệ IS-A), do đó C# cho phép thực hiện ngầm định (implicit conversion) mà không cần ép kiểu.",
        "diff": "easy", "tag": "Inheritance"
    },
    # 43
    {
        "q": "Khái niệm 'Downcasting' (ép kiểu xuôi xuống) có đặc điểm và điều kiện thực hiện nào?",
        "A": "Ép biến kiểu cha xuống kiểu con; chỉ thành công nếu thực thể thực tế trên Heap đúng là kiểu con",
        "B": "Luôn luôn thành công trong mọi trường hợp mà không cần bất kỳ sự kiểm tra nào tại thời điểm chạy",
        "C": "Không bao giờ được phép thực hiện trong C# vì vi phạm an toàn của hệ thống kiểu dữ liệu tĩnh",
        "D": "Chỉ có tác dụng đối với các biến kiểu int và float khi chuyển đổi qua lại trên ngăn xếp Stack",
        "corr": "A",
        "exp": "Downcasting là việc ép một biến tham chiếu kiểu lớp cha xuống kiểu lớp con. Phép này đòi hỏi ép kiểu tường minh. Tại runtime, CLR sẽ kiểm tra kiểu thực tế của đối tượng trên Heap; nếu đối tượng thực tế không phải là lớp con đó (hoặc lớp dẫn xuất của nó), CLR sẽ ném ra ngoại lệ InvalidCastException.",
        "diff": "medium", "tag": "Inheritance"
    },
    # 44
    {
        "q": "Từ khóa 'sealed' đặt trước khai báo một phương thức `override` mang ý nghĩa gì?",
        "A": "Ngăn không cho bất kỳ lớp con nào kế thừa tiếp theo được phép ghi đè phương thức này nữa",
        "B": "Bắt buộc các lớp con phải tiếp tục ghi đè phương thức này bằng từ khóa new thay thế vào",
        "C": "Biến phương thức thành hàm tĩnh có thể truy cập mà không cần tạo thực thể đối tượng cụ thể",
        "D": "Xóa bỏ hoàn toàn định nghĩa của phương thức khỏi bảng phương thức ảo (vtable) của lớp con",
        "corr": "A",
        "exp": "Khi một phương thức được đánh dấu là `sealed override`, nó cho biết phương thức này là phiên bản ghi đè cuối cùng trong chuỗi kế thừa. Các lớp dẫn xuất tiếp theo từ lớp này sẽ bị cấm không được phép tiếp tục `override` phương thức này nữa.",
        "diff": "medium", "tag": "Inheritance"
    },
    # 45
    {
        "q": "Mối quan hệ giữa lớp 'XeHoi' và lớp 'DongCo' trong thiết kế hướng đối tượng nên là quan hệ nào?",
        "A": "IS-A (Kế thừa - XeHoi kế thừa DongCo) vì xe hơi là một loại động cơ chuyển động trên mặt đất",
        "B": "HAS-A (Chứa gộp / Composition) vì một chiếc xe hơi chứa đựng một động cơ bên trong",
        "C": "Đa hình đồng mức (Polymorphism) thông qua việc nạp chồng các toán tử cộng trừ hai ngôi",
        "D": "Quan hệ bạn bè (Friendship) chia sẻ toàn bộ con trỏ ô nhớ trực tiếp trên bộ nhớ hệ thống",
        "corr": "B",
        "exp": "Xe hơi KHÔNG PHẢI là một động cơ (không thỏa mãn quan hệ IS-A để dùng kế thừa), mà Xe hơi CÓ một động cơ (thỏa mãn quan hệ HAS-A). Do đó, áp dụng nguyên lý 'Composition over Inheritance' (Ưu tiên chứa gộp hơn kế thừa) là lựa chọn chuẩn xác nhất.",
        "diff": "easy", "tag": "OOP Principles"
    },
    # 46
    {
        "q": "Từ khóa 'base' trong một phương thức của lớp con được dùng để làm gì?",
        "A": "Gọi đến việc thực thi phiên bản của phương thức đó ở lớp cha trực tiếp",
        "B": "Xóa sạch đối tượng lớp con để phục hồi lại trạng thái ban đầu của lớp cha trên Heap",
        "C": "Tạo ra một bản sao hoàn toàn mới của lớp cha trên phân vùng Large Object Heap của GC",
        "D": "Ép buộc luồng hiện tại phải tạm dừng cho đến khi lớp cha xử lý xong tác vụ tính toán",
        "corr": "A",
        "exp": "Từ khóa 'base' đại diện cho tham chiếu tới lớp cơ sở của đối tượng hiện tại. Trong thân phương thức ghi đè của lớp con, ta thường dùng `base.MethodName()` để tái sử dụng lại phần xử lý logic đã được định nghĩa ở lớp cha trước khi mở rộng thêm logic riêng của lớp con.",
        "diff": "easy", "tag": "Inheritance"
    },
    # 47
    {
        "q": "Khi lớp con kế thừa từ lớp cha, thứ tự thực thi của các Constructor khi tạo đối tượng con là gì?",
        "A": "Constructor của lớp con chạy trước, sau đó mới gọi ngược lên Constructor của lớp cha",
        "B": "Constructor của lớp cha chạy hoàn tất trước, sau đó mới đến Constructor của lớp con",
        "C": "Cả hai Constructor chạy song song đồng thời trên hai luồng khác nhau của hệ thống máy",
        "D": "Chỉ duy nhất Constructor của lớp con chạy, Constructor của lớp cha bị bỏ qua hoàn toàn",
        "corr": "B",
        "exp": "Quy tắc khởi tạo đối tượng trong C#: nền tảng cơ sở phải được xây dựng vững chắc trước. Do đó, CLR sẽ triệu gọi Constructor của lớp cha (từ gốc System.Object lần lượt xuống các cấp cha trung gian) để khởi tạo đầy đủ các thành viên lớp cơ sở trước, rồi mới bắt đầu thực thi phần thân Constructor của lớp con.",
        "diff": "medium", "tag": "Inheritance"
    },
    # 48
    {
        "q": "Lớp con KHÔNG THỂ truy cập thành viên nào sau đây được khai báo trong lớp cha?",
        "A": "Thành viên mang phạm vi truy cập protected bên trong nội bộ lớp",
        "B": "Thành viên mang phạm vi truy cập public được công khai ra ngoài",
        "C": "Thành viên mang phạm vi truy cập private bị đóng gói nội bộ",
        "D": "Thành viên mang phạm vi truy cập internal trong cùng Assembly",
        "corr": "C",
        "exp": "Thành viên private của một lớp bị đóng gói tuyệt đối bên trong lớp đó. Mặc dù khi kế thừa, đối tượng lớp con trong bộ nhớ vẫn chứa ô nhớ của biến private đó, nhưng mã nguồn của lớp con hoàn toàn không có quyền truy cập trực tiếp bằng tên biến.",
        "diff": "easy", "tag": "Encapsulation"
    },
    # 49
    {
        "q": "Mục đích của việc sử dụng từ khóa 'sealed' trước khai báo một class là gì?",
        "A": "Cho phép lớp được kế thừa bởi nhiều lớp con trong cùng Assembly nhưng cấm ở bên ngoài",
        "B": "Ngăn cấm không cho bất kỳ lớp nào khác được phép kế thừa từ lớp này (chống mở rộng)",
        "C": "Bắt buộc tất cả các phương thức trong lớp phải được triển khai dưới dạng hàm trừu tượng",
        "D": "Chuyển đổi toàn bộ các biến trong lớp thành kiểu dữ liệu chỉ đọc cấp phát trên Stack",
        "corr": "B",
        "exp": "Từ khóa 'sealed' ngăn chặn việc kế thừa. Lý do thiết kế: bảo vệ tính bảo mật, ngăn ngừa việc các lớp con can thiệp/phá vỡ hành vi dự kiến ban đầu, hoặc tối ưu hiệu năng gọi hàm (Devirtualization) vì JIT compiler biết chắc chắn không có lớp con nào ghi đè.",
        "diff": "easy", "tag": "Inheritance"
    },
    # 50
    {
        "q": "Nếu lớp cha có phương thức `public void Show()`, lớp con cũng viết `public void Show()` mà không có từ khóa nào đi kèm, kết quả biên dịch là gì?",
        "A": "Báo lỗi biên dịch nghiêm trọng và không thể sinh ra file mã nhị phân thực thi cho ứng dụng phần mềm",
        "B": "Biên dịch thành công kèm cảnh báo (warning), phương thức con sẽ ẩn (hide) phương thức cha",
        "C": "Phương thức của con sẽ tự động ghi đè (override) phương thức của cha tại thời điểm chạy",
        "D": "Phương thức của cha sẽ tự động bị xóa bỏ vĩnh viễn khỏi bảng mã trung gian MSIL của file",
        "corr": "B",
        "exp": "Khi lớp con định nghĩa một phương thức trùng tên và danh sách tham số với lớp cha mà không dùng 'override' hay 'new', trình biên dịch sẽ cảnh báo bạn đang vô tình 'ẩn' (hide) phương thức của cha. Để xóa cảnh báo và báo rõ ý định, lập trình viên nên thêm từ khóa 'new'.",
        "diff": "medium", "tag": "Inheritance"
    }
]

print(f"Part 1 contains {len(questions_part1)} questions.")
