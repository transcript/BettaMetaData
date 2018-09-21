#! /usr/bin/python3

def clean_indentifier(text):
    return text.split(":")[1].lstrip()

if __name__ == '__main__':
    import argparse as ap
    import glob
    import gzip
    from os.path import basename, splitext

    parser = ap.ArgumentParser(
        prog='ncbi-parser.py',
        conflict_handler='resolve',
        description=('Parser for NCBI BioSample text output.'))
    parser.add_argument('samples', metavar="DIRECTORY", type=str,
                        help=('Directory of zipped NCBI BioSample output.'))
    parser.add_argument('--prefix', metavar="PREFIX", type=str,
                        help=('Prefix for output.'))
    args = parser.parse_args()

    total = 0
    samples = {}
    attributes = {}
    values = {}
    total_samples = 0
    for file in glob.glob("{0}/*.gz".format(args.samples)):
        organism = splitext(splitext(basename(file))[0])[0]
        samples[organism] = []
        with gzip.open(file, 'r') as file_handle:
            """
            1: Pathogen: environmental/food/other sample from Campylobacter jejuni
            Identifiers: BioSample: SAMN10094112; Sample name: FSIS11813598; SRA: SRS3803845
            Organism: Campylobacter jejuni
            Attributes:
            /strain="FSIS11813598"
            /collected by="USDA-FSIS"
            /collection date="2018"
            /geographic location="USA:PR"
            /isolation source="raw intact chicken"
            /latitude and longitude="missing"
            Accession: SAMN10094112 ID: 10094112

            2: Pathogen: environmental/food/other sample from Campylobacter jejuni
            Identifiers: BioSample: SAMN10094111; Sample name: FSIS11813597; SRA: SRS3803849
            Organism: Campylobacter jejuni
            Attributes:
            /strain="FSIS11813597"
            /collected by="USDA-FSIS"
            /collection date="2018"
            /geographic location="USA:MS"
            /isolation source="animal-chicken-young chicken"
            /latitude and longitude="missing"
            Accession: SAMN10094111 ID: 10094111

            """
            current_biosample = {}
            for line in file_handle:
                line = line.strip().decode()

                if line:
                    if line.startswith("Identifiers"):
                        # print(line)
                        # Identifiers: BioSample: SAMN10094111; Sample name: FSIS11813597; SRA: SRS3803849
                        line = line.replace("Identifiers: ", "")
                        biosample = line.split(";")[0]
                        current_biosample['sample_accession'] = clean_indentifier(biosample)
                        if 'sample_accession' not in attributes:
                            attributes['sample_accession'] = 1
                        else:
                            attributes['sample_accession'] += 1
                    elif line.startswith("Organism"):
                        # Organism: Campylobacter jejuni
                        current_biosample["organism"] = line.replace("Organism: ", "")
                        if 'organism' not in attributes:
                            attributes['organism'] = 1
                        else:
                            attributes['organism'] += 1
                    elif line.startswith("/"):
                        # Attributes
                        # /strain="FSIS11813597"
                        key, value = line.split("=", 1)
                        key = key.replace("/", "").replace(" ", "_")
                        if key not in attributes:
                            attributes[key] = 1
                        else:
                            attributes[key] += 1

                        value = value.replace('"', '')
                        if value not in values:
                            values[value] = 1
                        else:
                            values[value] += 1
                        current_biosample[key] = value
                else:
                    total_samples += 1
                    samples[organism].append(current_biosample)
                    current_biosample = {}

    # Attributes
    cols = []
    required_total = 100000
    with open("ncbi-attributes.txt", 'w') as fh_out:
        for k, v in sorted(attributes.items(), key=lambda kv: kv[1], reverse=True):
            if v >= required_total:
                cols.append(k)
            fh_out.write("{0}\t{1}\n".format(k, v))

    # Values
    with open("ncbi-values.txt", 'w') as fh_out:
        for k, v in sorted(values.items(), key=lambda kv: kv[1], reverse=True):
            fh_out.write("{0}\t{1}\n".format(k, v))

    # Stats
    with open("ncbi-summary.txt", 'w') as fh_out:
        fh_out.write("input_file\t{0}\n".format("\t".join(cols)))
        for key, vals in samples.items():
            print("{0}\t{1}".format(key, len(vals)))
            for val in vals:
                col_vals = []
                has_value = False
                for attribute in cols:
                    if attributes[attribute] >= required_total:
                        value = ''
                        if attribute in val:
                            has_value = True
                            value = val[attribute]
                        col_vals.append(value)

                if has_value:
                    fh_out.write("{0}\t{1}\n".format(organism, "\t".join(col_vals)))
