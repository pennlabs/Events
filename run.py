#!/usr/bin/env python
from __future__ import absolute_import

from app import create_app


if __name__ == "__main__":
    app = create_app()
    app.run()
