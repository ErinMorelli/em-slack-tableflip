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
Module: slack_tableflip.storage

    - Sets database schema for storing user and app data
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


class AppInfo(DB.Model):
    ''' Table for storing application-specific data
    '''
    __tablename__ = 'app_info'

    name = DB.Column(DB.String(120), primary_key=True)
    client_id = DB.Column(DB.String(21))
    client_secret = DB.Column(DB.String(32))

    def __init__(self, name, client_id, client_secret):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret

    def __repr__(self):
        return '<AppInfo {0}>'.format(self.name)


try:
    # Attempt to initialize database
    DB.create_all()

except:
    # Other wise, refresh the session
    DB.session.rollback()
