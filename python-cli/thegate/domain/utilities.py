def check_not_none(thing):
    if thing is None:
        raise RuntimeError("Should not be None!")