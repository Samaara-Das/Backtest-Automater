# Backtest Automater

Backtest Automater is designed to automate the use of the Strategy Tester in MT4. It:
- extracts data from existing HTML back test reports to an Excel file called Backtest Report Data.
- reads settings from an Excel file
- configures the Strategy Tester in MT4 based on these settings
- runs the Strategy Tester
- downloads the generated reports into a folder
- extracts data from these reports to Backtest Report Data. 

The application uses `pywinauto` for automation.

## Pre-requisites
- MT4 should exist on the desktop
- The EAs in the Instruction file should exist in MT4 in the "Experts" directory
- Make sure that back testing data is available for all the symbols, periods and date ranges in the Instruction file

## GUI
- 