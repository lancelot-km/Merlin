import customtkinter as ctk
from ui.url_frame import URLFrame
from ui.settings_frame import SettingsFrame
from ui.control_frame import ControlFrame
from ui.options_frame import OptionsFrame
from ui.progress_frame import ProgressFrame
from downloader import extract_video_info, download_video, get_download_state, download_state
import threading
from downloader import CustomLogger


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("800x500")
        self.resizable(False, False)
        self.url_frame = URLFrame(self, self.fetch_info)
        self.settings_frame = SettingsFrame(self)
        self.options_frame = OptionsFrame(self)
        self.progress_frame = ProgressFrame(self)
        self.control_frame = ControlFrame(self, self.fetch_info, self.start_download)
        self.logger = CustomLogger(self.progress_frame.append_text)
        get_download_state().subscribe(
            on_next=self.update_button_states
        )
        self.video_info = {}
        self.formats = []

    def update_button_states(self, downloading: bool):
        if downloading:
            self.control_frame.set_download_enabled(False)
            self.control_frame.set_cancel_enabled(True)
        else:
            self.control_frame.set_download_enabled(True)
            self.control_frame.set_cancel_enabled(False)

    def fetch_info(self, url):
        if not url:
            self.control_frame.set_status("Please enter a URL.")
            return

        is_playlist = self.settings_frame.is_playlist_download()

        def task():
            self.logger._log("Fetching video info...")
            self.control_frame.set_status("Fetching video info...")
            try:
                self.video_info = extract_video_info(url, playlist=is_playlist)
                self.formats = self.video_info.get("formats", []) if not is_playlist else []
                self.options_frame.update_formats(self.formats)
                self.control_frame.set_status("Formats loaded.")
                self.logger._log("Formats loaded successfully.")
            except Exception as e:
                self.control_frame.set_status(f"Error: {e}")

        threading.Thread(target=task).start()

    def start_download(self):
        url = self.url_frame.get_url()
        output_path = self.settings_frame.get_download_path()
        audio_only = self.settings_frame.is_audio_only()
        playlist = self.settings_frame.is_playlist_download()

        video_id, audio_id = self.options_frame.get_selected_format_ids()

        if not url or not output_path:
            self.control_frame.set_status("Missing URL or output path.")
            return

        download_video(url, video_id, audio_id, output_path, self.progress_frame.append_text, audio_only, playlist) 

        self.settings_frame.save()


if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
