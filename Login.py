from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import time


load_dotenv()

tweet_author = ""
targets = []


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
    driver.get("https://x.com/i/flow/login")
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


def get_target(driver):
    global tweet_author
    driver.get(os.getenv("target_url"))
    delay(5)
    try:
        target_username = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[2]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span",
        )
    except Exception:
        target_username = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span",
        )
    tweet_author = target_username.text[1:]
    targets.append(tweet_author)


def get_followers(driver):
    driver.get(f"https://x.com/{tweet_author}/followers")
    delay(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    delay(2)
    followers = driver.find_elements(
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[*]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span",
    )
    for follower in followers:
        targets.append(follower.text[1])
    driver.execute_script("window.scrollTo(0, 0);")
    delay(2)
    followers = driver.find_elements(
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[*]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span",
    )
    for follower in followers:
        follower_text = follower.text[1]
        if follower_text not in targets:
            targets.append(follower_text)


def main():
    driver = init_driver()
    login(driver)
    get_target(driver)
    get_followers(driver)
    keep_open(driver)


if __name__ == "__main__":
    main()
