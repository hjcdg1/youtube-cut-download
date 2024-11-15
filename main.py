import sys
from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func

def download_youtube(url, range):
  ydl_opts = {
    'format': 'bestvideo[vcodec^=avc1][height<=1080]+bestaudio[acodec^=mp4a]/best',
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True
  }

  if range:
    [start_h, start_m, start_s] = range['start'].split(":")
    [end_h, end_m, end_s] = range['end'].split(":")

    start = int(start_h) * 3600 + int(start_m) * 60 + int(start_s)
    end = int(end_h) * 3600 + int(end_m) * 60 + int(end_s)

    # https://stackoverflow.com/questions/73516823/using-yt-dlp-in-a-python-script-how-do-i-download-a-specific-section-of-a-video
    # https://github.com/yt-dlp/yt-dlp/blob/c54ddfba0f7d68034339426223d75373c5fc86df/yt_dlp/YoutubeDL.py#L457
    ydl_opts['download_ranges'] = download_range_func(None, [(start, end)])
    ydl_opts['force_keyframes_at_cuts'] = True

  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

if __name__ == "__main__":
  """
  How to use:
  1. Create a virtual environment, and install required packages from `requirements.txt`.
  2. Install `ffmpeg`, and the directory containing `ffmpeg.exe`, `ffplay.exe`, `ffprobe.exe` must be in the PATH.
  3. Run this script like `python main.py "https://www.youtube.com/..." "00:00:05" "00:00:10"`.
  """

  if len(sys.argv) != 4:
    print("Usage: python main.py URL START_TIME END_TIME")
    sys.exit(1)

  url = sys.argv[1]
  start_time = sys.argv[2]
  end_time = sys.argv[3]

  download_youtube(url, {'start': start_time, 'end': end_time})
