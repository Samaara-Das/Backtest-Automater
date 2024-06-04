from components.settings_reader import SettingsReader
from components.mt4_controller import MT4Controller, StrategyTester
from components.logger import setup_logger

logger = setup_logger(__name__)

EXCEL_PATH = "D:\\Strategy Tester Settings.xlsx"

def main():
    try:
        mt4 = MT4Controller()
        settings_reader = SettingsReader(EXCEL_PATH)
        strategy_tester = StrategyTester(mt4)

        settings_list = settings_reader.read_settings()
        app = mt4.access_application(mt4.mt4_exe_path, mt4.timeout)

        for settings in settings_list:
            try:
                if settings['Expert'] is None:
                    logger.info("Skipping row with missing 'Expert' value.")
                    continue

                if not strategy_tester.configure_tester(app, settings):
                    logger.error(f"Failed to configure the strategy tester for settings: {settings}. Continuing.")
                    continue

                if not strategy_tester.run_test():
                    logger.error(f"Failed to run the test for settings: {settings}. Continuing.")

            except Exception as e:
                logger.error(f"Exception occurred while configuring the Strategy Tester: {e}")
                logger.info('Continuing...')
                continue
    except Exception as e:
        logger.error(f"Exception occurred: {e}")

if __name__ == "__main__":
    main()

