import tkinter as tk

def center_image_bottom():
    # Création de la fenêtre
    root = tk.Tk()
    root.geometry("400x400")

    # Création d'un canevas pour afficher l'image
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()

    # Chargement de l'image
    img = tk.PhotoImage(file="../Images/pixel-art-pokeball.png")

    # Affichage de l'image
    canvas.create_image(150, 300, anchor=tk.S, image=img)  # Ancre l'image en bas (S) du canevas

    root.mainloop()

# Appel de la fonction pour afficher la fenêtre
center_image_bottom()
