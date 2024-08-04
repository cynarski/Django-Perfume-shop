# load_data.py
import psycopg2
from django.conf import settings

def load_data():
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST']
    )
    cur = conn.cursor()

    with open('database/dump_postgres.sql', 'r') as f:
        cur.execute(f.read())
        print("Data loaded successfully")

    conn.commit()
    cur.close()
    conn.close()
