import os,logging,requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ocr.find_name import process_image_and_search
from med._1mg_script import get_medicine_info

load_dotenv()
YOUR_BOT_TOKEN = os.getenv("YOUR_BOT_TOKEN")
# print(YOUR_BOT_TOKEN)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi there! Welcome to the Prescription Pro! 🩺\n\n"
                                    "📸 Send me an image of a prescription, and I'll extract the medicine details for you.\n"
                                    )
    
    await update.message.reply_text("ℹ️ *How to Use This Bot*:\n"
                                    "1️⃣ Send a photo of a prescription 📸.\n"
                                    "2️⃣ I'll extract the medicines and provide details 📝.\n"
                                    "3️⃣ Get accurate medicine information including prices and links 🔗.\n"
                                    "\nGive it a try!")

# Handler for extracting medicines from an image
async def extract_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Check if a photo is sent
        if not update.message.photo:
            await update.message.reply_text("❌ Please send a photo of the prescription 📸.")
            return

        # Get the highest resolution image
        file_id = update.message.photo[-1].file_id
        file = await context.bot.get_file(file_id)
        
        # Download the file locally
        local_file_path = "downloaded_image.jpg"
        response = requests.get(file.file_path)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as f:
                f.write(response.content)
            await update.message.reply_text("✅ Image received! Extracting medicines... 🕵️‍♂️")

            # Process the downloaded image
            medicines = process_image_and_search(local_file_path)

            # Delete the file after processing
            os.remove(local_file_path)

        if not medicines:
            await update.message.reply_text("❌ Sorry, I couldn't recognize any medicines. Try again! 🧐")
            return
        
        medicines_list = "\n".join([f"{i+1}. {med}" for i, med in enumerate(medicines)])
        await update.message.reply_text(
        f"🎉 *Found Medicines*:\n{medicines_list}\n\nFetching details from 1mg... 🛒", parse_mode="Markdown")
       
        city = "Gurgaon" #by default  
        all_results = []
        for medicine in medicines:
            results = get_medicine_info(medicine, city)
            all_results.extend(results)

        if not all_results:
            await update.message.reply_text("No details found for the medicines. Please try again later.")
            return

        for result in all_results:
            message = (
                f"Name: {result['name']}\n"
                f"Label: {result['label']}\n"
                f"Price: ₹{result['discounted_price']}\n"
                f"Link: {result['url']}"
            )
            await update.message.reply_text(message)

    except Exception as e:
        logger.error(f"Error in extract_image: {e}")
        await update.message.reply_text("❌❌❌An error occurred while processing the image. Please try again.")

async def invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ I'm not sure what you mean. Use /start or /help to get started! 🤗")

def main():
    application = Application.builder().token(YOUR_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, extract_image))
    application.add_handler(MessageHandler(filters.COMMAND, invalid_command))

    application.run_polling()

if __name__ == "__main__":
    main()