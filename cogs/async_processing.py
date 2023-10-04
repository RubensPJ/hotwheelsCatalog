import threading
import pandas as pd
import queue
import logging
import urllib3

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


# Resto do seu código aqui

def process_link(index, car_link, result_queue, car_names_list):
    try:
        print(f"Searching in link: {car_link[0]}")
        tables = pd.read_html(car_link[0])
        result_queue.put((car_names_list[index], tables[2]))
    except Exception as e:
        print(f'Error while reading table: {e}\nTable not found.')

def process_links_async(call_table_links_list, car_names_list):
    result_queue = queue.Queue()
    threads = []

    for index, car_link in enumerate(call_table_links_list):
        thread = threading.Thread(target=process_link, args=(index, car_link, result_queue, car_names_list))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    [t.join() for t in threads]

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results
