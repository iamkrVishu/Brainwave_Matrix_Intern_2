import bcrypt

def hash_password(password):
    """ Hash password securely using bcrypt """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Return as string for DB storage

def check_password(password, hashed_password):
    """ Verify password against stored hash """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))