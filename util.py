import sys
from components.logger import setup_logger
from io import StringIO

logger = setup_logger(__name__)

def log_control_identifiers(window, output_file_path):
    """
    Logs the control identifiers of the window object to the specified output file.

    Args:
    - window: The object whose control identifiers need to be printed.
    - output_file_path: The path of the file where the output should be logged.
    """
    original_stdout = sys.stdout  # Save the current standard output
    
    try:
        sys.stdout = StringIO()  # Redirect standard output to a StringIO object
        window.print_control_identifiers()  # Print control identifiers
        output = sys.stdout.getvalue()  # Get the output from the StringIO object
        
        with open(output_file_path, 'w') as f:  # Write the output to the file
            f.write(output)
    
    finally:
        sys.stdout = original_stdout  # Restore the original standard output

def clean_log():
    """
    Cleans up 'app_log.log' by removing all its content.
    If 'app_log.log' does not exist, it will be created.
    """
    try:
        with open('app_log.log', 'w') as file:
            pass  # Truncates the file to 0 bytes
        logger.info("Log file 'app_log.log' has been successfully cleaned up.")
    except Exception as e:
        logger.error(f"Failed to clean up the log file 'app_log.log': {e}")
        raise

def keep_log_light():
    """
    To keep the log file lightweight, keep only the last 500 lines.
    """
    try:
        log_file_path = 'app_log.log'
        with open(log_file_path, 'r+') as file:
            lines = file.readlines()
            if len(lines) > 500:
                file.seek(0)  # Go to the start of the file
                file.writelines(lines[-500:])  # Write the last 500 lines
                file.truncate()  # Remove the rest of the content

        logger.info("Log file 'app_log.log' has been truncated to the last 500 lines.")
    except Exception as e:
        logger.error(f"Failed to truncate the log file 'app_log.html': {e}")
        raise