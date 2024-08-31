import argparse
import random
from PIL import Image, ImageDraw
# Define a function to generate a random color palette
def generate_color_palette(palette_type):
    # Predefined color palettes
    palettes = {
        'vibrant': ['#FF5733', '#FFBD33', '#75FF33', '#33FF57', '#33FFBD'],
        'pastel': ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF'],
        'monochrome': ['#000000', '#333333', '#666666', '#999999', '#CCCCCC']
    }
    return palettes.get(palette_type, ['#FFFFFF', '#000000'])
# Define a function to create abstract art
def create_abstract_art(args):
    try:
        # Parse the resolution
        width, height = map(int, args.resolution.split('x'))
        # Create a new image with white background
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        # Generate color palette
        color_palette = generate_color_palette(args.color_palette)
        # Generate shapes based on user input
        for _ in range(args.density * 10):
            shape_type = random.choice(args.shapes)
            color = random.choice(color_palette)
            x0 = random.randint(0, width)
            y0 = random.randint(0, height)
            x1 = x0 + random.randint(10, 100)
            y1 = y0 + random.randint(10, 100)
            if shape_type == 'circle':
                draw.ellipse([x0, y0, x1, y1], fill=color, outline=None)
            elif shape_type == 'square':
                draw.rectangle([x0, y0, x1, y1], fill=color, outline=None)
            elif shape_type == 'triangle':
                draw.polygon([x0, y0, (x0 + x1) // 2, y0 - 100, x1, y1], fill=color)
        # Save the generated image
        image.save(args.output_file, format=args.file_format.upper())
        # Log the parameters used
        print(f"Artwork created with parameters: Color Palette - {args.color_palette}, Shapes - {args.shapes}, Density - {args.density}, Resolution - {args.resolution}, Format - {args.file_format}")
    except Exception as e:
        print(f"An error occurred: {e}")
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Abstract Art Generator: Creates unique abstract art pieces using procedural generation techniques.\n\n"
                                                 "How to use:\n"
                                                 "1. Choose a color palette from predefined options or provide your own.\n"
                                                 "2. Select shape types you want to include in the artwork.\n"
                                                 "3. Specify pattern density, resolution, and output file format.\n"
                                                 "4. Run the script with these parameters to generate your artwork.")
    # Define command-line arguments
    parser.add_argument('--color_palette', type=str, default='vibrant', help="Color palette to use (e.g., vibrant, pastel, monochrome)")
    parser.add_argument('--shapes', nargs='+', default=['circle', 'square', 'triangle'], help="Types of shapes to include (e.g., circle, square, triangle)")
    parser.add_argument('--density', type=int, default=5, choices=[1, 2, 3, 4, 5], help="Pattern density (1=low, 5=high)")
    parser.add_argument('--resolution', type=str, default='1920x1080', help="Resolution of the image (e.g., 1920x1080)")
    parser.add_argument('--file_format', type=str, default='PNG', choices=['PNG', 'JPEG'], help="Output file format")
    parser.add_argument('--output_file', type=str, default='abstract_art.png', help="Output file name")
    # Parse the arguments
    args = parser.parse_args()
    # Call the function to create abstract art
    create_abstract_art(args)
# Run the main function
if __name__ == '__main__':
    main()