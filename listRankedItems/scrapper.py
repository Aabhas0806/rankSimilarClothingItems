from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from .ranker import model, ranker_function
from sklearn.metrics.pairwise import cosine_similarity

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id":'productTitle'})
        title_value = title.text
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""
    return title_string



def get_price(soup):
    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

    except AttributeError:
        try:
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

        except:
            price = ""
    return price



def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
        
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	
    return rating


def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	
    return review_count


def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	
    return available


def ranked_list_maker(input_data):
    print("start")
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})
    URL = f"https://www.amazon.com/s?k={input_data}"
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    links_list = []
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[], 'link':[]}
   
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        rating =get_rating(new_soup).split(' ')
        reviews = get_review_count(new_soup).split(' ')
        availability = get_availability(new_soup)
        price = get_price(new_soup)
        d['title'].append(get_title(new_soup)) #5
        try:
            d['price'].append(float(price[1:]))#2
        except:
            d['price'].append(0)#2
        # print("price", d['price'])
        
        try:
            d['rating'].append(float(rating[0])) #4
        except:
            d['rating'].append(0) #4
        try:
            d['reviews'].append(float(''.join(reviews[0].split(',')))) #1
        except:
            d['reviews'].append(0) #1
        # if availability =='In Stock':
        #     d['availability'].append(1) #3
        # else:
        #     d['availability'].append(0) #3
        d['link'].append("https://www.amazon.com" + link)
        # print( d['rating'], d['reviews'], d['availability'])
        # except:
            # pass
        # break
    print("stage 1 pass")
    
    sentences = [input_data] + d['title']
    sentence_embeddings = model.encode(sentences)
    
    similarity_list = cosine_similarity(
    [sentence_embeddings[0]],
    sentence_embeddings[1:]
)
    similarity_list = list(similarity_list[0])
    
    # print(similarity_list)
    
    rank_list_index = ranker_function(len(similarity_list),similarity_list, d['rating'])
   
    print("stage 2 pass")
    # print(rank_list_index)
    
    content = dict()
    count = 1
    for i in rank_list_index:
        content[count] = [d['title'][i], d['rating'][i], d['price'][i], d['reviews'][i], d['link'][i]]
        count+=1
        
    print("stage 3 pass")
    # print(content)
    print("finish")
    
    return content
        
    

# ranked_list_maker('shirt')
    