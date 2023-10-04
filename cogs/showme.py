import requests
import matplotlib.pyplot as plt
from math import sqrt, ceil
from io import BytesIO
from PIL import Image
import threading
import logging

import urllib3

# Sets a log file for the debugging matplotlib msgs
matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.ERROR)  # Define o nível de log para DEBUG ou outro nível desejado

log_handler = logging.FileHandler('matplotlib_debug.log')  # Nome do arquivo de log
log_handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s'))
matplotlib_logger.addHandler(log_handler)

# Repeat for Pillow logs
pillow_logger = logging.getLogger('PIL')
pillow_logger.setLevel(logging.ERROR)
pillow_log_handler = logging.FileHandler('pillow_debug.log')
pillow_log_handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s'))
pillow_logger.addHandler(pillow_log_handler)

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.ERROR)  # Define o nível de log para ERROR ou outro nível desejado


def download_image(link:str, image_list:list, index:int):
    """
    Download an image from a link and add it to the list of images
    :param str link: The URL for downloading the image
    :param list[Image] image_list: List where we will append downloaded image
    :param int index: Index in the list that this thread is working on
    """
    try:
        response = requests.get(link)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image_list[index] = image
        else:
            print(f"Failed to retrieve image from link: {link}")
    except Exception as e:
        print(f"Error processing link {link}: {e}")

def images_side_by_side(image_links):
    """
    Downloads and displays images in an automatically determined layout using matplotlib.

    Args:
        image_links (list): A list of image URLs to be displayed.

    Returns:
        None
    """
    num_images = len(image_links)
    cols = int(ceil(sqrt(num_images)))  # Number of columns
    rows = (num_images + cols - 1) // cols  # Number of rows

    gs = plt.GridSpec(rows, cols, width_ratios=[1] * cols, height_ratios=[1] * rows)
    fig = plt.figure(figsize=(cols * 4, rows * 4))

    image_list = [None] * num_images

    threads = []

    for i, link in enumerate(image_links):
        thread = threading.Thread(target=download_image, args=(link, image_list, i))
        thread.start()
        threads.append(thread)

    # for thread in threads:
    #     thread.join()

    [t.join() for t in threads]

    for i, image in enumerate(image_list):
        if image is not None:
            ax = fig.add_subplot(gs[i])
            ax.imshow(image)
            ax.axis("off")

    plt.tight_layout()

    # Fullscreen
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    # Função para sair do modo de tela cheia quando a tecla Esc é pressionada
    def on_key(event):
        if event.key == 'escape':
            plt.close()
    
    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()

