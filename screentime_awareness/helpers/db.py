import psycopg2 as psql
import json


class DBC:
    def __init__(self):
        with open('screentime_awareness/helpers/db.json') as file:
            self.db_info = json.load(file)
            print(self.db_info)
            print(self.db_info['database'])


