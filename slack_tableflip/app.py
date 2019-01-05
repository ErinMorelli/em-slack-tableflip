#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2015-2019 Erin Morelli.

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

from flask import redirect, render_template, request
import slack_tableflip.auth as auth
import slack_tableflip.flipper as flipper
from slack_tableflip import (APP, PROJECT_INFO, ALLOWED_TYPES, ALL_WORD_TYPES,
                             ALLOWED_COMMANDS, report_event)


@APP.route('/', methods=['GET', 'POST'])
def home():
    """Render app homepage template."""
    if request.method == 'POST':
        report_event('post_request', request.form.to_dict())
        return flipper.flip(request.form.to_dict())

    return render_template(
        'index.html',
        project=PROJECT_INFO,
        allowed_types=ALLOWED_TYPES,
        allowed_word_types=ALL_WORD_TYPES,
        allowed_commands=ALLOWED_COMMANDS
    )


@APP.route('/authenticate')
def authenticate():
    """Redirect to generated Slack user authentication url."""
    return redirect(auth.get_redirect())


@APP.route('/validate')
def validate():
    """Validate the returned values from user authentication."""
    return redirect(auth.validate_return(request.args.to_dict()))


@APP.route('/teams')
def teams():
    """Redirect the to the Slack team authentication url."""
    return redirect(auth.get_redirect('team'))


@APP.route('/authorize')
def authorize():
    """Authorize the returned values from team authentication."""
    return redirect(auth.validate_return(request.args.to_dict(), 'team'))
