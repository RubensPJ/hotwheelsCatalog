import subprocess
import configs
import logging
import pandas as pd
import re

# local modules
import writer
import showme
import htmlMng

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
        car_models = pd.read_html(configs.MAINSITE)

        # Finding right image tags
        pattern = configs.ONLY_IMAGES_URLS_PATERN
        matches = re.findall(pattern, crawler_table.get())

        # clearing the wrong images from the matches
        images = [configs.SUFIX_IMG_PATH + m for m in matches if configs.WRONG_IMG_PATERN not in m]
        
        # Getting links from model pages in table
        img_lnks = []
        img_lnks = htmlMng.get_pages_list(configs.MAINSITE)
        # print(img_lnks)
        
        # Dumping the data into the dataframe
        car_models[0]['Photo'] = images
        car_models[0]['Links'] = img_lnks

        # print(car_models[0])
        new_links_df = pd.DataFrame([ configs.WIKIPATH + links for links in car_models[0]['Links'] ])

        # Creates an object called cars {'model':['car_model_1_dataFrame']} passing dataFrame with names and an altered dataFrame with 
        # the initial http main url. 
        cars = htmlMng.table_list(
            car_models[0]['Name'], 
            new_links_df
            ) 
       
        
        # print(cars)

        # Get data from the car_model table first column 
        # titulos_colunas = car_models.iloc[:,0].tolist()


        # sub_models = pd.DataFrame()

        # Writes data from the matches list on a csv 
        images.insert(0, "Images")
        writer.to_csv(images,configs.LAMBOS_CSV_PATH)
        
        writer.to_csv_next_column(configs.LAMBOS_CSV_PATH, img_lnks, "Links")

        # Sending images to the html page
        # htmlMng.htmlInsert(images, "album-content")

        # showing the images all together
        # showme.images_side_by_side(images)


        
                

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

