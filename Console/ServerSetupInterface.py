import customtkinter
import threading

from CTkMessagebox import CTkMessagebox
from PIL import Image
from MulticolorCTkLabel import MultiColorLabel
from ServerConsole import Server


class ServerSetupInterface(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.title("Server Setup")
        self.server: Server | None = None
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

        self.server_event = threading.Event()
        self.fill_config_interface()

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
        self.server_info_label.pack(pady=40, fill=customtkinter.X, expand=True)

        self.server_status_label = MultiColorLabel(self.main_frame, fg_color="transparent", font=("Arial", 15, "bold"), corner_radius=10, height=70, width=50)
        self.server_status_label.add("Server status:\n", "white")
        self.server_status_label.add("    Running...", "green")
        self.server_status_label.pack(pady=0, padx=60, fill=customtkinter.X, expand=True)

        self.running_server_progress_bar = customtkinter.CTkProgressBar(self.main_frame, 100, corner_radius=10, mode="indeterminate", progress_color="green")
        self.running_server_progress_bar.pack(pady=5, padx=20, fill=customtkinter.X, expand=True)
        self.running_server_progress_bar.start()

        self.stop_server_button = customtkinter.CTkButton(self.main_frame, text="Stop server", font=("Arial", 15, "bold"),
                                                          corner_radius=10, fg_color="red", hover_color="dark red", command=self.stop_server, state=customtkinter.NORMAL)
        self.stop_server_button.pack(pady=30, fill=customtkinter.BOTH, expand=True, padx=50)

        self.restart_server_button = customtkinter.CTkButton(self.main_frame, text="Restart server", font=("Arial", 15, "bold"), corner_radius=10, fg_color="green", hover_color="dark green", command=self.restart_server, state=customtkinter.NORMAL)

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
            server_thread = threading.Thread(target=self.server.start, args=(self.server_event,))
            server_thread.start()
            self.self_hide_config_interface()
            self.fill_status_interface()
        elif self.msg.get() == "Change settings":
            self.msg.destroy()
            self.server = None
            self.start_button.configure(state=customtkinter.NORMAL)

    def stop_server(self):
        self.server_event.clear()
        self.server_status = False
        self.server_status_label.remove("    Running...")
        self.server_status_label.add("    Stopped", "red")
        self.running_server_progress_bar.configure(progress_color="red")
        self.running_server_progress_bar.stop()
        self.stop_server_button.pack_forget()
        self.restart_server_button.pack(pady=30, fill=customtkinter.BOTH, expand=True, padx=50)

    def restart_server(self):
        self.server_event.set()
        self.server_status = True
        self.server_status_label.remove("    Stopped")
        self.server_status_label.add("    Running...", "green")
        self.running_server_progress_bar.configure(progress_color="green")
        self.running_server_progress_bar.start()
        self.restart_server_button.pack_forget()
        self.stop_server_button.pack(pady=30, fill=customtkinter.BOTH, expand=True, padx=50)

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
            self.server_event.set()
            self.show_server_status()

    def on_close(self):
        try:
            self.msg.destroy()
        except AttributeError:
            pass
        try:
            self.server.stop()
        except:
            pass
        self.destroy()


if __name__ == '__main__':
    app = ServerSetupInterface()
    app.mainloop()
