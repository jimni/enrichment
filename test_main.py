import unittest
import os

TEMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp/')


class GenesListsTests(unittest.TestCase):
    def setUp(self):
        """
        make a temp folder with two files, set all assert expectations
        """
        if not os.path.exists(TEMPDIR):
            os.makedirs(TEMPDIR)

        self.completeFilepath = os.path.join(TEMPDIR, 'list1')
        tempfile = open(self.completeFilepath, 'w')
        for i in range(1, 21):
            tempfile.write(str(i)+'\n')
        tempfile.close()

        self.targetFilepath = os.path.join(TEMPDIR, 'list2')
        tempfile = open(self.targetFilepath, 'w')
        for i in range(10, 20):
            tempfile.write(str(i)+'\n')
        tempfile.close()

        self.metabolicFolder = os.path.join(TEMPDIR, 'metabolic/')
        if not os.path.exists(self.metabolicFolder):
            os.makedirs(self.metabolicFolder)

        self.geneFilename1 = 'GENE_ONE'
        tempfile = open(os.path.join(self.metabolicFolder, self.geneFilename1), 'w')
        for i in range(16, 26):
            tempfile.write(str(i)+'\n')
        tempfile.close()

        self.geneFilename2 = 'GENE_TWO'
        tempfile = open(os.path.join(self.metabolicFolder, self.geneFilename2), 'w')
        for i in range(5, 13):
            tempfile.write(str(i)+'\n')
        tempfile.close()

        self.expectedOutputContent = [
            "metabolic_name,complete_number,metabolic_clean_number,target_number,intersection_number,"
            "hypergeometric_score",
            "GENE_ONE,20,5,10,4,0.15170278637770917562",
            "GENE_TWO,20,8,10,3,0.91509883305549188925"
        ]

        self.main_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
        self.outputFilepath = os.path.join(TEMPDIR, 'out')

    def tearDown(self):
        """
        destroy the temp folder
        """
        for root, dirs, files in os.walk(TEMPDIR, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            # for name in dirs:
            #     os.rmdir(os.path.join(root, name))
            os.rmdir(root)

    def test_happy_path(self):
        command_line = "python "+self.main_py
        parameters = " -c "+self.completeFilepath
        parameters += " -t "+self.targetFilepath
        parameters += " -m "+self.metabolicFolder
        parameters += " -o "+self.outputFilepath
        os.system(command_line + parameters)
        self.assertTrue(os.path.exists(self.outputFilepath), 'no output file found')
        with open(self.outputFilepath) as outputFile:
            output_content = outputFile.read().splitlines()
            self.assertListEqual(output_content, self.expectedOutputContent, 'output content doesnt match:\n' +
                                 str(output_content)+"\n---\n"+str(self.expectedOutputContent))


suite = unittest.TestLoader().loadTestsFromTestCase(GenesListsTests)
unittest.TextTestRunner().run(suite)
