#!/usr/bin/env python3

from term_help import Terms
from subprocess import call
from argparse import ArgumentParser
from threading import Thread
from queue import Queue
import pandas as pd
import os


class Validator(object):

    def main(self):
        """
        Run all the methods
        """
        self.read_tsv(self.metadata_file)
        self.create_lexmapr_inputs()
        self.run_lexmapr()

    def read_tsv(self, tsvfile):
        """
        Read in the .tsv metadata file with pandas, and create a dictionary of all the headers: values
        """
        # Read in the .tsv file with pandas. Skip the comment lines
        dictionary = pd.read_csv(tsvfile, delimiter='\t', comment='#')
        for header in dictionary:
            # Create a variable to store whether a header isrequired
            required = False
            # Remove any asterisks that may be present in the header names
            clean_header = header.lstrip('*')
            if '*' in header:
                required = True
            # primary_key is the primary key, and value is the value of the cell for that key + header combination
            for primary_key, value in dictionary[header].items():
                # Update the dictionary with the new data
                try:
                    self.metadata_dict[primary_key].update({clean_header: value})
                # Create the nested dictionary if it hasn't been created yet
                except KeyError:
                    self.metadata_dict[primary_key] = dict()
                    self.metadata_dict[primary_key].update({clean_header: value})
                self.metadata_dict[primary_key].update({'required': required})
                # Add any terms with values to the set of terms to be processed by lecmapr
                if str(value) != 'nan' and clean_header not in self.term_list:
                    self.term_list.append(clean_header)

    def create_lexmapr_inputs(self):
        """
        Create a .csv file of all headings that have at least on value. This .csv file will be processed by
        LexMapr in order to refine the ontologies
        :return:
        """
        # Ensure that the term list actually exists
        if self.term_list:
            # Create the header
            # data = ','.join(term for term in self.term_list)
            # data += '\n'
            for term in self.term_list:
                # Set the header
                data = 'primary_key,{term}\n'.format(term=term)
                # Iterate through all the samples in the dictionary
                for primary_key in self.metadata_dict:
                    for field, value in self.metadata_dict[primary_key].items():
                        if field == term:
                            if str(value) == 'nan':
                                value = 'missing'
                            data += '{pk},{value},'.format(pk=primary_key,
                                                           value=value)
                    data += '\n'
                # Open the .csv file to be used by lexmapr
                with open(os.path.join(self.path, '{term}_input.csv'.format(term=term)), 'w') as lexmapr_file:
                    lexmapr_file.write(data)
        else:
            print('Empty metadata file?')

    def run_lexmapr(self):
        """
        Run LexMapr in a multi-threaded manner on the extracted terms
        """
        print('Running LexMapr on provided metadata values')
        for i in range(len(self.term_list)):
            # Start threads
            threads = Thread(target=self.lex_map, args=())
            # Set the daemon to True - something to do with thread management
            threads.setDaemon(True)
            # Start the threading
            threads.start()
        # Create the LexMapr command for each term
        for term in self.term_list:
            output = os.path.join(self.path, '{term}_output.csv'.format(term=term))
            # Don't run the analyses if the output file already exists
            if not os.path.isfile(output):
                lexmapr_command = ['lexmapr', '-o', output,
                                   os.path.join(self.path, '{term}_input.csv'.format(term=term)),
                                   os.path.join(self.path, 'lexmapr_logs')]
                # Add the command to the queue
                self.lex_queue.put(lexmapr_command)
        self.lex_queue.join()

    def lex_map(self):
        while True:
            cmd = self.lex_queue.get()
            # Run the system call with subprocess.call
            call(cmd)
            self.lex_queue.task_done()

    def __init__(self, args):
        self.metadata_file = os.path.join(args.metadatafile)
        assert os.path.isfile(self.metadata_file), 'Cannot find the metadata file you specified: {metadata}'\
            .format(metadata=self.metadata_file)
        self.terms = Terms()
        self.term_list = list()
        self.metadata_dict = dict()
        self.path = os.path.dirname(self.metadata_file)
        self.lex_queue = Queue()


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
