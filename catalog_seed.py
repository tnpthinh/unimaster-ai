"""Idempotent subject-catalog migration for fresh/cloud databases.

The production database may be created from an empty persistent volume.  Keep
this migration separate from large question-bank seeders: it guarantees that
all catalog subjects exist without deleting user data or existing questions.
"""
import database as db


CORE_SUBJECTS = (
    {
        "code": "MLN101",
        "name": "Triết học Mác - Lênin",
        "icon": "🧠",
        "category": "Lý luận chính trị",
        "description": "Môn học nền tảng về thế giới quan duy vật biện chứng và phương pháp luận biện chứng duy vật.",
    },
    {
        "code": "PLDC101",
        "name": "Pháp luật đại cương",
        "icon": "⚖️",
        "category": "Khoa học xã hội",
        "description": "Kiến thức nền tảng về Nhà nước, hệ thống pháp luật, vi phạm pháp luật và trách nhiệm pháp lý.",
    },
    {
        "code": "MATH101",
        "name": "Giải tích & Đại số tuyến tính",
        "icon": "📐",
        "category": "Khoa học tự nhiên",
        "description": "Ma trận, định thức, hệ phương trình tuyến tính, giới hạn, đạo hàm và tích phân nhiều biến.",
    },
    {
        "code": "CS101",
        "name": "Lập trình & Cấu trúc dữ liệu",
        "icon": "💻",
        "category": "Công nghệ thông tin",
        "description": "Ngôn ngữ C/C++, con trỏ, danh sách liên kết, ngăn xếp, hàng đợi, cây và đồ thị.",
    },
    {
        "code": "OOP_CSHARP",
        "name": "Lập trình Hướng đối tượng (C#)",
        "icon": "💻",
        "category": "CNTT",
        "description": "Class, kế thừa, đa hình, interface và thực hành lập trình C#.",
    },
    {
        "code": "DISCRETE_MATH_ALGO",
        "name": "Giải thuật & Toán rời rạc (Tự luận)",
        "icon": "📐",
        "category": "CNTT",
        "description": "Đồ thị, cây, quy nạp, Big-O và các thuật toán nền tảng.",
    },
    {
        "code": "NNLT1",
        "name": "Ngôn ngữ Lập trình 1 (Python)",
        "icon": "🐍",
        "category": "CNTT",
        "description": "Python List, Dict, chuỗi, đệ quy và lập trình thực hành.",
    },
    {
        "code": "AVCB3",
        "name": "Anh văn cơ bản 3 (AVCB 3 - IT English)",
        "icon": "🌐",
        "category": "Ngoại ngữ",
        "description": "Tiếng Anh công nghệ thông tin, trình độ B1/B2 và ngữ pháp.",
    },
)


def ensure_core_subject_catalog():
    """Create any missing catalog rows; never replace or delete existing data."""
    existing = {subject["code"] for subject in db.get_all_subjects()}
    added = 0
    for subject in CORE_SUBJECTS:
        if subject["code"] not in existing:
            db.add_subject(**subject)
            added += 1
    if added:
        print(f"📚 Subject catalog migration: added {added} core subject(s)")
    return added
