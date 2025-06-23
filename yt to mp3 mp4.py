import subprocess
from tkinter import Tk, filedialog

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
    output_template = f"{folder}/%(title)s.%(ext)s"
    
    command = [
        "yt-dlp",
        "-o", output_template,
        url
    ]

    if format_choice == "mp3":
        command += [
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", quality  # 192, 256, 320
        ]
    elif format_choice == "mp4":
        # Select appropriate resolution using format filters
        resolution_map = {
            "360": "bestvideo[height<=360]+bestaudio/best[height<=360]",
            "480": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "720": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        }
        format_string = resolution_map.get(quality, "bestvideo+bestaudio")
        command += ["-f", format_string, "--merge-output-format", "mp4"]

    try:
        subprocess.run(command, check=True)
        print("Download and conversion complete.")
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp error: {e}")

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
