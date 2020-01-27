from lifebartenders.config import ALLOWED_EXTENSIONS


def valid_extension(filename):
    if filename:
        if filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
            return True

    return False
