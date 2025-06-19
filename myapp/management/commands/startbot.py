from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = 'http://localhost:8000'  # Adjust if deployed

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your Django bot. Send /check to query the protected API.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the chat ID
    chat_id = update.message.chat_id
    # Use the token from .env or a hardcoded test token (replace with secure method later)
    token = os.getenv('SECRET_KEY')  # Use a proper token management system
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/protected/', headers=headers)
    if response.status_code == 200:
        await update.message.reply_text(f"API Response: {response.json()['message']}")
    else:
        await update.message.reply_text(f"API Error: {response.status_code} - {response.text}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    token = os.getenv('API_TOKEN')
    if not token:
        await update.message.reply_text("Error: API_TOKEN not found in .env")
        return
    headers = {'Authorization': f'Token {token}'}
    await update.message.reply_text(f"Debug: Using token {token}")  # Add this line
    response = requests.get(f'{BASE_URL}/protected/', headers=headers, timeout=10)
    if response.status_code == 200:
        await update.message.reply_text(f"API Response: {response.json()['message']}")
    else:
        await update.message.reply_text(f"API Error: {response.status_code} - {response.text}")
        
class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("check", check))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        application.run_polling()