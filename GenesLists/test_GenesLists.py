import unittest
from GenesLists import *

TEMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp/')


class GenesListsTests(unittest.TestCase):
    def setUp(self):
        """
        make a temp folder with two files, set all assert expectations
        """
        if not os.path.exists(TEMPDIR):
            os.makedirs(TEMPDIR)

        self.file1 = os.path.join(TEMPDIR, 'list1')
        tempfile = open(self.file1, 'w')
        tempfile.write('123\r\n'
                       'ggg\n'
                       '456\n'
                       '789\n'
                       '7 77\r\n'
                       '7; 77\r\n'
                       '7.77\r\n'
                       '777a\r\n')
        tempfile.close()
        self.geneList1 = MetabolicList(self.file1)
        self.expected_length = 3
        self.expected_name = 'list1'
        self.expected_genes = [123, 456, 789]

        self.file2 = os.path.join(TEMPDIR, 'list2')
        tempfile = open(self.file2, 'w')
        tempfile.write('789\n'
                       '456\n'
                       '777')
        tempfile.close()
        self.geneList2 = GeneList(self.file2)
        self.expected_intersection = [456, 789]
        self.expected_intersection_length = [2]

        self.expected_hypergeometric_score = 0.15170278637770629

    def tearDown(self):
        """
        destroy the temp folder
        """
        for root, dirs, files in os.walk(TEMPDIR, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
            os.rmdir(root)

    def test_initial_read(self):
        self.assertEqual(self.geneList1.initialLength, self.expected_length,
                         'read size: '+str(self.geneList1.initialLength)+' != '+str(self.expected_length))
        self.assertEqual(self.geneList1.name, self.expected_name,
                         'read name: '+str(self.geneList1.name)+' != '+str(self.expected_name))
        self.assertEqual(self.geneList1.geneIds, self.expected_genes,
                         'read genes: '+str(self.geneList1.geneIds)+' != '+str(self.expected_genes))
        self.assertEqual(self.geneList1.afterIntersectionLength, [],
                         'intersection array not empty')
        self.assertEqual(self.geneList1.hypergeometricScore, None,
                         'hypergeometric score not empty')

    def test_count_genes(self):
        self.assertEqual(self.geneList1.count_genes(), self.expected_length,
                         'count size: '+str(self.geneList1.count_genes())+' != '+str(self.expected_length))
        self.geneList1.geneIds = self.geneList1.geneIds[:-1]
        self.assertEqual(self.geneList1.count_genes(), self.expected_length-1,
                         'count size: '+str(self.geneList1.count_genes())+' != '+str(self.expected_length-1))

    def test_intersection(self):
        self.geneList1.intersect_with(self.geneList2)
        self.assertEqual(self.geneList1.geneIds, self.expected_intersection,
                         'intersection genes: '+str(self.geneList1.geneIds)+' != '+str(self.expected_intersection))
        self.assertEqual(self.geneList1.afterIntersectionLength, self.expected_intersection_length,
                         'intersection genes: '+str(self.geneList1.afterIntersectionLength)+' != ' +
                         str(self.expected_intersection_length))

    def test_hypergeometric_scoring(self):
        self.fakeCompleteGeneList = GeneList(self.file1)
        self.fakeCompleteGeneList.initialLength = 20
        self.fakeTargetGeneList = GeneList(self.file1)
        self.fakeTargetGeneList.initialLength = 10
        self.fakeMetabolicGeneList = MetabolicList(self.file1)
        self.fakeMetabolicGeneList.afterIntersectionLength.extend([5, 4])

        temp = self.fakeMetabolicGeneList.compute_hypergeometric_score(self.fakeCompleteGeneList, self.fakeTargetGeneList)
        self.assertAlmostEqual(self.fakeMetabolicGeneList.hypergeometricScore, self.expected_hypergeometric_score,
                               places=16,
                               msg='scoring went wrong: '+str(temp)+' != '+str(self.expected_hypergeometric_score))


suite = unittest.TestLoader().loadTestsFromTestCase(GenesListsTests)
unittest.TextTestRunner().run(suite)
