# main.py
import tkinter as tk
from tkinter import scrolledtext, filedialog
from functions import process_text

# Function to be called on button click
def on_send_click():
    input_prompt = prompt_textbox.get("1.0", tk.END).strip()
    input_content = response_textbox.get("1.0", tk.END).strip()
    output_text = process_text(input_prompt, input_content)
    response_textbox.delete("1.0", tk.END)
    response_textbox.insert(tk.END, output_text)

# Function to load content from a text file
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            file_content = file.read()
            response_textbox.delete("1.0", tk.END)
            response_textbox.insert(tk.END, file_content)

# Function to save content to a text file
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(response_textbox.get("1.0", tk.END))

# Create main window
root = tk.Tk()
root.title("GUI")

# Create text boxes
prompt_textbox = scrolledtext.ScrolledText(root, height=5, width=50, wrap=tk.WORD)
prompt_textbox.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

response_textbox = scrolledtext.ScrolledText(root, height=10, width=50, wrap=tk.WORD)
response_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)

# Create button
send_button = tk.Button(root, text="Send", command=on_send_click)
send_button.grid(row=2, column=1, pady=10)

# Create file load button
load_button = tk.Button(root, text="Load File", command=load_file)
load_button.grid(row=0, column=1, pady=10, padx=10)

# Create save button
save_button = tk.Button(root, text="Save", command=save_file)
save_button.grid(row=1, column=1, pady=10, padx=10)

# Configure row and column weights to make the GUI responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the GUI
root.mainloop()
