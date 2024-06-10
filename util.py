import sys
from components.logger import setup_logger
from io import StringIO

logger = setup_logger(__name__)

def log_control_identifiers(window, output_file_path):
    """
    Logs the control identifiers of the window object to the specified output file.

    :param window: The object whose control identifiers need to be printed.
    :param output_file_path: The path of the file where the output should be logged.
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

def remove_log():
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