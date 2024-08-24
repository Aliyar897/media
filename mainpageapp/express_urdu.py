import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from .utility import *
import requests
from .models import ScrapedNewsData
import logging
from dateutil import parser

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

def get_details_urdu(link): 

    try:
        options = Options()
        options.add_argument("--headless")  # Enables headless mode
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        WebDriverWait(driver, 20)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Extract data from specific metadata tags (replace with your logic)
        title = get_title_urdu(soup)
        description=get_description_urdu(soup)
        date=get_date_urdu(soup)
        image=get_image_urdu(soup)
        print('title',title)
        print('description',description)
        print('date',date)
        print('image',image)

        data={ "Title":title,
                "Description":description,
                "Date published":date,
                "Image":image,
                "link":link}
        print(data["Title"],data['Image'],data['Date published'],len(data["Description"]))
        print("-------"*10)
        return data
    except Exception as e:
            print(f"Error: {link} - {e}")
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
            if 'https://www.express.pk/story/' in href:
                article_links.add(href)
        return article_links
    except Exception as e:
        logger.error(f"Error fetching article links: {e}")
        return set()
# def get_article_links(url):

#   response = requests.get(url)
#   soup = BeautifulSoup(response.content, 'html.parser')

#   # Find all links on the page
#   links = soup.find_all('a')
#   # Filter links to news articles
#   article_links = set()
#   for link in links:
#     href = link.get('href')
#     if 'https://www.express.pk/story/' in href:
#         article_links.add(href)

#   return article_links
def fetch_and_save_articles(url, category, max_articles=3):
    article_links = get_article_links(url, max_articles)
    all_articles = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        all_articles = list(executor.map(get_details_urdu, article_links))

    # Filter out None values in case of errors
    all_articles = [article for article in all_articles if article is not None]

    # Save data to the database
    for count, article in enumerate(all_articles):
        if article['Title'] and article['Description'] and article['Date published'] and article['Image'] and article['link']:
            logger.info(f"Saving article {count + 1}")
            save_data_to_database(article['Title'], article['Description'], article['Date published'], article['Image'], article['link'], category, "Express Urdu")
def express_urdu():
    categories = {
        "home": "https://www.express.pk/",
        # "latest": "https://tribune.com.pk/latest",
        # "pakistan": "https://tribune.com.pk/pakistan",
        # "world": "https://tribune.com.pk/world",
        # "opinion": "https://tribune.com.pk/opinion",
        # "tech": "https://tribune.com.pk/tech",
        # "sport": "https://tribune.com.pk/sports",
        # "entertainment": "https://tribune.com.pk/entertainment",
    }
    max_articles = 4
    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
        futures = [executor.submit(fetch_and_save_articles, url, category, max_articles) for category, url in categories.items()]
        for future in futures:
            future.result()

    return "Got the data from all categories"

if __name__ == "__main__":
    express_urdu()


# def express_urdu():
#     url = "https://www.express.pk/"
#     article_links = get_article_links(url)
    
#     # Convert set to list to allow slicing
#     article_links = list(article_links)
    
#     # Limit to only 5 URLs
#     article_links = article_links[:5]
    
#     print("Hello", article_links)
#     print("Number of articles to be fetched:", len(article_links))
#     print(article_links)
    
#     all_articles = []
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         all_articles = list(executor.map(get_details_urdu, article_links))
    
#     print(all_articles)
#     print("Number of articles fetched:", len(all_articles))
#     return all_articles

# if __name__ == "__main__":
#     express_urdu()