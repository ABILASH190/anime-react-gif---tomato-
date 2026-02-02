import os
import random
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters, CallbackQueryHandler
from aiohttp import web

# ----------------- LOGGING -----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "animereacttomotobot"  # Change to your bot username

# ----------------- GIF DATABASE -----------------
GIFS = {
    # ----- INTERACTIVE (reply required) -----
    "bite": ["https://media.giphy.com/media/OqQOwXiCyJAmA/giphy.gif"],
    "bonk": ["PASTE_YOUR_LINK_HERE"],
    "cuddle": ["PASTE_YOUR_LINK_HERE"],
    "hug": ["PASTE_YOUR_LINK_HERE"],
    "kick": ["PASTE_YOUR_LINK_HERE"],
    "kill": ["PASTE_YOUR_LINK_HERE"],
    "kiss": ["PASTE_YOUR_LINK_HERE"],
    "lick": ["PASTE_YOUR_LINK_HERE"],
    "pat": ["PASTE_YOUR_LINK_HERE"],
    "poke": ["PASTE_YOUR_LINK_HERE"],
    "punch": ["PASTE_YOUR_LINK_HERE"],
    "slap": ["PASTE_YOUR_LINK_HERE"],
    "tickle": ["PASTE_YOUR_LINK_HERE"],
    "feed": ["PASTE_YOUR_LINK_HERE"],
    "pinch": ["PASTE_YOUR_LINK_HERE"],
    "proud": ["PASTE_YOUR_LINK_HERE"],
    "bully": ["PASTE_YOUR_LINK_HERE"],
    "spank": ["PASTE_YOUR_LINK_HERE"],
    "grape": ["PASTE_YOUR_LINK_HERE"],
    "lol": ["PASTE_YOUR_LINK_HERE"],
    "lmao": ["PASTE_YOUR_LINK_HERE"],
    "counter": ["PASTE_YOUR_LINK_HERE"],
    "bankai": ["PASTE_YOUR_LINK_HERE"],
    "revive": ["PASTE_YOUR_LINK_HERE"],
    "reverse": ["PASTE_YOUR_LINK_HERE"],
    "rasengan": ["PASTE_YOUR_LINK_HERE"],
    "explosion": ["PASTE_YOUR_LINK_HERE"],
    "world": ["https://tenor.com/view/za-warudo-the-world-jojos-bizarre-adventures-jjba-anime-gif-17783696.gif"],

    # ----- EXPRESSIONS (solo reactions) -----
    "baka": ["PASTE_YOUR_LINK_HERE"], "blush": ["PASTE_YOUR_LINK_HERE"], "clap": ["PASTE_YOUR_LINK_HERE"],
    "cry": ["PASTE_YOUR_LINK_HERE"], "cute": ["PASTE_YOUR_LINK_HERE"], "dance": ["PASTE_YOUR_LINK_HERE"],
    "fumo": ["PASTE_YOUR_LINK_HERE"], "laugh": ["PASTE_YOUR_LINK_HERE"], "meme": ["PASTE_YOUR_LINK_HERE"],
    "neko": ["PASTE_YOUR_LINK_HERE"], "rage": ["PASTE_YOUR_LINK_HERE"], "sad": ["PASTE_YOUR_LINK_HERE"],
    "scary": ["PASTE_YOUR_LINK_HERE"], "shy": ["PASTE_YOUR_LINK_HERE"], "sleep": ["PASTE_YOUR_LINK_HERE"],
    "smile": ["PASTE_YOUR_LINK_HERE"], "smug": ["PASTE_YOUR_LINK_HERE"], "stare": ["PASTE_YOUR_LINK_HERE"],
    "vibe": ["PASTE_YOUR_LINK_HERE"], "wink": ["PASTE_YOUR_LINK_HERE"], "wow": ["PASTE_YOUR_LINK_HERE"],
    "wtf": ["PASTE_YOUR_LINK_HERE"], "yawn": ["PASTE_YOUR_LINK_HERE"], "smoke": ["PASTE_YOUR_LINK_HERE"],
    "afk": ["PASTE_YOUR_LINK_HERE"], "pushup": ["PASTE_YOUR_LINK_HERE"], "hi": ["PASTE_YOUR_LINK_HERE"],
    "sus": ["PASTE_YOUR_LINK_HERE"], "goon": ["PASTE_YOUR_LINK_HERE"], "enough": ["PASTE_YOUR_LINK_HERE"],
    "eww": ["PASTE_YOUR_LINK_HERE"], "cringe": ["PASTE_YOUR_LINK_HERE"]
}

# ----- INTERACTIVE LIST -----
INTERACTIVE_LIST = [
    "bite", "bonk", "cuddle", "hug", "kick", "kill", "kiss", "lick", "pat", 
    "poke", "punch", "slap", "tickle", "feed", "pinch", "proud", "bully", 
    "spank", "grape", "lol", "lmao", "counter", "bankai", "revive", "reverse", 
    "rasengan", "explosion", "world"
]

# ----- VERBS FOR INTERACTIVE ACTIONS -----
VERBS = {cmd: cmd+"ed" for cmd in INTERACTIVE_LIST}
VERBS.update({"bite": "bit", "hug": "hugged", "world": "used"})

# ----------------- KEEP ALIVE SERVER -----------------
async def keep_alive():
    async def handle(request):
        return web.Response(text="Bot is alive!")
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logger.info("Keep-alive server started")

# ----------------- HELP BUTTON -----------------
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
        f"`{'`, `'.join(solo)}`\n\n"
        "➕ Add me to a group and enjoy anime vibes ✨"
    )
    await query.message.reply_text(help_text, parse_mode="Markdown")

# ----------------- START COMMAND -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_url = f"https://t.me/{BOT_USERNAME}?startgroup=true"
    keyboard = [[
        InlineKeyboardButton("➕ Add Me to Your Group", url=add_url),
        InlineKeyboardButton("📖 Help", callback_data="help")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 **Konnichiwa! I'm your Anime Reaction Bot!**\n"
        "Reply to someone with `+command` to interact!\n"
        "Example: `+hug`, `+slap`, `+pat`",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ----------------- REACTION HANDLER -----------------
async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or not msg.text.startswith("+"):
        return
    command = msg.text[1:].lower().split()[0]
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

# ----------------- MAIN -----------------
async def main():
    await keep_alive()  # start keep-alive server

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reaction_handler))
    app.add_handler(CallbackQueryHandler(help_button, pattern="help"))

    logger.info("Bot is running 24/7")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
