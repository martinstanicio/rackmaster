from sqlalchemy import Column, Enum, Integer, String

from src.base import Base
from src.status import Status
from src.util import format_coordinates


class Slot(Base):
    __tablename__ = "warehouse"

    xx = Column("xx", Integer, primary_key=True)
    yyy = Column("yyy", Integer, primary_key=True)
    zz = Column("zz", Integer, primary_key=True)
    article_code = Column("article_code", String)
    quantity = Column("quantity", Integer)
    status = Column("status", Enum(Status))

    def __init__(
        self,
        xx: int,
        yyy: int,
        zz: int,
        status=Status.divided_pallet,
        article_code: str | None = None,
        quantity=0,
    ) -> None:
        if quantity < 0:
            raise Exception("`quantity` must be a positive number")

        if status not in list(Status):
            raise Exception(
                "`status` must be 'blocked', 'full_pallet', or 'divided_pallet'"
            )

        self.xx = xx
        self.yyy = yyy
        self.zz = zz
        self.article_code = article_code
        self.quantity = quantity
        self.status = status

    def __repr__(self):
        coords = format_coordinates(self.xx, self.yyy, self.zz)
        status = (
            "Full pallet" if self.status == Status.full_pallet else "Divided pallet"
        )

        if self.status == Status.blocked:
            msg = "Blocked"
        elif self.quantity == 0:
            msg = "Empty"
        else:
            if self.status == Status.full_pallet:
                msg = f"Full pallet - {self.article_code} x{self.quantity}"
            else:
                msg = f"Divided pallet - {self.article_code} x{self.quantity}"

        return f"{coords} - {msg}"

    def is_blocked(self) -> bool:
        return self.status == Status.blocked

    def is_empty(self) -> bool:
        return not self.is_blocked() and self.quantity == 0
