#!/usr/bin/env python 3
from argparse import ArgumentParser
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
    assert os.path.isfile(method.lexmapr_inputs)


def clear_lexmapr_inputs():
    os.remove(method.lexmapr_inputs)


