
import sys
import unittest
import importlib.util

from datetime import datetime


def run_test_cases():
    unittest.main(argv=[''], verbosity=2)


class TestMetalArchivesDirectory(unittest.TestCase):

    def test_releases_endpoint(self):
        spec = importlib.util.spec_from_file_location('metalarchivist.export', './metalarchivist/export/__init__.py')
        self.assertIsNotNone(spec)

        export = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(export)

        sys.modules['metalarchivist.export'] = export
        spec.loader.exec_module(export)

        self.assertIn('MetalArchivesDirectory', dir(export))

        range_start = datetime(1990, 1, 1).strftime('%Y-%m-%d')
        range_stop = datetime(1990, 12, 31).strftime('%Y-%m-%d')

        self.assertEqual(range_start, '1990-01-01')
        self.assertEqual(range_stop, '1990-12-31')

        expected_endpoint = ('https://www.metal-archives.com/release/ajax-upcoming/json/1'
                             '?sEcho=0&iDisplayStart=0&iDisplayLength=100'
                             '&fromDate=1990-01-01&toDate=1990-12-31')

        actual_endpoint = export.MetalArchivesDirectory.upcoming_releases(0, 0, 100, range_start, range_stop)

        self.assertEqual(expected_endpoint, actual_endpoint)


class TestReleases(unittest.TestCase):

    def test_releases(self):
        spec = importlib.util.spec_from_file_location('metalarchivist.export', './metalarchivist/export/__init__.py')
        self.assertIsNotNone(spec)

        export = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(export)

        sys.modules['metalarchivist.export'] = export
        spec.loader.exec_module(export)

        self.assertIn('Releases', dir(export))

        upcoming_component_attributes = dir(export.Releases)
        self.assertIn('get_all', upcoming_component_attributes)
        self.assertIn('get_upcoming', upcoming_component_attributes)
        self.assertIn('get_range', upcoming_component_attributes)

    def test_upcoming(self):
        spec = importlib.util.spec_from_file_location('metalarchivist.export', './metalarchivist/export/__init__.py')
        self.assertIsNotNone(spec)

        export = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(export)

        sys.modules['metalarchivist.export'] = export
        spec.loader.exec_module(export)

        releases = export.Releases.get_upcoming()
        self.assertIsNotNone(releases)
        self.assertIsInstance(releases, export.ReleasePage)

        total_records = releases.total_records
        total_display_records = releases.total_display_records
        self.assertEqual(total_records, total_display_records)

        releases_attributes = dir(releases)
        self.assertIn('total_records', releases_attributes)
        self.assertIn('total_display_records', releases_attributes)
        self.assertIn('echo', releases_attributes)
        self.assertIn('data', releases_attributes)

        self.assertEqual(releases.echo, 0)

        data = releases.data
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), total_records)

        album_release = data.pop()
        self.assertIsInstance(album_release, export.AlbumRelease)

    def test_range(self):
        spec = importlib.util.spec_from_file_location('metalarchivist.export', './metalarchivist/export/__init__.py')
        self.assertIsNotNone(spec)

        export = importlib.util.module_from_spec(spec)
        self.assertIsNotNone(export)

        sys.modules['metalarchivist.export'] = export
        spec.loader.exec_module(export)

        releases = export.Releases.get_range(datetime(1990, 1, 1), datetime(1990, 12, 31))
        self.assertIsNotNone(releases)
        self.assertIsInstance(releases, export.ReleasePage)

        releases_attributes = dir(releases)
        self.assertIn('total_records', releases_attributes)
        self.assertIn('total_display_records', releases_attributes)
        self.assertIn('echo', releases_attributes)
        self.assertIn('data', releases_attributes)

        total_records = releases.total_records
        total_display_records = releases.total_display_records
        self.assertEqual(total_records, total_display_records)

        self.assertEqual(releases.echo, 0)

        data = releases.data
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), total_records)

        album_release = data.pop()
        self.assertIsInstance(album_release, export.AlbumRelease)


if __name__ == '__main__':
    run_test_cases()
