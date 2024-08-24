import pandas as pd
import hrequests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from utility import *



def get_details(link):
    """
    This function fetches the HTML content of a given URL and extracts all details to news articles.

    Args:
        url: The URL of the article to scrape.

    Returns:
        details of articles like title,description,date,image
    """
    try:
        options = Options()
        options.add_argument("--headless")  # Enables headless mode
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        WebDriverWait(driver, 20)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Extract data from specific metadata tags (replace with your logic)
        title = get_title(soup)
        description=get_description(soup)
        date=get_date(soup)
        image=get_image(soup)
        data={ "Title":title,
                "Description":description,
                "Date published":date,
                "Image":image,
                "link":link}
        print(data["Title"],data['Image'],data['Date published'])
        print("-------"*10)
        return data
    except Exception as e:
            print(f"Error: {link} - {e}")
            return None

def get_article_links(url):
  """
  This function fetches the HTML content of a given URL and extracts all links to news articles.

  Args:
      url: The URL of the website to scrape.

  Returns:
      A list of URLs of news articles found on the website.
  """
  response = hrequests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find all links on the page
  links = soup.find_all('a')
  # Filter links to news articles
  article_links = set()
  for link in links:
    href = link.get('href')
    if 'https://tribune.com.pk/story/' in href:
        article_links.add(href)

  return article_links




def tribune():
    url = "https://tribune.com.pk/"
    article_links = get_article_links(url)
    print(article_links)
    print("Number of articles to be fetched :",len(article_links))
    all_articles=[]
    with ThreadPoolExecutor(max_workers=4) as executor:
        all_articles = list(executor.map(get_details, article_links))
    print(all_articles)
    print("Number of articles fetched :",len(all_articles))
    df=pd.DataFrame(all_articles)
    df.to_csv('data.csv')
    return df

if __name__=="__main__":
   tribune()
