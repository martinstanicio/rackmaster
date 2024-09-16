from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from config import columns, db_url, levels, rows
from slot import Slot

engine = create_engine(db_url)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# if `warehouse` table is empty, it needs to be populated
first_time = len(session.query(Slot).all()) == 0
if first_time:
    try:
        for xx in rows:
            for yyy in columns:
                for zz in levels:
                    session.add(Slot(xx, yyy, zz))
    except Exception as e:
        print(f"An error ocurred while populating the database: {e}")
    else:
        print("Populating `warehouse` table...")
        session.commit()
