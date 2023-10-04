"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""
import os

from ml_git import log
from ml_git.constants import REFS_CLASS_NAME, EntityType
from ml_git.ml_git_message import output_messages
from ml_git.utils import ensure_path_exists, yaml_save, yaml_load


class Refs(object):
    def __init__(self, refspath, spec, repotype=EntityType.DATASETS.value):
        self._repotype = repotype
        self._spec = spec
        self._path = os.path.join(refspath, spec)
        ensure_path_exists(self._path)

    def update_head(self, tag, sha):
        refhead = os.path.join(self._path, 'HEAD')
        log.debug(output_messages['DEBUG_SETTING_HEAD'] % (self._spec, tag, sha), class_name=REFS_CLASS_NAME)
        yaml_save({tag: sha}, refhead)

    def head(self):
        refhead = os.path.join(self._path, 'HEAD')
        jr = yaml_load(refhead)
        keys = list(jr.keys())
        if len(keys) < 1:
            return None, None
        tag = keys[0]
        sha = jr[tag]
        return tag, sha

    def branch(self):
        return self.head()
