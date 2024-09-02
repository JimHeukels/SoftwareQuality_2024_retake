import hashlib


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

def validate_password(stored_password, provided_password):
    # hashed_provided = hashlib.sha256(provided_password.encode('utf-8')).hexdigest()
    return provided_password == stored_password