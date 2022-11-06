"""Sage."""

# load the environment variables before we start anything
try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv(override=False)

from sage.app import app


__all__ = ("app",)
