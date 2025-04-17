# -*- coding: utf-8 -*-

# giggle_bot.py - Starter Telegram Bot for Giggle Platform

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Dictionary to simulate a simple in-memory database
gig_list = []

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Giggle – Earn. Learn. Giggle."

"Type /post to post a gig or /browse to find one!"
    )

# Post a gig command
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Please type your gig in the following format:\nJob Title | Location | Pay | Time")

# Capture gig info
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if '|' in update.message.text:
        parts = update.message.text.split('|')
        if len(parts) == 3:
            title, desc, pay = map(str.strip, parts)
            gig = {
                'title': title,
                'desc': desc,
                'pay': pay,
                'posted_by': update.message.from_user.username or update.message.from_user.first_name
            }
            gig_list.append(gig)
            await update.message.reply_text("✅ Gig posted!")
        else:
            await update.message.reply_text("❌ Please follow the correct format: Title | Description | Pay (RM)")
    else:
        await update.message.reply_text("❌ Please follow the correct format: Title | Description | Pay (RM)")

# Browse gigs
async def browse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not gig_list:
        await update.message.reply_text("😕 No gigs available yet. Check back later!")
        return

    for gig in gig_list:
        msg = (
    f"📢 *{gig['title']}*\n"
    f"📍 Location: {gig['location']}\n"
    f"Pay: {gig['pay']}\n"
    f"🕒 Time: {gig['time']}"
)
{gig['desc']}
"RM{gig['pay']} | Posted by: {gig['posted_by']}"
  await update.message.reply_text(msg, parse_mode='Markdown')

# Bot setup
def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CommandHandler("browse", browse))
    app.add_handler(CommandHandler("help", start))  # reuse start for help
    app.add_handler(CommandHandler("giggle", start))  # playful extra command
    app.add_handler(MessageHandler(None, handle_message))
    print("✅ Giggle Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
