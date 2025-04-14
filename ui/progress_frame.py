import customtkinter as ctk


class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.text_box = ctk.CTkTextbox(self, wrap="word", height=400)
        self.text_box.grid(row=0, column=0, sticky="nsew")
        self.text_box.insert("1.0", "Download logs will appear here...\n")

    def append_text(self, text):
        self.text_box.insert("end", text + "\n")
        self.text_box.yview_moveto(1)
