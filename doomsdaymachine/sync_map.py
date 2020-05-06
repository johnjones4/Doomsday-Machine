import sqlite3
import os.path as path

class SyncMap:
    def __init__(self, job):
        self.connection = sqlite3.connect(path.join(job["output_folder"], "syncmap.sqlite3"))
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS resources (resource TEXT UNIQUE NOT NULL, last_modified NUMBER NOT NULL)")

    def get_last_modified(self, resource):
        self.cursor.execute("SELECT last_modified FROM resources WHERE resource=?", (resource, ))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0

    def set_last_modified(self, resource, last_modified):
        self.cursor.execute("SELECT last_modified FROM resources WHERE resource=?", (resource, ))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("UPDATE resources SET last_modified=? WHERE resource=?", (last_modified, resource))
        else:
            self.cursor.execute("INSERT INTO resources (last_modified, resource) VALUES (?, ?)", (last_modified, resource))

    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
