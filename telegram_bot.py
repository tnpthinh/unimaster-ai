# -*- coding: utf-8 -*-
"""
UniMaster AI Pro — Dedicated Telegram Quiz & Clinical Bot
Tự động gửi câu hỏi trắc nghiệm ôn thi tương tác, tra cứu liều thuốc thận và ca bệnh lâm sàng trên Telegram.

Cách sử dụng:
1. Nhắn /newbot với @BotFather trên Telegram để nhận Bot Token miễn phí.
2. Lưu token vào file telegram_token.txt hoặc biến môi trường TELEGRAM_BOT_TOKEN
3. Chạy lệnh: python telegram_bot.py
"""

import os
import sys
import json
import asyncio
import sqlite3
import random
import aiohttp
import database as db
import extensions

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "telegram_token.txt")

def get_bot_token():
    env_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if env_token:
        return env_token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

async def call_telegram_api(session, token, method, payload=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=20)) as resp:
            return await resp.json()
    except Exception as e:
        print(f"❌ Telegram API Error ({method}): {e}")
        return None

async def send_message(session, token, chat_id, text, reply_markup=None, parse_mode="HTML"):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return await call_telegram_api(session, token, "sendMessage", payload)

async def edit_message_text(session, token, chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return await call_telegram_api(session, token, "editMessageText", payload)

async def answer_callback_query(session, token, callback_query_id, text, show_alert=False):
    payload = {
        "callback_query_id": callback_query_id,
        "text": text,
        "show_alert": show_alert
    }
    return await call_telegram_api(session, token, "answerCallbackQuery", payload)

# Active user sessions for quiz state: { chat_id: { "q_id": ..., "correct": ..., "text": ..., "expl": ... } }
USER_QUIZ_CACHE = {}

async def handle_start(session, token, chat_id, user_first_name):
    welcome_text = (
        f"👋 <b>Xin chào {user_first_name}!</b>\n\n"
        f"Chào mừng bạn đến với <b>UniMaster AI Pro Telegram Bot</b> 🎓🩺\n\n"
        f"Hệ thống ôn thi Y Dược & Đa ngành thông minh hỗ trợ học tập mọi lúc mọi nơi:\n\n"
        f"⚡ <b>/quiz</b> : Nhận ngay 1 câu hỏi trắc nghiệm ngẫu nhiên bấm chọn trực tiếp\n"
        f"📚 <b>/stats</b> : Xem thống kê ngân hàng 677+ câu hỏi (522 câu Hóa Sinh CTUMP)\n"
        f"💊 <b>/dose [tên thuốc] [crcl]</b> : Tra cứu hiệu chỉnh liều theo thanh thải Creatinin\n"
        f"🩺 <b>/case</b> : Tình huống bệnh nhân ảo lâm sàng đa bước\n\n"
        f"🌐 Web App: <i>https://jvc-silk-expires-portions.trycloudflare.com</i>"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "⚡ Bắt đầu làm câu hỏi trắc nghiệm", "callback_data": "cmd_quiz"}],
            [{"text": "📊 Thống kê ngân hàng đề", "callback_data": "cmd_stats"}, {"text": "💊 Tra cứu Dược lý", "callback_data": "cmd_meds"}]
        ]
    }
    await send_message(session, token, chat_id, welcome_text, reply_markup=keyboard)

