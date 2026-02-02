import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from telegram.ext import CallbackQueryHandler

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


        await query.message.reply_text(help_text, parse_mode="Markdown")


# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "animereacttomotobot" 

# ================= GIF DATABASE =================
# ✅ Add your GIF URLs inside the lists below.
GIFS = {
    # INTERACTIVE
    "bite": ["https://media.giphy.com/media/OqQOwXiCyJAmA/giphy.gif"],
    "bonk": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2sybWtzY3RiYWI0ZnE2ZjN2OG9vMjd5cmF1M3l1NjQ3NW1paDd2dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/gsyDSxD5mpBdKftDLq/giphy.gif"],
    "cuddle": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDloZGxnOHplZTd5azFoa3F5bTN6cWNndTBtMGc5eHh0ZnI0MHljbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PHZ7v9tfQu0o0/giphy.gif"],
    "hug": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnhsM2U4dWQ0a3lrY2NrZ29zaWV0MmF5c2RhZHA0eGdlOWF4bzVucyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ZQN9jsRWp1M76/giphy.gif"],
    "kick": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3EwNnVpdmI3Nm1uZm50em5kNXc0b3F5ejA3ZDhkaG1pcW9xdXVwbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/u2LJ0n4lx6jF6/giphy.gif"],
    "kill": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTVpeWJmOTNqOG4zcG1manlpZGxqazdvcG12d2twZnVnNTRlbjBxbCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/puNw5dA8Vm1NrA2boJ/giphy.gif"],
    "kiss": ["https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Y3FjNnZpZmg3cG1kcHNpZ2JqMWN5a2w3dzJmMnkwYzEzOHJxa2N6ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dKBES1ypGwZdyFQBQ7/giphy.gif"],
    "lick": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmpvN2FhYzVsZXNmd2hxdHY1a3o2emE1aHo4anhsbGF2eGpic3Q0ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/DTbmKtrYbwUkw1Inyv/giphy.gif"],
    "pat": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3ppbzUxYjFxaWRlYWJpYTR4YjM2cWk2bmw5d3VyMzl3MWdpZzk1YSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5tmRHwTlHAA9WkVxTU/giphy.gif"],
    "poke": ["https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aXRscHZjbnk4aTE4a2FsMXBtYnU3MG8xdDVlZWh4Ym5na3JzamNkYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vaucvLYaM7UrNJHsgy/giphy.gif"],
    "punch": ["https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YzAwcHRjbXRicGU1M2duM2MyMWR1MmR3aHdvcG05ZmRqemMzbGhnMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/NuiEoMDbstN0J2KAiH/giphy.gif"],
    "slap": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNW91eGdibW1naTBoZ3c0dXI4cTkxNDlvbmRsMnBvc3RoNWtkN2dqdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WvzGVdiVRNq8qtWPKu/giphy.gif"],
    "tickle": ["https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3djg1a25tMWttcmRyN2h1MXppam0wNnhsNnAxN2dqNjQ4NXJ3bnppaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l42PklIAdGA3l3fwI/giphy.gif"],
    "feed": ["https://tenor.com/view/eat-eats-eating-anime-anime-eat-gif-24362033.gif"],
    "pinch": ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDRienRxc3loM2NzbzZqczI4bjdpdmVydWMwcmkzMml5ZXgwNWRxbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MC7fYhbA4ociQ/giphy.gif"],
    "proud": ["https://tenor.com/view/reaction-proud-clapping-hands-tears-of-joy-gif-14452622.gif"],
    "bully": ["https://tenor.com/view/cyberbullying-cyberbully-typing-typing-fast-anime-gif-25012932.gif"],
    "spank": ["https://tenor.com/view/rikka-takanashi-chunibyo-spanking-spank-anime-gif-18249073.gif"],
    "grape": ["https://tenor.com/view/chaika-eat-grape-feed-happy-gif-14855797.gif"],
    "lol": ["https://tenor.com/view/laughing-lol-slam-table-anime-cute-gif-17848238.gif"],
    "lmao": ["https://tenor.com/view/lol-lmao-laughing-hysterically-cat-gif-16935438.gif"],
    "counter": ["https://tenor.com/view/my-hero-academia-boku-anime-fight-battle-gif-17788396.gif"],
    "bankai": ["https://tenor.com/view/anime-bankai-bleach-gif-20300269.gif"],
    "revive": ["https://tenor.com/view/rezero-natsukisubaru-subaru-returnbydeath-gif-19396459.gif"],
    "reverse": ["https://tenor.com/view/satoru-gojo-jujutsu-kaisen-meme-uno-reverse-card-gif-4379783580460628181.gif"],
    "rasengan": ["https://tenor.com/view/50-fps-ナルト疾風伝-minato-namikaze-波風-gif-12801236794720890698.gif"],
    "explosion": ["https://tenor.com/view/konosuba-megumim-explosion-magic-anime-gif-16686316.gif"],

    # EXPRESSIONS (solo reactions)
    "baka": ["https://tenor.com/view/anime-baka-gif-10475156973113460459.gif"], "blush": ["https://tenor.com/view/my-dress-up-darling-my-dress-up-darling-s2-my-dress-up-darling-season-2-oceanicsx0-sono-bisque-doll-wa-koi-wo-suru-gif-4415441381493507146.gif"], "clap": ["https://tenor.com/view/sumi-sakurasawa-rent-a-girlfriend-anime-kanojo-okarishimasu-applause-gif-10524211690874500930.gif"], "cry": ["https://tenor.com/view/luffy-crying-gif-11917699240308028632.gif"], "cute": ["https://tenor.com/view/anime-tyan-girl-red-eyes-grey-hair-gif-440635602884634984.gif"],
    "dance": ["https://tenor.com/view/kakashi-dancing-naruto-anime-meme-gif-20691646.gif"], "fumo": ["https://tenor.com/view/smoking-gif-9745930313517122415.gif"], "laugh": ["https://tenor.com/view/sukuna-laugh-gif-23588521.gif"], "meme": ["https://tenor.com/view/absolute-cinema-sukuna-absolute-cinema-peak-cinema-gif-8953307231977611719.gif"], "neko": ["https://tenor.com/view/cat-dance-gif-25191017.gif"],
    "rage": ["https://tenor.com/view/aot-snk-erwin-smith-erwin-my-soldiers-gif-22330014.gif"], "sad": ["https://tenor.com/view/naruto-boruto-kakashi-kakashi-hatake-hatake-kakashi-gif-8171121379189437850.gif"], "scary": ["https://tenor.com/view/my-dress-up-darling-anime-scared-marin-kitagawa-gif-25223508.gif"], "shy": ["https://tenor.com/view/k-on-finger-point-yui-gif-5231586054704884072.gif"], "sleep": ["https://tenor.com/view/anime-sleep-sleepy-sleep-anime-goodnight-gif-11015724185220889541.gif"],
    "smile": ["https://tenor.com/view/kaoruko-waguri-the-fragrant-flower-blooms-with-dignity-kaoru-hana-wa-rin-to-saku-anime-girl-gif-6913843199269058193.gif"], "smug": ["https://tenor.com/view/smug-anime-nisekoi-false-love-smirk-gif-16228071.gif"], "stare": ["https://tenor.com/view/zenitsu-demon-slayer-anime-stare-angry-gif-11078347661675215665.gif"], "vibe": ["https://tenor.com/view/mateo-vibe-mateo-check-gif-25409606.gif"], "wink": ["https://tenor.com/view/starful-gif-27563628.gif"],
    "wow": ["https://tenor.com/view/anime-wow-sparkle-gif-10371761865050651714.gif"], "wtf": ["https://tenor.com/view/cute-anime-girl-kawaii-confused-gif-21196743.gif"], "yawn": ["https://tenor.com/view/me-when-im-bored-of-doing-it-again-and-again-gif-26673650.gif"], "smoke": ["https://tenor.com/view/anime-smoke-smoking-anime-girl-cute-gif-7708154617974967102.gif"], "afk": ["https://tenor.com/view/brb-gif-21428855.gif"],
    "pushup": ["https://tenor.com/view/push-up-okarun-dandadan-anime-boy-gif-13040120851751229965.gif"], "hi": ["https://tenor.com/view/akane-kurokawa-kurokawa-akane-oshi-no-ko-oshi-no-ko-season-2-episode-2-gif-7639923574130663404.gif"], "sus": ["https://tenor.com/view/sus-pretty-sus-anime-girl-pink-anime-pink-gif-9671833639381266400.gif"], "goon": ["https://tenor.com/view/anime-gif-21859388.gif"], "enough": ["https://tenor.com/view/einar-vinland-saga-season-2-farmland-arc-gif-918389513692373663.gif"],
    "eww": ["https://tenor.com/view/anime-spy-x-family-anya-what-the-what-the-hell-gif-25812280.gi"], "cringe": ["https://tenor.com/view/citrus-anime-matsuri-gif-25617935.gif"], "panic": ["https://tenor.com/view/choso-choso-jjk-choso-jujutsu-kaisen-choso-anime-jujutsu-kaisen-gif-10037971888755283102.gif"], 
    "world":  ["https://tenor.com/view/za-warudo-the-world-jojos-bizarre-adventures-jjba-anime-gif-17783696.gif"]

}

