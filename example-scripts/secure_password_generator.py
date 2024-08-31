import argparse
import string
import random
# Define the character sets
LOWERCASE_CHARS = string.ascii_lowercase
UPPERCASE_CHARS = string.ascii_uppercase
DIGIT_CHARS = string.digits
SPECIAL_CHARS = string.punctuation
# Create the parser
parser = argparse.ArgumentParser(
    prog="secure_password_generator",
    description="This script generates secure, random passwords based on user specifications.",
    epilog="""
    How to use:
    1. Run the script: 'python secure_password_generator.py'
    2. Specify the desired password length using the '--length' flag (e.g., '--length 12')
    3. Optionally, include or exclude specific character types using the '--include' and '--exclude' flags (e.g., '--include d,s' to include digits and special characters)
    4. The generated password will be printed to the console.
    """,
)
parser.add_argument("--length", type=int, default=8, help="Specify the desired password length (default: 8)")
parser.add_argument(
    "--include",
    metavar="chars",
    help="Include specific character types: l (lowercase), u (uppercase), d (digits), s (special)",
)
parser.add_argument(
    "--exclude",
    metavar="chars",
    help="Exclude specific character types: l (lowercase), u (uppercase), d (digits), s (special)",
)
# Define the character type mapping
CHAR_TYPE_MAP = {
    "l": LOWERCASE_CHARS,
    "u": UPPERCASE_CHARS,
    "d": DIGIT_CHARS,
    "s": SPECIAL_CHARS,
}
# Function to generate the password
def generate_password(length, include_chars, exclude_chars):
    """
    Generate a random password based on the specified length and character types.
    """
    # Ensure at least one digit and one special character are included
    include_chars += "d" if "d" not in include_chars else ""
    include_chars += "s" if "s" not in include_chars else ""
    # Create the character set by combining the specified character types
    char_set = "".join(CHAR_TYPE_MAP[char_type] for char_type in include_chars if char_type not in exclude_chars)
    # Generate the password by randomly selecting characters from the character set
    password = "".join(random.choice(char_set) for _ in range(length))
    # Shuffle the password for added security
    password = "".join(random.sample(password, len(password)))
    return password
# Parse the command-line arguments
args = parser.parse_args()
# Process the include and exclude character types
include_chars = ""
exclude_chars = ""
if args.include:
    for char_type in args.include.lower():
        if char_type in CHAR_TYPE_MAP:
            include_chars += char_type
        else:
            print(f"Warning: Invalid character type '{char_type}' in --include flag.")
if args.exclude:
    for char_type in args.exclude.lower():
        if char_type in CHAR_TYPE_MAP:
            exclude_chars += char_type
        else:
            print(f"Warning: Invalid character type '{char_type}' in --exclude flag.")
# Generate the password
try:
    password = generate_password(args.length, include_chars, exclude_chars)
    print(f"Generated password: {password}")
except ValueError as e:
    print(f"Error: {e}")