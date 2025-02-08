import hashlib

def sanitize_cache_key(name):
    return hashlib.md5(name.encode()).hexdigest()