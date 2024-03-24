import customtkinter as ctk


class CTkColoredTextbox(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        ctk.CTkTextbox.__init__(self, *args, **kwargs)

        self.configure(state=ctk.DISABLED)

    @property
    def last_tag(self):
        """Get the last tag in the label."""
        return self.tag_names()[-1]

    def add(self, text: str, color: str, **kwargs):
        """Add text to the label with a specific color.

        :param text: The text to add to the label.
        :param color: The color of the text.
        """
        tag = "tag_" + str(len(self.tag_names()))

        # Check if the keyword argument is valid
        if "line_break" in kwargs.keys():
            text += "\n"
        elif len(self.tag_names()) > 0:
            invalid_kwargs = [key for key in kwargs.keys() if key != "line_break"]
            if invalid_kwargs:
                raise ValueError(f"['{invalid_kwargs[0]}'] is not a valid keyword argument. Look at the documentation for supported arguments.")

        self.configure(state=ctk.NORMAL)

        self.insert(ctk.END, text, tag)
        self.tag_config(tag, foreground=color)

        self.configure(state=ctk.DISABLED)

    def change_color(self, text: str, new_color: str):
        """Change the color of a specific text in the label.

        :param text: The text to change the color of.
        :param new_color: The new color of the text.
        """
        self.configure(state=ctk.NORMAL)
        for tag in self.tag_names()[1:]:
            tag_text = self.get(f"{tag}.first", f"{tag}.last")
            if tag_text == text:
                self.tag_config(tag, foreground=new_color)
        self.configure(state=ctk.DISABLED)

    def change_color_last_tag(self, new_color: str):
        """Change the color of the last tag in the label.

        :param new_color: The new color of the last tag.
        """
        self.configure(state=ctk.NORMAL)
        self.tag_config(self.last_tag, foreground=new_color)
        self.configure(state=ctk.DISABLED)

    def change_color_all(self, new_color: str):
        """Change the color of all the text in the label.

        :param new_color: The new color of all the text in the label.
        """
        self.configure(state=ctk.NORMAL)
        for tag in self.tag_names()[1:]:
            self.tag_config(tag, foreground=new_color)
        self.configure(state=ctk.DISABLED)

    def remove(self, text: str):
        """Remove a specific text from the label.

        :param text: The text to remove from the label.
        """
        self.configure(state=ctk.NORMAL)
        for tag in self.tag_names()[1:]:
            tag_text = self.get(f"{tag}.first", f"{tag}.last")
            if tag_text == text:
                self.delete(f"{tag}.first", f"{tag}.last")
                self.tag_delete(tag)

        self.configure(state=ctk.DISABLED)

    def remove_last_tag(self):
        """Remove the last tag from the label."""
        self.configure(state=ctk.NORMAL)
        self.delete(f"{self.last_tag}.first", f"{self.last_tag}.last")
        self.tag_delete(self.last_tag)

        self.configure(state=ctk.DISABLED)

    def remove_all_tags(self):
        """Remove all the tags from the label."""
        self.configure(state=ctk.NORMAL)
        self.delete(1.0, ctk.END)
        self.configure(state=ctk.DISABLED)
