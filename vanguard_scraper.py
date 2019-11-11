from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

import credentials

options = webdriver.ChromeOptions()
options.add_argument(" - incognito")

browser = webdriver.Chrome(
    executable_path="./chromedriver",
    options=options
)
browser.implicitly_wait(10)
browser.get("https://investor.vanguard.com/home/")

username_input = browser.find_element_by_id('USER')
username_input.send_keys(credentials.USERNAME)

password_input = browser.find_element_by_id('PASSWORD')
password_input.send_keys(credentials.PASSWORD)

login_button = browser.find_element_by_id('login')
login_button.click()

mfa_code = input('Enter the security code you were just texted: ')

mfa_input = browser.find_element_by_id("LoginForm:ANSWER")
mfa_input.send_keys(mfa_code)

remember_me_option = browser.find_element_by_id("LoginForm:DEVICE:1")
remember_me_option.click()

continue_button = browser.find_element_by_id("LoginForm:ContinueInput")
continue_button.click()

WebDriverWait(browser, 20)