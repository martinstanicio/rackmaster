from sqlalchemy.orm import Session

from slot import Slot
from status import Status
from util import are_valid_coordinates, get_pallet_origin, is_int


def get_free_slots(session: Session) -> list[Slot]:
    """
    Returns a list of all slots that are not blocked and have 0 items.
    """
    return (
        session.query(Slot)
        .where(Slot.status != Status.blocked, Slot.quantity == 0)
        .all()
    )


def validate_inbound(
    quantity: int,
    xx: int,
    yyy: int,
    zz: int,
) -> None:
    """
    Raises an exception if coordinates are not valid, or quantity is not a positive integer.
    """
    if not are_valid_coordinates(xx, yyy, zz):
        raise Exception(
            f"Invalid coordinates: ({xx:02d}, {yyy:03d}, {zz:02d}). Coordinates are out of bounds."
        )

    if not is_int(quantity):
        raise Exception(f"Invalid quantity: {quantity}. Quantity must be an integer.")

    if quantity <= 0:
        raise Exception(
            f"Invalid quantity: {quantity}. Quantity must be greater than 0."
        )


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
            f"The target slot at ({xx:02d}, {yyy:03d}, {zz:02d}) is blocked."
        )

    if not target_slot.is_empty():
        raise Exception(
            f"The target slot at ({xx:02d}, {yyy:03d}, {zz:02d}) is not empty."
        )


def register_inbound(
    session: Session,
    article_code: str,
    quantity: int,
    xx: int,
    yyy: int,
    zz: int,
    use_full_pallet: bool,
) -> None:
    """
    Stores `article_code` and `quantity` in the corresponding slot, or slots if it is a full pallet.
    Raises an exception if there is any error, or saves the changes otherwise.
    """
    try:
        validate_inbound(quantity, xx, yyy, zz)

        target_slot = (
            session.query(Slot)
            .where(Slot.xx == xx, Slot.yyy == yyy, Slot.zz == zz)
            .one_or_none()
        )

        pallet_origin = get_pallet_origin(yyy)
        pallet_slots = (
            session.query(Slot)
            .where(
                Slot.xx == xx,
                Slot.yyy >= pallet_origin,
                Slot.yyy <= pallet_origin + 2,
                Slot.zz == zz,
            )
            .all()
        )

        if use_full_pallet:
            for slot in pallet_slots:
                validate_slot_availability(slot)
                slot.status = Status.full_pallet
                slot.article_code = article_code
                slot.quantity = quantity
        else:
            for slot in pallet_slots:
                validate_slot_availability(slot)
                slot.status = Status.divided_pallet

            target_slot.article_code = article_code
            target_slot.quantity = quantity
    except Exception as e:
        print(f"Operation was cancelled. {e}")
    else:
        session.commit()
