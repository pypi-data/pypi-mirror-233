# -*- coding: utf-8 -*-

"""

"""

import typing as T
import sys

from blessed import Terminal

if T.TYPE_CHECKING:
    from .item import Item


class ConsoleRender:
    """
    low level console render class.
    """

    def __init__(self):
        # blessed terminal
        self.terminal = Terminal()
        # _previous_error stores the last error object
        self._previous_error = None
        # _position stores the current line number position of the cursor
        self._position = 0

    def print_str(
        self,
        str_tpl: str,
        new_line=False,
        **kwargs,
    ):
        """
        打印一个字符串, 可以选择是否换行.

        :param str_tpl: string template, 一个字符串模板.
        :param new_line: 如果是 True, 那么会自动换行, 否则不会. 默认不会.
        :param kwargs: 额外的传递给 str_tpl 的参数.
        """
        if new_line:
            self._position += 1
        print(str_tpl.format(t=self.terminal, **kwargs), end="\n" if new_line else "")
        sys.stdout.flush()

    def print_line(
        self,
        str_tpl: str,
        new_line: bool = True,
        **kwargs,
    ):
        """
        打印一行, 默认自动换行.

        :param str_tpl: string template, 一个字符串模板.
        :param new_line: 如果是 True, 那么会自动换行, 否则不会. 默认自动换行.
        :param kwargs: 额外的传递给 str_tpl 的参数.
        """
        self.print_str(
            str_tpl + self.terminal.clear_eol(),
            new_line=new_line,
            **kwargs,
        )

    def _force_initial_column(self):
        """
        用回车符 (注意! 不是换行符) 把光标移动到本行初始位置.
        """
        self.print_str("\r")

    def relocate(self):
        """
        把光标移动到初始位置. 本质上是把光标向上回退移动到第一行, 然后再用回车符把光标移动到本行初始位置.
        """
        print(self._position * self.terminal.move_up, end="")
        self._force_initial_column()
        self._position = 0

    def clear_n_lines(self, n: int):
        """
        把光标以上的 n 行清空, 并把光标移动到行首. 常用于清除掉已经打印过的内容.
        """
        if n > self._position:
            raise ValueError
        for _ in range(n):
            print(self.terminal.move_up, end="")
            print(self.terminal.clear_eol(), end="")
        self._force_initial_column()
        self._position -= n

    def clear_all(self):
        """
        清除所有内容, 并把光标移动到行首.
        """
        self.clear_n_lines(n=self._position)

    def print_item(self, item: "Item"):
        if item.selected:
            color = self.terminal.blue
            symbol = "[x]"
        else:
            color = self.terminal.normal
            symbol = "[ ]"

        self.print_line(
            "{color}{symbol} {terminal.normal}{title}",
            color=color,
            symbol=symbol,
            title=item.title_text,
            terminal=self.terminal,
        )
        self.print_line(
            "    {terminal.normal}{subtitle}",
            subtitle=item.subtitle_text,
            terminal=self.terminal,
        )

    def print_items(self, items: T.Iterable["Item"]):
        for item in items:
            self.print_item(item)

    def clear_eos(self):
        print(self.terminal.clear_eos(), end="")

    @property
    def width(self):
        return self.terminal.width or 80

    @property
    def height(self):
        return self.terminal.width or 24
