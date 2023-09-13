 # Hot Wheels - collection - Data Scraping

How it's working right now:

![Code_axvQr4O02R](https://github.com/RubensPJ/hotwheelsCatalog/assets/20057755/f6358f32-1615-4961-9735-fda7c51f414a)


This repository contains the code necessary to scrape data from the Hot Wheels Lamborghini wiki page. The code is written in Python and uses the following libraries:

* `scrapy`: A library for scraping web pages.
* `pandas`: A library for data analysis and manipulation.
* `matplotlib`: A library for data visualization.
* `requests`: A library for making HTTP requests.
* `beautifulsoup4`: A library for parsing HTML.

### Step-by-Step Explanation

The code is divided into the following steps:

1. Import the necessary libraries.
2. Define the main function.
3. Define the `MySpider` class.
4. Define the `parse` method.
5. Define the `htmlInsert` function.
6. Define the `get_pages_list` function.
7. Define the `table_list` function.
8. Define the `images_side_by_side` function.
9. Define the `showme` function.
10. Define the `writer` function.
11. Define the `to_csv` function.
12. Define the `to_csv_next_column` function.
13. Run the code.

### Code Snippets

The following code snippets show the key parts of the code:

```python
# Dependencies
subprocess.check_call( ["pip", "install", "-r", "../requirements.txt", "--quiet"] )

# Stop the log on scrapy
logging.getLogger( 'scrapy' ).propagate = False


car_name_input = google.match_car_name( input( "| Type the car name: ") )

URL = spider_configs.MAINSITE.format( car= car_name_input )
print( URL )

import scrapy
from scrapy.crawler import CrawlerProcess

# Crawler Classe
class MySpider( scrapy.Spider ):

    name = 'hotwheels-list'
    # car_name = input( "| Type the car name: " )
    # start_urls =  [spider_configs.MAINSITE.format( car= car_name  )]

    def start_requests( self ):
        yield scrapy.Request(  url=URL, callback=self.parse  )


    # Parse function to collect data and store it on a csv
    def parse( self, response ):

        printit(  self.crawler.settings.get( "start_urls" )[0]  )
        
        start_urls = self.crawler.settings.get( "start_urls" )[0]
        
        printit( f"Searching over {start_urls}" )
        
        # import pdb; pdb.set_trace(  )

        car_models = pd.read_html( start_urls )

        selector = spider_configs.IMAGE_SELECTOR

        # Selector for all rows in the table
        rows = response.css('.wikitable tbody tr')

        # Initialize a list to store the links of the second <a> element in each row
        images = []

        # Iterate through the table rows
        for row in rows[1:]:
            # Select the second <a> element in each row and extract the 'href'
            link = row.css('td:nth-child(4) a::attr(href)').get()
            if link:
                images.append(link)

        printit( images )

        # import pdb; pdb.set_trace()
        # Getting links from model pages in table
        img_links = []
        img_links = html_handler.get_pages_list( start_urls )
        # print( img_links )
        

        # Dumping the data into the dataframe
        car_models[0]['Photo'] = images
        car_models[0]['Links'] = img_links

        # print( car_models[0] )
        new_links_df = pd.DataFrame( [ spider_configs.WIKIPATH + links for links in car_models[0]['Links'] ] )

        # Creates an object called cars {'model':['car_model_1_dataFrame']} passing dataFrame with names and an altered dataFrame with 
        # the initial http main url. 
        cars = html_handler.table_list( 
            car_models[0]['Name'], 
            new_links_df
             ) 

        # Counting the total of cars captured ( Sum of all of the rows in the dataframes )
        total_searched_cars = sum(  car.shape[0] for car in cars.values(  )  )
        

        # Output/logging the total amount of each model
        for car, value in cars.items(  ):
            printit(  car+ ": "+ str(value.shape[0])  )


        printit( f"Total cars found: {total_searched_cars}" )

        # Writes data from the matches list on a csv 
        images.insert( 0, "Images" )
        writer.to_csv( images,spider_configs.CARS_CSV_PATH )
        
        # adds a column to the cars main table with the image links captured
        writer.to_csv_next_column( spider_configs.CARS_CSV_PATH, img_links, "Links" )

        # writing a csv with the main tables
        writer.to_csv( cars.items(  ),spider_configs.DETAILED_CARS_CSV_PATH )
        
        # Sending images to the html page
        # htmlMng.htmlInsert( images, "album-content" )

        # showing the images all together
        showme.images_side_by_side( images )
```
