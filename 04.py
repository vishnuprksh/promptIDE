import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Grid Geometry Manager")
window.geometry("400x300")

# Label 1 in the first row, first column
label1 = tk.Label(window, text="Label 1", bg="yellow")
label1.grid(row=0, column=0)

# Label 2 in the first row, second column
label2 = tk.Label(window, text="Label 2", bg="cyan")
label2.grid(row=0, column=1)

# Label 3 in the second row, first column
label3 = tk.Label(window, text="Label 3", bg="pink")
label3.grid(row=1, column=0)

# Label 4 in the second row, second column
label4 = tk.Label(window, text="Label 4", bg="lightgreen")
label4.grid(row=1, column=1)

# Display the window
window.mainloop()
