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
'''
Module: slack_tableflip.auth

    - Generates Slack authentication URL
    - Validates data returned by Slack authentication
    - Stores authenticated user data
'''

from flask import abort
from urllib import urlencode
from datetime import timedelta
from slacker import OAuth, Auth, Error
from slack_tableflip import PROJECT_INFO
from slack_tableflip.storage import AppInfo, Users, DB
from sqlalchemy.exc import IntegrityError as IntegrityError
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


# Get app info from DB
APP_INFO = AppInfo.query.get('flip')

# Create serializer
GENERATOR = URLSafeTimedSerializer(APP_INFO.client_secret)


# =============================================================================
#  Authentication
# =============================================================================

def get_redirect():
    ''' Generates Slack authentication URL
    '''

    # Set OAuth base URL
    location_base = 'https://slack.com/oauth/authorize'

    # Generate state token
    state_token = GENERATOR.dumps(APP_INFO.client_id)

    # URL encode params
    params = urlencode({
        'client_id': APP_INFO.client_id,
        'redirect_uri': PROJECT_INFO['valid_url'],
        'scope': 'read,post,client',
        'state': state_token
    })

    # Set full location
    location = "{0}?{1}".format(location_base, params)

    # Return URL for redirect
    return location


# =============================================================================
#  Validation
# =============================================================================

def validate_state(state):
    ''' Validates state token returned by user authentication
    '''

    try:
        # Attempt to decode state
        state_token = GENERATOR.loads(
            state,
            max_age=timedelta(minutes=60).total_seconds()
        )

    except SignatureExpired:
        # Token has expired
        abort(400)

    except BadSignature:
        # Token is not authorized
        abort(401)

    if state_token != APP_INFO.client_id:
        # Token is not authorized
        abort(401)

    # Return success
    return


def get_user_token(code):
    ''' Requests a user token from the Slack API
    '''

    # Set OAuth access object
    oauth = OAuth()

    try:
        # Attempt to make request
        result = oauth.access(
            client_id=APP_INFO.client_id,
            client_secret=APP_INFO.client_secret,
            redirect_uri=PROJECT_INFO['valid_url'],
            code=code
        )

    except Error:
        abort(400)

    if not result.successful:
        abort(400)

    # Return token
    return result.body['access_token']


def validate_user(token):
    ''' Retrieves user information from Slack API
    '''

    # Set auth object
    auth = Auth(token)

    # Make request
    result = auth.test()

    # Check for errors
    if not result.successful:
        abort(400)

    # Return user info
    return result.body


def validate_return(args):
    ''' Wrapper function for data validation functions
        Stores new authenticated user data
    '''

    # Make sure we have args
    if not args.get('state') or not args.get('code'):
        abort(400)

    # Validate state
    validate_state(args.get('state'))

    # Get user token
    token = get_user_token(args.get('code'))

    # Validate user and get info
    user_info = validate_user(token)

    # Create new user
    new_user = Users(user_info['user_id'])
    new_user.team = user_info['team_id']
    new_user.token = token

    try:
        # Attempt to store new user
        DB.session.add(new_user)
        DB.session.commit()

    except IntegrityError:
        # User already exists
        abort(409)

    # Set success url
    redirect_url = '{0}?success=1'.format(PROJECT_INFO['base_url'])

    # Return successful
    return redirect_url
