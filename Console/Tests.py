import customtkinter



# Usage
root = customtkinter.CTk()
label = MultiColorLabel(root)
label.pack()

label.add("Hello ", "red")
label.add("world!", "blue")

root.mainloop()