from config import rows, columns, levels


def is_valid_coordinate(xx: int, yyy: int, zz: int) -> bool:
    if xx not in rows or yyy not in columns or zz not in levels:
        return False

    return True
