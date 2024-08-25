
def get_title(soup):
    try:
        title = None
        # Attempt to find title using Twitter metadata
        twitter_title = soup.find('meta', {"name": "twitter:title"})
        if twitter_title:
            title = twitter_title.get('content')
        # If not found, try Open Graph metadata
        elif not title:
            og_title = soup.find('meta', {"property": "og:title"})
            if og_title:
                title = og_title.get('content')
        # If still not found, try to find the title from a specific HTML tag
        if not title:
            title_tag = soup.find('h2', {"data-layout": "story"})
            if title_tag:
                title = title_tag.text.strip()
        return title
    except Exception as e:
        print("Error in getting title:", e)
        return None

# def summarize(text):
#     summarizer = pipeline("summarization")
#     summary = summarizer(text, max_length=99, min_length=33, do_sample=False)
#     return summary
    
def get_description(soup):
    try:
        description = None
        # Find the <div> tag with the class 'story__content'
        story_div = soup.find('div', class_='story__content')
        if story_div:
            # Find all <p> tags within the <div> tag
            p_tags = story_div.find_all('p')
            # Join the text content of all <p> tags
            description = ' '.join([p.text.strip() for p in p_tags])
            # summary = summarize(description)
            # summary = summary['summary_text']
            # print('this is the summary', summary)
        return description
    except Exception as e:
        print("Error in getting description:", e)
        return None

# def get_description(soup):
#     try:
#         description = None
#         # Attempt to find description using Twitter metadata
#         twitter_description = soup.find('meta', {"name": "twitter:description"})
#         if twitter_description:
#             description = twitter_description.get('content')
#         # If not found, try Open Graph metadata
#         elif not description:
#             og_description = soup.find('meta', {"property": "og:description"})
#             if og_description:
#                 description = og_description.get('content')
#         # If still not found, try to concatenate all paragraph texts
#         if not description:
#             description_paragraphs = soup.find_all('p')
#             if description_paragraphs:
#                 description = ''.join([desc.text.strip() for desc in description_paragraphs])
#         return description
#     except Exception as e:
#         print("Error in getting description:", e)
#         return None

def get_date(soup):
    try:
        date = None
        # Find date using Open Graph metadata
        og_date = soup.find('meta', {"property": "article:published_time"})
        if og_date:
            date = og_date.get('content')
        return date
    except Exception as e:
        print("Error in getting date:", e)
        return None

def get_image(soup):
    try:
        image = None
        # Find image using Twitter metadata
        twitter_image = soup.find('meta', {"property": "twitter:image"})
        if twitter_image:
            image = twitter_image.get('content')
        return image
    except Exception as e:
        print("Error in getting image:", e)
        return None




#Tribune functions
def get_title_tribune(soup):
    try:
        title = soup.find('meta', {"name": "twitter:title"}).get('content', None)
        if not title:
            title = soup.find('meta', {"property": "og:title"}).get('content', None)
        if not title:
            title = soup.find('h2', {"data-layout": "story"}).text.strip()
        return title
    except Exception as e:
        print("Error in getting title:", e)
        return None

def get_description_tribune(soup):
    try:
        description = None
        p_tags = soup.find_all('p')
        if p_tags:
            description = ' '.join([p.text.strip() for p in p_tags])
        if not description:
            description = soup.find('meta', {"og": "title"}).get('content', None)
        if not description:
            description = soup.find('meta', {"name": "twitter:description"}).get('content', None)
        return description
    except Exception as e:
        print("Error in getting description:", e)
        return None

def get_date_tribune(soup):
    try:
        date = soup.find('meta', {"property": "article:published_time"}).get('content', None)
        return date
    except Exception as e:
        print("Error in getting date:", e)
        return None

def general_image_getter_tribune(soup):
    try:
        image = soup.find('meta', {"property": "twitter:image"}).get('content', None)
        return image
    except Exception as e:
        print("Error in getting image:", e)
        return None

def tribune_image_getter_tribune(soup):
    try:
        image = soup.find('div', {"class": "featured-image-global"})
        if image:
            image = image.find("img").get('src', None)
        else:
            image = soup.find('meta', {"name": "twitter:image:src"}).get('content', None)
        return image
    except Exception as e:
        print("Error in getting image from tribune:", e)
        return None

def theNation_image_getter_tribune(soup):
    try:
        image = soup.find('div', {"class": "detail-page-main-image"})
        if image:
            image = image.find('img').get('src', None)
        return image
    except Exception as e:
        print("Error in getting image from The Nation:", e)
        return None

def get_image_tribune(soup):
    image = general_image_getter_tribune(soup)
    if not image:
        image = tribune_image_getter_tribune(soup)
    if not image:
        image = theNation_image_getter_tribune(soup)
    return image







#urdu data


def get_title_urdu(soup):
    try:
        try:
            title=soup.find('meta',{"name":"twitter:title"}).get('content')
            if title:
                return title
        except:
            title=soup.find('meta',{"property":"og:title"}).get('content')
            return title
        else:
            title=soup.find('h2',{"data-layout":"story"}).text
            return title
    except Exception as e:
        print("Error in getting title :",e)

def get_description_urdu(soup):
    try:
        try:
            description=soup.find_all('p')
            if description:
                full_desc=''.join([desc.text for desc in description])
                return full_desc
        except:
            description=soup.find('meta',{"og":"title"}).get('content')
            return description
        else:
            description=soup.find('meta',{"name":"twitter:description"}).get('content')
            return description
    except Exception as e:
        print("Error in getting description :",e)
