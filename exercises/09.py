import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("To-Do List")

# List to store tasks
tasks = []

# Function to add a task
def add_task():
    task = entry.get()
    if task:
        tasks.append(task)
        update_listbox()

# Function to delete a task
def delete_task():
    selected_task = listbox.curselection()
    if selected_task:
        tasks.pop(selected_task[0])
        update_listbox()

# Function to update the listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)

# Entry widget for task input
entry = tk.Entry(window, width=30)
entry.grid(row=0, column=0, padx=10, pady=10)

# Buttons to add and delete tasks
add_button = tk.Button(window, text="Add Task", command=add_task)
add_button.grid(row=0, column=1, padx=5, pady=10)
delete_button = tk.Button(window, text="Delete Task", command=delete_task)
delete_button.grid(row=0, column=2, padx=5, pady=10)

# Listbox to display tasks
listbox = tk.Listbox(window, selectmode=tk.SINGLE, height=10, width=40)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Display the window
window.mainloop()
