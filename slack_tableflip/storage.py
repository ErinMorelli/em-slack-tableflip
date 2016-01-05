#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# EM Slack Tableflip
# Copyright (c) 2015-2016 Erin Morelli
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
Module: slack_tableflip.storage

    - Sets database schema for storing user data
    - Initializes database structure
'''

from datetime import datetime
from slack_tableflip import APP
from flask.ext.sqlalchemy import SQLAlchemy


# Create database
DB = SQLAlchemy(APP)


class Users(DB.Model):
    ''' Table for storing authenticated user data
    '''
    __tablename__ = 'flip_users'

    id = DB.Column(DB.String(16), primary_key=True)
    team = DB.Column(DB.String(16))
    token = DB.Column(DB.String(60))
    added = DB.Column(DB.DateTime)

    def __init__(self, user_id):
        self.id = user_id
        self.added = datetime.now()

    def __repr__(self):
        return '<User {0}>'.format(self.id)


class Teams(DB.Model):
    ''' Table for storing authenticated user data
    '''
    __tablename__ = 'flip_teams'

    id = DB.Column(DB.String(16), primary_key=True)
    token = DB.Column(DB.String(60))
    added = DB.Column(DB.DateTime)

    def __init__(self, team_id):
        self.id = team_id
        self.added = datetime.now()

    def __repr__(self):
        return '<Team {0}>'.format(self.id)


try:
    # Attempt to initialize database
    DB.create_all()

except:
    # Other wise, refresh the session
    DB.session.rollback()
