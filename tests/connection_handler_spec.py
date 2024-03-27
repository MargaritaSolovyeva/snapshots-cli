import os
import unittest
from unittest.mock import patch


class TestConnectionHandler(unittest.TestCase):

    @patch('psycopg2.connect')
    @patch.dict(os.environ, {
        'SNAPSHOTS_DB_USERNAME': 'test_user',
        'SNAPSHOTS_DB_PASSWORD': 'test_password'
    })
    def test_get_snapshots_conn(self, mock_connect):
        from snapshots.connection_handler import get_snapshots_conn

        get_snapshots_conn('localhost:5432')

        # Assertions
        mock_connect.assert_called_once_with(
            host='localhost',
            port='5432',
            dbname='snapshots_db',
            user='test_user',
            password='test_password'
        )

    @patch('psycopg2.connect')
    @patch.dict(os.environ, {
        'METADATA_DB_USERNAME': 'test_user',
        'METADATA_DB_PASSWORD': 'test_password',
        'METADATA_DB_HOST': 'localhost',
        'METADATA_DB_PORT': '5432'
    })
    def test_get_metadata_conn(self, mock_connect):
        from snapshots.connection_handler import get_metadata_conn

        get_metadata_conn()

        mock_connect.assert_called_once_with(
            host='localhost',
            port='5432',
            dbname='metadata_db',
            user='test_user',
            password='test_password'
        )


if __name__ == '__main__':
    unittest.main()
