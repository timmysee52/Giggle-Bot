from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Sample in-memory storage for gigs
gig_list = []

# /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 Welcome to Giggle! Type /post to post a gig, or /browse to see gigs!")

# /post command
def post(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "📝 Please type your gig in this format:\n\n"
        "`Title | Description | Pay (RM)`\n\n"
        "Example:\n"
        "`Flyer Distributor | Hand out flyers in KLCC | 50`",
        parse_mode='Markdown'
    )

# Handle posted gigs
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    parts = text.split('|')

    if len(parts) != 3:
        update.message.reply_text("❌ Please follow the correct format: Title | Description | Pay (RM)")
        return

    title = parts[0].strip()
    description = parts[1].strip()
    try:
        pay = float(parts[2].strip())
    except ValueError:
        update.message.reply_text("❌ Pay must be a number (e.g. 50)")
        return

    gig = {'title': title, 'description': description, 'pay': pay}
    gig_list.append(gig)

    update.message.reply_text("✅ Your gig has been posted!")

# /browse command
def browse(update: Update, context: CallbackContext) -> None:
    if not gig_list:
        update.message.reply_text("😕 No gigs available yet. Check back later!")
        return

    for gig in gig_list:
        msg = (
            f"📢 *{gig['title']}*\n"
            f"📝 {gig['description']}\n"
            f"💰 RM{gig['pay']}"
        )
        update.message.reply_text(msg, parse_mode='Markdown')

# Main function
def main():
    updater = Updater("YOUR_BOT_TOKEN_HERE", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("post", post))
    dispatcher.add_handler(CommandHandler("browse", browse))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("🤖 Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

