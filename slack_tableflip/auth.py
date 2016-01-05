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
from slack_tableflip.storage import Users, Teams, DB
from sqlalchemy.exc import IntegrityError as IntegrityError
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


# Create serializer
GENERATOR = URLSafeTimedSerializer(PROJECT_INFO['client_secret'])


def get_redirect(scope='user'):
    ''' Generates Slack authentication URL
    '''

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
    ''' Validates state token returned by authentication
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

    if state_token != PROJECT_INFO['client_id']:
        # Token is not authorized
        abort(401)

    # Return success
    return


def get_token(code, scope='user'):
    ''' Requests a token from the Slack API
    '''

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

    except Error:
        abort(400)

    if not result.successful:
        abort(400)

    # Return token
    return result.body['access_token']


def validate_token(token):
    ''' Validates token and retrieves info from Slack API
    '''

    # Set auth object
    auth = Auth(token)

    try:
        # Make request
        result = auth.test()

    except Error:
        abort(400)

    # Check for errors
    if not result.successful:
        abort(400)

    # Return user info
    return result.body


def store_user(token, info):
    ''' Stores a validated user in the database
    '''

    # Create new user
    new_user = Users(info['user_id'])
    new_user.team = info['team_id']
    new_user.token = token

    try:
        # Attempt to store new user
        DB.session.add(new_user)
        DB.session.commit()

    except IntegrityError:
        # User already exists
        abort(409)

    return


def store_team(token, info):
    ''' Stores a validated team in the database
    '''

    # Create new team
    new_team = Teams(info['team_id'])
    new_team.token = token

    try:
        # Attempt to store new team
        DB.session.add(new_team)
        DB.session.commit()

    except IntegrityError:
        # Team already exists
        abort(409)

    return


def validate_return(args, scope='user'):
    ''' Wrapper function for data validation functions
        Stores new authenticated user data
    '''

    # Make sure we have args
    if not args.get('state') or not args.get('code'):
        abort(400)

    # Validate state
    validate_state(args.get('state'))

    # Get access token
    token = get_token(args.get('code'), scope)

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
