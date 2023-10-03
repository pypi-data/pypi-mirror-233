#!/usr/bin/env python3
'''
Functions for generating Markdown files.
'''

_SPECIAL_CHARS = r'\`*_{}[]<>()+-.!|'
_TRANS_TABLE = str.maketrans({char: f'\\{char}' for char in _SPECIAL_CHARS})


def escape(text):
    '''
    Escape special symbols in Markdown text.
    '''
    return text.translate(_TRANS_TABLE)
