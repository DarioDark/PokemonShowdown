import customtkinter as ctk
from typing import Literal


class CTkSeparator(ctk.CTkFrame):
    def __init__(self, master, orient: Literal["horizontal", "vertical"], fg_color: str, length: int):
        super().__init__(master)
        self.orient: Literal["horizontal", "vertical"] = orient
        self.fg_color: str = fg_color
        self.length: int = length
        if self.orient == "horizontal":
            self.configure(fg_color=fg_color, height=length, corner_radius=60)
        elif self.orient == "vertical":
            self.configure(fg_color=fg_color, width=length, corner_radius=60)
        else:
            raise ValueError("Invalid orientation for separator. Must be 'horizontal' or 'vertical'.")
