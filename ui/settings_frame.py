import customtkinter as ctk
from tkinter import filedialog
from settings_manager import load_settings, save_settings

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(pady=10, padx=10, fill="x")
        self.settings = load_settings()
        self.build_ui()

    def build_ui(self):
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(side="top", fill="x", expand=True)

        path_frame = ctk.CTkFrame(control_frame)
        path_frame.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(path_frame, text="Download Path").pack(anchor="w")
        self.path_entry = ctk.CTkEntry(path_frame)
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.path_entry.insert(0, self.settings.get("download_path", ""))
        self.browse_button = ctk.CTkButton(path_frame, text="Browse", command=self.browse_path)
        self.browse_button.pack(side="right", padx=(10, 0))

        self.audio_only = ctk.CTkCheckBox(self, text="Audio Only")
        if self.settings.get("audio_only"): self.audio_only.select()
        self.audio_only.pack(anchor="w", padx=20, pady=(10, 0))

        self.download_playlist = ctk.CTkCheckBox(self, text="Download Playlist")
        if self.settings.get("download_playlist"): self.download_playlist.select()
        self.download_playlist.pack(anchor="w", padx=20)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, path)

    def get_download_path(self):
        return self.path_entry.get().strip()

    def is_audio_only(self):
        return self.audio_only.get()

    def is_playlist_download(self):
        return self.download_playlist.get()

    def get_all_settings(self):
        return {
            "download_path": self.get_download_path(),
            "audio_only": self.is_audio_only(),
            "download_playlist": self.is_playlist_download()
        }

    def save(self):
        save_settings(self.get_all_settings())
