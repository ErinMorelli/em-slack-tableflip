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


@APP.route('/', methods=['GET', 'POST'])
def home():
    ''' Render app homepage template
    '''

    if request.method == 'POST':
        logging.warning(request.form)
        return flipper.flip(request.form)

    else:
        return render_template(
            'index.html',
            project=PROJECT_INFO,
            allowed_types=ALLOWED_TYPES,
            allowed_commands=ALLOWED_COMMANDS
        )


@APP.route('/authenticate')
def authenticate():
    ''' Redirect to generated Slack user authentication url
    '''
    return redirect(auth.get_redirect())


@APP.route('/validate')
def validate():
    ''' Validate the returned values from user authentication
    '''
    return redirect(auth.validate_return(request.args))


@APP.route('/teams')
def teams():
    ''' Redirect the to the Slack team authentication url
    '''
    return redirect(auth.get_redirect('team'))


@APP.route('/authorize')
def authorize():
    ''' Authorize the returned values from team authentication
    '''
    return redirect(auth.validate_return(request.args, 'team'))
