import os
from typing import List

def write_product_files(list_of_contents: List[str]):
    """
    Create or rewrite product files (Product 1 - Product 5) inside the 'output' directory
    located in the previous directory relative to this script.
    """
    # Get the parent directory of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    output_dir = os.path.join(parent_dir, 'output')

    # Ensure the 'output' directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create or rewrite product files based on the provided contents
    for i, content in enumerate(list_of_contents, start=1):
        file_name = f"Product {i}.txt"
        file_path = os.path.join(output_dir, file_name)

        # Write content to the file using UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"File written: {file_path}")