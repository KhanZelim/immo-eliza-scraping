from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Firefox()
driver.implicitly_wait(5)

driver.get("https://www.immoweb.be/en/search/apartment/for-sale")

def get_shadow_root(element):
    return driver.execute_script('return arguments[0].shadowRoot', element)

shadow_host = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usercentrics-root")))
cookie_button = get_shadow_root(shadow_host).find_element(By.CSS_SELECTOR, '[data-testid=uc-accept-all-button]')
cookie_button.click()

driver.implicitly_wait(5)

apartment_links = []
apartments = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card__title-link")))
for apartment in apartments:
    apartment_links.append(apartment.get_attribute("href"))
print(apartment_links)

url = apartment_links[0]
listing = driver.get(url)

driver.implicitly_wait(5)
listing_data = {}
listing_data_keys = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "classified-table__header")))
listing_data_values = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "classified-table__data")))
for key, value in zip(listing_data_keys, listing_data_values):
    key_text = key.text
    value_text = value.text
    listing_data[key_text] = value_text
print(listing_data)

df = pd.DataFrame(listing_data)
df.to_csv("data.csv", index=True)