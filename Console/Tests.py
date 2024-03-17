import customtkinter
from PIL import Image


root = customtkinter.CTk()


my_image = customtkinter.CTkImage(dark_image=Image.open("../Images/pixel-art-pokeball.png"), light_image=Image.open("../Images/pixel-art-pokeball.png"), size=(100, 100))

my_label = customtkinter.CTkLabel(root, text="", image=my_image)
my_label.pack(pady=10)

root.mainloop()
