# Updated block_programming_interface.py

# Import necessary libraries

class BlockProgrammingInterface:
    def __init__(self):
        self.connections = []  # To store current connections
        self.connection_lines = {}  # To track line IDs

    def add_connection(self, output, input):
        # Validation: Ensure connections are output to input
        if not self.validate_connection(output, input):
            raise ValueError("Invalid connection: must connect output to input.")

        # Add the connection
        connection_id = self.create_connection_line(output, input)
        self.connections.append((output, input))
        self.connection_lines[connection_id] = (output, input)

    def validate_connection(self, output, input):
        # Add condition to check that output and input are valid
        return output.is_output() and input.is_input()

    def remove_connection(self, wire_id):
        # Remove connection by clicking on wire
        if wire_id in self.connection_lines:
            del self.connection_lines[wire_id]
            self.connections = [c for c in self.connections if c[0] != wire_id]
            print(f"Connection {wire_id} removed.")
        else:
            raise ValueError("No connection found for the given wire ID.")

    def create_connection_line(self, output, input):
        # Implementation to create a visual connection line
        # This will return a unique ID for this connection
        return len(self.connections) + 1  # Example placeholder logic

    def handle_error(self, error):
        print(f"Error occurred: {error}")  # Improved error checking

    # Additional methods and functionality here
