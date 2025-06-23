import subprocess
from tkinter import Tk, filedialog

def choose_folder():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Download Folder")
    root.destroy()
    return folder

"""def sanitize_url(url):
    if "music.youtube.com" in url:
        url = url.replace("music.youtube.com", "www.youtube.com")
    if "youtu.be" in url:
        url = url.replace("youtu.be","www.youtube.com")
    if "&si=" in url:
        url = url.split("&si=")[0]
    return url"""

def sanitize_url(url):
    # Fix music domain
    url = url.replace("music.youtube.com", "www.youtube.com")

    # Convert youtu.be short links to proper full format
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1]
        if "?si=" in video_id:
            video_id = video_id.split("?si=")[0]
        url = f"https://www.youtube.com/watch?v={video_id}"

    # Remove ?si= or &si= parameters from normal URLs
    if "&si=" in url:
        url = url.split("&si=")[0]
    elif "?si=" in url:
        url = url.split("?si=")[0]

    return url


def download_youtube_audio(url, folder, bitrate):
    command = [
        "python", "-m", "yt_dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", bitrate,
        "-o", f"{folder}/%(title)s.%(ext)s",
        url
    ]

    try:
        subprocess.run(command, check=True)
        print("Download and conversion complete.")
    except subprocess.CalledProcessError as e:
        print(f" yt-dlp error: {e}")

def main():
    print("==== YouTube to MP3 Downloader ====")
    print("1. Single Video")
    print("2. Playlist")
    choice = input("Enter choice (1 or 2): ").strip()

    url = input("Enter YouTube video/playlist URL: ").strip()
    url = sanitize_url(url)

    bitrate = input("Enter MP3 bitrate (192, 256, 320): ").strip()
    if bitrate not in ['192', '256', '320']:
        print("Invalid bitrate. Using 192kbps.")
        bitrate = '192'

    folder = choose_folder()
    print(f"Download folder: {folder}")
    download_youtube_audio(url, folder, bitrate)

if __name__ == "__main__":
    main()
