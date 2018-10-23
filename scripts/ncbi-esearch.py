#! /usr/bin/env python3
"""
ncbi-query.py

Uses Entrez tools from BioPython to download XML reports from NCBI. Below are
the two queries used for this project.

All Bacterial WGS Submissions to SRA:
txid2[Organism:exp] AND genomic[Source] AND public[Access] AND wgs[Strategy]

All Bacteria BioSamples:
txid2[Organism:exp]

SRA Records Found: 721284
Biosample Records Found: 929027 (Not all are related to SRA entries)
Query Date: 2018-10-20
"""


if __name__ == '__main__':
    import argparse as ap
    import datetime
    import time
    from Bio import Entrez
    from urllib.error import HTTPError
    from statistics import mean
    Entrez.tool = "ncbi-query.py"
    RETMODE = 'text'
    RETTYPE = 'xml'

    parser = ap.ArgumentParser(
        prog='ncbi-esearch.py', conflict_handler='resolve',
        description="Download entries linked to query against NCBI database."
    )

    parser.add_argument('database', type=str, help='NCBI database to query.')
    parser.add_argument(
        'query', type=str, help='Query to search against NCBI.'
    )
    parser.add_argument(
        'email', type=str,
        help='Email address for NCBI to contact in case of issues.'
    )

    parser.add_argument(
        '--output', type=str,
        help='File to write output to. (Default: DATABASE.xml)'
    )

    parser.add_argument(
        '--api_key', type=str,
        help='NCBI API key to increase max queries per second.'
    )
    parser.add_argument(
        '--retmax', default=1000, type=int, metavar="INT",
        help='Maximum number of entries to download at once. (Default: 1000)'
    )

    args = parser.parse_args()
    Entrez.email = args.email

    if args.api_key:
        Entrez.api_key = args.api_key

    # Query SRA
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"Database: {args.database}")
    print(f"Query: {args.query}")
    print(f"Date: {current_time}")
    esearch_handle = Entrez.esearch(db=args.database, term=args.query,
                                    usehistory="y", idtype="acc")
    results = Entrez.read(esearch_handle)
    esearch_handle.close()
    print(f"Records Found: {results['Count']}")
    print(f"Batch Size: {args.retmax}")
    print("----------")

    # Download records
    batch_size = args.retmax
    qtimes = []
    completed = 0
    query_count = int(results['Count'])
    output = args.output if args.output else f"{args.database}.xml"
    with open(output, "w") as out_handle:
        for start in range(0, query_count, batch_size):
            end = min(query_count, start + batch_size)
            print(f"Downloading records {start + 1} to {end}")
            attempt = 0
            start_time = time.time()
            while attempt < 120:
                try:
                    fetch_handle = Entrez.efetch(
                        db=args.database, rettype="full", retmode="xml",
                        retstart=start, retmax=batch_size,
                        webenv=results["WebEnv"],
                        query_key=results["QueryKey"], idtype="acc"
                    )
                    print("\tEFetch query successful")
                    break
                except HTTPError as err:
                    attempt += 1
                    if 500 <= err.code <= 599:
                        print(f"\tReceived error from server {err}")
                        print(f"\tAttempt {attempt} of 120, sleeping for 30s.")
                        time.sleep(30)
                    else:
                        raise
            data = fetch_handle.read()
            fetch_handle.close()
            out_handle.write(data)
            qtime = time.time() - start_time
            qtimes.append(qtime)
            remaining = str(datetime.timedelta(seconds=round(
                ((query_count // batch_size) - len(qtimes)) * mean(qtimes)
            )))
            print(f"\tTook: {qtime:.2f}s ... EST Time Remaining: {remaining}")