async def handle_quiz(session, token, chat_id):
    # Fetch random question from database
    subjects = db.get_all_subjects()
    hs_sub = next((s for s in subjects if "HOASINH" in s.get("code", "")), subjects[0] if subjects else None)
    sid = hs_sub["id"] if hs_sub else 10

    questions = db.get_questions_by_subject(sid, random_order=True, limit=1)
    if not questions:
        await send_message(session, token, chat_id, "⚠️ Hiện chưa có câu hỏi nào trong ngân hàng dữ liệu.")
        return

    q = questions[0]
    USER_QUIZ_CACHE[chat_id] = {
        "id": q["id"],
        "correct": q["correct_option"].strip().upper(),
        "text": q["question_text"],
        "a": q["option_a"],
        "b": q["option_b"],
        "c": q["option_c"],
        "d": q["option_d"],
        "explanation": q.get("explanation", "Chưa có lời giải chi tiết.")
    }

    text = (
        f"📚 <b>[Câu hỏi trắc nghiệm Hóa Sinh Y Khoa]</b>\n\n"
        f"<b>{q['question_text']}</b>\n\n"
        f"<b>A.</b> {q['option_a']}\n"
        f"<b>B.</b> {q['option_b']}\n"
        f"<b>C.</b> {q['option_c']}\n"
        f"<b>D.</b> {q['option_d']}\n"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🅰️ Đáp án A", "callback_data": f"ans_A_{q['id']}"},
                {"text": "🅱️ Đáp án B", "callback_data": f"ans_B_{q['id']}"}
            ],
            [
                {"text": "🅲 Đáp án C", "callback_data": f"ans_C_{q['id']}"},
                {"text": "🅳 Đáp án D", "callback_data": f"ans_D_{q['id']}"}
            ]
        ]
    }
    await send_message(session, token, chat_id, text, reply_markup=keyboard)

async def handle_callback_query(session, token, cq):
    cq_id = cq.get("id")
    data = cq.get("data", "")
    msg = cq.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    message_id = msg.get("message_id")

    if data == "cmd_quiz":
        await answer_callback_query(session, token, cq_id, "Chuẩn bị câu hỏi...")
        await handle_quiz(session, token, chat_id)
        return
    elif data == "cmd_stats":
        await answer_callback_query(session, token, cq_id, "Thống kê ngân hàng đề")
        await handle_stats(session, token, chat_id)
        return
    elif data == "cmd_meds":
        await answer_callback_query(session, token, cq_id, "Dược lý lâm sàng")
        await handle_meds_list(session, token, chat_id)
        return

    if data.startswith("ans_"):
        parts = data.split("_")
        chosen = parts[1]
        cached = USER_QUIZ_CACHE.get(chat_id)
        if not cached:
            await answer_callback_query(session, token, cq_id, "Câu hỏi này đã hết hạn lượt tương tác. Hãy gõ /quiz để làm câu mới!", show_alert=True)
            return

        is_correct = (chosen == cached["correct"])
        alert_text = "🎉 CHÍNH XÁC! Bạn trả lời rất chuẩn!" if is_correct else f"❌ CHƯA ĐÚNG! Đáp án chuẩn là {cached['correct']}."
        await answer_callback_query(session, token, cq_id, alert_text, show_alert=False)

        badge = "✅ <b>CHÍNH XÁC!</b>" if is_correct else f"❌ <b>CHƯA ĐÚNG! (Đáp án đúng: {cached['correct']})</b>"
        updated_text = (
            f"📚 <b>[Câu hỏi trắc nghiệm Hóa Sinh Y Khoa]</b>\n\n"
            f"<b>{cached['text']}</b>\n\n"
            f"<b>A.</b> {cached['a']}\n"
            f"<b>B.</b> {cached['b']}\n"
            f"<b>C.</b> {cached['c']}\n"
            f"<b>D.</b> {cached['d']}\n\n"
            f"------------------------------------\n"
            f"Lựa chọn của bạn: <b>{chosen}</b> 👉 {badge}\n\n"
            f"💡 <b>Giải thích chi tiết:</b>\n<i>{cached['explanation']}</i>"
        )

        next_keyboard = {
            "inline_keyboard": [
                [{"text": "➡️ Câu hỏi tiếp theo", "callback_data": "cmd_quiz"}]
            ]
        }
        await edit_message_text(session, token, chat_id, message_id, updated_text, reply_markup=next_keyboard)

