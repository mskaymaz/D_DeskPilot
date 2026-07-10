"""Backward-compatible import shim for GorevKarti.

The implementation lives in kart.py; keep this module while internal callers
or old extensions still import gorev_karti.GorevKarti.
"""

from kart import GorevKarti

__all__ = ["GorevKarti"]
