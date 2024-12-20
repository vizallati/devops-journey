from flask import session, redirect, url_for


def check_user_auth():
    try:
        return session['loggedin']
    except KeyError:
        return False