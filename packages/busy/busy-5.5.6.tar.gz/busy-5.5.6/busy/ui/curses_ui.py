# A terminal-based UI uses Curses, which offers one-key access to most common
# operations.


import curses
from argparse import Namespace
from string import capwords
from time import sleep
from textwrap import wrap

from punkeditor.editbox import EditBox

from busy.ui.ui import Chooser, Prompt, TerminalUI, UserCancelError
from busy.model.collection import Collection


# Set the number of columns to be centered
FIX_WIDTH = 72


def crop(value, width):  # pragma: nocover
    if len(value) > width:
        return value[0:width - 3] + "..."
    else:
        return value


class WindowMaker:  # pragma: nocover
    """Works with curses globals so only instantiate it once"""

    DARK = 8
    LIGHT = 9
    WIDTH = 72
    color_pair = 0

    def __init__(self, fullwin):
        self.fullwin = fullwin
        self.h, oldw = fullwin.getmaxyx()
        self.x, self.w = int((oldw - self.WIDTH) / 2), self.WIDTH
        curses.init_color(self.LIGHT, 700, 700, 700)
        curses.init_color(self.DARK, 200, 200, 200)

        # Color pair for dark-on-light
        self.increment_color_pair()
        curses.init_pair(self.color_pair, self.LIGHT, self.DARK)
        self.default_color_pair = curses.color_pair(self.color_pair)

        # Color pair for action
        self.increment_color_pair()
        curses.init_pair(self.color_pair, curses.COLOR_GREEN, self.DARK)
        self.action_color_pair = curses.color_pair(self.color_pair)

        # Background region
        bkwin = fullwin.subwin(self.h, self.w+2, 0, self.x-1)
        bkwin.bkgd(" ", self.default_color_pair)
        bkwin.clear()
        bkwin.refresh()

    @classmethod
    def increment_color_pair(cls):
        cls.color_pair += 1

    def subwindow(self, h, y, color=None, border=False) -> curses.window:
        h = (self.h + h) if (h < 0) else h
        y = (self.h + y) if (y < 0) else y
        win = self.fullwin.subwin(h, self.w, y, self.x)
        self.increment_color_pair()
        if color is None:
            win.bkgd(" ", self.default_color_pair)
        else:
            curses.init_pair(self.color_pair, color, self.DARK)
            win.bkgd(" ", curses.color_pair(self.color_pair))
        if border:
            win.border()
            win.refresh()
            iwin = win.subwin(h-2, self.w-2, y+1, self.x+1)
            return iwin
        else:
            return win


class CursesError(Exception):
    pass


