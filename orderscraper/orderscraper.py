import os
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

load_dotenv(find_dotenv())

AMAZON_USERNAME = os.getenv("AMAZON_USERNAME")
AMAZON_PASSWORD = os.getenv("AMAZON_PASSWORD")

AMAZON_SIGN_IN_URL = 'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2F' \
                     'www.amazon.com%2Fgp%2Fcart%2Fview.html%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2F' \
                     'specs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=' \
                     'checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select' \
                     '&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&'
AMAZON_ORDER_URL = 'https://www.amazon.com/gp/css/order-history'
AMAZON_TRANSACTION_URL = 'https://www.amazon.com/cpe/yourpayments/transactions'

def driver_initialize() -> webdriver:
    """
    Initializes the webdriver.
    :return: instance of the webdriver.
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def amazon_log_in(driver: webdriver, username: str, password: str, url: str) -> webdriver:
    """
    Logs into amazon using the given username and password.
    :param driver: Webdriver created by selenium.
    :param username: Amazon username.
    :param password: Amazon password.
    :param url: Amazon sign in url.
    :return: instance of the webdriver.
    """
    driver.get(url)
    # handle captcha if necessary
    if driver.find_element('id', 'captchacharacters').is_displayed():
        continue_button = input('Captcha is displayed. Please solve it manually and press enter to continue.')

    driver.find_element('id', 'ap_email').send_keys(username)
    driver.find_element('id', 'continue').click()
    driver.find_element('id', 'ap_password').send_keys(password)
    driver.find_element('id', 'signInSubmit').click()

    # handle 2FA if necessary
    if driver.find_element('id', 'auth-mfa-otpcode').is_displayed():
        continue_button = input('OPT code required. Please enter it manually and press enter to continue.')

    return driver


def scrape_transaction_page(driver: webdriver, url: str) -> webdriver:
    """
    Navigates to and scrapes the transaction page and returns the webdriver.
    :param driver: Webdriver created by selenium.
    :param url: Amazon transaction page url.
    :return: instance of the webdriver.
    """
    driver.get(url)
    # TODO 3: Use selenium to scrape the transaction page and get each order
    order_num = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Order #')
    for order in order_num:
        order = order.text
        order = order.strip('Order #')
        print(order)
    return driver

def main():
    project_driver = driver_initialize()
    amazon_log_in(project_driver, AMAZON_USERNAME, AMAZON_PASSWORD, AMAZON_SIGN_IN_URL)
    scrape_transaction_page(project_driver, AMAZON_TRANSACTION_URL)

    time.sleep(6)

if __name__ == '__main__':
    main()

# TODO 4: Use selenium to click on each order and get the order details
