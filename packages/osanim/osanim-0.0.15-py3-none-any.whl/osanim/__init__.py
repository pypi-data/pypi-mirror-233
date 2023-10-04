r"""Osanim Systems API.

This exports:
  - xOne: a Business Utility Library used for messaging, payments and significantly focuses on simplicity and ease of use.
  - Schoolz: an Educational Library used to manage all activities of an institution

Consumers of this API would need some form authentication which can be done on the website https://api.osanim.com.

Callbacks and other customizations are also available on the website https://api.osanim.com.

This library is intended to be used as a drop-in replacement for multiple APIs from vast number of providers.

# :copyright: (c) 2013 Osanim Systems
"""

# from typing import Protocol

from .xone import xOne
from .schoolz import Schoolz

__version__ = '0.0.14'
__author__ = 'Godfred Owusu'
__contact__ = 'osanimsystems@gmail.com'
__homepage__ = 'https://api.osanim.com/'
__docformat__ = 'restructuredtext'
__keywords__ = 'utility business library'

__all__ = ['xOne', 'Schoolz']

# class _Decodable(Protocol):  # noqa: Y046
#     def decode(self, __encoding: str) -> str: ...

