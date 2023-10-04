"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_PUSH, MLGIT_TAG_LIST, MLGIT_COMMIT
from tests.integration.helper import check_output, init_repository, add_file, ML_GIT_DIR, create_spec, DATASETS, LABELS, \
    MODELS


@pytest.mark.usefixtures('tmp_dir', 'aws_session')
class ListTagAcceptanceTests(unittest.TestCase):

    def _list_tag_entity(self, entity_type):
        init_repository(entity_type, self)
        add_file(self, entity_type, '--bumpversion', 'new')
        self.assertIn(output_messages['INFO_COMMIT_REPO'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'metadata'), entity_type+'-ex'),
                      check_output(MLGIT_COMMIT % (entity_type, entity_type+'-ex', '')))
        check_output(MLGIT_PUSH % (entity_type, entity_type+'-ex'))
        self.assertIn('computer-vision__images__' + entity_type + '-ex__1',
                      check_output(MLGIT_TAG_LIST % (entity_type, entity_type+'-ex')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_list_all_tag_dataset(self):
        self._list_tag_entity(DATASETS)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_list_all_tag_labels(self):
        self._list_tag_entity(LABELS)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_list_all_tag_model(self):
        self._list_tag_entity(MODELS)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_04_list_tags_without_similar_tags(self):
        self._list_tag_entity(DATASETS)
        entity_type = DATASETS
        similar_entity = 'datasets-ex2'
        workspace = os.path.join(DATASETS, similar_entity)
        os.makedirs(workspace, exist_ok=True)
        create_spec(self, DATASETS, self.tmp_dir, artifact_name=similar_entity)
        add_file(self, DATASETS, '--bumpversion', 'new', artifact_name=similar_entity)
        self.assertIn(output_messages['INFO_COMMIT_REPO'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, DATASETS, 'metadata'), similar_entity),
                      check_output(MLGIT_COMMIT % (DATASETS, similar_entity, '')))
        check_output(MLGIT_PUSH % (DATASETS, similar_entity))
        self.assertNotIn(similar_entity,
                         check_output(MLGIT_TAG_LIST % (entity_type, entity_type + '-ex')))
        self.assertIn(similar_entity,
                      check_output(MLGIT_TAG_LIST % (entity_type, similar_entity)))
