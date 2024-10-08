from selenium import webdriver
from selenium.webdriver.common.by import By

sitemap_url = "https://www.immoweb.be/sitemap.xml"

driver = webdriver.Firefox()

driver.get(sitemap_url)

classified_links = []

sitemaps = driver.find_elements(By.TAG_NAME, "loc")

for sitemap in sitemaps:
    loc = sitemap.text
    if "classifieds" in loc:
        classified_links.append(loc)
        
for link in classified_links:
    print(link)