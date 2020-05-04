import random, string

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_disease_names(text, max_len):
    return [randomword(10).capitalize() for i in range(max_len)]