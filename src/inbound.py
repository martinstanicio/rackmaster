from sqlalchemy.orm import Session

from slot import Slot
from status import Status


def get_free_slots(session: Session) -> list[Slot]:
    return (
        session.query(Slot)
        .where(Slot.status != Status.blocked, Slot.quantity == 0)
        .all()
    )
