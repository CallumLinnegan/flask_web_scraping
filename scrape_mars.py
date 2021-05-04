from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #title
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    latest_title = soup.find('div', class_='content_title').text
    latest_title.replace("\n", "")
    
    #paragraph
    latest_paragraph = soup.find('div', class_='image_and_description_container').text
    latest_paragraph.replace("\n", "")

    #image address
    image_address = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg"
    
    
    #Mars Facts
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    Mars_facts = tables[0]
    Mars_facts.columns = ['Description','Mars']
    Mars_facts.set_index('Description', inplace=True)
    Mars_facts.to_html()
    
    # titles of mars hemispheres
    astro_dict_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_dict_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    titles = []
    titles = soup.find_all('h3')
    titles[1].text
    print(titles)
    
    #image urls
    img1 = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    img2 = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    img3 = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    img4 = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    images = [img1,img2,img3,img4]
    
    #combined dictionary
    
    hemisphere_dict = [
    {"title": titles[0].text, "img_url": images[0]},
    {"title": titles[1].text, "img_url": images[1]},
    {"title": titles[2].text, "img_url": images[2]},
    {"title": titles[3].text, "img_url": images[3]},
    ]
    
    browser.quit()

    total_dict ={}
    total_dict['title'] = latest_title
    total_dict['p'] = latest_paragraph
    total_dict['featured image'] = image_address
    total_dict['Mars_facts'] = Mars_facts
    total_dict['hemispheres'] = hemisphere_dict
    return (total_dict)


    