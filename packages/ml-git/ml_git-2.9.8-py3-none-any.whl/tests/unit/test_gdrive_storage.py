"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import unittest

import pytest

from ml_git.storages.google_drive_storage import GoogleDriveStorage


@pytest.mark.usefixtures('tmp_dir', 'switch_to_test_dir')
class GdriveStoreTestCases(unittest.TestCase):

    def test_get_file_id_from_url(self):
        file_url = 'https://drive.google.com/file/d/id_1/view?usp=sharing'
        folder_url = 'https://drive.google.com/drive/folders/id_2?usp=sharing'
        download_url = 'https://drive.google.com/uc?id=id_3'

        self.assertEqual(GoogleDriveStorage.get_file_id_from_url(file_url), 'id_1')
        self.assertEqual(GoogleDriveStorage.get_file_id_from_url(folder_url), 'id_2')
        self.assertEqual(GoogleDriveStorage.get_file_id_from_url(download_url), 'id_3')
