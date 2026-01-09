import socket
import subprocess
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

ALLOWED_USERS = [
    123456789  # your Telegram ID
]

RATE_LIMIT = 3
TIME_WINDOW = 600  # 10 minutes

user_requests = {}

# ===== HELPERS =====
def is_rate_limited(user_id):
    now = time.time()
    timestamps = user_requests.get(user_id, [])
    timestamps = [t for t in timestamps if now - t < TIME_WINDOW]
    user_requests[user_id] = timestamps

    if len(timestamps) >= RATE_LIMIT:
        return True

    timestamps.append(now)
    return False

def is_authorized(user_id):
    return user_id in ALLOWED_USERS

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ Access denied")
        return

    await update.message.reply_text(
        "🌐 IP & Port Scanner Bot\n\n"
        "Commands:\n"
        "/ip example.com\n"
        "/scan example.com\n\n"
        "⚠️ Use only on systems you own or have permission to test"
    )

async def ip_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /ip example.com")
        return

    domain = context.args[0]

    try:
        ip = socket.gethostbyname(domain)
        await update.message.reply_text(f"🔎 Domain: {domain}\n📌 IP: {ip}")
    except:
        await update.message.reply_text("❌ Could not resolve domain")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_authorized(user_id):
        return

    if is_rate_limited(user_id):
        await update.message.reply_text("⏳ Rate limit exceeded (3 scans / 10 min)")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /scan example.com")
        return

    domain = context.args[0]
    await update.message.reply_text("🔍 Scanning top ports...")

    try:
        ip = socket.gethostbyname(domain)

        process = subprocess.run(
            ["nmap", "-F", ip],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = process.stdout.strip()
        if not output:
            output = "No open ports found."

        if len(output) > 4000:
            output = output[-4000:]

        await update.message.reply_text(
            f"🌐 Target: {domain}\n📌 IP: {ip}\n\n📊 Result:\n{output}"
        )

    except:
        await update.message.reply_text("❌ Scan failed")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ip", ip_lookup))
    app.add_handler(CommandHandler("scan", scan))
    app.run_polling()

if __name__ == "__main__":
    main()
