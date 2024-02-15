import os
import logging
from _datetime import datetime
from io import BytesIO

from PIL import Image

# Configure logging
log_file = f"log_{datetime.now().strftime('%Y-%m-%d')}.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')


def calculate_histogram(image):
    """
    Calculate the color histogram of an image.

    Args:
    - image: A PIL Image object.

    Returns:
    - A dictionary where keys are color tuples (R, G, B) and values are the corresponding frequencies.
    """
    pixels = list(image.getdata())
    histogram = {}
    for pixel in pixels:
        histogram[pixel] = histogram.get(pixel, 0) + 1
    return histogram


def group_colors_by_similarity(color_values, base_color, histogram, threshold=7):
    total_frequency = 0
    for color in color_values:
        if all(abs(color[i] - base_color[i]) <= threshold for i in range(3)):
            total_frequency += histogram.get(color, 0)
    return base_color, total_frequency


def detect_background_color(histogram, base_color, total_frequency):
    highest_frequency_color = max(histogram, key=histogram.get)
    if highest_frequency_color == base_color or total_frequency > histogram[highest_frequency_color]:
        return "white"
    else:
        return "not white"


def is_white(file):
    """
    Determines if an image is "white" based on its background color and dominant colors.

    Args:
        file (file): File-like object containing the image data.

    Returns:
        bool: True if the image is considered white, False otherwise.
    """
    image = Image.open(BytesIO(file.read()))
    # image.verify()  # Verify it's not a corrupt JPEG
    histogram = calculate_histogram(image)
    base_white = (255, 255, 255)
    colors_to_group = [(r, g, b) for r in range(240, 256) for g in range(240, 256) for b in range(240, 256)]
    base_color, total_frequency = group_colors_by_similarity(colors_to_group, base_white, histogram, threshold=7)
    background_color = detect_background_color(histogram, base_white, total_frequency)
    print(f"The background color is {background_color}.")

    sorted_colors = sorted(histogram.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 Colors Detected:")
    for color, frequency in sorted_colors:
        print(f"Color: {color}, Frequency: {frequency}")
    if background_color == 'white':
        return True
    return False


# if __name__ == "__main__":
#     directory_path = 'BIOMETRICS/GOOD2/'
#     for filename in os.listdir(directory_path):
#         file_path = os.path.join(directory_path, filename)
#         if os.path.isfile(file_path):
#             print(f'\nchecking {file_path}')
#             is_white(file_path)
