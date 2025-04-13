import yt_dlp
import logging
from rx.subject import BehaviorSubject
import subprocess
import threading


current_download = None  # Global reference to the running process

download_state = BehaviorSubject(False)

def get_download_state():
    return download_state

# Custom Logger to capture yt-dlp output and update UI text box
class CustomLogger:
    def __init__(self, append_text_callback):
        self.append_text_callback = append_text_callback
        self.logger = logging.getLogger('yt_dlp')
        self.logger.setLevel(logging.DEBUG)

        # Creating a log handler that will print logs to the text box
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def debug(self, msg):
        self._log(msg)

    def info(self, msg):
        self._log(msg)

    def warning(self, msg):
        self._log(msg)

    def error(self, msg):
        self._log(msg)

    def _log(self, msg):
        # Update the text box with log messages
        self.append_text_callback(msg)


def extract_video_info(url, playlist=False):
    ydl_opts = {
        'extract_flat': not playlist
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# Function to handle the download
def download_video(url, video_format_id, audio_format_id, output_path, append_text_callback, audio_only=False, playlist=False):
    global current_download

    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True,  # Disable default terminal output
        'logger': CustomLogger(append_text_callback),  # Custom logger to handle appending logs
        'noplaylist': not playlist,
        'format': f'{video_format_id}+{audio_format_id}' if not audio_only else 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if audio_only else [],
    }

    current_download = yt_dlp.YoutubeDL(ydl_opts)
    yt_dlp.utils

    def task():
        try:
            download_state.on_next(True)  # Download started
            current_download.download([url])
            download_state.on_next(False)  # Download completed
        except Exception as e:
            download_state.on_next(False)  # Download failed
            append_text_callback(f"Error: {e}")

    # Start the download in a new thread
    threading.Thread(target=task).start()


def cancel_download():
    global current_download
    if current_download:
        current_download.abort()  # Calls internal method to stop download
        download_state.on_next(False)  # Update download state
        append_text_callback("Download cancelled.")
