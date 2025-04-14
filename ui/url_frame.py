import customtkinter as ctk


class URLFrame(ctk.CTkFrame):
    def __init__(self, master, fetch_callback):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Enter Video URL").grid(row=0, column=0)
        self.url_entry = ctk.CTkEntry(self, placeholder_text="https://...")
        self.url_entry.grid(row=1, column=0, sticky="ew", pady=10, padx=10)

        self.fetch_button = ctk.CTkButton(
            self, text="FETCH DETAILS", command=self._on_fetch
        )
        self.fetch_button.grid(row=1, column=1, sticky="ew", pady=10, padx=10)

        self.fetch_callback = fetch_callback

    def get_url(self):
        return self.url_entry.get().strip()

    def _on_fetch(self):
        self.fetch_callback(self.get_url())
