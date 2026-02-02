import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "animereacttomotobot"

# ================= GIF DATABASE =================
GIFS = {
    # INTERACTIVE
    "bite": ["https://media.giphy.com/media/OqQOwXiCyJAmA/giphy.gif"],
    "bonk": ["https://media.giphy.com/media/gsyDSxD5mpBdKftDLq/giphy.gif"],
    "cuddle": ["https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif"],
    "hug": ["https://media.giphy.com/media/ZQN9jsRWp1M76/giphy.gif"],
    "kick": ["https://media.giphy.com/media/u2LJ0n4lx6jF6/giphy.gif"],
    "kill": ["https://media.giphy.com/media/puNw5dA8Vm1NrA2boJ/giphy.gif"],
    "kiss": ["https://media.giphy.com/media/dKBES1ypGwZdyFQBQ7/giphy.gif"],
    "lick": ["https://media.giphy.com/media/DTbmKtrYbwUkw1Inyv/giphy.gif"],
    "pat": ["https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif"],
    "poke": ["https://media.giphy.com/media/vaucvLYaM7UrNJHsgy/giphy.gif"],
    "punch": ["https://media.giphy.com/media/NuiEoMDbstN0J2KAiH/giphy.gif"],
    "slap": ["https://media.giphy.com/media/WvzGVdiVRNq8qtWPKu/giphy.gif"],
    "tickle": ["https://media.giphy.com/media/l42PklIAdGA3l3fwI/giphy.gif"],
    "feed": ["https://tenor.com/view/eat-eats-eating-anime-anime-eat-gif-24362033.gif"],
    "pinch": ["https://media.giphy.com/media/MC7fYhbA4ociQ/giphy.gif"],
    "proud": ["https://tenor.com/view/reaction-proud-clapping-hands-tears-of-joy-gif-14452622.gif"],
    "bully": ["https://tenor.com/view/cyberbullying-cyberbully-typing-fast-anime-gif-25012932.gif"],
    "spank": ["https://tenor.com/view/rikka-takanashi-chunibyo-spanking-spank-anime-gif-18249073.gif"],
    "grape": ["https://tenor.com/view/chaika-eat-grape-feed-happy-gif-14855797.gif"],
    "lol": ["https://tenor.com/view/laughing-lol-slam-table-anime-cute-gif-17848238.gif"],
    "lmao": ["https://tenor.com/view/lol-lmao-laughing-hysterically-cat-gif-16935438.gif"],
    "counter": ["https://tenor.com/view/my-hero-academia-anime-fight-gif-17788396.gif"],
    "bankai": ["https://tenor.com/view/anime-bankai-bleach-gif-20300269.gif"],
    "revive": ["https://tenor.com/view/rezero-return-by-death-gif-19396459.gif"],
    "reverse": ["https://tenor.com/view/uno-reverse-card-gojo-gif-4379783580460628181.gif"],
    "rasengan": ["https://tenor.com/view/rasengan-naruto-gif-12801236794720890698.gif"],
    "explosion": ["https://tenor.com/view/konosuba-explosion-megumin-gif-16686316.gif"],

    # SOLO
    "baka": ["https://tenor.com/view/anime-baka-gif-10475156973113460459.gif"],
    "cry": ["https://tenor.com/view/luffy-crying-gif-11917699240308028632.gif"],
    "laugh": ["https://tenor.com/view/sukuna-laugh-gif-23588521.gif"],
    "smile": ["https://tenor.com/view/anime-smile-gif-6913843199269058193.gif"],
    "wink": ["https://tenor.com/view/anime-wink-gif-27563628.gif"],
    "panic": ["https://tenor.com/view/choso-jujutsu-kaisen-gif-10037971888755283102.gif"],
    "world": ["https://tenor.com/view/za-warudo-the-world-jojos-bizarre-adventures-jjba-anime-gif-17783696.gif"],
}

INTERACTIVE_LIST = [
    "bite","bonk","cuddle","hug","kick","kill","kiss","lick","pat","poke",
    "punch","slap","tickle","feed","pinch","proud","bully","spank","grape",
    "lol","lmao","counter","bankai","revive","reverse","rasengan","explosion"
]

VERBS = {
    "bite": "bit","bonk": "bonked","cuddle": "cuddled","hug": "hugged",
    "kick": "kicked","kill": "killed","kiss": "kissed","lick": "licked",
    "pat": "patted","poke": "poked","punch": "punched","slap": "slapped",
    "tickle": "tickled","feed": "fed","pinch": "pinched","proud": "praised",
    "bully": "bullied","spank": "spanked"
}

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_url = f"https://t.me/{BOT_USERNAME}?startgroup=true"
    keyboard = [[
        InlineKeyboardButton("➕ Add Me to Group", url=add_url),
        InlineKeyboardButton("📖 Help", callback_data="help")
    ]]
    await update.message.reply_text(
        "👋 **Anime Reaction Bot**\n\n"
        "Reply with `+reaction` to use actions.\n"
        "Example: `+hug`, `+world`",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ================= HELP =================
async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    interactive = sorted(INTERACTIVE_LIST)
    solo = sorted([k for k in GIFS if k not in INTERACTIVE_LIST])

    text = (
        "📖 **Help**\n\n"
        "🤝 **Interactive (reply required):**\n"
        f"`{'`, `'.join(interactive)}`\n\n"
        "🎭 **Solo:**\n"
        f"`{'`, `'.join(solo)}`"
    )
    await query.message.reply_text(text, parse_mode="Markdown")

# ================= REACTION HANDLER =================
async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text or not msg.text.startswith("+"):
        return

    command = msg.text[1:].lower()
    user = msg.from_user.first_name

    if command not in GIFS:
        return

    gif = random.choice(GIFS[command])

    if command in INTERACTIVE_LIST:
        if not msg.reply_to_message:
            await msg.reply_text("❌ Reply to someone!")
            return
        target = msg.reply_to_message.from_user.first_name
        caption = f"✨ {user} {VERBS.get(command, command+'ed')} {target}!"
    else:
        caption = f"💭 {user} is {command}ing..."

    await context.bot.send_animation(
        chat_id=msg.chat.id,
        animation=gif,
        caption=caption,
        reply_to_message_id=msg.message_id
    )

# ================= MAIN =================
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(help_button, pattern="help"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reaction_handler))
    app.run_polling()
