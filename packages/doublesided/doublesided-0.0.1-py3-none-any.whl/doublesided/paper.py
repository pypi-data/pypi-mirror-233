PAPER_SIZES = {
    "letter": (8.5, 11),
    "legal": (8.5, 14),
    "tabloid": (11, 17),
    "a0": (33.1, 46.8),
    "a1": (23.4, 33.1),
    "a2": (16.5, 23.4),
    "a3": (11.7, 16.5),
    "a4": (8.3, 11.7),
    "a5": (5.8, 8.3),
    "a6": (4.1, 5.8),
    "a7": (2.9, 4.1),
    "a8": (2.0, 2.9),
    "a9": (1.5, 2.0),
    "a10": (1.0, 1.5),
}


def get_paper_size_in_inch(name: str) -> tuple[int, int]:
    if name.lower() not in PAPER_SIZES:
        raise ValueError(f'Unknown paper size name {name}')
    return PAPER_SIZES[name.lower()]
