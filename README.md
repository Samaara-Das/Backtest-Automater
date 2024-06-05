## Note: This application works on MT4 only

## Below are the steps that this application should take:
1. Open the Strategy Tester
2. Read the "Strategy Tester Settings" Excel sheet for the settings to choose in the Strategy Tester.
3. As per the settings, select the inputs on the Strategy Tester.
4. Click the Start button to run the Strategy Tester
5. Go to the report tab, right click and choose save as HTML
6. Save the generated report in the folder

## For programmers
1. In the components\mt4_controller file, the `choose_EA()` method, there are 2 lines like this: `while i in range(50):`. Make sure that range is equal to/more than the number of EAs in the Experts folder on MT4.

2. In the components\mt4_controller file, `self.SETTINGS_TAB` should be a tuple containing coordinates for the Settings tab in the Strategy Tester. `self.REPORT_TAB` should be a tuple containing coordinates for the Report tab.