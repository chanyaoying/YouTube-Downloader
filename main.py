import os
import sys
from helpers import parse_size, parse_time
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube, Playlist
from pytube.helpers import safe_filename


root = tk.Tk()
root.withdraw()


# Playlist URL as an argument when this script is run from the command line.
playlist_url = sys.argv[1:]
if not playlist_url or "youtube.com/playlist?" not in playlist_url[0]:
    print("Please key in the URL of the YouTube playlist as an argument. For help, read the documentations here: https://github.com/chanyaoying/YouTube-Downloader")
    exit()

skips = []
total_size = 0

if playlist_url[0]:
    
    try:
        p = Playlist(playlist_url[0])
    except:
        print("Invalid Playlist URL.")
        exit()

    count = 1

    # Prompts user for the download location
    file_path = filedialog.askdirectory()
    print(f"Downloading to {file_path}")

    if file_path:

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

        exit()


print("Exited without downloading.")
