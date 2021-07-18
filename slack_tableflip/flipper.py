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

from .storage import User
from . import (project_info, allowed_types, all_word_types, word_types,
               restore_types, flipped_chars, allowed_commands, report_event)


# Set globals
errors = []
command = None

# Set not authenticated error message
auth_error = f"{project_info['name']} is not authorized to post on " \
             f"your behalf in this team: " \
             f"*<{project_info['auth_url']}|Click here to authorize>*"


class FlipParser(argparse.ArgumentParser):
    """Custom ArgumentParser object for special error and help messages."""

    def error(self, message):
        """Store all error messages in global errors list."""
        global errors
        errors.append(message)

    def print_help(self, req_type=None):  # pylint: disable=arguments-differ
        """Generate help and list messages."""
        global errors
        global command

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

            errors.append(help_msg.format(
                app_name=project_info['name'],
                command=command
            ))

        elif req_type == 'list':
            list_msg = "*{app_name}* knows these types of flips:\n\n"

            classic_msg = f"\n\n\t{allowed_types['classic']}\n\n"
            list_msg += "`{command}`" + classic_msg

            for allowed_type, desc in sorted(allowed_types.items()):
                if allowed_type != 'classic':
                    if allowed_type in all_word_types.keys():
                        flip_msg = f" {allowed_type} [word]`\n\n\t{desc}\n\n"
                    else:
                        flip_msg = f" {allowed_type}`\n\n\t{desc}\n\n"

                    # Set full message for type
                    list_msg += "`{command}" + flip_msg

            errors.append(list_msg.format(
                app_name=project_info['name'],
                command=command
            ))

        elif req_type == 'version':
            errors.append(f"{project_info['name']} v{project_info['version']}")


class TypeAction(argparse.Action):
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
        if (flip_type not in allowed_types and
                flip_type not in word_types and
                flip_type not in restore_types):
            report_event('flip_invalid', {'flip': flip_type})
            parser.error(f'Flip type "{flip_type}" is not known')

        # Set word value
        if flip_type in word_types or flip_type in restore_types:
            if len(values) >= 2:
                flip_word = ' '.join(values[1:len(values)])
            elif flip_type == 'word':
                report_event('flip_missing_word', {'flip': flip_type})
                parser.error(f'Flip type "{flip_type}" requires words to flip')

        # Set values
        setattr(namespace, 'flip_type', flip_type)
        setattr(namespace, 'flip_word', flip_word)


def get_parser():
    """Set up and returns custom ArgumentParser object."""
    parser = FlipParser()
    parser.add_argument('flip_type', nargs='+', action=TypeAction)
    return parser


def check_user(args):
    """Return authenticated user token data."""
    user = User.query.get(args['user_id'])

    # Validate user and team
    if not user or user.team != args['team_id']:
        return None

    # Return token
    return user.get_token()


def is_valid_token(token):
    """Check that the user has a valid token."""
    auth = Auth(token)

    try:
        # Make request
        result = auth.test()
    except Error as err:
        # Check for auth errors
        report_event(str(err), {})
        return False

    # Check for further errors
    if not result.successful:
        report_event('token_invalid', {'result': result.__dict__})
        return False

    # Return successful
    return True


def do_restore_flip(flip_type, words):
    """Restore a flipped word."""
    flip_base = restore_types[flip_type]
    return flip_base.format(words)


def do_word_flip(flip_type, words):
    """Flip some words."""
    char_list = [flipped_chars.get(char, char) for char in words]
    char_list.reverse()
    flipped_words = ''.join(char_list)
    return word_types[flip_type].format(flipped_words)


def do_flip(flip_type, flip_word=None):
    """Return the requested flip."""
    if flip_type == '':
        flip_type = 'classic'

    # Check for word flip
    if flip_word is not None:

        if flip_type in restore_types:
            # Do restore flip
            return do_restore_flip(flip_type, flip_word)

        if flip_type in word_types:
            # Do a word flip
            return do_word_flip(flip_type, flip_word)

    # Do a regular flip
    return allowed_types[flip_type]


def send_flip(token, table, args):
    """Post the flip as the authenticated user in Slack."""
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
        report_event(str(err), {'table': table, 'args': args})
        return f"{project_info['name']} encountered an error: {str(err)}"

    # Return without errors
    return None


def flip(args):
    """Run flip functions."""
    global errors
    errors = []

    # Make sure this is a valid slash command
    if args['command'] not in allowed_commands:
        report_event('command_not_allowed', args)
        return f'"{args["command"]}" is not an allowed command'

    # Set global command value to access later
    global command
    command = args['command']

    # Check to see if user has authenticated with the app
    token = check_user(args)

    # If the user or token is not valid, let them know
    if token is None or not is_valid_token(token):
        report_event('auth_error', {'args': args})
        return auth_error

    # If there's no input, use the default flip
    if not args['text']:
        flip_type = 'classic'
        flip_word = None

    else:
        # Set up text args for parser
        text_args = args['text'].split()

        # Parse args
        parser = get_parser()
        result = parser.parse_args(text_args)

        # Report any errors from parser
        if errors:
            report_event('parser_errors', {'errors': errors})
            return errors[0]

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
