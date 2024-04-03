import tkinter as tk
import sys
import subprocess
import customtkinter as ctk


class MainInterface(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Pokemon Setup")

        # Center the window
        width = 350
        height = 400

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        # Main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        pass

    def place_widgets(self):
        pass

    def on_close(self):
        self.destroy()


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="#1B1B1B")
        self.master = master

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.console_text = ctk.CTkTextbox(self, wrap=tk.WORD, width=500, height=500, font=("Cascadia Code", 12), fg_color="#1B1B1B", corner_radius=10)
        self.console_text.configure(scrollbar_button_color="", scrollbar_button_hover_color="") #Make scroll-bar invisible

    def place_widgets(self):
        self.console_text.pack(anchor="center", pady=10, padx=10) #Anchor the console box to the middle of the screen and add some padding


class ConsoleRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Auto-scroll to the bottom


# Start the Tkinter event loop
if __name__ == "__main__":
    root = MainInterface()
    sys.stdout = ConsoleRedirector(root.main_frame.console_text)
    sys.stderr = ConsoleRedirector(root.main_frame.console_text)
    root.mainloop()