from GenesLists import *
import argparse
import csv

# preset paths are used if no command line parameters are specified
metabolicListDirectory = '/Users/jim/Desktop/enrichment_maps_pathways/kegg_some'
completeListPath = '/Users/jim/Desktop/enrichment_maps_pathways/our_expressed.csv'
targetListPath = '/Users/jim/Desktop/enrichment_maps_pathways/target_68'
outFileName = 'result.csv'

# additional config
csvHeaderRow = [
    "metabolic_name",
    "complete_number",
    "metabolic_clean_number",
    "target_number",
    "intersection_number",
    "hypergeometric_score"
]


def main():
    # command line arguments parsing
    parser = argparse.ArgumentParser(description='Specify command line parameters for metabolic, complete and target '
                                                 'gene id lists or preset correct paths in `main.py`. From each file '
                                                 'only the strings with integer numbers are used.')
    parser.add_argument("-metabolics", "-m", dest="metabolicListDirectory",
                        help="path to folder with metabolic lists", default=metabolicListDirectory,
                        metavar="folder_path")
    parser.add_argument("-complete", "-c", dest="completeListPath",
                        help="path to file with complete list", default=completeListPath, metavar="file_path")
    parser.add_argument("-target", "-t", dest="targetListPath",
                        help="path to file with target list", default=targetListPath, metavar="file_path")
    parser.add_argument("-out", "-o", dest="outFilePath",
                        help="path to file with result, defaults to `%%target_list_name%%_"+outFileName+"` "
                        "in target list folder", metavar="file_path")
    args = parser.parse_args()
    args.outFilePath = args.outFilePath or os.path.splitext(args.targetListPath)[0]+'_'+outFileName

    # main body
    complete = GeneList(args.completeListPath)
    target = GeneList(args.targetListPath)
    result = csv.writer(open(args.outFilePath, 'w'))
    result.writerow(csvHeaderRow)

    metabolic_file_list = [
        os.path.join(args.metabolicListDirectory, fileName) for fileName in next(os.walk(args.metabolicListDirectory))[2]
        ]
    metabolics = []
    for fileName in metabolic_file_list:
        metabolics.append(MetabolicList(fileName))

    for metabolic in metabolics:
        metabolic.intersect_with(complete)
        metabolic.intersect_with(target)
        metabolic.compute_hypergeometric_score(complete, target)
        # metabolic.show(show_gene_ids=False)
        result.writerow([
            metabolic.name,
            complete.initialLength,
            metabolic.afterIntersectionLength[0],
            target.initialLength,
            metabolic.afterIntersectionLength[-1],
            "%.20f" % metabolic.hypergeometricScore
        ])

if __name__ == "__main__":
    main()
