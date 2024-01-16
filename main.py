# main.py
import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk
import os
from functions import process_text

# Function to be called on button click
def on_send_click():
    input_prompt = prompt_textbox.get("1.0", tk.END).strip()
    input_content = response_textbox.get("1.0", tk.END).strip()
    output_text = process_text(input_prompt, input_content)
    response_textbox.delete("1.0", tk.END)
    response_textbox.insert(tk.END, output_text)

# Function to load content from a text file
def load_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        response_textbox.delete("1.0", tk.END)
        response_textbox.insert(tk.END, file_content)

# Function to save content to a text file
def save_file(file_path):
    with open(file_path, 'w') as file:
        file.write(response_textbox.get("1.0", tk.END))

# Function to update file list in the left panel
def update_file_list(folder_path):
    file_list.delete(0, tk.END)
    for file_name in os.listdir(folder_path):
        file_list.insert(tk.END, file_name)

# Function to handle file selection event
def on_file_select(event):
    selected_file = file_list.get(file_list.curselection())
    file_path = os.path.join(selected_folder, selected_file)
    update_file_content(file_path)

# Function to update content in response_textbox based on selected file
def update_file_content(file_path):
    load_file(file_path)

# Create main window
root = tk.Tk()
root.title("GUI")

# Create left panel with file list
left_panel = ttk.Frame(root, width=200, height=400)
left_panel.grid(row=0, column=0, sticky="nsew",rowspan=3)

file_list = tk.Listbox(left_panel)
file_list.pack(fill=tk.BOTH, expand=True)
file_list.bind("<<ListboxSelect>>", on_file_select)

# Create text boxes
prompt_textbox = scrolledtext.ScrolledText(root, height=5, width=50, wrap=tk.WORD)
prompt_textbox.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")

response_textbox = scrolledtext.ScrolledText(root, height=10, width=50, wrap=tk.WORD)
response_textbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", rowspan=3)

# Create button
send_button = tk.Button(root, text="Send", command=on_send_click)
send_button.grid(row=3, column=2, pady=10)

# Create file load button
load_button = tk.Button(root, text="Load File", command=lambda: load_file(selected_file_path))
load_button.grid(row=3, column=0, pady=10, padx=10)

# Create save button
save_button = tk.Button(root, text="Save", command=lambda: save_file(selected_file_path))
save_button.grid(row=0, column=2, pady=10, padx=10)

# Configure row and column weights to make the GUI responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Initialize folder and file path variables
selected_folder = "/home/vishnuprakash/promptIDE"
selected_file_path = "/home/vishnuprakash/promptIDE"


# Run the GUI
root.mainloop()
