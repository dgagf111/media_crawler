"""
Compatibility module that exposes the FastAPI app instance.
"""

from .app import app, create_application

__all__ = ["app", "create_application"]

