import os
import subprocess
from pytube import YouTube, Playlist
from tkinter import Tk, filedialog
from pathlib import Path

def choose_folder():
    print("📂 Opening folder selector...")
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Download Folder")
    root.destroy()
    return folder or str(Path.home() / "Downloads")

def convert_to_mp3(input_file, bitrate_kbps):
    output_file = os.path.splitext(input_file)[0] + ".mp3"
    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-ab", f"{bitrate_kbps}k",
        "-ar", "44100",
        "-y",
        output_file
    ], check=True)
    os.remove(input_file)
    return output_file

def download_video(url, output_path, bitrate_kbps):
    yt = YouTube(url)
    print(f"🎥 Downloading: {yt.title}")
    stream = yt.streams.filter(only_audio=True).first()
    downloaded_file = stream.download(output_path=output_path)
    mp3_file = convert_to_mp3(downloaded_file, bitrate_kbps)
    print(f"✅ Saved MP3: {mp3_file}")

def download_playlist(url, output_path, bitrate_kbps):
    pl = Playlist(url)
    print(f"📃 Downloading Playlist: {pl.title}")
    for video in pl.videos:
        try:
            print(f"\n▶ {video.title}")
            stream = video.streams.filter(only_audio=True).first()
            downloaded_file = stream.download(output_path=output_path)
            mp3_file = convert_to_mp3(downloaded_file, bitrate_kbps)
            print(f"✅ Saved MP3: {mp3_file}")
        except Exception as e:
            print(f"❌ Error with video: {video.title} - {e}")

def main():
    print("==== YouTube to MP3 Converter ====")
    print("1. Download single video")
    print("2. Download playlist")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice not in ['1', '2']:
        print("❌ Invalid choice.")
        return

    url = input("Enter YouTube video/playlist URL: ").strip()

    bitrate = input("Enter MP3 bitrate (192, 256, 320): ").strip()
    if bitrate not in ['192', '256', '320']:
        print("❌ Invalid bitrate. Using default: 192kbps.")
        bitrate = '192'

    # 💡 Moved this line here to ensure it gets called correctly
    folder = choose_folder()
    print(f"📁 Download folder: {folder}")

    try:
        if choice == '1':
            download_video(url, folder, bitrate)
        else:
            download_playlist(url, folder, bitrate)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
