#!/usr/bin/env python
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
''' Script to start Flask server for hosted table flipping
'''

import logging
import slack_tableflip.auth as auth
import slack_tableflip.flipper as flipper
from flask import redirect, render_template, request
from slack_tableflip import APP, PROJECT_INFO, ALLOWED_TYPES, ALLOWED_COMMANDS


@APP.route('/')
def home():
    ''' Render app homepage template
    '''
    logging.warning('HOME')
    return render_template(
        'index.html',
        project=PROJECT_INFO,
        allowed_types=ALLOWED_TYPES,
        allowed_commands=ALLOWED_COMMANDS
    )


@APP.route('/authenticate')
def authenticate():
    ''' Redirect user to generated Slack authentication url
    '''
    return redirect(auth.get_redirect())


@APP.route('/validate')
def validate():
    ''' Validate the returned values from authentication
    '''
    return redirect(auth.validate_return(request.args))


@APP.route('/table', methods=['GET', 'POST'])
def table():
    ''' Return a flipped table from a Slack POST call
    '''
    use_args = request.args

    if request.method == 'POST':
        use_args = request.form

    return flipper.flip(use_args)


if __name__ == '__main__':
    APP.run()
