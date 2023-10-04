"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import filecmp
import os
import shutil
import unittest

import boto3
import botocore
import pytest
from moto import mock_s3

from ml_git.config import get_sample_config_spec, get_sample_spec
from ml_git.constants import DATASET_SPEC_KEY, MODEL_SPEC_KEY
from ml_git.file_system.cache import Cache
from ml_git.file_system.hashfs import MultihashFS
from ml_git.file_system.index import MultihashIndex, Status, FullIndex
from ml_git.file_system.local import LocalRepository
from ml_git.file_system.objects import Objects
from ml_git.sample import SampleValidate, SampleValidateException
from ml_git.storages.s3_storage import S3Storage
from ml_git.utils import yaml_load, yaml_save, ensure_path_exists, set_write_read
from tests.unit.conftest import MODELS, STRICT, S3

hs = {
    'zdj7WWsMkELZSGQGgpm5VieCWV8NxY5n5XEP73H4E7eeDMA3A',
    'zdj7We7Je5MRECsZUF7uptseHHPY29zGoqFsVHw6sbgv1MbWS',
    'zdj7WcMf5jG3dUpFVEqN38Rv2XAd6dNFuC91AvrQq4psha7qE',
    'zdj7WWG34cqLmcRe4CUEwevXr6TGdXPpM51yW85roL2LMs3PU',
    'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh'
}
testprofile = os.getenv('MLGIT_TEST_PROFILE', 'personal')
testregion = os.getenv('MLGIT_TEST_REGION', 'us-east-1')
testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')

files_mock = {'zdj7Wm99FQsJ7a4udnx36ZQNTy7h4Pao3XmRSfjo4sAbt9g74': {'1.jpg'},
              'zdj7WnVtg7ZgwzNxwmmDatnEoM3vbuszr3xcVuBYrcFD6XzmW': {'2.jpg'},
              'zdj7Wi7qy2o3kgUC72q2aSqzXV8shrererADgd6NTP9NabpvB': {'3.jpg'},
              'zdj7We7FUbukkozcTtYgcsSnLWGqCm2PfkK53nwJWLHEtuef4': {'6.jpg'},
              'zdj7WZzR8Tw87Dx3dm76W5aehnT23GSbXbQ9qo73JgtwREGwB': {'7.jpg'},
              'zdj7WfQCZgACUxwmhVMBp4Z2x6zk7eCMUZfbRDrswQVUY1Fud': {'8.jpg'},
              'zdj7WdjnTVfz5AhTavcpsDT62WiQo4AeQy6s4UC1BSEZYx4NP': {'9.jpg'},
              'zdj7WXiB8QrNVQ2VABPvvfC3VW6wFRTWKvFhUW5QaDx6JMoma': {'10.jpg'}}

bucket = {
    'aws-credentials': {'profile': testprofile},
    'region': testregion
}

DATA_IMG_1 = os.path.join('data', 'imghires.jpg')
DATA_IMG_2 = os.path.join('data', 'imghires2.jpg')
HDATA_IMG_1 = os.path.join('hdata', 'imghires.jpg')


