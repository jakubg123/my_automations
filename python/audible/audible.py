from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

web = "https://www.audible.com/search"

driver.get(web)

container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
products = container.find_elements(By.XPATH,'.//li')

book_title = []
book_author = []
book_length = []

time.sleep(5)

for product in products:
    try:
        title_elements = product.find_elements(By.XPATH, './/h3[contains(@class, "bc-heading")]')
        author_elements = product.find_elements(By.XPATH, './/li[contains(@class, "authorLabel")]')
        length_elements = product.find_elements(By.XPATH, './/li[contains(@class, "runtimeLabel")]')

        if title_elements and author_elements and length_elements and length_elements[0].text != "N/A":
            book_title.append(title_elements[0].text)
            book_author.append(author_elements[0].text)
            book_length.append(length_elements[0].text)
        else:
            raise ValueError("Required elements not found or length is N/A.")
    
    except ValueError as e:
        print(e)


driver.quit()

df_books = pd.DataFrame({'title' : book_title, 'author' : book_author, 'length' : book_length})
df_books.to_csv('books.csv', index=False)
