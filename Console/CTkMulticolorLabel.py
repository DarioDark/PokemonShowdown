import customtkinter


class MultiColorLabel(customtkinter.CTkTextbox):
    def __init__(self, *args, **kwargs):
        customtkinter.CTkTextbox.__init__(self, *args, **kwargs)

        # Disable text editing
        self.configure(state=customtkinter.DISABLED)

    def add(self, text, color):
        tag = "tag_" + str(len(self.tag_names()))

        # Enable text editing
        self.configure(state=customtkinter.NORMAL)

        self.insert(customtkinter.END, text, tag)
        self.tag_config(tag, foreground=color)

        # Disable text editing
        self.configure(state=customtkinter.DISABLED)

    def remove(self, text):
        # Enable text editing
        self.configure(state=customtkinter.NORMAL)
        for tag in self.tag_names()[1:]:
            tag_text = self.get(f"{tag}.first", f"{tag}.last")
            if tag_text == text:
                self.delete(f"{tag}.first", f"{tag}.last")
                self.tag_delete(tag)

        # Disable text editing
        self.configure(state=customtkinter.DISABLED)