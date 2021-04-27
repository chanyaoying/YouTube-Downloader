import tkinter as tk
from tkinter import filedialog
from pytube import YouTube, Playlist
from pytube.helpers import safe_filename
import string
import os
from dotenv import load_dotenv
from helpers import parse_size, parse_time


root = tk.Tk()
root.withdraw()

# Prompts user for the download location
file_path = filedialog.askdirectory()

load_dotenv()
playlist_url = os.environ.get('PLAYLIST_URL')

skips = []
total_size = 0

if file_path:

    print(f"Downloading to {file_path}")
    p = Playlist(playlist_url)
    count = 1

    for url in p.video_urls:
        try:
            yt = YouTube(url)
        except Exception as exception:
            skips.append(url)
            print(f'Video {url} is unavailable, skipping.')
        else:
            print(f"Downloading ({count}/{len(p.video_urls)}): {yt.title}")
            try:

                # Download the highest resolution video
                stream = yt.streams.filter(
                    file_extension='mp4').get_highest_resolution()
                stream.download(output_path=file_path, max_retries=3)
                size = stream.filesize_approx
                total_size += size

                # Download English captions as SubRip (.srt) if avavilable
                try:
                    english_captions = yt.captions['en']
                    english_captions.download(
                        title=(yt.title+".srt"), output_path=file_path)
                except:
                    english_captions = None

                # Create a text file containing metadata

                contents = [
                    f'Title: {yt.title}',
                    f'Author: {yt.author}',
                    f'Description:\n\n{yt.description}',
                    f'Rating: {yt.rating}',
                    f'Length: {parse_time(yt.length)}',
                    f'Publish Date: {yt.publish_date}',
                    f"Captions downloaded: {english_captions}"
                ]
                divider = '\n==============================================\n'
                contents = [divider[1:]] + \
                    [line + divider for line in contents]

                with open(f"{os.path.join(file_path, safe_filename(yt.title))}.txt", "w", errors='ignore') as f:
                    f.writelines(contents)

            except Exception as exception:
                skips.append(url)
                print(exception)
            finally:
                count += 1

    print(f"Downloads from \"{p.title}\" finished. Videos are in {file_path}.")
    print(f"Total amount of space used: {parse_size(total_size)}")

    if skips:
        print(f"Videos skipped: {skips}")

else:

    print("Exited without downloading.")
