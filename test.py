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

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("𝗦𝗲𝗻𝗱 𝗺𝗲 𝗮 𝗹𝗶𝗻𝗸 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗮 𝘃𝗶𝗱𝗲𝗼 𝗳𝗿𝗼𝗺 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗼𝗿 𝗬𝗼𝘂𝗧𝘂𝗯𝗲...")

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        video_title, file_path = download_video(url)
        update.message.reply_text('𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱: {video_title}')
        with open(file_path, 'rb') as video_file:
            update.message.reply_video(video_file, caption='𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱: {video_title}')
        
        # Optionally, delete the file after sending
        os.remove(file_path)
        
    except Exception as e:
        update.message.reply_text(f'Error: {str(e)}')

def main() -> None:
    updater = Updater("7373160480:AAEg-hW3KrPGxmp7yYroHccHezvsfAQmr1c") 

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()
