import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ================= GIF / VIDEO DATABASE =================
GIFS = {
    # Interactive
    "hug": ["https://media.tenor.com/7XK0tZx6d5AAAAAC/anime-hug.mp4"],
    "slap": ["https://media.tenor.com/3z8JxY8XyQAAAAAC/anime-slap.mp4"],
    "kiss": ["https://media.tenor.com/9zG8KxH2lXAAAAAC/anime-kiss.mp4"],
    "pat": ["https://media.tenor.com/Lb8cQY5Z1N8AAAAC/anime-pat.mp4"],
    "punch": ["https://media.tenor.com/7dM4Z3Zl3kAAAAAC/anime-punch.mp4"],

    # Express
    "cry": ["https://media.tenor.com/8tG0cPqjN1EAAAAC/anime-cry.mp4"],
    "laugh": ["https://media.tenor.com/5X8y4k6vP5EAAAAC/anime-laugh.mp4"],
    "smile": ["https://media.tenor.com/wF8qvN8Rk9kAAAAC/anime-smile.mp4"],
    "angry": ["https://media.tenor.com/8YvYy8fZk7kAAAAC/anime-angry.mp4"],

    # Anime attacks
    "rasengan": ["https://media.tenor.com/VHn8z2k5N-AAAAAC/rasengan-naruto.mp4"],
    "chidori": ["https://media.tenor.com/VZ7Yzj6f1cQAAAAC/chidori-sasuke.mp4"],
    "amaterasu": ["https://media.tenor.com/sq2wT8wA5VgAAAAC/amaterasu-itachi.mp4"],
    "bankai": ["https://media.tenor.com/0KJv8vZ8FJcAAAAC/bankai-bleach.mp4"]
}

INTERACTIVE = ["hug", "slap", "kiss", "pat", "punch"]
EXPRESS = ["cry", "laugh", "smile", "angry"]
ATTACKS = ["rasengan", "chidori", "amaterasu", "bankai"]

# ================= /start =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add me to group", url=f"https://t.me/{context.bot.username}?startgroup=true")]
    ])
    await update.message.reply_text(
        "🤖 Anime Reaction Bot is online!\n\n"
        "Use commands like:\n"
        "+cry\n"
        "+hug (reply)\n"
        "+rasengan (reply)",
        reply_markup=keyboard
    )

# ================= REACTION HANDLER =================
async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text or not msg.text.startswith("+"):
        return

    command = msg.text[1:].lower()
    user = msg.from_user.first_name

    # Interactive
    if command in INTERACTIVE and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        video = random.choice(GIFS[command])
        caption = f"💞 {user} {command}ed {target}"
        await context.bot.send_video(msg.chat.id, video=video, caption=caption)

    # Express
    elif command in EXPRESS:
        video = random.choice(GIFS[command])
        caption = f"💭 {user} is {command}"
        await context.bot.send_video(msg.chat.id, video=video, caption=caption)

    # Attacks
    elif command in ATTACKS and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        video = random.choice(GIFS[command])
        caption = f"💥 {user} used {command.upper()} on {target}!"
        await context.bot.send_video(msg.chat.id, video=video, caption=caption)

# ================= MAIN =================
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, reaction_handler))

    print("Bot is running...")
    app.run_polling()
