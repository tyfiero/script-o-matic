#!/usr/bin/env python3
import argparse
import json
import random
import sys
import os
from colorama import init, Fore, Style
# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)
def load_story(config_path):
    """
    Load story configuration from a JSON file.
    """
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Story configuration file not found at {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Invalid JSON in story configuration file")
        sys.exit(1)
def save_progress(story_state, save_file):
    """
    Save current story progress to a file.
    """
    try:
        with open(save_file, 'w') as f:
            json.dump(story_state, f)
        print(f"{Fore.GREEN}Progress saved successfully!")
    except IOError:
        print(f"{Fore.RED}Error: Unable to save progress")
def load_progress(save_file):
    """
    Load saved story progress from a file.
    """
    try:
        with open(save_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.YELLOW}No saved progress found. Starting a new story.")
        return None
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Invalid save file")
        return None
def print_story_text(text):
    """
    Print story text with formatting.
    """
    print(f"\n{Fore.CYAN}{text}{Style.RESET_ALL}\n")
def get_user_choice(choices):
    """
    Prompt user for a choice and validate input.
    """
    while True:
        for i, choice in enumerate(choices, 1):
            print(f"{Fore.YELLOW}{i}. {choice}")
        try:
            choice = int(input(f"\n{Fore.GREEN}Enter your choice (1-{len(choices)}): {Style.RESET_ALL}"))
            if 1 <= choice <= len(choices):
                return choice - 1
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.")
def navigate_story(story, current_node="start", story_state=None):
    """
    Navigate through the story based on user choices.
    """
    if story_state is None:
        story_state = {"path": [], "inventory": []}
    while True:
        node = story["nodes"][current_node]
        print_story_text(node["text"])
        if "item" in node:
            story_state["inventory"].append(node["item"])
            print(f"{Fore.GREEN}You obtained: {node['item']}")
        if "choices" in node:
            choice_index = get_user_choice(node["choices"])
            next_node = node["next"][choice_index]
            story_state["path"].append(next_node)
            current_node = next_node
        elif "ending" in node:
            print_story_text(f"THE END - {node['ending']}")
            break
        else:
            print(f"{Fore.RED}Error: Invalid story node structure")
            break
    return story_state
def main():
    parser = argparse.ArgumentParser(description="""
    Interactive Story Generator
    This script creates an immersive, choice-driven narrative experience.
    Navigate through a branching story by making decisions that affect the plot and lead to various endings.
    How to use:
    1. Prepare a JSON configuration file with your story structure.
    2. Run the script with the path to your configuration file.
    3. Optionally, specify a save file to continue a previous session.
    4. Follow the prompts and make choices to progress through the story.
    Enjoy your unique adventure!
    """)
    parser.add_argument("config", help="Path to the story configuration JSON file")
    parser.add_argument("-s", "--save", help="Path to save/load progress")
    parser.add_argument("-d", "--difficulty", choices=["easy", "medium", "hard"], default="medium", 
                        help="Set the difficulty level of the story (default: medium)")
    args = parser.parse_args()
    story = load_story(args.config)
    # Apply difficulty settings (this is a placeholder - implement as needed)
    if args.difficulty == "easy":
        story["time_limit"] = 300  # example: 5 minutes for easy mode
    elif args.difficulty == "hard":
        story["time_limit"] = 120  # example: 2 minutes for hard mode
    else:
        story["time_limit"] = 180  # example: 3 minutes for medium mode
    story_state = None
    if args.save:
        story_state = load_progress(args.save)
    print(f"{Fore.MAGENTA}Welcome to the Interactive Story Generator!{Style.RESET_ALL}")
    print(f"Difficulty: {args.difficulty}")
    story_state = navigate_story(story, story_state=story_state)
    if args.save:
        save_progress(story_state, args.save)
    print(f"\n{Fore.GREEN}Thanks for playing!{Style.RESET_ALL}")
    print("Your path through the story:")
    print(" -> ".join(story_state["path"]))
    print("\nItems collected:")
    print(", ".join(story_state["inventory"]) if story_state["inventory"] else "None")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Story interrupted. Thanks for playing!")
        sys.exit(0)