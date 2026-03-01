import curses


class CliInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.selected_index = 0

    def _print(self, row, col, string, attr=curses.A_NORMAL):
        self.stdscr.addstr(row, col, string, attr)

    def _get_key(self):
        key = self.stdscr.getkey()
        return key

    # select using 0-9 and j, k, h, l
    def get_choice(self, choices):
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
                self.selected_index += 1
            elif ch == 'k':
                if self.selected_index > 0:
                    self.selected_index -= 1
            elif ch == '\n':
                choice_index = page_index * choices_per_page + self.selected_index
                return choices[choice_index]
            elif ch.isnumeric():
                choice_index = page_index * choices_per_page + int(ch)
                return choices[choice_index]
            else:
                self.show_lines("Unknown character:", ch)
            

    def _show_choice_page(self, choices, choices_per_page, page_index, page_max_index):
        self.stdscr.clear()
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
            choice = choices[choice_index]
            self._print(i, 0, f"{i}: {choice}", attr)

        if page_max_index > 0:
            self._print(choices_per_page, 0,
                        f"Page {page_index + 1} of {page_max_index + 1}")

    def show_lines(self, *lines):
        self.stdscr.clear()
        row = 0
        for line in lines:
            self._print(row, 0, line)
            row += 1
        self._print(row, 0, "Press any character to continue")
        key = self._get_key()
