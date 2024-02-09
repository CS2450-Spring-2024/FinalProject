def parse_word(word: str, addr: int) -> int:
    try:
        val = int(word)
    except ValueError as e:
        raise ValueError(f"Could not parse ${addr}: {word}")
    return val
