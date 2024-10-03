import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

# Define the download function
def download_video(url) -> str:
    ydl_opts = {
        'cookiefile': 'cookies.txt',  # Update this path as needed
        'format': 'bestvideo+bestaudio/best',  # Best video and audio combination
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,  # Prevent playlist downloading
        'postprocessors': [
            {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}  # Convert to mp4 if not already
        ],
        'merge_output_format': 'mp4',  # Ensure mp4 format
        'video-quality': 'high',  # High video quality
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(video_info)  # Return the downloaded file path

# Define the command handler for the bot
def start(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.get_me().username  # Get the bot's username
    
    keyboard = [
        [
            InlineKeyboardButton("𝗕𝗼𝘁 𝗨𝗽𝗱𝗮𝘁𝗲𝘀", url="https://t.me/alcyonebots"),
            InlineKeyboardButton("𝗕𝗼𝘁 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url="https://t.me/alcyone_support")
        ],
        [
            InlineKeyboardButton("Add me to your groups ➕", url=f"https://t.me/{bot_username}?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://i.imghippo.com/files/OTItE1727595318.jpg"
    
    # Send the image with the caption
    update.message.reply_photo(
        photo=image_url,
        caption=(
            "𝗛𝗶 𝘁𝗵𝗲𝗿𝗲 👋🏻\n"
            "Welcome to 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, your go-to bot for downloading high-quality content from YouTube and Instagram!! 🎬\n"
            "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
            "◎ Start a chat with @AlcDownloaderBot and send /start\n"
            "◎ Works fine in Public group chats!! \nIn private group chats send /start@AlcyoneDownloaderbot then send link by replying to my message!!\n\n"
            "Join our channel and support group to use the bot\n\n"
            "Let's Get Started 👾"
        ),
        reply_markup=reply_markup
    )

# Function to check if the message contains a YouTube or Instagram link
def is_valid_url(text: str) -> bool:
    youtube_pattern = r'(https?://)?(www\.)?(youtube|youtu\.be)(\.com)?/.*'
    instagram_pattern = r'(https?://)?(www\.)?instagram\.com/.*'
    return re.match(youtube_pattern, text) or re.match(instagram_pattern, text)

# Handle messages with links
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if is_valid_url(url):
        try:
            file_path = download_video(url)  # Download the video

            # Define the inline buttons
            keyboard = [
                [
                    InlineKeyboardButton("𝗕𝗼𝘁 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 ", url="https://t.me/alcyonebots"),
                    InlineKeyboardButton("𝗕𝗼𝘁 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 ", url="https://t.me/alcyone_support")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the video with inline buttons
            with open(file_path, 'rb') as video_file:
                update.message.reply_video(video_file, reply_markup=reply_markup)
            
            os.remove(file_path)  # Remove the file after sending
        except Exception as e:
            update.message.reply_text(f'Error: {str(e)}')
    # In group chats, if it's not a valid URL, ignore the message
    elif update.message.chat.type != 'private':
        return  # Ignore non-valid messages in group chats
    # In private chat, prompt for valid URL if the message doesn't contain one
    else:
        update.message.reply_text("Please send a valid YouTube or Instagram link.")

# Main function to start the bot
def main() -> None:
    updater = Updater("7488772903:AAGP-ZvbH7K2XzYG9vv-jIsA12iRxTeya3U")  # Your bot token

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
