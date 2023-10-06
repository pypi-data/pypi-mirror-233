import os
import shutil
import unittest
import tempfile
from xalgorithm.utils import *
from xalgorithm.metrics import *
import sklearn.metrics as M
import numpy as np

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.actual = [1,1,1,1,0,0,0,0,0,0]
        self.predicted = [1,1,1,1,1,1,1,1,1,1]
    def test_confusion_matrix(self):
        actual_metrics = M.confusion_matrix(self.actual, self.predicted)
        test_metrics = confusion_matrix(self.actual, self.predicted)
        np.testing.assert_array_almost_equal(test_metrics, actual_metrics)
    def test_precision(self):
        actual_metrics = M.precision_score(self.actual, self.predicted)
        test_metrics = precision(self.actual, self.predicted)
        self.assertAlmostEqual(test_metrics, actual_metrics)
    def test_recall(self):
        actual_metrics = M.recall_score(self.actual, self.predicted)
        test_metrics = recall(self.actual, self.predicted)
        self.assertAlmostEqual(test_metrics, actual_metrics)
    def test_f1(self):
        actual_metrics = M.f1_score(self.actual, self.predicted)
        test_metrics = f1_score(self.actual, self.predicted)
        self.assertAlmostEqual(test_metrics, actual_metrics)

class TestPath(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.system("touch {}/test_file.txt".format(self.test_dir))
    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)
    def test_ojoin(self):
        self.assertEqual("path/to/dir/file", ojoin("path/to/dir/", "file"))
    def test_opath(self):
        expect_path = "{}/{}".format(os.getcwd(), "haha")
        self.assertEqual(expect_path, opath("./%s"%"haha"))
    def test_ofind(self):
        search_pattern = r".*\.txt"
        found_files = list(ofind(self.test_dir, search_pattern)) 
        self.assertEqual(len(found_files), 1)
        self.assertTrue(os.path.exists(found_files[-1]))
    def test_osplit(self):
        path = ojoin(self.test_dir, 'unix/test.py')
        self.assertEqual("test.py", osplit(path)[-1])
        self.assertEqual("py", osplit(path, sep='.')[-1])
    def test_osimplify(self):
        self.assertEqual("/path", osimplify("../../path"))
        self.assertEqual("/home/foo", osimplify("/home///foo/"))
    

