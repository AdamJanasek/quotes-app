from flask import session, redirect, url_for, flash
from flask_caching import Cache

cache = Cache()


# Decorators responsible for managing user rights
def login_required(func):
    def wrapper(*args, **kwargs):
        if session.get('User-Token'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('app.login'))

    return wrapper


def check_logged(func):
    def wrapper(*args, **kwargs):
        if session.get('User-Token'):
            return func(*args, **kwargs)
        else:
            flash("You must be logged in!")
            return redirect(url_for('app.quotes'))

    return wrapper


# Get information or error
def show_message(code, response, message):
    if code == 200:
        flash(message)
    else:
        flash(response.get('error'))
