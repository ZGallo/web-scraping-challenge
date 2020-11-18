#relevant imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
import time

def scraper_function():
    
    ###################################
    #           NASA Mars News        #
    ###################################
      
    #using  chromedriver and browser method
    #setup and fire up browser task 1 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit URL
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    #find relevant class and store in a list 
    item_list = soup.find_all('li', class_ = 'slide')

    #loop and strip the html
    titles = []
    descriptions = []
    for data in item_list:
    
        title = data.find('h3').text
        titles.append(title)
    
        description = data.find('a').text
        descriptions.append(description) 
    
    # Close the browser after scraping
    browser.quit()    
    
    ###########################################
    # JPL Mars Space Images - Featured Image  #
    ###########################################
    
    #using request method 
    #initial URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url)

    #soup object: html doc
    soup = bs(response.text, 'html.parser')

    #url inspection and finding the image's parent class
    img_src = soup.footer.a["data-fancybox-href"]

    featured_img = "https://www.jpl.nasa.gov/" + img_src


    ########################################
    #            Mars Facts                #
    ########################################
    
    facts_url = 'https://space-facts.com/mars/'
    df = pd.read_html(facts_url)
    
    mars_table = df[0]
    mars_table = mars_table.rename({0: "", 1: "Data"}, axis =1).set_index("")

    #export as a html file
    mars_table.to_html("mars_facts.html")
    
    ########################################
    #          Mars Hemispheres            #
    ########################################
    
    #using  chromedriver and browser method
    #setup and fire up browser task 1 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    time.sleep(2)
    
    #all items where the links are stored
    items = soup.find_all('div', class_ = 'item')

    home_url = 'https://astrogeology.usgs.gov' 

    #here I will store dictionaries for each item
    links_list = []

    #looping through each item
    for item in items:
        
        #initialising empty dictionary to store the links of each image
        hemishpere_data = {}
    
        #dictionary key: 'title' ; value-pair: item title
        hemishpere_data['title'] = item.find('h3').text.strip('Enhanced').strip()
    
        #find image link, create new URL, request and create soup object
        img_link = item.find('a')['href']
        new_url = home_url + img_link
        response = requests.get(new_url)
        soup = bs(response.text, 'html.parser')
   
        #find full image link 
        full_size_img = soup.find_all('div', class_ = 'downloads')[0].find('li').find('a')['href']
    
        #dictionary key for link
        hemishpere_data['img_url'] = full_size_img
    
        #appending dictionary to the list 
        links_list.append(hemishpere_data)

    ############################
    #  ALL SCRAPES COMPLETE    # 
    ###########################

    #Compiling all scrapes into 1 dictionary but the table which I have already exported to a html
    mars_data = {"news_title": titles[0],
                "mars_news":descriptions[0],
                "featured_img": featured_img,
                "hemispheres": links_list
                 }
    
    # Close the browser after scraping
    browser.quit()
    
    return mars_data