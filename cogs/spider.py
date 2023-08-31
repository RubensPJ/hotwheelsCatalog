import subprocess
import logging
import pandas as pd
import re

# local modules
import writer
import spider_configs
# import showme
import html_handle
import time_controler as runtime
import search_engine as google

# Dependencies
subprocess.check_call( ["pip", "install", "-r", "../requirements.txt", "--quiet"] )

# Stop the log on scrapy
logging.getLogger( 'scrapy' ).propagate = False

car_name_input = google.match_car_name( input( "| Type the car name: ") )

URL = spider_configs.MAINSITE.format( car= car_name_input )

import scrapy
from scrapy.crawler import CrawlerProcess

# My own print
def printit( *args ):
    print( "|-===================================================-" )
    print( "|" )
    
    print( f"| { ''.join( str( i ) for i in args ) }" )
    print( "|" )

# Crawler Classe
class MySpider( scrapy.Spider ):

    name = 'hotwheels-list'
    # car_name = input( "| Type the car name: " )
    # start_urls =  [spider_configs.MAINSITE.format( car= car_name  )]

    def start_requests( self ):
        yield scrapy.Request(  url=URL, callback=self.parse  )


    # Parse function to collect data and store it on a csv
    def parse( self, response ):
        
        start_urls = self.crawler.settings.get( "start_urls" )[0]
        
        printit( f"Searching over {start_urls}" )
        
        # import pdb; pdb.set_trace(  )

        crawler_table = response.css( spider_configs.MAINGTABLE_CSS_CLASS )
        car_models = pd.read_html( start_urls )

        # Finding right image tags
        pattern = spider_configs.ONLY_IMAGES_URLS_PATERN
        matches = re.findall( pattern, crawler_table.get(  ) )

        # clearing the wrong images from the matches
        images = [spider_configs.SUFIX_IMG_PATH + m for m in matches if spider_configs.WRONG_IMG_PATERN not in m]
        # print( images )
        # Getting links from model pages in table
        img_lnks = []
        img_lnks = html_handle.get_pages_list( start_urls )
        # print( img_lnks )
        

        # Dumping the data into the dataframe
        car_models[0]['Photo'] = images
        car_models[0]['Links'] = img_lnks

        # print( car_models[0] )
        new_links_df = pd.DataFrame( [ spider_configs.WIKIPATH + links for links in car_models[0]['Links'] ] )

        # Creates an object called cars {'model':['car_model_1_dataFrame']} passing dataFrame with names and an altered dataFrame with 
        # the initial http main url. 
        cars = html_handle.table_list( 
            car_models[0]['Name'], 
            new_links_df
             ) 
    
        # print( cars )

        # Counting the total of cars captured ( Sum of all of the rows in the dataframes )
        total_searched_cars = sum(  car.shape[0] for car in cars.values(  )  )
        

        # Output/logging the total amount of each model
        for car, value in cars.items(  ):
            printit(  car, ": ", value.shape[0]  )


        printit( f"Total cars found: {total_searched_cars}" )

        # Writes data from the matches list on a csv 
        images.insert( 0, "Images" )
        writer.to_csv( images,spider_configs.CARS_CSV_PATH )
        
        # adds a column to the cars main table with the image links captured
        writer.to_csv_next_column( spider_configs.CARS_CSV_PATH, img_lnks, "Links" )

        # writing a csv with the main tables
        writer.to_csv( cars.items(  ),spider_configs.DETAILED_CARS_CSV_PATH )

        # Trying to write a pickle dataframe file with the merged dataFrames
        
        # Sending images to the html page
        # htmlMng.htmlInsert( images, "album-content" )

        # showing the images all together
        # showme.images_side_by_side( images )




        
                

# Scrapy header config 
settings = {
    'USER_AGENT': 'Mozilla/5.0 ( Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36 ( KHTML, like Gecko ) Chrome/94.0.4606.81 Safari/537.36'
}

# initialization
process = CrawlerProcess( settings={
    "start_urls": [URL]
} )


# Adding spider to the process
process.crawl( MySpider )

# Executing the fun
process.start(  )

