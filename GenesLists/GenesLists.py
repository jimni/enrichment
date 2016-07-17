import os
import csv
from scipy.stats import hypergeom


class GeneList:
    """
    Class for gene id lists of any kind
    """
    def __init__(self, filepath):
        with open(filepath) as inputFile:
            self.geneIds = []
            for line in inputFile:
                clean_line = line.replace("\n", "").replace("\r", "")
                if clean_line.isdigit():
                    self.geneIds.append(int(clean_line))
        self.initialLength = self.count_genes()
        self.afterIntersectionLength = []
        self.name = ''
        self.hypergeometricScore = None
        self.geneNames = []

    def count_genes(self):
        return len(self.geneIds)

    def show(self, show_gene_ids=False):
        print 'Name: %s' % self.name
        print 'Initial length: %s' % self.initialLength
        print 'Length after n-th intersection: %s' % self.afterIntersectionLength
        print 'Hypergeometric score: %s' % self.hypergeometricScore
        if show_gene_ids:
            print 'Gene IDs list: %s' % self.geneIds

    def convert_ids_to_names(self, conversion_map_filepath, delimiter_char=','):
        # todo: add utest for convert_ids_to_names
        with open(conversion_map_filepath, 'r') as mapFile:
            reader = csv.reader(mapFile, delimiter=delimiter_char)
            gene_id_name_dict = {rows[0]: rows[1] for rows in reader}
        self.geneNames = [gene_id_name_dict.get(str(geneId), "not found id %s" % geneId) for geneId in self.geneIds]

class MetabolicList(GeneList):
    """
    Class for gene id lists, that represent metabolic information
    """
    def __init__(self, filepath):
        GeneList.__init__(self, filepath)
        self.name = os.path.splitext(os.path.basename(filepath))[0]

    def intersect_with(self, another_list):
        self.geneIds = list(set(self.geneIds).intersection(another_list.geneIds))
        self.afterIntersectionLength.append(self.count_genes())

    def compute_hypergeometric_score(self, complete_list, target_list):
        M = complete_list.initialLength
        n = self.afterIntersectionLength[0]
        N = target_list.initialLength
        x = self.afterIntersectionLength[-1]
        self.hypergeometricScore = hypergeom.sf(x-1, M, n, N)
        return self.hypergeometricScore

