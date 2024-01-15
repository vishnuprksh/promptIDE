import tkinter as tk
import random

class GridApp:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = 40

        self.canvas = tk.Canvas(master, width=cols * self.cell_size, height=rows * self.cell_size)
        self.canvas.pack()

        self.grid_data = [[random.choice(['red', 'blue', 'green', 'yellow']) for _ in range(cols)] for _ in range(rows)]

        self.draw_grid()

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = self.grid_data[row][col]
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root, rows=5, cols=5)
    root.mainloop()
