import customtkinter as ctk

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(pady=5, padx=10, fill="x")
        self.video_combobox = ctk.CTkComboBox(self, values=[""])
        self.audio_combobox = ctk.CTkComboBox(self, values=[""])
        ctk.CTkLabel(self, text="Video Quality").pack(anchor="w")
        self.video_combobox.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(self, text="Audio Quality").pack(anchor="w")
        self.audio_combobox.pack(fill="x")

    def update_formats(self, formats):
        video_formats = []
        audio_formats = []

        for f in formats:
            if f.get("vcodec") != "none" and f.get("acodec") == "none":
                video_formats.append(f)
            elif f.get("vcodec") == "none" and f.get("acodec") != "none":
                audio_formats.append(f)

        def fmt_string(f): return f"{f['format_id']} - {f.get('format_note', '')} - {f['ext']}"

        self.video_combobox.configure(values=[fmt_string(f) for f in video_formats])
        self.audio_combobox.configure(values=[fmt_string(f) for f in audio_formats])

        if video_formats:
            self.video_combobox.set(fmt_string(video_formats[0]))
        if audio_formats:
            self.audio_combobox.set(fmt_string(audio_formats[0]))

        self.video_ids = {fmt_string(f): f['format_id'] for f in video_formats}
        self.audio_ids = {fmt_string(f): f['format_id'] for f in audio_formats}

    def get_selected_format_ids(self):
        video_fmt = self.video_combobox.get()
        audio_fmt = self.audio_combobox.get()
        return self.video_ids.get(video_fmt), self.audio_ids.get(audio_fmt)

