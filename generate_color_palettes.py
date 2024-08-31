import argparse
import random
import colorsys
# Function to convert RGB to HEX
def rgb_to_hex(r, g, b):
    """Converts RGB values to HEX format."""
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))
# Function to generate a random base color
def generate_base_color():
    """Generates a random base color in RGB."""
    return random.random(), random.random(), random.random()
# Function to generate a complementary color palette
def generate_complementary_palette(base_color):
    """Generates a complementary color palette from a base color."""
    r, g, b = base_color
    complementary_color = (1 - r, 1 - g, 1 - b)
    return [rgb_to_hex(*base_color), rgb_to_hex(*complementary_color)]
# Function to generate an analogous color palette
def generate_analogous_palette(base_color):
    """Generates an analogous color palette from a base color."""
    h, l, s = colorsys.rgb_to_hls(*base_color)
    analogous_colors = [
        colorsys.hls_to_rgb((h + 0.1) % 1, l, s),
        colorsys.hls_to_rgb((h - 0.1) % 1, l, s)
    ]
    return [rgb_to_hex(*base_color)] + [rgb_to_hex(*color) for color in analogous_colors]
# Function to generate a triadic color palette
def generate_triadic_palette(base_color):
    """Generates a triadic color palette from a base color."""
    h, l, s = colorsys.rgb_to_hls(*base_color)
    triadic_colors = [
        colorsys.hls_to_rgb((h + 1/3) % 1, l, s),
        colorsys.hls_to_rgb((h + 2/3) % 1, l, s)
    ]
    return [rgb_to_hex(*base_color)] + [rgb_to_hex(*color) for color in triadic_colors]
# Main function to generate color palettes
def generate_color_palettes(number_of_palettes, color_scheme_type):
    """Generates the specified number of color palettes based on the chosen scheme."""
    palettes = []
    for _ in range(number_of_palettes):
        base_color = generate_base_color()
        if color_scheme_type == "complementary":
            palette = generate_complementary_palette(base_color)
        elif color_scheme_type == "analogous":
            palette = generate_analogous_palette(base_color)
        elif color_scheme_type == "triadic":
            palette = generate_triadic_palette(base_color)
        else:
            raise ValueError("Invalid color scheme type. Choose from 'complementary', 'analogous', or 'triadic'.")
        palettes.append(palette)
    return palettes
# Main entry point of the script
def main():
    # Setting up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate artistic color palettes by blending complementary, analogous, or triadic colors. Use this script to create unique palettes for digital art.")
    parser.add_argument("number_of_palettes", type=int, help="The number of color palettes to generate.")
    parser.add_argument("color_scheme_type", choices=["complementary", "analogous", "triadic"], help="The type of color scheme to use: 'complementary', 'analogous', or 'triadic'.")
    # Parsing arguments
    args = parser.parse_args()
    try:
        # Generating the color palettes
        palettes = generate_color_palettes(args.number_of_palettes, args.color_scheme_type)
        # Displaying the generated palettes
        for i, palette in enumerate(palettes, start=1):
            print(f"Palette {i}: {', '.join(palette)}")
    except ValueError as e:
        # Handling invalid color scheme type
        print(f"Error: {e}")
    except Exception as e:
        # Handling any other unexpected errors
        print(f"An unexpected error occurred: {e}")
# Ensures the script runs only when executed directly
if __name__ == "__main__":
    main()