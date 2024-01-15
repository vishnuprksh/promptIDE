import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Buttons and Event Handling")
window.geometry("400x300")

# Function to handle button click
def on_button_click():
    label.config(text="Button Clicked!")

# Button widget
button = tk.Button(window, text="Click Me!", command=on_button_click)
button.pack(pady=20)

# Label to display event response
label = tk.Label(window, text="")
label.pack()

# Display the window
window.mainloop()
