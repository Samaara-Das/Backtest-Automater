import sys
from io import StringIO

def log_control_identifiers(tradeview, output_file_path):
    """
    Logs the control identifiers of the tradeview object to the specified output file.

    :param tradeview: The object whose control identifiers need to be printed.
    :param output_file_path: The path of the file where the output should be logged.
    """
    original_stdout = sys.stdout  # Save the current standard output
    
    try:
        sys.stdout = StringIO()  # Redirect standard output to a StringIO object
        tradeview.print_control_identifiers()  # Print control identifiers
        output = sys.stdout.getvalue()  # Get the output from the StringIO object
        
        with open(output_file_path, 'w') as f:  # Write the output to the file
            f.write(output)
    
    finally:
        sys.stdout = original_stdout  # Restore the original standard output