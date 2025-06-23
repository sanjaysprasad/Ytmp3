import subprocess
from tkinter import Tk, filedialog
import os
import shutil

def choose_folder():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Download Folder")
    root.destroy()
    return folder

def sanitize_url(url):
    url = url.replace("music.youtube.com", "www.youtube.com")
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
        url = f"https://www.youtube.com/watch?v={video_id}"
    if "&si=" in url:
        url = url.split("&si=")[0]
    elif "?si=" in url:
        url = url.split("?si=")[0]
    return url



def download_youtube_media(url, folder, format_choice):

    print("🎧 Downloading best audio with yt-dlp...")
    
    # Use yt-dlp to download best audio and keep original title
    yt_info_cmd = [
        "yt-dlp",
        "--get-title",
        "--skip-download",
        url
    ]
    try:
        title = subprocess.check_output(yt_info_cmd).decode().strip()
    except Exception as e:
        print("Failed to fetch title.")
        return

    temp_audio = os.path.join(folder, "temp_audio.m4a")
    download_cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "-o", temp_audio,
        url
    ]

    try:
        subprocess.run(download_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return

    # Quality level map (VBR): ffmpeg uses qscale for quality
    vbr_levels = {
        "320kbps": "0",  # Best VBR
        "256kbps": "2",
        "192kbps": "4"
    }

    for folder_name, qscale in vbr_levels.items():
        output_dir = os.path.join(folder, folder_name)
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"{title}.mp3")
        convert_cmd = [
            "ffmpeg", "-y",
            "-i", temp_audio,
            "-codec:a", "libmp3lame",
            "-qscale:a", qscale,
            output_path
        ]

        print(f"🎛Converting to {folder_name}...")
        try:
            subprocess.run(convert_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed at {folder_name}: {e}")

    os.remove(temp_audio)
    print(" All VBR MP3 versions created.")

def main():
    print("==== YouTube to MP3/MP4 Downloader ====")
    print("1. Single Video")
    print("2. Playlist")
    choice = input("Enter choice (1 or 2): ").strip()

    url = input("Enter YouTube video/playlist URL: ").strip()
    url = sanitize_url(url)

    format_choice = input("Choose format - mp3 or mp4: ").strip().lower()

    if format_choice == "mp3":
        bitrate = input("Enter MP3 bitrate (192, 256, 320): ").strip()
        if bitrate not in ['192', '256', '320']:
            print("Invalid bitrate. Defaulting to 192kbps.")
            bitrate = '192'
        quality = bitrate
    elif format_choice == "mp4":
        resolution = input("Enter video resolution (360, 480, 720, 1080): ").strip()
        if resolution not in ['360', '480', '720', '1080']:
            print("Invalid resolution. Defaulting to 720p.")
            resolution = '720'
        quality = resolution
    else:
        print("Invalid format. Exiting.")
        return

    folder = choose_folder()
    print(f"Download folder: {folder}")
    download_youtube_media(url, folder, format_choice, quality)

if __name__ == "__main__":
    main()
