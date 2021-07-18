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

from flask_wtf.csrf import CSRFProtect
from flask import redirect, render_template, request

from . import (app, project_info, allowed_types, all_word_types,
               allowed_commands, report_event, auth, flipper)


# Setup CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)


@csrf.exempt
@app.route('/', methods=['GET', 'POST'])
def home():
    """Render app homepage template."""
    if request.method == 'POST':
        report_event('post_request', request.form.to_dict())
        return flipper.flip(request.form.to_dict())

    return render_template(
        'index.html',
        project=project_info,
        allowed_types=allowed_types,
        allowed_word_types=all_word_types,
        allowed_commands=allowed_commands
    )


@app.route('/authenticate', methods=['GET'])
def authenticate():
    """Redirect to generated Slack user authentication url."""
    return redirect(auth.get_redirect())


@app.route('/validate', methods=['GET'])
def validate():
    """Validate the returned values from user authentication."""
    return redirect(auth.validate_return(request.args.to_dict()))


@app.route('/teams', methods=['GET'])
def teams():
    """Redirect the to the Slack team authentication url."""
    return redirect(auth.get_redirect('team'))


@app.route('/authorize', methods=['GET'])
def authorize():
    """Authorize the returned values from team authentication."""
    return redirect(auth.validate_return(request.args.to_dict(), 'team'))
