import sqlite3
import os.path as path

class SyncMap2:
    def __init__(self, job):
        self.connection = sqlite3.connect(path.join(job["output_folder"], "syncmap.sqlite3"))
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS resources (resource TEXT UNIQUE NOT NULL, signature TEXT NOT NULL)")

    def get_signature(self, resource):
        self.cursor.execute("SELECT signature FROM resources WHERE resource=?", (resource, ))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def set_signature(self, resource, signature):
        self.cursor.execute("SELECT signature FROM resources WHERE resource=?", (resource, ))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("UPDATE resources SET signature=? WHERE resource=?", (signature, resource))
        else:
            self.cursor.execute("INSERT INTO resources (signature, resource) VALUES (?, ?)", (signature, resource))

    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
