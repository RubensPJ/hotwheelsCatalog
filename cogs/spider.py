# -*- coding: utf-8 -*-
# Yeshua
import warnings
warnings.filterwarnings("ignore")
import subprocess
import logging
import pandas as pd
import re
from collections import OrderedDict

# local modules
import writer
import spider_configs
from customized_print import *
import showme
import html_handler
import time_controler as runtime
import search_engine as google

import sys
from twisted.internet import selectreactor

# Use SelectReactor para evitar problemas com AsyncioSelectorReactor
selectreactor.install()

# Dependencies
subprocess.check_call(["pip", "install", "-r", "../requirements.txt", "--quiet"])

# Stop the log on scrapy
logging.getLogger('scrapy').propagate = False

car_name_input = google.match_car_name(input("| Type the car name: "))

# Capturing the car name for practical testing before I build the website that will use a search textbox 
URL = spider_configs.MAINSITE.format(car=car_name_input)
print(URL)

import scrapy
from scrapy.crawler import CrawlerProcess

# Crawler Classe
class MySpider(scrapy.Spider):

    name = 'hotwheels-list'

    def start_requests(self):
        yield scrapy.Request(url=URL, callback=self.parse)

    # Parse function to collect data and store it on a csv
    def parse(self, response):
        printit(self.crawler.settings.get("start_urls")[0])
        start_urls = self.crawler.settings.get("start_urls")[0]
        printit(f"Searching over {start_urls}")

        # decode downloaded html into utf-8
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')
        if 'text/html' in content_type:
            html_content = response.body.decode('utf-8')

        car_models = pd.read_html(html_content)

        # Selector for all rows in the table
        rows = response.css('.wikitable tbody tr')
        if len(rows) == 0:
            rows = response.css('.fandom-table tbody tr')
        # Initialize a list to store the links of the second <a> element in each row
        images = []

        # Iterate through the table rows
        for row in rows[1:]:
            # Select the second <a> element in each row and extract the 'href'
            link = row.css('td:nth-child(4) a::attr(href)').get()
            if link:
                images.append(link)

        printit(images)

        # Getting links from model pages in table
        img_links = html_handler.get_pages_list(start_urls)
        
        
        for table in img_links:
            html_handler.get_pages_list(table)

        # Dumping the data into the dataframe
        car_models[0]['Photo'] = images
        car_models[0]['Links'] = img_links

        new_links_df = pd.DataFrame([spider_configs.WIKIPATH + links for links in car_models[0]['Links']])

        # Creates an object called cars {'model':['car_model_1_dataFrame']} passing dataFrame with names and an altered dataFrame with 
        # the initial http main url. 
        cars = html_handler. in _list(car_models[0]['Name'], new_links_df) 

        # Counting the total of cars captured ( Sum of all of the rows in the dataframes )
        total_searched_cars = sum(car.shape[0] for car in cars.values())

        # Output/logging the total amount of each model
        for car, value in cars.items():
            printit(car + ": " + str(value.shape[0]))

        printit(f"Total cars found: {total_searched_cars}")

        # Writes data from the matches list on a csv 
        images.insert(0, "Images")
        writer.to_csv(images, spider_configs.CARS_CSV_PATH)
        
        # adds a column to the cars main table with the image links captured
        writer.to_csv_next_column(spider_configs.CARS_CSV_PATH, img_links, "Links")

        # writing a csv with the main tables
        writer.to_csv(cars.items(), spider_configs.DETAILED_CARS_CSV_PATH)

        # Sending images to the html page
        # html_handler.htmlInsert(images, "album-content")

        # showing the images all together
        showme.images_side_by_side(images)

# Scrapy header config 
settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

# initialization
process = CrawlerProcess(settings={
    "start_urls": [URL]
})

# Adding spider to the process
process.crawl(MySpider)

# Executing the fun
process.start()
