from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from .utility import *  # Assumes utility functions like get_title, get_description, etc., are defined here
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from .models import ScrapedNewsData
from datetime import datetime
from dateutil import parser
from dateutil import parser
from .ml_model import summarize

import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_data_to_database(title, description, date_published, image, link, category, source):
    logger.info('Saving data to database')
    try:
        existing_entry = ScrapedNewsData.objects.filter(title=title).first()
        if existing_entry:
            return existing_entry
        parsed_date = parser.parse(date_published)
        data = ScrapedNewsData.objects.create(
            title=title,
            description=description,
            date_published=parsed_date,
            image=image,
            link=link,
            category=category,
            source=source,
        )
        return data
    except Exception as e:
        logger.error(f"Error saving data to database: {e}")

def get_details(link):
    logger.info(f"Fetching details for link: {link}")
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        WebDriverWait(driver, 20)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = get_title(soup)
        description = get_description(soup)
        if not description:
            logger.warning(f"No description found for link: {link}")
            driver.quit()
            return None
        print("length of description################################################################################################################################", (description))
        # summary = summarize(description)
        # print("length of summary################################################################################################################################", len(summary))

        date = get_date(soup)
        image = get_image(soup)
        driver.quit()
        data = {
            "Title": title,
            "Description": description,
            "Date published": date,
            "Image": image,
            "Link": link
        }
        return data
    except Exception as e:
        logger.error(f"Error fetching details: {link} - {e}")
        return None

