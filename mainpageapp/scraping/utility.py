def get_title(soup):
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

def get_description(soup):
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
def get_date(soup):
    try:
        date=soup.find('meta',{"property":"article:published_time"}).get('content')
        return date
        pass
    except Exception as e:
        print("Error in getting date :",e)

def general_image_getter(soup):
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
def tribune_image_getter(soup):
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
def theNation_image_getter(soup):
    try:
        image=soup.find('div',{"class":"detail-page-main-image"})
        if image:
            image=image.find('img').get('src')
            return image
    except Exception as e:
        print("Error in getting image The Nation :",e)
        return None 

def get_image(soup):
    image=general_image_getter(soup)
    if image:
        return image
    image=tribune_image_getter(soup)
    if image:
        return image
    image=theNation_image_getter(soup)
    if image:
        return image
    
# import pandas as pd
# df=pd.read_csv('data.csv')
# print(len(df))
# df.dropna(inplace=True)
# print(len(df))