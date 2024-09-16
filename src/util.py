from config import columns, levels, rows


def are_valid_coordinates(xx: int, yyy: int, zz: int) -> bool:
    """
    Returns `True` if the coordinates are within the boundaries configured, or `False` otherwise.
    """
    if xx not in rows or yyy not in columns or zz not in levels:
        return False

    return True


def get_pallet_origin(yyy: int) -> int:
    """
    Returns the `yyy` coordinate for the first slot in the pallet the given slot is in.

    Each rack can hold 3 pallets, which are themselves divided into 3 slots, resulting in 9 available slots per rack.
    Given the column `yyy`, the function returns the number of the first column in the corresponding pallet.
    """
    while True:
        if yyy % 3 == 1:
            return yyy

        yyy -= 1
