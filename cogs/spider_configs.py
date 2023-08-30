
# paths
DATA_PATH = "../data/"
CARS_CSV_PATH = "mainCars.csv"
DETAILED_CARS_CSV_PATH = "models.csv"
DATETIME_EXEC_PATH = "datetime_exec_control_file.txt"
# pickle dataframe files


# main site to scrape from (must be wiki)
MAINSITE = 'https://hotwheels.fandom.com/wiki/{car}'
WIKIPATH = 'https://hotwheels.fandom.com'
MAINGTABLE_CSS_CLASS = ".wikitable"
IMGS_CSS_PATH = "table a"
SUBTABLE_CLASS = "wikitable sortable article-table jquery-tablesorter"
DADOS_TABELA = {'date':1,'name':3, 'img':13}
SUFIX_IMG_PATH = "https://static.wikia.nocookie.net/hotwheels/images/"
WRONG_IMG_PATERN = "scale-to-width-down"

# REGEXES
SCALE_PATERN = r'scale-to-width-down\d+'
ONLY_IMAGES_URLS_PATERN = r'https://static.wikia.nocookie.net/hotwheels/images/([^"]+)'