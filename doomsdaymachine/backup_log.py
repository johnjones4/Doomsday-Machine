import sqlite3
import time
from uuid import uuid4

class BackupLog():
    def __init__(self, config):
        self.connection = sqlite3.connect(config["backup_log_path"])
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS log (job TEXT NOT NULL, job_instance_id TEXT NOT NULL, event TEXT NOT NULL, timestamp NUMBER NOT NULL)")

    def start_job(self, job):
        start_time = time.time()
        job_instance_id = str(uuid4())
        self.cursor.execute("INSERT INTO log (job, job_instance_id, event, timestamp) VALUES (?, ?, 'start', ?)", (job, job_instance_id, start_time))
        self.connection.commit()
        return (start_time, job_instance_id)

    def end_job(self, job, job_instance_id):
        end_time = time.time()
        self.cursor.execute("INSERT INTO log (job, job_instance_id, event, timestamp) VALUES (?, ?, 'end', ?)", (job, job_instance_id, end_time))
        self.connection.commit()
        return end_time

    def get_active_job(self):
        self.cursor.execute("SELECT job, event, timestamp FROM log ORDER BY timestamp DESC LIMIT 1")
        row = self.cursor.fetchone()
        if row and row[1] == "start":
            return dict(
                job=row[0],
                start_time=row[2]
            )
        return dict(
            job=None,
            start_time=None
        )

    def get_last_execution_time(self, job):
        self.cursor.execute("SELECT event, timestamp FROM log WHERE job = ? ORDER BY timestamp DESC LIMIT 2", (job, ))
        rows = self.cursor.fetchall()
        if len(rows) != 2 or rows[0][0] == "start" or rows[1][0] == "end":
            return None
        return rows[0][1] - rows[1][1]
