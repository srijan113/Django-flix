import random
import string

def get_random_string(size = 4, chars = string.ascii_lowercase + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])