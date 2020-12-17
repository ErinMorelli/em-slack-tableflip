#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# pylint: disable=anomalous-backslash-in-string
"""
Copyright (c) 2015-2020 Erin Morelli.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
"""

import os
from datetime import date
from threading import Thread
from pkg_resources import get_provider
from flask import Flask
import keen


# =============================================================================
#  App Constants
# =============================================================================

# Set module name
__module__ = "slack_tableflip.{0}".format(__file__)


# Get module info
def set_project_info():
    """Set project information from setup tools installation."""
    # CUSTOMIZE THIS VALUE FOR YOUR OWN INSTALLATION
    base_url = os.environ['BASE_URL']

    # Get app info from the dist
    app_name = 'slack_tableflip'
    provider = get_provider(app_name)

    return {
        'name': app_name,
        'name_full': 'EM Slack Tableflip',
        'author_url': 'http://www.erinmorelli.com',
        'github_url': 'https://github.com/ErinMorelli/em-slack-tableflip',
        'version': '1.10',
        'version_int': 1.10,
        'package_path': provider.module_path,
        'copyright': f'2015-{str(date.today().year)}',
        'client_secret': os.environ['SLACK_CLIENT_SECRET'],
        'client_id': os.environ['SLACK_CLIENT_ID'],
        'base_url': base_url,
        'oauth_url': os.environ['OAUTH_URL'],
        'auth_url': f'{base_url}/authenticate',
        'user_url': f'{base_url}/validate',
        'team_url': f'{base_url}/authorize',
        'team_scope': [
            'commands'
        ],
        'user_scope': [
            'chat:write:bot',
            'chat:write:user',
            'identify'
        ]
    }


# Project info
PROJECT_INFO = set_project_info()

# Set the template directory
TEMPLATE_DIR = os.path.join(PROJECT_INFO['package_path'], 'templates')

# Allowed slash commands
ALLOWED_COMMANDS = [
    '/flip',
    '/fliptable',
    '/tableflip',
    '/flip_table',
    '/table_flip'
]

# Allowed flip types
# Sources:
#   http://www.emoticonfun.org/flip/
#   http://emojicons.com/table-flipping
#   http://tableflipping.com/
ALLOWED_TYPES = {
    'adorable': "(づ｡◕‿‿◕｡)づ ︵ ┻━┻",
    'battle': "(╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)",
    'bear': "ʕノ•ᴥ•ʔノ ︵ ┻━┻",
    'bomb': "( ・_・)ノ⌒●~*",
    'bored': "(ノ゜-゜)ノ ︵ ┻━┻",
    'buffet': "(╯°□°）╯︵ ┻━━━┻ ",
    'chill': "┬─┬ ノ( ◕◡◕ ノ)",
    'classic': "(╯°□°)╯︵ ┻━┻",
    'cry': "(╯'□')╯︵ ┻━┻",
    'cute': "┻━┻ ︵ ლ(⌒-⌒ლ)",
    'dead': "(╯°□°）╯︵ /(x_x)|",
    'eyes': "(👁 ͜ʖ👁) ╯︵ ┻━┻",
    'force': "(._.) ~ ︵ ┻━┻",
    'freakout': "(ﾉಥДಥ)ﾉ︵┻━┻･/",
    'fury': "┻━┻彡 ヽ(ಠДಠ)ノ彡┻━┻﻿",
    'glare': "(╯ಠ_ಠ）╯︵ ┻━┻",
    'hypnotic': "(╯°.°）╯ ┻━┻",
    'jake': "(┛❍ᴥ❍﻿)┛彡┻━┻",
    'laptop': "(ノÒ益Ó)ノ彡▔▔▏",
    'magic': "(/¯◡ ‿ ◡)/¯ ~ ┻━┻",
    'monocle': "(╯ಠ_ರೃ)╯︵ ┻━┻",
    'opposite': "ノ┬─┬ノ ︵ ( \o°o)\\",
    'owl': "(ʘ∇ʘ)ク 彡 ┻━┻",
    'people': "(/ .□.)\ ︵╰(゜Д゜)╯︵ /(.□. \)",
    'person': "(╯°□°）╯︵ /(.□. \)",
    'pudgy': "(ノ ゜Д゜)ノ ︵ ┻━┻",
    'rage': "(ﾉಥ益ಥ）ﾉ﻿ ┻━┻",
    'relax': "┬─┬ノ( º _ ºノ)",
    'return': "(ノ^_^)ノ┻━┻ ┬─┬ ノ( ^_^ノ)",
    'robot': "┗[© ♒ ©]┛ ︵ ┻━┻",
    'shrug': "┻━┻ ︵﻿ ¯\(ツ)/¯ ︵ ┻━┻",
    'strong': "/(ò.ó)┛彡┻━┻",
    'tantrum': "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    'teeth': "(ノಠ益ಠ)ノ彡┻━┻",
    'two': "┻━┻ ︵╰(°□°)╯︵ ┻━┻",
    'whoops': "┬──┬﻿ ¯\_(ツ)",
    'yelling': "(┛◉Д◉)┛彡┻━┻"
}

