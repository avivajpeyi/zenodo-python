import unittest
from zenodo_python import ZenodoHandler
import shutil, os

class TestZenodoPython(unittest.TestCase):

    def setUp(self) -> None:
        self.tmpdir = "tmp_test"
        os.makedirs(self.tmpdir, exist_ok=True)
        self.z = ZenodoHandler(test=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_get_deposition_titles(self):
        titles = self.z.get_deposition_titles()
        self.assertTrue("TEST" in titles)





if __name__ == '__main__':
    unittest.main()
