class BlockProgrammingInterface:
    def __init__(self):
        self.connections = []  # List to store connections
        self.connection_line_ids = {}  # To store line IDs

    def validate_connection(self, output_block, input_connector):
        # Ensure output blocks only connect to input connectors
        if output_block.type != 'output' or input_connector.type != 'input':
            raise ValueError("Invalid connection: An output block cannot be connected to another output block.")

    def add_connection(self, output_block, input_connector):
        self.validate_connection(output_block, input_connector)
        connection_id = len(self.connections)
        self.connections.append((output_block, input_connector))
        self.connection_line_ids[connection_id] = self.draw_connection(output_block, input_connector)
        self.highlight_connector(input_connector)

    def remove_connection(self, connection_id):
        if connection_id in self.connection_line_ids:
            # Logic to remove the wire (depends on the drawing library used)
            self.delete_connection_line(self.connection_line_ids[connection_id])
            del self.connection_line_ids[connection_id]
            del self.connections[connection_id]

    def draw_connection(self, output_block, input_connector):
        # Method to visually represent the connection (placeholder)
        pass

    def delete_connection_line(self, line_id):
        # Logic to delete connection line on canvas (placeholder)
        pass

    def highlight_connector(self, connector):
        # Logic to highlight connector points (placeholder)
        pass

    def remove_connection_by_click(self, line_id):
        # Detect clicks on connection lines and remove them
        if line_id in self.connection_line_ids:
            self.remove_connection(line_id)
