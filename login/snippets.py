from ArtChart.settings import SECRET_KEY
import hashlib
import time

def get_hash(user):
    hasher = hashlib.sha256()
    hasher.update(user.username.encode())
    hasher.update(user.email.encode())
    hasher.update(user.password.encode())
    hasher.update(str(user.is_active).encode())
    hasher.update(SECRET_KEY.encode())
    return hasher.hexdigest()
