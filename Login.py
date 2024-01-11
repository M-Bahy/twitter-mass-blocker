from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

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


def main():
    driver = init_driver()
    driver.get("https://www.youtube.com/watch?v=pcmNmaXKtX0")
    keep_open(driver)


if __name__ == "__main__":
    main()
