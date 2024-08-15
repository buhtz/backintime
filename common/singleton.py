# SPDX-FileCopyrightText: © 2022 Mars Landis
# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: CC0-1.0
#
# This file is licensed under Creative Commons Zero v1.0 Universal (CC0-1.0)
# and is part of the program "Back In time" which is released under GNU General
# Public License v2 (GPLv2). See file LICENSE or go to
# <https://www.gnu.org/licenses/#GPL>.
#
# Credits to Mr. Mars Landis describing that solution in his artile
# 'Better Python Singleton with a Metaclass' at
# <https://python.plainenglish.io/better-python-singleton-with-a-metaclass-41fb8bfe2127>
# himself refering to this Stack Overflow
# <https://stackoverflow.com/q/6760685/4865723> question as his inspiration.
#
# Original code adapted by Christian Buhtz.

"""Flexible and pythonic singleton implemention.

Support inheritance and multiple classes. Multilevel inheritance is
theoretically possible if the '__allow_reinitialization' approach would be
implemented as described in the original article.

Example ::

    >>> from singleton import Singleton
    >>>
    >>> class Foo(metaclass=Singleton):
    ...     def __init__(self):
    ...          self.value = 'Alyssa Ogawa'
    >>>
    >>> class Bar(metaclass=Singleton):
    ...     def __init__(self):
    ...          self.value = 'Naomi Wildmann'
    >>>
    >>> f = Foo()
    >>> ff = Foo()
    >>> f'{f.value=} :: {ff.value=}'
    "f.value='Alyssa Ogawa' :: ff.value='Alyssa Ogawa'"
    >>> ff.value = 'Who?'
    >>> f'{f.value=} :: {ff.value=}'
    "f.value='Who?' :: ff.value='Who?'"
    >>>
    >>> b = Bar()
    >>> bb = Bar()
    >>> f'{b.value=} :: {bb.value=}'
    "b.value='Naomi Wildmann' :: bb.value='Naomi Wildmann'"
    >>> b.value = 'thinking ...'
    >>> f'{b.value=} :: {bb.value=}'
    "b.value='thinking ...' :: bb.value='thinking ...'"
    >>>
    >>> id(f) == id(ff)
    True
    >>> id(b) == id(bb)
    True
    >>> id(f) == id(b)
    False
"""
class Singleton(type):
    """
    """
    _instances = {}
    """Hold single instances of multiple classes."""

    def __call__(cls, *args, **kwargs):

        try:
            # Re-use existing instance
            return cls._instances[cls]

        except KeyError as exc:
            # Create new instance
            cls._instances[cls] = super().__call__(*args, **kwargs)

            return cls._instances[cls]