async def handle_stats(session, token, chat_id):
    stats = db.get_system_stats()
    subjects = db.get_all_subjects()
    
    sub_lines = []
    for s in subjects:
        sub_lines.append(f"• <b>{s['name']}</b> ({s['code']}): {s.get('question_count', 0)} câu")
    
    text = (
        f"📊 <b>THỐNG KÊ NGÂN HÀNG UNIMASTER AI</b> 🎓\n\n"
        f"🔢 Tổng số câu hỏi: <b>{stats.get('total_questions', 0)} câu</b>\n"
        f"📚 Tổng số môn học: <b>{stats.get('total_subjects', 0)} môn</b>\n"
        f"🃏 Tổng số thẻ Flashcard: <b>{stats.get('total_flashcards', 0)} thẻ</b>\n\n"
        f"<b>Chi tiết theo môn học:</b>\n" + "\n".join(sub_lines) + "\n\n"
        f"<i>Sẵn sàng thi trực tuyến tại Web App!</i>"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "⚡ Làm câu hỏi trắc nghiệm ngay", "callback_data": "cmd_quiz"}]
        ]
    }
    await send_message(session, token, chat_id, text, reply_markup=keyboard)

async def handle_meds_list(session, token, chat_id):
    drugs = extensions.DRUG_DATABASE
    lines = []
    for d in drugs:
        lines.append(f"💊 <b>{d['name']}</b> ({d['group']})")
    
    text = (
        f"💊 <b>DANH MỤC THUỐC CÓ HIỆU CHỈNH LIỀU THẬN</b>\n\n"
        + "\n".join(lines) +
        f"\n\nCú pháp tra nhanh: <code>/dose vancomycin 35</code>\n(với 35 là CrCl tính bằng ml/phút)"
    )
    await send_message(session, token, chat_id, text)

async def handle_dose_calc(session, token, chat_id, args):
    if len(args) < 2:
        await send_message(
            session, token, chat_id,
            "⚠️ Vui lòng nhập đúng cú pháp: <code>/dose [tên thuốc] [crcl]</code>\nVí dụ: <code>/dose vancomycin 25</code>"
        )
        return

    drug_name = args[0].strip().lower()
    try:
        crcl = float(args[1].replace(",", "."))
    except ValueError:
        await send_message(session, token, chat_id, "⚠️ Trị số CrCl phải là số thực (ml/phút). Ví dụ: <code>/dose meropenem 35</code>")
        return

    drug = next((d for d in extensions.DRUG_DATABASE if drug_name in d["id"] or drug_name in d["name"].lower()), None)
    if not drug:
        await send_message(
            session, token, chat_id,
            f"❌ Không tìm thấy thuốc '<b>{drug_name}</b>'. Gõ <code>/meds</code> để xem danh sách thuốc hỗ trợ."
        )
        return

    # Evaluate recommendation based on CrCl
    if crcl >= 50:
        rec = drug["crcl_normal"]
    elif crcl >= 20:
        rec = drug["crcl_mod"]
    else:
        rec = drug["crcl_severe"]

    text = (
        f"💊 <b>KẾT QUẢ HIỆU CHỈNH LIỀU THẬN: {drug['name']}</b>\n"
        f"Phân nhóm: <i>{drug['group']}</i>\n"
        f"Thanh thải Creatinin (CrCl): <b>{crcl:.1f} ml/phút</b>\n\n"
        f"📋 <b>Liều chuẩn (chức năng thận bình thường):</b>\n{drug['std_dose']}\n\n"
        f"🎯 <b>KHUYẾN CÁO HIỆU CHỈNH LIỀU CHO BỆNH NHÂN NÀY:</b>\n<b>{rec}</b>\n\n"
        f"⚠️ <b>Lưu ý an toàn:</b>\n<i>{drug['warning']}</i>"
    )
    await send_message(session, token, chat_id, text)

