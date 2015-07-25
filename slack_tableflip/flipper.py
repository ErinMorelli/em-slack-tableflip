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
Module: slack_tableflip.flipper

    - Parses POST data from Slack
    - Parses user flip request
    - Retrieves and returns flip data from TFaaS
'''

import argparse
import requests
import slack_tableflip as stf
from urllib import quote_plus
from slacker import Chat, Error
from slack_tableflip.storage import Users


# Set globals
ERRORS = []
COMMAND = None


class FlipParser(argparse.ArgumentParser):
    ''' Custom ArgumentParser object for special error and help messages.
    '''

    def error(self, message):
        ''' Stores all error messages in global errors list
        '''
        global ERRORS
        ERRORS.append(message)

    def print_help(self, req_type):
        ''' Generates help and list messages
        '''
        global ERRORS
        global COMMAND

        if req_type == 'help':
            help_msg = "*{app_name}* can flip all kinds of tables for you!\n"
            help_msg += "Here are some examples:\n\n"
            help_msg += "`{command}`\n\tFlips a classic table\n\n"
            help_msg += "`{command} patience`\n\tPuts the table back\n\n"
            help_msg += "`{command} word table`\n\tFlips the word 'table'\n\n"
            help_msg += "`{command} list`\n\tLists available flip types\n\n"
            help_msg += "`{command} help`\n\tShows this message\n"

            ERRORS.append(help_msg.format(
                app_name=stf.project_info['name_full'],
                command=COMMAND
            ))

        elif req_type == 'list':
            list_msg = "*{app_name}* knows these types of flips:\n\n"
            list_msg += "`{command}` - the classic\n"

            for allowed_type, desc in stf.allowed_types.iteritems():
                flip_msg = " {0}` - {1}\n".format(allowed_type, desc)
                list_msg += "`{command}" + flip_msg

            ERRORS.append(list_msg.format(
                app_name=stf.project_info['name_full'],
                command=COMMAND
            ))


class TypeAction(argparse.Action):
    ''' Custom Action object for validating and parsing flip arguments
    '''

    def __call__(self, parser, namespace, values, option_string=None):
        ''' Validates flip arguments and stores them to namespace
        '''
        flip_type = values[0].lower()
        flip_word = None

        # Check for help
        if flip_type in ['help', 'list']:
            parser.print_help(flip_type)
            return

        # Check that the type is valid
        if flip_type not in stf.allowed_types:
            parser.error('Flip type "{0}" is not valid'.format(flip_type))

        if flip_type == 'word':

            if len(values) >= 2:
                # Set word value
                flip_word = ' '.join(values[1:len(values)])

            else:
                parser.error('Flip type "word" requires a word to flip')

        # Set values
        setattr(namespace, 'flip_type', flip_type)
        setattr(namespace, 'flip_word', flip_word)

        return


def get_parser():
    ''' Sets up and returns custom ArgumentParser object
    '''

    # Create flip parser
    parser = FlipParser()

    # Add valid args
    parser.add_argument('flip_type', nargs='+', action=TypeAction)

    return parser


def check_user(args):
    ''' Checks that the user is authenticated with the app
        Returns authenticated user token data
    '''

    # Set not authenticated error message
    auth_msg = "{0} is not authorized to post on your behalf in this team: {1}"
    auth_error = auth_msg.format(
        stf.project_info['name_full'],
        '*<{0}|Click here to authorize>*'.format(stf.project_info['auth_url'])
    )

    # Look for user in DB
    user = Users.query.get(args['user_id'])

    # Validate user
    if not user:
        return False, auth_error

    # Validate team
    if user.team != args['team_id']:
        return False, auth_error

    # Return token
    return True, user.token


def do_flip(flip_type, flip_word=None):
    ''' Requests a flip from TFaaS
    '''
    params = flip_type

    # Fall back to a basic flip
    if flip_type == '':
        params = 'flipping'

    # Set params for word flip
    if flip_word is not None:
        params = 'flipping/{0}'.format(quote_plus(flip_word))

    # Generate flip request url
    flip_url = 'http://table-flip.herokuapp.com/{0}'.format(params)

    # Make request
    return requests.get(flip_url).text


def send_flip(token, table, args):
    ''' Posts the flip as the authenticated user in Slack
    '''

    # Set up chat object
    chat = Chat(token)

    try:
        # Attempt to post message
        chat.post_message(
            args['channel_id'],
            table,
            username=args['user_id'],
            as_user=True
        )

    except Error as err:
        # Report if we got any errors
        return err

    # Return successful
    return


def flip(args):
    ''' Wrapper function for flip functions
        Returned error messages will post as private slackbot messages
    '''

    # Reset global error traker
    global ERRORS
    ERRORS = []

    # Make sure this is a valid slash command
    if args['command'] not in stf.allowed_commands:
        return '"{0}" is not an allowed command'.format(args['command'])

    else:
        # Set global command value to access later
        global COMMAND
        COMMAND = args['command']

    # Check to see if user has authenticated with the app
    (valid, token) = check_user(args)

    # If the user is not valid, let them know
    if not valid:
        return token

    # If there's no input, use the default flip
    if not args['text']:
        flip_type = 'flipping'
        flip_word = None

    else:
        # Set up text args for parser
        text_args = args['text'].split()

        # Get parser
        parser = get_parser()

        # Parse args
        result = parser.parse_args(text_args)

        # Report any errors from parser
        if len(ERRORS) > 0:
            return ERRORS[0]

        # Set values
        flip_type = result.flip_type
        flip_word = result.flip_word

    # Get requested flip from TFaaS
    table = do_flip(flip_type, flip_word)

    # Post flip as user
    err = send_flip(token, table, args)

    # If there were problems posting, report it
    if err is not None:
        return err

    # Return successful
    return ('', 204)