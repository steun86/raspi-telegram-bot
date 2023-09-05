import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import subprocess

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def space(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #get free space on disk
    free_space = subprocess.run(["df", "-h", "/"], capture_output=True).stdout.decode("utf-8")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=free_space)

async def magnet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # check if it is a magnet link
    if update.message.text.startswith("magnet:?xt=urn:btih:"):
        # add magnet link to qbittorrent
        subprocess.run(["qbittorrent-nox", update.message.text]) 
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Magnet link added to qbittorrent")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Not a magnet link")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6315327775:AAFO8HFxs4UIxdxW_WkLKXUcgD2l132AAcQ').build()
    
    space_handler = CommandHandler('space', space)
    magnet_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), magnet)
    application.add_handler(space_handler)
    application.add_handler(magnet_handler)
    application.run_polling()