INTERACTIVE_LIST = [
    "bite", "bonk", "cuddle", "hug", "kick", "kill", "kiss", "lick", "pat", 
    "poke", "punch", "slap", "tickle", "feed", "pinch", "proud", "bully", 
    "spank", "grape", "lol", "lmao", "counter", "bankai", "revive", "reverse", 
    "rasengan", "explosion"
]

# Grammar captions for interactive actions
VERBS = {
    "hug": "hugged", "slap": "slapped", "pat": "patted", 
    "bite": "bit", "kiss": "kissed", "poke": "poked",
    "punch": "punched", "kick": "kicked", "kill": "killed",
    "lick": "licked", "pinch": "pinched", "tickle": "tickled",
    "bonk": "bonked", "cuddle": "cuddled", "feed": "fed",
    "spank": "spanked", "bully": "bullied"
}

# ================= HANDLERS =================

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
            "Example: `+hug`, `+slap`, `+pat`",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or not msg.text.startswith("+"):
        return

    parts = msg.text[1:].lower().split()
    command = parts[0]
    user_name = msg.from_user.first_name

    # Debug prints to help see issues
    print("Command typed:", command)
    print("GIFS keys:", list(GIFS.keys()))
    print("GIFS[command]:", GIFS.get(command))

    if command not in GIFS:
        return

    if not GIFS[command]:
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



# ================= RUN =================
if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reaction_handler))
    app.add_handler(CallbackQueryHandler(help_button, pattern="help"))
if __name__ == "__main__":
    app.run_polling()

        )
    

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
