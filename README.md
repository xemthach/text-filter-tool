# Text Filter Tool

A clean, simple Python GUI tool for filtering text files by keyword with multithreading support.

## Features

- **File/Folder Selection**: Choose a single `.txt` file or a folder containing multiple `.txt` files
- **Keyword Filtering**: Find all lines containing a specific keyword (case-insensitive)
- **Background Processing**: Multithreaded processing that never freezes the GUI
- **Auto-encoding Detection**: Handles UTF-8, UTF-16, cp1252, and other encodings
- **Exact Line Preservation**: Outputs complete lines without modification
- **Dated Output Files**: Creates files with format `result_ddMMyyyy@keyword.txt`

## Project Structure

```
text_filter_tool/
├── main.py              # GUI interface (Tkinter)
├── core/
│   └── engine.py        # Core filtering logic
├── utils/
│   ├── file_loader.py   # File reading with encoding detection
│   └── file_writer.py   # Result file export and logging
├── output/              # Generated result files
└── README.md
```

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Select input:**
   - Click "Choose File" for a single file
   - Click "Choose Folder" for multiple files

3. **Enter keyword:**
   - Type your search term (e.g., `@icloud.com`)

4. **Start filtering:**
   - Click "Start Filtering"
   - Processing runs in background
   - GUI remains responsive

5. **Check results:**
   - Output file: `output/result_21072025@icloud.com.txt`
   - Logs: `logs.txt`

## Output Format

- **Filename**: `result_{ddMMyyyy}@{keyword}.txt`
- **Content**: Complete original lines containing the keyword
- **Location**: `output/` folder (auto-created)

## Example

**Input file:**
```
user1@icloud.com:password123
admin@gmail.com:adminpass
support@icloud.com:helpdesk
```

**Keyword:** `icloud.com`

**Output file:** `result_21072025@icloud.com.txt`
```
user1@icloud.com:password123
support@icloud.com:helpdesk
```

## Requirements

- Python 3.7+
- Tkinter (usually included with Python)
- No external dependencies

## Technical Details

- **Multithreading**: Uses `threading.Thread` for background processing
- **Encoding Detection**: Tries UTF-8, UTF-16, cp1252, latin-1, iso-8859-1
- **Error Handling**: Comprehensive error catching and GUI feedback
- **Logging**: All operations logged to `logs.txt` with timestamps 
