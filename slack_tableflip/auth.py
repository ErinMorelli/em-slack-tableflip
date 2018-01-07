#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2015-2018 Erin Morelli.

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

from datetime import timedelta
from urllib.parse import urlencode
from flask import abort
from slacker import OAuth, Auth, Error
from slack_tableflip import PROJECT_INFO, report_event
from slack_tableflip.storage import Users, Teams, DB
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


# Create serializer
GENERATOR = URLSafeTimedSerializer(PROJECT_INFO['client_secret'])


def get_redirect(scope='user'):
    """Generate Slack authentication URL."""
    # Generate state token
    state_token = GENERATOR.dumps(PROJECT_INFO['client_id'])

    # Setup scope
    scope_type = '{0}_scope'.format(scope)

    # Setup return URL
    return_url = '{0}_url'.format(scope)

    # URL encode params
    params = urlencode({
        'client_id': PROJECT_INFO['client_id'],
        'redirect_uri': PROJECT_INFO[return_url],
        'scope': ' '.join(PROJECT_INFO[scope_type]),
        'state': state_token
    })

    # Set full location
    location = "{0}?{1}".format(PROJECT_INFO['oauth_url'], params)

    # Return URL for redirect
    return location


def validate_state(state):
    """Validate state token returned by authentication."""
    try:
        # Attempt to decode state
        state_token = GENERATOR.loads(
            state,
            max_age=timedelta(minutes=60).total_seconds()
        )

    except SignatureExpired:
        # Token has expired
        report_event('token_expired', {
            'state': state
        })
        abort(400)

    except BadSignature:
        # Token is not authorized
        report_event('token_not_authorized', {
            'state': state
        })
        abort(401)

    if state_token != PROJECT_INFO['client_id']:
        # Token is not authorized
        report_event('token_not_valid', {
            'state': state,
            'state_token': state_token
        })
        abort(401)

    # Return success
    return


def get_token(code, scope='user'):
    """Request a token from the Slack API."""
    # Set OAuth access object
    oauth = OAuth()

    # Setup return URL
    return_url = '{0}_url'.format(scope)

    try:
        # Attempt to make request
        result = oauth.access(
            client_id=PROJECT_INFO['client_id'],
            client_secret=PROJECT_INFO['client_secret'],
            redirect_uri=PROJECT_INFO[return_url],
            code=code
        )

    except Error as err:
        report_event('oauth_error', {
            'code': code,
            'return_url': return_url,
            'error': str(err)
        })
        abort(400)

    if not result.successful:
        report_event('oauth_unsuccessful', {
            'code': code,
            'return_url': return_url,
            'result': result.__dict__
        })
        abort(400)

    # Return token
    return result.body['access_token']


def validate_token(token):
    """Validate token and retrieves info from Slack API."""
    # Set auth object
    auth = Auth(token)

    try:
        # Make request
        result = auth.test()

    except Error as err:
        report_event(str(err), {
            'token': token
        })
        abort(400)

    # Check for errors
    if not result.successful:
        report_event('token_invalid', {
            'token': token,
            'result': result.__dict__
        })
        abort(400)

    # Return user info
    return result.body


def store_user(token, info):
    """Store a validated user in the database."""
    # Check if user exists
    user = Users.query.filter_by(
        id=info['user_id'],
        team=info['team_id']
    ).first()

    if user is None:
        # Create new user
        new_user = Users(
            user_id=info['user_id'],
            team_id=info['team_id'],
            token=token
        )

        # Store new user
        report_event('user_added', {
            'token': token,
            'info': info
        })
        DB.session.add(new_user)

    else:
        # Update user token
        report_event('user_updated', {
            'token': token,
            'info': info
        })
        user.token = token

    # Update DB
    DB.session.commit()


def store_team(token, info):
    """Store a validated team in the database."""
    # Check if team exists
    team = Teams.query.get(info['team_id'])

    if team is None:
        # Create new team
        new_team = Teams(
            team_id=info['team_id'],
            token=token
        )

        # Store new team
        report_event('team_added', {
            'token': token,
            'info': info
        })
        DB.session.add(new_team)

    else:
        # Update team token
        report_event('team_updated', {
            'token': token,
            'info': info
        })
        team.token = token

    # Update DB
    DB.session.commit()


def validate_return(args, scope='user'):
    """Run data validation functions."""
    # Make sure we have args
    if not args['state'] or not args['code']:
        report_event('missing_args', args)
        abort(400)

    # Validate state
    validate_state(args['state'])

    # Get access token
    token = get_token(args['code'], scope)

    # Validate token and get info
    token_info = validate_token(token)

    # Set up storage methods
    store_methods = {
        'user': store_user,
        'team': store_team
    }

    # Store token data
    store_methods[scope](token, token_info)

    # Set success url
    redirect_url = '{0}?success=1'.format(PROJECT_INFO['base_url'])

    # Return successful
    return redirect_url
