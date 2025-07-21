from typing import List

def load_lines(file_path: str) -> List[str]:
    """
    Load lines from a text file with auto-encoding detection.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        List of lines from the file
        
    Raises:
        Exception: If file cannot be read with any encoding
    """
    encodings = ['utf-8', 'utf-16', 'cp1252', 'latin-1', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.readlines()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    raise Exception(f"Could not read file {file_path} with any supported encoding") 
