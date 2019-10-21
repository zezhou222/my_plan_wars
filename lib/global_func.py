from uuid import uuid4


def get_random_filename():
    return uuid4().__str__()
