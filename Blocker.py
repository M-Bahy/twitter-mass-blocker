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
blocked = 0


def init_driver():
    chrome_path = os.getenv("chrome_path")
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    return webdriver.Chrome(options=chrome_options)


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
    print("Logged in successfully")


def get_target(driver, url):
    global tweet_author
    driver.get(url)
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
    print(f"Target is {tweet_author}")


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
        targets.append(follower.text[1:])
    driver.execute_script("window.scrollTo(0, 0);")
    delay(2)
    followers = driver.find_elements(
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[*]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span",
    )
    for follower in followers:
        follower_text = follower.text[1:]
        if follower_text not in targets:
            targets.append(follower_text)
    print(f"Found {len(targets)-1} followers")


def mass_block(driver):
    global blocked
    for target in targets:
        print(f"Blocked {blocked} out of {len(targets)}")
        driver.get(f"https://x.com/{target}")
        delay(2)
        try:
            three_dots_button = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[1]",
            )
            three_dots_button.click()
        except Exception:
            continue
        delay(1)
        try:
            block_button = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div[4]/div[2]/div/span",
            )
            block_button.click()
            delay(1)
            confirm_block_button = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]",
            )
            confirm_block_button.click()
            delay(2)
            blocked += 1
        except Exception:
            continue


def collect_targets(driver, url):
    get_target(driver, url)
    get_followers(driver)


def main():
    driver = init_driver()
    login(driver)

    if not os.path.exists("targets.txt"):
        open("targets.txt", "w").close()
    with open("targets.txt", "r") as file:
        for url in file:
            collect_targets(driver, url.strip())

    mass_block(driver)

    open("targets.txt", "w").close()


if __name__ == "__main__":
    main()
