# -*- coding: utf-8 -*-

from decimal import Decimal
from math import isnan
from pathlib import Path
import pytest
import csv
from io import StringIO

from probs_runner import load_datasource


def limit_to_rows_matching_prefix(infile, outfile, column, prefix):
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(next(reader))  # header
    for row in reader:
        if row[column].startswith(prefix):
            writer.writerow(row)


def comtrade_datasource_limited_to_prefix(prefix):
    source = load_datasource(Path(__file__).parent / "testing_datasources/COMTRADE")

    # Replace the data with a subset having only the codes matching the given
    # prefix
    CODE_COLUMN = 22
    for tgt, src in source.input_files.items():
        if src.name == "ct-2018-imports.csv":
            data = StringIO(newline="")
            with open(src, "rt", newline="") as f:
                limit_to_rows_matching_prefix(f, data, CODE_COLUMN, prefix)
            data.seek(0)
            source.input_files[tgt] = data

    return source


class TestCOMTRADECodes105:
    @pytest.fixture(scope="class")
    def rdfox(self, probs_endpoint_from_datasource):
        source = comtrade_datasource_limited_to_prefix("105")
        with probs_endpoint_from_datasource(source) as rdfox:
            yield rdfox

    # @pytest.mark.xfail(reason="extra unnamed parent object is created")
    def test_expected_number_of_objects(self, rdfox):
        results = rdfox.query_records(r"""
            SELECT ?Object ?ObjectName ?ParentName
            WHERE {
                ?Object a :Object .
                OPTIONAL { ?Object rdfs:label ?ObjectName }.
                OPTIONAL { ?Parent :objectComposedOf ?Object ; rdfs:label ?ParentName }.
            }
            ORDER BY ?ObjectName
        """)
        assert len(results) == 6709

    def testpwd_expected_direct_observations(self, rdfox):
        results = rdfox.query_records(r"""
            SELECT ?ObjectName ?Measurement
            WHERE {
                ?Object a :Object ; rdfs:label ?ObjectName .
                FILTER( STRSTARTS(?ObjectName, "COMTRADE Object from Code 105") ||
                        ?ObjectName = "COMTRADE Object from Code 1" ||
                        ?ObjectName = "COMTRADE Object from Code TOTAL" )
                OPTIONAL { ?Observation a :DirectObservation ;
                                  :objectDefinedBy ?Object ;
                                  :measurement ?Measurement . }
            }
            ORDER BY ?ObjectName
        """)
        to_check = [(row["ObjectName"], row["Measurement"]) for row in results]
        assert to_check == [
            ('COMTRADE Object from Code 1', None),
            ('COMTRADE Object from Code 105', 0.0),
            ('COMTRADE Object from Code 10511', 52650005.0),
            ('COMTRADE Object from Code 10512', 0.0),
            ('COMTRADE Object from Code 10513', 5910.0),
            ('COMTRADE Object from Code 10514', None),
            ('COMTRADE Object from Code 10515', None),
            ('COMTRADE Object from Code 10594', 62417.0),
            ('COMTRADE Object from Code 10599', None),
            ('COMTRADE Object from Code TOTAL', None)
        ]

 
