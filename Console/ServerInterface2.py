import customtkinter as ctk
import threading

from CTkMessagebox import CTkMessagebox
from ServerConsole import Server
from ClientConsole import Client


class ServerInterface:
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.master = master
        self.master.title("Server Setup")
        self.server: Server | None = None
        self.server_status: bool = False

        # Center the window
        width = 350
        height = 400

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")
        self.master.resizable(False, False)

        self.master.attributes('-topmost', 1)

        # Main frame
        self.main_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.main_frame.pack(expand=True, fill=ctk.BOTH, padx=50, pady=50)

        self.server_event = threading.Event()
        self.fill_config_interface()

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def fill_config_interface(self):
        self.title_label = ctk.CTkLabel(self.main_frame, text="Server Setup", font=("Arial", 20, "bold"), corner_radius=10, text_color="white")
        self.host_entry = ctk.CTkEntry(self.main_frame, 50, placeholder_text="IP Address")
        self.port_entry = ctk.CTkEntry(self.main_frame, 50, placeholder_text="Port")
        self.start_button = ctk.CTkButton(self.main_frame, text="Check config", font=("Arial", 15, "bold"), corner_radius=10,
                                                    command=self.start_server, state=ctk.DISABLED, text_color=("white", "white"))

        self.host_entry.bind("<KeyRelease>", self.check_entries)
        self.port_entry.bind("<KeyRelease>", self.check_entries)

        self.title_label.pack(pady=3, fill=ctk.X, expand=True)
        self.host_entry .pack(pady=3, fill=ctk.X, expand=True, padx=50)
        self.port_entry .pack(pady=3, fill=ctk.X, expand=True, padx=50)
        self.start_button.pack(pady=3, fill=ctk.X, expand=True, padx=54)


    def show_server_status(self):
        self.start_button.configure(state=ctk.DISABLED)
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
        elif self.msg.get() == "Change settings":
            self.msg.destroy()
            self.server = None
            self.start_button.configure(state=ctk.NORMAL)

    def self_hide_config_interface(self):
        self.title_label.pack_forget()
        self.host_entry.pack_forget()
        self.port_entry.pack_forget()
        self.start_button.pack_forget()

    def entry_filled(self) -> bool:
        return self.host_entry.get() != '' and self.port_entry.get() != ''

    def check_entries(self, event):
        if self.host_entry.get() and self.port_entry.get():
            self.start_button.configure(state=ctk.NORMAL)
        else:
            self.start_button.configure(state=ctk.DISABLED)

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
            self.client = Client(host, port)

    def on_close(self):
        try:
            self.msg.destroy()
        except AttributeError:
            pass
        try:
            self.server.stop()
        except:
            pass
        self.master.destroy()


if __name__ == '__main__':
    app = ctk.CTk()
    server_interface = ServerInterface(app)
    server_interface.master.mainloop()
