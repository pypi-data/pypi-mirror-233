"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git import api
from ml_git.constants import STORAGE_LOG
from tests.integration.helper import ML_GIT_DIR, create_spec, DATASETS, DATASET_NAME, MODELS, LABELS, STRICT
from tests.integration.helper import init_repository


@pytest.mark.usefixtures('tmp_dir')
class APIAcceptanceTests(unittest.TestCase):

    def create_file(self, path, file_name, code):
        file = os.path.join('data', file_name)
        with open(os.path.join(path, file), 'w') as file:
            file.write(code * 2048)

    def set_up_test(self, entity):
        init_repository(entity, self)
        workspace = os.path.join(self.tmp_dir, entity, entity+'-ex')
        os.makedirs(workspace, exist_ok=True)
        create_spec(self, entity, self.tmp_dir, 20, STRICT)
        os.makedirs(os.path.join(workspace, 'data'), exist_ok=True)

        self.create_file(workspace, 'file1', '0')
        self.create_file(workspace, 'file2', '1')
        self.create_file(workspace, 'file3', 'a')
        self.create_file(workspace, 'file4', 'b')

        api.add(entity, entity+'-ex', bumpversion=True, fsck=False, file_path=['file'])
        api.commit(entity, entity+'-ex')

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_01_dataset_push(self):
        self.set_up_test(DATASETS)
        cache = os.path.join(self.tmp_dir, ML_GIT_DIR, DATASETS, 'cache')
        api.push(DATASETS, DATASET_NAME, 2, False)
        self.assertTrue(os.path.exists(cache))
        self.assertFalse(os.path.isfile(os.path.join(cache, STORAGE_LOG)))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_02_model_push(self):
        self.set_up_test(MODELS)
        cache = os.path.join(self.tmp_dir, ML_GIT_DIR, MODELS, 'cache')
        api.push(MODELS, 'models-ex', 2, False)
        self.assertTrue(os.path.exists(cache))
        self.assertFalse(os.path.isfile(os.path.join(cache, STORAGE_LOG)))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_03_labels_push(self):
        self.set_up_test(LABELS)
        cache = os.path.join(self.tmp_dir, ML_GIT_DIR, LABELS, 'cache')
        api.push(LABELS, 'labels-ex', 2, False)
        self.assertTrue(os.path.exists(cache))
        self.assertFalse(os.path.isfile(os.path.join(cache, STORAGE_LOG)))
