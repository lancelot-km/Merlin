import customtkinter as ctk

class URLFrame(ctk.CTkFrame):
    def __init__(self, master, fetch_callback):
        super().__init__(master)
        self.pack(pady=10, padx=10, fill="x")

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter video URL")
        self.url_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.fetch_button = ctk.CTkButton(self, text="Fetch Info", command=self._on_fetch)
        self.fetch_button.pack(side="right")

        self.fetch_callback = fetch_callback

    def get_url(self):
        return self.url_entry.get().strip()

    def _on_fetch(self):
        self.fetch_callback(self.get_url())

