import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.helpers import escape_markdown
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the download function
def download_video(url, update, context):
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%')
            update.message.edit_text(f"Downloading... {percent}")

    ydl_opts = {
        'cookiefile': 'cookies.txt',  # Update this path as needed
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [progress_hook],  # Hook to track download progress
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url)
        video_title = video_info['title']
        file_path = ydl.prepare_filename(video_info)
        ydl.download([url])
    
    return video_title, file_path

# Define the start command handler for the bot
def start(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.get_me().username  # Get the bot's username
    
    # Inline keyboard buttons for joining channel, support, and adding to groups
    keyboard = [
        [
            InlineKeyboardButton("Join Channel", url="https://t.me/alcyonebots"),
            InlineKeyboardButton("Join Support", url="https://t.me/alcyone_support")
        ],
        [
            InlineKeyboardButton("Add me to your groups ➕", url=f"https://t.me/{bot_username}?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Image URL
    image_url = "https://i.imghippo.com/files/OTItE1727595318.jpg"
    
    # Send the image with a caption
    update.message.reply_photo(
        photo=image_url,
        caption=(
            "𝗛𝗶 𝘁𝗵𝗲𝗿𝗲 👋🏻\n"
            "Welcome to 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, your go-to bot for downloading high-quality content from YouTube and Instagram!! 🎬\n"
            "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
            "◎ Start a chat with @AlcDownloaderBot and send /start\n"
            "◎ Add me to your group and I'll be there for you for downloading videos\n\n"
            "Join our channel and support group to use the bot\n\n"
            "Let's Get Started 👾"
        ),
        reply_markup=reply_markup
    )

# Handler for video download messages
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        if "youtube.com/shorts" in url or "instagram.com/reel" in url:  # Only respond to YouTube Shorts or Instagram Reels
            message = update.message.reply_text("Preparing to download...")
            video_title, file_path = download_video(url, message, context)
            message.edit_text(f'Downloaded: {escape_markdown(video_title)}')

            with open(file_path, 'rb') as video_file:
                update.message.reply_video(video_file, caption= {escape_markdown(video_title)}')
            
            # Optionally, delete the file after sending
            os.remove(file_path)
        else:
            update.message.reply_text("Sorry, I can only download YouTube shorts and Instagram reels.")
        
    except Exception as e:
        update.message.reply_text(f'Error: {escape_markdown(str(e))}')

# Main function to start the bot
def main() -> None:
    updater = Updater("7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U", use_context=True)  # Replace with your bot token

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Message handler for text that is not commands, restricted to group chats for specific URLs
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.groups, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # Create the downloads directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()
