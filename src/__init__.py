"""Financial transaction analyzer package."""

from flask import Flask
from pathlib import Path
from . import views  # noqa: F401

# Create Flask application
app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)