# Allowed restore flip types
RESTORE_TYPES = {
    'chill': "{0} ノ( ◕◡◕ ノ)",
    'relax': "{0} ノ( º _ ºノ)",
    'whoops': "{0} ¯\_(ツ)"
}

# Allowed word flip types
WORD_TYPES = {
    'adorable': "(づ｡◕‿‿◕｡)づ ︵ {0}",
    'bear': "ʕノ•ᴥ•ʔノ ︵ {0}",
    'bored': "(ノ゜-゜)ノ ︵ {0}",
    'cry': "(╯'□')╯︵ {0}",
    'cute': "{0} ︵ ლ(⌒-⌒ლ)",
    'eyes': "(👁 ͜ʖ👁) ╯︵ {0}",
    'force': "(._.) ~ ︵ {0}",
    'glare': "(╯ಠ_ಠ）╯︵ {0}",
    'hypnotic': "(╯°.°）╯ {0}",
    'jake': "(┛❍ᴥ❍﻿)┛彡{0}",
    'magic': "(/¯◡ ‿ ◡)/¯ ~ {0}",
    'monocle': "(╯ಠ_ರೃ)╯︵ {0}",
    'owl': "(ʘ∇ʘ)ク 彡 {0}",
    'pudgy': "(ノ ゜Д゜)ノ ︵ {0}",
    'rage': "(ﾉಥ益ಥ）ﾉ﻿ {0}",
    'robot': "┗[© ♒ ©]┛ ︵ {0}",
    'strong': "/(ò.ó)┛彡{0}",
    'teeth': "(ノಠ益ಠ)ノ彡{0}",
    'word': "(╯°□°)╯︵ {0}",
    'yelling': "(┛◉Д◉)┛彡{0}"
}

# Get list of all types with words
ALL_WORD_TYPES = {**WORD_TYPES, **RESTORE_TYPES}

# Flipped character mapping
FLIPPED_CHARS = {
    " ": " ",
    "a": "ɐ",
    "b": "q",
    "c": "ɔ",
    "d": "p",
    "e": "ǝ",
    "f": "ɟ",
    "g": "ƃ",
    "h": "ɥ",
    "i": "ı",
    "j": "ɾ",
    "k": "ʞ",
    "l": "l",
    "m": "ɯ",
    "n": "u",
    "o": "o",
    "p": "d",
    "q": "b",
    "r": "ɹ",
    "s": "s",
    "t": "ʇ",
    "u": "n",
    "v": "ʌ",
    "w": "ʍ",
    "x": "x",
    "y": "ʎ",
    "z": "z",
    "A": "∀",
    "B": "𐐒",
    "C": "Ɔ",
    "D": "p",
    "E": "Ǝ",
    "F": "Ⅎ",
    "G": "פ",
    "H": "H",
    "I": "I",
    "J": "ſ",
    "K": "ʞ",
    "L": "˥",
    "M": "W",
    "N": "N",
    "O": "O",
    "P": "Ԁ",
    "Q": "Ό",
    "R": "ᴚ",
    "S": "S",
    "T": "┴",
    "U": "∩",
    "V": "Λ",
    "W": "M",
    "X": "X",
    "Y": "⅄",
    "Z": "Z",
    "1": "Ɩ",
    "2": "ᄅ",
    "3": "Ɛ",
    "4": "ㄣ",
    "5": "ϛ",
    "6": "9",
    "7": "ㄥ",
    "8": "8",
    "9": "6",
    ",": "'",
    "!": "¡",
    "?": "¿",
    "(": ")",
    ")": "(",
    "[": "]",
    "]": "[",
    "{": "}",
    "}": "{",
    "<": ">",
    ">": "<",
    ".": "˙",
    '"': ",,",
    "'": ",",
    "’": ",",
    "`": ",",
    "“": ",,",
    "”": ",,",
    "¿": "?",
    "&": "⅋",
    "_": "‾"
}


def report_event(name, event):
    """Asynchronously report an event."""
    # Set up thread
    event_report = Thread(
        target=keen.add_event,
        args=(name, event)
    )

    # Set up as asynchronous daemon
    event_report.daemon = True

    # Start event report
    event_report.start()


# =============================================================================
# Flask App Configuration
# =============================================================================

# Initialize flask app
APP = Flask(
    'em-slack-tableflip',
    template_folder=TEMPLATE_DIR,
    static_folder=TEMPLATE_DIR
)

# Set up flask config
# SET THESE ENV VALUES FOR YOUR OWN INSTALLATION
APP.config.update({
    'SECRET_KEY': os.environ['SECURE_KEY'],
    'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
})
