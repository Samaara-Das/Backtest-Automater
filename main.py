from components.settings_reader import SettingsReader
from components.mt4_controller import MT4Controller, StrategyTester, SHARED_FOLDER_PATH
from components.logger import setup_logger
from backtest_reports_processor import process_html_file
from browser import ChromeBrowser
from util import remove_log
import os

logger = setup_logger(__name__)

EXCEL_PATH = "D:\\Strategy Tester Settings.xlsx"
HTML_REPORTS_PATH = "D:\\Shared folder of HTML Reports"
BROWSER = ChromeBrowser(keep_open=False, headless=True)  # Set headless to True

def process_existing_reports():
    """
    Processes all existing HTML reports in the shared folder before running new tests.
    """
    try:
        html_files = [f for f in os.listdir(HTML_REPORTS_PATH) if f.endswith('.html') or f.endswith('.htm')]
        for html_file in html_files:
            report_path = os.path.join(HTML_REPORTS_PATH, html_file)
            process_html_file(report_path, BROWSER)
            logger.info(f"Processed existing report: {html_file}")
    except Exception as e:
        logger.error(f"Exception occurred while processing existing reports: {e}")

def main():
    """
    Main function to run the backtesting automation process.

    It processes existing HTML reports, reads settings from an Excel file,
    configures and runs the strategy tester based on the settings, and saves 
    generated reports as HTML files. After saving, it processes the reports.
    """
    try:
        # Process existing reports
        process_existing_reports()

        mt4 = MT4Controller()
        settings_reader = SettingsReader(EXCEL_PATH)
        strategy_tester = StrategyTester(mt4)

        settings_list = settings_reader.read_settings()  # Read settings from the Excel file
        count = mt4.greatest_count(HTML_REPORTS_PATH)  # Get the current greatest HTML report file number

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

                # Process the HTML report
                report_path = os.path.join(HTML_REPORTS_PATH, f"{mt4.ea_base_name(settings['Expert'])}{count}.html")
                process_html_file(report_path, BROWSER)
            except Exception as e:
                logger.error(f"Exception occurred while configuring the Strategy Tester: {e}")
                logger.info('Continuing...')
                continue
    except Exception as e:
        logger.error(f"Exception occurred: {e}")

if __name__ == "__main__":
    remove_log()
    main()

