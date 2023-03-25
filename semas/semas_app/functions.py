SALT = "Python++"

def get_hash(password):
    import hashlib
    key = password + SALT
    hashed = hashlib.md5(key.encode())
    return hashed.hexdigest()
