AIzaSyBS32n9ZPpzuaf2ZzyvHVjui89C6TJAK58 os
import logging
from telegram.ext import Application, MessageHandler, filters
from google import genai
from telegram import Update
from telegram.ext import ContextTypes
from google.genai import types as genai_types

# ==========================================================
# သင်ပေးထားသော Token အသစ်နှင့် Gemini Key
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
        logger.info("✅ Gemini Client ကို အောင်မြင်စွာ စတင်ခဲ့ပါပြီ။")
    except Exception as e:
        logger.error(f"❌ Gemini Client Error: {e}")

async def gemini_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text("Gemini API Error!")
        return

    user_message = update.message.text
    if not user_message: return

    try:
        # Bot ရဲ့ ကိုယ်ပိုင်အမှတ်အသား သတ်မှတ်ချက်
        system_instruction = "သင်၏အမည်မှာ YuKi V77 ဖြစ်သည်။"
        config = genai_types.GenerateContentConfig(system_instruction=system_instruction)
        
        # အမှန်ကန်ဆုံး model name ကို အသုံးပြုထားပါသည်
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=user_message,
            config=config
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"❌ API Error: {e}")
        # Render တွင် Conflict မဖြစ်စေရန် Error တက်ပါက သတိပေးမည်
        await update.message.reply_text("ခေတ္တစောင့်ဆိုင်းပေးပါ၊ Server အလုပ်လုပ်နေပါသည်။")

def main() -> None:
    if not BOT_TOKEN: return
    application = Application.builder().token(BOT_TOKEN).build()
    
    # စာသားများကို လက်ခံဖြေကြားရန် Handler ထည့်သွင်းခြင်း
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gemini_chat))
    
    logger.info("🚀 Bot လည်ပတ်နေပါပြီ...")
    
    # Render တွင် Bot ကို ပုံမှန်အတိုင်း အမြဲတမ်း run ပေးထားမည့် စနစ်
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Render ၏ Startup Logic အမှန်
if __name__ == '__main__':
    main()
    



