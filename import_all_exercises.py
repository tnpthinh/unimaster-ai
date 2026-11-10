"""
Import all 10 OOP C# exercises and additional questions 51-100 from user's React code
"""
import sqlite3
import json
from database import add_exercise, add_question, get_connection

exercises_data = [
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
    "problem": "Trung tâm đăng kiểm xe cơ giới quản lý 02 loại phương tiện phổ biến: Xe ô tô con (Car) và Xe tải vận tải (Truck). Mỗi loại phương tiện có cách tính chi phí đăng kiểm và phí sử dụng đường bộ hàng năm khác nhau dựa trên dung tích động cơ hoặc tải trọng.",
    "specs": [
      "A. Lớp cơ sở trừu tượng PhuongTien: BiSoXe (string), HangSanXuat (string), NamSanXuat (int), GiaTriXe (double >= 0). Phương thức: public abstract double TinhPhiDangKiem(), public virtual void NhapThongTin(), public virtual void InThongTin().",
      "B1. Lớp Car (Kế thừa PhuongTien): Bổ sung SoChoNgoi (int). TinhPhiDangKiem() = 340,000 + (SoChoNgoi > 5 ? 100,000 : 50,000) VND.",
      "B2. Lớp Truck (Kế thừa PhuongTien): Bổ sung TaiTrongTan (double). TinhPhiDangKiem() = 500,000 + (TaiTrongTan * 80,000) VND.",
      "C. Hàm Main: Tạo 01 Car và 01 Truck. Đưa vào List<PhuongTien>, duyệt InThongTin(), tính tổng phí đăng kiểm và tìm xe có phí cao nhất."
    ],
    "sampleCode": """abstract class PhuongTien
{
    public string BiSoXe { get; set; }
    public string HangSanXuat { get; set; }
    public int NamSanXuat { get; set; }
    public double GiaTriXe { get; set; }
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
  },
  {
    "id": 3,
    "title": "BÀI TẬP 3: QUẢN LÝ TÀI KHOẢN NGÂN HÀNG VÀ TÍNH LÃI PHÍ (BANK ACCOUNT)",
    "problem": "Một ngân hàng thương mại áp dụng chính sách quản lý giao dịch đối với 02 loại tài khoản: Tài khoản thanh toán (CheckingAccount) và Tài khoản tiết kiệm (SavingsAccount).",
    "specs": [
      "A. Lớp cơ sở trừu tượng TaiKhoan: SoTaiKhoan (string), TenChuTaiKhoan (string), SoDu (double >= 0). Phương thức: public abstract double TinhGiaTriPhatSinh(), InThongTin().",
      "B1. Lớp CheckingAccount: Bổ sung PhiGiaoDichHangThang. TinhGiaTriPhatSinh() = -PhiGiaoDichHangThang.",
      "B2. Lớp SavingsAccount: Bổ sung LaiSuatNam, KyHanThang. TinhGiaTriPhatSinh() = SoDu * (LaiSuatNam / 100.0) * (KyHanThang / 12.0)."
    ],
    "sampleCode": """abstract class TaiKhoan
{
    public string SoTaiKhoan { get; set; }
    public string TenChuTaiKhoan { get; set; }
    public double SoDu { get; set; }
    public abstract double TinhGiaTriPhatSinh();
}

class CheckingAccount : TaiKhoan
{
    public double PhiGiaoDichHangThang { get; set; }
    public override double TinhGiaTriPhatSinh() => -PhiGiaoDichHangThang;
}

class SavingsAccount : TaiKhoan
{
    public double LaiSuatNam { get; set; }
    public int KyHanThang { get; set; }
    public override double TinhGiaTriPhatSinh() => SoDu * (LaiSuatNam / 100.0) * (KyHanThang / 12.0);
}"""
  },
  {
    "id": 4,
    "title": "BÀI TẬP 4: QUẢN LÝ SẢN PHẨM KHU THƯƠNG MẠI (PRODUCT MANAGEMENT)",
    "problem": "Một siêu thị kinh doanh 02 mặt hàng chính: Hàng thực phẩm tươi sống (FoodProduct) và Hàng điện máy gia dụng (ApplianceProduct).",
    "specs": [
      "A. Lớp cơ sở trừu tượng SanPham: MaSP, TenSP, GiaGoc, SoLuongTon. Phương thức: TinhGiaBan().",
      "B1. Lớp FoodProduct: Bổ sung PhiBaoQuanLanh. TinhGiaBan() = GiaGoc * 1.15 + PhiBaoQuanLanh.",
      "B2. Lớp ApplianceProduct: Bổ sung ThoiGianBaoHanhThang, PhiBaoHanh. TinhGiaBan() = GiaGoc * 1.25 + PhiBaoHanh."
    ],
    "sampleCode": """abstract class SanPham
{
    public string MaSP { get; set; }
    public string TenSP { get; set; }
    public double GiaGoc { get; set; }
    public int SoLuongTon { get; set; }
    public abstract double TinhGiaBan();
}

class FoodProduct : SanPham
{
    public double PhiBaoQuanLanh { get; set; }
    public override double TinhGiaBan() => GiaGoc * 1.15 + PhiBaoQuanLanh;
}

class ApplianceProduct : SanPham
{
    public int ThoiGianBaoHanhThang { get; set; }
    public double PhiBaoHanh { get; set; }
    public override double TinhGiaBan() => GiaGoc * 1.25 + PhiBaoHanh;
}"""
  },
  {
    "id": 5,
    "title": "BÀI TẬP 5: QUẢN LÝ VẬN CHUYỂN BƯU PHẨM LOGISTICS (PACKAGE DELIVERY)",
    "problem": "Một công ty dịch vụ chuyển phát nhanh quản lý 02 loại bưu gửi: Bưu phẩm tiêu chuẩn (StandardPackage) và Bưu phẩm hỏa tốc (ExpressPackage).",
    "specs": [
      "A. Lớp cơ sở trừu tượng BuuGui: MaDonHang, NguoiNhan, TrongLuongKg, KhoangCachKm. Phương thức: TinhCuocVanChuyen().",
      "B1. Lớp StandardPackage: Bổ sung DonGiaKg. TinhCuocVanChuyen() = (TrongLuongKg * DonGiaKg) + (KhoangCachKm * 1,500).",
      "B2. Lớp ExpressPackage: Bổ sung PhiHoaTocCoDinh. TinhCuocVanChuyen() = (TrongLuongKg * 15,000) + (KhoangCachKm * 3,000) + PhiHoaTocCoDinh."
    ],
    "sampleCode": """abstract class BuuGui
{
    public string MaDonHang { get; set; }
    public string NguoiNhan { get; set; }
    public double TrongLuongKg { get; set; }
    public double KhoangCachKm { get; set; }
    public abstract double TinhCuocVanChuyen();
}

class StandardPackage : BuuGui
{
    public double DonGiaKg { get; set; }
    public override double TinhCuocVanChuyen() => (TrongLuongKg * DonGiaKg) + (KhoangCachKm * 1500);
}

class ExpressPackage : BuuGui
{
    public double PhiHoaTocCoDinh { get; set; }
    public override double TinhCuocVanChuyen() => (TrongLuongKg * 15000) + (KhoangCachKm * 3000) + PhiHoaTocCoDinh;
}"""
  },
  {
    "id": 6,
    "title": "BÀI TẬP 6: QUẢN LÝ ĐỘC GIẢ VÀ PHÍ THƯ VIỆN (LIBRARY READER MANAGEMENT)",
    "problem": "Thư viện trung tâm phục vụ 02 đối tượng độc giả chính: Độc giả Sinh viên (StudentReader) và Độc giả Giảng viên (LecturerReader).",
    "specs": [
      "A. Lớp cơ sở trừu tượng DocGia: MaDocGia, HoTen, SoThangGiaHan. Phương thức: TinhPhiLamThe().",
      "B1. Lớp StudentReader: TruongDaiHoc. TinhPhiLamThe() = SoThangGiaHan * 15,000 VND.",
      "B2. Lớp LecturerReader: KhoaCongTac. TinhPhiLamThe() = SoThangGiaHan * 30,000 VND."
    ],
    "sampleCode": """abstract class DocGia
{
    public string MaDocGia { get; set; }
    public string HoTen { get; set; }
    public int SoThangGiaHan { get; set; }
    public abstract double TinhPhiLamThe();
}

class StudentReader : DocGia
{
    public string TruongDaiHoc { get; set; }
    public override double TinhPhiLamThe() => SoThangGiaHan * 15000;
}

class LecturerReader : DocGia
{
    public string KhoaCongTac { get; set; }
    public override double TinhPhiLamThe() => SoThangGiaHan * 30000;
}"""
  },
  {
    "id": 7,
    "title": "BÀI TẬP 7: QUẢN LÝ KHÓA HỌC VÀ TRỢ GIÁ HỌC PHÍ (COURSE MANAGEMENT)",
    "problem": "Trung tâm đào tạo CNTT tổ chức 02 loại khóa học: Khóa học Ngắn hạn (ShortCourse) và Khóa học Chuyên sâu (BootcampCourse).",
    "specs": [
      "A. Lớp cơ sở trừu tượng KhoaHoc: MaKhoaHoc, TenKhoaHoc, HocPhiCoBan, SoBuoiHoc. Phương thức: TinhHocPhiThucTe().",
      "B1. Lớp ShortCourse: TienTaiLieu. TinhHocPhiThucTe() = HocPhiCoBan + TienTaiLieu.",
      "B2. Lớp BootcampCourse: PhiDoAnThucTe. TinhHocPhiThucTe() = HocPhiCoBan * 0.90 + PhiDoAnThucTe."
    ],
    "sampleCode": """abstract class KhoaHoc
{
    public string MaKhoaHoc { get; set; }
    public string TenKhoaHoc { get; set; }
    public double HocPhiCoBan { get; set; }
    public int SoBuoiHoc { get; set; }
    public abstract double TinhHocPhiThucTe();
}

class ShortCourse : KhoaHoc
{
    public double TienTaiLieu { get; set; }
    public override double TinhHocPhiThucTe() => HocPhiCoBan + TienTaiLieu;
}

class BootcampCourse : KhoaHoc
{
    public double PhiDoAnThucTe { get; set; }
    public override double TinhHocPhiThucTe() => HocPhiCoBan * 0.90 + PhiDoAnThucTe;
}"""
  },
  {
    "id": 8,
    "title": "BÀI TẬP 8: QUẢN LÝ HÓA ĐƠN TIỀN ĐIỆN VẬN HÀNH (ELECTRICITY BILL)",
    "problem": "Công ty điện lực quản lý hóa đơn của 02 nhóm hộ tiêu thụ: Hộ gia đình sinh hoạt (ResidentialCustomer) và Hộ kinh doanh sản xuất (BusinessCustomer).",
    "specs": [
      "A. Lớp cơ sở trừu tượng HoaDonDien: MaKhachHang, TenChuHo, SoKwhTieuThu. Phương thức: TinhTienDien().",
      "B1. Lớp ResidentialCustomer: DinhMucKwh. Nếu SoKwhTieuThu <= DinhMucKwh: SoKwhTieuThu * 1,800; Ngược lại: (DinhMuc * 1,800) + (Dư * 2,500).",
      "B2. Lớp BusinessCustomer: TyleKwhCaoDiem (%). TinhTienDien() = (Thường * 2,000) + (Cao điểm * 3,200)."
    ],
    "sampleCode": """abstract class HoaDonDien
{
    public string MaKhachHang { get; set; }
    public string TenChuHo { get; set; }
    public double SoKwhTieuThu { get; set; }
    public abstract double TinhTienDien();
}

class ResidentialCustomer : HoaDonDien
{
    public double DinhMucKwh { get; set; }
    public override double TinhTienDien()
    {
        if (SoKwhTieuThu <= DinhMucKwh) return SoKwhTieuThu * 1800;
        return (DinhMucKwh * 1800) + (SoKwhTieuThu - DinhMucKwh) * 2500;
    }
}

class BusinessCustomer : HoaDonDien
{
    public double TyleKwhCaoDiem { get; set; }
    public override double TinhTienDien()
    {
        return (SoKwhTieuThu * (1 - TyleKwhCaoDiem / 100.0) * 2000)
             + (SoKwhTieuThu * (TyleKwhCaoDiem / 100.0) * 3200);
    }
}"""
  },
  {
    "id": 9,
    "title": "BÀI TẬP 9: QUẢN LÝ BẤT ĐỘNG SẢN CHO THUÊ (REAL ESTATE MANAGEMENT)",
    "problem": "Sàn giao dịch bất động sản quản lý cho thuê 02 loại bất động sản chính: Căn hộ chung cư (Apartment) và Nhà mặt phố kinh doanh (Townhouse).",
    "specs": [
      "A. Lớp cơ sở trừu tượng BatDongSan: MaBDS, DiaChi, DienTichM2, DonGiaM2. Phương thức: TinhTienThueHangThang().",
      "B1. Lớp Apartment: PhiQuanLyToaNha. Tiền = (DienTich * DonGia) + PhiQuanLy.",
      "B2. Lớp Townhouse: SoMatTienM. Tiền = (DienTich * DonGia) + (SoMatTienM * 2,000,000)."
    ],
    "sampleCode": """abstract class BatDongSan
{
    public string MaBDS { get; set; }
    public string DiaChi { get; set; }
    public double DienTichM2 { get; set; }
    public double DonGiaM2 { get; set; }
    public abstract double TinhTienThueHangThang();
}

class Apartment : BatDongSan
{
    public double PhiQuanLyToaNha { get; set; }
    public override double TinhTienThueHangThang() => (DienTichM2 * DonGiaM2) + PhiQuanLyToaNha;
}

class Townhouse : BatDongSan
{
    public double SoMatTienM { get; set; }
    public override double TinhTienThueHangThang() => (DienTichM2 * DonGiaM2) + (SoMatTienM * 2000000);
}"""
  },
  {
    "id": 10,
    "title": "BÀI TẬP 10: QUẢN LÝ THIẾT BỊ CÔNG NGHIỆP TRONG NHÀ XƯỞNG (EQUIPMENT MANAGEMENT)",
    "problem": "Một nhà máy sản xuất quản lý 02 nhóm thiết bị chính: Máy gia công tự động (CNCStation) và Rô-bốt hàn công nghiệp (WeldingRobot).",
    "specs": [
      "A. Lớp cơ sở trừu tượng ThietBi: MaThietBi, TenThietBi, ZinGiaGoc, SoThangSuDung. Phương thức: TinhChiPhiKhauHaoThang().",
      "B1. Lớp CNCStation: PhiThayDaoDinhKy. Khấu hao = (ZinGiaGoc / 60) + PhiThayDaoDinhKy.",
      "B2. Lớp WeldingRobot: PhiHieuChinhGoc. Khấu hao = (ZinGiaGoc / 48) + PhiHieuChinhGoc."
    ],
    "sampleCode": """abstract class ThietBi
{
    public string MaThietBi { get; set; }
    public string TenThietBi { get; set; }
    public double ZinGiaGoc { get; set; }
    public int SoThangSuDung { get; set; }
    public abstract double TinhChiPhiKhauHaoThang();
}

class CNCStation : ThietBi
{
    public double PhiThayDaoDinhKy { get; set; }
    public override double TinhChiPhiKhauHaoThang() => (ZinGiaGoc / 60.0) + PhiThayDaoDinhKy;
}

class WeldingRobot : ThietBi
{
    public double PhiHieuChinhGoc { get; set; }
    public override double TinhChiPhiKhauHaoThang() => (ZinGiaGoc / 48.0) + PhiHieuChinhGoc;
}"""
  }
]

# Additional 35 questions from 51 to 100
additional_questions = [
  (
    "Câu 51 (Lý thuyết - Sealed Class): Trong C#, khi một lớp được khai báo với từ khóa `sealed` (ví dụ: `public sealed class B`), ý nghĩa của nó là gì?",
    "Bị phong ấn, ngăn không cho bất kỳ lớp nào khác kế thừa từ nó", "Không thể khởi tạo bằng toán tử new", "Biến tất cả các hàm thành abstract", "Chỉ cho phép kế thừa 1 lần",
    "A", "Từ khóa sealed khóa lớp lại, ngắt khả năng kế thừa của các lớp khác từ lớp này."
  ),
  (
    "Câu 52 (Đọc hiểu mã - Operator Overloading Comparison): Cho đoạn mã C# sau:\n```csharp\nclass Hop\n{\n    public double TheTich { get; set; }\n    public static bool operator >(Hop h1, Hop h2) => h1.TheTich > h2.TheTich;\n    public static bool operator <(Hop h1, Hop h2) => h1.TheTich < h2.TheTich;\n}\n// Trong hàm Main:\nHop a = new Hop { TheTich = 10 };\nHop b = new Hop { TheTich = 20 };\nConsole.WriteLine(a > b);\n```",
    "False", "True", "Lỗi biên dịch", "10",
    "A", "a.TheTich (10) > b.TheTich (20) là False. Console in 'False'."
  ),
  (
    "Câu 53 (Lý thuyết - base Keyword): Từ khóa `base` trong lớp con dùng để làm gì?",
    "Truy cập đến các thành viên (Constructor, phương thức, thuộc tính) của lớp cha", "Khai báo lớp mới", "Tạo ra một đối tượng tĩnh", "Xóa đối tượng ở lớp cha",
    "A", "base cho phép lớp con gọi lại Constructor hoặc các phương thức/thuộc tính của lớp cha bị che giấu/ghi đè."
  ),
  (
    "Câu 54 (Đọc hiểu mã - base method call): Cho đoạn mã C# sau:\n```csharp\nclass NhanVien\n{\n    public virtual void ChamCong() => Console.Write(\"NV \");\n}\nclass QuanLy : NhanVien\n{\n    public override void ChamCong()\n    {\n        base.ChamCong();\n        Console.Write(\"QL \");\n    }\n}\n// Trong hàm Main:\nNhanVien q = new QuanLy();\nq.ChamCong();\n```",
    "NV QL", "QL", "NV", "Lỗi biên dịch",
    "A", "base.ChamCong() in 'NV ', sau đó in tiếp 'QL '. Kết quả: 'NV QL '."
  ),
  (
    "Câu 55 (Lý thuyết - Operator Overloading Pair Rules): Khi nạp chồng toán tử so sánh `==` trong C#, bạn BẮT BUỘC phải nạp chồng đi kèm toán tử nào?",
    "!=", ">", "<", "+=",
    "A", "Các toán tử so sánh trong C# bắt buộc nạp chồng theo cặp: (== và !=), (> và <), (>= và <=)."
  ),
  (
    "Câu 56 (Đọc hiểu mã - Inherited Property Access): Cho đoạn mã C# sau:\n```csharp\nclass Xe\n{\n    public string Hang { get; set; } = \"Honda\";\n}\nclass XeMay : Xe {}\n// Trong hàm Main:\nXeMay xm = new XeMay();\nConsole.WriteLine(xm.Hang);\n```",
    "Honda", "null", "Lỗi biên dịch", "XeMay",
    "A", "XeMay kế thừa thuộc tính Hang từ Xe nên xm.Hang lấy giá trị mặc định là 'Honda'."
  ),
  (
    "Câu 57 (Lý thuyết - Type Checking `is` operator): Toán tử `is` trong C# được dùng để làm gì?",
    "Kiểm tra xem một đối tượng có tương thích/thuộc về một kiểu dữ liệu cụ thể hay không (trả về bool)", "Ép kiểu đối tượng và trả về null nếu thất bại", "Gán giá trị cho đối tượng", "So sánh giá trị hai biến số",
    "A", "Toán tử `is` dùng để kiểm tra tính tương thích kiểu dữ liệu của đối tượng thời điểm runtime và trả về true/false."
  ),
  (
    "Câu 58 (Đọc hiểu mã - Type Checking `is` operator): Cho đoạn mã C# sau:\n```csharp\nclass NhanVien {}\nclass LapTrinhVien : NhanVien {}\n// Trong hàm Main:\nNhanVien nv = new LapTrinhVien();\nif (nv is LapTrinhVien)\n    Console.Write(\"LTV \");\nif (nv is NhanVien)\n    Console.Write(\"NV \");\n```",
    "LTV NV", "LTV", "NV", "Lỗi biên dịch",
    "A", "nv là instance của LapTrinhVien, đồng thời LapTrinhVien kế thừa NhanVien nên cả 2 điều kiện is đều đúng -> 'LTV NV '."
  ),
  (
    "Câu 59 (Lý thuyết - Casting in Inheritance): Hiện tượng gán một đối tượng của lớp con cho một biến kiểu lớp cha (Upcasting) diễn ra như thế nào?",
    "Diễn ra tự động (ngầm định) và an toàn", "Bắt buộc phải ép kiểu tường minh", "Luôn gây ra lỗi Runtime Exception", "Chỉ làm được nếu dùng từ khóa ref",
    "A", "Upcasting (chuyển từ lớp con lên lớp cha) luôn an toàn và được C# hỗ trợ tự động/ngầm định."
  ),
  (
    "Câu 60 (Đọc hiểu mã - Downcasting with `is` check): Cho đoạn mã C# sau:\n```csharp\nclass PhuongTien { }\nclass Oto : PhuongTien\n{\n    public void Lai() => Console.Write(\"LaiOto \");\n}\n// Trong hàm Main:\nPhuongTien pt = new Oto();\nif (pt is Oto xe)\n{\n    xe.Lai();\n}\n```",
    "LaiOto", "Lỗi biên dịch", "Lỗi Runtime Exception", "Không in gì cả",
    "A", "Cú pháp pattern matching với `is` (pt is Oto xe) kiểm tra đúng và tự động gán biến xe kiểu Oto để gọi xe.Lai() -> 'LaiOto '."
  ),
  (
    "Câu 66 (Lý thuyết - Interface Definition): Phát biểu nào sau đây miêu tả ĐÚNG bản chất của `Interface` trong C#?",
    "Là một bản hợp đồng định nghĩa các thành viên mà lớp thực thi phải cài đặt, không chứa dữ liệu thực thể (instance fields)", "Interface có thể chứa các trường dữ liệu private", "Khởi tạo đối tượng trực tiếp bằng new IInterface()", "Một lớp chỉ được phép thực thi duy nhất 1 Interface",
    "A", "Interface đóng vai trò bản hợp đồng định nghĩa giao diện phục vụ giao tiếp, không lưu trạng thái thực thể."
  ),
  (
    "Câu 67 (Lý thuyết - Multiple Interface Implementation): Một lớp trong C# có thể thực thi (implement) bao nhiêu Interface cùng một lúc?",
    "Nhiều Interface cùng lúc (Đa thực thi Interface)", "Duy nhất 1 Interface", "Tối đa 2 Interface", "Không thể thực thi Interface nếu đã kế thừa lớp",
    "A", "C# cho phép một lớp thực thi nhiều Interface cùng lúc để giải quyết bài toán đa kế thừa tính năng."
  ),
  (
    "Câu 76 (Lý thuyết - Array vs ArrayList vs List<T>): Sự khác biệt căn bản giữa `ArrayList` và `List<T>` khi quản lý danh sách đối tượng trong C# là gì?",
    "ArrayList lưu đối tượng dạng object nên bị Boxing/Unboxing và không an toàn kiểu, còn List<T> là Generic đảm bảo an toàn kiểu và hiệu năng cao", "ArrayList có kích thước cố định còn List<T> thì không", "List<T> không lưu được đối tượng tự định nghĩa", "ArrayList chỉ chạy được trên mảng 1 chiều",
    "A", "ArrayList ép mọi đối tượng về kiểu `object` gây tốn chi phí boxing/unboxing, trong khi `List<T>` duy trì kiểu dữ liệu gốc an toàn."
  ),
  (
    "Câu 91 (Lý thuyết - Exception Handling Concept): Trong C#, mục đích chính của việc sử dụng khối lệnh `try - catch` khi viết chương trình là gì?",
    "Bắt và xử lý các lỗi phát sinh trong quá trình chạy (Runtime Exceptions) để tránh ứng dụng bị ngắt đột ngột", "Giúp chương trình chạy nhanh hơn", "Phát hiện các lỗi cú pháp khi biên dịch", "Tự động sửa lỗi mã nguồn",
    "A", "Cấu trúc try-catch dùng để bắt và xử lý ngoại lệ Runtime, đảm bảo chương trình không bị crash ngắt đột ngột."
  ),
  (
    "Câu 93 (Lý thuyết - `finally` Block Behavior): Trong cấu trúc `try - catch - finally`, khối lệnh `finally` có đặc điểm hoạt động như thế nào?",
    "Luôn luôn được thi hành dù có ngoại lệ xảy ra hay không", "Chỉ thi hành khi có ngoại lệ xảy ra", "Chỉ thi hành khi không có ngoại lệ xảy ra", "Bị bỏ qua nếu đã có khối catch",
    "A", "Khối finally đảm bảo luôn luôn được thực thi (thường dùng để đóng kết nối, giải phóng tài nguyên)."
  )
]

def run():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM subjects WHERE code = 'OOP_CSHARP'")
    row = c.fetchone()
    if not row:
        print("OOP_CSHARP subject not found!")
        return
    sid = row['id']
    
    # Xóa các exercises cũ nếu có để tránh trùng
    c.execute("DELETE FROM exercises WHERE subject_id = ?", (sid,))
    conn.commit()
    conn.close()

    print("Adding 10 OOP Exercises...")
    for ex in exercises_data:
        add_exercise(
            subject_id=sid,
            title=ex["title"],
            problem=ex["problem"],
            specs=ex["specs"],
            sample_code=ex["sampleCode"]
        )

    print("Adding additional OOP questions...")
    for q in additional_questions:
        add_question(
            subject_id=sid,
            question_text=q[0],
            option_a=q[1],
            option_b=q[2],
            option_c=q[3],
            option_d=q[4],
            correct_option=q[5],
            explanation=q[6],
            q_type='mcq'
        )

    print("Successfully populated exercises and additional questions!")

if __name__ == "__main__":
    run()
