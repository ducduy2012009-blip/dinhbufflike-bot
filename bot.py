import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Lấy token từ biến môi trường
TOKEN = os.getenv("TOKEN")

API_URL = "https://free-like-api-aditya-ffm.vercel.app/like"

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Xin chào! Gõ /like uid server_name để dùng bot.\nVí dụ: /like 123456 VN"
    )

# Lệnh /like uid server_name
async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Sai cú pháp!\nDùng: /like uid server_name")
        return

    uid = context.args[0]
    server_name = context.args[1]

    try:
        # Gọi API
        response = requests.get(API_URL, params={
            "uid": uid,
            "server_name": server_name,
            "key": "@adityaapis"
        })

        if response.status_code == 200:
            data = response.json()
            await update.message.reply_text(f"✅ Thành công!\nDữ liệu: {data}")
        else:
            await update.message.reply_text("❌ Lỗi khi gọi API!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi: {e}")

# Chạy bot
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("like", like))

    print("Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
