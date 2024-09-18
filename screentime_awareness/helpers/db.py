import psycopg2 as psql
import json


class DBC:
    def __init__(self):
        with open('screentime_awareness/helpers/db.json') as file:
            self.db_info = json.load(file)

    def open_connection(self):
        return psql.connect(database=self.db_info['database'], user=self.db_info['user'],
                            password=self.db_info['password'], host=self.db_info['host'], port=self.db_info['port'])

    def write(self, sql: str):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def select(self, sql: str):
        conn = self.open_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        conn.close()
        return records
