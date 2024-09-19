from sqlalchemy.orm import Session

from slot import Slot
from status import Status
from util import is_pallet_origin


def get_article_slots(
    session: Session,
    article_code: str,
) -> list[Slot]:
    """
    Returns a list of all the slots whose `article_code` matches the one given.
    """
    slots = session.query(Slot).where(Slot.article_code == article_code).all()
    results: list[Slot] = []

    for slot in slots:
        if slot.status == Status.full_pallet and not is_pallet_origin(slot.yyy):
            continue
        results.append(slot)

    return results


def get_article_stock(
    session: Session,
    article_code: str,
) -> list[Slot]:
    """
    Given an `article_code`, returns the amount of that item in the warehouse.
    """
    slots = get_article_slots(session, article_code)
    quantity = 0

    for slot in slots:
        quantity += slot.quantity

    return quantity
