import customtkinter as ctk
from downloader import cancel_download

class ControlFrame(ctk.CTkFrame):
    def __init__(self, master, fetch_callback, download_callback):
        super().__init__(master)
        self.pack(pady=5, padx=10, fill="x")
        self.download_button = ctk.CTkButton(self, text="Download", command=download_callback)
        self.download_button.pack(side="left", padx=5)
        self.cancel_button = ctk.CTkButton(self, text="Cancel Download", command=self.cancel_download)
        self.cancel_button.pack(side="left", padx=10)
        self.cancel_button.configure(state="disabled")  # initially disabled

        self.status_label = ctk.CTkLabel(self, text="Status: Ready")
        self.status_label.pack(side="left", padx=10)

    def set_status(self, text):
        self.status_label.configure(text=f"Status: {text}")
    
    def set_download_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.download_button.configure(state=state)

    def set_cancel_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.cancel_button.configure(state=state)

    def cancel_download(self):
        cancel_download()
        self.set_status("Cancelling download...")

