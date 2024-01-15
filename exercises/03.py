import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Pack Geometry Manager")
window.geometry("400x300")

# Label 1 using Pack
label1 = tk.Label(window, text="Label 1 - Top", bg="yellow")
label1.pack(side="top")

# Label 2 using Pack
label2 = tk.Label(window, text="Label 2 - Bottom", bg="cyan")
label2.pack(side="bottom")

# Label 3 using Pack
label3 = tk.Label(window, text="Label 3 - Left", bg="pink")
label3.pack(side="left")

# Label 4 using Pack
label4 = tk.Label(window, text="Label 4 - Right", bg="lightgreen")
label4.pack(side="right")

# Display the window
window.mainloop()
