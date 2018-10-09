#import libraries
import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

#get reddit's home page
def get_home_page():
    url = r"https://old.reddit.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"}
    home_page = requests.get(url, headers=headers)
    if home_page.status_code == 200:
        print("Response Received")
    else:
        raise
    return home_page.text

def extract_and_store(page):
    #parse the html object
    soup = BeautifulSoup(page, 'html.parser')
    #get list of links
    links = soup.find_all("div", attrs={"class": "top-matter"})
    #get info from each link
    link_info = []
    for link in links:
        try:
            headline = link.find('a', attrs={"class": "title"}).text
            timestamp = link.find("time").get("title")
            hyperlink = link.find('a', attrs={"class": "title"}).get("href")
            comments = link.find('a', attrs={"class": "bylink"}).text
            submitter = link.find("a", attrs={"class": "author"}).text
            subreddit = link.find('a', attrs={"class": "subreddit"}).text
            link_info.append({"extract_time": str(datetime.datetime.now()),\
                              "headline": headline,\
                              "timestamp": timestamp,\
                              "hyperlink": hyperlink,\
                              "comments": comments,\
                              "submitter": submitter,\
                              "subreddit": subreddit})
        except:
            pass
    return link_info

def create_df():
	#create df to store scraped data
	return pd.DataFrame(columns=["extract_time", "headline", "timestamp", "hyperlink",\
	                             "comments", "submitter", "subreddit"])

if __name__ == "__main__":
	#create df
	home_page_info = create_df()
	#get home_page every hour
	while True:
		try:
			print("Trying to get home page")
			home_page = get_home_page()
			#store current links in df
			print("Storing extracted home page info to local df")
			home_page_info = home_page_info.append(extract_and_store(home_page))
			#store as a file
			print("Updating csv")
			home_page_info.to_csv(r"./reddit_extract.csv", index=False, mode="w")
			print(f"Data Extracted as at {datetime.datetime.now()}")
		except:
			print("No Response. Trying again in 1 minute.")
			time.sleep(60)
			continue
		print("Suspending program for 1 hour...")
		time.sleep(3600)