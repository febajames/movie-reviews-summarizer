from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re


# Chrome driver for selenium
chrome_path = './chromedriver/chromedriver'
driver = webdriver.Chrome(chrome_path)

# Load the file with urls --just the train dataset
neg_urls = pd.read_csv("train/urls_neg.txt", header=None)
pos_urls = pd.read_csv("train/urls_pos.txt", header=None)

# Combine the files
urls_df = pd.concat([pos_urls, neg_urls])
urls_df.columns = ["url"]

# Get the unique rows
urls_df.drop_duplicates(inplace=True)
urls_df.reset_index(inplace=True, drop=True)

# Remove "/usercomments" from the urls
urls_df["url"] = urls_df.url.apply(lambda x: x.split('/usercomments')[0])



# Try for everything

names = []
genres = []

count=0
for i in range(urls_df.shape[0]):
    driver.get(urls_df.url[i])
    source = driver.page_source
    time.sleep(0.5)
    soup = BeautifulSoup(source, 'html.parser')
    # Get the title
    try: 
        name = soup.find("div", {"class":"title_wrapper"}).find("h1").text
        name = re.sub("\xa0","",name).strip()
        names.append(name)
        # Get the genre
        xx = soup.find("div", {"class":"title_wrapper"}).find_all("a")
        xxa = [x.text.strip() for x in xx if "genre" in x["href"]]
        xxa = ",".join(xxa)
        genres.append(xxa)
    except:
        names.append("")
        genres.append("")
    print(count)
    count += 1



urls_df["title"] = names
urls_df["genres"] = genres

# write to csv

urls_df.to_csv("train_url_titles_genres.csv", columns=urls_df.columns, encoding="utf8")