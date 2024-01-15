import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Place Geometry Manager")
window.geometry("400x300")

# Label placed using the Place geometry manager
label_place = tk.Label(window, text="Placed Label", bg="yellow")
label_place.place(relx=0.5, rely=0.5, anchor="center")

# Button placed using the Place geometry manager
button_place = tk.Button(window, text="Click Me", command=lambda: label_place.config(text="Button Clicked!"))
button_place.place(relx=0.5, rely=0.7, anchor="center")

# Display the window
window.mainloop()
