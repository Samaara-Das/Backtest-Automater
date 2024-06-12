import tkinter as tk
from tkinter import messagebox, filedialog
from os import listdir, path
from main import main as run_main, HTML_REPORTS_PATH

def get_html_report_count():
    return len([f for f in listdir(HTML_REPORTS_PATH) if f.endswith('.html') or f.endswith('.htm')])

def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def select_folder(entry):
    folder_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_path)

def start_application():
    try:
        global REPORT_DATA_FILE_PATH, SETTINGS_EXCEL_PATH, MT4_EXE_PATH, ME_EXE_PATH
        
        # Update constants with user inputs
        SETTINGS_EXCEL_PATH = settings_path_entry.get()
        MT4_EXE_PATH = mt4_exe_path_entry.get()
        ME_EXE_PATH = me_exe_path_entry.get()
        
        # Run main function from main.py
        run_main()
        
        # Show "Finished!" message for 3 seconds
        finished_label = tk.Label(root, text="Finished!", font=("Arial", 16))
        finished_label.grid(row=7, columnspan=2, pady=10)
        root.after(3000, finished_label.destroy)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Backtest Automater")

# Create and place labels, entry fields, and buttons for each constant
tk.Label(root, text="Settings Excel Path:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
settings_path_entry = tk.Entry(root, width=50)
settings_path_entry.grid(row=1, column=1, padx=10, pady=5)
settings_path_entry.insert(0, "D:\\Strategy Tester Settings.xlsx")
tk.Button(root, text="Browse", command=lambda: select_file(settings_path_entry)).grid(row=1, column=2, padx=5)

tk.Label(root, text="MT4 EXE Path:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
mt4_exe_path_entry = tk.Entry(root, width=50)
mt4_exe_path_entry.grid(row=3, column=1, padx=10, pady=5)
mt4_exe_path_entry.insert(0, r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\terminal.exe")
tk.Button(root, text="Browse", command=lambda: select_file(mt4_exe_path_entry)).grid(row=3, column=2, padx=5)

tk.Label(root, text="MetaEditor EXE Path:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
me_exe_path_entry = tk.Entry(root, width=50)
me_exe_path_entry.grid(row=4, column=1, padx=10, pady=5)
me_exe_path_entry.insert(0, r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\metaeditor.exe")
tk.Button(root, text="Browse", command=lambda: select_file(me_exe_path_entry)).grid(row=4, column=2, padx=5)

# Add a label to show the total number of HTML reports
html_report_count = get_html_report_count()
tk.Label(root, text=f'Total HTML Reports currently in "{path.basename(HTML_REPORTS_PATH)}": {html_report_count}').grid(row=5, columnspan=3, padx=10, pady=5)

# Add a Start button
start_button = tk.Button(root, text="Start", command=start_application)
start_button.grid(row=6, columnspan=3, pady=10)

# Start the main event loop
root.mainloop()
