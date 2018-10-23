#! /usr/bin/env python3
"""
ncbi-summarize.py

Summarizes the findings of NCBI SRA and BioSample queries. Input is expected to
be in JSON format.
"""


def read_json(json_file):
    """Return input JSON."""
    import json
    with open(json_file, 'r') as json_handle:
        return json.load(json_handle)


def write_summary_counts(data, output, minimum=0):
    """Write the summary count results to a file."""
    cols = []
    with open(output, 'w') as fh_out:
        for k, v in sorted(data.items(), key=lambda kv: kv[1], reverse=True):
            if minimum:
                if v >= minimum:
                    cols.append(k)
            fh_out.write("{0}\t{1}\n".format(k, v))
    return cols


def write_summary(data, output, attributes):
    """Write a tab-delimited summary report."""
    with open(output, 'w') as fh_out:
        fh_out.write("{0}\n".format("\t".join(attributes)))
        for record in data:
            col_vals = []
            for attribute in attributes:
                value = ''
                if attribute in record:
                    value = record[attribute]
                col_vals.append(value)
            fh_out.write("{0}\n".format("\t".join(col_vals)))


if __name__ == '__main__':
    import argparse as ap
    from collections import defaultdict
    parser = ap.ArgumentParser(
        prog='ncbi-summarize.py', conflict_handler='resolve',
        description="Summarize NCBI query results."
    )

    parser.add_argument('sra_json', type=str, help='SRA results in JSON.')
    parser.add_argument(
        'biosample_json', type=str, help='BioSample results in JSON.'
    )
    parser.add_argument(
        '--minimum', default=1000, type=int, metavar="INT",
        help=('Minimum nuber of entries for an attribute to be in the '
              'tab-delimited summary report. (Default: 1000)')
    )

    args = parser.parse_args()
    sra = read_json(args.sra_json)
    biosample = read_json(args.biosample_json)
    print(f'Found {len(sra)} SRA entries')
    print(f'Found {len(biosample)} BioSample entries')

    sra_attributes = defaultdict(int)
    sra_values = defaultdict(int)
    sra_empty_attributes = defaultdict(int)
    sample_accessions = []
    biosample_counts = defaultdict(int)
    for record in sra:
        sample_accessions.append(record['sample_accession'])
        biosample_counts[record['sample_accession']] += 1
        for key, value in record.items():
            sra_attributes[key] += 1
            sra_values[value] += 1
            if not value:
                sra_empty_attributes[key] += 1

    # Write SRA summaries
    sra_cols = write_summary_counts(sra_attributes, "ncbi-sra-attributes.txt",
                                    minimum=args.minimum)
    write_summary_counts(sra_empty_attributes, "ncbi-sra-empty-attributes.txt")
    write_summary_counts(sra_values, "ncbi-sra-values.txt")
    write_summary(sra, "ncbi-sra-summary.txt", sra_cols)

    # Pull BioSamples with SRA entry
    sample_accessions = set(sample_accessions)
    biosample_attributes = defaultdict(int)
    biosample_empty_attributes = defaultdict(int)
    biosample_values = defaultdict(int)
    print(f'Found {len(sample_accessions)} unique BioSamples represented in SRA entries')
    for record in biosample:
        if record['sample_accession'] in sample_accessions:
            for key, value in record.items():
                biosample_attributes[key] += 1
                biosample_values[value] += 1
                if not value:
                    biosample_empty_attributes[key] += 1

    # Write BioSample summaries
    biosample_cols = write_summary_counts(
        biosample_attributes, "ncbi-biosample-attributes.txt",
        minimum=args.minimum
    )
    write_summary_counts(biosample_empty_attributes,
                         "ncbi-biosample-empty-attributes.txt")
    write_summary_counts(biosample_values, "ncbi-biosample-values.txt")
    write_summary_counts(biosample_counts, "ncbi-biosample-counts.txt")
    write_summary(biosample, "ncbi-biosample-summary.txt", biosample_cols)
