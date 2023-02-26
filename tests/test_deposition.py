import unittest
from zenodo_python import Deposition
from zenodo_python.api import TEST_MODE
import random
import shutil
import os
from datetime import datetime




def make_tmp_file(outdir):
    os.makedirs(outdir, exist_ok=True)
    # human readable timestamp
    curr_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fname = f"{outdir}/tmp_{curr_timestamp}.txt"
    with open(fname, 'w') as f:
        f.write("test")
    return fname

class TestDeposition(unittest.TestCase):

    def setUp(self) -> None:
        TEST_MODE = True
        self.tmpdir = "tmp_test"
        os.makedirs(self.tmpdir, exist_ok=True)
        self.d = Deposition.from_title(title="TEST")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_loader(self):
        d = self.d
        self.assertTrue(d.files is not None, d.files)

    def test_upload_file(self):
        d = self.d
        fname = make_tmp_file(self.tmpdir)
        d.upload_files(fname)
        d1 = Deposition.from_title(title="TEST")
        self.assertTrue(fname in d1.filenames)


    def test_make_new_version(self):
        d = self.d
        fname = make_tmp_file(self.tmpdir)
        d.upload_files(fname)
        d1 = Deposition.from_title(title="TEST")
        self.assertTrue(fname in d1.filenames)
        d1.make_new_version()
        d2 = Deposition.from_title(title="TEST")
        self.assertTrue(fname in d2.filenames)
        self.assertTrue(d1.version != d2.version)



if __name__ == '__main__':
    unittest.main()
