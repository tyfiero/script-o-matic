#!/usr/bin/env python3
import argparse
import json
import sys
import random
import unicodedata
# Import the emoji library for handling emojis
try:
    import emoji
except ImportError:
    print("The 'emoji' library is not installed. Please install it using 'pip install emoji'.")
    sys.exit(1)
def load_emoji_mapping(mapping_file=None):
    """
    Load the emoji mapping from a file or use default mapping.
    """
    default_mapping = {
        'a': '🍎', 'b': '🍌', 'c': '🍪', 'd': '🍩', 'e': '🥚', 'f': '🍟', 'g': '🍇', 'h': '🍯',
        'i': '🍦', 'j': '🥙', 'k': '🥝', 'l': '🍋', 'm': '🍄', 'n': '🥜', 'o': '🍊', 'p': '🍑',
        'q': '🥐', 'r': '🌹', 's': '🍓', 't': '🌳', 'u': '☂️', 'v': '🍅', 'w': '🌊', 'x': '❌',
        'y': '🧸', 'z': '🦓', ' ': '  '
    }
    if mapping_file:
        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                custom_mapping = json.load(f)
            # Merge custom mapping with default, prioritizing custom
            default_mapping.update(custom_mapping)
        except json.JSONDecodeError:
            print(f"Error: The mapping file {mapping_file} is not a valid JSON file.")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The mapping file {mapping_file} was not found.")
            sys.exit(1)
    return default_mapping
def text_to_emoji_art(input_string, emoji_mapping):
    """
    Convert input string to emoji art.
    """
    emoji_art = ""
    for char in input_string.lower():
        if char in emoji_mapping:
            emoji_art += emoji_mapping[char]
        else:
            emoji_art += char  # Keep original character if no mapping found
    return emoji_art
def save_to_file(emoji_art, output_file):
    """
    Save the emoji art to a text file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(emoji_art)
        print(f"Emoji art saved to {output_file}")
    except IOError as e:
        print(f"Error saving to file: {e}")
def display_in_console(emoji_art):
    """
    Display the emoji art in the console.
    """
    print("\nYour Emoji Art:")
    print(emoji_art)
def generate_random_art(length=10):
    """
    Generate random emoji art.
    """
    emojis = list(emoji.EMOJI_DATA.keys())
    return ''.join(random.choice(emojis) for _ in range(length))
def main():
    parser = argparse.ArgumentParser(
        description="Emoji Art Generator: Convert text to emoji art!",
        epilog="""
How to use:
1. Basic usage: python emoji_art_generator.py "Your text here"
2. Use custom mapping: python emoji_art_generator.py "Your text" --mapping_file custom_map.json
3. Save to file: python emoji_art_generator.py "Your text" --output_file art.txt
4. Generate random art: python emoji_art_generator.py --random
Enjoy creating colorful emoji art!
        """
    )
    parser.add_argument('input_string', nargs='?', help='The text to convert into emoji art')
    parser.add_argument('--mapping_file', help='Path to a JSON file containing custom character-emoji mappings')
    parser.add_argument('--output_file', help='Path to save the emoji art as a text file')
    parser.add_argument('--no_console', action='store_true', help='Do not display the output in the console')
    parser.add_argument('--random', action='store_true', help='Generate random emoji art')
    parser.add_argument('--length', type=int, default=10, help='Length of random emoji art (default: 10)')
    args = parser.parse_args()
    # Check if neither input_string nor --random is provided
    if not args.input_string and not args.random:
        parser.print_help()
        sys.exit(1)
    emoji_mapping = load_emoji_mapping(args.mapping_file)
    if args.random:
        emoji_art = generate_random_art(args.length)
    else:
        emoji_art = text_to_emoji_art(args.input_string, emoji_mapping)
    if not args.no_console:
        display_in_console(emoji_art)
    if args.output_file:
        save_to_file(emoji_art, args.output_file)
if __name__ == "__main__":
    main()