import os
import argparse
from pathlib import Path
def count_files(directory, file_extension=None):
    """
    Count the number of files in a given directory, optionally filtering by file extension.
    Args:
        directory (str): The path to the directory to count files in.
        file_extension (str, optional): The file extension to filter by (e.g., '.py', '.txt'). Default is None, which counts all files.
    Returns:
        int: The number of files in the directory, optionally filtered by file extension.
    """
    try:
        if file_extension:
            return sum(1 for _ in directory.glob(f'*{file_extension}'))
        else:
            return sum(1 for _ in directory.glob('*'))
    except (OSError, PermissionError) as e:
        print(f"Error: {e}")
        return None
def main():
    """
    The main function that parses command-line arguments and runs the file counting logic.
    """
    parser = argparse.ArgumentParser(description="A script to count the number of files in a directory.",
                                     epilog="How to use:\n"
                                           "1. Run the script without any arguments to count files in your desktop directory.\n"
                                           "2. Use the --path argument to specify a different directory.\n"
                                           "3. Use the --extension argument to filter files by a specific file extension.")
    parser.add_argument("--path", type=str, default=str(Path.home() / "Desktop"), help="The path to the directory to count files in. Default is the user's desktop.")
    parser.add_argument("--extension", type=str, help="The file extension to filter by (e.g., '.py', '.txt'). Default is None, which counts all files.")
    args = parser.parse_args()
    directory = Path(args.path)
    if not directory.exists():
        print(f"Error: The specified path '{args.path}' does not exist.")
        return
    total_files = count_files(directory, args.extension)
    if total_files is not None:
        if args.extension:
            print(f"Number of files with the '{args.extension}' extension: {total_files}")
        else:
            print(f"Total number of files: {total_files}")
if __name__ == "__main__":
    main()