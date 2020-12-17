#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# pylint: disable=invalid-name,too-few-public-methods
"""
EM Slack Tableflip module: slack_tableflip.storage.

    - Sets database schema for storing user data
    - Initializes database structure

Copyright (c) 2015-2016 Erin Morelli

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

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from slack_tableflip import APP


# Create database
DB = SQLAlchemy(APP)


class Users(DB.Model):
    """Table for storing authenticated user data."""

    __tablename__ = 'flip_users'

    id = DB.Column(DB.String(16), primary_key=True)
    team = DB.Column(DB.String(16))
    token = DB.Column(DB.String(255))
    added = DB.Column(DB.DateTime, default=datetime.now)

    def __init__(self, user_id, team_id, token):
        """Initialize new User in db."""
        self.id = user_id
        self.team = team_id
        self.token = token

    def __repr__(self):
        """Friendly representation of User for debugging."""
        return f'<User id={self.id} team={self.team}>'


class Teams(DB.Model):
    """Table for storing authenticated user data."""

    __tablename__ = 'flip_teams'

    id = DB.Column(DB.String(16), primary_key=True)
    token = DB.Column(DB.String(255))
    added = DB.Column(DB.DateTime, default=datetime.now)

    def __init__(self, team_id, token):
        """Initialize new Team in db."""
        self.id = team_id
        self.token = token

    def __repr__(self):
        """Friendly representation of Team for debugging."""
        return f'<Team id={self.id}>'


try:
    # Attempt to initialize database
    DB.create_all()

except SQLAlchemyError:
    # Other wise, refresh the session
    DB.session.rollback()
