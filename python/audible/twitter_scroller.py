from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.by import By
from time import sleep

twitter = "https://twitter.com/elonmusk"

def initialize_driver(web):
    options = Options()
    #options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get(web)
    driver.maximize_window()

    return driver


def get_tweet(element):
    try:
        user = element.find_element(By.XPATH,".//span[contains(text(),'@')]").text
        text = element.find_element(By.XPATH, ".//div[@lang]").text 
        tweets_data = [user, text]
    except:
        tweets_data = ['user', 'text']
    return tweets_data




user_data = []
context_data = []
tweet_ids = set()
driver = initialize_driver("https://twitter.com/elonmusk")

wait = WebDriverWait(driver, 10)  
not_now_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'css-901oao') and text()='Not now']")))
not_now_element.click()

sleep(10)

scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
    for tweet in tweets[-15:]:
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append(tweet_list[0])
            context_data.append(tweet_list[1])


    pre_loop_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == pre_loop_height:
            scrolling = False
            break
        else:
            pre_loop_height = new_height
            break







#driver = initialize_driver("https://twitter.com/elonmusk")
#wait = WebDriverWait(driver,10)
#tweets = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
#user_data = []
#context_data = []

#for tweet in tweets:
#    tweet_list = get_tweet(tweet)
#    user_data.append(tweet_list[0])
#    context_data.append(tweet_list[1])


#driver.quit()



df_tweets = pd.DataFrame({'user' : user_data, 'text': context_data})
df_tweets.to_csv('tweets.csv', index=False)

