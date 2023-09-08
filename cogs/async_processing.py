import threading
import pandas as pd
import queue

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
