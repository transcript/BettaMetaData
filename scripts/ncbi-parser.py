from bs4 import BeautifulSoup

fields = {
    'sample_accession': True,
    'organism': True,
    'sample_name': True,
    'title': True,
    'organism': True,
    'taxonomy_id': True,
    'comment': True,
    'submitter': True,
    'contact_email': True,
    'first_name': True,
    'last_name': True,
    'submission_model': True,
    'submission_package': True,
    'submission_package_name': True
}
samples = []
totals = {}
with open("senterica-ncbi.xml", 'r') as xml_handle:
    soup = BeautifulSoup(xml_handle, "xml")

    for sample in soup.find_all('BioSample'):
        new_sample = {'sample_accession': sample['accession']}

        # Sample Name
        for id in sample.Ids.find_all('Id'):
            if "db_label" in id.attrs:
                if id.attrs["db_label"] == "Sample name":
                    fields['sample_name'] = True
                    new_sample['sample_name'] = id.text

        # Description
        new_sample['title'] = sample.Description.Title.text
        new_sample['organism'] = sample.Description.Organism.OrganismName.text
        new_sample['taxonomy_id'] = sample.Description.Organism['taxonomy_id']
        if sample.Description.Comment:
            new_sample['comment'] = sample.Description.Comment.Paragraph.text

        # Owner
        new_sample['submitter'] = sample.Owner.Name.text
        if sample.Owner.Contacts:
            new_sample['contact_email'] = sample.Owner.Contacts.Contact['email']
            new_sample['first_name'] = sample.Owner.Contacts.Contact.Name.First.text
            new_sample['last_name'] = sample.Owner.Contacts.Contact.Name.Last.text

        # Submission Model
        new_sample['submission_model'] = sample.Models.Model.text
        new_sample['submission_package'] = sample.Package.text
        new_sample['submission_package_name'] = sample.Package['display_name']

        # Attributes
        for attribute in sample.Attributes.find_all('Attribute'):
            fields[attribute['attribute_name']] = True
            new_sample[attribute['attribute_name']] = attribute.text

        break
print(sorted(fields.keys()))

"""
Example BioSample Entry

<BioSample accession="SAMN10058925" id="10058925" submission_date="2018-09-13T22:11:06.313"
           last_update="2018-09-13T22:47:19.883" publication_date="2018-09-13T00:00:00.000" access="public">
    <Ids>
        <Id is_primary="1" db="BioSample">SAMN10058925</Id>
        <Id db_label="Sample name">MER-222</Id>
        <Id db="SRA">SRS3773353</Id
    </Ids>
    <Description>
        <Title>MERINO1_TRIAL</Title>
        <Organism taxonomy_name="Klebsiella pneumoniae" taxonomy_id="573">
            <OrganismName>Klebsiella pneumoniae</OrganismName>
        </Organism>
        <Comment>
            <Paragraph>Patient with bloodstream infection</Paragraph>
        </Comment>
    </Description>
    <Owner>
        <Name>University of Queensland</Name>
        <Contacts>
            <Contact email="padstock@hotmail.com">
                <Name>
                    <First>Patrick</First>
                    <Last>Harris</Last>
                </Name>
            </Contact>
        </Contacts>
    </Owner>
    <Models>
        <Model>Pathogen.cl</Model>
    </Models>
    <Package display_name="Pathogen: clinical or host-associated; version 1.0">Pathogen.cl.1.0</Package>
    <Attributes>
        <Attribute display_name="strain" harmonized_name="strain" attribute_name="strain">N/A</Attribute>
        <Attribute display_name="isolate" harmonized_name="isolate" attribute_name="isolate">N/A</Attribute>
        <Attribute display_name="collected by" harmonized_name="collected_by" attribute_name="collected_by">UQCCR</Attribute>
        <Attribute display_name="collection date" harmonized_name="collection_date" attribute_name="collection_date">2016</Attribute>
        <Attribute display_name="geographic location" harmonized_name="geo_loc_name" attribute_name="geo_loc_name">Australia</Attribute>
        <Attribute display_name="host" harmonized_name="host" attribute_name="host">Homo sapiens</Attribute>
        <Attribute display_name="host disease" harmonized_name="host_disease" attribute_name="host_disease">bacterial infectious disease</Attribute>
        <Attribute display_name="isolation source" harmonized_name="isolation_source" attribute_name="isolation_source">blood</Attribute>
        <Attribute display_name="latitude and longitude" harmonized_name="lat_lon" attribute_name="lat_lon">N/A</Attribute>
        <Attribute display_name="culture collection" harmonized_name="culture_collection" attribute_name="culture_collection">N/A</Attribute>
        <Attribute display_name="genotype" harmonized_name="genotype" attribute_name="genotype">261</Attribute>
        <Attribute display_name="host age" harmonized_name="host_age" attribute_name="host_age">47</Attribute>
        <Attribute display_name="host description" harmonized_name="host_description" attribute_name="host_description">N/A</Attribute>
        <Attribute display_name="host disease outcome" harmonized_name="host_disease_outcome" attribute_name="host_disease_outcome">N/A</Attribute>
        <Attribute display_name="host disease stage" harmonized_name="host_disease_stage" attribute_name="host_disease_stage">N/A</Attribute>
        <Attribute display_name="host health state" harmonized_name="host_health_state" attribute_name="host_health_state">N/A</Attribute>
        <Attribute display_name="host sex" harmonized_name="host_sex" attribute_name="host_sex">male</Attribute>
        <Attribute display_name="host subject id" harmonized_name="host_subject_id" attribute_name="host_subject_id">RBWH-K1-1</Attribute>
        <Attribute display_name="host tissue sampled" harmonized_name="host_tissue_sampled" attribute_name="host_tissue_sampled">Blood</Attribute>
        <Attribute display_name="passage history" harmonized_name="passage_history" attribute_name="passage_history">N/A</Attribute>
        <Attribute display_name="pathotype" harmonized_name="pathotype" attribute_name="pathotype">N/A</Attribute>
        <Attribute display_name="serotype" harmonized_name="serotype" attribute_name="serotype">N/A</Attribute>
        <Attribute display_name="serovar" harmonized_name="serovar" attribute_name="serovar">N/A</Attribute>
        <Attribute display_name="specimen voucher" harmonized_name="specimen_voucher" attribute_name="specimen_voucher">N/A</Attribute>
        <Attribute display_name="subgroup" harmonized_name="subgroup" attribute_name="subgroup">N/A</Attribute>
        <Attribute display_name="subtype" harmonized_name="subtype" attribute_name="subtype">N/A</Attribute>
    </Attributes>
    <Links>
        <Link label="PRJNA398288" target="bioproject" type="entrez">398288</Link>
    </Links>
    <Status when="2018-09-13T22:11:06.313" status="live"/>
</BioSample>
"""
