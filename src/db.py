from copy import deepcopy
from functools import cmp_to_key

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.base import Base
from src.i18n import t
from src.slot import Slot
from src.status import Status
from src.util import format_coordinates, get_pallet_origin, is_int, is_pallet_origin


class Database:
    _session: sessionmaker[Session]
    session: Session

    def __init__(
        self,
        db_url: str,
        rows: list[int],
        columns: list[int],
        levels: list[int],
    ) -> None:
        self.rows = rows
        self.columns = columns
        self.levels = levels
        engine = create_engine(db_url)
        Base.metadata.create_all(bind=engine)
        self._session = sessionmaker(bind=engine)

    def __enter__(self) -> None:
        """
        Opens a new database connection.
        """
        self.session = self._session()

        # if `warehouse` table is empty, it needs to be populated
        first_time = len(self.session.query(Slot).all()) == 0
        if first_time:
            self.populate()

        return self

    def __exit__(self, *_) -> None:
        """
        Closes the database connection.
        """
        self.session.close()

    def populate(self) -> None:
        """
        Populates the database with all possible slots in the warehouse.
        """
        try:
            for xx in self.rows:
                for yyy in self.columns:
                    for zz in self.levels:
                        self.session.add(Slot(xx, yyy, zz))
        except Exception as e:
            raise Exception(f"{t("db_populate_error")}: {e}")
        else:
            self.session.commit()

    def are_valid_coordinates(self, xx: int, yyy: int, zz: int) -> bool:
        """
        Returns `True` if the coordinates are within the boundaries configured, or `False` otherwise.
        """
        return (xx in self.rows) and (yyy in self.columns) and (zz in self.levels)

    def get_pallet_slots(self, slot: Slot) -> list[Slot]:
        """
        Returns a list of all slots for the given pallet.
        """
        origin = get_pallet_origin(slot.yyy)

        return (
            self.session.query(Slot)
            .where(
                Slot.xx == slot.xx,
                Slot.yyy >= origin,
                Slot.yyy <= origin + 2,
                Slot.zz == slot.zz,
            )
            .all()
        )

    def get_slot(self, xx: int, yyy: int, zz: int) -> Slot | None:
        """
        Returns the slot with the given coordinates, or `None` if it does not exist.
        """
        return (
            self.session.query(Slot)
            .where(Slot.xx == xx, Slot.yyy == yyy, Slot.zz == zz)
            .one_or_none()
        )

    def get_free_slots(self) -> list[Slot]:
        """
        Returns a list of all slots that are not blocked and have 0 items.
        """
        return (
            self.session.query(Slot)
            .where(Slot.status != Status.blocked, Slot.quantity == 0)
            .all()
        )

    def register_inbound(
        self,
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
            if not is_int(quantity):
                raise Exception(
                    f"{t("invalid_quantity")}: {quantity}. {t("quantity_must_be_integer")}."
                )

            if quantity <= 0:
                raise Exception(
                    f"{t("invalid_quantity")}: {quantity}. {t("quantity_must_be_greater_than_0")}."
                )

            if not self.are_valid_coordinates(xx, yyy, zz):
                raise Exception(
                    f"{t("invalid_coordinates")}: {format_coordinates(xx, yyy, zz)}. {t("coordinates_out_of_bounds")}."
                )

            target_slot = self.get_slot(xx, yyy, zz)

            if target_slot is None:
                raise Exception(
                    f"{t('slot_at')} {format_coordinates(xx, yyy, zz)} {t('not_found')}."
                )

            pallet_slots = self.get_pallet_slots(target_slot)

            for slot in pallet_slots:
                coords = format_coordinates(slot.xx, slot.yyy, slot.zz)

                if slot.is_blocked():
                    raise Exception(f"{t("slot_at")} {coords} {t("slot_at_blocked")}.")

                if not slot.is_empty():
                    raise Exception(
                        f"{t("slot_at")} {coords} {t("slot_at_not_empty")}."
                    )

                if use_full_pallet:
                    slot.status = Status.full_pallet
                    slot.article_code = article_code
                    slot.quantity = quantity
                else:
                    slot.status = Status.divided_pallet

            if not use_full_pallet:
                target_slot.article_code = article_code
                target_slot.quantity = quantity
        except Exception as e:
            self.session.rollback()
            raise Exception(f"{t("operation_cancelled")}. {e}")
        else:
            self.session.commit()

    def update_stock(self, xx: int, yyy: int, zz: int, quantity_to_add: int) -> None:
        """
        Updates the quantity of the slot with the given coordinates.
        """
        if not self.are_valid_coordinates(xx, yyy, zz):
            raise Exception(
                f"{t('invalid_coordinates')}: {format_coordinates(xx, yyy, zz)}. {t('coordinates_out_of_bounds')}."
            )

        if not is_int(quantity_to_add):
            raise Exception(
                f"{t('invalid_quantity')}: {quantity_to_add}. {t('quantity_must_be_integer')}."
            )

        if quantity_to_add <= 0:
            raise Exception(
                f"{t('invalid_quantity')}: {quantity_to_add}. {t('quantity_must_be_greater_than_0')}."
            )

        try:
            target_slot = self.get_slot(xx, yyy, zz)
            pallet_slots = self.get_pallet_slots(target_slot)

            slots_to_update = (
                pallet_slots
                if target_slot.status == Status.full_pallet
                else [target_slot]
            )

            for slot in slots_to_update:
                if slot is None:
                    raise Exception(
                        f"{t('slot_at')} {format_coordinates(slot.xx, slot.yyy, slot.zz)} {t('not_found')}."
                    )

                if slot.status == Status.blocked:
                    raise Exception(
                        f"{t('slot_at')} {format_coordinates(slot.xx, slot.yyy, slot.zz)} {t('slot_at_blocked')}."
                    )

                if slot.is_empty():
                    raise Exception(
                        f"{t('slot_at')} {format_coordinates(slot.xx, slot.yyy, slot.zz)} {t('slot_at_empty')}."
                    )

                slot.quantity += quantity_to_add
        except Exception as e:
            self.session.rollback()
            raise Exception(f"{t('operation_cancelled')}. {e}")
        else:
            self.session.commit()

    def get_article_slots(
        self,
        article_code: str,
    ) -> list[Slot]:
        """
        Returns a list of all the slots whose `article_code` matches the one given.
        """
        slots = self.session.query(Slot).where(Slot.article_code == article_code).all()
        results: list[Slot] = []

        for slot in slots:
            if slot.status == Status.full_pallet and not is_pallet_origin(slot.yyy):
                continue
            results.append(slot)

        return results

    def get_article_stock(self, article_code: str) -> int:
        """
        Given an `article_code`, returns the amount of that item in the warehouse.
        """
        slots = self.get_article_slots(article_code)
        quantity = 0

        for slot in slots:
            quantity += slot.quantity

        return quantity

    def compare_slots(self, slot1: Slot, slot2: Slot) -> int:
        if slot1.xx > slot2.xx:
            return 1
        if slot1.xx < slot2.xx:
            return -1

        if slot1.yyy > slot2.yyy:
            return 1
        if slot1.yyy < slot2.yyy:
            return -1

        if slot1.zz > slot2.zz:
            return 1
        if slot1.zz < slot2.zz:
            return -1

        return 0

    def register_outbound(self, *articles_with_quantity: tuple[str, int]) -> list[Slot]:
        """
        Given a list of `articles_with_quantity`, returns a list of slots that can be used for retrieval.

        Raises an exception if there are missing articles.
        """
        slots: list[Slot] = []
        missing_articles: list[tuple[str, int]] = []

        for article, quantity in articles_with_quantity:
            slots_available = self.get_article_slots(article)

            sorted_slots = sorted(slots_available, key=cmp_to_key(self.compare_slots))

            for slot in sorted_slots:
                if quantity == 0:
                    break

                slots_to_update: list[Slot] = (
                    self.get_pallet_slots(slot)
                    if slot.status == Status.full_pallet
                    else [slot]
                )

                if slot.quantity <= quantity:
                    quantity -= slot.quantity
                    slot.quantity = 0
                else:
                    slot.quantity -= quantity
                    quantity = 0

                for s in slots_to_update:
                    s.quantity = slot.quantity

                    if s.quantity == 0:
                        s.article_code = None

                slots.append(deepcopy(slot))

            if quantity > 0:
                missing_articles.append((article, quantity))

        if len(missing_articles) > 0:
            self.session.rollback()
            raise Exception(
                f"{t("operation_cancelled")}. {t('missing_articles')}:\n{'\n'.join([f"{article[0]}: {article[1]}" for article in missing_articles])}"
            )
        else:
            self.session.commit()
            return slots

    def swap_pallets(self, slot1: Slot, slot2: Slot) -> None:
        pallet1 = self.get_pallet_slots(slot1)
        pallet2 = self.get_pallet_slots(slot2)

        for slot in pallet1 + pallet2:
            if slot.is_blocked():
                raise Exception(
                    f"{t("operation_cancelled")}. Cannot swap pallets with blocked slots."
                )

        for i in range(len(pallet1)):
            (pallet1[i].article_code, pallet2[i].article_code) = (
                pallet2[i].article_code,
                pallet1[i].article_code,
            )
            (pallet1[i].quantity, pallet2[i].quantity) = (
                pallet2[i].quantity,
                pallet1[i].quantity,
            )
            (pallet1[i].status, pallet2[i].status) = (
                pallet2[i].status,
                pallet1[i].status,
            )

        self.session.commit()
