from PIL import Image


def calculate_histogram(image):
    """
    Calculate the color histogram of an image.

    Args:
    - image: A PIL Image object.

    Returns:
    - A dictionary where keys are color tuples (R, G, B) and values are the corresponding frequencies.
    """
    # Get image data as a list of pixel values
    pixels = list(image.getdata())

    # Initialize histogram dictionary
    histogram = {}

    # Calculate histogram
    for pixel in pixels:
        histogram[pixel] = histogram.get(pixel, 0) + 1

    return histogram


def group_colors_by_similarity(color_values, base_color, threshold=10):
    """
    Group colors based on their similarity to a base color.

    Args:
    - color_values: A list of color tuples (R, G, B) to be grouped.
    - base_color: The base color tuple (R, G, B) for comparison.
    - threshold: The maximum difference allowed between each color channel for two colors to be considered similar.

    Returns:
    - A tuple containing the base color tuple (R, G, B) and the total frequency of similar colors.
    """
    total_frequency = 0
    for color in color_values:
        if all(abs(color[i] - base_color[i]) <= threshold for i in range(3)):
            total_frequency += histogram.get(color, 0)
    return base_color, total_frequency


# Load the image
filename = 'BIOMETRICS/GOOD/OLORUNDARE PRECIOUS TAYE PIC.jpg'
image = Image.open(filename)

# Calculate the color histogram
histogram = calculate_histogram(image)

# Define the base white color
base_white = (255, 255, 255)

# Define the colors to group
colors_to_group = [(r, g, b) for r in range(240, 256) for g in range(240, 256) for b in range(240, 256)]

# Group colors by similarity to white and get the total frequency
base_color, total_frequency = group_colors_by_similarity(colors_to_group, base_white,
                                                         threshold=10)  # Increased threshold

# Check if the total frequency of the base white color is higher than other colors
highest_frequency_color = max(histogram, key=histogram.get)

# Print the result
# if highest_frequency_color == base_white and total_frequency > histogram[highest_frequency_color]:
if highest_frequency_color == base_white or total_frequency > histogram[highest_frequency_color]:
    print("The background color is white.")
else:
    print("The background color is not white.")

# List the top 5 colors detected
sorted_colors = sorted(histogram.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 Colors Detected:")
for color, frequency in sorted_colors:
    print(f"Color: {color}, Frequency: {frequency}")
# print(total_frequency)
# Get the average RGB values of the top 5 colors detected
# top_colors = [color for color, _ in sorted_colors]
# average_color = tuple(int(sum(color[channel] for color in top_colors) / len(top_colors)) for channel in range(3))
#
# # Check if the average color is within the white range
# is_white = all(240 <= value <= 255 for value in average_color)
#
# # Print the result
# if is_white:
#     print("The background color is white.")
# else:
#     print("The background color is not white.")
