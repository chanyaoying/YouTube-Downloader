# YouTube Downloader
Download YouTube videos from a public playlist using pytube. If English captions are available, they will be downloaded in `.srt` files in the same directory. A `.txt` file containing metadata about the video is also created.
 
To learn more about PyTube, [see the documentations here.](https://pytube.io/en/latest/index.html)

## Installation
Install the required dependencies from `requirements.txt` in this directory.

```bash
pip install -r requirements.txt
```

## Usage
### Before running the script
Clone this repository in any location on your machine. The download location can be different from this one.

### Running the script
Run `main.py` on your terminal like so, with the playlist URL as an argument:
```bash
python main.py https://www.youtube.com/playlist?list=<PLAYLIST INFORMATION HERE>
```

### Upon running the script
You will be prompted to select a location where you'd want to save the videos at. Videos that have already been downloaded will not be downloaded again.

The videos, with subtitles if available, and their metadata is downloaded.

## Issues and Changes
If you would like to contribute, pull requests are welcome! You can also open an issue and we can discuss any changes.
