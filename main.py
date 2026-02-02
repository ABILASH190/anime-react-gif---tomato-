import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    ContextTypes, filters, CallbackQueryHandler
)
from aiohttp import web  # for heartbeat

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "animereacttomotobot"

# ================= GIF DATABASE =================
GIFS = {
    "bite": ["https://media.giphy.com/media/OqQOwXiCyJAmA/giphy.gif"],
    "bonk": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2sybWtzY3RiYWI0ZnE2ZjN2OG9vMjd5cmF1M3l1NjQ3NW1paDd2dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/gsyDSxD5mpBdKftDLq/giphy.gif"],
    "hug": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnhsM2U4dWQ0a3lrY2NrZ29zaWV0MmF5c2RhZHA0eGdlOWF4bzVucyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ZQN9jsRWp1M76/giphy.gif"],
    "rasengan": ["https://tenor.com/view/50-fps-ナルト疾風伝-minato-namikaze-波風-gif-12801236794720890698.gif"],
    "world": ["https://tenor.com/view/za-warudo-the-world-jojos-bizarre-adventures-jjba-anime-gif-17783696.gif"],
    # Add all other GIFs here...
}

INTERACTIVE_LIST = [
    "bite", "bonk", "hug", "rasengan", "world"
]

VERBS = {
    "hug": "hugged", "bonk": "bonked", "bite": "bit",
    "rasengan": "used Rasengan on", "world": "used ZA WARUDO on"
}

# ================= HELP BUTTON =================
async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    interactive = sorted(INTERACTIVE_LIST)
    solo = sorted([r for r in GIFS.keys() if r not in INTERACTIVE_LIST])
    help_text = (
        "📖 **Anime Reaction Bot – Help**\n\n"
        "🔹 **How to use**\n"
        "• Reply to someone with `+reaction` for interactive actions\n"
        "• Send `+reaction` normally for solo reactions\n\n"
        "🤝 **Interactive Reactions (reply required):**\n"
        f"`{'`, `'.join(interactive)}`\n\n"
        "🎭 **Solo / Expression Reactions:**\n"
        f"`{'`, `'.join(solo)}`"
    )
    await query.message.reply_text(help_text, parse_mode="Markdown")

# ================= START COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_url = f"https://t.me/{BOT_USERNAME}?startgroup=true"
    keyboard = [
        [
            InlineKeyboardButton("➕ Add Me to Your Group", url=add_url),
            InlineKeyboardButton("📖 Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 **Konnichiwa! I'm your Anime Reaction Bot!**\n\n"
        "Reply to someone with `+command` to interact!\n"
        "Example: `+hug`, `+rasengan`, `+world`",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ================= REACTION HANDLER =================
async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or not msg.text.startswith("+"):
        return
    command = msg.text[1:].lower()
    user_name = msg.from_user.first_name
    if command not in GIFS or not GIFS[command]:
        await msg.reply_text(f"⚠️ Add links for `+{command}` first!")
        return
    gif_url = random.choice(GIFS[command])
    if command in INTERACTIVE_LIST:
        if not msg.reply_to_message:
            await msg.reply_text(f"❌ Reply to someone to use `+{command}`!")
            return
        target_name = msg.reply_to_message.from_user.first_name
        action = VERBS.get(command, f"{command}ed")
        caption = f"✨ {user_name} {action} {target_name}!"
    else:
        caption = f"💭 {user_name} is {command}ing..."
    try:
        await context.bot.send_animation(
            chat_id=msg.chat_id,
            animation=gif_url,
            caption=caption,
            reply_to_message_id=msg.message_id
        )
    except Exception as e:
        logger.error(f"Error sending animation: {e}")

# ================= 24/7 KEEP-ALIVE =================
async def handle_root(request):
    return web.Response(text="Anime Reaction Bot is ONLINE ✅")

def keep_alive():
    app = web.Application()
    app.add_routes([web.get('/', handle_root)])
    runner = web.AppRunner(app)
    return runner

# ================= RUN BOT =================
if __name__ == "__main__":
    runner = keep_alive()
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    loop.run_until_complete(site.start())

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reaction_handler))
    app.add_handler(CallbackQueryHandler(help_button, pattern="help"))

    print("Bot started successfully ✅")
    loop.run_until_complete(app.start())
    loop.run_until_complete(app.updater.start_polling())
    loop.run_forever()
