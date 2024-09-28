import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters
from telegram.error import BadRequest

# Function to download video from the provided URL
def download_video(url, output_path='downloads/'):
    ydl_opts = {
        'outtmpl': f'{output_path}%(title)s.%(ext)s',  # Path to save the video
        'cookies': 'cookies.txt',  # Path to your cookies file if needed
        'format': 'best',  # Best available quality
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)  # Return the filename for sending to the user

# Function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Send me a YouTube, Instagram, or Facebook video link, and I will download it for you!')

# Function to handle video link messages
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    chat_id = update.message.chat_id
    valid_sites = ['youtube.com', 'youtu.be', 'instagram.com', 'facebook.com']

    # Check if the URL is valid
    if any(site in url for site in valid_sites):
        try:
            # Download the video
            video_file = download_video(url)
            
            # Send the video to the user
            with open(video_file, 'rb') as video:
                update.message.reply_video(video)
        except Exception as e:
            update.message.reply_text(f"Error: {e}")
    else:
        update.message.reply_text("Please send a valid YouTube, Instagram, or Facebook video link.")

# Function to handle errors
def error(update: Update, context: CallbackContext):
    try:
        raise context.error
    except BadRequest as e:
        update.message.reply_text(f"BadRequest Error: {e}")

# Main function to run the bot
def main():
    # Create an updater and pass in your bot's token
    updater = Updater("7070026696:AAF2ahAcrT7DUwr2bHnKoObu5mdO-1GNuas", use_context=True)
    dispatcher = updater.dispatcher

    # Command handler for /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Message handler for video links
    dispatcher.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handler
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')  # Create a directory to save downloaded videos
    main()
