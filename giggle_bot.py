from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Sample in-memory storage for gigs
gig_list = []

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Giggle! Type /post to post a gig, or /browse to see gigs!")

# /post command
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Please type your gig in this format:\n\n"
        "`Title | Description | Pay (RM)`\n\n"
        "Example:\n"
        "`Flyer Distributor | Hand out flyers in KLCC | 50`",
        parse_mode='Markdown'
    )

# Handle posted gigs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split('|')

    if len(parts) != 3:
        await update.message.reply_text("❌ Please follow the correct format: Title | Description | Pay (RM)")
        return

    title = parts[0].strip()
    description = parts[1].strip()
    try:
        pay = float(parts[2].strip())
    except ValueError:
        await update.message.reply_text("❌ Pay must be a number (e.g. 50)")
        return

    gig = {'title': title, 'description': description, 'pay': pay}
    gig_list.append(gig)

    await update.message.reply_text("✅ Your gig has been posted!")

# /browse command
async def browse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not gig_list:
        await update.message.reply_text("😕 No gigs available yet. Check back later!")
        return

    for gig in gig_list:
        msg = (
            f"📢 *{gig['title']}*\n"
            f"📝 {gig['description']}\n"
            f"💰 RM{gig['pay']}"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

# Main function
if __name__ == '__main__':
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CommandHandler("browse", browse))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

