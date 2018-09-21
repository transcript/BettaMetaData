from accessoryFunctions.accessoryFunctions import MetadataObject
from term_help import Terms
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
        name_dict = dict()
        for header in dictionary:

            required = False
            # Remove any asterisks that may be present in the header names
            clean_header = header.lstrip('*')
            if '*' in header:
                required = True
            # print(clean_header)
            # primary_key is the primary key, and value is the value of the cell for that key + header combination
            for primary_key, value in dictionary[header].items():
                if clean_header == 'sample_name':
                    # print(clean_header, primary_key, value)
                    if str(value) != 'nan':
                        name_dict[primary_key] = value
                    else:
                        name_dict[primary_key] = 'missing'
                # Update the dictionary with the new data
                try:
                    self.metadata_dict[primary_key].update({clean_header: value})
                # Create the nested dictionary if it hasn't been created yet
                except KeyError:
                    self.metadata_dict[primary_key] = dict()
                    self.metadata_dict[primary_key].update({clean_header: value})
                self.metadata_dict[primary_key].update({'required': required})
                # print(primary_key, value, required)
                # if required and str(value) == 'nan':
                #     print('Sample number {number} ({name}) is missing a value for the following
                # required field: {field}'
                #           .format(number=primary_key + 1,
                #                   name=name_dict[primary_key],
                #                   field=clean_header))
                #     print(self.terms.term_dict[clean_header])
        # for primary_key in self.metadata_dict:
        #     for header, value in self.metadata_dict[primary_key].items():
        #         print(header, value)

    def __init__(self, args):
        self.metadata_file = os.path.join(args.metadatafile)
        assert os.path.isfile(self.metadata_file), 'Cannot find the metadata file you specified: {metadata}'\
            .format(metadata=self.metadata_file)
        self.terms = Terms()
        self.metadata_dict = dict()


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
