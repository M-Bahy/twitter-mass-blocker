from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import time


load_dotenv()


def init_driver():
    chrome_path = os.getenv("chrome_path")
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    return webdriver.Chrome(options=chrome_options)


def keep_open(driver):
    while True:
        if not any(tab for tab in driver.window_handles if tab):
            driver.quit()
            break


def delay(seconds):
    time.sleep(seconds)


def login(driver):
    driver.get("https://twitter.com/i/flow/login")
    delay(2)
    username_field = driver.find_element(By.NAME, "text")
    username_field.click()
    delay(1)
    username_field.send_keys(os.getenv("account_username"))
    delay(1)
    username_field.send_keys(Keys.RETURN)
    delay(1)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(os.getenv("PASSWORD"))
    password_field.send_keys(Keys.RETURN)
    delay(2)


def main():
    driver = init_driver()
    login(driver)
    keep_open(driver)


if __name__ == "__main__":
    main()
