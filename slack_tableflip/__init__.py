"""
Copyright (c) 2015-2021 Erin Morelli.

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

import keen
from flask import Flask


# Common project metadata
__version__ = open('VERSION').read()
__app_name__ = 'EM Slack Tableflip'
__copyright__ = f'2015-{str(date.today().year)}'

# Project URLs
base_url = os.environ.get('BASE_URL', None)
github_url = os.environ.get('GITHUB_URL', None)

# Project info
project_info = {
    'name': __app_name__,
    'version': __version__,
    'copyright': __copyright__,
    'base_url': base_url,
    'github_url': github_url,
    'client_secret': os.environ.get('SLACK_CLIENT_SECRET', None),
    'client_id': os.environ.get('SLACK_CLIENT_ID', None),
    'oauth_url': os.environ.get('OAUTH_URL', None),
    'auth_url': f'{base_url}/authenticate',
    'user_url': f'{base_url}/validate',
    'team_url': f'{base_url}/authorize',
    'team_scope': [
        'commands'
    ],
    'user_scope': [
        'chat:write'
    ]
}

# Set the template directory
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Allowed slash commands
allowed_commands = [
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
allowed_types = {
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
    'opposite': "ノ┬─┬ノ ︵ ( \\o°o)\\",
    'owl': "(ʘ∇ʘ)ク 彡 ┻━┻",
    'people': "(/ .□.)\\ ︵╰(゜Д゜)╯︵ /(.□. \\)",
    'person': "(╯°□°）╯︵ /(.□. \\)",
    'pudgy': "(ノ ゜Д゜)ノ ︵ ┻━┻",
    'rage': "(ﾉಥ益ಥ）ﾉ﻿ ┻━┻",
    'relax': "┬─┬ノ( º _ ºノ)",
    'return': "(ノ^_^)ノ┻━┻ ┬─┬ ノ( ^_^ノ)",
    'robot': "┗[© ♒ ©]┛ ︵ ┻━┻",
    'shrug': "┻━┻ ︵﻿ ¯\\(ツ)/¯ ︵ ┻━┻",
    'strong': "/(ò.ó)┛彡┻━┻",
    'tantrum': "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    'teeth': "(ノಠ益ಠ)ノ彡┻━┻",
    'two': "┻━┻ ︵╰(°□°)╯︵ ┻━┻",
    'whoops': "┬──┬﻿ ¯\\_(ツ)",
    'yelling': "(┛◉Д◉)┛彡┻━┻"
}

# Allowed restore flip types
restore_types = {
    'chill': "{0} ノ( ◕◡◕ ノ)",
    'relax': "{0} ノ( º _ ºノ)",
    'whoops': "{0} ¯\\_(ツ)"
}

# Allowed word flip types
word_types = {
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
all_word_types = {**word_types, **restore_types}

# Flipped character mapping
flipped_chars = {
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

# Set up Flask app
app = Flask(
    'em-slack-tableflip',
    template_folder=template_dir,
    static_folder=template_dir
)

# Set up flask config
app.config.update({
    'SECRET_KEY': os.environ.get('SECURE_KEY_STR', None),
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL', None),
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
})


def report_event(name, event):
    """Asynchronously report an event."""
    event_report = Thread(
        target=keen.add_event,
        args=(name, event)
    )

    # Set up as asynchronous daemon
    event_report.daemon = True

    # Start event report
    event_report.start()
