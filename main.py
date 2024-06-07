from components.settings_reader import SettingsReader
from components.mt4_controller import MT4Controller, StrategyTester, SHARED_FOLDER_PATH
from components.logger import setup_logger

logger = setup_logger(__name__)

EXCEL_PATH = "D:\\Strategy Tester Settings.xlsx"

def main():
    """
    Main function to run the backtesting automation process.

    It reads settings from an Excel file, configures and runs the strategy tester based on the settings 
    and saves generated reports as HTML files.
    """
    try:
        mt4 = MT4Controller()
        settings_reader = SettingsReader(EXCEL_PATH)
        strategy_tester = StrategyTester(mt4)

        settings_list = settings_reader.read_settings()  # Read settings from the Excel file
        count = mt4.greatest_count(SHARED_FOLDER_PATH)  # Get the current greatest HTML report file number
      
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

                if not strategy_tester.download_report(settings['Expert'], count):
                    logger.error(f"Failed to save the report for settings: {settings}. Continuing.")
                    continue

                count += 1  # Increase the file number count so that the next file that gets saved will be unique
            except Exception as e:
                logger.error(f"Exception occurred while configuring the Strategy Tester: {e}")
                logger.info('Continuing...')
                continue
    except Exception as e:
        logger.error(f"Exception occurred: {e}")

if __name__ == "__main__":
    main()
