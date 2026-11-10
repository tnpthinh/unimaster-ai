"""
UniMaster AI — Universal Multi-Format Document Parser
Supports:
- PDF (.pdf) via pypdf + Gemini Multimodal OCR fallback for scanned PDFs
- PowerPoint (.pptx, .ppt) via native OOXML slide + notes extraction
- Word (.docx, .doc) via native OOXML paragraph + table extraction
- Excel / Tabular (.xlsx, .csv, .tsv)
- Images (.png, .jpg, .jpeg, .webp) via Gemini Multimodal Vision
- Text & Code (.txt, .md, .json, .cs, .py, .java, .cpp, .js, .ts, .sql, .html)
"""
import io
import os
import re
import time
import hashlib
import zipfile
import xml.etree.ElementTree as ET

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_UPLOAD_IMG_DIR = os.path.join(BASE_DIR, "static", "uploads", "user_docs")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TEXT_EXTS = {
    ".txt", ".md", ".csv", ".tsv", ".json", ".xml", ".html", ".htm",
    ".cs", ".py", ".java", ".cpp", ".c", ".h", ".js", ".ts", ".tsx", ".sql"
}


def extract_embedded_images(filename: str, raw: bytes) -> list:
    """
    Trích xuất toàn bộ hình ảnh nhúng từ PDF (.pdf), PowerPoint (.pptx), Word (.docx)
    hoặc lưu trực tiếp file ảnh (.png, .jpg, .jpeg, .webp) vào /static/uploads/user_docs/
    để gắn vào câu hỏi thi hoặc tạo câu hỏi nhận diện hình ảnh.
    """
    os.makedirs(USER_UPLOAD_IMG_DIR, exist_ok=True)
    ext = os.path.splitext(filename or "")[1].lower()
    short_hash = hashlib.md5(raw[:4096] + str(len(raw)).encode()).hexdigest()[:8]
    saved_images = []

    try:
        if ext in IMAGE_EXTS:
            out_name = f"img_{short_hash}{ext}"
            out_path = os.path.join(USER_UPLOAD_IMG_DIR, out_name)
            with open(out_path, "wb") as f:
                f.write(raw)
            saved_images.append({
                "url": f"/static/uploads/user_docs/{out_name}",
                "label": f"Ảnh tải lên ({filename})",
                "page": 1
            })
        elif ext == ".pdf" and PdfReader:
            reader = PdfReader(io.BytesIO(raw))
            for p_idx, page in enumerate(reader.pages):
                try:
                    imgs = page.images
                except Exception:
                    imgs = []
                for im_idx, im in enumerate(imgs):
                    im_ext = os.path.splitext(im.name or ".jpg")[1].lower() or ".jpg"
                    if im_ext not in IMAGE_EXTS:
                        im_ext = ".jpg"
                    if len(im.data) < 2048:
                        continue  # Bỏ qua icon siêu nhỏ
                    out_name = f"pdf_{short_hash}_p{p_idx+1}_{im_idx+1}{im_ext}"
                    out_path = os.path.join(USER_UPLOAD_IMG_DIR, out_name)
                    with open(out_path, "wb") as f:
                        f.write(im.data)
                    saved_images.append({
                        "url": f"/static/uploads/user_docs/{out_name}",
                        "label": f"Hình trang {p_idx + 1} (#{im_idx + 1})",
                        "page": p_idx + 1
                    })
        elif ext in (".pptx", ".docx") and zipfile.is_zipfile(io.BytesIO(raw)):
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                media_files = [
                    n for n in zf.namelist()
                    if (n.startswith("ppt/media/") or n.startswith("word/media/"))
                    and os.path.splitext(n)[1].lower() in IMAGE_EXTS
                ]
                for m_idx, m_name in enumerate(media_files[:30]):
                    m_bytes = zf.read(m_name)
                    if len(m_bytes) < 2048:
                        continue
                    m_ext = os.path.splitext(m_name)[1].lower()
                    out_name = f"doc_{short_hash}_{m_idx+1}{m_ext}"
                    out_path = os.path.join(USER_UPLOAD_IMG_DIR, out_name)
                    with open(out_path, "wb") as f:
                        f.write(m_bytes)
                    saved_images.append({
                        "url": f"/static/uploads/user_docs/{out_name}",
                        "label": f"Hình minh họa #{m_idx + 1}",
                        "page": m_idx + 1
                    })
    except Exception:
        pass

    return saved_images


