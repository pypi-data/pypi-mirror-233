# -*- coding: utf-8 -*-

import typing as T
import readchar

from . import exc
from . import events
from .item import T_ITEM
from .line_editor import LineEditor
from .dropdown import Dropdown
from .render import UIRender
from .debug import debugger


class UI:
    """
    Alfred Workflow UI simulator.

    :param handler: a callable function that takes a query string as input and
        returns a list of items.
    """

    def __init__(
        self,
        handler: T.Callable[[str], T.List[T_ITEM]],
    ):
        self.handler = handler
        self.render = UIRender()
        self.event_generator = events.KeyEventGenerator()

        # --- items related ---
        self.line_editor: LineEditor = LineEditor()
        self.dropdown: Dropdown = Dropdown([])
        self.n_items_on_screen: int = 0

        # --- controller flags ---
        self.need_clear_query = True
        self.need_clear_items = True
        self.need_print_query = True
        self.need_print_items = True
        self.need_run_handler = True

    def clear_query(self):
        """
        Clear the ``[Query]: {user_query}`` line
        """
        if self.need_clear_query:
            if self.render._line_number == 1:
                self.render.clear_n_lines(n=1)
        self.need_clear_query = True

    def clear_items(self):
        """
        Clear the item dropdown menu.
        """
        if self.need_clear_items:
            if self.render._line_number > 1:
                self.render.clear_n_lines(n=self.render._line_number - 1)
        self.need_clear_items = True

    def print_query(self):
        if self.need_print_query:
            self.render.print_line_editor(self.line_editor)
        self.need_print_query = True

    def print_items(self):
        if self.need_print_items:
            if self.need_run_handler:
                items = self.handler(self.line_editor.line)
                self.dropdown.update(items)
            n_items_on_screen = self.render.print_dropdown(self.dropdown)
            self.n_items_on_screen = n_items_on_screen
        self.render.move_cursor_to_line_editor(self.line_editor)
        self.need_print_items = True
        self.need_run_handler = True

    def process_key_pressed_input(self, pressed: str):
        """
        Process user keyboard input.

        - UP: move up
        - DOWN: move down
        - LEFT: move left
        - RIGHT: move right
        - HOME: move to start of the line
        - END: move to end of the line

        - CTRL + E: move up
        - CTRL + D: move down
        - CTRL + R: scroll up
        - CTRL + F: scroll down
        - CTRL + H: move left
        - CTRL + L: move right
        - CTRL + G: move word left
        - CTRL + K: move word right

        - CTRL + X: clear input

        Actions:

        - Enter:
        - CTRL + A:
        - CTRL + W:
        - CTRL + P:
        """
        debugger.log(f"pressed: {[pressed]} {[readchar.key.CTRL_J]}")
        if pressed == readchar.key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed == readchar.key.TAB:
            self.line_editor.clear_line()
            selected_item = self.dropdown.selected_item
            if selected_item.autocomplete:
                self.line_editor.enter_text(selected_item.autocomplete)
            return

        if pressed == readchar.key.CTRL_X:
            self.line_editor.clear_line()
            return

        if pressed in (
            readchar.key.UP,
            readchar.key.DOWN,
            readchar.key.CTRL_E,
            readchar.key.CTRL_D,
            readchar.key.CTRL_R,
            readchar.key.CTRL_F,
        ):
            self.need_clear_query = False
            self.need_print_query = False
            self.need_run_handler = False

            if pressed in (readchar.key.UP, readchar.key.CTRL_E):
                self.dropdown.press_up()
            elif pressed in (readchar.key.DOWN, readchar.key.CTRL_D):
                self.dropdown.press_down()
            elif pressed == readchar.key.CTRL_R:
                self.dropdown.scroll_up()
            elif pressed == readchar.key.CTRL_F:
                self.dropdown.scroll_down()
            else:  # pragma: no cover
                raise NotImplementedError
            return

        if pressed in (
            readchar.key.LEFT,
            readchar.key.RIGHT,
            readchar.key.HOME,
            readchar.key.END,
            readchar.key.CTRL_H,
            readchar.key.CTRL_L,
            readchar.key.CTRL_G,
            readchar.key.CTRL_K,
        ):
            self.need_clear_query = False
            self.need_clear_items = False
            self.need_print_query = False
            self.need_print_items = False
            self.need_run_handler = False
            if pressed in (readchar.key.LEFT, readchar.key.CTRL_H):
                self.line_editor.press_left()
            elif pressed in (readchar.key.RIGHT, readchar.key.CTRL_L):
                self.line_editor.press_right()
            elif pressed == readchar.key.HOME:
                self.line_editor.press_home()
            elif pressed == readchar.key.END:
                self.line_editor.press_end()
            elif pressed == readchar.key.CTRL_G:
                self.line_editor.move_word_backward()
            elif pressed == readchar.key.CTRL_K:
                self.line_editor.move_word_forward()
            else:  # pragma: no cover
                raise NotImplementedError
            return

        if pressed == readchar.key.BACKSPACE:
            self.line_editor.press_backspace()
            return

        if pressed == readchar.key.DELETE:
            self.line_editor.press_delete()
            return

        if pressed in (
            readchar.key.ENTER,
            readchar.key.CR,
            readchar.key.LF,
            readchar.key.CTRL_A,
            readchar.key.CTRL_W,
            readchar.key.CTRL_P,
        ):
            if self.dropdown.n_items == 0:
                raise exc.EndOfInputError(
                    selection="select nothing",
                )
            else:
                self.move_to_end()
                selected_item = self.dropdown.selected_item
                if pressed in (
                    readchar.key.ENTER,
                    readchar.key.CR,
                    readchar.key.LF,
                ):
                    selected_item.enter_handler()
                elif pressed == readchar.key.CTRL_A:
                    selected_item.ctrl_a_handler()
                elif pressed == readchar.key.CTRL_W:
                    selected_item.ctrl_w_handler()
                elif pressed == readchar.key.CTRL_P:
                    selected_item.ctrl_p_handler()
                else:  # pragma: no cover
                    raise NotImplementedError
                raise exc.EndOfInputError(selection=selected_item)

        self.line_editor.press_key(pressed)

    def process_input(self):
        event = self.event_generator.next()
        if isinstance(event, events.KeyPressedEvent):
            self.process_key_pressed_input(pressed=event.value)

    def move_to_end(self):
        self.render.move_to_end(n_items=self.n_items_on_screen)

    def _event_loop(self):
        try:
            while True:
                debugger.log("=== new loop start ===")
                debugger.log("--- clear_items ---")
                self.clear_items()
                debugger.log("--- clear_query ---")
                self.clear_query()
                debugger.log("--- print_query ---")
                self.print_query()
                debugger.log("--- print_items ---")
                self.print_items()
                debugger.log("--- process_input ---")
                self.process_input()
                debugger.log("--- move_to_end ---")
                self.move_to_end()
        except exc.EndOfInputError as e:
            return e.selection
        except Exception as e:

            raise e

    def run(self):
        try:
            return self._event_loop()
        finally:
            print("")
