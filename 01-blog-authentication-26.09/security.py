from flask import abort
from functools import wraps
from flask_login import current_user


def admin_only(function):
    @wraps(function)  # Keeps the original function name instead of replacing it with a literal "wrapper_function"
    def wrapper_function(*args, **kwargs):
        if current_user.get_id() == "1" or current_user.get_id() == "2":
            return function(*args, **kwargs)
        else:
            return abort(403)
    return wrapper_function
