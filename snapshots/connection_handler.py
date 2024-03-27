import os
import psycopg2


def get_snapshots_conn(database):
    db_host, db_port = database.split(':')

    user = os.getenv('SNAPSHOTS_DB_USERNAME')
    password = os.getenv('SNAPSHOTS_DB_PASSWORD')

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname='snapshots_db',
        user=user,
        password=password
    )

    return conn


def get_metadata_conn():
    user = os.getenv('METADATA_DB_USERNAME')
    password = os.getenv('METADATA_DB_PASSWORD')
    host = os.getenv('METADATA_DB_HOST')
    port = os.getenv('METADATA_DB_PORT')

    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname='metadata_db',
        user=user,
        password=password
    )

    return conn
