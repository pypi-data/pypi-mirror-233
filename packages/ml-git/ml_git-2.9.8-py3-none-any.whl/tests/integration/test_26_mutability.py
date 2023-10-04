"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git.ml_git_message import output_messages
from ml_git.spec import get_spec_key
from tests.integration.commands import MLGIT_ADD, MLGIT_COMMIT, MLGIT_PUSH, MLGIT_UPDATE, MLGIT_CHECKOUT
from tests.integration.helper import ML_GIT_DIR, create_spec, create_file, DATASETS, MODELS, LABELS, DATASET_TAG, STRICT, MUTABLE, FLEXIBLE
from tests.integration.helper import check_output, clear, init_repository, ERROR_MESSAGE, yaml_processor


@pytest.mark.usefixtures('tmp_dir', 'aws_session')
class MutabilityAcceptanceTests(unittest.TestCase):

    def _create_entity_with_mutability(self, entity_type, mutability_type):
        init_repository(entity_type, self)
        workspace = os.path.join(self.tmp_dir, entity_type, entity_type + '-ex')
        create_spec(self, entity_type, self.tmp_dir, 1, mutability_type)
        os.makedirs(os.path.join(workspace, 'data'))

        create_file(workspace, 'file1', '0')
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ADD % (entity_type, entity_type+'-ex', '')))

        self.assertIn(output_messages['INFO_COMMIT_REPO'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'metadata'), entity_type+'-ex'),
                      check_output(MLGIT_COMMIT % (entity_type, entity_type + '-ex', '')))

        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_PUSH % (entity_type, entity_type+'-ex')))
        clear(os.path.join(self.tmp_dir, ML_GIT_DIR))
        clear(workspace)
        clear(os.path.join(self.tmp_dir, entity_type))

    def _checkout_entity(self, entity_type, tag=DATASET_TAG):
        init_repository(entity_type, self)
        self.assertIn(output_messages['INFO_MLGIT_PULL'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'metadata')),
                      check_output(MLGIT_UPDATE % entity_type))

        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_CHECKOUT % (entity_type, tag)))

    def _verify_mutability(self, entity_type, mutability_type, spec_with_categories):
        with open(spec_with_categories) as y:
            ws_spec = yaml_processor.load(y)
            self.assertEqual(ws_spec[entity_type]['mutability'], mutability_type)
        return ws_spec

    def _change_mutability(self, entity_type, mutability_type, spec_with_categories, ws_spec):
        with open(spec_with_categories, 'w') as y:
            ws_spec[entity_type]['mutability'] = mutability_type
            ws_spec[entity_type]['version'] = 2
            yaml_processor.dump(ws_spec, y)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_mutability_strict_push(self):
        entity_type = DATASETS
        self._create_entity_with_mutability(entity_type, STRICT)
        self._checkout_entity(entity_type)

        spec_with_categories = os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', entity_type + '-ex.spec')

        entity_spec_key = get_spec_key(entity_type)
        ws_spec = self._verify_mutability(entity_spec_key, STRICT, spec_with_categories)
        self._change_mutability(entity_spec_key, FLEXIBLE, spec_with_categories, ws_spec)

        create_file(os.path.join(entity_type, entity_type+'-ex'), 'file2', '012')

        self.assertIn(output_messages['ERROR_MUTABILITY_CANNOT_CHANGE'], check_output(MLGIT_ADD % (entity_type, entity_type+'-ex', '')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_mutability_flexible_push(self):
        entity_type = MODELS
        self._create_entity_with_mutability(entity_type, FLEXIBLE)
        self._checkout_entity(entity_type, 'computer-vision__images__models-ex__1')

        spec_with_categories = os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', entity_type + '-ex.spec')

        entity_spec_key = get_spec_key(entity_type)
        ws_spec = self._verify_mutability(entity_spec_key, FLEXIBLE, spec_with_categories)
        self._change_mutability(entity_spec_key, STRICT, spec_with_categories, ws_spec)

        create_file(os.path.join(self.tmp_dir, entity_type, entity_type+'-ex'), 'file2', '012')

        self.assertIn(output_messages['ERROR_MUTABILITY_CANNOT_CHANGE'], check_output(MLGIT_ADD % (entity_type, entity_type+'-ex', '')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_mutability_mutable_push(self):
        entity_type = LABELS
        self._create_entity_with_mutability(entity_type, MUTABLE)
        self._checkout_entity(entity_type, 'computer-vision__images__labels-ex__1')

        spec_with_categories = os.path.join(self.tmp_dir, entity_type,  entity_type + '-ex', entity_type + '-ex.spec')

        entity_spec_key = get_spec_key(entity_type)
        ws_spec = self._verify_mutability(entity_spec_key, MUTABLE, spec_with_categories)
        self._change_mutability(entity_spec_key, STRICT, spec_with_categories, ws_spec)

        create_file(os.path.join(self.tmp_dir, entity_type, entity_type+'-ex'), 'file2', '012')

        self.assertIn(output_messages['ERROR_MUTABILITY_CANNOT_CHANGE'], check_output(MLGIT_ADD % (entity_type, entity_type+'-ex', '')))
