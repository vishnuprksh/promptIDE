import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Checkbuttons and Radiobuttons")
window.geometry("400x300")

# Variables to store the state of checkbuttons and radiobuttons
check_var = tk.IntVar()
radio_var = tk.StringVar()

# Checkbutton widget
checkbutton = tk.Checkbutton(window, text="Check me", variable=check_var)
checkbutton.pack(pady=10)

# Radiobutton widgets
radio1 = tk.Radiobutton(window, text="Option 1", variable=radio_var, value="Option 1")
radio1.pack()
radio2 = tk.Radiobutton(window, text="Option 2", variable=radio_var, value="Option 2")
radio2.pack()

# Function to display selected options
def show_selected():
    result_label.config(text=f"Selected: Check - {check_var.get()}, Radio - {radio_var.get()}")

# Button to show selected options
show_button = tk.Button(window, text="Show Selected", command=show_selected)
show_button.pack(pady=20)

# Label to display selected options
result_label = tk.Label(window, text="")
result_label.pack()

# Display the window
window.mainloop()
