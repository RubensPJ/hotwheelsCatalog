import re
import threading
from bs4 import BeautifulSoup
import pandas as pd
import queue
import logging
import requests
import urllib3
from customized_print import *

# Configurar um arquivo de log para as mensagens de depuração do matplotlib
matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.ERROR)  # Define o nível de log para DEBUG ou outro nível desejado
log_handler = logging.FileHandler('matplotlib_debug.log')  # Nome do arquivo de log
log_handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s'))
matplotlib_logger.addHandler(log_handler)

# Repita o mesmo processo para o Pillow (PIL)
pillow_logger = logging.getLogger('PIL')
pillow_logger.setLevel(logging.ERROR)
pillow_log_handler = logging.FileHandler('pillow_debug.log')
pillow_log_handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s'))
pillow_logger.addHandler(pillow_log_handler)
# Desativar os logs de depuração do urllib3
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.ERROR)  # Define o nível de log para ERROR ou outro nível desejado

UNIC_CARS_SELECTOR = "#mw-content-text > div > div.table-wide > div > table > tbody > tr:nth-child(1) > td:nth-child(13) > a > img"
HTML_TABLEROW_LIST_SELECTOR = "#mw-content-text > div > div.table-wide > div > table > tbody > tr"

def get_imgs_from_htmltable(html_links:list):
    import showme
    img_url_pattern = re.compile(r'https://static\.wikia\.nocookie\.net/hotwheels/images/.+?/revision/latest\?cb=\d+')
    car_imgs_list = []

    for index, car_link in enumerate(html_links):
        
        response = requests.get(car_link[0])
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find(name='table', attrs={'class': ['wikitable','sortable','jquery-tablesorter']})
        # print(table)
        
        table_rows = table.find_all(
            name='a', 
            attrs={'href': img_url_pattern, 'class': lambda x: x == 'image'}
            )
        # printit(f"car_link: {car_link}")
        for index, row in enumerate(table_rows):
            car_imgs_list.append(row['href'])
            print(f"Row {index}: {row['href']}")
        # printit(car_imgs_list)
    showme.images_side_by_side( car_imgs_list )

def process_link(index, car_link, result_queue, car_names_list):
    try:

        # get_imgs_from_htmltable(car_link[0])
        
        # printit(f"Searching in link: {car_link[0]}")
        tables = pd.read_html(car_link[0])

        # Supondo que você esteja procurando por uma tabela com um cabeçalho específico
        desired_header = ["Col #", "Year", "Color"]  # Exemplo de cabeçalhos esperados
        # printit("\n\n\n\n\n\n\n")
        # Loop para verificar cada tabela
        for table in tables:
            if all(header in table.columns for header in desired_header):
                # printit(table)
                # Se a tabela contém todos os cabeçalhos desejados, coloque no result_queue
                result_queue.put((car_names_list[index], table))
                break
            
            else:
                # Se o loop terminar sem encontrar a tabela, levante uma exceção ou imprima uma mensagem
                raise ValueError("Tabela desejada não encontrada.")
            
        # printit("\n\n\n\n\n\n\n")
    
    except Exception as e:
        printit(f'Error while reading table: {e}\nTable not found.')

def process_links_async(call_table_links_list, car_names_list):
    result_queue = queue.Queue()
    threads = []

    for index, car_link in enumerate(call_table_links_list):
        thread = threading.Thread(target=process_link, args=(index, car_link, result_queue, car_names_list))
        threads.append(thread)
        thread.start()

    # for thread in threads:
    #     thread.join()

    [t.join() for t in threads]

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results
