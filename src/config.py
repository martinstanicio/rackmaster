import os

from appdirs import user_data_dir

data_dir = user_data_dir(appname="RackMaster", appauthor="Martín Stanicio")
print(data_dir)
os.makedirs(data_dir, exist_ok=True)

db_path = os.path.join(data_dir, "rackmaster.db")
db_url = f"sqlite:///{db_path}"

min_row = 50
max_row = 53
min_column = 1
max_column = 90
min_level = 1
max_level = 5

rows = [i for i in range(min_row, max_row + 1)]
columns = [i for i in range(min_column, max_column + 1)]
levels = [i for i in range(min_level, max_level + 1)]
