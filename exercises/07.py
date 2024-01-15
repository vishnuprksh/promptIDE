import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Frames and Containers")
window.geometry("400x300")

# Frame 1
frame1 = tk.Frame(window, bg="lightblue", bd=5)
frame1.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

# Frame 2
frame2 = tk.Frame(window, bg="lightgreen", bd=5)
frame2.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.5, anchor="n")

# Label inside Frame 1
label1 = tk.Label(frame1, text="This is Frame 1", bg="lightblue")
label1.pack(expand=True, fill="both")

# Label inside Frame 2
label2 = tk.Label(frame2, text="This is Frame 2", bg="lightgreen")
label2.pack(expand=True, fill="both")

# Display the window
window.mainloop()
