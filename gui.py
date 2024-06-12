import tkinter as tk
from tkinter import messagebox, filedialog
from os import listdir, path
from main import main as run_main, HTML_REPORTS_PATH
from datetime import datetime
import threading

# Global variable to signal the stopping of the thread
stop_event = threading.Event()

def get_html_report_count():
    """
    Returns the number of HTML reports in `HTML_REPORTS_PATH`.

    Returns:
        int: The number of HTML report files.
    """
    return len([f for f in listdir(HTML_REPORTS_PATH) if f.endswith('.html') or f.endswith('.htm')])

def select_excel_file(entry):
    """
    Opens a file dialog to select an Excel file and updates `entry` with the selected file path.

    Args:
        entry (tk.Entry): The entry widget to update with the selected file path.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def select_exe_file(entry):
    """
    Opens a file dialog to select an executable file and updates `entry` with the selected file path.

    Args:
        entry (tk.Entry): The entry widget to update with the selected file path.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def run_main_thread():
    """
    Runs the main function in a separate thread and updates the GUI with the completion status.

    Raises:
        Exception: If an error occurs during the execution of the main function.
    """
    global stop_event, finished_label, html_report_label
    
    try:
        # Run main function from main.py, passing the stop_event
        run_main(stop_event)
        
        if not stop_event.is_set():
            # Show "Finished at [time of completion]" message
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            finished_label.config(text=f"Finished at {completion_time}")
            finished_label.grid(row=7, columnspan=2, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        # Update HTML report count
        post_execution_report_count = get_html_report_count()
        html_report_label.config(text=f'Total HTML Reports currently in "{path.basename(HTML_REPORTS_PATH)}": {post_execution_report_count}')

def start_app():
    """
    Starts the application by resetting the stop_event, clearing the finished_label, and starting the main function in a new thread.
    """
    global stop_event
    stop_event.clear()  # Reset the stop event before starting the thread
    finished_label.grid_forget()
    
    # Update constants with user inputs
    SETTINGS_EXCEL_PATH = settings_path_entry.get()
    MT4_EXE_PATH = mt4_exe_path_entry.get()
    ME_EXE_PATH = me_exe_path_entry.get()
    
    # Start the main function in a new thread
    threading.Thread(target=run_main_thread).start()

def stop_app():
    """
    Stops the application by setting the stop_event and updating the finished_label and html_report_label.
    """
    global stop_event, finished_label, html_report_label
    stop_event.set()  # Signal the thread to stop
    
    # Update the finished label
    finished_label.config(text="Execution halted by user.")
    finished_label.grid(row=7, columnspan=2, pady=10)
    
    # Update HTML report count
    post_execution_report_count = get_html_report_count()
    html_report_label.config(text=f'Total HTML Reports currently in "{path.basename(HTML_REPORTS_PATH)}": {post_execution_report_count}')

# Create the main window
root = tk.Tk()
root.title("Backtest Automater")

# Input field and label to select the Settings Excel file
tk.Label(root, text="Settings Excel Path:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
settings_path_entry = tk.Entry(root, width=50)
settings_path_entry.grid(row=1, column=1, padx=10, pady=5)
settings_path_entry.insert(0, "D:\\Strategy Tester Settings.xlsx")
tk.Button(root, text="Browse", command=lambda: select_excel_file(settings_path_entry)).grid(row=1, column=2, padx=5)

# Input field and label to select the MT4 exe path
tk.Label(root, text="MT4 EXE Path:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
mt4_exe_path_entry = tk.Entry(root, width=50)
mt4_exe_path_entry.grid(row=3, column=1, padx=10, pady=5)
mt4_exe_path_entry.insert(0, r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\terminal.exe")
tk.Button(root, text="Browse", command=lambda: select_exe_file(mt4_exe_path_entry)).grid(row=3, column=2, padx=5)

# Input field and label to select the MetaEditor exe path
tk.Label(root, text="MetaEditor EXE Path:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
me_exe_path_entry = tk.Entry(root, width=50)
me_exe_path_entry.grid(row=4, column=1, padx=10, pady=5)
me_exe_path_entry.insert(0, r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\metaeditor.exe")
tk.Button(root, text="Browse", command=lambda: select_exe_file(me_exe_path_entry)).grid(row=4, column=2, padx=5)

# Add a label to show the total number of HTML reports
html_report_count = get_html_report_count()
html_report_label = tk.Label(root, text=f'Total HTML Reports currently in "{path.basename(HTML_REPORTS_PATH)}": {html_report_count}')
html_report_label.grid(row=5, columnspan=3, padx=10, pady=5)

# Add a Start button
start_button = tk.Button(root, text="Start", command=start_app)
start_button.grid(row=6, column=0, pady=10)

# Add a Stop button
stop_button = tk.Button(root, text="Stop", command=stop_app)
stop_button.grid(row=6, column=1, pady=10)

# Add a label to display the completion message
finished_label = tk.Label(root, text="", font=("Arial", 16))

# Start the main event loop
root.mainloop()