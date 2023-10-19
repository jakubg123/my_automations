import datetime
from spotify_settings import EMAIL, PASSWORD
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from pytube import YouTube
import os

def get_spotify_links(id):
    chrome_options = Options()

    spotify = {

    }

    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get("https://accounts.spotify.com/en/login?continue")

        email_elem = driver.find_element(By.XPATH, '//*[@id="login-username"]')
        email_elem.send_keys(EMAIL)
        password_elem = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        password_elem.send_keys(PASSWORD)

        login_button = driver.find_element(By.XPATH, '//span[text()="Log In"]/..')
        login_button.click()

        driver.implicitly_wait(5)
        account_overview_button = driver.find_element(By.XPATH, '//*[@id="account-settings-link"]/span[1]')
        account_overview_button.click()

        driver.implicitly_wait(10)

        driver.get(f"https://open.spotify.com/playlist/{id}")

        elements = driver.find_elements(By.XPATH, '//div[@data-testid="tracklist-row"]')

        count = len(elements)

        for index, _ in enumerate(range(count), start=1):
            element_title = driver.find_element("xpath",
                                                f'//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[1]/section/div[2]/div[3]/div[1]/div[2]/div[2]/div[{index}]/div/div[2]/div/a/div')
            title = element_title.text

            parent_element = driver.find_elements(By.XPATH,
                                                  f'//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[1]/section/div[2]/div[3]/div[1]/div[2]/div[2]/div[{index}]/div/div[2]/div/span')

            element_author = parent_element[0]
            author_elements = element_author.find_elements(By.TAG_NAME, 'a')

            authors = [author.text for author in author_elements]

            spotify[title] = authors

        driver.quit()

        return spotify



def search_google(query):

    driver = webdriver.Chrome()

    try:
        driver.get("https://www.youtube.com")
        driver.implicitly_wait(5)
        conf_button = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
        conf_button.click()
        sleep(3)
        search_field = driver.find_element(By.NAME,"search_query")
        search_field.clear()

        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        sleep(4)

        videos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "video-title"))
        )

        element = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[2]/div[1]/ytd-thumbnail/a')#thumbnail /html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a
        link = element.get_attribute('href')

        return link
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()



def download_youtube_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
    audio_stream.download(output_path=os.getcwd())


dict = get_spotify_links('2A03IwV2MWMitDMlIGsGIN')
youtube_links = [] 
for song, authors in dict.items():
    print(f"{song} {authors}")
    query = f"{song} {' '.join(authors)}"
    youtube_links.append(search_google(query))

for object in youtube_links:
    download_youtube_audio(object)





