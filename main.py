import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Set up logging for better error tracking
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the progress hook to track download progress
def progress_hook(d, update):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        eta = d['eta']  # Estimated time remaining in seconds
        update.message.reply_text(f"Downloading... {percent} \n Complete at {speed} \n Estimated Time Remaining: {eta} seconds")

    if d['status'] == 'finished':
        update.message.reply_text("Download finished, now sending the video...🎬")

# Define the download function with proxy settings
def download_video(url, update):
    proxy_url = 'http://your_proxy_url:your_proxy_port'  # Replace with your actual proxy
    proxy = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    ydl_opts = {
        'cookiefile': 'cookies.txt',  # Update this path as needed
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,  # Prevent playlist downloading
        'retries': 10,  # Retry downloading in case of failure
        'timeout': 1200,  # Increase timeout to 20 minutes (1200 seconds)
        'continuedl': True,  # Resume downloads if possible
        'http_chunk_size': 10485760,  # Download in 10 MB chunks
        'progress_hooks': [lambda d: progress_hook(d, update)],  # Hook for download progress
        'proxy': proxy  # Add proxy settings here
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url)
            video_title = video_info['title']
            file_path = ydl.prepare_filename(video_info)
            ydl.download([url])
        return video_title, file_path
    except Exception as e:
        logger.error(f"Error downloading video from {url}: {str(e)}")
        raise  # Re-raise the exception to handle it in the calling function

# Updated start function with image and caption
def start(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.get_me().username  
    
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
            "◎ Add me to your group and send /start then send the link of the video by replying to my message.\n\n"
            "Join our channel and support group to use the bot\n\n"
            "Let's Get Started 👾"
        ),
        reply_markup=reply_markup
    )

# Handle messages that contain download links
def handle_message(update: Update, context: CallbackContext) -> None:
    # Ensure update.message and update.message.text exist before proceeding
    if not update.message or not update.message.text:
        logger.error(f"Received non-text update: {update}")
        return

    # Check if the message is a reply to the bot's message
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        url = update.message.text.strip()

        # Check if the URL is from YouTube or Instagram
        if url.startswith("http") and ("youtube.com" in url or "instagram.com" in url):
            try:
                update.message.reply_text(f"Starting download for: {url}")
                video_title, file_path = download_video(url, update)
                update.message.reply_text(f'Downloaded Successfully: {video_title}')
                
                # Send the downloaded video
                with open(file_path, 'rb') as video_file:
                    update.message.reply_video(video_file, caption=f'{video_title}')
                
                # Optionally, delete the file after sending
                os.remove(file_path)  # Uncomment if you want to delete the file right after sending.
            except Exception as e:
                update.message.reply_text(f"An error occurred: {str(e)}")
                logger.error(f"Error: {str(e)}")
        else:
            # Ignore messages that are not valid YouTube or Instagram links
            update.message.reply_text("Please send a valid YouTube or Instagram link.")
    else:
        # Ignore messages that are not replies to the bot
        return

# Main function to start the bot
def main() -> None:
    # Replace this with your actual bot token
    updater = Updater("7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()
