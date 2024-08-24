import pandas as pd
import hrequests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from .utility import *
from .models import ScrapedNewsData
from .ml_model import summarize
import requests
from dateutil import parser

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
        data.save()  # Ensure the object is saved to the database
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
        driver.quit()  # Close the browser

        # Extract data from the soup using utility functions
        title = get_title_tribune(soup)
        description = get_description_tribune(soup)
        if not description:
            logger.warning(f"No description found for link: {link}")
            return None
        
        # summary = summarize(description)
        date = get_date_tribune(soup)
        image = get_image_tribune(soup)

        data = {
            "Title": title,
            "Description": description,
            "Date published": date or '',
            "Image": image or '',
            "Link": link or '',
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

        # Find all links on the page
        links = soup.find_all('a')
        article_links = set()
        for link in links:
            if len(article_links) >= max_links:
                break
            href = link.get('href')
            if href and 'https://tribune.com.pk/story/' in href:
                article_links.add(href)
        return article_links
    except Exception as e:
        logger.error(f"Error fetching article links: {e}")
        return set()

def fetch_and_save_articles(url, category, max_articles=3):
    article_links = get_article_links(url, max_articles)
    all_articles = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        all_articles = list(executor.map(get_details, article_links))

    # Filter out None values in case of errors
    all_articles = [article for article in all_articles if article is not None]

    # Save data to the database
    for count, article in enumerate(all_articles):
        if article['Title'] and article['Description'] and article['Date published'] and article['Image'] and article['Link']:
            logger.info(f"Saving article {count + 1}")
            save_data_to_database(article['Title'], article['Description'], article['Date published'], article['Image'], article['Link'], category, "Express Tribune")

def tribune():
    categories = {
        "home": "https://tribune.com.pk/",
        "latest": "https://tribune.com.pk/latest",
        "pakistan": "https://tribune.com.pk/pakistan",
        "world": "https://tribune.com.pk/world",
        "opinion": "https://tribune.com.pk/opinion",
        "tech": "https://tribune.com.pk/tech",
        "sport": "https://tribune.com.pk/sports",
        "entertainment": "https://tribune.com.pk/entertainment",
    }
    max_articles = 2
    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
        futures = [executor.submit(fetch_and_save_articles, url, category, max_articles) for category, url in categories.items()]
        for future in futures:
            future.result()

    return "Got the data from all categories"

if __name__ == "__main__":
    tribune()