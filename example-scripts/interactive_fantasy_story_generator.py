#!/usr/bin/env python3
import argparse
import json
import random
import sys
import time
from typing import Dict, List, Tuple
# Third-party imports
import colorama
from colorama import Fore, Style
# Initialize colorama for cross-platform colored terminal text
colorama.init(autoreset=True)
class Character:
    """Represents the main character in the story."""
    def __init__(self, name: str, background: str, skills: List[str]):
        self.name = name
        self.background = background
        self.skills = skills
        self.inventory = []
        self.health = 100
class StoryNode:
    """Represents a single node in the story graph."""
    def __init__(self, text: str, choices: List[Tuple[str, 'StoryNode']] = None):
        self.text = text
        self.choices = choices if choices else []
class InteractiveStory:
    """Manages the interactive story, including state and progression."""
    def __init__(self, character: Character, theme: str):
        self.character = character
        self.theme = theme
        self.current_node = self._create_story_graph()
        self.story_log = []
    def _create_story_graph(self) -> StoryNode:
        """Creates and returns the root node of the story graph."""
        # This is a simplified version. In a full implementation, this would be much more complex.
        root = StoryNode(f"Welcome, {self.character.name}, to a world of {self.theme}!")
        node1 = StoryNode("You find yourself at a crossroads.")
        node2 = StoryNode("You enter a dark forest.")
        node3 = StoryNode("You arrive at a bustling city.")
        root.choices = [
            ("Head towards the mountains", node1),
            ("Enter the dark forest", node2),
            ("Go to the nearby city", node3)
        ]
        return root
    def progress_story(self, choice: int) -> bool:
        """Moves the story forward based on the user's choice."""
        if 0 <= choice < len(self.current_node.choices):
            self.story_log.append((self.current_node.text, choice))
            self.current_node = self.current_node.choices[choice][1]
            return True
        return False
    def get_current_text(self) -> str:
        """Returns the text of the current story node."""
        return self.current_node.text
    def get_current_choices(self) -> List[str]:
        """Returns the available choices at the current story node."""
        return [choice[0] for choice in self.current_node.choices]
    def is_story_end(self) -> bool:
        """Checks if the current node is an end node (has no choices)."""
        return len(self.current_node.choices) == 0
    def to_dict(self) -> Dict:
        """Converts the current story state to a dictionary for saving."""
        return {
            "character": self.character.__dict__,
            "theme": self.theme,
            "story_log": self.story_log
        }
    @classmethod
    def from_dict(cls, data: Dict) -> 'InteractiveStory':
        """Creates an InteractiveStory instance from a saved state dictionary."""
        character = Character(data['character']['name'],
                              data['character']['background'],
                              data['character']['skills'])
        character.inventory = data['character']['inventory']
        character.health = data['character']['health']
        story = cls(character, data['theme'])
        story.story_log = data['story_log']
        # Reconstruct the story state
        for _, choice in story.story_log:
            story.progress_story(choice)
        return story
def slow_print(text: str, delay: float = 0.03):
    """Prints text slowly for a more engaging experience."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
def save_story(story: InteractiveStory, filename: str):
    """Saves the current story state to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(story.to_dict(), f)
    print(f"{Fore.GREEN}Story saved successfully to {filename}")
def load_story(filename: str) -> InteractiveStory:
    """Loads a story state from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return InteractiveStory.from_dict(data)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Save file {filename} not found.")
        sys.exit(1)
def create_character() -> Character:
    """Prompts the user to create a character."""
    print(f"{Fore.CYAN}Let's create your character!")
    name = input("What's your character's name? ")
    print("\nChoose your background:")
    backgrounds = ["Noble", "Peasant", "Merchant", "Warrior"]
    for i, bg in enumerate(backgrounds, 1):
        print(f"{i}. {bg}")
    background = backgrounds[int(input("Enter the number of your choice: ")) - 1]
    print("\nChoose your skills (enter numbers separated by spaces):")
    all_skills = ["Swordsmanship", "Archery", "Magic", "Stealth", "Charisma"]
    for i, skill in enumerate(all_skills, 1):
        print(f"{i}. {skill}")
    skills = [all_skills[int(i)-1] for i in input("Enter your choices: ").split()]
    return Character(name, background, skills)
def main():
    parser = argparse.ArgumentParser(description="""
    Interactive Fantasy Story Generator
    This script creates an immersive, interactive fantasy story experience.
    You can create a new character and embark on a unique adventure, or continue a previously saved story.
    How to use:
    1. To start a new story:
       python interactive_fantasy_story_generator.py --new
    2. To load a saved story:
       python interactive_fantasy_story_generator.py --load filename.json
    Enjoy your adventure!
    """)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--new', action='store_true', help='Start a new story')
    group.add_argument('--load', type=str, help='Load a saved story from a JSON file')
    args = parser.parse_args()
    if args.new:
        character = create_character()
        print("\nChoose your story theme:")
        themes = ["High Fantasy", "Dark Fantasy", "Steampunk Fantasy", "Urban Fantasy"]
        for i, theme in enumerate(themes, 1):
            print(f"{i}. {theme}")
        theme = themes[int(input("Enter the number of your choice: ")) - 1]
        story = InteractiveStory(character, theme)
    else:
        story = load_story(args.load)
    print(f"\n{Fore.YELLOW}Welcome to your interactive fantasy adventure!")
    while True:
        slow_print(f"\n{Fore.CYAN}{story.get_current_text()}")
        if story.is_story_end():
            print(f"{Fore.GREEN}Congratulations! You've reached the end of your journey.")
            break
        print(f"\n{Fore.YELLOW}What would you like to do?")
        choices = story.get_current_choices()
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        print(f"{len(choices) + 1}. Save and quit")
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            if choice == len(choices):
                filename = input("Enter a filename to save your story: ")
                save_story(story, filename)
                break
            if not story.progress_story(choice):
                print(f"{Fore.RED}Invalid choice. Please try again.")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.")
    print(f"{Fore.GREEN}Thank you for playing! We hope you enjoyed your adventure.")
if __name__ == "__main__":
    main()