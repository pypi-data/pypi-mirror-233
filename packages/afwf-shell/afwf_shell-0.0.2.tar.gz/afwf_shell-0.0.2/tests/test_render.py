# -*- coding: utf-8 -*-

from afwf_shell.render import Render

# -*- coding: utf-8 -*-

import time
import dataclasses
from fuzzywuzzy import process
from afwf_shell.item import Item
from afwf_shell.render import Render, UIRender, LineEditor, Dropdown


render = Render()
ui_render = UIRender()


def example1():
    render.print_line("hello")
    render.print_line("world")
    time.sleep(1)


def example2():
    render.print_str("alice, ")
    render.print_str("bob, ")
    render.print_str("cathy", new_line=True)
    render.print_line("hello")
    render.print_line("world")
    time.sleep(1)

    render.move_to_start()
    time.sleep(1)


def example3():
    render.print_line("alice")
    render.print_line("bob")
    render.print_line("cathy")
    render.print_line("david")
    time.sleep(1)

    render.clear_n_lines(1)
    time.sleep(1)

    render.clear_n_lines(1)
    time.sleep(1)

    render.clear_all()
    time.sleep(1)


def example4():
    render.print_line("alice")
    render.print_line("bob")
    render.print_line("cathy")
    render.print_line("david")
    time.sleep(1)

    render.move_to_start()
    time.sleep(1)


# ------------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------------


@dataclasses.dataclass
class MyItem(Item):
    def enter_handler(self):
        print(f"enter: {self.title}")


def get_items():
    zen_of_python = [
        "Beautiful is better than ugly.",
        "Explicit is better than implicit.",
        "Simple is better than complex.",
        "Complex is better than complicated.",
        "Flat is better than nested.",
        "Sparse is better than dense.",
        "Readability counts.",
        "Special cases aren't special enough to break the rules.",
        "Although practicality beats purity.",
        "Errors should never pass silently.",
        "Unless explicitly silenced.",
        "In the face of ambiguity, refuse the temptation to guess.",
        "There should be one-- and preferably only one --obvious way to do it.",
        "Although that way may not be obvious at first unless you're Dutch.",
        "Now is better than never.",
        "Although never is often better than *right* now.",
        "If the implementation is hard to explain, it's a bad idea.",
        "If the implementation is easy to explain, it may be a good idea.",
        "Namespaces are one honking great idea -- let's do more of those!",
    ]
    items = [
        MyItem(
            uid=f"id-{str(ith).zfill(2)}",
            title=zen,
            subtitle=f"subtitle {str(ith).zfill(2)}",
            autocomplete=zen,
            arg=zen,
        )
        for ith, zen in enumerate(zen_of_python, start=1)
    ]
    return items


def handler(query: str):
    items = get_items()
    if query:
        mapper = {item.title: item for item in items}
        title_list = list(mapper.keys())
        result = process.extract(query, title_list, limit=len(items))
        return [mapper[title] for title, score in result]
    else:
        return items


def example5():
    query = ""
    le = LineEditor()
    le.enter_text(query)
    items = handler(query)
    dd = Dropdown(items=items)

    n_items = ui_render.print_ui(le, dd)
    time.sleep(1)

    ui_render.move_to_end(n_items)
    time.sleep(1)


def test():
    example1()
    example2()
    example3()
    example4()
    example5()


if __name__ == "__main__":
    from afwf_shell.tests import run_cov_test

    run_cov_test(__file__, "afwf_shell.render", preview=False)