class CursesUI(TerminalUI):  # pragma: nocover

    name = "curses"

    def start(self):
        self._mode = "WORK"
        chooser = Chooser()
        commands = self.handler.get_commands('key')
        scommands = sorted(commands, key=lambda c: c.name)
        for command in scommands:
            chooser.add_choice(
                keys=[command.key],
                words=[command.name],
                action=command
            )
        chooser.add_choice(keys=['q'], words=['quit'])
        self._command_prompt = chooser

        curses.wrapper(self.term_loop)

    def output(self, intro=""):
        """
        Output is a shell operation.
        """
        # maxy, maxx = self._descwin.getmaxyx()
        # x, y = self._descwin.getyx()
        # limit = maxy - y - 1
        # lines = intro.split("\n")
        # self._descwin.addstr('\n'.join(lines[0:limit]))
        # self._descwin.refresh()

    def edit_items(self, collection: Collection, indices):
        """Edit just one item at a time in curses"""
        items = collection.items(indices)
        item = items[0]
        item.description = self.edit_text(item.description)
        collection.changed = True
        return [item]

    def edit_text(self, text):
        win = self._todowin
        win.clear()
        maxy, maxx = win.getmaxyx()
        wrapped = wrap(text, maxx - 1)
        for y in range(min(maxy + 1, len(wrapped))):
          win.move(y, 0)
          win.addstr(wrapped[y])
        win.refresh()
        win.move(0, 0)
        editor = EditBox(win, insert_mode=True)
        newvalue = editor.edit()
        return newvalue.strip()


    def write_prompt(self, prompt):
        """
        Output a chooser prompt with underlines to a window.
        """
        if prompt.intro:
            self._descwin.addstr(prompt.intro + " ")
        if prompt.default:
            self._descwin.addstr(f"[{prompt.default}] ",
                                 self.maker.action_color_pair)
        for choice in prompt.choices:
            if choice.word == prompt.default:
                continue
            pre, it, post = choice.word.partition(choice.key)
            self._descwin.addstr(pre,  self.maker.action_color_pair)
            self._descwin.addstr(it, curses.A_UNDERLINE |
                                 self.maker.action_color_pair)
            self._descwin.addstr(post + " ",  self.maker.action_color_pair)
        self._descwin.refresh()
        # cy, cx = self._descwin.getyx()
        # self._descwin.move(cy, cx)

    # TODO: Use a better editing component
    #
    # NOTE: get_string assumes that everything has been cleared and we are in
    # the right place.

    def get_string(self, intro, default=""):
        prompt = Prompt(intro=intro, default=default)
        self._update()
        self.write_prompt(prompt)
        curses.echo()
        try:
            string = self._descwin.getstr()
        except KeyboardInterrupt:
            raise UserCancelError
        value = string.decode() or default
        curses.noecho()
        self._descwin.clear()
        self._descwin.refresh()
        return value

    def get_option(self, chooser):
        """Get a 1-keystroke choice from the user"""
        self._update()
        self.write_prompt(chooser)
        key = self._get_key()
        self._descwin.clear()
        self._descwin.refresh()
        return chooser.choice_by_key(chr(key))

    def term_loop(self, fullwin):
        self._fullwin = fullwin
        self.maker = WindowMaker(fullwin)
        self._queuewin = self.maker.subwindow(2, 1, curses.COLOR_CYAN)
        self._todowin = self.maker.subwindow(
            4, 3, curses.COLOR_YELLOW, border=True)
        self._descwin = self.maker.subwindow(-11, 8)
        self._statuswin = self.maker.subwindow(2, -2, curses.COLOR_MAGENTA)
        self._set_queue("tasks")
        self._status = "Welcome to Busy!"
        fullwin.refresh()
        while True:
            self.index = max(0, min(len(self.collection) - 1, self.index))
            self._update()
            self._descwin.clear()
            self.write_prompt(self._command_prompt)
            try:
                key = self._get_key()
            except UserCancelError:
                break
            except CursesError:
                sleep(1)
                continue
            if chr(key) == "q":
                break
            elif key == curses.KEY_DOWN:
                self.index += 1
            elif key == curses.KEY_UP:
                self.index -= 1
            else:
                command = self.handler.get_command(
                    'key', chr(key), ui=self, storage=self.handler.storage,
                    queue=self.queue)
                if not command:
                    self._status = f"Invalid command {hex(key)}"
                    continue
                if command.collection_state == 'todo':
                    command.criteria = [self.index+1]
                command_name = capwords(command.name)
                self._descwin.clear()
                try:
                    result = command.execute()
                    self._status = command.status or ""
                    if hasattr(command, 'switch'):
                        self._set_queue(command.switch)
                except UserCancelError:
                    self._status = f"{command_name} command canceled"

    def _set_queue(self, queue):
        self.queue = queue
        self.index = 0

    @property
    def collection(self):
        return self.handler.storage.get_collection(self.queue)

    @property
    def item(self):
        return self.collection[self.index]

    def _update(self):
        self._queuewin.clear()
        self._queuewin.move(0, 0)
        q = capwords(self.queue)
        c = len(self.collection)
        i = self.index + 1 if c else "-"
        self._queuewin.addstr(f"{q} | Todo | {i}/{c}")
        self._queuewin.move(0, FIX_WIDTH-len("Busy"))
        self._queuewin.addstr("Busy")
        self._queuewin.refresh()

        self._todowin.clear()
        if self.collection:
            value = crop(self.item.first, FIX_WIDTH-3)
            self._todowin.move(0, 0)
            self._todowin.addstr(value, curses.A_BOLD)
            if (value := self.item.next):
                self._todowin.move(1, 2)
                self._todowin.addstr('--> ' + crop(value, FIX_WIDTH - 9))
        self._todowin.refresh()

        self._statuswin.clear()
        self._statuswin.move(0, 0)
        self._statuswin.addstr(crop(self._status, FIX_WIDTH))
        self._statuswin.refresh()

    # Convenience method to get one keystroke from the user.
    #

    def _get_key(self):
        try:
            key = self._fullwin.getch()
        except KeyboardInterrupt:
            raise UserCancelError
        except curses.error:
            raise CursesError
        return key
