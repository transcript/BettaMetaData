# Summary of *ncbi-biosample/* Directory

## Acquiring SRA and BioSample Records From NCBI
I tried to use the edirect tools to download from NCBI but due to the large number of records returned it would randomly time out. To get over this, I ended up using BioPython to download XML records from NCBI and retry on timeouts. The [*ncbi-esearch.py*](https://github.com/transcript/BettaMetaData/blob/master/scripts/ncbi-esearch.py) was used to download SRA/BioSample records.

### Queries and Execution
#### SRA
The query **txid2[Organism:exp] AND genomic[Source] AND public[Access] AND wgs[Strategy]** was used to return all public bacterial samples in SRA that have are marked as being genomic and whole genome sequences. In total 721,284 SRA Experiment records were downloaded on October 20th, 2018. A record of this run can be found at [*sra-bacteria-esearch.txt*](https://github.com/transcript/BettaMetaData/blob/master/data/ncbi-biosample/sra-bacteria-esearch.txt). Below is how the script was executed:
```
python3 -u ncbi-esearch.py sra "txid2[Organism:exp] AND genomic[Source] AND public[Access] AND wgs[Strategy]" robert.petit@emory.edu --retmax 500 --output sra-bacteria.xml | tee sra-bacteria-esearch.txt
```

#### BioSample
The query **txid2[Organism:exp]** was used to return all bacterial BioSamples. In total 929,027 BioSample records were downloaded on October 20th, 2018. A record of this run can be found at [*biosample-bacteria-esearch.txt*](https://github.com/transcript/BettaMetaData/blob/master/data/ncbi-biosample/biosample-bacteria-esearch.txt). Below is how the script was executed:

```
python3 -u ncbi-esearch.py biosample "txid2[Organism:exp]" robert.petit@emory.edu --retmax 10000 --output biosample-bacteria.xml | tee biosample-bacteria-esearch.txt
```

## Parsing NCBI XML
### Converting NCBI XML To Single Line Entries
After downloading the XML files, each line contained entries for multiple records. The Python parser (lxml, BeautifulSoup4) did not like this and it was necessary to convert the XML to contain only one record per line. This required a simple find and replace. Here is the command:
```
# SRA
sed 's/<EXPERIMENT_PACKAGE>/\n<EXPERIMENT_PACKAGE>/g' sra-bacteria.xml | grep '^<EXPERIMENT_PACKAGE>' > sra-bacteria-fixed.xml

# BioSample
sed 's/<BioSample /\n<BioSample /g' biosample-bacteria.xml | grep '^<BioSample ' > biosample-bacteria-fixed.xml
```

### Converting XML to JSON
Now that the XML in was in proper format for parsing, it was necessary extract useful information and store each record in JSON format. This was due to the slowness of parsing the XML. The SRA XML file was 15GB and took 3 hours to get through. There was probably an better way to get through it but a one time conversion to a much smaller JSON file worked. The script [*ncbi-xml-to-json.py*](https://github.com/transcript/BettaMetaData/blob/master/scripts/ncbi-xml-to-json.py) was used to convert both the SRA and BioSample XMLs to JSON.

#### Command
```
# SRA
python3 -u ncbi-xml-to-json.py sra-bacteria-fixed.xml

# BioSample
python3 -u ncbi-xml-to-json.py biosample-bacteria-fixed.xml --biosample
```

#### example-biosample.xml & example-sra.xml
These two files were used to get a general idea for SRA and BioSample XML.

#### Example JSON Output
###### SRA
```
[
    {
        "BioSampleModel": "Pathogen.cl",
        "collected_by": "CDC",
        "collection_date": "missing",
        "contact_email": "eih9@cdc.gov",
        "contact_first_name": "Eija",
        "contact_last_name": "Trees",
        "experiment_accession": "SRX4908796",
        "experiment_title": "",
        "geo_loc_name": "USA",
        "host": "missing",
        "host_disease": "missing",
        "instrument": "ILLUMINA",
        "instrument_model": "Illumina MiSeq",
        "isolate": "missing",
        "isolation_source": "missing",
        "lat_lon": "missing",
        "library_construction_protocol": "NexteraXT",
        "library_name": "NexteraXT",
        "library_selection": "RANDOM",
        "library_source": "GENOMIC",
        "library_strategy": "WGS",
        "organism": "Listeria monocytogenes",
        "organization_name": "PulseNet Next Generation Subtyping Methods Unit",
        "organization_name_abbr": "Pulsenet",
        "sample_accession": "SAMN10262275",
        "sample_alias": "PNUSAL004451",
        "sample_title": "Listeria monocytogenes",
        "secondary_experiment_accession": "PNUSAL004451:wgs",
        "secondary_sample_accession": "SRS3954821",
        "secondary_study_accession": "SRP028271",
        "sra_lab_name": "",
        "strain": "PNUSAL004451",
        "study_accession": "PRJNA212117",
        "submission_accession": "SRA796276",
        "taxonomy_id": "1639"
    }
]
```

###### BioSample
```
[
    {
        "biosample_title": "Pathogen: environmental/food/other sample from Salmonella enterica",
        "collected_by": "USDA-FSIS",
        "collection_date": "2018",
        "contact_email": "NCBISubmissions@fsis.usda.gov",
        "first_name": "Glenn",
        "geo_loc_name": "USA:GA",
        "isolation_source": "chicken carcass",
        "last_name": "Tillman",
        "lat_lon": "missing",
        "name": "USDA FSIS",
        "organism": "Salmonella enterica",
        "publication_date": "2018-10-19T00:00:00.000",
        "sample_accession": "SAMN10262515",
        "sample_name": "FSIS21822465",
        "serovar": "Kentucky",
        "strain": "FSIS21822465",
        "subgroup": "enterica",
        "submission_model": "Pathogen.env",
        "submission_package": "Pathogen.env.1.0",
        "submission_package_name": "Pathogen: environmental/food/other; version 1.0",
        "submitter": "USDA FSIS",
        "taxonomy_id": "28901"
    }
]
```

## XML and JSON Availability
At the moment the XMLs and JSONs are stored on Robert Petit's personal Dropbox account. Once things are finalized they will be moved to Figshare or some other similar data hosting site.


# Summary of *ncbi-biosample/summary/* Directory
This directory includes files output from [*ncbi-summarize.py*](https://github.com/transcript/BettaMetaData/blob/master/scripts/ncbi-summarize.py). *ncbi-summarize.py* used the JSON files descibed above to create a number of summaries. Summary information for SRA (*ncbi-sra* prefix) entries and BioSample (*ncbi-biosample* prefix) entries linked to at least one SRA experiement.

#### *ncbi-summarize.py* Command
```
ncbi-summarize.py sra-bacteria-fixed.json biosample-bacteria-fixed.json --minimum 100000
```

#### *-attributes.txt
These files include the attribute (or field) name and a count for the number of times information was given by the submitter. 

###### Example output:
```
biosample_title 676549
name    676549
organism        676549
publication_date        676549
sample_accession        676549
```

#### *.empty-attributes.txt
These files include the number of times an actual empty string ('') was identified for a given attribute.

###### Example output:
```
name    38
submitter       38
host    13
last_name       1
comment_paragraph       1
```

#### *.summary.txt.gz
These files are a summary of values for each sample. The first row includes a header of attribute names, and each row is the value given for said attribute for each SRA Experiment or BioSample. Only columns with **>100,000** values entered were included in this summary. The column names should be in the same order as seen in the *attributes* file. 

###### Example output:
Excluding from this as its kind of big.

#### *.values.txt.gz
These files include the number of times a value was associated with any given attribute. There is a mixture of user-generated and auto-generated values. For the example below. *missing* is from a user, but *Generic*|*Generic.1.0* is auto-generated on the selection of the BioSample type (Generic vs Microbe vs Pathogen).

**Note** Only values observed > 100000 times were included in these files.

###### Example output:
```
missing 607437
Generic 589875
EBI     309422
Generic.1.0     294666
Missing 277852
```

#### ncbi-biosample-counts.txt
There was not a 1-to-1 relationship between SRA Experiments and BioSamples. In total 676,549 BioSamples were linked to 721,284 SRA Experiments. This file represents the number of SRA Experiments a BioSample was linked to. For example, the BioSample SAMN05853047 was linked to 576 unique SRA Experiments.

###### Example output:
```
SAMN05853047    576
SAMN08211502    324
SAMN03342197    133
SAMN00103269    102
SAMN06562698    96
```
