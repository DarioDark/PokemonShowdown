import customtkinter as ctk

class CTkSeparator(ctk.CTkFrame):
    def __init__(self, master, orient: str = "horizontal"):
        super().__init__(master)
        self.orient = orient
        if self.orient == "horizontal":
            self.configure(fg_color="#1A1A1A", height=3, corner_radius=60)
        elif self.orient == "vertical":
            self.configure(fg_color="#1A1A1A", width=3, corner_radius=60)
        else:
            raise ValueError("Invalid orientation for separator. Must be 'horizontal' or 'vertical'.")
