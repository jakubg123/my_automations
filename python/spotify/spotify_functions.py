import datetime
from spotify_settings import EMAIL, PASSWORD, SPOTIFY_ID
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from pytube import YouTube
import os


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("headless=new")
    return webdriver.Chrome(options=chrome_options)

def login_to_spotify(driver, email, password):
    driver.get("https://accounts.spotify.com/en/login?continue")

    email_elem = driver.find_element(By.XPATH, '//*[@id="login-username"]')
    email_elem.send_keys(email)
    password_elem = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    password_elem.send_keys(password)

    login_button = driver.find_element(By.XPATH, '//span[text()="Log In"]/..')
    login_button.click()
    driver.implicitly_wait(10)
    account_overview_button = driver.find_element(By.XPATH, '//*[@id="account-settings-link"]/span[1]')
    account_overview_button.click()

def get_playlist_details(driver, id):
    driver.get(f"https://open.spotify.com/playlist/{id}")
    elements = driver.find_elements(By.XPATH, '//div[@data-testid="tracklist-row"]')
    try:
        playlist_element = driver.find_element(By.ID, f'listrow-title-spotify:playlist:{id}')
        playlist_name = playlist_element.find_element(By.CLASS_NAME, 'ListRowTitle__LineClamp-sc-1xe2if1-0').text
    except:
        playlist_name = None

    return playlist_name, elements

def extract_playlist_data(driver, elements):
    count = len(elements)
    
    spotify = {}
    
    for index, _ in enumerate(range(count+1), start=2):
        try:
            element_title = driver.find_element(By.CSS_SELECTOR, f"[aria-rowindex='{index}']")
            title_element = element_title.find_element(By.CSS_SELECTOR, "a[data-testid='internal-track-link']")
            title = title_element.text
            
            authors_element = element_title.find_element(By.CSS_SELECTOR, "span.Type__TypeElement-sc-goli3j-0.bDHxRN.rq2VQ5mb9SDAFWbBIUIn.standalone-ellipsis-one-line")
            authors = authors_element.text

            time_element = element_title.find_element(By.CSS_SELECTOR, "div.Type__TypeElement-sc-goli3j-0.bDHxRN.Btg2qHSuepFGBG6X0yEN")
            time = time_element.text

            print(f"{title} {authors} {time}")

            spotify[title] = authors
        except Exception as e:
            print(f"Index: {index} Error: {e}")
            
    return spotify


def get_spotify_links(id):
    driver = initialize_driver()
    spotify = {}

    with driver:
        login_to_spotify(driver, EMAIL, PASSWORD)
        playlist_name, elements = get_playlist_details(driver,SPOTIFY_ID)
        spotify = extract_playlist_data(driver, elements)
        driver.quit()

    return spotify, playlist_name 

def search_google(query):
    driver = initialize_driver()

    try:
        driver.get("https://www.youtube.com")
        driver.implicitly_wait(10)
        conf_button = driver.find_element(By.XPATH,
                                          '//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
        conf_button.click()
        sleep(3)
        driver.implicitly_wait(10)
        search_field = driver.find_element(By.NAME, "search_query")
        search_field.clear()

        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        driver.implicitly_wait(10)

        videos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "video-title"))
        )

        element = driver.find_element(By.XPATH,
                                      '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[2]/div[1]/ytd-thumbnail/a')  # thumbnail /html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a
        link = element.get_attribute('href')

        return link
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


def download_youtube_audio(url, playlist):
    yt = YouTube(url)
    result = yt.title.split('/')[0]
    result = f"{result}.mp4"

    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
    output_directory = os.path.join(os.getcwd(), playlist)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    audio_stream.download(output_path=output_directory,filename=result)

    return result
