#!/usr/bin/python3


class Terms(object):

    def term_help(self, term):
        try:
            return self.term_dict[term]
        except KeyError:
            return 'Missing key!'

    def __init__(self):
        self.term_dict = {
            'sample_name': 'Sample Name is a name that you choose for the sample. It can have any format, but we suggest that you make it concise, unique and consistent within your lab, and as informative as possible. Every Sample Name from a single Submitter must be unique.',
            'sample_title': 'Preferred Sample Title. Examples: Escherichia coli O104:H4 str. C227-11 clinical isolate 2010_333_NC-6; CD8+ T cells from female TSG6-knockout BALB/c mouse; Human metagenome isolated from urine of healthy female',
            'bioproject_accession': '',
            'organism': 'The most descriptive organism name for this sample (to the species, if possible). It is OK to submit an organism name that is not in our database. In the case of a new species, provide the desired organism name, and our taxonomists may assign a provisional taxID. In the case of unidentified species, choose the appropriate Genus and include "sp.", e.g., "Escherichia sp.". When sequencing a genome from a non-metagenomic source, include a strain or isolate name too, e.g., "Pseudomonas sp. UK4".',
            'strain': 'microbial or eukaryotic strain name',
            'isolate': 'identification or description of the specific individual from which this sample was obtained',
            'collected_by': 'Name of persons or institute who collected the sample',
            'collection_date': 'Date of sampling, in "DD-Mmm-YYYY", "Mmm-YYYY" or "YYYY" format (eg., 30-Oct-1990, Oct-1990 or 1990) or ISO 8601 standard "YYYY-mm-dd", "YYYY-mm" or "YYYY-mm-ddThh:mm:ss" (eg., 1990-10-30, 1990-10 or 1990-10-30T14:41:36)',
            'geo_loc_name': 'Geographical origin of the sample; use the appropriate name from this list http://www.insdc.org/documents/country-qualifier-vocabulary. Use a colon to separate the country or ocean from more detailed information about the location, eg "Canada: Vancouver" or "Germany: halfway down Zugspitze, Alps"',
            'host': 'The natural (as opposed to laboratory) host to the organism from which the sample was obtained. Use the full taxonomic name, eg, "Homo sapiens".',
            'host_disease': 'Name of relevant disease, e.g. Salmonella gastroenteritis. Controlled vocabulary, http://bioportal.bioontology.org/ontologies/1009 or http://www.ncbi.nlm.nih.gov/mesh',
            'isolation_source': 'Describes the physical, environmental and/or local geographical source of the biological sample from which the sample was derived.',
            'lat_lon': 'The geographical coordinates of the location where the sample was collected. Specify as degrees latitude and longitude in format "d[d.dddd] N|S d[dd.dddd] W|E", eg, 38.98 N 77.11 W',
            'culture_collection': 'Name of source institute and unique culture identifier. See the description for the proper format and list of allowed institutes, http://www.insdc.org/controlled-vocabulary-culturecollection-qualifier',
            'genotype': 'observed genotype',
            'host_age': 'Age of host at the time of sampling',
            'host_description': 'Additional information not included in other defined vocabulary fields',
            'host_disease_outcome': 'Final outcome of disease, e.g., death, chronic disease, recovery',
            'host_disease_stage': 'Stage of disease at the time of sampling',
            'host_health_state': 'Information regarding health state of the individual sampled at the time of sampling',
            'host_sex': 'Gender or physical sex of the host. Allowed values: male, female, pooled male and female, neuter, hermaphrodite, intersex, not determined, missing, not applicable, not collected',
            'host_subject_id': 'a unique identifier by which each subject can be referred to, de-identified, e.g. #131',
            'host_tissue_sampled': 'Type of tissue the initial sample was taken from. Controlled vocabulary, http://bioportal.bioontology.org/ontologies/1005',
            'passage_history': 'Number of passages and passage method',
            'pathotype': 'Some bacterial specific pathotypes (example Eschericia coli - STEC, UPEC)',
            'serotype': 'Taxonomy below subspecies; a variety (in bacteria, fungi or virus) usually based on its antigenic properties. Same as serovar and serogroup. e.g. serotype="H1N1" in Influenza A virus CY098518.',
            'serovar': 'Taxonomy below subspecies; a variety (in bacteria, fungi or virus) usually based on its antigenic properties. Same as serovar and serotype. Sometimes used as species identifier in bacteria with shaky taxonomy, e.g. Leptospira, serovar saopaolo S76607 (65357 in Entrez).',
            'specimen_voucher': 'Identifier for the physical specimen. Use format: "[<institution-code>:[<collection-code>:]]<specimen_id>", eg, "UAM:Mamm:52179". Intended as a reference to the physical specimen that remains after it was analyzed. If the specimen was destroyed in the process of analysis, electronic images (e-vouchers) are an adequate substitute for a physical voucher specimen. Ideally the specimens will be deposited in a curated museum, herbarium, or frozen tissue collection, but often they will remain in a personal or laboratory collection for some time before they are deposited in a curated collection. There are three forms of specimen_voucher qualifiers. If the text of the qualifier includes one or more colons it is a "structured voucher". Structured vouchers include institution-codes (and optional collection-codes) taken from a controlled vocabulary maintained by the INSDC that denotes the museum or herbarium collection where the specimen resides, please visit: http://www.insdc.org/controlled-vocabulary-specimenvoucher-qualifier',
            'subgroup': 'Taxonomy below subspecies; sometimes used in viruses to denote subgroups taken from a single isolate.',
            'subtype': 'Used as classifier in viruses (e.g. HIV type 1, Group M, Subtype A).',
            'description': 'Provide any additional information here. Comments in this field will appear in the publicly released record.',
        }

helper = Terms()
print(helper.term_help('sample_title'))