# -*- coding: utf-8 -*-

from decimal import Decimal
import pytest

from probs_runner import PROBS
from utils import make_observation

class TestObservationCompositionMultipleSteps:
    """Test longer chains of inferred observations."""

    @pytest.fixture(scope="class")
    def object_facts(self):
        """These are the sample objects we will test."""
        return r"""
        :Cupcakes a :Object .
        :Muffins a :Object .
        :Cake a :Object .
        :Bread a :Object .
        :BakedGoods a :Object .

        :BakedGoods :objectComposedOf :Cake, :Bread .
        :Cake :objectComposedOf :Cupcakes, :Muffins .
        """

    @pytest.fixture(scope="class")
    def all_facts(self, object_facts):
        """Sample data about the objects."""
        return (
            object_facts
            + make_observation(obs_id="1", object=":Cupcakes", measurement=2)
            + make_observation(obs_id="2", object=":Muffins", measurement=3)
            + make_observation(obs_id="3", object=":Bread", measurement=6)
        )

    @pytest.fixture(scope="class")
    def rdfox(self, probs_endpoint_from_facts, all_facts):
        with probs_endpoint_from_facts(all_facts) as rdfox:
            yield rdfox

    def test_observations_are_summed_across_multiple_steps(self, rdfox):
        results = rdfox.query_records(r"""
            SELECT ?measurement ?bound
            WHERE {
                ?observation :objectDefinedBy :BakedGoods ;
                    :measurement ?measurement ;
                    :hasBound ?bound .
            }
            ORDER BY ?measurement
        """)

        assert results == [
            {"bound": PROBS.ExactBound, "measurement": 11},
        ]

    def test_observation_was_derived_from(self, rdfox):
        # Check the expected observations have been derived with
        # prov:wasDerivedFrom relationships.
        results = rdfox.query_records(r"""
            PREFIX prov: <http://www.w3.org/ns/prov#>
            SELECT ?observation1 ?observation2
            WHERE {
                ?observation1 :objectDefinedBy :Cake ;
                      prov:wasDerivedFrom :Observation1, :Observation2 .
                ?observation2 :objectDefinedBy :BakedGoods ;
                      prov:wasDerivedFrom :Observation3, ?observation1 .
            }
        """)

        assert len(results) == 1

    def test_only_one_exact_observations_at_top_level(self, rdfox):
        results = rdfox.query_records(r"""
            SELECT ?measurement
            WHERE {
                ?observation :objectDefinedBy :BakedGoods ;
                    :measurement ?measurement ;
                    :hasBound :ExactBound .
            }
            ORDER BY ?measurement
        """)

        assert results == [
            {"measurement": 11},
        ]
