#! /usr/bin/env python3
"""
ena-biosample

Read output from EBI's data warehouse API and output to STDOUT.

ENA browser info: https://www.ebi.ac.uk/ena/about/browser
ENA Usage: https://www.ebi.ac.uk/ena/data/warehouse/usage
"""
SAMPLE_FIELDS = [
    'accession', 'secondary_sample_accession',
    'bio_material', 'cell_line', 'cell_type', 'collected_by',
    'collection_date', 'country', 'cultivar', 'culture_collection',
    'description', 'dev_stage', 'ecotype', 'environmental_sample',
    'first_public', 'germline', 'identified_by', 'isolate', 'isolation_source',
    'location', 'mating_type', 'serotype', 'serovar', 'sex', 'submitted_sex',
    'specimen_voucher', 'strain', 'sub_species', 'sub_strain',
    'tissue_lib', 'tissue_type', 'variety', 'tax_id', 'scientific_name',
    'sample_alias', 'checklist', 'center_name', 'depth', 'elevation',
    'altitude', 'environment_biome', 'environment_feature',
    'environment_material', 'temperature', 'salinity', 'sampling_campaign',
    'sampling_site', 'sampling_platform', 'protocol_label', 'project_name',
    'host', 'host_tax_id', 'host_status', 'host_sex', 'submitted_host_sex',
    'host_body_site', 'host_gravidity', 'host_phenotype', 'host_genotype',
    'host_growth_conditions', 'environmental_package', 'investigation_type',
    'experimental_factor', 'sample_collection', 'sequencing_method',
    'target_gene', 'ph', 'broker_name'
]


def query_ena(taxon_id, limit):
    """Use ENA's API to retrieve the latest results."""
    import requests

    address = 'http://www.ebi.ac.uk/ena/data/warehouse/search'
    query = "tax_tree({0})".format(taxon_id)
    result = 'result=sample'
    display = 'display=report'
    limit = 'limit={0}'.format(limit)

    url = '{0}?query={1}&{2}&{3}&{4}&fields={5}'.format(
        address, query, result, display, limit, ','.join(SAMPLE_FIELDS)
    )

    response = requests.get(url)
    if not response.text:
        raise Exception('No results were returned from ENA.')

    return response.text.split('\n')


if __name__ == '__main__':
    import argparse as ap

    parser = ap.ArgumentParser(
        prog='ena-biosample.py',
        conflict_handler='resolve',
        description=('Pull BioSample information from ENA for a Taxon ID.'))
    parser.add_argument('taxon_id', metavar="TAXON_ID", type=str,
                        help=('Taxon tree to pull BioSamples for.'))
    parser.add_argument('--limit', metavar="INT", type=int,
                        help='Number of samples to pull.', default=1000000)
    args = parser.parse_args()

    for sample in query_ena(args.taxon_id, args.limit):
        print(sample)
