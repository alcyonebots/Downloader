import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
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
async def start(update: Update, context):
    await update.message.reply_text('Send me a YouTube, Instagram, or Facebook video link, and I will download it for you!')

# Function to handle video link messages
async def handle_message(update: Update, context):
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
                await update.message.reply_video(video)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
    else:
        await update.message.reply_text("Please send a valid YouTube, Instagram, or Facebook video link.")

# Function to handle errors
async def error(update: Update, context):
    try:
        raise context.error
    except BadRequest as e:
        await update.message.reply_text(f"BadRequest Error: {e}")

# Main function to run the bot
async def main():
    # Create the Application and pass in your bot's token
    application = Application.builder().token("7070026696:AAF2ahAcrT7DUwr2bHnKoObu5mdO-1GNuas").build()

    # Command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Message handler for video links
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handler
    application.add_error_handler(error)

    # Start the bot
    await application.start()
    await application.updater.stop()  # Replace 'start_polling' with 'start' and 'stop'

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')  # Create a directory to save downloaded videos
    import asyncio
    asyncio.run(main())
