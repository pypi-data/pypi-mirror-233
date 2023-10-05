# -*- coding: utf-8 -*-

import typing as T
import dataclasses


@dataclasses.dataclass
class Item:
    """
    Item in the UI.

    :param uid: item unique id.
    :param title: title of item.
    :param subtitle: subtitle of item.
    :param arg: argument that will be passed to the next action.
    :param autocomplete: the text that will be filled in the input box when hit TAB
    :param selected: whether the item is selected.
    :param variables: additional variables that can be used in the next action.
    """

    uid: str = dataclasses.field()
    title: str = dataclasses.field()
    subtitle: T.Optional[str] = dataclasses.field(default=None)
    arg: T.Optional[str] = dataclasses.field(default=None)
    autocomplete: T.Optional[str] = dataclasses.field(default=None)
    selected: bool = dataclasses.field(default=False)
    variables: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)

    @property
    def title_text(self) -> str:
        return self.title

    @property
    def subtitle_text(self) -> str:
        return self.subtitle or ""

    def enter_handler(self):
        """
        This is the abstract method that when you hit Enter on this item.
        """
        pass
