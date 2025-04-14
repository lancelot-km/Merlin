import customtkinter as ctk
from ui.url_frame import URLFrame
from ui.settings_frame import SettingsFrame
from ui.control_frame import ControlFrame
from ui.options_frame import OptionsFrame
from ui.progress_frame import ProgressFrame
from downloader import (
    extract_video_info,
    download_video,
    get_download_state,
    download_state,
)
import threading
from downloader import CustomLogger

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Merlin VD")
        self.geometry("800x400")
        self.resizable(False, False)

        # Configure grid layout (1 row, 2 columns)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Sidebar widgets
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Merlin",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(
            self.sidebar_frame, text="Home", command=self.show_home
        )
        self.home_button.grid(row=1, column=0, padx=20, pady=10)

        self.settings_button = ctk.CTkButton(
            self.sidebar_frame, text="Settings", command=self.show_settings
        )
        self.settings_button.grid(row=2, column=0, padx=20, pady=10)

        self.logs_button = ctk.CTkButton(
            self.sidebar_frame, text="Logs", command=self.show_logs
        )
        self.logs_button.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, text="Theme:", anchor="w"
        )
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_option = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode,
        )
        self.appearance_mode_option.grid(row=7, column=0, padx=20, pady=(10, 20))

        # Main content area
        self.main_content = ctk.CTkFrame(self, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Create frames (but don't grid them yet)
        self.url_frame = URLFrame(self.main_content, self.fetch_info)
        self.options_frame = OptionsFrame(self.main_content)
        self.control_frame = ControlFrame(
            self.main_content, self.fetch_info, self.start_download
        )
        self.progress_frame = ProgressFrame(self.main_content)

        self.logger = CustomLogger(self.progress_frame.append_text)
        get_download_state().subscribe(on_next=self.update_button_states)
        self.video_info = {}
        self.formats = []

        # Set defaults
        self.appearance_mode_option.set("System")
        self.show_home()

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    def show_home(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.grid_forget()

        # Show home layout
        self.url_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.options_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.control_frame.grid(row=2, column=0, sticky="ew", pady=10)

    def show_settings(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.grid_forget()

        # Show settings
        self.settings_frame = SettingsFrame(self.main_content)
        self.settings_frame.grid(row=0, column=0, sticky="nsew")

    def show_logs(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.grid_forget()

        # Show logs (expanded progress frame)
        self.progress_frame.grid(row=0, column=0, sticky="nsew")

    def update_button_states(self, downloading: bool):
        if downloading:
            self.control_frame.set_download_enabled(False)
            self.control_frame.set_cancel_enabled(True)
        else:
            self.control_frame.set_download_enabled(True)
            self.control_frame.set_cancel_enabled(False)

    def fetch_info(self, url):
        if not url:
            self.control_frame.set_status("Please enter a URL.", color="red")
            return

        def task():
            self.logger._log("Fetching video info...")
            self.control_frame.set_status("Fetching video info...", color="orange")
            try:
                self.video_info = extract_video_info(url, playlist=False)
                self.formats = self.video_info.get("formats", [])
                self.options_frame.update_formats(self.formats)
                self.control_frame.set_status("Formats loaded.", color="lightgreen")
                self.logger._log("Formats loaded successfully.")
            except Exception as e:
                self.control_frame.set_status(f"Error: {e}", text_color="red")

        threading.Thread(target=task).start()

    def start_download(self):
        url = self.url_frame.get_url()

        if not url:
            self.control_frame.set_status("Please enter a URL.", color="red")
            return

        output_path = self.settings_frame.get_download_path()
        audio_only = self.settings_frame.is_audio_only()
        playlist = self.settings_frame.is_playlist_download()

        video_id, audio_id = self.options_frame.get_selected_format_ids()

        if not url or not output_path:
            self.control_frame.set_status("Missing URL or output path.", color="red")
            return

        download_video(
            url,
            video_id,
            audio_id,
            output_path,
            self.progress_frame.append_text,
            audio_only,
            playlist,
        )


if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
