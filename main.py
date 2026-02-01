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

# ================= SAFE MP4 LINKS =================
GIFS = {
    "cry": [
        "https://files.catbox.moe/7w1z5k.mp4"
    ],
    "hug": [
        "https://files.catbox.moe/2x3k9v.mp4"
    ],
    "rasengan": [
        "https://files.catbox.moe/1l4e2s.mp4"
    ]
}

INTERACTIVE = ["hug"]
EXPRESS = ["cry"]
ATTACKS = ["rasengan"]

# ================= /start =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "➕ Add me to group",
            url=f"https://t.me/{context.bot.username}?startgroup=true"
        )]
    ])

    await update.message.reply_text(
        "🤖 Anime Reaction Bot is ONLINE!\n\n"
        "Commands:\n"
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

    # Express
    if command in EXPRESS:
        video = random.choice(GIFS[command])
        await context.bot.send_video(
            chat_id=msg.chat.id,
            video=video,
            caption=f"💭 {user} is crying"
        )

    # Interactive
    elif command in INTERACTIVE and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        video = random.choice(GIFS[command])
        await context.bot.send_video(
            chat_id=msg.chat.id,
            video=video,
            caption=f"💞 {user} hugged {target}"
        )

    # Attacks
    elif command in ATTACKS and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        video = random.choice(GIFS[command])
        await context.bot.send_video(
            chat_id=msg.chat.id,
            video=video,
            caption=f"💥 {user} used RASENGAN on {target}!"
        )

# ================= MAIN =================
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, reaction_handler))

    print("Bot started successfully")
    app.run_polling()
