import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from snapshots.snapshots_cli import import_files, list_snapshots, sync


def strip_whitespace(str):
    return str.replace(" ", "").replace("\t", "").replace("\n", "")


class TestListSnapshots(unittest.TestCase):

    @patch('snapshots.snapshots_cli.get_metadata_conn')
    def test_list_snapshots_with_data(self, mock_get_metadata_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__.return_value.cursor.return_value = mock_cursor
        mock_get_metadata_conn.return_value = mock_conn

        expected_query = """
            SELECT created_on, file_name
            FROM snapshots_metadata;
        """
        sample_rows = [(datetime(2022, 1, 1), 'snapshot_20230101.csv'),
                       (datetime(2022, 1, 2), 'snapshot_20230102.csv')]
        sample_description = (('created_on',), ('file_name',))

        with patch('builtins.print') as mock_print:
            mock_cursor_context = mock_cursor.__enter__.return_value

            mock_cursor_context.fetchall.return_value = sample_rows
            mock_cursor_context.description = sample_description

            runner = CliRunner()
            runner.invoke(list_snapshots, [])

            mock_cursor_context.execute.assert_called_once()

            actual_query = mock_cursor_context.execute.call_args[0][0].strip()
            self.assertEqual(strip_whitespace(actual_query), strip_whitespace(expected_query))

            expected_output = ('+---------------------+-----------------------+\n'
                               '|     created_on      |       file_name       |\n'
                               '+---------------------+-----------------------+\n'
                               '| 2022-01-01 00:00:00 | snapshot_20230101.csv |\n'
                               '| 2022-01-02 00:00:00 | snapshot_20230102.csv |\n'
                               '+---------------------+-----------------------+')
            mock_print.assert_called_once_with(expected_output)

    @patch('snapshots.snapshots_cli.get_metadata_conn')
    def test_list_snapshots_with_no_data(self, mock_get_metadata_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.__enter__.return_value.cursor.return_value = mock_cursor
        mock_get_metadata_conn.return_value = mock_conn

        expected_query = """
            SELECT created_on, file_name
            FROM snapshots_metadata;
        """
        sample_description = (('created_on',), ('file_name',))

        with patch('builtins.print') as mock_print:
            mock_cursor_context = mock_cursor.__enter__.return_value

            mock_cursor_context.fetchall.return_value = []
            mock_cursor_context.description = sample_description

            runner = CliRunner()
            runner.invoke(list_snapshots, [])

            mock_cursor_context.execute.assert_called_once()

            actual_query = mock_cursor_context.execute.call_args[0][0].strip()
            self.assertEqual(strip_whitespace(actual_query), strip_whitespace(expected_query))

            mock_print.assert_called_once_with('No snapshots imported yet')


class TestSync(unittest.TestCase):

    def test_sync_missing_database_option(self):
        runner = CliRunner()

        result = runner.invoke(sync, ['--data-dir', 'test_data'])

        expected_error_message = ('Usage: sync [OPTIONS]\n'
                                  'Try \'sync --help\' for help.\n\n'
                                  'Error: Missing option \'--database\'.\n')

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn(expected_error_message, result.output)

    def test_sync_missing_data_dir_option(self):
        runner = CliRunner()

        result = runner.invoke(sync, ['--database', 'localhost:5432'])

        expected_error_message = ('Usage: sync [OPTIONS]\n'
                                  'Try \'sync --help\' for help.\n\n'
                                  'Error: Missing option \'--data-dir\'.\n')

        self.assertNotEqual(result.exit_code, 0)  # Ensure command fails
        self.assertIn(expected_error_message, result.output)


class TestImportFiles(unittest.TestCase):

    def test_import_files_missing_database(self):
        # Test case for missing database argument
        csv_files = ['snapshot.csv']

        # Call the import_files command using CliRunner
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('snapshot.csv', 'w') as f:
                f.write('Hello World!')

            result = runner.invoke(import_files, csv_files)

        # Check that the command fails with a click.exceptions.MissingParameter exception
        expected_error_message = ("Usage: import [OPTIONS] CSV_FILES...\n"
                                  "Try 'import --help' for help.\n\n"
                                  "Error: Missing option '--database'.\n")

        self.assertIn(expected_error_message, result.output)
        self.assertEqual(result.exit_code, 2)

    def test_import_files_file_does_not_exist(self):
        csv_files = ['file1.csv', 'file2.csv']
        database = 'localhost:5432'

        # Call the import_files command using CliRunner
        runner = CliRunner()
        result = runner.invoke(import_files, ['--database', database] + csv_files)

        # Check that the command fails with a click.exceptions.MissingParameter exception
        expected_error_message = ("Usage: import [OPTIONS] CSV_FILES...\n"
                                  "Try 'import --help' for help.\n\n"
                                  "Error: Invalid value for 'CSV_FILES...': Path 'file1.csv' does not exist.\n")

        self.assertIn(expected_error_message, result.output)
        self.assertEqual(result.exit_code, 2)

    def test_import_files_missing_csv_files(self):
        # Test case for missing csv_files argument
        database = 'localhost:5432'

        # Call the import_files command using CliRunner
        runner = CliRunner()
        result = runner.invoke(import_files, ['--database', database])

        # Check that the command fails with a click.exceptions.MissingParameter exception
        expected_error_message = ("Usage: import [OPTIONS] CSV_FILES...\n"
                                  "Try 'import --help' for help.\n\n"
                                  "Error: Missing argument 'CSV_FILES...'.\n")

        self.assertIn(expected_error_message, result.output)
        self.assertEqual(result.exit_code, 2)


if __name__ == '__main__':
    unittest.main()
