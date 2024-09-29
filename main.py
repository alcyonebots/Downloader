import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Define the download function with progress updates
def download_video(url, update: Update, context: CallbackContext):
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': False,  # Prevent playlist downloading
        'progress_hooks': [lambda d: progress_hook(d, update, context)],  # Hook for progress updates
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url)
        video_title = video_info['title']
        file_path = ydl.prepare_filename(video_info)
        ydl.download([url])
    
    return video_title, file_path

def progress_hook(d, update: Update, context: CallbackContext):
    if d['status'] == 'downloading':
        total_bytes = d['total_bytes']
        downloaded_bytes = d['downloaded_bytes']
        percentage = (downloaded_bytes / total_bytes) * 100
        update.message.reply_text(f"Downloading... {percentage:.2f}% completed.")

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
            "Welcome to 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, your go-to bot for downloading high-quality content from all the top social platforms!! 🎬\n"
            "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
            "◎ Start a chat with @AlcDownloaderBot and send /start\n"
            "◎ In group send /start and then send the link of the video while replying me!!\n\n"
            "Join our channel and support group to use the bot\n\n"
            "Let's Get Started 👾"
        ),
        reply_markup=reply_markup
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    # Ensure update.message and update.message.text exist before proceeding
    if not update.message or not update.message.text:
        print(f"Received non-text update: {update}")
        return
    
    # Check if the message is a reply to the bot's message
    if not update.message.reply_to_message or update.message.reply_to_message.from_user.id != context.bot.id:
        return  # Ignore if it's not a reply to the bot's message

    url = update.message.text.strip()

    # Check if the URL is from YouTube or Instagram
    if url.startswith("http") and ("youtube.com" in url or "youtu.be" in url or "instagram.com" in url):
        try:
            video_title, file_path = download_video(url, update, context)
            update.message.reply_text(f'Downloaded: {video_title}')
            with open(file_path, 'rb') as video_file:
                update.message.reply_video(video_file, caption=f'Downloaded: {video_title}')
            
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
