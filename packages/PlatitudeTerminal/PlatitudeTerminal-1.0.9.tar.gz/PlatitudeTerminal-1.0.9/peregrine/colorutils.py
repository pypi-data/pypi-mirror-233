from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import PromptSession

class ColorSelector:
    def __init__(self, items):
        self.items = items
        self.selected = 0

    def __str__(self):
        result = ""
        for idx, item in enumerate(self.items):
            if idx == self.selected:
                result += f"<ansiblue>{item}</ansiblue>"
            else:
                result += item
            result += " "
        return result

    def move_left(self):
        self.selected = max(0, self.selected - 1)

    def move_right(self):
        self.selected = min(len(self.items) - 1, self.selected + 1)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'