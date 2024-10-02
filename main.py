from src.config import columns, db_url, levels, rows
from src.db import Database
from ui.gui import GUI


def main() -> None:
    with Database(db_url, rows, columns, levels) as db:
        gui = GUI(db)
        gui.run()


if __name__ == "__main__":
    main()
