import csv
import time
import os
import re
from datetime import datetime
from tabulate import tabulate
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import click

from snapshots.connection_handler import get_metadata_conn, get_snapshots_conn
from snapshots.monitoring import monitored


def import_csv(database, csv_files):
    with get_snapshots_conn(database) as conn:
        with conn.cursor() as cursor:

            for csv_file in csv_files:
                with open(csv_file, 'r') as file:
                    reader = csv.DictReader(file)
                    data = []
                    for row in reader:
                        data.append(row)

                    insert_query = """
                    INSERT INTO snapshots (user_id, name, store_name, credit_limit)
                    VALUES (%(user_id)s, %(name)s, %(store_name)s, %(credit_limit)s)
                    ON CONFLICT (user_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    store_name = EXCLUDED.store_name,
                    credit_limit = EXCLUDED.credit_limit;
                    """

                    cursor.executemany(insert_query, data)

            log_snapshots(csv_files)
            print(f"Inserted data from {csv_files} into database")


def log_snapshots(csv_files):
    created_on = datetime.now()
    data = []

    for csv_file in csv_files:
        file_name = re.sub(r'[^/]+$', r'\1', csv_file)
        data.append({'created_on': created_on, 'file_name': file_name})

    insert_query = """
                INSERT INTO snapshots_metadata (created_on, file_name)
                VALUES (%(created_on)s, %(file_name)s);
                """

    with get_metadata_conn() as conn:
        with conn.cursor() as curs:
            curs.executemany(insert_query, data)


class SnapshotHandler(FileSystemEventHandler):
    def __init__(self, database, data_dir):
        super().__init__()
        self.database = database
        self.data_dir = data_dir

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith('.csv'):
            print(f"Detected new snapshot file: {event.src_path}")
            import_csv(self.database, [event.src_path])


@click.group()
def snapshots():
    pass


@click.command(name='import')
@click.option('--database',
              required=True,
              help='PostgreSQL database host:port string (e.g., localhost:5432)')
@click.argument('csv_files', nargs=-1, type=click.Path(exists=True), required=True)
@monitored
def import_files(database, csv_files):
    import_csv(database, csv_files)


@click.command(name='list')
@monitored
def list_snapshots():
    select_query = """
        SELECT created_on, file_name
        FROM snapshots_metadata;
        """

    with get_metadata_conn() as conn:
        with conn.cursor() as curs:
            curs.execute(select_query)
            rows = curs.fetchall()

            if not rows:
                print('No snapshots imported yet')
                return

            columns = [desc[0] for desc in curs.description]

            print(tabulate(rows, headers=columns, tablefmt='pretty'))


@click.command(name='sync')
@click.option('--database', required=True, help='PostgreSQL database connection string (e.g., localhost:5432)')
@click.option('--data-dir', required=True, help='Directory to monitor for snapshot files')
@monitored
def sync(database, data_dir):
    observer = Observer()
    absolute_path = os.path.abspath(data_dir)

    observer.schedule(SnapshotHandler(database, data_dir), path=absolute_path)
    observer.start()

    try:
        print(f"Watching directory {data_dir} for snapshot files...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    snapshots.add_command(list_snapshots)
    snapshots.add_command(import_files)
    snapshots.add_command(sync)
    snapshots()
