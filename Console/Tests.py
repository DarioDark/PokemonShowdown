import tkinter as tk

# Création de la fenêtre principale
root = tk.Tk()
root.title("Séparateurs avec grid")

# Séparateur horizontal
separator_horizontal = tk.Frame(root, height=2, relief='sunken', bg='black')
separator_horizontal.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

# Texte entre les séparateurs
label = tk.Label(root, text="Contenu entre les séparateurs")
label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

# Séparateur vertical
separator_vertical = tk.Frame(root, width=2, relief='sunken', bg='black')
separator_vertical.grid(row=0, column=1, rowspan=2, sticky='ns', padx=5, pady=10)

# Lancement de la boucle principale
root.mainloop()