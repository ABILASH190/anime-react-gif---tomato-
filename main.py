import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive

# ===== BOT TOKEN =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== GIF DATABASE =====
GIFS = {
    # Interactive commands
    "bite": ["https://media.tenor.com/1.gif"],
    "bonk": ["https://media.tenor.com/2.gif"],
    "cuddle": ["https://media.tenor.com/3.gif"],
    "hug": ["https://media.tenor.com/4.gif"],
    "kick": ["https://media.tenor.com/5.gif"],
    "kill": ["https://media.tenor.com/6.gif"],
    "kiss": ["https://media.tenor.com/7.gif"],
    "lick": ["https://media.tenor.com/8.gif"],
    "pat": ["https://media.tenor.com/9.gif"],
    "poke": ["https://media.tenor.com/10.gif"],
    "punch": ["https://media.tenor.com/11.gif"],
    "slap": ["https://media.tenor.com/12.gif"],
    "tickle": ["https://media.tenor.com/13.gif"],
    "feed": ["https://media.tenor.com/14.gif"],
    "pinch": ["https://media.tenor.com/15.gif"],
    "proud": ["https://media.tenor.com/16.gif"],
    "bully": ["https://media.tenor.com/17.gif"],
    "spank": ["https://media.tenor.com/18.gif"],
    "grape": ["https://media.tenor.com/19.gif"],

    # Anime Attacks
    "counter": ["https://media.tenor.com/20.gif"],
    "bankai": ["https://media.tenor.com/21.gif"],
    "revive": ["https://media.tenor.com/22.gif"],
    "reverse": ["https://media.tenor.com/23.gif"],
    "rasengan": ["https://media.tenor.com/24.gif"],
    "amaterasu": ["https://media.tenor.com/25.gif"],
    "chidori": ["https://media.tenor.com/26.gif"],
    "kamehameha": ["https://media.tenor.com/27.gif"],
    "getsuga": ["https://media.tenor.com/28.gif"],
    "bankai2": ["https://media.tenor.com/29.gif"],

    # Express Yourself
    "baka": ["https://media.tenor.com/30.gif"],
    "blush": ["https://media.tenor.com/31.gif"],
    "clap": ["https://media.tenor.com/32.gif"],
    "cry": ["https://media.tenor.com/33.gif"],
    "cute": ["https://media.tenor.com/34.gif"],
    "dance": ["https://media.tenor.com/35.gif"],
    "fumo": ["https://media.tenor.com/36.gif"],
    "laugh": ["https://media.tenor.com/37.gif"],
    "meme": ["https://media.tenor.com/38.gif"],
    "neko": ["https://media.tenor.com/39.gif"],
    "rage": ["https://media.tenor.com/40.gif"],
    "sad": ["https://media.tenor.com/41.gif"],
    "scary": ["https://media.tenor.com/42.gif"],
    "shy": ["https://media.tenor.com/43.gif"],
    "sleep": ["https://media.tenor.com/44.gif"],
    "smile": ["https://media.tenor.com/45.gif"],
    "smug": ["https://media.tenor.com/46.gif"],
    "stare": ["https://media.tenor.com/47.gif"],
    "vibe": ["https://media.tenor.com/48.gif"],
    "wink": ["https://media.tenor.com/49.gif"],
    "wow": ["https://media.tenor.com/50.gif"],
    "wtf": ["https://media.tenor.com/51.gif"],
    "lol": ["https://media.tenor.com/52.gif"],
    "yawn": ["https://media.tenor.com/53.gif"],
    "smoke": ["https://media.tenor.com/54.gif"],
    "afk": ["https://media.tenor.com/55.gif"],
    "hi": ["https://media.tenor.com/56.gif"],
    "pushup": ["https://media.tenor.com/57.gif"],
    "sus": ["https://media.tenor.com/58.gif"],
    "goon": ["https://media.tenor.com/59.gif"],
    "enough": ["https://media.tenor.com/60.gif"],
    "lmao": ["https://media.tenor.com/61.gif"],
    "eww": ["https://media.tenor.com/62.gif"],
    "cringe": ["https://media.tenor.com/63.gif"]
}

INTERACTIVE = [
    "bite","bonk","cuddle","hug","kick","kill","kiss","lick","pat","poke",
    "punch","slap","tickle","feed","pinch","proud","bully","spank","grape"
]

EXPRESS = [
    "baka","blush","clap","cry","cute","dance","fumo","laugh","meme","neko",
    "rage","sad","scary","shy","sleep","smile","smug","stare","vibe","wink",
    "wow","wtf","lol","yawn","smoke","afk","hi","pushup","sus","goon","enough",
    "lmao","eww","cringe"
]

ATTACKS = [
    "counter","bankai","revive","reverse","rasengan","amaterasu",
    "chidori","kamehameha","getsuga","bankai2"
]

# ===== HANDLER =====
async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    text = msg.text.strip()
    if not text.startswith("+"):
        return

    command = text[1:].lower()
    user = msg.from_user.first_name

    # Interactive (need reply)
    if command in INTERACTIVE and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        gif = random.choice(GIFS.get(command, []))
        caption = f"💞 {user} {command}ed {target}"
        await context.bot.send_animation(chat_id=msg.chat.id, animation=gif, caption=caption)

    # Express (no reply needed)
    elif command in EXPRESS:
        gif = random.choice(GIFS.get(command, []))
        caption = f"💭 {user} is {command}"
        await context.bot.send_animation(chat_id=msg.chat.id, animation=gif, caption=caption)

    # Attacks (need reply)
    elif command in ATTACKS and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        gif = random.choice(GIFS.get(command, []))
        caption = f"💥 {user} used **{command.upper()}** on {target}!"
        await context.bot.send_animation(chat_id=msg.chat.id, animation=gif, caption=caption)


    command = msg.text[1:].lower()
    user = msg.from_user.first_name

    # Interactive commands
    if command in INTERACTIVE and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        gif = random.choice(GIFS.get(command, []))
        caption = f"💞 {user} {command}ed {target}"
        await context.bot.send_animation(chat_id=msg.chat.id, animation=gif, caption=caption)

    # Express yourself
    elif command in EXPRESS:
        gif = random.choice(GIFS.get(command, []))
        caption = f"💭 {user} is {command}"
        await context.bot.send_animation(chat_id=msg.chat.id, animation=gif, caption=caption)

    # Anime attacks
    elif command in ATTACKS and msg.reply_to_message:
        target = msg.reply_to_message.from_user.first_name
        gif = random.choice(GIFS.get(command, []))
        caption = f"💥 {user} used **{command.upper()}** on {target}!"
        await context.bot.send_animation(chat_id=msg.chat.id, animation=gif, caption=caption)

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am Anime Reaction Bot!\nUse +commands like +hug, +rasengan, +cry etc."
    )

# ===== Start Bot =====
keep_alive()
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(
        filters.TEXT & (~filters.COMMAND),  # handle all text except /commands
        reaction_handler
    )
)

app.run_polling()
