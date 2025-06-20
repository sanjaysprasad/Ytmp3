import os
import shutil
import subprocess
from pytube import Playlist, YouTube

def run(pl):
    # Insert the downloads destination (optional)
    filepath = input("Downloads destination (optional): ")

    # Get linked list of links in the playlist
    links = pl.video_urls

    # Download each item in the list
    for l in links:
        os.system("cls" if os.name == "nt" else "clear")

        try:
            # Converts the link to a YouTube object
            yt = YouTube(l)
            print(f"Processing: {yt.title}")

            # Gets the first audio stream with mp4 extension
            music = yt.streams.filter(only_audio=True, file_extension="mp4").first()

            # Ensure the file is downloaded in the current directory
            music.download(output_path="./")
            default_filename = music.default_filename
            print(f"Downloaded: {default_filename}")

            # Safely rename the file
            default_filename_remove_spaces = default_filename.replace(" ", "_")
            try:
                os.rename(os.path.join("./", default_filename), os.path.join("./", default_filename_remove_spaces))
            except FileNotFoundError:
                print(f"Error: {default_filename} not found for renaming.")

            # Convert to mp3
            new_filename_remove_spaces = default_filename_remove_spaces.replace("mp4", "mp3")
            print("Converting to mp3...")
            subprocess.call(f'ffmpeg -i "{default_filename_remove_spaces}" "{new_filename_remove_spaces}"', shell=True)

            # Move to the specified download directory
            try:
                if filepath == "":
                    download_path = os.path.join(os.path.abspath("./Downloads"), new_filename_remove_spaces)
                else:
                    download_path = os.path.join(os.path.abspath(filepath), new_filename_remove_spaces)

                os.makedirs(os.path.dirname(download_path), exist_ok=True)
                shutil.move(new_filename_remove_spaces, download_path)
                print(f"File saved to: {download_path}")
            except Exception as e:
                print(f"Error moving file: {e}")

            # Remove the original mp4 file
            try:
                os.remove(default_filename_remove_spaces)
            except FileNotFoundError:
                print(f"Error: {default_filename_remove_spaces} not found for deletion.")

        except Exception as e:
            print(f"Error processing video: {e}")

    print("Download and conversion completed.")


if __name__ == "__main__":
    url = input("Please enter the URL of the playlist you wish to download: ")
    try:
        pl = Playlist(url)
        print(f"Downloading playlist: {pl.title}")
        run(pl)
    except Exception as e:
        print(f"Error: {e}")
