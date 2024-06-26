import customtkinter as ctk
import threading

from CTkMessagebox import CTkMessagebox
from CTkColoredTextbox import CTkColoredTextbox
from ServerConsole import Server


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

    def fill_status_interface(self):
        self.server_info_label = ctk.CTkLabel(self.main_frame, text="Server Info", font=("Arial", 20, "bold"), corner_radius=10, text_color="white")
        self.server_info_label.pack(pady=40, fill=ctk.X, expand=True)

        self.server_status_label = CTkColoredTextbox(self.main_frame, fg_color="transparent", font=("Arial", 15, "bold"), corner_radius=10, height=70, width=50)
        self.server_status_label.add("Server status:", "white", line_break=True)
        self.server_status_label.add("    Running", "green")
        self.server_status_label.pack(pady=0, padx=60, fill=ctk.X, expand=True)

        self.running_server_progress_bar = ctk.CTkProgressBar(self.main_frame, 100, corner_radius=10, mode="determinate", progress_color="green")
        self.running_server_progress_bar.pack(pady=5, padx=20, fill=ctk.X, expand=True)
        self.running_server_progress_bar.set(1)

        self.stop_server_button = ctk.CTkButton(self.main_frame, text="Stop server", font=("Arial", 15, "bold"),
                                                          corner_radius=10, fg_color="red", hover_color="dark red", command=self.stop_server,
                                                          state=ctk.NORMAL, text_color="white")

        self.restart_server_button = ctk.CTkButton(self.main_frame, text="Restart server", font=("Arial", 15, "bold"), corner_radius=10, fg_color="green",
                                                             hover_color="dark green", command=self.restart_server, state=ctk.NORMAL, text_color="white")

        self.stop_server_button.pack(pady=30, fill=ctk.BOTH, expand=True, padx=50)

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
            self.fill_status_interface()
        elif self.msg.get() == "Change settings":
            self.msg.destroy()
            self.server = None
            self.start_button.configure(state=ctk.NORMAL)

    def stop_server(self):
        self.server_event.clear()
        self.server.stop()
        self.server_status = False
        self.server_status_label.remove_last_tag()
        self.server_status_label.add("    Stopped", "red")
        self.running_server_progress_bar.configure(progress_color="red")

        self.stop_server_button.pack_forget()
        self.restart_server_button.pack(pady=30, fill=ctk.BOTH, expand=True, padx=50)
        self.restart_server_button.configure(state=ctk.DISABLED)

        self.master.after(500, lambda: self.restart_server_button.configure(state=ctk.NORMAL))

    def restart_server(self):
        self.server_event.set()
        self.server_status = True
        self.server_status_label.remove_last_tag()
        self.server_status_label.add("    Running", "green")
        self.running_server_progress_bar.configure(progress_color="green")

        self.restart_server_button.pack_forget()
        self.stop_server_button.pack(pady=30, fill=ctk.BOTH, expand=True, padx=50)
        self.stop_server_button.configure(state=ctk.DISABLED)

        self.master.after(500, lambda: self.stop_server_button.configure(state=ctk.NORMAL))

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
        self.master.destroy()


if __name__ == '__main__':
    app = ctk.CTk()
    server_interface = ServerInterface(app)
    server_interface.master.mainloop()
