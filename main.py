import os
import yt_dlp
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace these with your actual channel and group usernames
CHANNEL_USERNAME = '@alcyonebots'
GROUP_USERNAME = '@alcyone_support'
DELETE_DELAY = 1800  # Time in seconds before the file is deleted (e.g., 300 seconds = 5 minutes)

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
    keyboard = [
        [
            InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
            InlineKeyboardButton("Join Support", url=f"https://t.me/{GROUP_USERNAME[1:]}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "𝗦𝗲𝗻𝗱 𝗺𝗲 𝗮 𝗹𝗶𝗻𝗸 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗮 𝘃𝗶𝗱𝗲𝗼 𝗳𝗿𝗼𝗺 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗼𝗿 𝗬𝗼𝘂𝗧𝘂𝗯𝗲...\n\n"
        "𝗕𝗲𝗳𝗼𝗿𝗲 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗲 𝗯𝗼𝘁, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗷𝗼𝗶𝗻 𝘁𝗵𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗮𝗻𝗱 𝘁𝗵𝗲 𝗴𝗿𝗼𝘂𝗽\n"
        "𝗢𝘄𝗻𝗲𝗿 [C Ξ N Z O](https://t.me/Cenzeo),
        reply_markup=reply_markup
        )

def check_membership(update: Update, context: CallbackContext) -> bool:
    user_id = update.message.from_user.id
    chat_id_group = update.message.chat.id
    
    # Check if user is in the group
    group_member = update.message.chat.get_member(user_id)
    if group_member.status not in ['member', 'administrator']:
        return False
    
    # Check if user is in the channel
    try:
        member_status = context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member_status.status not in ['member', 'administrator']:
            return False
    except Exception as e:
        print(f"Error checking channel membership: {str(e)}")
        return False
    
    return True

def handle_message(update: Update, context: CallbackContext) -> None:
    if not check_membership(update, context):
        update.message.reply_text(
            "𝗣𝗹𝗲𝗮𝘀𝗲 𝗺𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘁𝗵𝗮𝘁 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗷𝗼𝗶𝗻𝗲𝗱 𝗯𝗼𝘁 𝗴𝗿𝗼𝘂𝗽 𝗮𝗻𝗱 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁."
        )
        return
    
    url = update.message.text
    try:
        video_title, file_path = download_video(url)
        update.message.reply_text(
            f'𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱: {video_title}\n\n'
            f'Forward your video to your saved messages or it will be deleted in {DELETE_DELAY // 60} minutes.'
        )
        with open(file_path, 'rb') as video_file:
            video_message = update.message.reply_video(video_file, caption=f'𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱: {video_title}')
        
        # Start a timer to delete the file after DELETE_DELAY seconds
        threading.Timer(DELETE_DELAY, delete_file, args=[file_path]).start()
        
    except Exception as e:
        update.message.reply_text(f'Error: {str(e)}')

def delete_file(file_path):
    """Delete the video file from the server."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {str(e)}")

def main() -> None:
    updater = Updater("YOUR_TOKEN_HERE")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    main()
