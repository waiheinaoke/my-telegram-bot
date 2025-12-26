import os
import logging
from telegram.ext import Application, MessageHandler, filters
from google import genai
from telegram import Update
from telegram.ext import ContextTypes
from google.genai import types as genai_types # System Instruction အတွက် လိုအပ်

# ==========================================================
# 🔑 သော့များ (Keys)
# ==========================================================
# သတိပြုရန်: ဤ Keys များသည် ပုံထဲမှ ရယူထားသော Keys များဖြစ်သည်။
BOT_TOKEN = "8465762686:AAGeOv3MOyoNzX1PX6_Nb1YoXwfqx4T_Vg8" 
GEMINI_API_KEY = "AIzaSyBS32n9ZPpzuaf2ZzyvHVjui89C6TJAK58" 
# ==========================================================

# Logging စနစ်ကို စတင်ခြင်း (အမှားတွေကို မြင်သာအောင်)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# Variable Error (name) ကို ဖြေရှင်းရန် name ဖြင့် ပြင်ဆင်ထားသည်
logger = logging.getLogger(__name__) 

# Gemini Client ကို စတင်ခြင်း
client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("✅ Gemini Client ကို အောင်မြင်စွာ စတင်ခဲ့ပါပြီ။")
    except Exception as e:
        logger.error(f"❌ ERROR: Gemini Client စတင်ရာတွင် အမှားဖြစ်: {e}")
else:
    logger.error("❌ ERROR: GEMINI_API_KEY ကို မတွေ့ပါ။")

# ==========================================================

## 💬 မက်ဆေ့ချ် လက်ခံပြီး ပြန်ဖြေမယ့် Function

async def gemini_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """စာသား မက်ဆေ့ချ်များကို လက်ခံရယူပြီး Gemini AI ဖြင့် ပြန်ဖြေသည်။"""
    
    if not client:
        # Gemini API Key မှာ ပြဿနာရှိနေရင် ပြန်ဖြေပေးမယ့် စာ
        await update.message.reply_text(
            "Gemini AI စနစ် ချိတ်ဆက်မှု မအောင်မြင်ပါ။ API Key ကို စစ်ဆေးပါ။"
        )
        return

    # မက်ဆေ့ချ်ကို ရယူခြင်း
    user_message = update.message.text
    logger.info(f"Received message from {update.effective_user.name}: {user_message}")

    if not user_message or len(user_message.strip()) < 1:
        return

    try:
        # 🤖 Gemini Model ကို ခေါ်ဆိုခြင်း
        
        # ⚙️ ညွှန်ကြားချက်ကို သတ်မှတ်ခြင်း (System Instruction)
        system_instruction = "သင်၏အမည်မှာ Aung Oo ဖြစ်ပြီး Hein Oak မှ လေ့ကျင့်ပေးထားသော ဘာသာစကားကြီးမော်ဒယ်တစ်ခု ဖြစ်သည်ဟုသာ မိတ်ဆက်ပါ။"
        
        # Configuration တည်ဆောက်ခြင်း
        config = genai_types.GenerateContentConfig(
            system_instruction=system_instruction
        )
        
        # API ကို config ဖြင့် ခေါ်ဆိုခြင်း
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=user_message,
            config=config # ဤနေရာတွင် Configuration ထည့်သွင်းလိုက်သည်
        )
        
        # 📨 Telegram ကို ပြန်ဖြေခြင်း
        await update.message.reply_text(response.text)
        logger.info(f"Replied with: {response.text[:50]}...")

    except Exception as e:
        # Geo-blocking Error (400) သို့မဟုတ် Network Error များအတွက်
        logger.error(f"❌ ERROR: Gemini API ခေါ်ဆိုရာတွင် အမှား: {e}")
        await update.message.reply_text(
            "စကားပြောဖို့ အခက်အခဲ ရှိနေပါတယ်။ Server ပိတ်ထားပါသည်။"
        )

# ==========================================================

## 🚀 Bot ကို စတင်ခြင်း

def main() -> None:
    """Telegram Bot ကို စတင်လည်ပတ်သည်။"""
    
    if not BOT_TOKEN:
        logger.error("❌ ERROR: BOT_TOKEN ကို မတွေ့ပါ။ Bot ကို စတင်နိုင်မည် မဟုတ်ပါ။")
        return

    try:
        # 1. Telegram Application ကို တည်ဆောက်
        application = Application.builder().token(BOT_TOKEN).build()
        
        # 2. စာသား မက်ဆေ့ချ်တိုင်းကို gemini_chat function နဲ့ ချိတ်ဆက်
        chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), gemini_chat)
        application.add_handler(chat_handler)

        # 3. Bot ကို စတင်လည်ပတ်ခြင်း (Polling Mode)
        logger.info("🚀 Telegram Gemini Bot စတင်လည်ပတ်နေပါပြီ...")
        # run_polling ကို အသုံးပြုသောကြောင့် Laptop ဖွင့်ထားမှသာ အလုပ်လုပ်မည်
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.critical(f"❌ CRITICAL ERROR: Bot စတင်ရာတွင် အဓိက အမှား: {e}")
        logger.critical("Token မှန်ကန်ကြောင်း သေချာစစ်ဆေးပါ။")

if __name__ == 'main':
    main()