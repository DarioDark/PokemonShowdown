import customtkinter

from CTkMessagebox import CTkMessagebox
from PIL import Image
from ServerConsole import Server

class ServerSetupInterface(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.title("Server Setup")
        self.server_status: bool = False

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
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(expand=True, fill=customtkinter.BOTH, padx=50, pady=50)

        self.fill_status_interface()


        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def fill_config_interface(self):
        self.title_label = customtkinter.CTkLabel(self.main_frame, text="Server Setup", font=("Arial", 20, "bold"), corner_radius=10, text_color="white")
        self.host_entry = customtkinter.CTkEntry(self.main_frame, 50, placeholder_text="IP Address")
        self.port_entry = customtkinter.CTkEntry(self.main_frame, 50, placeholder_text="Port")
        settings_image = customtkinter.CTkImage(Image.open("../Images/settings-icon-disabled.png"), size=(20, 20))
        self.start_button = customtkinter.CTkButton(self.main_frame, text="Check config", font=("Arial", 15, "bold"), corner_radius=10,
                                                    command=self.start_server, state=customtkinter.DISABLED, image=settings_image, compound="left", text_color=("white", "white"))

        self.host_entry.bind("<KeyRelease>", self.check_entries)
        self.port_entry.bind("<KeyRelease>", self.check_entries)

        self.title_label.pack(pady=3, fill=customtkinter.X, expand=True)
        self.host_entry .pack(pady=3, fill=customtkinter.X, expand=True, padx=50)
        self.port_entry .pack(pady=3, fill=customtkinter.X, expand=True, padx=50)
        self.start_button.pack(pady=3, fill=customtkinter.X, expand=True, padx=50)

    def fill_status_interface(self):
        self.server_info_label = customtkinter.CTkLabel(self.main_frame, text="Server Info", font=("Arial", 20, "bold"), corner_radius=10, text_color="white")
        self.server_info_label.pack(pady=3, fill=customtkinter.X, expand=True)

        self.server_status_label = customtkinter.CTkLabel(self.main_frame, text="Server status: Not running", font=("Arial", 15, "bold"), corner_radius=10, text_color="white")
        self.server_status_label.pack(pady=3, fill=customtkinter.X, expand=True)
        if self.server_status:
            self.server_status_label.configure(text="Server status: Running", text_color="green")


        self.running_server_progress_bar = customtkinter.CTkProgressBar(self.main_frame, 100, corner_radius=10, mode="indeterminate")
        self.running_server_progress_bar.pack(pady=3, padx=10, fill=customtkinter.X, expand=True)
        self.running_server_progress_bar.start()



    def self_hide_config_interface(self):
        self.title_label.pack_forget()
        self.host_entry.pack_forget()
        self.port_entry.pack_forget()
        self.start_button.pack_forget()

    def entry_filled(self) -> bool:
        return self.host_entry.get() != '' and self.port_entry.get() != ''

    def check_entries(self, event):
        if self.host_entry.get() and self.port_entry.get():
            self.start_button.configure(state=customtkinter.NORMAL)
        else:
            self.start_button.configure(state=customtkinter.DISABLED)

    def start_server(self) -> None:
        if not self.entry_filled():
            return
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        try:
            self.server = Server(host, port)
        except WindowsError as e:
            if e.winerror == 10048:
                self.server_status: bool = False
        else:
            self.server_status: bool = True
        finally:
            self.show_server_status()

    def show_server_status(self):
        self.start_button.configure(state=customtkinter.DISABLED)
        if self.server_status:
            self.msg = self.server_response_window = CTkMessagebox(self, title="Server status",
                                                                    message=f"The server is ready to start with the provided settings.",
                                                                    corner_radius=10, icon="check", option_1="Start", option_3="Change settings", button_width=10)
        else:
            self.msg = self.server_response_window = CTkMessagebox(self, title="Server status",
                                                        message="The server cannot be started with the current settings.",
                                                        corner_radius=10,
                                                        icon="cancel")
        if self.msg.get() == "Start":
            self.server.start(self)
        elif self.msg.get() == "Change settings":
            self.msg.destroy()
            self.start_button.configure(state=customtkinter.NORMAL)

    def on_close(self):
        try:
            self.msg.destroy()
        except AttributeError:
            pass
        self.destroy()


if __name__ == '__main__':
    app = ServerSetupInterface()
    app.mainloop()
