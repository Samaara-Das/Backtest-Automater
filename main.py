import os
from components.settings_reader import SettingsReader
from components.mt4_controller import MT4Controller, StrategyTester
from components.logger import setup_logger
from components.excel_utils import ExcelUtil
from components.reports_processor import process_html_file, titles_and_selectors
from components.browser import ChromeBrowser
from util import remove_log

logger = setup_logger(__name__)

# specify the path to the Excel file
REPORT_DATA_FILE_PATH = "D:\\Backtest Report Data.xlsx"
SETTINGS_EXCEL_PATH = "D:\\Strategy Tester Settings.xlsx"
HTML_REPORTS_PATH = "D:\\Shared folder of HTML Reports"
MT4_EXE_PATH = r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\terminal.exe"
ME_EXE_PATH = r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\metaeditor.exe"

def process_existing_reports(browser, excel_util):
    """
    Processes all existing HTML reports in `HTML_REPORTS_PATH` before running new tests.

    Args:
        browser (ChromeBrowser): An instance of ChromeBrowser used for processing HTML reports.
        excel_util (ExcelUtil): An instance of ExcelUtil used to add data to the Excel file.

    Raises:
        Exception: If an error occurs while processing existing reports.
    """
    try:
        html_files = [f for f in os.listdir(HTML_REPORTS_PATH) if f.endswith('.html') or f.endswith('.htm')]
        for html_file in html_files:
            report_path = os.path.join(HTML_REPORTS_PATH, html_file)
            process_html_file(report_path, browser, excel_util.add_data_to_excel)
            logger.info(f"Processed existing report: {html_file}")
    except Exception as e:
        logger.error(f"Exception occurred while processing existing reports: {e}")

def main(stop_event, reports_data_excel_path, settings_excel_path, html_reports_path, mt4_exe_path, me_exe_path):
    """
    Main function to run the backtesting automation process.

    It processes existing HTML reports, reads settings from an Excel file,
    configures and runs the strategy tester based on the settings, and saves 
    generated reports as HTML files. After saving, it processes the reports.

    Args:
        stop_event (threading.Event): Event to stop the execution of the function.

    Raises:
        Exception: If an error occurs during the backtesting automation process.
    """
    try:
        remove_log()  # Remove the log file

        browser = ChromeBrowser(keep_open=False, headless=True)  # Set headless to True
        excel_util = ExcelUtil(reports_data_excel_path)

        # Make sure that the Backtest Report Data file exists with the correct headers
        excel_util.setup_excel_file(titles_and_selectors)

        # Process existing reports
        process_existing_reports(browser, excel_util)

        mt4 = MT4Controller(mt4_exe_path, me_exe_path, html_reports_path)
        settings_reader = SettingsReader(settings_excel_path)
        strategy_tester = StrategyTester(mt4)

        settings_list = settings_reader.read_settings()  # Read settings from the Excel file
        count = mt4.greatest_count(reports_data_excel_path)  # Get the current greatest HTML report file number

        for settings in settings_list:
            if stop_event.is_set():
                logger.info("Stopping execution...")
                break
            
            try:
                if settings['Expert'] is None:
                    logger.info("Skipping row with missing 'Expert' value.")
                    continue

                if not strategy_tester.configure_tester(settings):
                    logger.error(f"Failed to configure the strategy tester for settings: {settings}. Continuing.")
                    continue

                if not strategy_tester.run_test():
                    logger.error(f"Failed to run the test for settings: {settings}. Continuing.")
                    continue
                
                count += 1  # Increase the file number count so that the next file that gets saved will be unique

                if not strategy_tester.download_report(settings['Expert'], count):
                    logger.error(f"Failed to save the report for settings: {settings}. Continuing.")
                    continue

                # Process the newly downloaded HTML report
                report_path = os.path.join(reports_data_excel_path, f"{mt4.ea_base_name(settings['Expert'])}{count}.html")
                process_html_file(report_path, browser, excel_util.add_data_to_excel)
            except Exception as e:
                logger.error(f"Exception occurred while configuring the Strategy Tester: {e}")
                logger.info('Continuing...')
                continue
    except Exception as e:
        logger.error(f"Exception occurred: {e}")

