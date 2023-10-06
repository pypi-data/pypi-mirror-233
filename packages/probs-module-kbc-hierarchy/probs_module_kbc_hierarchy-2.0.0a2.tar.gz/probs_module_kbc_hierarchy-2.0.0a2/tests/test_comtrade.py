# -*- coding: utf-8 -*-

from decimal import Decimal
from math import isnan
from pathlib import Path
import pytest
import csv
from io import StringIO

from probs_runner import load_datasource



class TestCOMTRADECodes105:
    @pytest.fixture(scope="class")
    def rdfox(self, probs_endpoint_from_enhanced):
        with probs_endpoint_from_enhanced() as rdfox:
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

    def test_expected_direct_observations(self, rdfox):
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

    def test_expected_number_of_inferred_observations(self, rdfox):
        results = rdfox.query_records(r"""
            SELECT ?Observation ?ObjectName ?Measurement
            WHERE {
                ?Observation a :InferredObservation ;
                     :objectDefinedBy [ rdfs:label ?ObjectName ] ;
                     :measurement ?Measurement
            }
            ORDER BY ?ObjectName ?Measurement
        """)
        to_check = [(row["ObjectName"], int(row["Measurement"])) for row in results]
        assert to_check == [
            ('COMTRADE Object from Code 1', 0),              # 2a. inferred from direct obs on 105
            ('COMTRADE Object from Code 1', 52718332),       # 2b. inferred from (1)
            ('COMTRADE Object from Code 105', 52718332),     # 1.  sum of direct, lower bound
            ('COMTRADE Object from Code TOTAL', 0),          # 3a. inferred from (2a)
            ('COMTRADE Object from Code TOTAL', 52718332),   # 3b. inferred from (2b)

        ]
