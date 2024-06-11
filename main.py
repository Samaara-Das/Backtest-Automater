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
    - browser (ChromeBrowser): The browser instance to use.
    - excel_util (ExcelUtil): The ExcelUtil instance to use.
    """
    try:
        html_files = [f for f in os.listdir(HTML_REPORTS_PATH) if f.endswith('.html') or f.endswith('.htm')]
        for html_file in html_files:
            report_path = os.path.join(HTML_REPORTS_PATH, html_file)
            process_html_file(report_path, browser, excel_util.add_data_to_excel)
            logger.info(f"Processed existing report: {html_file}")
    except Exception as e:
        logger.error(f"Exception occurred while processing existing reports: {e}")

def main(settings_excel_path: str, html_reports_path: str, mt4_exe_path: str, me_exe_path: str):
    """
    Main function to run the backtesting automation process.

    It processes existing HTML reports, reads settings from an Excel file,
    configures and runs the strategy tester based on the settings, and saves 
    generated reports as HTML files. After saving, it processes the reports.

    Args:
    - settings_excel_path (str): Path to the Excel file containing the strategy tester settings.
    - html_reports_path (str): Path to the directory containing the HTML reports.
    - mt4_exe_path (str): Path to the MT4 exe file.
    - me_exe_path (str): Path to the MetaEditor exe file.
    """
    try:
        browser = ChromeBrowser(keep_open=False, headless=True)  # Set headless to True
        excel_util = ExcelUtil(REPORT_DATA_FILE_PATH)

        # Make sure that the Backtest Report Data file exists with the correct headers
        excel_util.setup_excel_file(titles_and_selectors)

        # Process existing reports
        process_existing_reports(browser, excel_util)

        mt4 = MT4Controller(mt4_exe_path, me_exe_path, html_reports_path)
        settings_reader = SettingsReader(settings_excel_path)
        strategy_tester = StrategyTester(mt4)

        settings_list = settings_reader.read_settings()  # Read settings from the Excel file
        count = mt4.greatest_count(html_reports_path)  # Get the current greatest HTML report file number

        for settings in settings_list:
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
                report_path = os.path.join(html_reports_path, f"{mt4.ea_base_name(settings['Expert'])}{count}.html")
                process_html_file(report_path, browser, excel_util.add_data_to_excel)
            except Exception as e:
                logger.error(f"Exception occurred while configuring the Strategy Tester: {e}")
                logger.info('Continuing...')
                continue
    except Exception as e:
        logger.error(f"Exception occurred: {e}")

if __name__ == "__main__":
    remove_log()
    main()
