import os
import logging
from telegram.ext import Application, MessageHandler, filters
from google import genai
from telegram import Update
from telegram.ext import ContextTypes
from google.genai import types as genai_types

# ==========================================================
# သင်ပေးထားသော Token အသစ်နှင့် API Key အသစ်
BOT_TOKEN = "7022247360:AAGIUApvre2OkNcuHXvQLRPGjOCjmwrwIDw" 
GEMINI_API_KEY = "AIzaSyBolky-yf8ARHWUss-sfE7rYn_dw6AAFqg" 
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
        logger.info("✅ Gemini Client Started.")
    except Exception as e:
        logger.error(f"❌ Gemini Client Error: {e}")

async def gemini_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client or not update.message.text: return
    try:
        # Bot အမည်ကို YuKi V77 သို့ သတ်မှတ်ထားပါသည်
        system_instruction = "သင်၏အမည်မှာ YuKi V77 ဖြစ်သည်။"
        config = genai_types.GenerateContentConfig(system_instruction=system_instruction)
        
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=update.message.text,
            config=config
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"❌ API Error: {e}")
        await update.message.reply_text("ခေတ္တစောင့်ဆိုင်းပေးပါ။")

def main() -> None:
    if not BOT_TOKEN: return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gemini_chat))
    logger.info("🚀 Bot လည်ပတ်နေပါပြီ...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
    nder
