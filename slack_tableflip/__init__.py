#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# EM Slack Tableflip
# Copyright (c) 2015 Erin Morelli
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
'''
Module: slack_tableflip

    - Sets up Flask application and module constants
'''

from os import path
from flask import Flask
from datetime import date
from pkginfo import Installed
from pkg_resources import get_provider


# =============================================================================
#  App Constants
# =============================================================================

# Set module name
__module__ = "slack_tableflip.{0}".format(__file__)


# Get module info
def set_project_info():
    ''' Set project information from setup tools installation
    '''

    # CUSTOMIZE THIS VALUE FOR YOUR OWN INSTALLATION
    base_url = 'http://dev.erinmorelli.com/slack/flip'

    # Get app info from the dist
    app_name = 'slack_tableflip'
    provider = get_provider(app_name)
    dist = Installed(app_name).__dict__

    # Set extra info
    dist.update({
        'name_full': 'EM Slack Tableflip',
        'author_url': 'http://www.erinmorelli.com',
        'version_int': 0.101,
        'package_path': provider.module_path,
        'copyright': str(date.today().year),
        'base_url': base_url,
        'auth_url': '{0}/authenticate'.format(base_url),
        'valid_url': '{0}/validate'.format(base_url)
    })

    return dist

# Project info
PROJECT_INFO = set_project_info()

# Set the template directory
TEMPLATE_DIR = path.join(PROJECT_INFO['package_path'], 'templates')

# Set required args
REQUIRED_ARGS = [
    'command',
    'team_id',
    'user_id',
    'channel_id'
]

# Allowed slash commands
ALLOWED_COMMANDS = [
    '/flip',
    '/fliptable',
    '/tableflip',
    '/flip_table',
    '/table_flip'
]

# Allowed flip types
ALLOWED_TYPES = {
    'patience': 'no flip',
    'pudgy': 'fat flip',
    'battle': 'fight to flip',
    'me': "the table's revenge",
    'aggravated': "FFFUUUUUU",
    'putback': 'peace at last',
    'dude': 'no tables nearby',
    'emotional': 'I know that feel, bro',
    'freakout': 'screw this game!',
    'hercules': 'RAWR!',
    'jedi': 'flip or flip not, there is no try',
    'bear': 'but this table flipped just right',
    'magical': 'not just an illusion',
    'robot': 'all the good table flipping jobs...',
    'russia': 'in Soviet Russia table flip you',
    'happy': 'all smiles',
    'word': 'flip a word of your choice'
}

# =============================================================================
# Flask App Configuration
# =============================================================================

# Initalize flask app
APP = Flask(
    'em-slack-tableflip',
    template_folder=TEMPLATE_DIR,
    static_folder=TEMPLATE_DIR
)

# Set up flask config
# CUSTOMIZE THESE VALUES FOR YOUR OWN INSTALLATION
APP.config.update({
    'SQLALCHEMY_DATABASE_URI': 'mysql://username:password@host:port/database',
    'SECRET_KEY': 'set_custom_key_for_your_installation'
})
