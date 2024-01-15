import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("My Tkinter Window")
window.geometry("400x300")

# Add a label
label = tk.Label(window, text="Enter your name:")
label.pack()

# Add an entry widget
entry = tk.Entry(window)
entry.pack()

# Display the window
window.mainloop()
