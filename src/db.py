from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from base import Base
from slot import Slot


class Database:
    session: Session

    def __init__(
        self,
        db_url: str,
        rows: list[int],
        columns: list[int],
        levels: list[int],
    ):
        self.rows = rows
        self.columns = columns
        self.levels = levels
        engine = create_engine(db_url)
        Base.metadata.create_all(bind=engine)

        _Session = sessionmaker(bind=engine)
        self.session = _Session()

        # if `warehouse` table is empty, it needs to be populated
        first_time = len(self.session.query(Slot).all()) == 0
        if first_time:
            self.populate()

    def populate(self):
        try:
            for xx in self.rows:
                for yyy in self.columns:
                    for zz in self.levels:
                        self.session.add(Slot(xx, yyy, zz))
        except Exception as e:
            print(f"An error ocurred while populating the database: {e}")
        else:
            print("Populating `warehouse` table...")
            self.session.commit()

    def close(self):
        self.session.close()
