import os
import logging
from telegram.ext import Application, MessageHandler, filters
from google import genai
from telegram import Update
from telegram.ext import ContextTypes
from google.genai import types as genai_types

# ==========================================================
BOT_TOKEN = "8465762686:AAGeOv3MOyoNzX1PX6_Nb1YoXwfqx4T_Vg8" 
GEMINI_API_KEY = "AIzaSyBS32n9ZPpzuaf2ZzyvHVjui89C6TJAK58" 
# ==========================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__) 

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("✅ Gemini Client ကို စတင်ခဲ့ပါပြီ။")
    except Exception as e:
        logger.error(f"❌ Gemini Client Error: {e}")

async def gemini_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text("Gemini API Error!")
        return

    user_message = update.message.text
    if not user_message: return

    try:
        system_instruction = "သင်၏အမည်မှာ Aung Oo ဖြစ်သည်။"
        config = genai_types.GenerateContentConfig(system_instruction=system_instruction)
        
        # အမှန်ပြင်ထားသော model name: gemini-1.5-flash
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=user_message,
            config=config
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"❌ API Error: {e}")
        await update.message.reply_text("Server အခက်အခဲ ရှိနေပါသည်။")

def main() -> None:
    if not BOT_TOKEN: return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gemini_chat))
    
    logger.info("🚀 Bot လည်ပတ်နေပါပြီ...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Render အတွက် အမှန်ပြင်ထားသော startup logic
if __name__ == '__main__':
    main()
