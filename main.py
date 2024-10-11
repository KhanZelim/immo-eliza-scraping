from scraper.scraper import ImmowebScraper
import asyncio
import os

async def main():
    scraper = ImmowebScraper()

    await scraper.scrape_links_async()

    for file in os.listdir("data/filtered_links"):
        file_path = os.path.join("data/filtered_links", file)

        with open(file_path, "r") as links_file:
            links = links_file.readlines()

        for link in links:
            await scraper.get_data_async(link)
            
    await scraper.save_to_csv_async()
    scraper.close_driver()

asyncio.run(main())