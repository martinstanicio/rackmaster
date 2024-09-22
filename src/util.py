from slot import Slot
from util import format_coordinates


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


def is_pallet_origin(yyy: int) -> bool:
    """
    Checks if the `yyy` coordinate corresponds to the first slot of any pallet.
    """
    return yyy == get_pallet_origin(yyy)


def is_int(num) -> bool:
    """
    Checks if a number is an integer, regardless of its data type.
    """
    if type(num) == str:
        try:
            num = float(num)
        except ValueError:
            return False

    return num % 1 == 0


def format_coordinates(xx: int, yyy: int, zz: int) -> str:
    """
    Returns a string in the format `(xx, yyy, zz)`.
    """
    return f"({xx:02d}, {yyy:03d}, {zz:02d})"


def validate_slot_availability(
    target_slot: Slot,
) -> None:
    """
    Raises an exception if the target slot is blocked or not empty.
    """
    xx = target_slot.xx
    yyy = target_slot.yyy
    zz = target_slot.zz

    if target_slot.is_blocked():
        raise Exception(
            f"The target slot at {format_coordinates(xx,yyy,zz)} is blocked."
        )

    if not target_slot.is_empty():
        raise Exception(
            f"The target slot at {format_coordinates(xx,yyy,zz)} is not empty."
        )
