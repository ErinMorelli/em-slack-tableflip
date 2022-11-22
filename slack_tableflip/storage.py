"""
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

import os
from datetime import datetime

from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from . import app


# Create database
db = SQLAlchemy(app)


class EncryptedToken:
    """Mixin for managing token encryption."""
    __cipher = Fernet(os.environ.get('TOKEN_KEY', '').encode('utf8'))

    encrypted_token = db.Column(db.BLOB)

    def set_token(self, token):
        """Encrypt and set token value."""
        if not isinstance(token, bytes):
            token = token.encode('utf-8')
        self.encrypted_token = self.__cipher.encrypt(token)

    def get_token(self):
        """Retrieve decrypted token."""
        return self.__cipher.decrypt(self.encrypted_token).decode('utf-8')


class User(db.Model, EncryptedToken):
    """Table for storing authenticated user data."""
    __tablename__ = 'flip_users'

    id = db.Column(db.String(16), primary_key=True)
    team = db.Column(db.String(16))
    added = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, team_id, token):
        """Initialize new User in db."""
        self.id = user_id
        self.team = team_id
        self.set_token(token)

    def __repr__(self):
        """Friendly representation of User for debugging."""
        return f'<User id={self.id} team={self.team}>'


class Team(db.Model, EncryptedToken):
    """Table for storing authenticated user data."""
    __tablename__ = 'flip_teams'

    id = db.Column(db.String(16), primary_key=True)
    added = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, team_id, token):
        """Initialize new Team in db."""
        self.id = team_id
        self.set_token(token)

    def __repr__(self):
        """Friendly representation of Team for debugging."""
        return f'<Team id={self.id}>'


try:
    # Attempt to initialize database
    with app.app_context():
        db.create_all()
except SQLAlchemyError:
    # Other wise, refresh the session
    db.session.rollback()
