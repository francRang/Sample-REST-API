from os import environ, path
from dotenv import load_dotenv
import os

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

"""
Maybe add some env vars for ports, debug, et al.
"""
class Config:
    """Set Flask configuration vars from .env file."""

    # General
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
