#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (c) 2015-2020 Erin Morelli.

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

from os import environ
import newrelic.agent

from slack_tableflip.app import APP


if __name__ == '__main__':
    # Start New Relic agent
    newrelic.agent.initialize()

    # Start Flask app
    APP.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
