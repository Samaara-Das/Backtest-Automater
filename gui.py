import tkinter as tk
from tkinter import messagebox, filedialog
from re import sub
from os import listdir, path as os_path
from main import main as run_main
from datetime import datetime
import threading

# Global variable to signal the stopping of the thread
stop_event = threading.Event()

def clean_path(input_path: str):
    """Strip whitespaces and remove single/double quotes."""
    return sub(r'[\'"]', '', input_path.strip())

def get_html_report_count():
    """
    Returns the number of HTML reports in the selected folder in the GUI. In the case of an exception, `None` is returned.

    Returns:
        int: The number of HTML report files.
    """
    try:
        reports_folder = clean_path(reports_folder_path_entry.get())
        return len([f for f in listdir(reports_folder) if f.endswith('.html') or f.endswith('.htm')])
    except Exception as e:
        return None

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

def run_main_thread(report_data_excel_path, settings_excel_path, html_reports_path, mt4_exe_path, me_exe_path):
    """
    Runs the main function in a separate thread and updates the GUI with the completion status.

    Raises:
        Exception: If an error occurs during the execution of the main function.
    """
    global stop_event, finished_label, html_report_label
    
    try:
        # Run main function from main.py
        run_main(stop_event, report_data_excel_path, settings_excel_path, html_reports_path, mt4_exe_path, me_exe_path)
        
        if not stop_event.is_set():
            # Show "Finished at [time of completion]" message
            completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            finished_label.config(text=f"Finished at {completion_time}")
            finished_label.grid(row=8, columnspan=2, pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        # Update HTML report count
        post_execution_report_count = get_html_report_count()
        reports_folder = clean_path(reports_folder_path_entry.get())
        html_report_label.config(text=f'Total HTML Reports currently in "{os_path.basename(reports_folder)}": {post_execution_report_count}')

def start_app():
    global stop_event
    stop_event.clear()
    finished_label.grid_forget()
    
    # Fetch path values from entries, clean them
    html_reports_path = clean_path(reports_folder_path_entry.get())
    settings_excel_path = clean_path(settings_path_entry.get())
    report_data_excel_path = clean_path(backtest_data_path_entry.get())
    mt4_exe_path = clean_path(mt4_exe_path_entry.get())
    me_exe_path = clean_path(me_exe_path_entry.get())

    # List of paths to check along with their associated entries for user feedback
    paths_to_check = [
        (html_reports_path, reports_folder_path_label),
        (settings_excel_path, settings_path_label),
        (report_data_excel_path, backtest_data_path_label),
        (mt4_exe_path, mt4_exe_path_label),
        (me_exe_path, me_exe_path_label)
    ]

    # Check if any path is blank or does not exist
    for path, name in paths_to_check:
        if not path:
            messagebox.showerror("Error", f"{name} is required but not provided.")
            return
        if not os_path.exists(path):
            messagebox.showerror("Failure Error", f"The specified path for {name} does not exist")
            return

    # Start the main function in a new thread with user inputs
    threading.Thread(target=run_main_thread, args=(report_data_excel_path, settings_excel_path, html_reports_path, mt4_exe_path, me_exe_path)).start()

def stop_app():
    """
    Stops the application by setting the stop_event and updating the finished_label and html_report_label.
    """
    global stop_event, finished_label, html_report_label
    stop_event.set()  # Signal the thread to stop
    
    # Update the finished label
    finished_label.config(text="Execution stopped by user.")
    finished_label.grid(row=8, columnspan=2, pady=10)
    
    # Update HTML report count
    post_execution_report_count = get_html_report_count()
    reports_folder = clean_path(reports_folder_path_entry.get())
    html_report_label.config(text=f'Total HTML Reports currently in "{os_path.basename(reports_folder)}": {post_execution_report_count}')

# Create the main window
root = tk.Tk()
root.title("Backtest Automater")

# Input field and label to type the path of the html reports folder
reports_folder_path_label = "HTML Reports folder"
tk.Label(root, text=reports_folder_path_label).grid(row=1, column=0, padx=10, pady=5, sticky="e")
reports_folder_path_entry = tk.Entry(root, width=50)
reports_folder_path_entry.grid(row=1, column=1, padx=10, pady=5)
# reports_folder_path_entry.insert(0, r"D:\Shared folder of HTML Reports")

# Input field and label to select the Settings Excel file
settings_path_label = "Settings file"
tk.Label(root, text=settings_path_label).grid(row=2, column=0, padx=10, pady=5, sticky="e")
settings_path_entry = tk.Entry(root, width=50)
settings_path_entry.grid(row=2, column=1, padx=10, pady=5)
settings_path_entry.insert(0, "D:\\Strategy Tester Settings.xlsx")
tk.Button(root, text="Browse", command=lambda: select_excel_file(settings_path_entry)).grid(row=2, column=2, padx=5)

# Input field and label to select the Back test data Excel file
backtest_data_path_label = "Back Test Data file"
tk.Label(root, text=backtest_data_path_label).grid(row=3, column=0, padx=10, pady=5, sticky="e")
backtest_data_path_entry = tk.Entry(root, width=50)
backtest_data_path_entry.grid(row=3, column=1, padx=10, pady=5)
backtest_data_path_entry.insert(0, "D:\\Backtest Report Data.xlsx")
tk.Button(root, text="Browse", command=lambda: select_excel_file(backtest_data_path_entry)).grid(row=3, column=2, padx=5)

# Input field and label to select the MT4 exe path
mt4_exe_path_label = "MT4 exe"
tk.Label(root, text=mt4_exe_path_label).grid(row=4, column=0, padx=10, pady=5, sticky="e")
mt4_exe_path_entry = tk.Entry(root, width=50)
mt4_exe_path_entry.grid(row=4, column=1, padx=10, pady=5)
mt4_exe_path_entry.insert(0, r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\terminal.exe")
tk.Button(root, text="Browse", command=lambda: select_exe_file(mt4_exe_path_entry)).grid(row=4, column=2, padx=5)

# Input field and label to select the MetaEditor exe path
me_exe_path_label = "MetaEditor exe"
tk.Label(root, text=me_exe_path_label).grid(row=5, column=0, padx=10, pady=5, sticky="e")
me_exe_path_entry = tk.Entry(root, width=50)
me_exe_path_entry.grid(row=5, column=1, padx=10, pady=5)
me_exe_path_entry.insert(0, r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\metaeditor.exe")
tk.Button(root, text="Browse", command=lambda: select_exe_file(me_exe_path_entry)).grid(row=5, column=2, padx=5)

# Add a label to show the total number of HTML reports
html_report_count = get_html_report_count()
html_report_label = tk.Label(root, text=f'Total reports currently in HTML Reports Folder: {html_report_count}')
html_report_label.grid(row=6, columnspan=3, padx=10, pady=5)

# Add a Start button
start_button = tk.Button(root, text="Start", command=start_app)
start_button.grid(row=7, column=0, pady=10)

# Add a Stop button
stop_button = tk.Button(root, text="Stop", command=stop_app)
stop_button.grid(row=7, column=1, pady=10)

# Add a label to display the completion message
finished_label = tk.Label(root, text="", font=("Arial", 16))

# Start the main event loop
root.mainloop()