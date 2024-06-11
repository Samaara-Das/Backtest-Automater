import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from main import main as run_main

# Function to count HTML files in the selected source folder
def count_html_files(source_folder):
    try:
        return len([f for f in os.listdir(source_folder) if f.endswith(".htm") or f.endswith(".html")])
    except Exception as e:
        return 0

# Function to handle Run button click
def run_script():
    global settings_excel_path, html_reports_path, mt4_exe_path, me_exe_path, stop_event

    if not html_reports_path or not os.path.exists(html_reports_path):
        messagebox.showerror("Error", "Please choose a valid HTML Reports Path.")
        return

    if not settings_excel_path or not os.path.exists(settings_excel_path):
        messagebox.showerror("Error", "Please choose a valid Settings Excel Path.")
        return

    if not mt4_exe_path or not os.path.exists(mt4_exe_path):
        messagebox.showerror("Error", "Please choose a valid MT4 EXE Path.")
        return

    if not me_exe_path or not os.path.exists(me_exe_path):
        messagebox.showerror("Error", "Please choose a valid MetaEditor EXE Path.")
        return

    # Clear the stop event before running the script
    stop_event.clear()

    # Run the main script in a separate thread to avoid freezing the UI
    threading.Thread(target=run_main, args=(settings_excel_path, html_reports_path, mt4_exe_path, me_exe_path)).start()

# Function to handle Stop button click
def stop_script():
    global stop_event
    stop_event.set()
    messagebox.showinfo("Info", "Script execution stopped.")

# Function to select HTML Reports Path
def select_html_reports_path():
    global html_reports_path, html_file_count_label
    html_reports_path = filedialog.askdirectory()
    html_file_count = count_html_files(html_reports_path)
    html_file_count_label.config(text=f"Total HTML Reports currently: {html_file_count}")

# Function to select Settings Excel Path
def select_settings_excel_path():
    global settings_excel_path
    settings_excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])

# Function to select MT4 EXE Path
def select_mt4_exe_path():
    global mt4_exe_path
    mt4_exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe"), ("All files", "*.*")])

# Function to select MetaEditor EXE Path
def select_me_exe_path():
    global me_exe_path
    me_exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe"), ("All files", "*.*")])

# Initialize the main window
root = tk.Tk()
root.title("Backtest Automater")

html_reports_path = ""
settings_excel_path = ""
mt4_exe_path = ""
me_exe_path = ""
stop_event = threading.Event()

# Create and place labels, entry fields, and buttons
settings_excel_path_entry = tk.Button(root, text="Settings Excel File Path", command=select_settings_excel_path)
settings_excel_path_entry.pack(pady=10)

html_reports_path_entry = tk.Button(root, text="HTML Reports Path:", command=select_html_reports_path)
html_reports_path_entry.pack(pady=10)

html_file_count_label = tk.Label(root, text="Total HTML Reports currently: 0")
html_file_count_label.pack(pady=5)

mt4_exe_path_entry = tk.Button(root, text="MT4 EXE Path:", command=select_mt4_exe_path)
mt4_exe_path_entry.pack(pady=10)

me_exe_path_entry = tk.Button(root, text="MetaEditor EXE Path:", command=select_me_exe_path)
me_exe_path_entry.pack(pady=10)

# Add Run and Stop buttons
run_button = tk.Button(root, text="Run", command=run_script)
run_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_script)
stop_button.pack(pady=10)

# Start the main event loop
root.mainloop()
