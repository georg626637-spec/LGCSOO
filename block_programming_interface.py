import tkinter as tk
from tkinter import messagebox

class Block:
    """Represents a draggable block in the canvas"""
    def __init__(self, canvas, x, y, block_type, block_id):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.block_type = block_type
        self.block_id = block_id
        self.width = 100
        self.height = 80
        self.inputs = []
        self.outputs = []
        self.dragging = False
        
        # Define block colors based on type
        colors = {
            'AND': '#FF6B6B',
            'OR': '#4ECDC4',
            'NOT': '#45B7D1',
            'XOR': '#FFA07A',
            'INPUT': '#95E1D3',
            'OUTPUT': '#F38181'
        }
        self.color = colors.get(block_type, '#95E1D3')
        self.draw()
        
    def draw(self):
        """Draw the block on canvas"""
        # Draw block rectangle
        self.rect = self.canvas.create_rectangle(
            self.x - self.width//2, self.y - self.height//2,
            self.x + self.width//2, self.y + self.height//2,
            fill=self.color, outline='black', width=2, tags='block'
        )
        
        # Draw block label
        self.label = self.canvas.create_text(
            self.x, self.y - 10,
            text=self.block_type,
            font=('Arial', 10, 'bold'),
            tags='block'
        )
        
        # Draw input/output connectors
        self.draw_connectors()
        
    def draw_connectors(self):
        """Draw input and output connection points"""
        connector_radius = 4
        
        if self.block_type not in ['INPUT', 'OUTPUT']:
            # Input connectors on left
            if self.block_type == 'NOT':
                num_inputs = 1
            else:
                num_inputs = 2
            
            for i in range(num_inputs):
                input_y = self.y - self.height//2 + 20 + i * 20
                self.canvas.create_oval(
                    self.x - self.width//2 - connector_radius,
                    input_y - connector_radius,
                    self.x - self.width//2 + connector_radius,
                    input_y + connector_radius,
                    fill='green', outline='black', tags='connector'
                )
                self.inputs.append((self.x - self.width//2, input_y))
            
            # Output connector on right
            output_y = self.y
            self.canvas.create_oval(
                self.x + self.width//2 - connector_radius,
                output_y - connector_radius,
                self.x + self.width//2 + connector_radius,
                output_y + connector_radius,
                fill='red', outline='black', tags='connector'
            )
            self.outputs.append((self.x + self.width//2, output_y))
        
        elif self.block_type == 'INPUT':
            # Input has only output
            output_y = self.y
            self.canvas.create_oval(
                self.x + self.width//2 - connector_radius,
                output_y - connector_radius,
                self.x + self.width//2 + connector_radius,
                output_y + connector_radius,
                fill='red', outline='black', tags='connector'
            )
            self.outputs.append((self.x + self.width//2, output_y))
        
        elif self.block_type == 'OUTPUT':
            # Output has only input
            input_y = self.y
            self.canvas.create_oval(
                self.x - self.width//2 - connector_radius,
                input_y - connector_radius,
                self.x - self.width//2 + connector_radius,
                input_y + connector_radius,
                fill='green', outline='black', tags='connector'
            )
            self.inputs.append((self.x - self.width//2, input_y))
    
    def contains(self, x, y):
        """Check if coordinates are within block"""
        return (self.x - self.width//2 <= x <= self.x + self.width//2 and
                self.y - self.height//2 <= y <= self.y + self.height//2)
    
    def move(self, dx, dy):
        """Move block and update connectors"""
        self.x += dx
        self.y += dy
        self.canvas.delete(self.rect, self.label)
        # Delete all connector ovals before redrawing
        self.canvas.delete('connector')
        self.inputs = []
        self.outputs = []
        self.draw()
    
    def get_input_connector(self, index=0):
        """Get position of input connector"""
        return self.inputs[index] if index < len(self.inputs) else None
    
    def get_output_connector(self, index=0):
        """Get position of output connector"""
        return self.outputs[index] if index < len(self.outputs) else None


class BlockProgrammingInterface:
    """Main GUI window for block programming"""
    def __init__(self, root):
        self.root = root
        self.root.title("Logic Gate Block Programming Interface - Scratch Style")
        self.root.geometry("1200x700")
        
        self.blocks = {}
        self.connections = []
        self.selected_block = None
        self.connecting = False
        self.connection_start = None
        self.connection_text_id = None
        
        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar for tools
        sidebar = tk.Frame(main_frame, width=150, bg='#f0f0f0', relief=tk.SUNKEN, bd=2)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        sidebar.pack_propagate(False)
        
        # Add title
        title = tk.Label(sidebar, text="Gate Blocks", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        title.pack(pady=10)
        
        # Add buttons for each gate type
        gate_types = ['INPUT', 'AND', 'OR', 'NOT', 'XOR', 'OUTPUT']
        for gate in gate_types:
            btn = tk.Button(sidebar, text=f"Add {gate}", width=14,
                           command=lambda g=gate: self.add_block(g))
            btn.pack(pady=5, padx=5)
        
        # Add separator
        tk.Frame(sidebar, height=2, bg='gray', relief=tk.SUNKEN, bd=1).pack(fill=tk.X, pady=10)
        
        # Add control buttons
        clear_btn = tk.Button(sidebar, text="Clear All", width=14, command=self.clear_all, bg='#ffcccc')
        clear_btn.pack(pady=5, padx=5)
        
        simulate_btn = tk.Button(sidebar, text="Simulate", width=14, command=self.simulate, bg='#ccffcc')
        simulate_btn.pack(pady=5, padx=5)
        
        # Create canvas
        self.canvas = tk.Canvas(main_frame, bg='white', cursor='cross')
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_canvas_release)
        self.canvas.bind('<Button-3>', self.on_canvas_right_click)
        
        self.block_counter = 0
    
    def add_block(self, block_type):
        """Add a new block to canvas"""
        # Add block at default position
        x, y = 300 + (self.block_counter % 5) * 120, 100 + (self.block_counter // 5) * 120
        block_id = f"{block_type}_{self.block_counter}"
        self.blocks[block_id] = Block(self.canvas, x, y, block_type, block_id)
        self.block_counter += 1
    
    def on_canvas_click(self, event):
        """Handle canvas click"""
        # Find clicked block
        for block_id, block in self.blocks.items():
            if block.contains(event.x, event.y):
                self.selected_block = block
                block.dragging = True
                self.last_x = event.x
                self.last_y = event.y
                break
    
    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if self.selected_block and self.selected_block.dragging:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.selected_block.move(dx, dy)
            self.last_x = event.x
            self.last_y = event.y
            self.redraw_connections()
    
    def on_canvas_release(self, event):
        """Handle mouse release"""
        if self.selected_block:
            self.selected_block.dragging = False
            self.selected_block = None
    
    def on_canvas_right_click(self, event):
        """Handle right click for connections"""
        for block_id, block in self.blocks.items():
            if block.contains(event.x, event.y):
                if not self.connecting:
                    self.connecting = True
                    self.connection_start = block
                    self.connection_text_id = self.canvas.create_text(event.x, event.y - 30, text="Click target", 
                                           fill='blue', font=('Arial', 8))
                else:
                    # Complete connection
                    if block != self.connection_start:
                        self.connections.append((self.connection_start, block))
                        self.draw_connection(self.connection_start, block)
                    self.connecting = False
                    self.connection_start = None
                    # Delete the instruction text
                    if self.connection_text_id:
                        self.canvas.delete(self.connection_text_id)
                        self.connection_text_id = None
                break
    
    def draw_connection(self, from_block, to_block):
        """Draw a connection line between blocks"""
        from_connector = from_block.get_output_connector()
        to_connector = to_block.get_input_connector()
        
        # Check if connectors exist before drawing
        if from_connector and to_connector:
            from_x, from_y = from_connector
            to_x, to_y = to_connector
            self.canvas.create_line(from_x, from_y, to_x, to_y,
                                   fill='blue', width=2, tags='connection')
    
    def redraw_connections(self):
        """Redraw all connections"""
        self.canvas.delete('connection')
        for from_block, to_block in self.connections:
            self.draw_connection(from_block, to_block)
    
    def clear_all(self):
        """Clear all blocks and connections"""
        if messagebox.askyesno("Clear", "Are you sure you want to clear all?"):
            self.canvas.delete('all')
            self.blocks = {}
            self.connections = []
            self.block_counter = 0
    
    def simulate(self):
        """Simulate the circuit"""
        messagebox.showinfo("Simulate", "Circuit simulation feature coming soon!\n\nYour circuit has:\n" + 
                           f"- {len(self.blocks)} blocks\n" +
                           f"- {len(self.connections)} connections")


def main():
    root = tk.Tk()
    app = BlockProgrammingInterface(root)
    root.mainloop()


if __name__ == '__main__':
    main()