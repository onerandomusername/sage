"""Sage."""

__all__ = ("app",)

# load the environment variables before we start anything
try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv(override=False)

import sage.logging
from sage.app import app


sage.logging.configure_logging()