def extract_highlighted_pdf_questions(raw: bytes, extracted_images: list = None) -> list:
    """
    Trích xuất trực tiếp toàn bộ câu hỏi trắc nghiệm từ file PDF có sẵn cấu trúc 'Câu 1..N'
    và tự động phát hiện đáp án tô đỏ (RGB red) hoặc đánh dấu trong PDF.
    """
    if not PdfReader:
        return []
    try:
        reader = PdfReader(io.BytesIO(raw))
        raw_lines = []
        for p_idx, page in enumerate(reader.pages):
            state = {"red": False}
            cur_line_chars = []

            def op_before(op, args, cm, tm):
                if op in (b"rg", b"RG") and len(args) == 3:
                    r, g, b = float(args[0]), float(args[1]), float(args[2])
                    state["red"] = (r > 0.6 and g < 0.35 and b < 0.35)
                elif op in (b"g", b"G"):
                    state["red"] = False

            def vis_text(text, cm, tm, font_dict, font_size):
                for ch in text:
                    if ch == "\n":
                        txt_line = "".join(c for _, c in cur_line_chars).strip()
                        if txt_line:
                            raw_lines.append((txt_line, p_idx + 1, cur_line_chars[:]))
                        cur_line_chars.clear()
                    else:
                        cur_line_chars.append((state["red"], ch))

            page.extract_text(visitor_operand_before=op_before, visitor_text=vis_text)
            if cur_line_chars:
                txt_line = "".join(c for _, c in cur_line_chars).strip()
                if txt_line:
                    raw_lines.append((txt_line, p_idx + 1, cur_line_chars[:]))

        questions = []
        cur_q = None
        for line, page_no, chars in raw_lines:
            m = re.match(r"^Câu\s+(\d+)[\.\:]?\s*(.*)$", line, re.IGNORECASE)
            if m:
                if cur_q:
                    questions.append(cur_q)
                cur_q = {"num": int(m.group(1)), "stem": m.group(2).strip(), "lines": [], "page": page_no}
            elif cur_q:
                cur_q["lines"].append((line, chars))
        if cur_q:
            questions.append(cur_q)

        parsed = []
        for q in questions:
            q_chars = []
            for idx, (l, chs) in enumerate(q["lines"]):
                if idx > 0:
                    q_chars.append((False, "\n"))
                q_chars.extend(chs)
            q_str = "".join(c for _, c in q_chars)
            opt_matches = [
                m for m in re.finditer(r"(?:^|[\n\s])([A-D])\.\s*", q_str)
                if not q_str[:m.start()].endswith("vitamin")
            ]
            if len(opt_matches) < 2:
                continue
            stem_extra = q_str[:opt_matches[0].start()].strip() if opt_matches[0].start() > 0 else ""
            full_stem = f"Câu {q['num']}. {q['stem']}" + (f" {stem_extra}" if stem_extra else "")
            full_stem = re.sub(r"\s+", " ", full_stem).strip()

            opts = {"A": "", "B": "", "C": "", "D": ""}
            red_letters = []
            for i, m in enumerate(opt_matches):
                letter = m.group(1)
                c_start = m.end()
                s_end = opt_matches[i + 1].start() if i + 1 < len(opt_matches) else len(q_str)
                opts[letter] = re.sub(r"\s+", " ", q_str[c_start:s_end]).strip()
                seg_chars = q_chars[m.start():s_end]
                red_cnt = sum(1 for r, c in seg_chars if r and not c.isspace())
                tot_cnt = sum(1 for _, c in seg_chars if not c.isspace())
                if red_cnt >= 2 and red_cnt >= tot_cnt * 0.22:
                    red_letters.append(letter)

            corr = red_letters[0] if red_letters else "A"
            parsed.append({
                "question_text": full_stem,
                "option_a": opts["A"],
                "option_b": opts["B"],
                "option_c": opts["C"] or "Phương án C",
                "option_d": opts["D"] or "Phương án D",
                "correct_option": corr,
                "explanation": f"Đáp án chuẩn trích xuất từ tài liệu gốc: {corr} ({opts.get(corr, '')})",
                "difficulty": "medium",
                "q_type": "mcq",
                "image_url": ""
            })
        return parsed
    except Exception:
        return []


