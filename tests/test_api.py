import unittest
from zenodo_python import Api
import shutil, os

class TestZenodoPython(unittest.TestCase):

    def setUp(self) -> None:
        self.tmpdir = "tmp_test"
        os.makedirs(self.tmpdir, exist_ok=True)
        self.z = Api(test=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_get_deposition_titles(self):
        titles = self.z.get_deposition_titles()
        self.assertTrue("TEST" in titles)

    def test_get_deposition_id_from_title(self):
        deposition_ids = self.z.get_deposition_ids_from_title("TEST")
        self.assertTrue(isinstance(deposition_ids[0], int))
        all_ids = self.z.get_deposition_ids()
        self.assertTrue(set(deposition_ids).issubset(set(all_ids)))



if __name__ == '__main__':
    unittest.main()
