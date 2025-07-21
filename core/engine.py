import os
from typing import List
from utils.file_loader import load_lines
from utils.file_writer import write_result_file

def process_files(file_paths: List[str], keyword: str, progress_callback=None, cancellation_check=None) -> str:
    """
    Process multiple files, filter lines by keyword, and export results.
    
    Args:
        file_paths: List of file paths to process
        keyword: Keyword to search for (case-insensitive)
        progress_callback: Optional callback function(progress_percent, status_text) for progress updates
        cancellation_check: Optional function that returns True if processing should be cancelled
        
    Returns:
        Success message with output file details
    """
    if not file_paths:
        raise Exception("No files to process")
    
    if not keyword.strip():
        raise Exception("No keyword provided")
    
    keyword = keyword.strip()
    all_matching_lines = []
    total_files = len(file_paths)
    
    if progress_callback:
        progress_callback(0, f"Starting keyword search for '{keyword}'...")
    
    # Process each file
    for file_index, file_path in enumerate(file_paths):
        # Check for cancellation
        if cancellation_check and cancellation_check():
            raise Exception("Processing cancelled by user")
        
        try:
            # Update progress
            if progress_callback:
                progress_percent = int((file_index / total_files) * 100)
                progress_callback(
                    progress_percent,
                    f"Processing file {file_index + 1}/{total_files}: {os.path.basename(file_path)}"
                )
            
            # Load lines from file
            lines = load_lines(file_path)
            
            # Filter lines containing the keyword (case-insensitive)
            matching_lines = filter_lines_by_keyword(lines, keyword)
            
            # Add matching lines to collection
            all_matching_lines.extend(matching_lines)
            
        except Exception as e:
            raise Exception(f"Error processing file {file_path}: {str(e)}")
    
    # Final progress update
    if progress_callback:
        progress_callback(100, "Writing results to file...")
    
    # Write results to output file
    if all_matching_lines:
        output_filename = write_result_file(all_matching_lines, keyword)
        return f"Found {len(all_matching_lines)} matching lines. Saved to: {output_filename}"
    else:
        return f"No lines found containing keyword '{keyword}'"

def filter_lines_by_keyword(lines: List[str], keyword: str) -> List[str]:
    """
    Filter lines that contain the given keyword (case-insensitive).
    Preserves original line content exactly.
    
    Args:
        lines: List of lines to filter
        keyword: Keyword to search for
        
    Returns:
        List of lines containing the keyword (original content preserved)
    """
    return [line for line in lines if keyword.lower() in line.lower()] 
