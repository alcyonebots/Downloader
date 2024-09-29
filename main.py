import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Global variable to store message object
progress_message = None

# Define the download function
def download_video(url, update):
    ydl_opts = {
        'cookiefile': 'cookies.txt',  # Update this path as needed
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,  # Prevent playlist downloading
        'retries': 10,  # Retry downloading in case of failure
        'timeout': 600,  # Timeout for long downloads
        'continuedl': True,  # Resume downloads if possible
        'progress_hooks': [lambda d: progress_hook(d, update)]  # Hook for download progress
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url)
        video_title = video_info['title']
        file_path = ydl.prepare_filename(video_info)
        ydl.download([url])
    
    return video_title, file_path

# Progress hook to show download progress
def progress_hook(d, update):
    global progress_message
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        eta = d['eta']
        speed = d['_speed_str']
        message_text = f"Downloading... {percent} complete. Speed: {speed}. ETA: {eta} seconds."
        
        # Print progress in console
        print(message_text)

        # Send progress to the user
        if progress_message is None:  # First update, send a new message
            progress_message = update.message.reply_text(message_text)
        else:  # Edit the existing progress message
            progress_message.edit_text(message_text)
    
    if d['status'] == 'finished':
        print("Download completed.")
        if progress_message:
            progress_message.edit_text("Download completed.")
            progress_message = None  # Reset after completion

# Updated start function with image and caption
def start(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.get_me().username  # Get the bot's username
    
    keyboard = [
        [
            InlineKeyboardButton("Join Channel", url="https://t.me/alcyonebots"),
            InlineKeyboardButton("Join Support", url="https://t.me/alcyone_support")
        ],
        [
            InlineKeyboardButton("Add me to your groups +", url=f"https://t.me/{bot_username}?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://i.imghippo.com/files/OTItE1727595318.jpg"
    
    # Send the image with the caption
    update.message.reply_photo(
        photo=image_url,
        caption=(
            "𝗛𝗶 𝘁𝗵𝗲𝗿𝗲 👋🏻\n"
            "Welcome to 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, your go-to bot for downloading high-quality content from Instagram and Youtube!! 🎬\n"
            "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
            "◎ Start a chat with @AlcDownloaderBot and send /start\n"
            "◎ Add me to your group send /start then send the link of the short/reel by replying to my message.\n\n"
            "Join our channel and support group from the buttons given below‼️ \n\n"
            "Let's Get Started 👾"
        ),
        reply_markup=reply_markup
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    # Ensure update.message and update.message.text exist before proceeding
    if not update.message or not update.message.text:
        print(f"Received non-text update: {update}")
        return

    url = update.message.text.strip()

    # Check if the URL is from YouTube or Instagram
    if url.startswith("http") and ("youtube.com" in url or "instagram.com" in url):
        try:
            video_title, file_path = download_video(url, update)
            update.message.reply_text(f' Successfully Downloaded!{video_title}\n\n'
                                      'Wait a few seconds to get your video🎬')
            with open(file_path, 'rb') as video_file:
                update.message.reply_video(video_file, caption=f' ')
            
            # Optionally, delete the file after sending
            os.remove(file_path)  # Uncomment if you want to delete the file right after sending.
        except Exception as e:
            # Log the error instead of sending a message to the user
            print(f'Error: {str(e)}')
    else:
        # Ignore messages that are not valid YouTube or Instagram links
        pass

def main() -> None:
    # Make sure to replace this with your actual bot token
    updater = Updater("7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()
