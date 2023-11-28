import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import re
import getpass


SEARCH_BOX_SELECTOR = 'input[aria-label="Search"]'
CHANNEL_SELECTOR = 'div[aria-label="{}"]'
MESSAGE_TIMESTAMP_SELECTOR = '#message-timestamp-1178381716537213018'

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def login(driver, email, password):
    username_field = driver.find_element(By.NAME, 'email')
    password_field = driver.find_element(By.NAME, 'password')

    username_field.send_keys(email)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)


def scroll_to_date(driver, target_date):
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search"]'))
    )
    search_box.send_keys(target_date)
    search_box.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'your_search_results_selector_here'))
    )


def navigate_to_channel(driver, channel_id, chat_id):
    channel_selector = CHANNEL_SELECTOR.format(channel_id)
    channel_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, channel_selector))
    )
    channel_element.click()

    full_url = f'https://discord.com/channels/{channel_id}/{chat_id}'
    driver.get(full_url)
    time.sleep(2)


def scroll_until_element_by_datetime(driver, datetime_pattern):
    while True:
        try:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
            element = WebDriverWait(driver, 0.3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'time[datetime]'))
            )
            datetime_value = element.get_attribute('datetime')
            if re.match(datetime_pattern, datetime_value):
                break
        except TimeoutException:
            for _ in range(5):
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)


if __name__ == "__main__":
    driver = initialize_driver()
    discord_login = 'https://discord.com/login'
    discord_channels = 'https://discord.com/channels'
    driver.get(discord_login)

    discord_email = input('Discord email:')
    discord_password = getpass.getpass('Discord password: ')

    login(driver, discord_email, discord_password)
    channel_id = '1111983596572520458'  # 1111983596572520458 ciekawy discord LLM
    chat_id = '1112794268080283728'  # 1112794268080283728

    full_url = discord_channels + '/' + channel_id + '/' + chat_id
    driver.get(full_url)
    time.sleep(3)

    datetime_pattern = r'^2023-11-20'
    scroll_until_element_by_datetime(driver, datetime_pattern)

    input("stop")

    driver.quit()
