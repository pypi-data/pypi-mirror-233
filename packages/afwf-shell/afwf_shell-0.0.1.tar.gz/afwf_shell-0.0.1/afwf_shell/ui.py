# -*- coding: utf-8 -*-

import typing as T
import readchar

from . import exc
from . import events
from .item import Item
from .render import ConsoleRender
from .debug import debugger


class UI:
    """
    Alfred Workflow UI simulator.

    :param handler:
    """

    def __init__(
        self,
        handler: T.Callable[[str], T.List[Item]],
    ):
        self.handler = handler
        self.render = ConsoleRender()

        # --- query related ---
        self.event_generator = events.KeyEventGenerator()
        self.query_chars = []
        self.query_cursor_offset = 0

        # --- items related ---
        self.items: T.List[Item]
        self.items_mapper: T.Dict[str, "Item"]
        self.selected_item_index: int

        # --- controller flags ---
        self.need_clear_query = True
        self.need_clear_items = True
        self.need_print_query = True
        self.need_print_items = True
        self.need_run_handler = True

    @property
    def query(self) -> str:
        return "".join(self.query_chars)

    def clear_query(self):
        """
        Clear the ``[Query]: {user_query}`` line
        """
        if self.need_clear_query:
            if self.render._position == 1:
                self.render.clear_n_lines(n=1)
        self.need_clear_query = True

    def clear_items(self):
        """
        Clear the item drop down menu.
        """
        if self.need_clear_items:
            if self.render._position > 1:
                self.render.clear_n_lines(n=self.render._position - 1)
        self.need_clear_items = True

    def print_query(self):
        if self.need_print_query:
            self.render.print_line(
                str_tpl="{color}[Query]: {terminal.normal}{query}",
                color=self.render.terminal.blue,
                query=self.query,
                terminal=self.render.terminal,
            )
        self.need_print_query = True

    def print_items(self):
        if self.need_print_items:
            if self.need_run_handler:
                self.items = self.handler(self.query)
                self.items_mapper = {item.uid: item for item in self.items}
                self.selected_item_index = 0
                if self.items:
                    self.items[self.selected_item_index].selected = True
            self.render.print_items(self.items)
        self.need_print_items = True
        self.need_run_handler = True

    def process_key_pressed_input(self, pressed: str):
        debugger.log(f"pressed: {pressed}")
        if pressed == readchar.key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed == readchar.key.TAB:
            item = self.items[self.selected_item_index]
            if item.autocomplete:
                self.query_chars = list(item.autocomplete)

        if pressed == readchar.key.UP:
            self.need_clear_query = False
            self.need_print_query = False
            if len(self.items) == 0 or self.selected_item_index == 0:
                self.need_clear_items = False
                self.need_print_items = False
            else:
                self.need_run_handler = False
                self.items[self.selected_item_index].selected = False
                self.selected_item_index -= 1
                self.items[self.selected_item_index].selected = True
            return

        if pressed == readchar.key.DOWN:
            self.need_clear_query = False
            self.need_print_query = False
            if len(self.items) == 0 or self.selected_item_index == len(self.items) - 1:
                self.need_clear_items = False
                self.need_print_items = False
            else:
                self.need_run_handler = False
                self.items[self.selected_item_index].selected = False
                self.selected_item_index += 1
                self.items[self.selected_item_index].selected = True
            return

        if pressed in (
            readchar.key.LEFT,
            readchar.key.RIGHT,
        ):
            self.need_clear_query = False
            self.need_clear_items = False
            self.need_print_query = False
            self.need_print_items = False
            return

        if pressed == readchar.key.BACKSPACE:
            if self.query_cursor_offset == 0:
                pass
            elif self.query_cursor_offset == len(self.query_chars):
                self.query_chars.pop()
                self.query_cursor_offset -= 1
            else:
                self.query_chars.pop(self.query_cursor_offset)
                self.query_cursor_offset -= 1
            return

        if pressed in (readchar.key.ENTER, readchar.key.CR, readchar.key.LF):
            if len(self.items) == 0:
                raise exc.EndOfInputError(
                    selection="select nothing",
                )
            else:
                self.items[self.selected_item_index].enter_handler()
                raise exc.EndOfInputError(
                    selection=self.items[self.selected_item_index]
                )

        if self.query_cursor_offset == len(self.query_chars):
            self.query_chars.append(pressed)
            self.query_cursor_offset += 1
        else:
            self.query_chars.insert(self.query_cursor_offset, pressed)
            self.query_cursor_offset += 1

    def process_input(self):
        event = self.event_generator.next()
        if isinstance(event, events.KeyPressedEvent):
            self.process_key_pressed_input(pressed=event.value)

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
        except exc.EndOfInputError as e:
            return e.selection

    def run(self):
        try:
            return self._event_loop()
        finally:
            print("")