def get_article_links(url, max_links=20):
    logger.info(f"Getting article links from: {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        article_links = set()
        for link in links:
            if len(article_links) >= max_links:
                break
            href = link.get('href')
            if href and '/news/' in href:
                article_links.add(href)
        return article_links
    except Exception as e:
        logger.error(f"Error getting article links from: {url} - {e}")
        return set()

def fetch_and_save_articles(url, category, max_articles=3):
    logger.info(f"Fetching and saving articles for category: {category}")
    article_links = get_article_links(url, max_articles)
    all_articles = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        all_articles = list(executor.map(get_details, article_links))
    all_articles = [article for article in all_articles if article is not None]
    for article in all_articles:
        if article['Title'] and article['Description'] and article['Date published'] and article['Image'] and article['Link']:
            save_data_to_database(article['Title'], article['Description'], article['Date published'], article['Image'], article['Link'], category, "Dawn News")
from django.conf import settings

def dawn():
    logger.info('Starting dawn scraping')
    categories = {
        "home": "https://www.dawn.com/",
        "sport": "https://www.dawn.com/sport",
        "opinion": "https://www.dawn.com/opinion",
        "world": "https://www.dawn.com/world",
        "tech": "https://www.dawn.com/tech",
        "latest-news": "https://www.dawn.com/latest-news",
        "pakistan": "https://www.dawn.com/pakistan",
        "popular": "https://www.dawn.com/popular",
    }
    max_articles = settings.NUMBER_OF_NEWS
    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
        futures = [executor.submit(fetch_and_save_articles, url, category, max_articles) for category, url in categories.items()]
        for future in futures:
            future.result()
    return "Data fetched from all categories"

if __name__ == "__main__":
    dawn()

# def save_data_to_database(title, description, date_published, image, link, category, source):
#     print('This save to database function')
#     try:
#         existing_entry = ScrapedNewsData.objects.filter(title=title).first()
#         if existing_entry:
#             # print(f"Entry with title '{title}' already exists. Skipping insertion.")
#             return existing_entry

#         # Parse the datetime string using dateutil.parser
#         parsed_date = parser.parse(date_published)
        
#         # Create the ScrapedNewsData object with the parsed datetime
#         data = ScrapedNewsData.objects.create(
#             title=title,
#             description=description,
#             date_published=parsed_date,
#             image=image,
#             link=link,
#             category=category,
#             source=source,
#         )
#         return data
#     except Exception as e:
#         print("Error saving data to database:", e)



# def get_details(link):

#     try:
#         options = Options()
#         options.add_argument("--headless")  # Enables headless mode
#         driver = webdriver.Chrome(options=options)
#         driver.get(link)
#         WebDriverWait(driver, 20)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         # Extract data from specific metadata tags (replace with your logic)
#         title = get_title(soup)
#         description = get_description(soup)

#         # print('Getting description...', description)
#         # summary = summarize(description)

#         # print('final_summary', summary)
#         # description = summary
#         # print('Got the summary...', description)

#         date = get_date(soup)
#         image = get_image(soup)
#         data = {
#             "Title": title,
#             # "Description": summary,
#             "Description": description,
#             "Date published": date,
#             "Image": image,
#             "Link": link
#         }
#         print(data)
#         print("-------" * 10)
#         return data

#     except Exception as e:
#         print(f"Error: {link} - {e}")
#         return None

# def get_article_links(url, max_links=20):
#     # print('This is get article links...', url)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     print('soup', soup)
#     # Find all links on the page
#     links = soup.find_all('a')

#     # Filter links to news articles
#     article_links = set()
#     for link in links:

#         if len(article_links) >= max_links:

#             break
#         href = link.get('href')
#         print("href", href)
#         if href and '/news/' in href:
#             article_links.add(href)
#     # print("The article_links from the URL", article_links)

#     return article_links
# #     return "Got the aarticle"
# def fetch_and_save_articles(url, category, max_articles=3):
#     article_links = get_article_links(url, max_articles)
#     # print(f"Number of articles to be fetched for category {category}: {len(article_links)}")

#     all_articles = []
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         all_articles = list(executor.map(get_details, article_links))

#     # Filter out None values in case of errors
#     all_articles = [article for article in all_articles if article is not None]
#     print('The data here', all_articles)
#     # Save data to the database
#     for article in all_articles:
#         print("*****************")
#         print("                 ")
#         print("                 ", article)
#         print("                 ")
#         print("                 ")
#         print("*****************")

#         if article['Title'] and article['Description'] and article['Date published'] and article['Image'] and article['Link']:
#             save_data_to_database(article['Title'], article['Description'], article['Date published'], article['Image'], article['Link'], category, "Dawn News")
        

# def dawn():
#     print('I was called in dawn()')
#     categories = {
#         "home": "https://www.dawn.com/",
#         "sport": "https://www.dawn.com/sport",
#         "opinion": "https://www.dawn.com/opinion",
#         "world": "https://www.dawn.com/world",
#         "tech": "https://www.dawn.com/tech",
#         "latest-news": "https://www.dawn.com/latest-news",
#         "pakistan": "https://www.dawn.com/pakistan",
#         "popular": "https://www.dawn.com/popular",

#     }

#     max_articles = 1

#     with ThreadPoolExecutor(max_workers=len(categories)) as executor:
#         futures = [executor.submit(fetch_and_save_articles, url, category, max_articles) for category, url in categories.items()]
#         for future in futures:
#             future.result()

#     return "Got the data from all categories"




# if __name__ == "__main__":
#     dawn()


# import requests
# from bs4 import BeautifulSoup
# from concurrent.futures import ThreadPoolExecutor
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from dateutil import parser

# def save_data_to_database(title, description, date_published, image, link, category):
#     print('This save to database function')
#     try:
#         existing_entry = ScrapedNewsData.objects.filter(title=title).first()
#         if existing_entry:
#             return existing_entry

#         # Parse the datetime string using dateutil.parser
#         parsed_date = parser.parse(date_published)
        
#         # Create the ScrapedNewsData object with the parsed datetime
#         data = ScrapedNewsData.objects.create(
#             title=title,
#             description=description,
#             date_published=parsed_date,
#             image=image,
#             link=link,
#             category=category,
#         )
#         data.save()
#         return data
#     except Exception as e:
#         print("Error saving data to database:", e)

# def get_details(link):
#     try:
#         options = Options()
#         options.add_argument("--headless")  # Enables headless mode
#         driver = webdriver.Chrome(options=options)
#         driver.get(link)
#         WebDriverWait(driver, 20)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         driver.quit()  # Don't forget to quit the driver after use

#         title = get_title(soup)
#         description = get_description(soup)
#         summary = summarize(description)
#         date = get_date(soup)
#         image = get_image(soup)

#         data = {
#             "Title": title,
#             "Description": summary,
#             "Date published": date,
#             "Image": image,
#             "Link": link
#         }
#         print(data)
#         print("-------" * 10)
#         return data
#     except Exception as e:
#         print(f"Error: {link} - {e}")
#         return None

# def get_article_links(url, max_links=20):
#     print('This is get article links...', url)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     print('soup', soup)
#     links = soup.find_all('a')

#     article_links = set()
#     for link in links:
#         if len(article_links) >= max_links:
#             break
#         href = link.get('href')
#         print("href", href)
#         if href and '/news/' in href:
#             article_links.add(href)
#     print("The article_links from the URL", article_links)

#     return article_links

# def fetch_and_save_articles(url, category, max_articles=3):
#     article_links = get_article_links(url, max_articles)
#     print(f"Number of articles to be fetched for category {category}: {len(article_links)}")

#     with ThreadPoolExecutor(max_workers=4) as executor:
#         for article_data in executor.map(get_details, article_links):
#             if article_data and article_data['Title'] and article_data['Description'] and article_data['Date published'] and article_data['Image'] and article_data['Link']:
#                 save_data_to_database(article_data['Title'], article_data['Description'], article_data['Date published'], article_data['Image'], article_data['Link'], category)

# def dawn():
#     print('I was called in dawn()')
#     categories = {
#         "home": "https://www.dawn.com/",
#         "sport": "https://www.dawn.com/sport",
#         "opinion": "https://www.dawn.com/opinion",
#         "world": "https://www.dawn.com/world",
#         "tech": "https://www.dawn.com/tech",
#         "latest-news": "https://www.dawn.com/latest-news"
#     }

#     max_articles = 10

#     with ThreadPoolExecutor(max_workers=len(categories)) as executor:
#         futures = [executor.submit(fetch_and_save_articles, url, category, max_articles) for category, url in categories.items()]
#         for future in futures:
#             future.result()

#     return "Got the data from all categories"

# if __name__ == "__main__":
#     dawn()
