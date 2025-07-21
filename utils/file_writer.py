import os
from datetime import datetime
from typing import List

def write_result_file(lines: List[str], keyword: str) -> str:
    """
    Write filtered lines to a result file with the format: result_ddMMyyyy@keyword.txt
    
    Args:
        lines: List of lines to write
        keyword: The keyword that was used for filtering
        
    Returns:
        The name of the created output file
    """
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with current date and keyword
    current_date = datetime.now().strftime('%d%m%Y')
    filename = f"result_{current_date}@{keyword}.txt"
    output_path = os.path.join(output_dir, filename)
    
    # Write lines to file (preserving original content exactly)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # Log the operation
    _log_operation(keyword, len(lines), filename)
    
    return filename

def _log_operation(keyword: str, match_count: int, filename: str):
    """
    Log the filtering operation to logs.txt
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] Keyword: {keyword}, Matches: {match_count}, Output: {filename}\n"
    
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(log_message) 