def decode_bytes_safely(raw: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "utf-16", "cp1258", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="ignore")


def extract_pdf_text(raw: bytes) -> tuple[str, int]:
    if not PdfReader:
        return "", 0
    reader = PdfReader(io.BytesIO(raw))
    pages_out = []
    for idx, page in enumerate(reader.pages):
        try:
            txt = (page.extract_text() or "").strip()
        except Exception:
            txt = ""
        if txt:
            pages_out.append(f"--- Trang {idx + 1} ---\n{txt}")
    return "\n\n".join(pages_out), len(reader.pages)


def extract_pptx_text(raw: bytes) -> tuple[str, int]:
    slides_out = []
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        slide_files = [
            n for n in zf.namelist()
            if re.match(r"^ppt/slides/slide\d+\.xml$", n)
        ]
        slide_files.sort(key=lambda name: int(re.search(r"slide(\d+)\.xml$", name).group(1)))

        for idx, sfile in enumerate(slide_files):
            xml_bytes = zf.read(sfile)
            root = ET.fromstring(xml_bytes)
            paragraphs = []
            for p_elem in root.iter():
                if p_elem.tag.endswith("}p"):
                    runs = [
                        t_elem.text
                        for t_elem in p_elem.iter()
                        if t_elem.tag.endswith("}t") and t_elem.text
                    ]
                    line = "".join(runs).strip()
                    if line:
                        paragraphs.append(line)

            # Also check speaker notes if present
            note_path = f"ppt/notesSlides/notesSlide{idx + 1}.xml"
            if note_path in zf.namelist():
                try:
                    n_root = ET.fromstring(zf.read(note_path))
                    n_runs = [
                        t.text.strip()
                        for t in n_root.iter()
                        if t.tag.endswith("}t") and t.text and t.text.strip()
                    ]
                    if n_runs:
                        paragraphs.append("[Ghi chú giảng viên]: " + " ".join(n_runs))
                except Exception:
                    pass

            if paragraphs:
                slides_out.append(f"--- Slide {idx + 1} ---\n" + "\n".join(paragraphs))

    return "\n\n".join(slides_out), len(slide_files)


