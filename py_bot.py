import logging
import os
from telegram.ext import ChatMemberHandler, filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler
import handlers
from dotenv import load_dotenv
load_dotenv()  # Loads environment variables from `.env` file

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    """ application.add_handler(CommandHandler('timer', handlers.callback_timer)) """
    application.add_handler(CommandHandler('start', handlers.start))
    application.add_handler(CommandHandler('chat_id', handlers.get_chat_id))
    application.add_handler(CommandHandler('confess', handlers.confess, filters=~filters.Entity("url")))
    application.add_handler(CommandHandler('confess', handlers.confess_without_link, filters=filters.Entity("url")))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handlers.greet_new_user))
    application.add_handler(CommandHandler('ban', handlers.ban_member))
    application.add_handler(CommandHandler('create_invite_link', handlers.create_invite_link))
    application.add_handler(CommandHandler('spurge', handlers.spurge))
    application.add_handler(CommandHandler('unban', handlers.unban_user))
    application.add_handler(CommandHandler('kick', handlers.kick_user))
    application.add_handler(CommandHandler('summary', handlers.summary))
    application.add_handler(MessageHandler(filters.COMMAND, handlers.unknown))
    # Start polling for updates
    application.run_polling()