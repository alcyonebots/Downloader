# 7070026696:AAF2ahAcrT7DUwr2bHnKoObu5mdO
import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Define the download function
def download_video(url):
    ydl_opts = {
        'cookiefile': 'cookies.txt',  # Update this path as needed
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,  # Prevent playlist downloading
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url)
        video_title = video_info['title']
        file_path = ydl.prepare_filename(video_info)
        ydl.download([url])
    
    return video_title, file_path

# Define the command handler for the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a link to download a video from Instagram, Facebook, or YouTube.")

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        video_title, file_path = download_video(url)
        update.message.reply_text(f'Downloaded: {video_title}')
        with open(file_path, 'rb') as video_file:
            update.message.reply_video(video_file, caption=f'Downloaded: {video_title}')
        
        # Optionally, delete the file after sending
        os.remove(file_path)
        
    except Exception as e:
        update.message.reply_text(f'Error: {str(e)}')

# Main function to start the bot
def main() -> None:
    updater = Updater("7070026696:AAF2ahAcrT7DUwr2bHnKoObu5mdO")  # Replace with your bot token

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # Create the downloads directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()