@mock_s3
@pytest.mark.usefixtures('md5_fixture', 'tmp_dir', 'switch_to_test_dir', 'aws_session')
class LocalRepositoryTestCases(unittest.TestCase):

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
            s3.meta.client.head_bucket(Bucket=testbucketname)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = '{bucket} should not exist.'.format(bucket=testbucketname)
            raise EnvironmentError(err)
        client.create_bucket(Bucket=testbucketname)
        for h in hs:
            client.upload_file(Filename=os.path.join('hdata', h), Bucket=testbucketname, Key=h)

    def test_push(self):

        mlgit_dir = os.path.join(self.tmp_dir, '.ml-git')

        indexpath = os.path.join(mlgit_dir, 'index-test')
        mdpath = os.path.join(mlgit_dir, 'metadata-test')
        objectpath = os.path.join(mlgit_dir, 'objects-test')
        specpath = os.path.join(mdpath, 'vision-computing/images/dataset-ex')
        ensure_path_exists(specpath)
        ensure_path_exists(indexpath)
        shutil.copy('hdata/dataset-ex.spec', specpath + '/dataset-ex.spec')
        shutil.copy('hdata/config.yaml', mlgit_dir + '/config.yaml')
        manifestpath = os.path.join(specpath, 'MANIFEST.yaml')
        yaml_save({'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh': {'imghires.jpg'}}, manifestpath)

        # adds chunks to ml-git Index
        idx = MultihashIndex(specpath, indexpath, objectpath)
        idx.add('data-test-push/', manifestpath)

        fi = yaml_load(os.path.join(specpath, 'INDEX.yaml'))
        self.assertTrue(len(fi) > 0)
        self.assertTrue(os.path.exists(indexpath))

        o = Objects(specpath, objectpath)
        o.commit_index(indexpath, self.tmp_dir)

        self.assertTrue(os.path.exists(objectpath))
        c = yaml_load('hdata/config.yaml')
        r = LocalRepository(c, objectpath)
        r.push(objectpath, specpath + '/dataset-ex.spec')
        s3 = boto3.resource(
            S3,
            region_name='eu-west-1',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
        )
        for key in idx.get_index():
            self.assertIsNotNone(s3.Object(testbucketname, key))

    def test_fetch(self):
        mdpath = os.path.join(self.tmp_dir, 'metadata-test')
        testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
        config_spec = get_sample_config_spec(testbucketname, testprofile, testregion)
        dataset_spec = get_sample_spec(testbucketname)

        specpath = os.path.join(mdpath, 'vision-computing', 'images', 'dataset-ex')
        ensure_path_exists(specpath)
        yaml_save(dataset_spec, os.path.join(specpath, 'dataset-ex.spec'))

        manifestpath = os.path.join(specpath, 'MANIFEST.yaml')
        yaml_save({'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh': {'imghires.jpg'}}, manifestpath)

        objectpath = os.path.join(self.tmp_dir, 'objects-test')
        spec = 'vision-computing__images__dataset-ex__5'

        r = LocalRepository(config_spec, objectpath)
        r.fetch(mdpath, spec, None)

        fs = set()
        for root, dirs, files in os.walk(objectpath):
            for file in files:
                fs.add(file)

        self.assertEqual(len(hs), len(fs))
        self.assertTrue(len(hs.difference(fs)) == 0)

    def test_get_update_cache(self):
        hfspath = os.path.join(self.tmp_dir, 'objectsfs')
        ohfs = MultihashFS(hfspath)
        key = ohfs.put(HDATA_IMG_1)

        cachepath = os.path.join(self.tmp_dir, 'cachefs')
        cache = Cache(cachepath, '', '')

        testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
        c = get_sample_config_spec(testbucketname, testprofile, testregion)

        r = LocalRepository(c, hfspath)
        r._update_cache(cache, key)

        self.assertTrue(os.path.exists(cache.get_keypath(key)))
        self.assertEqual(self.md5sum(HDATA_IMG_1), self.md5sum(cache.get_keypath(key)))

    def test_get_update_links_wspace(self):
        wspath = os.path.join(self.tmp_dir, 'wspace')

        hfspath = os.path.join(self.tmp_dir, 'objectsfs')
        ohfs = MultihashFS(hfspath)
        key = ohfs.put(HDATA_IMG_1)
        fidx = FullIndex(self.tmp_dir, self.tmp_dir)
        cachepath = os.path.join(self.tmp_dir, 'cachefs')
        cache = Cache(cachepath, '', '')

        testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
        c = get_sample_config_spec(testbucketname, testprofile, testregion)

        r = LocalRepository(c, hfspath)
        r._update_cache(cache, key)

        mfiles = {}
        files = {DATA_IMG_1}
        args = {'obj_files': {key: files}, 'key': key, 'mutability': STRICT, 'mfiles': mfiles, 'ws_path': wspath,
                'cache': cache, 'fidx': fidx}
        r._update_links_wspace(key, Status.u.name, args)

        wspace_file = os.path.join(wspath, DATA_IMG_1)
        set_write_read(wspace_file)
        self.assertTrue(os.path.exists(wspace_file))
        self.assertEqual(self.md5sum(HDATA_IMG_1), self.md5sum(wspace_file))
        st = os.stat(wspace_file)
        fi = fidx.get_index()
        for k, v in fi.items():
            self.assertEqual(k, os.path.join('data', 'imghires.jpg'))
            self.assertEqual(v['hash'], 'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh')
            self.assertEqual(v['status'], 'u')
            self.assertEqual(v['ctime'], st.st_ctime)
            self.assertEqual(v['mtime'], st.st_mtime)
        self.assertTrue(st.st_nlink == 2)
        self.assertEqual(mfiles, {DATA_IMG_1: 'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh'})

    def test_get_update_links_wspace_with_duplicates(self):
        wspath = os.path.join(self.tmp_dir, 'wspace')

        hfspath = os.path.join(self.tmp_dir, 'objectsfs')
        ohfs = MultihashFS(hfspath)
        key = ohfs.put(HDATA_IMG_1)
        fidx = FullIndex(self.tmp_dir, self.tmp_dir)
        cachepath = os.path.join(self.tmp_dir, 'cachefs')
        cache = Cache(cachepath, '', '')

        testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
        c = get_sample_config_spec(testbucketname, testprofile, testregion)

        r = LocalRepository(c, hfspath)
        r._update_cache(cache, key)

        mfiles = {}
        files = {DATA_IMG_1, DATA_IMG_2}
        args = {'obj_files': {key: files}, 'key': key, 'mutability': STRICT, 'mfiles': mfiles, 'ws_path': wspath,
                'cache': cache, 'fidx': fidx}
        r._update_links_wspace(key, Status.u.name, args)

        wspace_file = os.path.join(wspath, DATA_IMG_1)
        self.assertTrue(os.path.exists(wspace_file))
        self.assertEqual(self.md5sum(HDATA_IMG_1), self.md5sum(wspace_file))

        wspace_file = os.path.join(wspath, DATA_IMG_2)
        self.assertTrue(os.path.exists(wspace_file))
        self.assertEqual(self.md5sum(HDATA_IMG_1), self.md5sum(wspace_file))
        st = os.stat(wspace_file)
        self.assertTrue(st.st_nlink == 3)
        self.assertEqual(mfiles, {DATA_IMG_1: 'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh',
                                  DATA_IMG_2: 'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh'})

        wspath = os.path.join(self.tmp_dir, 'wspace')
        ensure_path_exists(wspath)
        to_be_removed = os.path.join(wspath, 'to_be_removed')
        with open(to_be_removed, 'w') as f:
            f.write('DEAD\n')

        hfspath = os.path.join(self.tmp_dir, 'objectsfs')
        ohfs = MultihashFS(hfspath)
        key = ohfs.put(HDATA_IMG_1)
        fidx = FullIndex(self.tmp_dir, self.tmp_dir)
        cachepath = os.path.join(self.tmp_dir, 'cachefs')
        cache = Cache(cachepath, '', '')
        c = yaml_load('hdata/config.yaml')
        r = LocalRepository(c, hfspath)
        r._update_cache(cache, key)

        mfiles = {}
        files = {DATA_IMG_1, DATA_IMG_2}
        args = {'obj_files': {key: files}, 'key': key, 'mutability': STRICT, 'mfiles': mfiles, 'ws_path': wspath,
                'cache': cache, 'fidx': fidx}
        r._update_links_wspace(key, Status.u.name, args)
        r._remove_unused_links_wspace(wspath, mfiles)
        self.assertFalse(os.path.exists(to_be_removed))

    def test_sample(self):
        samples = {'range': '1:8'}
        set_files = SampleValidate.process_samples(samples, files_mock)
        self.assertTrue(len(set_files) == 7)
        samples = {'range': '1:all'}
        set_files = SampleValidate.process_samples(samples, files_mock)
        self.assertTrue(len(set_files) == 7)
        samples = {'range': '1:all:1'}
        set_files = SampleValidate.process_samples(samples, files_mock)
        self.assertTrue(len(set_files) == 7)
        samples = {'random': '1:7', 'seed': '1'}
        set_files = SampleValidate.process_samples(samples, files_mock)
        self.assertTrue(len(set_files) == 1)
        samples = {'group': '1:6', 'seed': '1'}
        set_files = SampleValidate.process_samples(samples, files_mock)
        self.assertTrue(len(set_files) == 1)

    def test_range_sample_exception(self):
        samples = {'range': 'a:a'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'range': 'a:1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'range': '1:0'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'range': '-1:3'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, {}))
        samples = {'range': '1:2'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, {}))
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(None, None))
        samples = {'range': '0:50'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'range': '0:5:6'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'range': '0:5:8'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))

    def test_group_sample_exception(self):
        samples = {'group': 'a:a', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'group': 'a:1', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'group': '1:0', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'group': '1:2', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, {}))
        samples = {'group': '1:2', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(None, None))
        samples = {'group': '0:50', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'group': '10:1', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'group': '8:8:8', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))

    def test_random_sample_exception(self):
        samples = {'random': 'a:a', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'random': 'a:1', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'random': '1:0', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'random': '1:2', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, {}))
        samples = {'random': '1:2', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(None, None))
        samples = {'random': '0:50', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'random': '6:6', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))
        samples = {'random': '9:9', 'seed': '1'}
        self.assertRaises(SampleValidateException, lambda: SampleValidate.process_samples(samples, files_mock))

    def test_import_files(self):
        path_obj = os.path.join(self.tmp_dir, 'objects')

        c = yaml_load('hdata/config.yaml')

        r = LocalRepository(c, path_obj)
        r.change_config_storage(testprofile, testbucketname, S3, region=None, endpoint_url=None)
        r.import_files(None, None, self.tmp_dir, 2, '{}://{}'.format(S3, testbucketname))

        for h in hs:
            file_path = os.path.join(self.tmp_dir, h)
            dir_file = os.path.join('hdata', h)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(filecmp.cmp(dir_file, file_path))

    def test_remote_fsck(self):
        testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
        hfspath = os.path.join(self.tmp_dir, 'objectsfs')
        ohfs = MultihashFS(hfspath)
        ohfs.put(HDATA_IMG_1)

        s3 = boto3.resource(
            S3,
            region_name='us-east-1',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
        )

        s3.Object(testbucketname, 'zdj7WWsMkELZSGQGgpm5VieCWV8NxY5n5XEP73H4E7eeDMA3A').delete()
        self.assertRaises(botocore.exceptions.ClientError, lambda: self.check_delete(s3, testbucketname))
        mdpath = os.path.join(self.tmp_dir, 'metadata-test')

        dataset_spec = get_sample_spec(testbucketname)
        specpath = os.path.join(mdpath, 'vision-computing', 'images', 'dataset-ex')
        ensure_path_exists(specpath)

        yaml_save(dataset_spec, os.path.join(specpath, 'dataset-ex.spec'))
        manifestpath = os.path.join(specpath, 'MANIFEST.yaml')

        yaml_save({'zdj7WjdojNAZN53Wf29rPssZamfbC6MVerzcGwd9tNciMpsQh': {'imghires.jpg'}}, manifestpath)
        fullspecpath = os.path.join(specpath, os.path.join(specpath, 'dataset-ex.spec'))
        spec = 'dataset-ex'
        c = yaml_load('hdata/config.yaml')
        r = LocalRepository(c, hfspath)
        ret = r.remote_fsck(mdpath, spec, fullspecpath, 2, True, True)
        self.assertTrue(ret)

        self.assertEqual(None, s3.Object(testbucketname, 'zdj7WWsMkELZSGQGgpm5VieCWV8NxY5n5XEP73H4E7eeDMA3A').load())

    def test_get_ipld(self):
        testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
        hfspath = os.path.join(self.tmp_dir, 'objectsfs')

        s3 = boto3.resource(
            S3,
            region_name='eu-west-1',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
        )

        keypath = 'zdj7WdjnTVfz5AhTavcpsDT62WiQo4AeQy6s4UC1BSEZYx4NP'
        file = os.path.join('hdata', keypath)

        with open(file, 'rb') as f:
            s3.Bucket(testbucketname).Object(keypath).put(file, Body=f)

        c = yaml_load('hdata/config.yaml')
        r = LocalRepository(c, hfspath)
        s3storage = S3Storage(testbucketname, bucket)

        links = {'Links': [{'Hash': 'zdj7WVyQ8wTdnDXsbg8wxwwFkt2Bzp95Tncsfg8PCgKXeLTye', 'Size': 16822}]}

        self.assertEqual(links, r._get_ipld(s3storage, keypath))

    def test_mount_blobs(self):
        testbucketname = os.getenv('MLGIT_TEST_BUCKET', 'ml-git-datasets')
        hfspath = os.path.join(self.tmp_dir, 'objectsfs')

        s3 = boto3.resource(
            S3,
            region_name='eu-west-1',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
        )

        keypath = 'zdj7We7Je5MRECsZUF7uptseHHPY29zGoqFsVHw6sbgv1MbWS'
        file = os.path.join('hdata', keypath)

        with open(file, 'rb') as f:
            s3.Bucket(testbucketname).Object(keypath).put(file, Body=f)

        c = yaml_load('hdata/config.yaml')
        r = LocalRepository(c, hfspath)
        s3storage = S3Storage(testbucketname, bucket)

        links = {'Links': [{'Hash': keypath, 'Size': 16822}]}

        with open(file, 'rb') as f:
            self.assertEqual(f.read(), r._mount_blobs(s3storage, links))

    def test_add_metrics(self):
        hashfs_path = os.path.join(self.tmp_dir, 'objectsfs')
        test_config = yaml_load('hdata/config.yaml')
        local_repo = LocalRepository(test_config, hashfs_path, repo_type=MODELS)
        spec_path = os.path.join(self.tmp_dir, 'model-ex.spec')
        shutil.copy('hdata/dataset-ex.spec', spec_path)
        spec_file = yaml_load(spec_path)
        model = spec_file[DATASET_SPEC_KEY].copy()
        del spec_file[DATASET_SPEC_KEY]
        spec_file[MODEL_SPEC_KEY] = model
        yaml_save(spec_file, spec_path)
        local_repo.add_metrics(spec_path, (('metric_a', '10'), ('metric_b', '9')), None)

        test_spec_file = yaml_load(spec_path)
        self.assertTrue(test_spec_file[MODEL_SPEC_KEY]['metrics'].get('metric_a', '') == 10.0)
        self.assertTrue(test_spec_file[MODEL_SPEC_KEY]['metrics'].get('metric_b', '') == 9.0)

    def test_add_metrics_wrong_entity(self):
        hashfs_path = os.path.join(self.tmp_dir, 'objectsfs')
        test_config = yaml_load('hdata/config.yaml')
        local_repo = LocalRepository(test_config, hashfs_path)
        spec_path = os.path.join(self.tmp_dir, 'dataset-ex.spec')
        shutil.copy('hdata/dataset-ex.spec', spec_path)
        local_repo.add_metrics(spec_path, (('metric_a', '10'), ('metric_b', '9')), None)
        test_spec_file = yaml_load(spec_path)
        self.assertFalse('metrics' in test_spec_file[DATASET_SPEC_KEY])

    def test_add_metrics_with_none_metrics_options(self):
        hashfs_path = os.path.join(self.tmp_dir, 'objectsfs')
        test_config = yaml_load('hdata/config.yaml')
        local_repo = LocalRepository(test_config, hashfs_path, repo_type=MODELS)
        spec_path = os.path.join(self.tmp_dir, 'model-ex.spec')
        shutil.copy('hdata/dataset-ex.spec', spec_path)
        spec_file = yaml_load(spec_path)
        model = spec_file[DATASET_SPEC_KEY].copy()
        del spec_file[DATASET_SPEC_KEY]
        spec_file[MODEL_SPEC_KEY] = model
        yaml_save(spec_file, spec_path)
        local_repo.add_metrics(spec_path, (), None)

        test_spec_file = yaml_load(spec_path)
        self.assertFalse('metrics' in test_spec_file[MODEL_SPEC_KEY])

    @pytest.mark.usefixtures('create_csv_file')
    def test_add_metrics_file(self):
        hashfs_path = os.path.join(self.tmp_dir, 'objectsfs')
        test_config = yaml_load('hdata/config.yaml')
        local_repo = LocalRepository(test_config, hashfs_path, repo_type=MODELS)
        spec_path = os.path.join(self.tmp_dir, 'model-ex.spec')
        shutil.copy('hdata/dataset-ex.spec', spec_path)
        spec_file = yaml_load(spec_path)
        model = spec_file[DATASET_SPEC_KEY].copy()
        del spec_file[DATASET_SPEC_KEY]
        spec_file[MODEL_SPEC_KEY] = model
        yaml_save(spec_file, spec_path)
        metrics_file_path = os.path.join(self.tmp_dir, 'metrics.csv')
        self.create_csv_file(metrics_file_path, {'metric_a': 10, 'metric_b': 9})
        local_repo.add_metrics(spec_path, (), metrics_file_path)

        test_spec_file = yaml_load(spec_path)
        self.assertEqual(test_spec_file[MODEL_SPEC_KEY]['metrics'].get('metric_a', ''), 10.0)
        self.assertEqual(test_spec_file[MODEL_SPEC_KEY]['metrics'].get('metric_b', ''), 9.0)

    def check_delete(self, s3, testbucketname):
        try:
            s3.Object(testbucketname, 'zdj7WWsMkELZSGQGgpm5VieCWV8NxY5n5XEP73H4E7eeDMA3A').load()
        except botocore.exceptions.ClientError as e:
            self.assertTrue(e.response['Error']['Code'] == '404')
            raise e

    def tearDown(self):
        s3 = boto3.resource(
            S3,
            region_name='eu-west-1',
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
        )
        bucket = s3.Bucket(testbucketname)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
