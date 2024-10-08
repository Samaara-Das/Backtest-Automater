'''
This module works with the HTML backtest reports on the browser.
'''

import os
import time
from components.logger import setup_logger, INFO
from components.browser import By

# Set up logger for this file
main_logger = setup_logger(__name__, INFO)

# Each key is a stat on an HTML report and its value is an XPATH selector
titles_and_selectors = {
    "Initial deposit": '//td[contains(text(), "Initial deposit")]/following-sibling::td',
    "Total net profit": '//td[contains(text(), "Total net profit")]/following-sibling::td',
    "Gross profit": '//td[contains(text(), "Gross profit")]/following-sibling::td',
    "Gross loss": '//td[contains(text(), "Gross loss")]/following-sibling::td',
    "Profit factor": '//td[contains(text(), "Profit factor")]/following-sibling::td',
    "Expected payoff": '//td[contains(text(), "Expected payoff")]/following-sibling::td',
    "Absolute drawdown": '//td[contains(text(), "Absolute drawdown")]/following-sibling::td',
    "Maximal drawdown": '//td[contains(text(), "Maximal drawdown")]/following-sibling::td',
    "Relative drawdown": '//td[contains(text(), "Relative drawdown")]/following-sibling::td',
    "Total trades": '//td[contains(text(), "Total trades")]/following-sibling::td',
    "Short positions (won %)": '//td[contains(text(), "Short positions (won %)")]/following-sibling::td',
    "Long positions (won %)": '//td[contains(text(), "Long positions (won %)")]/following-sibling::td',
    "Profit trades (% of total)": '//td[contains(text(), "Profit trades (% of total)")]/following-sibling::td',
    "Loss trades (% of total)": '//td[contains(text(), "Loss trades (% of total)")]/following-sibling::td',
    "Largest profit trade": "//td[contains(text(), 'Largest')]/following-sibling::td[contains(text(), 'profit trade')]/following-sibling::td",
    "Largest loss trade": "//td[contains(text(), 'Largest')]/following-sibling::td[contains(text(), 'loss trade')]/following-sibling::td",
    "Average profit trade": "//td[contains(text(), 'Average')]/following-sibling::td[contains(text(), 'profit trade')]/following-sibling::td",
    "Average loss trade": "//td[contains(text(), 'Average')]/following-sibling::td[contains(text(), 'loss trade')]/following-sibling::td",
    "Maximum consecutive wins (profit in money)": "//td[contains(text(), 'Maximum')]/following-sibling::td[contains(text(), 'consecutive wins (profit in money)')]/following-sibling::td",
    "Maximum consecutive losses (loss in money)": "//td[contains(text(), 'Maximum')]/following-sibling::td[contains(text(), 'consecutive losses (loss in money)')]/following-sibling::td",
    "Maximal consecutive profit (count of wins)": "//td[contains(text(), 'Maximal')]/following-sibling::td[contains(text(), 'consecutive profit (count of wins)')]/following-sibling::td",
    "Maximal consecutive loss (count of losses)": "//td[contains(text(), 'Maximal')]/following-sibling::td[contains(text(), 'consecutive loss (count of losses)')]/following-sibling::td",
    "Average consecutive wins": "//td[contains(text(), 'Average')]/following-sibling::td[contains(text(), 'consecutive wins')]/following-sibling::td",
    "Average consecutive losses": "//td[contains(text(), 'Average')]/following-sibling::td[contains(text(), 'consecutive losses')]/following-sibling::td"
}


def process_html_file(file_path, browser_instance, add_data_to_excel):
    """
    Opens the HTML report located at `file_path`, scrapes the data from it, and adds/updates it in the Backtest Report Data Excel file.
    
    Args:
        file_path (str): The full path to the HTML file.
        browser_instance (browser.Browser): The browser instance to use for scraping.
        add_data_to_excel (excel_utils.add_data_to_excel): The function to add/update the scraped data in the Backtest Report Data Excel file.
    
    Raises:
        Exception: If an error occurs during the processing of the HTML file.
    """
    try:
        real_path = 'file:\\' + os.path.realpath(file_path).replace('html', 'htm')
        browser_instance.open_page(real_path)
        time.sleep(1)

        # Check if there's an error when opening the file in the browser
        if browser_instance.is_no_error(1.5) == False:
            browser_instance.refresh_page() # if there's an error, refresh the page so that the file can load

        # Dictionary to hold the scraped data
        data = {"Source File": file_path}

        # Scrape and store the data
        main_logger.info(f'Scraping data from file')
        for title, selector in titles_and_selectors.items():
            try:
                element = browser_instance.driver.find_element(By.XPATH, selector)
                data[title] = element.text
            except Exception as e:
                main_logger.error(f'Error finding {title} in file {file_path}: {e}')
                data[title] = "N/A"

        # Append or update the scraped data in the Excel file
        add_data_to_excel(data)
    except Exception as e:
        main_logger.error(f'Error processing HTML file {file_path}: {e}')
        raise
