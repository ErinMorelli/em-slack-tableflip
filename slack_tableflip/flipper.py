#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# pylint: disable=global-variable-not-assigned,global-statement
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

import argparse
from slacker import Auth, Chat, Error

import slack_tableflip as stf
from slack_tableflip.storage import Users


# Set globals
ERRORS = []
COMMAND = None

# Set not authenticated error message
AUTH_ERROR = f"{stf.PROJECT_INFO['name_full']} is not authorized to post on " \
           f"your behalf in this team: " \
           f"*<{stf.PROJECT_INFO['auth_url']}|Click here to authorize>*"


class FlipParser(argparse.ArgumentParser):
    """Custom ArgumentParser object for special error and help messages."""

    def error(self, message):
        """Store all error messages in global errors list."""
        global ERRORS
        ERRORS.append(message)

    def print_help(self, req_type=None):  # pylint: disable=arguments-differ
        """Generate help and list messages."""
        global ERRORS
        global COMMAND

        if req_type == 'help':
            help_msg = "*{app_name}* can flip all kinds of tables for you!\n"
            help_msg += "Here are some examples:\n\n"
            help_msg += "`{command}`\n\tFlips a classic table\n\n"
            help_msg += "`{command} relax`\n\tPuts a table back\n\n"
            help_msg += "`{command} word table`\n\tFlips the word 'table'\n\n"
            help_msg += "`{command} relax table`\n\t"
            help_msg += "Puts the word 'table' back\n\n"
            help_msg += "`{command} list`\n\tLists available flip types\n\n"
            help_msg += "`{command} help`\n\tShows this message\n"

            ERRORS.append(help_msg.format(
                app_name=stf.PROJECT_INFO['name_full'],
                command=COMMAND
            ))

        elif req_type == 'list':
            list_msg = "*{app_name}* knows these types of flips:\n\n"

            classic_msg = f"\n\n\t{stf.ALLOWED_TYPES['classic']}\n\n"
            list_msg += "`{command}`" + classic_msg

            for allowed_type, desc in sorted(stf.ALLOWED_TYPES.items()):
                if allowed_type != 'classic':
                    if allowed_type in stf.ALL_WORD_TYPES.keys():
                        flip_msg = f" {allowed_type} [word]`\n\n\t{desc}\n\n"
                    else:
                        flip_msg = f" {allowed_type}`\n\n\t{desc}\n\n"

                    # Set full message for type
                    list_msg += "`{command}" + flip_msg

            ERRORS.append(list_msg.format(
                app_name=stf.PROJECT_INFO['name_full'],
                command=COMMAND
            ))

        elif req_type == 'version':
            ERRORS.append(f"{stf.PROJECT_INFO['name_full']} "
                          f"v{stf.PROJECT_INFO['version']}")


class TypeAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """Custom Action object for validating and parsing flip arguments."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Validate flip arguments and stores them to namespace."""
        flip_type = values[0].lower()
        flip_word = None

        # Check for help
        if flip_type in ['help', 'list', 'version']:
            parser.print_help(flip_type)
            return

        # Check that the type is valid
        if (flip_type not in stf.ALLOWED_TYPES and
                flip_type not in stf.WORD_TYPES and
                flip_type not in stf.RESTORE_TYPES):
            stf.report_event('flip_invalid', {
                'flip': flip_type
            })
            parser.error(f'Flip type "{flip_type}" is not known')

        if flip_type in stf.WORD_TYPES or flip_type in stf.RESTORE_TYPES:

            if len(values) >= 2:
                # Set word value
                flip_word = ' '.join(values[1:len(values)])

            else:
                # Check for flip that requires words
                if flip_type == 'word':
                    stf.report_event('flip_missing_word', {
                        'flip': flip_type
                    })
                    parser.error(
                        f'Flip type "{flip_type}" requires words to flip')

        # Set values
        setattr(namespace, 'flip_type', flip_type)
        setattr(namespace, 'flip_word', flip_word)

        return


