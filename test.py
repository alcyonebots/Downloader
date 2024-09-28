import os
import yt_dlp
import instaloader
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# YouTube and Facebook Video Downloader
def download_video(url):
    ydl_opts = {
        'format': 'best',  # Best available quality
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Download directory and file name template
        'cookies': 'cookies.txt'  # Relative path to the cookies file
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        return info['title'], info['filepath']  # Return title and file path

# Instagram Video Downloader
def download_instagram_video(url):
    loader = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
    loader.download_post(post, target=f"downloads/{post.shortcode}")
    return post.shortcode, f"downloads/{post.shortcode}/{post.shortcode}.mp4"  # Return shortcode and file path

# Command to handle start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send a YouTube, Facebook, or Instagram video link to download.")

# Handle video links
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    
    if "youtube.com" in url or "youtu.be" in url:
        update.message.reply_text("Downloading YouTube video...")
        video_title, file_path = download_video(url)
        context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'), caption=f"Downloaded: {video_title}")
    elif "instagram.com" in url:
        update.message.reply_text("Downloading Instagram video...")
        shortcode, file_path = download_instagram_video(url)
        context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'), caption=f"Downloaded Instagram video: {shortcode}")
    elif "facebook.com" in url:
        update.message.reply_text("Downloading Facebook video...")
        video_title, file_path = download_video(url)
        context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'), caption=f"Downloaded Facebook video: {video_title}")
    else:
        update.message.reply_text("Unsupported URL. Please send a YouTube, Facebook, or Instagram video link.")

# Main function to start the bot
def main():
    updater = Updater("7070026696:AAF2ahAcrT7DUwr2bHnKoObu5mdO-1GNuas", use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    main()
