import requests
import matplotlib.pyplot as plt
from math import sqrt, ceil
from io import BytesIO
from PIL import Image

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

    for i, link in enumerate(image_links):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                ax = fig.add_subplot(gs[i])
                ax.imshow(image)
                ax.axis("off")
            else:
                print(f"Failed to retrieve image from link: {link}")
        except Exception as e:
            print(f"Error processing link {link}: {e}")

    plt.tight_layout()
    plt.show()


# Example usage
# image_links = [
#     "https://static.wikia.nocookie.net/hotwheels/images/b/b5/Image_Not_Available.jpg/revision/latest?cb=20151025125428",
#     "https://static.wikia.nocookie.net/hotwheels/images/8/86/LamborghiniCountachLPI800-4.jpg/revision/latest?cb=20230608133127",
#     "https://static.wikia.nocookie.net/hotwheels/images/8/8f/Premium_1-43_2023_Mix_1_Lamborghini_Countach_LPI_800-4_White_China_HMD49.jpg/revision/latest?cb=20230718212810",
#     "https://static.wikia.nocookie.net/hotwheels/images/2/26/Lamborghini_Urus_red_metallic_2015.JPG/revision/latest?cb=20141201175637",
#     "https://static.wikia.nocookie.net/hotwheels/images/0/04/IMG_0105.jpg/revision/latest?cb=20171222011939"
# ]

# display_images_mosaic(image_links)

# # Exemplo de uso
# image_links = [
#     "https://static.wikia.nocookie.net/hotwheels/images/0/0c/S7300405.JPG/revision/latest?cb=20140608003602",
#     "https://static.wikia.nocookie.net/hotwheels/images/6/6e/Lamborghini_Diablo_RedUH.JPG/revision/latest?cb=20091010222005",
#     "https://static.wikia.nocookie.net/hotwheels/images/b/b2/Lamborghini_Countach_Yel.JPG/revision/latest?cb=20090122230722",
# ]

# images_side_by_side(image_links)
