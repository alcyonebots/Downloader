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
        'socket_timeout': 60,  # Increase socket timeout to 60 seconds
        'http_chunk_size': 10 * 1024 * 1024,  # Split the file into 10MB chunks to avoid long write operations
        'max_filesize': 2 * 1024 * 1024 * 1024,  # Set a 2GB limit for the downloaded video in bytes (2GB = 2 * 1024^3)
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
            InlineKeyboardButton("𝗔𝗱𝗱 𝗺𝗲 𝘁𝗼 𝘆𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽𝘀 ➕", url=f"https://t.me/{bot_username}?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://i.imghippo.com/files/OTItE1727595318.jpg"
    
    # Send the image with the caption
    update.message.reply_photo(
        photo=image_url,
        caption=(
            "𝗛𝗶 𝘁𝗵𝗲𝗿𝗲 👋🏻\n"
            "𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝗈 𝗩𝗶𝗱𝗲𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁 𝗯𝘆 𝗔𝗹𝗰𝘆𝗼𝗻𝗲, 𝗒𝗈𝗎𝗋 𝗀𝗈-𝗍𝗈 𝖻𝗈𝗍 𝖿𝗈𝗋 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗁𝗂𝗀𝗁-𝗊𝗎𝖺𝗅𝗂𝗍𝗒 𝖼𝗈𝗇𝗍𝖾𝗇𝗍 𝖿𝗋𝗈𝗆 𝖸𝗈𝗎𝖳𝗎𝖻𝖾 𝖺𝗇𝖽 𝖨𝗇𝗌𝗍𝖺𝗀𝗋𝖺𝗆!!🎬\n"
            "𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗶𝘁 𝘄𝗼𝗿𝗸?\n"
            "◎ 𝖲𝗍𝖺𝗋𝗍 𝖺 𝖼𝗁𝖺𝗍 𝗐𝗂𝗍𝗁 @AlcDownloaderbot 𝖺𝗇𝖽 𝗌𝖾𝗇𝖽 /start\n"
            "◎ 𝖶𝗈𝗋𝗄𝗌 𝖿𝗂𝗇𝖾 𝗂𝗇 𝖯𝗎𝖻𝗅𝗂𝖼 𝗀𝗋𝗈𝗎𝗉 𝖼𝗁𝖺𝗍𝗌!! \n𝖨𝗇 𝗉𝗋𝗂𝗏𝖺𝗍𝖾 𝗀𝗋𝗈𝗎𝗉 𝖼𝗁𝖺𝗍𝗌 𝗌𝖾𝗇𝖽 /Start 𝗍𝗁𝖾𝗇 𝗌𝖾𝗇𝖽 𝗅𝗂𝗇𝗄 𝖻𝗒 𝗋𝖾𝗉𝗅𝗒𝗂𝗇𝗀 𝗍𝗈 𝗆𝗒 𝗆𝖾𝗌𝗌𝖺𝗀𝖾!!\n\n"
            "𝖩𝗈𝗂𝗇 𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝗇𝖽 𝗌𝗎𝗉𝗉𝗈𝗋𝗍 𝗀𝗋𝗈𝗎𝗉 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝖾 𝖻𝗈𝗍\n"
            f"𝖥𝗈𝗋 𝖺𝗇𝗒 𝗊𝗎𝖾𝗋𝗂𝖾𝗌, 𝖧𝗂𝗍 𝖺𝗍 : @CENZEO \n\n"
            "𝖫𝖾𝗍'𝗌 𝖦𝖾𝗍 𝖲𝗍𝖺𝗋𝗍𝖾𝖽 👾"
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
        update.message.reply_text("𝖯𝗅𝖾𝖺𝗌𝖾 𝗌𝖾𝗇𝖽 𝖺 𝗏𝖺𝗅𝗂𝖽 𝖸𝗈𝗎𝖳𝗎𝖻𝖾 𝗈𝗋 𝖨𝗇𝗌𝗍𝖺𝗀𝗋𝖺𝗆 𝗅𝗂𝗇𝗄.")

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
