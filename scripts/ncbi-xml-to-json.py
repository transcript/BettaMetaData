#! /usr/bin/env python3
"""
ncbi-xml-to-json.py

A script to convert the NCBI XML output to JSON format for futher analysis.

Before running this script, you have apply a fix to the NCBI XML to work with
BeautifulSoup4. It's basically just turning each result into a single line.

sed 's/<EXPERIMENT_PACKAGE>/\n<EXPERIMENT_PACKAGE>/g' sra-bacteria.xml | \
    grep '^<EXPERIMENT_PACKAGE>' > sra-bacteria-fixed.xml

sed 's/<BioSample /\n<BioSample /g' biosample-bacteria.xml | \
    grep '^<BioSample ' > biosample-bacteria-fixed.xml

SRA Records Found: 721284
Biosample Records Found: 929027 (Not all are related to SRA entries)
Query Date: 2018-10-20
"""
import sys
from bs4 import BeautifulSoup


def parse_instrument(instrument_obj):
    try:
        # ILLUMINA
        return ['ILLUMINA', instrument_obj.ILLUMINA.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # PACBIO_SMRT
        return ['PACBIO_SMRT', instrument_obj.PACBIO_SMRT.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # ION_TORRENT
        return ['ION_TORRENT', instrument_obj.ION_TORRENT.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # ABI_SOLID
        return ['ABI_SOLID', instrument_obj.ABI_SOLID.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # LS454
        return ['LS454', instrument_obj.LS454.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # BGISEQ
        return ['BGISEQ', instrument_obj.BGISEQ.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # CAPILLARY
        return ['CAPILLARY', instrument_obj.CAPILLARY.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # COMPLETE_GENOMICS
        return ['COMPLETE_GENOMICS', instrument_obj.COMPLETE_GENOMICS.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # HELICOS
        return ['HELICOS', instrument_obj.HELICOS.INSTRUMENT_MODEL.text]
    except AttributeError:
        pass
    try:
        # OXFORD_NANOPORE
        return ['OXFORD_NANOPORE', instrument_obj.OXFORD_NANOPORE.INSTRUMENT_MODEL.text]
    except AttributeError as error:
        raise RuntimeError(f"Error parsing xml. {instrument_obj}") from error


def parse_organism(organism_name):
    names = organism_name.split(" ")
    if len(names) == 3:
        return [names[0], names[1], ' '.join(names[2:])]
    elif len(names) == 2:
        return [names[0], names[1], '']
    else:
        return [names[0], '', '']


def parse_biosample(biosample_xml):
    """Parse BioSample XML from NCBI."""
    biosamples = []
    with open(biosample_xml, 'r') as biosample_fh:
        for line in biosample_fh:
            line = line.rstrip()
            soup = BeautifulSoup(line, "xml")
            for sample in soup.find_all('BioSample'):
                try:
                    new_sample = {
                        'sample_accession': sample['accession'],
                        'publication_date': sample['publication_date'],
                    }

                    # Sample Name
                    for id in sample.Ids.find_all('Id'):
                        if "db_label" in id.attrs:
                            if id.attrs["db_label"] == "Sample name":
                                new_sample['sample_name'] = id.text

                    # Description and Owner
                    new_sample['biosample_title'] = sample.Description.Title.text
                    new_sample['organism'] = sample.Description.Organism['taxonomy_name']
                    new_sample['taxonomy_id'] = sample.Description.Organism['taxonomy_id']
                    new_sample['submitter'] = sample.Owner.Name.text

                    # Catch missing fields between BioSamples
                    try:
                        new_sample['contact_email'] = sample.Owner.Contacts.Contact['email']
                    except KeyError:
                        pass
                    except TypeError:
                        pass
                    except AttributeError:
                        pass
                    try:
                        new_sample['contact_lab'] = sample.Owner.Contacts.Contact['lab']
                    except KeyError:
                        pass
                    except TypeError:
                        pass
                    except AttributeError:
                        pass
                    try:
                        new_sample['comment_table'] = sample.Description.Comment.Table['class']
                    except TypeError:
                        pass
                    except AttributeError:
                        pass
                    except KeyError:
                        pass
                    try:
                        new_sample['name'] = sample.Owner.Name.text
                    except AttributeError:
                        pass
                    try:
                        new_sample['first_name'] = sample.Owner.Contacts.Contact.Name.First.text
                    except AttributeError:
                        pass
                    try:
                        new_sample['last_name'] = sample.Owner.Contacts.Contact.Name.Last.text
                    except AttributeError:
                        pass
                    try:
                        new_sample['name'] = sample.Owner.Name.text
                    except AttributeError:
                        pass
                    try:
                        new_sample['comment_paragraph'] = sample.Description.Comment.Paragraph.text
                    except AttributeError:
                        pass

                    # Submission Model
                    new_sample['submission_model'] = sample.Models.Model.text
                    new_sample['submission_package'] = sample.Package.text
                    new_sample['submission_package_name'] = sample.Package['display_name']

                    # Attributes
                    for attribute in sample.Attributes.find_all('Attribute'):
                        new_sample[attribute['attribute_name']] = attribute.text
                    biosamples.append(new_sample)
                except Exception as error:
                    raise RuntimeError(f"Error parsing xml. {sample.prettify()}") from error
    return biosamples


def parse_sra(sra_xml):
    """Parse SRA XML from NCBI."""
    experiments = []
    with open(sra_xml, 'r') as sra_handle:
        for line in sra_handle:
            line = line.rstrip()
            soup = BeautifulSoup(line, "xml")
            try:
                new_exp = {
                    'experiment_accession': soup.EXPERIMENT.IDENTIFIERS.PRIMARY_ID.text,
                    'submission_accession': soup.SUBMISSION.IDENTIFIERS.PRIMARY_ID.text,
                    'sample_accession': soup.SAMPLE.IDENTIFIERS.EXTERNAL_ID.text,
                    'secondary_sample_accession': soup.SAMPLE.IDENTIFIERS.PRIMARY_ID.text,
                    'sample_alias': soup.SAMPLE['alias'],
                }

                # Organism Name
                try:
                    new_exp['taxonomy_id'] = soup.SAMPLE.SAMPLE_NAME.TAXON_ID.text
                    new_exp['organism'] = soup.SAMPLE.SAMPLE_NAME.SCIENTIFIC_NAME.text
                except AttributeError:
                    new_exp['taxonomy_id'] = soup.Pool.Member['tax_id']
                    new_exp['organism'] = soup.Pool.Member['organism']

                # Sample Attributes
                try:
                    for attribute in soup.SAMPLE.SAMPLE_ATTRIBUTES.find_all('SAMPLE_ATTRIBUTE'):
                        try:
                            new_exp[attribute.TAG.text] = attribute.VALUE.text
                        except AttributeError:
                            new_exp[attribute.TAG.text] = ''
                except AttributeError:
                    # BioSample is empty
                    pass

                # Study Accession
                try:
                    new_exp['study_accession'] = soup.STUDY.IDENTIFIERS.EXTERNAL_ID.text
                except AttributeError:
                    try:
                        new_exp['study_accession'] = soup.EXPERIMENT.STUDY_REF.IDENTIFIERS.SECONDARY_ID.text
                    except AttributeError:
                        pass

                try:
                    new_exp['secondary_study_accession'] = soup.STUDY.IDENTIFIERS.PRIMARY_ID.text
                except AttributeError:
                    new_exp['secondary_study_accession'] = soup.EXPERIMENT.STUDY_REF.IDENTIFIERS.PRIMARY_ID.text

                # Sequencer (annoying, figure out better way)
                new_exp['instrument'], new_exp['instrument_model'] = parse_instrument(soup.EXPERIMENT.PLATFORM)

                # Catch missing fields between BioSamples
                try:
                    new_exp['contact_email'] = soup.Organization.Contact['email']
                except KeyError:
                    pass
                except TypeError:
                    pass
                try:
                    new_exp['sra_lab_name'] = soup.SUBMISSION['lab_name']
                except KeyError:
                    pass
                except TypeError:
                    pass
                try:
                    new_exp['organization_name_abbr'] = soup.Organization.Name['abbr']
                except KeyError:
                    pass
                except TypeError:
                    pass
                try:
                    new_exp['secondary_experiment_accession'] = soup.EXPERIMENT.IDENTIFIERS.EXTERNAL_ID.text
                except AttributeError:
                    pass
                try:
                    new_exp['experiment_title'] = soup.EXPERIMENT.TITLE.text
                except AttributeError:
                    pass
                try:
                    new_exp['study_title'] = soup.EXPERIMENT.STUDY.DESCRIPTOR.TITLE.text
                except AttributeError:
                    pass
                try:
                    new_exp['library_construction_protocol'] = soup.EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_CONSTRUCTION_PROTOCOL.text
                except AttributeError:
                    pass
                try:
                    new_exp['sample_title'] = soup.SAMPLE.TITLE.text
                except AttributeError:
                    pass
                try:
                    new_exp['contact_first_name'] = soup.Organization.Contact.Name.First.text
                except AttributeError:
                    pass
                try:
                    new_exp['contact_last_name'] = soup.Organization.Contact.Name.Last.text
                except AttributeError:
                    pass
                try:
                    new_exp['library_name'] = soup.EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_NAME.text
                except AttributeError:
                    pass
                try:
                    new_exp['organization_name'] = soup.Organization.Name.text
                except AttributeError:
                    pass
                try:
                    new_exp['library_strategy'] = soup.EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_STRATEGY.text
                except AttributeError:
                    pass
                try:
                    new_exp['library_source'] = soup.EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_SOURCE.text
                except AttributeError:
                    pass
                try:
                    new_exp['library_selection'] = soup.EXPERIMENT.DESIGN.LIBRARY_DESCRIPTOR.LIBRARY_SELECTION.text
                except AttributeError:
                    pass

                experiments.append(new_exp)
            except Exception as error:
                Raise(f"Error parsing xml. {error} {soup.prettify()}", file=sys.stderr)
    return experiments


if __name__ == '__main__':
    import argparse as ap
    import json
    parser = ap.ArgumentParser(
        prog='ncbi-parser.py', conflict_handler='resolve',
        description="Parse BioSample and SRA XML from NCBI."
    )

    parser.add_argument(
        'ncbi_xml', type=str,
        help='Uncompressed XML output from NCBI database.'
    )
    parser.add_argument('--biosample', action="store_true",
                        help='Input is XML from the BioSample database.')

    parser.add_argument(
        '--outdir', type=str, default='./',
        help='Directory to write output to. (Default: ./)'
    )
    args = parser.parse_args()
    records = None
    if args.biosample:
        records = parse_biosample(args.ncbi_xml)
    else:
        records = parse_sra(args.ncbi_xml)

    with open(f'{args.ncbi_xml}.json', 'w') as json_output:
        json_output.write(json.dumps(records, indent=4, sort_keys=True))
