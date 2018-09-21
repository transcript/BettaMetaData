#!/usr/bin/env python 3
from argparse import ArgumentParser
from glob import glob
import pytest
import sys
import os

testpath = os.path.abspath(os.path.dirname(__file__))
scriptpath = os.path.join(testpath, '..')
sys.path.append(scriptpath)
from validator import Validator

__author__ = 'adamkoziol'


@pytest.fixture()
def variables():
    v = ArgumentParser()
    v.metadatafile = os.path.join(testpath, 'testdata', 'pathogen.tsv')

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


def test_lexmapr_inputs():
    method.create_lexmapr_inputs()
    assert os.path.isfile(os.path.join(method.path, 'sample_name_input.csv'))


def test_lexmapr_run():
    method.run_lexmapr()
    assert os.path.isfile(os.path.join(method.path, 'sample_name_output.csv'))
    assert os.path.getsize(os.path.join(method.path, 'sample_name_output.csv')) > 100


def test_clear_lexmapr_inputs():
    inputs = glob(os.path.join(method.path, '*_input.csv'))
    for input_file in inputs:
        os.remove(input_file)


def test_clear_lexmapr_outputs():
    outputs = glob(os.path.join(method.path, '*_output.csv'))
    for output_file in outputs:
        os.remove(output_file)



