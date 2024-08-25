from bs4 import BeautifulSoup
import hrequests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from .utility import *
from .models import ScrapedNewsData
from .ml_model import summarize
import requests
from dateutil import parser
from concurrent.futures import ThreadPoolExecutor
import re
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
        driver.quit()  # Close the browser

        # Extract data from the soup using utility functions
        title = get_title_aljazeera(soup)
        description = get_description_aljazeera(soup)
        if not description:
            logger.warning(f"No description found for link: {link}")
            return None
        
        # summary = summarize(description)
        date = get_date_aljazeera(soup)
        image = get_image_aljazeera(soup)

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
    response = hrequests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')  
    links = soup.find_all('a')
    article_links = set()
    for link in links:
        if len(article_links) >= max_links:
            break
        href = link.get('href')    
        pattern = r'/\d{4}/\d{2}/\d{2}/[^/]+/[^/]+-[^/]+-[^/]+/index\.html'
        if href and re.match(pattern, href):
            full_url = 'https://edition.cnn.com' + href
            print(full_url)
            article_links.add(full_url)

    return article_links



def fetch_and_save_articles(url, category, max_articles=3):
    logger.info(f"Fetching and saving articles for category: {category}")
    article_links = get_article_links(url, max_articles)
    all_articles = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        all_articles = list(executor.map(get_details, article_links))
    all_articles = [article for article in all_articles if article is not None]
    for article in all_articles:
        if article['Title'] and article['Description'] and article['Date published'] and article['Image'] and article['Link']:
            save_data_to_database(article['Title'], article['Description'], article['Date published'], article['Image'], article['Link'], category, "CNN News")

from django.conf import settings

def cnn_news():
    logger.info('Starting dawn scraping')
    categories = {
        "world": "https://edition.cnn.com/world",
   
    }
    max_articles = settings.NUMBER_OF_NEWS
    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
        futures = [executor.submit(fetch_and_save_articles, url, category, max_articles) for category, url in categories.items()]
        for future in futures:
            future.result()
    return "Data fetched from all categories"

if __name__=="__main__":
   cnn_news()
