import time
from datetime import datetime
from pywinauto import Application
from pywinauto.keyboard import send_keys
from pywinauto.mouse import click
from pyperclip import copy, paste
import re
import psutil
from os import path
from components.logger import setup_logger
from pywinauto.timings import TimeoutError

logger = setup_logger(__name__)

MT4_EXE_PATH = r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\terminal.exe"
ME_EXE_PATH = r"C:\Program Files (x86)\Tradeview MetaTrader 4 Terminal\metaeditor.exe"
TIMEOUT = 15

class MT4Controller:
    def __init__(self):
        self.logger = logger
        self.mt4_exe_path = MT4_EXE_PATH
        self.me_exe_path = ME_EXE_PATH
        self.timeout = TIMEOUT
        self.SETTINGS_TAB = {'name': 'Settings', 'coords': (45, 992)}
        self.REPORT_TAB = {'name': 'Report', 'coords': (214, 992)}

    def configure_expert_properties(self, ea_name, properties_string):
        """
        Configures the expert properties in the MetaTrader 4 Strategy Tester.

        Args:
            ea_name (str): The name of the expert advisor.
            properties_string (str): The properties to be configured in the format 'name=value, name=value,...'.
        """
        try:
            if properties_string is None or properties_string.strip() == '':
                self.logger.info("No properties to set. Exiting.")
                return True

            self.strategy_tester.child_window(title="Modify expert", class_name="Button").click_input()
            self.logger.info("Clicked on 'Modify expert' button")

            app = self.access_application(self.me_exe_path, self.timeout)
            editor = self.wait_for_window(app, title_re=".*MetaEditor.*", timeout=self.timeout)
            editor.set_focus()
            editor.maximize()

            file = editor.child_window(best_match=self.ea_base_name(ea_name) + ".mq4")
            file.set_focus()
            file.maximize()
            send_keys('^a^c')

            original_code = paste()
            modified_code = original_code

            for prop in properties_string.split(','):
                name, value = prop.split('=')
                name, value = name.strip(), value.strip()
                changed_code = self.change_input_value(modified_code, name, value)
                if changed_code:
                    modified_code = changed_code
                    self.logger.info(f"Setting property '{name}' to '{value}'")
                else:
                    self.logger.info(f"Value of property '{name}' failed to be modified. Skipping.")

            copy(modified_code)
            send_keys('^v')
            send_keys('{F7}')
            time.sleep(1.3)
            send_keys('^{F4}')
            send_keys('%{F4}')
            self.logger.info("Confirmed the changes and closed the Expert properties window")
            return True
        except Exception as e:
            self.logger.error(f"An error occurred while configuring expert properties: {e}")
            return False

    def replace_value(self, original_text, new_value):
        """
        Replaces the value between '=' and ';' in `original_text` with `new_value`.

        Args:
            original_text (str): The original string containing the value to be replaced.
            new_value (str): The new value to insert between '=' and ';'.

        Returns:
            str: The modified string with the replaced value.
        """
        try:
            start_index = original_text.find('=') + 1
            end_index = original_text.find(';')
            
            if start_index == 0 or end_index == -1:
                raise ValueError("The input string does not contain '=' and/or ';'")
            
            modified_string = original_text[:start_index] + new_value + original_text[end_index:]
            logger.info("Successfully replaced the value in the string.")
            
            return modified_string
        except Exception as e:
            logger.error(f"An error occurred in replace_value: {e}")
            return None

    def change_input_value(self, text, prop, value):
        """
        Finds and replaces the value of a specific property in the given text.

        Args:
            text (str): The text to look for the property.
            prop (str): The property name to search for.
            value (str): The new value to replace the old value.

        Returns:
            str: The modified text with the replaced value, or None if the property is not found.
        """
        try:
            pattern = rf'^(input.*?;\s*//\s*{re.escape(prop)}\s*)$'
            line = re.findall(pattern, text, re.MULTILINE)
            
            if not line:
                logger.warning(f"Property '{prop}' not found in the text.")
                return None
            
            repl_val = self.replace_value(line[0], value) 
            if repl_val is None:
                return None
            result = re.sub(pattern, repl_val, text, flags=re.MULTILINE)
            logger.info(f"Successfully replaced the value for property '{prop}'.")
            
            return result
        except Exception as e:
            logger.error(f"An error occurred in change_input_value: {e}")
            return None

    def ea_base_name(self, ea_name):
        """
            Extracts the base name of an expert advisor from its full path.

            Args:
                ea_name (str): The full path of the expert advisor.

            Returns:
                str: The base name of the expert advisor.
        """
        try:
            name_without_ex4 = re.sub(r'\.ex4$', '', ea_name) # Remove ".ex4" extension
            name_without_slash = re.sub(r'.*\\', '', name_without_ex4) # Extract the part after the last slash (if any)
            return name_without_slash
        except Exception as e:
            logger.error(f"Error converting string '{ea_name}': {e}")
            return None

    def is_application_running(self, exe_path):
        """
        Checks if an application is already running.

        Args:
            exe_path (str): The path of the application executable.

        Returns:
            int: The process ID (PID) of the running application, or None if not running.
        """
        self.logger.info("Checking if the application is already running.")
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] and path.normpath(proc.info['exe']) == path.normpath(exe_path):
                    self.logger.info(f"Application is already running with PID: {proc.info['pid']}")
                    return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                self.logger.error(f"Exception occurred while checking running processes: {e}")
                return False
        self.logger.info("Application is not running.")
        return None

    def access_application(self, exe_path, timeout):
        """
        Starts the application or connects to it if it's already running.

        Args:
            exe_path (str): The path of the application executable.
            timeout (int): The time to wait for the application to start or connect.

        Returns:
            Application: The connected application object.
        """
        try:
            pid = self.is_application_running(exe_path)

            if pid == False:
                return None
            elif pid:
                logger.info(f"Connecting to the running instance with PID: {pid}.")
                app = Application(backend="win32").connect(process=pid)
            else:
                logger.info(f"Starting the application from path: {exe_path}.")
                app = Application(backend="win32").start(exe_path, timeout=timeout)
            
            return app
        except Exception as e:
            logger.error(f"Exception occurred while accessing the application: {e}")
            return None

    def wait_for_window(self, app, title_re, timeout):
        """
        Waits for a window with the given title to appear.

        Args:
            app (Application): The application object.
            title_re (str): The regular expression to match the window title.
            timeout (int): The time to wait for the window.

        Returns:
            WindowSpecification: The matched window object.
        """
        self.logger.info(f"Waiting for window with title matching: {title_re}.")
        try:
            window = app.window(title_re=title_re)
            window.wait("exists visible", timeout=timeout)
            self.logger.info("Window found and ready.")
            return window
        except Exception as e:
            self.logger.error(f"Exception occurred while waiting for the window: {e}")
            return None

    def is_strategy_tester_open(self, window, timeout):
        """
        Checks if the Strategy Tester is open.

        Args:
            window (WindowSpecification): The main window of the application.
            timeout (int): The time to wait for the Strategy Tester to appear.

        Returns:
            tuple: A tuple containing a boolean indicating if the Strategy Tester is open and the Strategy Tester window object.
        """
        self.logger.info("Checking if the Strategy Tester is open...")
        try:
            self.strategy_tester = window.child_window(title="Tester")
            self.strategy_tester.wait('exists visible', timeout=timeout)
            self.logger.info("Strategy Tester is open.")
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred while checking the Strategy Tester: {e}")
            return False

    def tester_switch_tab(self, tradeview, tab):
        """
        Switches to the specified tab in the Strategy Tester.

        Args:
            tab (str): The name of the tab to switch to. Possible values are only self.SETTINGS_TAB (for the Settings tab) and self.REPORT_TAB (for the Report tab). 

        Returns:
            bool: True if the tab was successfully switched, False otherwise.
        """
        try:
            if not tradeview.is_maximized():
                tradeview.maximize() # MT4 needs to be maximized because the mouse coordinates for the tabs will work only when MT4 is maximized
            click(coords=tab['coords'])
            self.logger.info(f"Successfully switched to tab: {tab['name']}")
            time.sleep(1)
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred while switching to {tab['name']} tab: {e}")
            return False

    def select_expert_advisor(self):
        """
        Ensures that 'Expert Advisor' is selected in the Strategy Tester.
        """
        try:
            self.logger.info("Checking for 'Indicator' combo box...")
            indicator_combo = self.strategy_tester.child_window(title="Indicator", class_name="ComboBox")
            indicator_combo.wait('exists visible', timeout=7)
            self.logger.info("Changing the value of 'Indicator' combo box to 'Expert Advisor'.")
            indicator_combo.select("Expert Advisor")
            self.logger.info("Successfully changed the value to 'Expert Advisor'.")
            return True
        except TimeoutError as e:
            self.logger.error(f"It is likely that Expert Advisor has already been chosen")
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred while selecting Expert Advisor: {e}")
            return False

    def choose_EA(self, ea_name):
        """
        Selects the specified expert advisor (EA) in the Strategy Tester.

        Args:
            ea_name (str): The name of the expert advisor.

        Returns:
            bool: True if the EA was successfully selected, False otherwise.
        """
        try:
            self.logger.info("Searching for the Expert input in the Strategy Tester")
            time.sleep(2) # give the Strategy Tester time to load
            combo_boxes = self.strategy_tester.children(class_name="ComboBox")
            ea_box_found = False

            for combo in combo_boxes:
                title = combo.window_text()
                if "ex4" in title:
                    combo.click_input()
                    ea_box_found = True
                    i = 0
                    prev_option = ''
                    current_option = combo.window_text()

                    self.logger.info(f"Navigating through options to find '{ea_name}'")
                    while i in range(50):
                        if ea_name == current_option: # if the EA is found
                            logger.info(f"Found '{ea_name}' in the options.")
                            return True
                        
                        send_keys('{DOWN}')
                        time.sleep(0.1)
                        prev_option = current_option
                        current_option = combo.window_text()
                        if prev_option == current_option: # if the limit of the EAs has been reached 
                            break

                        i += 1
                    
                    # Use UP key to navigate through the dropdown options
                    i = 0
                    while i in range(50):
                        if ea_name == current_option: # if the EA is found
                            logger.info(f"Found '{ea_name}' in the options.")
                            return True
                        
                        send_keys('{UP}')
                        time.sleep(0.1)
                        prev_option = current_option
                        current_option = combo.window_text()
                        if prev_option == current_option: # if the limit of the EAs has been reached 
                            return False

                        i += 1
            if not ea_box_found:
                self.logger.warning("No combo box with 'ex4' or 'ex5' found.")
                return False
        except Exception as e:
            self.logger.error(f"Exception occurred while selecting the combo box: {e}")
            return False

    def choose_symbol(self, symbol):
        """
        Selects the specified symbol in the Strategy Tester.

        Args:
            symbol (str): The symbol to select.

        Returns:
            bool: True if the symbol was successfully selected, False otherwise.
        """
        try:
            self.logger.info("Searching for the Symbol input in the Strategy Tester")
            combo_boxes = self.strategy_tester.children(class_name="ComboBox")
            for combo in combo_boxes:
                title = combo.window_text()
                if "vs" in title or 'NOKSEK' in title:
                    self.logger.info(f'Found symbol input: {combo}')
                    if symbol in title:
                        self.logger.info(f'{symbol} has already been selected.')
                        return True
                    else:
                        combo.click()
                        for i, full_symbol in enumerate(combo.item_texts()):
                            if symbol in full_symbol:
                                combo.select(i)
                                combo.set_keyboard_focus()
                                send_keys('{ENTER}')
                                self.logger.info(f'Found and selected {symbol} in the dropdown.')
                                return True
            return False
        except Exception as e:
            self.logger.error(f'Error has occurred when choosing the symbol: {e}')
            return False

    def choose_period(self, period):
        """
        Selects the specified period in the Strategy Tester.

        Args:
            period (str): The period to select.

        Returns:
            bool: True if the period was successfully selected, False otherwise.
        """
        try:
            self.logger.info("Searching for the Period input in the Strategy Tester")
            combo_boxes = self.strategy_tester.children(class_name="ComboBox")
            for combo in combo_boxes:
                title = combo.window_text()
                if "M1" in title or 'M5' in title or 'M15' in title or 'M30' in title or 'H1' in title or 'H4' in title or 'Daily' in title:
                    self.logger.info(f'Found Period input: {combo}')
                    if period in title:
                        self.logger.info(f'{period} has already been selected.')
                        return True
                    else:
                        combo.click()
                        for i, option in enumerate(combo.item_texts()):
                            if period in option:
                                combo.select(i)
                                combo.set_keyboard_focus()
                                send_keys('{ENTER}')
                                self.logger.info(f'Found and selected {period} in the dropdown.')
                                return True
            
            return False
        except Exception as e:
            self.logger.error(f'Error has occurred when choosing the period: {e}')
            return False

    def choose_modelling(self, model):
        """
        Selects the specified modeling type in the Strategy Tester.

        Args:
            model (str): The modeling type to select.

        Returns:
            bool: True if the modeling type was successfully selected, False otherwise.
        """
        try:
            self.logger.info("Searching for the Model input in the Strategy Tester")
            combo_boxes = self.strategy_tester.children(class_name="ComboBox")
            for combo in combo_boxes:
                title = combo.window_text()
                if "Every tick" in title or 'Control points' in title or 'Open prices' in title:
                    self.logger.info(f'Found Model input: {combo}')
                    if model in title:
                        self.logger.info(f'{model} has already been selected.')
                        return True
                    else:
                        combo.click()
                        for i, option in enumerate(combo.item_texts()):
                            if model in option:
                                combo.select(i)
                                combo.set_keyboard_focus()
                                send_keys('{ENTER}')
                                self.logger.info(f'Found and selected {model} in the dropdown.')
                                return True
            return False
        except Exception as e:
            self.logger.error(f'Error has occurred when choosing the model: {e}')
            return False

    def configure_visual_mode(self):
        """
        Configures the Visual mode in the Strategy Tester by unchecking it.

        Returns:
            bool: True if Visual mode was successfully unchecked, False otherwise.
        """
        try:
            self.logger.info("Searching for the Visual mode button in the Strategy Tester")
            buttons = self.strategy_tester.children(class_name="Button")
            for btn in buttons:
                if btn.window_text() == 'Visual mode':
                    btn.uncheck()
                    self.logger.info("Visual mode unchecked.")
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f'Error has occurred when unchecking Visual mode: {e}')
            return False

    def configure_dates(self, from_date, to_date):
        """
        Configures the date range in the Strategy Tester.

        Args:
            from_date (str): The start date in 'YYYY.MM.DD' format.
            to_date (str): The end date in 'YYYY.MM.DD' format.

        Returns:
            bool: True if the dates were successfully configured, False otherwise.
        """
        try:
            if from_date == None and to_date == None:
                self.logger.info("No dates to configure. Exiting.")
                return True

            self.logger.info("Searching for the Use date button in the Strategy Tester...")
            buttons = self.strategy_tester.children(class_name="Button")
            for btn in buttons:
                if btn.window_text() == 'Use date':
                    btn.check()
                    self.logger.info("Use date checked.")
                    break

            self.logger.info("Searching for the dates in the Strategy Tester...")
            dates = self.strategy_tester.children(class_name="SysDateTimePick32")

            if from_date is not None:
                _from = datetime.strptime(from_date, '%Y.%m.%d')
                dates[0].set_time(year=_from.year, month=_from.month, day=_from.day)

            if to_date is not None:
                to = datetime.strptime(to_date, '%Y.%m.%d')
                dates[1].set_time(year=to.year, month=to.month, day=to.day)

            self.logger.info("Dates configured successfully.")
            return True
        except Exception as e:
            self.logger.error(f'Error has occurred when configuring the dates: {e}')
            return False

    def start_strategy_tester(self):
        """
        Starts the Strategy Tester by clicking the Start button.

        Returns:
            bool: True if the Strategy Tester was successfully started, False otherwise.
        """
        try:
            self.logger.info("Searching for the Start button in the Strategy Tester...")
            buttons = self.strategy_tester.children(class_name="Button")
            for btn in buttons:
                if btn.window_text() == 'Start':
                    btn.click()
                    self.logger.info("Clicked on 'Start' button")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"An error occurred while starting the Strategy Tester: {e}")
            return False