def get_date_urdu(soup):
    try:
        date=soup.find('meta',{"property":"article:published_time"}).get('content')
        return date
    except Exception as e:
        print("Error in getting date :",e)

def get_date_jung_urdu(soup):
    try:
        date_text=[]
        dates=soup.find_all('div',{"class":"detail-time"})
        for date in dates:
            date_text.append(date.text)
        return date_text[-1]
    except Exception as e:
        print("Error in getting date jung :",e)

def general_image_getter_urdu(soup):
    try:
        image=soup.find('meta',{"property":"twitter:image"}).get('content')
        return image
    except Exception as e:
        print("Error in getting image :",e)
        image=soup.find('meta',{"property":"og:image"})
        if image:
            image=image.get('content')
            return image
        else:
            print("Could not find image")
            return None
def tribune_image_getter_urdu(soup):
    try:
        image=soup.find('div',{"class":"featured-image-global"})
        if image:
            image=image.find("img").get('src')
            return image
        else:
            image=soup.find('meta',{"name":"twitter:image:src"}).get('content')
            return image
    except Exception as e:
        print("Error in getting image tribune :",e)
        return None
def theNation_image_getter_urdu(soup):
    try:
        image=soup.find('div',{"class":"detail-page-main-image"})
        if image:
            image=image.find('img').get('src')
            return image
    except Exception as e:
        print("Error in getting image The Nation :",e)
        return None 
def express_image_getter_urdu(soup):
    try:
        image=soup.find('div',{"class":"story-image catbdr"})
        if image:
            image=image.find('img').get('src')
            return image
    except Exception as e:
        print("Error in getting image express :",e)
        return None

def jang_image_getter_urdu(soup):
    try:
        image=soup.find('div',{"class":"medium-insert-images ui-sortable"})
        if image:
            image=image.find('img').get('src')
            return image
    except Exception as e:
        print("Error in getting image jang :",e)
        return None



def get_image_urdu(soup):
    image=general_image_getter_urdu(soup)
    if image:
        return image
    image=tribune_image_getter_urdu(soup)
    if image:
        return image
    image=theNation_image_getter_urdu(soup)
    if image:
        return image
    image=express_image_getter_urdu(soup)
    if image:
        return image
    image=jang_image_getter_urdu(soup)
    if image:
        return image

    

# for aljazeera data
def get_title_aljazeera(soup):
    try:
        try:
            title=soup.find('meta',{"name":"twitter:title"}).get('content')
            if title:
                return title
        except:
            title=soup.find('meta',{"property":"og:title"}).get('content')
            return title
        else:
            title=soup.find('h2',{"data-layout":"story"}).text
            return title
    except Exception as e:
        print("Error in getting title :",e)

def get_description_aljazeera(soup):
    try:
        try:
            description=soup.find_all('p')
            if description:
                full_desc=''.join([desc.text for desc in description])
                return full_desc
        except:
            description=soup.find('meta',{"og":"title"}).get('content')
            return description
        else:
            description=soup.find('meta',{"name":"twitter:description"}).get('content')
            return description
    except Exception as e:
        print("Error in getting description :",e)
def get_date_aljazeera(soup):
    try:
        date=None
        if date is None:
            try:
                date=soup.find('meta',{"property":"article:published_time"}).get('content')
            except:
                date=None
        if date is None:
            try:
                date=soup.find('meta',{'name':'publishedDate'}).get('content')
            except:
                date=None
        if date is not None:
            return date
    except Exception as e:
        print("Error in getting date :",e)

def get_date_jung_aljazeera(soup):
    try:
        date_text=[]
        dates=soup.find_all('div',{"class":"detail-time"})
        for date in dates:
            date_text.append(date.text)
        return date_text[-1]
    except Exception as e:
        print("Error in getting date jung :",e)

def general_image_getter_aljazeera(soup):
    try:
        image=soup.find('meta',{"property":"twitter:image"}).get('content')
        return image
    except Exception as e:
        print("Error in getting image :",e)
        image=soup.find('meta',{"property":"og:image"})
        if image:
            image=image.get('content')
            return image
        else:
            print("Could not find image")
            return None
def tribune_image_getter_aljazeera(soup):
    try:
        image=soup.find('div',{"class":"featured-image-global"})
        if image:
            image=image.find("img").get('src')
            return image
        else:
            image=soup.find('meta',{"name":"twitter:image:src"}).get('content')
            return image
    except Exception as e:
        print("Error in getting image tribune :",e)
        return None
def theNation_image_getter_aljazeera(soup):
    try:
        image=soup.find('div',{"class":"detail-page-main-image"})
        if image:
            image=image.find('img').get('src')
            return image
    except Exception as e:
        print("Error in getting image The Nation :",e)
        return None 
def express_image_getter_aljazeera(soup):
    try:
        image=soup.find('div',{"class":"story-image catbdr"})
        if image:
            image=image.find('img').get('src')
            return image
    except Exception as e:
        print("Error in getting image express :",e)
        return None

def jang_image_getter_aljazeera(soup):
    try:
        image=soup.find('div',{"class":"medium-insert-images ui-sortable"})
        if image:
            image=image.find('img').get('src')
            return image
    except Exception as e:
        print("Error in getting image jang :",e)
        return None



def get_image_aljazeera(soup):
    image=general_image_getter_aljazeera(soup)
    if image:
        return image
    image=tribune_image_getter_aljazeera(soup)
    if image:
        return image
    image=theNation_image_getter_aljazeera(soup)
    if image:
        return image
    image=express_image_getter_aljazeera(soup)
    if image:
        return image
    image=jang_image_getter_aljazeera(soup)
    if image:
        return image
