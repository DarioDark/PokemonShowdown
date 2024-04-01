import customtkinter as ctk
import threading
import socket

from CTkMessagebox import CTkMessagebox

from ServerConsole import Server
from ClientConsole import Client
from PlayerConsole import Player


class BaseServerInterface:
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel, player: Player, title: str):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.master = master
        self.master.title(title)
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

        self.player: Player = player

        # Main frame
        self.main_frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.main_frame.pack(expand=True, fill=ctk.BOTH, padx=50, pady=50)

    def on_close(self):
        try:
            self.server.stop()
        except AttributeError:
            pass
        self.master.destroy()


class HostServerInterface(BaseServerInterface):
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel, player: Player):
        super().__init__(master, player, "Server Setup")

        self.client: Client | None = None
        self.server: Server | None = None
        self.server_response_window: CTkMessagebox | None = None
        self.server_error: str = ""

        self.server_event = threading.Event()

        self.create_widgets()
        self.bind_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self.main_frame, text="Server Setup", font=("Arial", 20, "bold"), corner_radius=10, text_color="white")
        self.host_entry = ctk.CTkEntry(self.main_frame, 50, placeholder_text="IP Address")
        self.port_entry = ctk.CTkEntry(self.main_frame, 50, placeholder_text="Port")
        self.check_config_button = ctk.CTkButton(self.main_frame, text="Check config", font=("Arial", 15, "bold"), corner_radius=10,
                                                 command=self.start_server, state=ctk.DISABLED, text_color=("white", "white"))

    def bind_widgets(self):
        self.host_entry.bind("<KeyRelease>", self.check_entries)
        self.port_entry.bind("<KeyRelease>", self.check_entries)

    def place_widgets(self):
        self.title_label.pack(pady=3, fill=ctk.X, expand=True)
        self.host_entry.pack(pady=3, fill=ctk.X, expand=True, padx=50)
        self.port_entry.pack(pady=3, fill=ctk.X, expand=True, padx=50)
        self.check_config_button.pack(pady=3, fill=ctk.X, expand=True, padx=54)

    def show_server_status(self):
        self.check_config_button.configure(state=ctk.DISABLED)
        if self.server_status:
            self.server_response_window = CTkMessagebox(self.master, title="Server status", message=f"The server is ready to start with the provided settings.",
                                                        corner_radius=10, icon="check", option_1="Start", option_3="Change settings", button_width=10, text_color="green")
        else:
            self.server_response_window = CTkMessagebox(self.master, title="Server status", message=f"The server cannot be started with the current settings.\n{self.server_error}",
                                                        corner_radius=10, icon="cancel", option_1="Change settings", button_width=10, text_color="#C83E00")

        if self.server_response_window.get() == "Start":
            server_thread = threading.Thread(target=self.server.start, args=(self.server_event,))
            server_thread.start()
            self.master.destroy()
        else:
            self.server = None
            self.check_config_button.configure(state=ctk.NORMAL)

    def entry_filled(self) -> bool:
        return self.host_entry.get() != '' and self.port_entry.get() != ''

    def check_entries(self, event):
        if self.host_entry.get() and self.port_entry.get():
            self.check_config_button.configure(state=ctk.NORMAL)
        else:
            self.check_config_button.configure(state=ctk.DISABLED)

    def start_server(self) -> None:
        if not self.entry_filled():
            return

        host = self.host_entry.get()
        port = int(self.port_entry.get())

        try:
            self.server = Server(host, port)
        except WindowsError as e:
            self.server_status: bool = False
            if e.winerror == 10048:
                self.server_error = "The address and port are already in use !"
        except OverflowError:
            self.server_status: bool = False
            self.server_error = "The port must be between 0-65535 !"
        else:
            self.server_status: bool = True
        finally:
            self.server_event.set()
            self.show_server_status()

    def on_close(self):
        try:
            self.server_response_window.destroy()
        except AttributeError:
            pass
        super().on_close()


class ClientServerInterface(BaseServerInterface):
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel, player: Player):
        super().__init__(master, player, "Client Connection")
        self.title: str = "Client Connection"
        self.client: Client | None = None
        self.client_status: bool = False
        self.player: Player = player
        self.connection_error: str = ""

        self.create_widgets()
        self.bind_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self.main_frame, text=self.title, font=("Arial", 20, "bold"), corner_radius=10, text_color="white")
        self.host_entry = ctk.CTkEntry(self.main_frame, 50, placeholder_text="IP Address")
        self.port_entry = ctk.CTkEntry(self.main_frame, 50, placeholder_text="Port")
        self.connect_button = ctk.CTkButton(self.main_frame, text="Check config", font=("Arial", 15, "bold"), corner_radius=10,
                                            command=self.connect_to_server, state=ctk.DISABLED, text_color=("white", "white"))

    def bind_widgets(self):
        self.host_entry.bind("<KeyRelease>", self.check_entries)
        self.port_entry.bind("<KeyRelease>", self.check_entries)

    def place_widgets(self):
        self.title_label.pack(pady=3, fill=ctk.X, expand=True)
        self.host_entry.pack(pady=3, fill=ctk.X, expand=True, padx=50)
        self.port_entry.pack(pady=3, fill=ctk.X, expand=True, padx=50)
        self.connect_button.pack(pady=3, fill=ctk.X, expand=True, padx=54)

    # TODO fix this function
    def connect_to_server(self) -> None:
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        self.client = Client(self.player, host, port)
        try:
            self.client_status = bool(self.client.start())
            print(self.client_status)
            if self.client_status:
                self.show_server_status()
                return
        except socket.gaierror as e:
            if e.errno == 11001:
                self.client_status = False
                self.connection_error = "The IP adress is invalid !"
        except WindowsError as e:
            self.client_status = False
            if e.winerror == 10061:
                self.connection_error = "The server is not accepting connections with the provided settings."
            else:
                self.connection_error = f"An unknown error occurred ! : {e.winerror}"
        except ConnectionRefusedError:
            self.client_status = False
            self.connection_error = "The server is not accepting connections with the provided settings."
        except OverflowError:
            self.client_status = False
            self.connection_error = "The port must be between 0-65535!"
        except Exception as e:
            self.client_status = False
            self.connection_error = f"An unknown error occurred ! : {e}"
        else:
            self.client_status = True
        finally:
            self.show_server_status()

    def check_entries(self, event):
        if self.host_entry.get() and self.port_entry.get():
            self.connect_button.configure(state=ctk.NORMAL)
        else:
            self.connect_button.configure(state=ctk.DISABLED)

    def show_server_status(self):
        self.connect_button.configure(state=ctk.DISABLED)
        if self.server_status:
            self.server_response_window = CTkMessagebox(self.master, title="Server status", message=f"The server is ready to accept your device with the provided settings.",
                                                        corner_radius=10, icon="check", option_1="Connect", option_3="Change settings", button_width=10, text_color="green")
        else:
            self.server_response_window = CTkMessagebox(self.master, title="Server status", message=f"The server cannot accept your device with the provided settings :\n{self.connection_error}",
                                                        corner_radius=10, icon="cancel", option_1="Change settings", button_width=10, text_color="#C83E00")

        if self.server_response_window.get() == "Start":
            self.client.start()
            self.master.destroy()
        else:
            self.client = None
            self.connect_button.configure(state=ctk.NORMAL)


if __name__ == '__main__':
    player = Player("Player 1")
    app = ctk.CTk()
    server_interface = ClientServerInterface(app, player)
    server_interface.master.mainloop()
