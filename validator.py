from argparse import ArgumentParser
import pandas as pd
import os


class Validator(object):

    def main(self):
        self.read_tsv(self.metadata_file)

    def read_tsv(self, tsvfile):
        """

        :return:
        """
        # Read in the .tsv file with pandas. Skip the comment lines
        dictionary = pd.read_csv(tsvfile, delimiter='\t', comment='#')
        for header in dictionary:
            # Remove any asterisks that may be present in the header names
            clean_header = header.lstrip('*')
            print(clean_header)
            # Sample is the primary key, and value is the value of the cell for that primary key + header combination
            for sample, value in dictionary[header].items():
                print(sample, value)

    def __init__(self, args):
        self.metadata_file = os.path.join(args.metadatafile)
        assert os.path.isfile(self.metadata_file), 'Cannot find the metadata file you specified: {metadata}'\
            .format(metadata=self.metadata_file)


if __name__ == '__main__':
    # Parser for arguments
    parser = ArgumentParser(description='Validate NCBI BioSample Metadata')
    parser.add_argument('-m', '--metadatafile',
                        required=True,
                        help='Name and absolute path of a .tsv file containing BioSample metadata')
    # Get the arguments into an object
    arguments = parser.parse_args()
    # Run the pipeline
    pipeline = Validator(arguments)
    pipeline.main()
