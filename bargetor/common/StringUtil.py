import random
import string

def get_random_str(str_len = 32):
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(str_len))

