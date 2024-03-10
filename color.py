from colorama import Fore, Back, Style

def indicator(foreground, background, indicate, string):
    """Formats and prints a string with color codes (using colorama library)."""

    print(f"{background}{indicate}{Fore.WHITE}{foreground}{string}{Style.RESET_ALL}", end='')

# Print a red string with a green background and a yellow indicator
indicator(Fore.RED, Back.GREEN, Fore.YELLOW, "This is an error message!")

# Print a blue string on a white background with a magenta indicator
indicator(Fore.BLUE, Back.WHITE, Fore.MAGENTA, "This is informational text.")

# Print a cyan string with no background and no indicator
indicator(Fore.CYAN, None, None, "This is a simple message.")