def get_parser():
    """Set up and returns custom ArgumentParser object."""
    # Create flip parser
    parser = FlipParser()

    # Add valid args
    parser.add_argument('flip_type', nargs='+', action=TypeAction)

    return parser


def check_user(args):
    """Return authenticated user token data."""
    # Look for user in DB
    user = Users.query.get(args['user_id'])

    # Validate user
    if not user:
        return None

    # Validate team
    if user.team != args['team_id']:
        return None

    # Return token
    return user.token


def is_valid_token(token):
    """Check that the user has a valid token."""
    # Set auth object
    auth = Auth(token)

    try:
        # Make request
        result = auth.test()

    except Error as err:
        # Check for auth errors
        stf.report_event(str(err), {
            'token': token
        })
        return False

    # Check for further errors
    if not result.successful:
        stf.report_event('token_invalid', {
            'token': token,
            'result': result.__dict__
        })
        return False

    # Return successful
    return True


def do_restore_flip(flip_type, words):
    """Restore a flipped word."""
    flip_base = stf.RESTORE_TYPES[flip_type]

    return flip_base.format(words)


def do_word_flip(flip_type, words):
    """Flip some words."""
    # Flip characters using mapping
    char_list = [
        stf.FLIPPED_CHARS.get(char, char)
        for char in words
    ]
    char_list.reverse()

    flipped_words = ''.join(char_list)

    flip_base = stf.WORD_TYPES[flip_type]

    return flip_base.format(flipped_words)


def do_flip(flip_type, flip_word=None):
    """Return the requested flip."""
    # Fall back to a basic flip
    if flip_type == '':
        flip_type = 'classic'

    # Check for word flip
    if flip_word is not None:

        if flip_type in stf.RESTORE_TYPES:
            # Do restore flip
            return do_restore_flip(flip_type, flip_word)

        if flip_type in stf.WORD_TYPES:
            # Do a word flip
            return do_word_flip(flip_type, flip_word)

    # Do a regular flip
    return stf.ALLOWED_TYPES[flip_type]


def send_flip(token, table, args):
    """Post the flip as the authenticated user in Slack."""
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
        stf.report_event(str(err), {
            'token': token,
            'table': table,
            'args': args
        })

        # Report if we got any errors
        return f"{stf.PROJECT_INFO['name_full']} encountered an " \
               f"error: {str(err)}"

    # Return without errors
    return None


def flip(args):
    """Run flip functions."""
    # Reset global error tracker
    global ERRORS
    ERRORS = []

    # Make sure this is a valid slash command
    if args['command'] not in stf.ALLOWED_COMMANDS:
        stf.report_event('command_not_allowed', args)
        return f'"{args["command"]}" is not an allowed command'

    # Set global command value to access later
    global COMMAND
    COMMAND = args['command']

    # Check to see if user has authenticated with the app
    token = check_user(args)

    # If the user or token is not valid, let them know
    if token is None or not is_valid_token(token):
        stf.report_event('auth_error', {
            'args': args,
            'token': token
        })
        return AUTH_ERROR

    # If there's no input, use the default flip
    if not args['text']:
        flip_type = 'classic'
        flip_word = None

    else:
        # Set up text args for parser
        text_args = args['text'].split()

        # Get parser
        parser = get_parser()

        # Parse args
        result = parser.parse_args(text_args)

        # Report any errors from parser
        if ERRORS:
            stf.report_event('parser_errors', {
                'errors': ERRORS
            })
            return ERRORS[0]

        # Set values
        flip_type = result.flip_type
        flip_word = result.flip_word

    # Get requested flip
    table = do_flip(flip_type, flip_word)

    # Post flip as user
    err = send_flip(token, table, args)

    # If there were problems posting, report it
    if err is not None:
        return err

    # Return successful
    return '', 204
