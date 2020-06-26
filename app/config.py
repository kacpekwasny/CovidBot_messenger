import os

class Config(object):
    SECRET_KEY = 'xxxxxxxxxxxxx'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///path'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VERIFY_TOKEN = "xxxxxxx"
    AT = "xxxxxx"
    command_ls = ["folw", "unfw"]
