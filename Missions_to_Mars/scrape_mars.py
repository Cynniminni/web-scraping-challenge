import pandas as pd
import json
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def save_html(html, path):
    with open(path, 'w') as file:
        file.write(html)

def open_html(path):
    with open(path, 'r') as file:
        return file.read()

def nasa_mars_news() -> tuple:
    # Mars News Site: https://redplanetscience.com - Using selenium
    driver = webdriver.Chrome()
    url = "https://redplanetscience.com"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Pull out the first news title and news paragraph
    news_title = soup.select_one('.content_title').text
    news_p = soup.select_one('.article_teaser_body').text
    print(f"News title = {news_title}")
    print(f"News p = {news_p}")

    return news_title, news_p

def jpl_mars_space_images() -> str:
    # JPL Mars Space Images - Featured Image: https://spaceimages-mars.com - using Splinter
    url = "https://spaceimages-mars.com"
    browser = Browser('chrome')
    browser.visit(url)
    featured_image_url = browser.find_by_xpath('/html/body/div[1]/img').first['src']
    browser.quit()

    return featured_image_url

def mars_facts() -> str:
    # Mars Facts webpage - https://galaxyfacts-mars.com
    url = "https://galaxyfacts-mars.com"

    # Use pandas to pull web page, this is returned as a list of DataFrames
    mars_facts = pd.read_html(url)

    # Combine list of DataFrames into one DataFrame
    mars_facts_data_frame = pd.concat(mars_facts)

    # Use Pandas to convert the data to a HTML table string.
    mars_facts_html = mars_facts_data_frame.to_html()
    return mars_facts_html

def mars_hemispheres() -> list:
    # Mars Hemispheres - https://marshemispheres.com
    url = "https://marshemispheres.com"

    # Open browser and go to the web page
    driver = webdriver.Chrome()
    driver.get(url)

    # Get all <a> elements
    links_list = driver.find_elements(by=By.TAG_NAME, value="a")

    filtered_links_list = []
    for link in links_list:
        # Only deal with the ones that contain a partial url of ".html"
        # And only keep the ones that has non-zero size values
        href = link.get_attribute(name="href")
        size = link.size
        if (".html" in href) and (size["height"] and size["width"]):
            filtered_links_list.append(href)

    print("List of links to click on:")
    print("\n".join(filtered_links_list))

    hemisphere_image_urls = []
    for url in filtered_links_list:
        # Initialize data to add later
        data = {}

        # Navigate to each link
        driver.get(url)

        # Get the corresponding title
        title = driver.find_element(by=By.CLASS_NAME, value="title")
        data["title"] = title.text

        # Get list of all <a> tags
        a_links_list = driver.find_elements(by=By.TAG_NAME, value="a")

        # Only look at the <a> tag that has partial url of "full.jpg"
        for a_link in a_links_list:
            href = a_link.get_attribute(name="href")
            if "full.jpg" in href:
                data["img_url"] = href
                break
        hemisphere_image_urls.append(data)

    # Close browser
    driver.quit()

    return hemisphere_image_urls

def scrape():
    data = {
        "nasa_mars_news": nasa_mars_news(),
        "jpl_mars_space_images": jpl_mars_space_images(),
        "mars_facts": mars_facts(),
        "mars_hemispheres": mars_hemispheres()
    }

    with open('data.json', 'w') as convert_file:
        convert_file.write(json.dumps(data))


if __name__ == "__main__":
    result = mars_facts()
