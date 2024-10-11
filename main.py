from scraper.scraper import ImmowebScraper

scraper = ImmowebScraper()

scraper.get_links()
scraper.download_links_async()
scraper.filter_links()

scraper.get_data()
scraper.close_driver()
scraper.save_to_csv()