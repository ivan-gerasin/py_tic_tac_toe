import curses


class CursesMainRenderer:

    def __init__(self, screen=None):
        if screen:
            self.screen = screen
        else:
            self.screen = curses.initscr()
        self.main()

    def main(self):
        curses.curs_set(0)
        stdscr = self.screen
        stdscr.clear()

        menu = MainMenu()
        menu.render()

        #stdscr.getkey()

    def term(self):
        screen = self.screen
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()


class MainMenu:
    HEIGHT = 10
    WIDTH = 50
    X_POS = 8
    Y_POS = 1

    def __init__(self):
        self.win = curses.newwin(self.HEIGHT, self.WIDTH, self.Y_POS, self.X_POS)

    def render(self):
        self.win.addstr(0, 0, 'Welcome to Tic-Tac-Toe game!', curses.A_BOLD)
        self.win.addstr(2, 5, 'Start new game')
        self.win.addstr(2, 3, '>')
        self.win.addstr(4, 5, 'Exit')
        self.win.refresh()
        self.win.getkey()

curses.wrapper(CursesMainRenderer)
