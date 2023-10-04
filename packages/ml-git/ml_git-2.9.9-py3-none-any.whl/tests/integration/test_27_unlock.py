"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest
from stat import S_IREAD, S_IRGRP, S_IROTH

import pytest

from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_ADD, MLGIT_UNLOCK
from tests.integration.helper import check_output, ERROR_MESSAGE, DATASETS, DATASET_NAME, STRICT, FLEXIBLE, MUTABLE
from tests.integration.helper import create_spec, init_repository


@pytest.mark.usefixtures('tmp_dir')
class UnlockAcceptanceTests(unittest.TestCase):
    file = os.path.join('data', 'file1')
    workspace = os.path.join(DATASETS, DATASET_NAME)
    file_path = os.path.join(workspace, file)

    def set_up_unlock(self, entity_type, mutability_type):
        init_repository(entity_type, self)
        workspace = os.path.join(entity_type, entity_type+'-ex')
        create_spec(self, entity_type, self.tmp_dir, 1, mutability=mutability_type)

        os.makedirs(os.path.join(workspace, 'data'))

        with open(os.path.join(workspace, self.file), 'w') as file:
            file.write('0' * 2048)

        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ADD % (entity_type, entity_type+'-ex', '--bumpversion')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_unlock_in_strict_mode(self):
        self.set_up_unlock(DATASETS, STRICT)

        self.assertEqual(2, os.stat(self.file_path).st_nlink)
        self.assertIn(output_messages['INFO_MUTABILITY_CANNOT_BE_STRICT'], check_output(MLGIT_UNLOCK % (DATASETS, DATASET_NAME, 'data/file1')))
        self.assertEqual(2, os.stat(self.file_path).st_nlink)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_unlock_wrong_file(self):
        self.set_up_unlock(DATASETS, FLEXIBLE)

        self.assertEqual(2, os.stat(self.file_path).st_nlink)
        self.assertIn(output_messages['ERROR_FILE_NOT_FOUND'] % 'data/file10',
                      check_output(MLGIT_UNLOCK % (DATASETS, DATASET_NAME, 'data/file10')))
        self.assertEqual(2, os.stat(self.file_path).st_nlink)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_unlock_flexible_mode(self):
        self.set_up_unlock(DATASETS, FLEXIBLE)

        self.assertEqual(2, os.stat(self.file_path).st_nlink)
        self.assertIn(output_messages['INFO_PERMISSIONS_CHANGED_FOR'] % 'data/file1', check_output(MLGIT_UNLOCK % (DATASETS, DATASET_NAME, 'data/file1')))
        self.assertTrue(os.access(self.file_path, os.W_OK))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_04_unlock_mutable_mode(self):
        self.set_up_unlock(DATASETS, MUTABLE)

        os.chmod(self.file_path, S_IREAD | S_IRGRP | S_IROTH)
        self.assertEqual(1, os.stat(self.file_path).st_nlink)
        self.assertIn(output_messages['INFO_PERMISSIONS_CHANGED_FOR'] % 'data/file1', check_output(MLGIT_UNLOCK % (DATASETS, DATASET_NAME, 'data/file1')))
        self.assertEqual(1, os.stat(self.file_path).st_nlink)
        self.assertTrue(os.access(self.file_path, os.W_OK))
