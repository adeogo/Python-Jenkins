import sqlite3
import datetime
from jenkinsapi.jenkins import Jenkins

# Database
conn = sqlite3.connect('api.db')
cursor = conn.cursor()


def get_server_instance():
    jenkins_url = 'http://localhost:8080'
    server = Jenkins(jenkins_url, username='adeogo', password='111111')
    return server


"""Get job details of each job on the Jenkins instance"""


def insert_job_details():
    server = get_server_instance()
    for j in server.get_jobs():
        job_instance = server.get_job(j[0])
        job_name = job_instance.name
        job_running = job_instance.is_running()  # Boolean
        job_enabled = job_instance.is_enabled()  # Boolean
        checked = str(datetime.datetime.utcnow())
        sql_insert = "INSERT INTO jobs VALUES (?, ?, ?, ?)"
        data = [
            (job_name, job_running, job_enabled, checked)
        ]
        cursor.executemany(sql_insert, data)
        conn.commit()


insert_job_details()

sql_show = "Select * FROM jobs"
cursor.execute(sql_show)
print(cursor.fetchall())
