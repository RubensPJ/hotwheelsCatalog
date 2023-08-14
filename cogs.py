
import subprocess
import configs
import logging
import pandas as pd
import re
import writer


# Dependencies
subprocess.check_call(["pip", "install", "-r", "requirements.txt", "--quiet"])

# Stop the log on scrapy
logging.getLogger('scrapy').propagate = False

import scrapy
from scrapy.crawler import CrawlerProcess

# Crawler Classe
class MySpider(scrapy.Spider):

    name = 'hotwheels-list'
    start_urls = [configs.MAINSITE]

    # Parse function to collect data and store it on a csv
    def parse(self, response):

        crawler_table = response.css(configs.MAINGTABLE_CSS_CLASS)
        processed_table = pd.read_html(configs.MAINSITE)

        pattern = configs.ONLY_IMAGES_URLS_PATERN
        matches = re.findall(pattern, crawler_table.get())

        matches = [configs.SUFIX_IMG_PATH + m for m in matches if configs.WRONG_IMG_PATERN not in m]

        processed_table[0]['Photo'] = matches

        # Writes data from the matches list on a csv 
        writer.to_csv(matches, "lambos.csv")
                

# Scrapy header config 
settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

# initialization
process = CrawlerProcess(settings)

# Adding spider to the process
process.crawl(MySpider)


# Executing the fun
process.start()
