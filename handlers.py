import logging
import asyncio
from telegram import ChatMember, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ChatMemberHandler, filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler
from uuid import uuid4
import os
import telegram.ext
from dotenv import load_dotenv
load_dotenv()

logger = logging.basicConfig(
        filename = 'app.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

logger = logging.getLogger(__name__)  # __name__ will set the logger's name to the module name

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("%s started the bot", update.effective_user.username)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def callback_alarm(context: ContextTypes.DEFAULT_TYPE):
    # Beep the person who called this alarm:
    job_data = context.job.data
    await context.bot.send_message(chat_id = context.job.chat_id, text=f'BEEP!', reply_to_message_id = job_data["message_id"])
 
async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    await context.bot.send_message(chat_id=chat_id, text='Setting a timer for 1 minute!')
    # Set the alarm:
    context.job_queue.run_once(callback_alarm, 60, data={"message_id": message_id}, chat_id=chat_id)

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f"Chat ID: {chat_id}")

async def confess(update:Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s made a confession", update.effective_user.username)
    channel_id = os.getenv("CHANNEL_ID") 
    confession_text = ' '.join(context.args)
    confession_number = context.chat_data.get("confession_number", 22)
    global confessions_made
    if confession_text:
        sent_message = await context.bot.send_message(chat_id=channel_id, text=f"#Confession_{confession_number} \n {confession_text}")
        context.chat_data["confession_number"] = confession_number + 1
        forwarded_message_id = sent_message.message_id
        message_link = f"https://t.me/{channel_id[1:]}/{forwarded_message_id}"
        await context.bot.send_message(chat_id = update.effective_chat.id, text=f"Confession made!, view it [here]({message_link})", reply_to_message_id=update.message.message_id, parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a confession after /confess.", reply_to_message_id=update.message.message_id)

async def greet_new_user(update:Update, context:ContextTypes.DEFAULT_TYPE):
    for new_member in update.effective_message.new_chat_members:
        if not new_member.is_bot:
            welcome_message = f"Hello {new_member.first_name}! Welcome to the chat!"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

async def ban_member(update:Update, context:ContextTypes.DEFAULT_TYPE):
    admin_list = await context.bot.get_chat_administrators(update.effective_chat.id)
    user_id = update.message.from_user.id
    if user_id in admin_list:
        user_to_ban_name= update.message.reply_to_message.from_user.first_name
        user_to_ban_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_to_ban_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{user_to_ban_name} banned from chat.")
    else:
        await update.message.reply_text(f"You need to be an admin to do this.")

async def unban_user(update: Update, context:ContextTypes.DEFAULT_TYPE):
    user_to_unban_id = update.message.reply_to_message.from_user.id
    admin_list = await context.bot.get_chat_administrators(update.effective_chat.id)
    user_id = update.message.from_user.id
    if user_id in admin_list:
        try:
            await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id= user_to_unban_id, only_if_banned=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"User unbanned.")
            
        except telegram.error.BadRequest as e:
            if "user is not banned" in str(e):
                context.bot.send_message(chat_id=update.effective_chat.id, text="User is not banned.")
            else:
                raise e

async def kick_user(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_to_kick_id = update.message.reply_to_message.from_user.id
    admin_list = await context.bot.get_chat_administrators(update.effective_chat.id)
    user_id = update.message.from_user.id
    if user_id in admin_list:
        await context.bot.kick_chat_member(chat_id=update.effective_chat.id, user_id=user_to_kick_id)
        await context.bot.send_message(chat_id= update.effective_chat.id, text=f"{update.message.from_user.first_name} kicked {update.message.reply_to_message.from_user.first_name}")
    else:
        await update.message.reply_text("You need to be an admin to do this.")

async def create_invite_link(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        invite_link = await context.bot.create_chat_invite_link(chat_id=update.effective_chat.id)
        invite_link_url = invite_link.invite_link
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Here is the chat's invite link, {invite_link_url}")
    except telegram.error.TelegramError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error creating invite link: {e}")

async def spurge(update:Update, context:ContextTypes.DEFAULT_TYPE):
    message_ids = []
    replied_to_message_id = update.effective_message.reply_to_message.message_id 
    new_message_id = update.effective_message.message_id
    for message_id in range(replied_to_message_id, new_message_id):
        message_ids.append(int(message_id))
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if chat_member.status not in ('administrator', 'creator'):
        await context.bot.reply_text("You need to be an admin to use this command.")
    try:
        await context.bot.delete_messages(chat_id=update.effective_chat.id, message_ids=message_ids)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Messages deleted successfully.")
    except telegram.error.TelegramError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error deleting messages: {e}")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didnt understand that command.")

