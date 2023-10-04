"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import shutil
import unittest

import boto3
import botocore
import pytest
from moto import mock_s3

from ml_git.file_system.index import MultihashIndex, FullIndex
from ml_git.file_system.local import LocalRepository
from ml_git.file_system.objects import Objects
from ml_git.storages.s3_storage import S3MultihashStorage, S3Storage
from ml_git.utils import ensure_path_exists, yaml_save, yaml_load
from tests.unit.conftest import S3

files_mock = {'zdj7Wm99FQsJ7a4udnx36ZQNTy7h4Pao3XmRSfjo4sAbt9g74': {'1.jpg'}}

testprofile = os.getenv('MLGIT_TEST_PROFILE', 'personal')
testregion = os.getenv('MLGIT_TEST_REGION', 'us-east-1')
testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-models')
testbucketname_2 = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
bucket = {
    'aws-credentials': {'profile': testprofile},
    'region': testregion
}
bucketname = testbucketname
bucketname_2 = testbucketname_2


@mock_s3
@pytest.mark.usefixtures('md5_fixture', 'tmp_dir', 'switch_to_test_dir', 'aws_session')
class S3StoreTestCases(unittest.TestCase):
    def setUp(self):
        client = boto3.client(
            S3,
            region_name='us-east-1',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
        )

        try:
            s3 = boto3.resource(
                S3,
                region_name='us-east-1',
                aws_access_key_id='fake_access_key',
                aws_secret_access_key='fake_secret_key',
            )
            s3.meta.client.head_bucket(Bucket=bucketname)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = '{bucket} should not exist.'.format(bucket=bucketname)
            raise EnvironmentError(err)
        client.create_bucket(Bucket=bucketname)
        client.create_bucket(Bucket=bucketname_2)

    def test_put(self):
        s3storage = S3MultihashStorage(bucketname, bucket, blocksize=1024 * 1024)
        k = 'think-hires.jpg'
        f = 'data/think-hires.jpg'
        self.assertFalse(s3storage.key_exists(k))
        self.assertEqual(s3storage.put(k, f), k)
        self.assertTrue(s3storage.key_exists(k))

    def test_get(self):
        s3storage = S3MultihashStorage(bucketname, bucket)
        k = 'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh'
        f = 'hdata/zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh'
        self.assertFalse(s3storage.key_exists(k))
        self.assertEqual(s3storage.put(k, f), k)
        self.assertTrue(s3storage.key_exists(k))
        fpath = os.path.join(self.tmp_dir, 's3.dat')
        self.assertTrue(s3storage.get(fpath, k))
        self.assertEqual(self.md5sum(fpath), self.md5sum(f))

    def test_push(self):
        indexpath = os.path.join(self.tmp_dir, 'index-test')
        mdpath = os.path.join(self.tmp_dir, 'metadata-test')
        objectpath = os.path.join(self.tmp_dir, 'objects-test')
        specpath = os.path.join(mdpath, 'vision-computing/images/dataset-ex')
        ensure_path_exists(indexpath)
        ensure_path_exists(specpath)
        shutil.copy('hdata/dataset-ex.spec', specpath + '/dataset-ex.spec')
        manifestpath = os.path.join(specpath, 'MANIFEST.yaml')
        yaml_save(files_mock, manifestpath)
        idx = MultihashIndex(specpath, indexpath, objectpath)
        idx.add('data-test-push-1/', manifestpath)
        fidx = FullIndex(specpath, indexpath)

        self.assertTrue(os.path.exists(indexpath))
        c = yaml_load('hdata/config.yaml')
        o = Objects(specpath, objectpath)
        o.commit_index(indexpath, self.tmp_dir)

        self.assertTrue(os.path.exists(objectpath))

        r = LocalRepository(c, objectpath)
        self.assertTrue(r.push(objectpath, specpath + '/dataset-ex.spec') == 0)
        self.assertTrue(len(fidx.get_index()) == 1)

    def test_list_files_from_path(self):
        s3storage = S3Storage(bucketname, bucket)
        k = 'path/think-hires.jpg'
        f = 'data/think-hires.jpg'
        s3storage.put(k, f)
        self.assertTrue(s3storage.key_exists('path/think-hires.jpg'))

        files = s3storage.list_files_from_path('path')
        self.assertEqual(files[0], 'path/think-hires.jpg')

        files = s3storage.list_files_from_path(None)
        self.assertEqual(files[0], 'path/think-hires.jpg')

    def test_get_object(self):
        s3storage = S3Storage(bucketname, bucket)
        k = 'path/think-hires.jpg'
        f = 'data/think-hires.jpg'

        self.assertFalse(s3storage.key_exists(k))

        s3storage.put(k, f)

        img = s3storage.get_object(k)

        with open(f, 'rb') as file:
            img2 = file.read()
            self.assertEqual(img, img2)

        s3storage._delete(k)

        self.assertRaises(Exception, s3storage.get_object, k)

    def test_put_object(self):
        s3storage = S3Storage(bucketname, bucket)
        f = 'data/think-hires.jpg'
        k = 'path/think-hires.jpg'

        self.assertFalse(s3storage.key_exists(k))

        with open(f, 'rb') as file:
            s3storage.put_object(k, file.read())

        self.assertTrue(s3storage.key_exists(k))

    def tearDown(self):
        s3 = boto3.resource(
            S3,
            region_name='eu-west-1',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
        )
        bucket = s3.Bucket(bucketname)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
