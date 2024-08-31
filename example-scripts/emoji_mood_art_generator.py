import argparse
import random
import emoji
import json
from typing import Dict, List
from colorama import Fore, Style, init
# Initialize colorama for colored output
init(autoreset=True)
# Define the emoji dictionary
EMOJI_DICT = {
    "happy": ["😊", "😄", "😃", "🌟", "🎉"],
    "sad": ["😢", "😭", "😔", "💔", "🌧️"],
    "nature": ["🌳", "🌻", "🍃", "🦋", "🌈"],
    "love": ["❤️", "😍", "💑", "💖", "🌹"],
    "food": ["🍕", "🍔", "🍟", "🍦", "🍓"],
}
def load_custom_emojis() -> Dict[str, List[str]]:
    """Load custom emojis from a JSON file."""
    try:
        with open("custom_emojis.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_custom_emojis(custom_emojis: Dict[str, List[str]]) -> None:
    """Save custom emojis to a JSON file."""
    with open("custom_emojis.json", "w") as f:
        json.dump(custom_emojis, f)
def add_custom_emoji(theme: str, new_emojis: List[str]) -> None:
    """Add custom emojis to the dictionary."""
    custom_emojis = load_custom_emojis()
    if theme in custom_emojis:
        custom_emojis[theme].extend(new_emojis)
    else:
        custom_emojis[theme] = new_emojis
    save_custom_emojis(custom_emojis)
    print(f"{Fore.GREEN}Custom emojis added successfully!{Style.RESET_ALL}")
def generate_art(theme: str, rows: int, cols: int) -> str:
    """Generate emoji art based on the given theme and dimensions."""
    custom_emojis = load_custom_emojis()
    emojis = EMOJI_DICT.get(theme, []) + custom_emojis.get(theme, [])
    if not emojis:
        raise ValueError(f"No emojis found for the theme '{theme}'")
    art = ""
    for _ in range(rows):
        row = "".join(random.choice(emojis) for _ in range(cols))
        art += row + "\n"
    return art
def main():
    parser = argparse.ArgumentParser(description="""
    Emoji Mood Art Generator
    This script generates emoji art based on a chosen theme or mood. 
    You can specify the dimensions of the art piece and add custom emojis to expand the available themes.
    How to use:
    1. Generate art: python emoji_mood_art_generator.py generate happy 5 10
    2. Add custom emojis: python emoji_mood_art_generator.py add_emoji party 🎈 🕺 💃
    """)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # Generate art command
    generate_parser = subparsers.add_parser("generate", help="Generate emoji art")
    generate_parser.add_argument("theme", help="Theme or mood for the art")
    generate_parser.add_argument("rows", type=int, help="Number of rows in the art")
    generate_parser.add_argument("cols", type=int, help="Number of columns in the art")
    # Add custom emoji command
    add_emoji_parser = subparsers.add_parser("add_emoji", help="Add custom emojis")
    add_emoji_parser.add_argument("theme", help="Theme or mood for the custom emojis")
    add_emoji_parser.add_argument("emojis", nargs="+", help="Custom emojis to add")
    args = parser.parse_args()
    if args.command == "generate":
        try:
            art = generate_art(args.theme, args.rows, args.cols)
            print(f"\n{Fore.CYAN}Emoji Mood Art for '{args.theme}':{Style.RESET_ALL}\n")
            print(emoji.emojize(art))
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    elif args.command == "add_emoji":
        add_custom_emoji(args.theme, args.emojis)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()