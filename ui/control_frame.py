import customtkinter as ctk
from downloader import cancel_download


class ControlFrame(ctk.CTkFrame):
    def __init__(self, master, fetch_callback, download_callback):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.download_button = ctk.CTkButton(
            self, text="DOWNLOAD", command=download_callback
        )
        self.download_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.cancel_button = ctk.CTkButton(
            self, text="CANCEL DOWNLOAD", command=self.cancel_download
        )
        self.cancel_button.grid(row=0, column=1, padx=5, sticky="ew")
        self.cancel_button.configure(state="disabled")

        self.status_label = ctk.CTkLabel(
            self, text="Status: Ready", text_color="lightgreen", font=("", 15)
        )
        self.status_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w"
        )

    def set_status(self, text, color):
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def set_download_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.download_button.configure(state=state)

    def set_cancel_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.cancel_button.configure(state=state)

    def cancel_download(self):
        cancel_download()
        self.set_status("Cancelling download...")
