import random, string

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_disease_names_by_text(text, max_len):
    return _get_disease_names_by_text(max_len)


def _get_disease_names_by_text(max_len):
    return [randomword(10).capitalize() for i in range(max_len)]


def get_doctor_by_disease(disease_name):
    return _get_doctor_by_disease(disease_name)


def _get_doctor_by_disease(disease_name):
    return f"Doctor against disease '{disease_name}'"


