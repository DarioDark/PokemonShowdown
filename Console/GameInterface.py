import customtkinter as ctk

from TeamBuilderInterface3 import TeambuilderInterface


class MainInterface(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Game Interface")

        # Center the window
        width = 350
        height = 400

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        t = TeambuilderInterface
        t.mainloop()

        self.create_widgets()
        self.place_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        self.main_frame = MainFrame(self)

    def place_widgets(self):
        self.main_frame.pack(expand=True, fill=ctk.BOTH, padx=50, pady=50)

    def on_close(self):
        self.destroy()



class MainFrame(ctk.CTkFrame):
    def __init__(self, master, corner_radius: int = 10):
        super().__init__(master, corner_radius=corner_radius)
        self.master = master

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.server_button = ctk.CTkButton(self, text="Server setup", font=("Arial", 15, "bold"), corner_radius=10, command=self.open_server,
                                           fg_color="#3C3C3C", hover_color="#2B2B2B", border_color="red", border_width=2)
        self.teambuilder_button = ctk.CTkButton(self, text="Teambuilder", font=("Arial", 15, "bold"), corner_radius=10, command=self.open_teambuilder,
                                                fg_color="#3C3C3C", hover_color="#2B2B2B", border_color="red", border_width=2)
        self.play_button = ctk.CTkButton(self, text="Play", font=("Arial", 15, "bold"), corner_radius=10, command=self.open_teambuilder,
                                                fg_color="#3C3C3C", hover_color="#2B2B2B", state=ctk.DISABLED)

    def place_widgets(self):
        self.server_button.pack(pady=15, fill=ctk.BOTH, expand=True, padx=20)
        self.teambuilder_button.pack(pady=15, fill=ctk.BOTH, expand=True, padx=20)
        self.play_button.pack(pady=15, fill=ctk.BOTH, expand=True, padx=20)

    def open_server(self):
        pass

    def open_teambuilder(self):
        pass


if __name__ == '__main__':
    m = MainInterface()
    m.mainloop()