class StrategyTester:
    def __init__(self, mt4):
        self.mt4 = mt4
        self.logger = setup_logger(__name__)

    def configure_tester(self, app, settings):
        """
        Configures the MetaTrader 4 Strategy Tester with the given settings.

        Args:
            app (Application): The connected MT4 application.
            settings (dict): A dictionary containing the settings for the Strategy Tester.

        Returns:
        bool: True if the configuration was successful, False otherwise.
        """
        try:
            # Open MT4 or connect to it if it's already open
            tradeview = self.mt4.wait_for_window(app, title_re=".*Tradeview.*", timeout=self.mt4.timeout)
            if tradeview is None:
                self.logger.error("Failed to find the Tradeview window.")
                return False

            tradeview.set_focus()
            if not tradeview.is_maximized():
                tradeview.maximize()
                time.sleep(1)

            tester_open = self.mt4.is_strategy_tester_open(tradeview, 3)
            if tester_open == False: # Check if the Strategy Tester is open. Open it if it's not
                self.logger.info("Strategy Tester is not open. Trying to open it.")
                tradeview.send_keystrokes('^r') # Press Ctrl+R to open the Strategy Tester
                time.sleep(2.5) # Give the Strategy Tester time to open
                tester_open = self.mt4.is_strategy_tester_open(tradeview, 3)
                if not tester_open:
                    self.logger.error("Failed to open the Strategy Tester. Exiting.")
                    return False

            if not self.mt4.tester_switch_tab(tradeview, self.mt4.SETTINGS_TAB): # Switch to Strategy Tester tab
                self.logger.error("Failed to switch to Settings tab in the Strategy Tester. Exiting.")
                return False

            if not self.mt4.select_expert_advisor(): # Make sure that "Expert Advisor" is selected in the Strategy Tester
                self.logger.error(f"Failed to select Expert Advisor in Strategy Tester. Continuing.")
                return False

            ea_name = settings['Expert'].strip()
            if not self.mt4.choose_EA(ea_name): # Select the EA
                self.logger.error(f"Failed to select EA '{ea_name}'. Continuing.")
                return False

            # Configure Expert properties
            if not self.mt4.configure_expert_properties(settings['Expert'], settings['Expert properties']):
                self.logger.error(f"Failed to configure properties for EA '{ea_name}'. Continuing.")
                return False

            tradeview = self.mt4.wait_for_window(app, title_re=".*Tradeview.*", timeout=7)
            if tradeview is None:
                self.logger.error("Failed to re-focus the Tradeview window after configuring properties.")
                return False

            symbol = settings['Symbol'].strip()
            if not self.mt4.choose_symbol(symbol): # Select the symbol
                self.logger.error(f"Failed to select symbol '{symbol}'. Continuing.")
                return False

            period = settings['Period'].strip()
            if not self.mt4.choose_period(period): # Select the period
                self.logger.error(f"Failed to select period '{period}'. Continuing.")
                return False

            model = settings['Model'].strip()
            if not self.mt4.choose_modelling(model): # Select the model
                self.logger.error(f"Failed to select model '{model}'. Continuing.")
                return False

            if not self.mt4.configure_visual_mode(): # Configure Visual mode
                self.logger.error(f"Failed to uncheck Visual mode. Continuing.")
                return False

            if not self.mt4.configure_dates(settings['From'], settings['To']): # Configure the dates
                self.logger.error(f"Failed to configure the dates. Continuing.")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Exception occurred while configuring the Strategy Tester: {e}")
            return False

    def run_test(self):
        '''
        This starts a back test and waits until it stops.
        '''
        try:
            if not self.mt4.start_strategy_tester(): # Start the Strategy Tester
                self.logger.error(f"Failed to start the Strategy Tester. Continuing.")
                return False

            # Loop will run as long as the "Stop" button is visible, indicating the test is running
            while True:
                try:
                    self.mt4.strategy_tester.child_window(class_name="Button", title="Stop").wait("exists visible", 1)
                except Exception as e:
                    self.logger.info("Stop button is no longer present, assuming the test has finished.")
                    break
            
            # As soon as the while loop exits, the test has finished because the "Stop" button is not visible anymore
            self.logger.info("Test has finished.")
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred while waiting for the Strategy Tester to start: {e}")
            return False