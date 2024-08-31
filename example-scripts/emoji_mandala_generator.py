import argparse
from collections import defaultdict
from PIL import Image, ImageDraw, ImageColor
import random
def create_mandala(size, emojis, color_map, output_format):
    """
    Generates an intricate mandala pattern using the specified emojis and colors.
    Args:
        size (int): The dimensions of the mandala (size x size).
        emojis (list): The list of emojis to use in the mandala.
        color_map (dict): A dictionary mapping emojis to their corresponding colors.
        output_format (str): The output format for the mandala ('png' or 'jpg').
    Returns:
        None
    """
    # Create a new image with the specified size
    mandala = Image.new('RGB', (size, size), color=(0, 0, 0))
    draw = ImageDraw.Draw(mandala)
    # Calculate the center of the mandala
    center_x, center_y = size // 2, size // 2
    # Generate the mandala pattern
    for i in range(size):
        for j in range(size):
            # Calculate the distance from the center
            distance = ((i - center_x) ** 2 + (j - center_y) ** 2) ** 0.5
            # Select the emoji based on the distance from the center
            emoji = emojis[int(distance / size * (len(emojis) - 1))]
            # Get the color for the emoji
            color = color_map.get(emoji, (255, 255, 255))
            # Draw the emoji on the mandala
            draw.text((i, j), emoji, font=None, fill=color)
    # Save the mandala as an image
    mandala.save(f'mandala.{output_format}')
    print(f'Mandala saved as mandala.{output_format}')
def main():
    """
    The main function that handles command-line arguments and calls the create_mandala function.
    """
    parser = argparse.ArgumentParser(description='Emoji Mandala Generator')
    parser.add_argument('-s', '--size', type=int, default=20, help='The size of the mandala (default: 20x20)')
    parser.add_argument('-e', '--emojis', nargs='+', required=True, help='The emojis to use in the mandala (e.g., 🌸 🌼 🌈)')
    parser.add_argument('-c', '--colors', nargs='+', type=str, required=True, help='The colors to use for the emojis (e.g., red green blue)')
    parser.add_argument('-f', '--format', choices=['png', 'jpg'], default='png', help='The output format for the mandala (default: png)')
    parser.description += """
    How to use:
    1. Provide a list of emojis you want to use in the mandala.
    2. Provide a list of colors (in RGB format) to map to the emojis.
    3. Choose the size of the mandala (default is 20x20).
    4. Choose the output format (png or jpg).
    5. The script will generate the mandala and save it as an image file in the current directory.
    """
    args = parser.parse_args()
    # Create a color map from the provided colors
    color_map = {emoji: ImageColor.getrgb(color) for emoji, color in zip(args.emojis, args.colors)}
    try:
        create_mandala(args.size, args.emojis, color_map, args.format)
    except Exception as e:
        print(f'Error: {e}')
if __name__ == '__main__':
    main()