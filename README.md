 # Hot Wheels - Collection - Data Scraping

How it's working right now: (There are things to improve, but it's getting there)

![fullscreen](https://github.com/RubensPJ/hotwheelsCatalog/assets/20057755/b32fc1e6-9f6e-4985-beb0-3d085292b3ca)

### Features:
This Python application is designed to collect data from Hot Wheels car thumbnails and offers the following functionalities:

### Thumbnail Download:

Download Hot Wheels car thumbnails directly from the website.

### Table Data Collection:

The application allows you to input the desired car brand name via the terminal.
It collects data from the tables related to the specified car brand on the website.

### Display Data in Tables:

After data collection, the application presents the collected data in a tabular format, making it easy to read.

### Export to CSV File:

The collected data can be exported to a CSV file for further analysis or use in other applications.\

### Image Link Collection:

In addition to table data, the application also collects links to images related to car thumbnails.

### Temporary Image Viewing:

The application temporarily displays the collected images in a window for quick preview.

### Tecs

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
        img_lnks = htmlMng.get_pages
```
