import customtkinter as ctk


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # self.grid_columnconfigure(0)

        ctk.CTkLabel(self, text="SELECT VIDEO QUALITY").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.video_combobox = ctk.CTkComboBox(self, values=[""])
        self.video_combobox.grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkLabel(self, text="SELECT AUDIO QUALITY").grid(
            row=0, column=1, padx=10, pady=10
        )
        self.audio_combobox = ctk.CTkComboBox(self, values=[""])
        self.audio_combobox.grid(row=1, column=1, padx=10, pady=10)

    def update_formats(self, formats):
        video_formats = []
        audio_formats = []

        for f in formats:
            if f.get("vcodec") != "none" and f.get("acodec") == "none":
                video_formats.append(f)
            elif f.get("vcodec") == "none" and f.get("acodec") != "none":
                audio_formats.append(f)

        def fmt_string(f):
            return f"{f['format_id']} - {f.get('format_note', '')} - {f['ext']}"

        self.video_combobox.configure(values=[fmt_string(f) for f in video_formats])
        self.audio_combobox.configure(values=[fmt_string(f) for f in audio_formats])

        if video_formats:
            self.video_combobox.set(fmt_string(video_formats[0]))
        if audio_formats:
            self.audio_combobox.set(fmt_string(audio_formats[0]))

        self.video_ids = {fmt_string(f): f["format_id"] for f in video_formats}
        self.audio_ids = {fmt_string(f): f["format_id"] for f in audio_formats}

    def get_selected_format_ids(self):
        video_fmt = self.video_combobox.get()
        audio_fmt = self.audio_combobox.get()
        return self.video_ids.get(video_fmt), self.audio_ids.get(audio_fmt)
