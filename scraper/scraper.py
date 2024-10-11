from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
import os
import xml.etree.ElementTree as ET

class ImmowebScraper:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.sitemap_url = "https://www.immoweb.be/sitemap.xml"
        self.download_folder = "data/raw_links"
        self.listings = []

    def get_shadow_root(self, element):
        return self.driver.execute_script('return arguments[0].shadowRoot', element)

    def accept_cookies(self):
        shadow_host = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "usercentrics-root")))
        cookie_button = self.get_shadow_root(shadow_host).find_element(By.CSS_SELECTOR, '[data-testid=uc-accept-all-button]')
        cookie_button.click()

    def get_links(self) -> list:      
        self.driver.get(self.sitemap_url)
        classifieds = []

        sitemaps = self.driver.find_elements(By.TAG_NAME, "loc")

        for sitemap in sitemaps:
            loc = sitemap.text
            if "classifieds" in loc:
                classifieds.append(loc)

        self.driver.close()

        return classifieds

    def download_links(self, classified: str):
        filename = classified.split("/")[-1]

        file_path = os.path.join(self.download_folder, filename)

        response = requests.get(classified)

        with open(file_path, "wb") as file:
            file.write(response.content)

    def filter_links(self, file):
        tree = ET.parse(f"{self.download_folder}/{file}")
        root = tree.getroot()

        ns = {
            "default": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml"
        }

        unique_links = set()

        for url in root.findall("default:url", ns):
            for link in url.findall("xhtml:link", ns):
                if link.attrib.get("hreflang") == "en-BE" and "for-sale" in link.attrib.get("href"):
                    if "house" in link.attrib.get("href") or "apartment" in link.attrib.get("href"):
                        if "new-real-estate-project" not in link.attrib.get("href"):
                            unique_links.add(link.attrib["href"])

        with open(f"./filtered_links/{file}", "w") as filtered_links:
            for unique_link in unique_links:
                filtered_links.write(unique_link)
                filtered_links.write("\n")

    def get_data(self, url: str):
        url = "https://www.immoweb.be/en/classified/house/for-sale/wondelgem/9032/20211172"
        listing_data = {}
        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        classified_data = self.driver.execute_script("return window.classified;")
        listing_data["property_id"] = classified_data["id"]
        listing_data["locality"] = classified_data["property"]["location"]["locality"]
        listing_data["postal_code"] = classified_data["property"]["location"]["postalCode"]
        listing_data["price"] = classified_data["transaction"]["sale"].get("price", None)
        listing_data["property_type"] = classified_data["property"].get("type", None)
        listing_data["property_subtype"] = classified_data["property"].get("subtype", None)
        listing_data["sale_type"] = classified_data["price"].get("type", None)
        listing_data["number_of_rooms"] = classified_data["property"].get("bedroomCount", None)
        listing_data["living_area"] = classified_data["property"]["livingRoom"].get("surface", None)
        listing_data["equipped_kitchen"] = classified_data["property"]["kitchen"].get("type", None)
        listing_data["furnished"] = 1 if classified_data["transaction"]["sale"]["isFurnished"] else 0
        listing_data["open_fire"] = 1 if classified_data["property"]["fireplaceExists"] else 0
        listing_data["terrace"] = classified_data["property"].get("terraceSurface", None)
        listing_data["garden"] = classified_data["property"].get("gardenSurface", None)
        listing_data["facades"] = classified_data["property"]["building"].get("facadeCount", None)
        listing_data["swimming_pool"] = 1 if classified_data["property"]["hasSwimmingPool"] else 0
        listing_data["state_of_building"] = classified_data["property"]["building"].get("condition", None)

        self.listings.append(listing_data)

    def save_to_csv(self):
        df = pd.DataFrame(self.listings)
        df.to_csv("data.csv", index=False)