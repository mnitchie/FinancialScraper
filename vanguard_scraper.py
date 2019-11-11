from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import argparse

import credentials

def main(implicit_wait):
    # Open chrome in incognito mode. No need to keep cookies around.
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")

    # Establish the web drivare binary
    browser = webdriver.Chrome(
        executable_path="./chromedriver",
        options=options
    )
    # If the driver can't immediately find an element, tell it to keep trying for
    # 10 seconds before giving up
    browser.implicitly_wait(implicit_wait)
    browser.get("https://investor.vanguard.com/home/")

    # Enter the username and password
    username_input = browser.find_element_by_id('USER')
    username_input.send_keys(credentials.USERNAME)
    password_input = browser.find_element_by_id('PASSWORD')
    password_input.send_keys(credentials.PASSWORD)
    login_button = browser.find_element_by_id('login')
    login_button.click()

    # Enter the 2fa code, if prompted. It appears that if you have a valid
    # session in another browser then the web driver will be able to bypass
    # 2fa, even though we are in incognito mode and that is very weird anyway
    try:
        mfa_input = browser.find_element_by_id("LoginForm:ANSWER")
    except NoSuchElementException as nse:
        pass
    else:
        mfa_code = input('Enter the security code you were just texted: ')
        mfa_input.send_keys(mfa_code)

        # Do not use "remember me"
        remember_me_option = browser.find_element_by_id("LoginForm:DEVICE:1")
        remember_me_option.click()
        continue_button = browser.find_element_by_id("LoginForm:ContinueInput")
        continue_button.click()

    browser.get('https://personal.vanguard.com/us/XHTML/myaccounts/balancesbydate')

    tables = browser.find_elements_by_css_selector('.dataTable')

    results_dict = {}
    
    # Here be hacks. Nothing useful uniquely identifies the tables on the page
    # I care about, but I know it's every 3rd table.
    for index, table in enumerate(tables, start=0):
        if index % 3 == 0:
            # This is so bad. I know it's the 1st td (zero indexed), but boy is this brittle
            account_name = table.find_element_by_tag_name('td:nth-child(2)').text
            results_dict[account_name] = []
        if index % 3 == 2:
            # The account_name will still be the preceeding table, so add it to
            # the results dict now
            rows = table.find_elements_by_tag_name('tr')
            last_row_index = len(rows)
            for row_index, row in enumerate(rows, start=0):
                # Skip the header rows
                if row_index <= 1 or row_index == last_row_index:
                    continue
                
                account_info = {}
                account_info['holding'] = row.find_element_by_css_selector('td:nth-child(2)').text
                account_info['value'] = row.find_element_by_css_selector('td:last-child').text
                results_dict[account_name].append(account_info)
    
    
    import pdb
    pdb.set_trace()
    # Just to let me see the results of the final click. Delete eventually
    WebDriverWait(browser, 20)

    #https://personal.vanguard.com/us/XHTML/myaccounts/balancesbydate
    # input#balancesByDateForm:fromDate - enter the date (last day of the previous month)
    # input#balancesByDateForm:submitDateBtnInput - trigger a click
    # 

    # Looks like a table with a class of datatable. Get the rows with [index] > 1
    # And get the second (name of fund) and last (total amount) column/td

    # But, like, it's every 3rd datatable. This is so gross.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--implicit_wait',
        type=int,
        action='store',
        default=3
    )
    args = parser.parse_args()
    main(args.implicit_wait)