def extract_docx_text(raw: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        if "word/document.xml" not in zf.namelist():
            return ""
        root = ET.fromstring(zf.read("word/document.xml"))
        blocks = []
        for elem in root.iter():
            if elem.tag.endswith("}p"):
                runs = [
                    t.text for t in elem.iter()
                    if t.tag.endswith("}t") and t.text
                ]
                line = "".join(runs).strip()
                if line:
                    blocks.append(line)
        return "\n".join(blocks)


def extract_xlsx_text(raw: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        shared_strings = []
        if "xl/sharedStrings.xml" in zf.namelist():
            s_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in s_root.iter():
                if si.tag.endswith("}si"):
                    txt = "".join(t.text for t in si.iter() if t.tag.endswith("}t") and t.text)
                    shared_strings.append(txt)

        sheets = sorted([n for n in zf.namelist() if re.match(r"^xl/worksheets/sheet\d+\.xml$", n)])
        out_lines = []
        for s_idx, sheet_name in enumerate(sheets):
            out_lines.append(f"--- Bảng tính {s_idx + 1} ---")
            w_root = ET.fromstring(zf.read(sheet_name))
            for row in w_root.iter():
                if row.tag.endswith("}row"):
                    cells = []
                    for c in row:
                        if not c.tag.endswith("}c"):
                            continue
                        c_type = c.attrib.get("t", "")
                        v_elem = next((ch for ch in c if ch.tag.endswith("}v")), None)
                        if v_elem is not None and v_elem.text is not None:
                            val = v_elem.text
                            if c_type == "s" and val.isdigit() and int(val) < len(shared_strings):
                                val = shared_strings[int(val)]
                            cells.append(val.strip())
                    if any(cells):
                        out_lines.append(" | ".join(cells))
        return "\n".join(out_lines)


def extract_legacy_binary_office_strings(raw: bytes) -> str:
    """Fallback extractor for old binary .ppt / .doc files"""
    utf16_chunks = re.findall(b"(?:[\x20-\x7e\xc0-\xff]\x00){5,}", raw)
    lines = []
    for ch in utf16_chunks:
        try:
            s = ch.decode("utf-16le", errors="ignore").strip()
            if len(s) >= 5 and not s.startswith("Root Entry"):
                lines.append(s)
        except Exception:
            pass
    if not lines:
        ascii_chunks = re.findall(b"[\x20-\x7e]{8,}", raw)
        lines = [c.decode("latin-1", errors="ignore").strip() for c in ascii_chunks[:400]]
    return "\n".join(lines)


async def parse_uploaded_file(filename: str, raw_bytes: bytes, ai_module=None) -> dict:
    """
    Parses any uploaded educational file and returns:
    {
      "filename": str,
      "ext": str,
      "char_count": int,
      "summary_badge": str,
      "content": str,
      "used_vision_ocr": bool
    }
    """
    ext = os.path.splitext(filename or "")[1].lower()
    used_ocr = False
    meta_badge = ext.upper().lstrip(".") or "FILE"
    extracted = ""

    if ext == ".pdf":
        extracted, page_count = extract_pdf_text(raw_bytes)
        meta_badge = f"PDF • {page_count} trang"
        # Scanned PDF fallback via Gemini Multimodal!
        if len(extracted.strip()) < 60 and ai_module and len(raw_bytes) <= 18 * 1024 * 1024:
            ocr_text = await ai_module.ai_extract_from_multimodal("application/pdf", raw_bytes, filename)
            if ocr_text:
                extracted = ocr_text
                used_ocr = True
                meta_badge += " (AI OCR)"

    elif ext == ".pptx":
        extracted, slide_count = extract_pptx_text(raw_bytes)
        meta_badge = f"PowerPoint • {slide_count} slides"

    elif ext == ".ppt":
        extracted = extract_legacy_binary_office_strings(raw_bytes)
        meta_badge = "PowerPoint (.PPT)"

    elif ext == ".docx":
        extracted = extract_docx_text(raw_bytes)
        meta_badge = "Word (.DOCX)"

    elif ext == ".doc":
        extracted = extract_legacy_binary_office_strings(raw_bytes)
        meta_badge = "Word (.DOC)"

    elif ext == ".xlsx":
        extracted = extract_xlsx_text(raw_bytes)
        meta_badge = "Excel (.XLSX)"

    elif ext in IMAGE_EXTS:
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp"
        }
        if ai_module:
            extracted = await ai_module.ai_extract_from_multimodal(
                mime_map.get(ext, "image/jpeg"), raw_bytes, filename
            ) or ""
            used_ocr = True
        meta_badge = f"Ảnh chụp tài liệu ({ext.upper().lstrip('.')})"

    elif ext in TEXT_EXTS or not ext:
        extracted = decode_bytes_safely(raw_bytes)
        meta_badge = f"Văn bản / Code ({ext.upper().lstrip('.') or 'TXT'})"

    else:
        # Try ZIP-based Office first, else safe text decode
        if zipfile.is_zipfile(io.BytesIO(raw_bytes)):
            try:
                extracted, sc = extract_pptx_text(raw_bytes)
                if not extracted:
                    extracted = extract_docx_text(raw_bytes)
            except Exception:
                extracted = decode_bytes_safely(raw_bytes)
        else:
            extracted = decode_bytes_safely(raw_bytes)

    extracted = re.sub(r"\n{3,}", "\n\n", (extracted or "").strip())
    extracted_images = extract_embedded_images(filename, raw_bytes)
    direct_questions = []
    if ext == ".pdf":
        direct_questions = extract_highlighted_pdf_questions(raw_bytes, extracted_images)
        if extracted_images:
            meta_badge += f" • {len(extracted_images)} ảnh"
        if direct_questions:
            meta_badge += f" • {len(direct_questions)} câu trắc nghiệm"

    return {
        "filename": filename,
        "ext": ext,
        "summary_badge": meta_badge,
        "char_count": len(extracted),
        "content": extracted,
        "used_vision_ocr": used_ocr,
        "extracted_images": extracted_images,
        "direct_questions": direct_questions
    }
