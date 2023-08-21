from itertools import islice


def chunk(it: list, size: int = 10) -> list[tuple]:
    """Split a list into equally-sized (except the last one) tuples"""
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))
