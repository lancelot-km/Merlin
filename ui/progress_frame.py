import customtkinter as ctk

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(pady=5, padx=10, fill="both")
        
        # Create the text box for displaying logs
        self.text_box = ctk.CTkTextbox(self, height=100, wrap="word")
        self.text_box.pack(fill="x")

    def append_text(self, text):
        # Append the log text to the textbox and scroll to the bottom
        self.text_box.insert("end", text + "\n")
        self.text_box.yview_moveto(1)  # Scroll to the bottom

