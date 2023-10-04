"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_INIT, MLGIT_REMOTE_ADD
from tests.integration.helper import check_output, ML_GIT_DIR, GIT_PATH, yaml_processor, DATASETS, LABELS, MODELS


@pytest.mark.usefixtures('tmp_dir')
class AddRemoteAcceptanceTests(unittest.TestCase):

    def _add_remote(self, entity_type):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        self.assertIn(output_messages['INFO_ADD_REMOTE'] % (os.path.join(self.tmp_dir, GIT_PATH), entity_type),
                      check_output(MLGIT_REMOTE_ADD % (entity_type, os.path.join(self.tmp_dir, GIT_PATH))))
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(os.path.join(self.tmp_dir, GIT_PATH), config[entity_type]['git'])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_01_add_remote_dataset(self):
        self._add_remote(DATASETS)

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_02_add_remote_labels(self):
        self._add_remote(LABELS)

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_03_add_remote_model(self):
        self._add_remote(MODELS)

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_04_add_remote_subfolder(self):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        os.chdir(os.path.join(self.tmp_dir, ML_GIT_DIR))
        self.assertIn(output_messages['INFO_ADD_REMOTE'] % (GIT_PATH, DATASETS), check_output(MLGIT_REMOTE_ADD % (DATASETS, GIT_PATH)))
        self.check_remote_in_config(os.path.join('config.yaml'))

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_05_add_remote_uninitialized_directory(self):
        self.assertIn(output_messages['ERROR_NOT_IN_RESPOSITORY'], check_output(MLGIT_REMOTE_ADD % (DATASETS, GIT_PATH)))
        self.assertFalse(os.path.exists('.ml-git'))

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_06_change_remote_repository(self):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        self.assertIn(output_messages['INFO_ADD_REMOTE'] % (GIT_PATH, DATASETS), check_output(MLGIT_REMOTE_ADD % (DATASETS, GIT_PATH)))
        self.check_remote_in_config(os.path.join(ML_GIT_DIR, 'config.yaml'))
        output_message = check_output(MLGIT_REMOTE_ADD % (DATASETS, 'second_path'))
        self.assertIn(output_messages['WARN_HAS_CONFIGURED_REMOTE'], output_message)
        self.assertIn(output_messages['INFO_CHANGING_REMOTE'] % (GIT_PATH, 'second_path', DATASETS), output_message)
        self.check_remote_in_config(os.path.join(ML_GIT_DIR, 'config.yaml'), 'second_path')

    def check_remote_in_config(self, path, git_repo=GIT_PATH):
        with open(path, 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(git_repo, config[DATASETS]['git'])
