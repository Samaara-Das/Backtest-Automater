from os import getenv
from components.logger import setup_logger, INFO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.utils import read_version_from_cmd 
from webdriver_manager.core.os_manager import PATTERN
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logger for this file
main_logger = setup_logger(__name__, INFO)

CHROME_PROFILES_PATH = getenv('CHROME_PROFILES_PATH')
CHROMEDRIVER_EXE_PATH = getenv('CHROMEDRIVER_EXE_PATH')

class ChromeBrowser:
    def __init__(self, keep_open: bool, headless: bool, chrome_profile_path: str) -> None:
        chrome_options = Options() 
        # the application will run without opening the chrome browser and be lightwight on system resources. This also won't interfere with other selenium controlled browsers.
        if headless:
            chrome_options.add_argument('--headless') 
        
        chrome_options.add_experimental_option("detach", keep_open)
        chrome_options.add_argument(f"--user-data-dir={chrome_profile_path}")

        cmd = "powershell -command \"&{(Get-Item 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe').VersionInfo.ProductVersion}\""
        version = read_version_from_cmd(cmd, PATTERN["google-chrome"])
        service = ChromeDriverManager(driver_version=version).install()
        self.driver = webdriver.Chrome(service=ChromeService(service), options=chrome_options)

        main_logger.info('Chrome Browser initialized')

    def open_page(self, url: str):
        '''This opens `url` and maximizes the window'''
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            main_logger.info(f'Opened {url}')
            return True
        except WebDriverException:
            main_logger.exception(f'Cannot open this url: {url}. Error: ')
            return False 
        
    def is_no_error(self, timeout) -> bool:
        '''
        This checks if the "ERR_FILE_NOT_LOADED" error is not present on the page.
        
        Args:
            timeout (int): Time to wait for the confirmation that the error page is not loaded.

        Returns:
            bool: True if error page is not displayed, False otherwise
        '''
        try:
            error_xpath = "//div[@class='error-code' and text()='ERR_FILE_NOT_FOUND']"
            # Wait until the error message element is no longer visible
            no_error_element = WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.XPATH, error_xpath))
            )
            
            if no_error_element:
                main_logger.info('No error page is displayed.')
                return True
            
        except TimeoutException:
            main_logger.error('Timeout while checking for no error on the page. This means that there is an error.')
            return False
    
    def refresh_page(self) -> None:
        '''
        This refreshes the current page and waits until it loads.
        
        Returns:
            True if the page is refreshed successfully.
        
        Raises:
        	WebDriverException: If there is an error while refreshing the page.
        '''
        try:
            self.driver.refresh()
            main_logger.info('Page refreshed. Waiting for it to load...')
            self.driver.implicitly_wait(5) # waits for the page to load before throwing an exception
            main_logger.info('Page loaded.')
            return True
        except WebDriverException:
            main_logger.exception('Error occurred while trying to refresh page: ')
            raise