async def handle_case(session, token, chat_id):
    cases = extensions.VIRTUAL_CASES
    if not cases:
        await send_message(session, token, chat_id, "⚠️ Chưa có ca bệnh lâm sàng nào.")
        return
    c = cases[0]
    p = c["patient"]
    text = (
        f"🩺 <b>CA BỆNH LÂM SÀNG: {c['title']}</b>\n\n"
        f"👤 <b>Bệnh nhân:</b> {p['name']}, {p['age']} tuổi, {p['gender']}\n"
        f"🚨 <b>Lý do vào viện:</b> {p['chief_complaint']}\n\n"
        f"📖 <b>Bệnh sử tóm tắt:</b>\n{p['history']}\n\n"
        f"🩺 <b>Khám thực thể:</b>\n{p['physical_exam']}\n\n"
        f"<i>💡 Để thực hiện đầy đủ 5 bước mô phỏng và nhập chỉ định cận lâm sàng, vui lòng mở mục 'Bệnh nhân ảo' trên Web App!</i>"
    )
    await send_message(session, token, chat_id, text)

async def run_bot():
    token = get_bot_token()
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("=" * 70)
        print("ℹ️ CHƯA CÓ TELEGRAM BOT TOKEN!")
        print("Để kích hoạt bot Telegram ôn thi UniMaster:")
        print("1. Mở ứng dụng Telegram, tìm kiếm @BotFather")
        print("2. Gửi lệnh /newbot và làm theo hướng dẫn (mất 30 giây)")
        print("3. Sao chép Token và dán vào file: telegram_token.txt")
        print("4. Chạy lại: python telegram_bot.py")
        print("=" * 70)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write("YOUR_TELEGRAM_BOT_TOKEN_HERE\n")
        return

    print(f"🤖 Đang khởi chạy UniMaster Telegram Bot...")
    offset = 0
    async with aiohttp.ClientSession() as session:
        # Verify token with getMe
        me = await call_telegram_api(session, token, "getMe")
        if not me or not me.get("ok"):
            print(f"❌ Token Telegram không hợp lệ: {me}")
            return

        bot_info = me.get("result", {})
        print(f"✅ Bot đã kết nối thành công: @{bot_info.get('username')} ({bot_info.get('first_name')})")
        print(f"🚀 Đang lắng nghe tin nhắn từ người dùng...")

        while True:
            try:
                updates_resp = await call_telegram_api(session, token, "getUpdates", {
                    "offset": offset,
                    "timeout": 25
                })
                if updates_resp and updates_resp.get("ok"):
                    updates = updates_resp.get("result", [])
                    for u in updates:
                        offset = u["update_id"] + 1

                        # Handle Callback Queries (button clicks)
                        if "callback_query" in u:
                            await handle_callback_query(session, token, u["callback_query"])
                            continue

                        # Handle Messages
                        if "message" in u:
                            msg = u["message"]
                            chat_id = msg.get("chat", {}).get("id")
                            text = msg.get("text", "").strip()
                            first_name = msg.get("from", {}).get("first_name", "Bạn")

                            if not text or not chat_id:
                                continue

                            if text == "/start":
                                await handle_start(session, token, chat_id, first_name)
                            elif text.startswith("/quiz"):
                                await handle_quiz(session, token, chat_id)
                            elif text == "/stats":
                                await handle_stats(session, token, chat_id)
                            elif text == "/meds":
                                await handle_meds_list(session, token, chat_id)
                            elif text.startswith("/dose"):
                                parts = text.split()
                                await handle_dose_calc(session, token, chat_id, parts[1:])
                            elif text == "/case" or text.startswith("/patient"):
                                await handle_case(session, token, chat_id)
                            else:
                                await handle_start(session, token, chat_id, first_name)

                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"⚠️ Lỗi vòng lặp bot: {e}")
                await asyncio.sleep(3)

if __name__ == "__main__":
    db.init_db()
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n👋 Bot đã dừng.")
