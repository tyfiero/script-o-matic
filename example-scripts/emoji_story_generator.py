import argparse
import random
import emoji
import requests
from textblob import TextBlob
def fetch_words(theme, num_words=50):
    """
    Fetch theme-related words from Datamuse API.
    """
    try:
        response = requests.get(f"https://api.datamuse.com/words?ml={theme}&max={num_words}")
        response.raise_for_status()
        return [word['word'] for word in response.json()]
    except requests.RequestException as e:
        print(f"Error fetching words: {e}")
        return []
def get_themed_emojis(theme, num_emojis):
    """
    Get a list of theme-related emojis.
    """
    # Define emoji sets for different themes
    emoji_themes = {
        'adventure': '🏔️🌋🏕️🧗‍♀️🏄‍♂️🚵‍♀️🏂🧳🗺️🧭🛶🏜️🏞️🌴',
        'romance': '❤️💕💘💖💗💓💑👫💏🌹🍷🎻🌙✨',
        'horror': '👻💀☠️🧟‍♂️🧛‍♀️🦇🕷️🕸️🌚🔪🩸🎃👹👺',
        'sci-fi': '🚀👽🛸🌌🔭🧬🧪⚗️🖥️🤖🧠💻🛰️',
        'fantasy': '🧙‍♀️🧝‍♂️🧚‍♀️🐉🦄🏰🗡️🛡️🧝‍♀️🧜‍♂️🧞‍♀️🔮📜',
        'comedy': '😂🤣😆😅😁🎭🤡🃏🎪🍌🥁🤹‍♀️',
    }
    # Use a default set if theme not found
    theme_emojis = emoji_themes.get(theme.lower(), '😀😃😄😁😆😅😂🤣☺️😊😇')
    return random.sample(theme_emojis, min(num_emojis, len(theme_emojis)))
def generate_story(theme, num_emojis):
    """
    Generate a short story based on the theme and number of emojis.
    """
    # Fetch theme-related words
    words = fetch_words(theme)
    if not words:
        return "Unable to generate story due to lack of theme-related words."
    # Get themed emojis
    story_emojis = get_themed_emojis(theme, num_emojis)
    # Generate story
    story = f"A {theme} tale begins... "
    for e in story_emojis:
        emoji_name = emoji.demojize(e).replace(":", "").replace("_", " ")
        related_word = random.choice(words)
        sentence = TextBlob(f"The {emoji_name} {related_word}.")
        story += f"{e} {sentence.correct()} "
    return story.strip()
def main():
    parser = argparse.ArgumentParser(description="""
    Emoji Story Generator: Create captivating short stories with emojis!
    This script generates creative short stories based on a specified number of
    randomly selected emojis, chosen from a predefined list organized by themes or genres.
    How to use:
    1. Specify the number of emojis you want in your story (--num_emojis).
    2. Choose a theme for your story (--theme).
    3. Run the script and enjoy your emoji-filled narrative!
    Example:
    python emoji_story_generator.py --num_emojis 5 --theme adventure
    """)
    parser.add_argument('--num_emojis', type=int, default=5, help='Number of emojis to use in the story')
    parser.add_argument('--theme', type=str, default='adventure', help='Theme or genre of the story (e.g., adventure, romance, horror)')
    args = parser.parse_args()
    try:
        story = generate_story(args.theme, args.num_emojis)
        print("\nYour Emoji Story:")
        print(story)
    except Exception as e:
        print(f"An error occurred while generating the story: {e}")
if __name__ == "__main__":
    main()