import tkinter as tk

class Block:
    def __init__(self, canvas, x, y, gate_type):
        self.canvas = canvas
        self.gate_type = gate_type
        self.rect = canvas.create_rectangle(x, y, x + 100, y + 50, fill='lightgrey')
        self.label = canvas.create_text(x + 50, y + 25, text=gate_type)
        self.canvas.tag_bind(self.rect, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.rect, '<B1-Motion>', self.on_drag)

        self.offset_x = 0
        self.offset_y = 0

    def on_press(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        x = self.canvas.canvasx(event.x - self.offset_x)
        y = self.canvas.canvasy(event.y - self.offset_y)
        self.canvas.moveto(self.rect, x, y)
        self.canvas.moveto(self.label, x + 50, y + 25)

class CircuitBuilder:
    def __init__(self, master):
        self.master = master
        master.title("Circuit Builder")
        self.canvas = tk.Canvas(master, bg='white', width=800, height=600)
        self.canvas.pack()
        
        self.create_blocks()

    def create_blocks(self):
        Block(self.canvas, 50, 50, 'AND')
        Block(self.canvas, 200, 50, 'OR')
        Block(self.canvas, 50, 150, 'NOT')
        Block(self.canvas, 200, 150, 'XOR')

if __name__ == "__main__":
    root = tk.Tk()
    circuit_builder = CircuitBuilder(root)
    root.mainloop()