#!/usr/bin/env python 3
from argparse import ArgumentParser
from glob import glob
import pytest
import sys
import os

testpath = os.path.abspath(os.path.dirname(__file__))
scriptpath = os.path.join(testpath, '..')
datapath = os.path.join(testpath, 'testdata')
sys.path.append(scriptpath)
from validator import Validator

__author__ = 'adamkoziol'


@pytest.fixture()
def variables():
    v = ArgumentParser()
    v.metadatafile = os.path.join(datapath, 'pathogen.tsv')
    return v


@pytest.fixture()
def method_init(variables):
    method = Validator(variables)
    return method


method = method_init(variables())


def variable_update():
    global method
    method = method_init(variables())


def test_read_tsv(variables):
    method.read_tsv(variables.metadatafile)
    assert method.term_list[0] == 'sample_name'


def test_ensure_unique_names():
    method.ensure_unique_names()
    assert sorted(method.sample_ids)[1] == 'YZU0097'


def test_calculate_score():
    method.calculate_score()
    assert method.missing == 80


def test_lexmapr_inputs():
    method.create_lexmapr_inputs()
    assert os.path.isfile(os.path.join(method.path, 'host_input.csv'))


def test_lexmapr_run():
    method.run_lexmapr()
    assert os.path.isfile(os.path.join(method.path, 'host_output.csv'))
    assert os.path.getsize(os.path.join(method.path, 'host_output.csv')) > 100


def test_parse_lexmapr_outputs():
    method.parse_lexmapr_outputs()
    assert method.metadata_dict[0]['host'] == 'hu child'


def test_parse_collection_date():
    method.parse_collection_date()
    assert method.metadata_dict[4]['collection_date'] == 'missing'


def test_clean_metadata():
    method.clean_metadata()
    assert method.metadata_dict[0]['organism'] == 'missing'


def test_create_clean_report():
    method.create_clean_report()
    assert os.path.isfile(method.clean_metadata_file)
    assert os.path.getsize(method.clean_metadata_file) > 100


def test_score():
    method.score()
    assert method.pass_value == 'A-'


def test_clear_lexmapr_inputs():
    inputs = glob(os.path.join(method.path, '*_input.csv'))
    for input_file in inputs:
        os.remove(input_file)


def test_clear_lexmapr_outputs():
    outputs = glob(os.path.join(method.path, '*_output.csv'))
    for output_file in outputs:
        os.remove(output_file)


def test_remove_clean_report():
    os.remove(method.clean_metadata_file)
