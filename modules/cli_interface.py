import curses


class CliInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr

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

    def _get_height(self):
        height, width = self.stdscr.getmaxyx()
        return height - 1

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
        selected_index = 0
        previous_numeric_char = None
        choices = self._normalize_choices(choices)
        choices_per_page = 10 # necessary to be able to have 1 press numeric selection
        page_index = 0
        page_max_index = (len(choices) - 1) // choices_per_page
        while True:
            selected_index = self._show_choice_page(
                choices, choices_per_page, page_index, page_max_index, selected_index)
            ch = self._get_key()
            if ch == 'h':
                if page_index > 0:
                    page_index -= 1
            elif ch == 'l':
                if page_index < page_max_index:
                    page_index += 1
            elif ch == 'j':
                if selected_index < choices_per_page:
                    selected_index += 1
            elif ch == 'k':
                if selected_index > 0:
                    selected_index -= 1
            elif ch == '\n':
                choice_index = page_index * choices_per_page + selected_index
                label, value = choices[choice_index]
                return choice_index, value
            elif ch.isnumeric():
                choice_index = page_index * choices_per_page + int(ch)
                label, value = choices[choice_index]
                return choice_index, value
            elif ch == '?':
                self.show_lines("0-9 - choose using index", "j/k - move selector down/up",
                                "h/l - switch page left/right", "enter - choose using selector")
            elif ch == 'q':
                exit()
            else:
                self._show_lines_page("Unknown character:", ch)

    def _show_choice_page(self, choices, choices_per_page, page_index, page_max_index, selected_index):
        self._clear()
        self._print("Select choice:", curses.A_BOLD)
        for i in range(choices_per_page):
            choice_index = page_index * choices_per_page + i

            if i == choices_per_page - 1:
                # this is not working, but my laptop is running out of battery
                if selected_index > i:
                    selected_index = i

            if choice_index == len(choices):
                break

            if i == selected_index:
                attr = curses.A_STANDOUT
            else:
                attr = curses.A_NORMAL
            label, value = choices[choice_index]
            self._print(f"{i}: {label}", attr)

        if page_max_index > 0:
            self._print(
                f"Page {page_index + 1} of {page_max_index + 1}", curses.A_BOLD)
        return selected_index

    def _get_continue(self):
        self._print("Press any character to continue", curses.A_BOLD)
        key = self._get_key()

    def show_lines(self, lines):
        start_line_index = 0
        lines_per_page = self._get_height()
        while True:
            self._show_lines_page(lines, lines_per_page, start_line_index)
            ch = self._get_key()
            if ch in ['j', 'k', 'u', 'd']:
                match ch:
                    case 'j':
                        dl = 1
                    case 'k':
                        dl = -1
                    case 'd':
                        dl = lines_per_page // 2
                    case 'u':
                        dl = -lines_per_page // 2
                    case _:
                        dl = 0
                start_line_index += dl
                start_line_index = min(lines_per_page - 1, start_line_index)
                start_line_index = max(0, start_line_index)
            elif ch == '\n':
                return
            elif ch == 'q':
                exit()

    def _show_lines_page(self, lines, lines_per_page, start_line_index):
        self._clear()
        for i in range(lines_per_page):
            line_index = start_line_index + i
            if line_index < len(lines):
                self._print(lines[line_index])
