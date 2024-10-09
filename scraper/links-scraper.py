from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os

sitemap_url = "https://www.immoweb.be/sitemap.xml"

driver = webdriver.Firefox()

driver.get(sitemap_url)

classified_links = []

sitemaps = driver.find_elements(By.TAG_NAME, "loc")

for sitemap in sitemaps:
    loc = sitemap.text
    if "classifieds" in loc:
        classified_links.append(loc)

driver.close()

download_folder = "data\raw_links"

for link in classified_links:
    filename = link.split("/")[-1]

    file_path = os.path.join(download_folder, filename)

    response = requests.get(link)

    with open(file_path, "wb") as file:
        file.write(response.content)