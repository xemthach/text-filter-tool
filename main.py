import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from typing import Optional, List

class TextFilterGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Text Filter Tool - v.0.1 - atolgo.com')
        self.root.geometry('500x350')
        
        # Variables
        self.file_path: Optional[str] = None
        self.folder_path: Optional[str] = None
        self.keyword_var = tk.StringVar()
        self.cancellation_flag = False
        
        self._build_gui()
    
    def _build_gui(self):
        # File/Folder selection
        file_frame = ttk.LabelFrame(self.root, text='Select File or Folder')
        file_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(file_frame, text='Choose File', command=self._choose_file).pack(side='left', padx=5, pady=5)
        ttk.Button(file_frame, text='Choose Folder', command=self._choose_folder).pack(side='left', padx=5, pady=5)
        
        self.path_label = ttk.Label(file_frame, text='No file or folder selected')
        self.path_label.pack(side='left', padx=10)
        
        # Keyword input
        keyword_frame = ttk.LabelFrame(self.root, text='Keyword')
        keyword_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(keyword_frame, text='Enter keyword:').pack(side='left', padx=5)
        ttk.Entry(keyword_frame, textvariable=self.keyword_var, width=30).pack(side='left', padx=5, fill='x', expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill='x', padx=10, pady=10)
        
        self.start_btn = ttk.Button(action_frame, text='Start Filtering', command=self._start_filtering)
        self.start_btn.pack(side='left', padx=(0, 5))
        
        self.stop_btn = ttk.Button(action_frame, text='Stop', command=self._stop_filtering, state='disabled')
        self.stop_btn.pack(side='left')
        
        # Status
        self.status_label = ttk.Label(action_frame, text='Ready')
        self.status_label.pack(side='left', padx=10)
        
        # Progress bar
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.pack(fill='x')
        
        self.progress_label = ttk.Label(progress_frame, text='')
        self.progress_label.pack()
    
    def _choose_file(self):
        path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if path:
            self.file_path = path
            self.folder_path = None
            self.path_label.config(text=f'File: {path}')
    
    def _choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            self.file_path = None
            self.path_label.config(text=f'Folder: {path}')
    
    def _start_filtering(self):
        # Validate inputs
        if not self.file_path and not self.folder_path:
            messagebox.showerror('Error', 'Please select a file or folder')
            return
        
        keyword = self.keyword_var.get().strip()
        if not keyword:
            messagebox.showerror('Error', 'Please enter a keyword')
            return
        
        # Get file paths
        file_paths = self._get_file_paths()
        if not file_paths:
            messagebox.showerror('Error', 'No .txt files found')
            return
        
        # Reset cancellation flag and start processing
        self.cancellation_flag = False
        self.status_label.config(text='Processing...')
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress_bar['value'] = 0
        self.progress_label.config(text='Initializing...')
        
        thread = threading.Thread(
            target=self._process_files,
            args=(file_paths, keyword),
            daemon=True
        )
        thread.start()

    def _stop_filtering(self):
        """Stop the filtering process"""
        self.cancellation_flag = True
        self.status_label.config(text='Stopping...')
        self.stop_btn.config(state='disabled')
        self.progress_label.config(text='Cancelling...')
    
    def _get_file_paths(self) -> List[str]:
        import os
        file_paths = []
        
        if self.file_path:
            file_paths = [self.file_path]
        elif self.folder_path:
            for filename in os.listdir(self.folder_path):
                if filename.endswith('.txt'):
                    file_paths.append(os.path.join(self.folder_path, filename))
        
        return file_paths
    
    def _process_files(self, file_paths: List[str], keyword: str):
        try:
            from core.engine import process_files
            result = process_files(
                file_paths, 
                keyword, 
                progress_callback=self._update_progress,
                cancellation_check=lambda: self.cancellation_flag
            )
            
            # Update GUI from main thread
            if self.cancellation_flag:
                self.root.after(0, self._on_cancelled)
            else:
                self.root.after(0, lambda: self._on_complete(result))
            
        except Exception as e:
            error_msg = f'Error: {str(e)}'
            self.root.after(0, lambda: self._on_error(error_msg))

    def _update_progress(self, value: int, text: str):
        """Update progress bar and label from worker thread"""
        self.root.after(0, lambda: self._update_progress_safe(value, text))
    
    def _update_progress_safe(self, value: int, text: str):
        """Update progress bar and label (called from main thread)"""
        self.progress_bar['value'] = value
        self.progress_label.config(text=text)
    
    def _on_complete(self, result: str):
        self.status_label.config(text='Complete!')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress_bar['value'] = 100
        self.progress_label.config(text='Processing completed!')
        messagebox.showinfo('Success', f'Filtering completed!\n{result}')

    def _on_cancelled(self):
        self.status_label.config(text='Cancelled!')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress_bar['value'] = 0
        self.progress_label.config(text='')
        messagebox.showinfo('Cancelled', 'Filtering was cancelled.')
    
    def _on_error(self, error_msg: str):
        self.status_label.config(text='Error!')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress_bar['value'] = 0
        self.progress_label.config(text='')
        messagebox.showerror('Error', error_msg)


def main():
    root = tk.Tk()
    app = TextFilterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main() 
