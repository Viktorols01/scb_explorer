import curses


class CliInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.selected_index = 0

    def _clear(self):
        self.stdscr.clear()

    def _print(self, string, attr=curses.A_NORMAL, row=None, col=None):
        string_and_newline = f"{string}\n"
        if row is None or col is None:
            self.stdscr.addstr(string_and_newline, attr)
        else:
            self.stdscr.addstr(row, col, string_and_newline, attr)

    def _get_key(self):
        key = self.stdscr.getkey()
        return key
    
    def _normalize_choices(self, choices):
        normalized = []

        for choice in choices:
            if isinstance(choice, tuple) and len(choice) == 2:
                label, value = choice
            else:
                label = str(choice)
                value = choice

            normalized.append((label, value))

        return normalized
    
    def get_input(self, message=""):
        curses.echo()  # show typed characters
        self._clear()
        self._print(message, curses.A_BOLD)
        user_input = self.stdscr.getstr().decode("utf-8")
        return user_input

    # select using 0-9 and j, k, h, l
    def get_choice(self, choices):
        choices = self._normalize_choices(choices)
        choices_per_page = 10
        page_index = 0
        page_max_index = (len(choices) - 1) // choices_per_page
        while True:
            self._show_choice_page(
                choices, choices_per_page, page_index, page_max_index)
            ch = self._get_key()
            if ch == 'h':
                if page_index > 0:
                    page_index -= 1
            elif ch == 'l':
                if page_index < page_max_index:
                    page_index += 1
            elif ch == 'j':
                if self.selected_index < choices_per_page:
                    self.selected_index += 1
            elif ch == 'k':
                if self.selected_index > 0:
                    self.selected_index -= 1
            elif ch == '\n':
                choice_index = page_index * choices_per_page + self.selected_index
                label, value = choices[choice_index]
                return choice_index, value
            elif ch.isnumeric():
                choice_index = page_index * choices_per_page + int(ch)
                label, value = choices[choice_index]
                return choice_index, value
            elif ch == '?':
                self.show("0-9 - choose using index", "j/k - move selector down/up", "h/l - switch page left/right", "enter - choose using selector")
            elif ch == 'q':
                exit()
            else:
                self.show("Unknown character:", ch)
            

    def _show_choice_page(self, choices, choices_per_page, page_index, page_max_index):
        self._clear()
        self._print("Select choice:", curses.A_BOLD)
        for i in range(choices_per_page):
            choice_index = page_index * choices_per_page + i

            if choice_index == len(choices) - 1:
                if self.selected_index > i:
                    self.selected_index = i
            if choice_index == len(choices):
                break

            if i == self.selected_index:
                attr = curses.A_STANDOUT
            else:
                attr = curses.A_NORMAL
            label, value = choices[choice_index]
            self._print(f"{i}: {label}", attr)

        if page_max_index > 0:
            self._print(f"Page {page_index + 1} of {page_max_index + 1}", curses.A_BOLD)
    
    def _get_continue(self):
        self._print("Press any character to continue", curses.A_BOLD)
        key = self._get_key()

    def show(self, *objs):
        self._clear()
        for obj in objs:
            self._print(obj)
        self._get_continue()
