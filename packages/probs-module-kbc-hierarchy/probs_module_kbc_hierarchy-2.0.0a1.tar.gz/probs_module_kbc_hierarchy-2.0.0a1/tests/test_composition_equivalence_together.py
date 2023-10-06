# -*- coding: utf-8 -*-

from decimal import Decimal
import pytest

from probs_runner import PROBS


from utils import make_observation
from rdflib import URIRef


# These are the sample objects we will test
SIMPLIFIED_OBJECT_FACTS = r"""
:BGS1 a :Object .
:BGSCrushedStone a :Object .
:CrushedStone a :Object .
:SandGravel a :Object .
:Aggregates a :Object .

:Aggregates :objectComposedOf :CrushedStone, :SandGravel .
:CrushedStone :objectEquivalentTo :BGSCrushedStone .
:BGSCrushedStone :objectComposedOf :BGS1 .
"""


# Template queries for the tests below

OBJECT_QUERY = """
SELECT ?measurement ?bound
WHERE {
    ?observation :objectDefinedBy %s ;
         :measurement ?measurement .
    OPTIONAL { ?observation :hasBound ?bound . }
}
ORDER BY ?measurement
"""

OBJECT_QUERY_TIME = """
SELECT ?measurement ?bound ?year
WHERE {
    ?observation :objectDefinedBy %s ;
         :measurement ?measurement .
    OPTIONAL { ?observation :hasTime ?year . }
    OPTIONAL { ?observation :hasBound ?bound . }
}
ORDER BY ?year ?measurement
"""


class TestSimplifiedBGSExample:
    """Test longer chains of inferred observations including both composition and equivalence.

    The issue arises when A = B + C

    but B has two observations, one direct and one inferred via composition AND equivalence
    """

    @pytest.fixture(scope="class")
    def all_facts(self):
        """Sample data about the objects."""
        return (
            SIMPLIFIED_OBJECT_FACTS
            + make_observation(object=":BGS1", measurement=101000000000.0)  # Obs3
            + make_observation(object=":CrushedStone", measurement=99000000000.0)  # Obs 2
            + make_observation(object=":SandGravel", measurement=56000000000.0)  # Obs 4
        )

    @pytest.fixture(scope="class")
    def rdfox(self, probs_endpoint_from_facts, all_facts):
        with probs_endpoint_from_facts(all_facts) as rdfox:
            yield rdfox

    def test_observations_crushed_stone(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY % ":CrushedStone")
        assert results == [
            {"bound": PROBS.ExactBound, "measurement": Decimal('99000000000')},  # Obs 2 (direct)
            {"bound": PROBS.ExactBound, "measurement": Decimal('101000000000')}, # Obs 3 (inferred)
        ]

    def test_observations_sand_gravel(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY % ":SandGravel")
        assert results == [
            {"bound": PROBS.ExactBound, "measurement": Decimal('56000000000')},  # Obs 4
        ]


    def test_observations_aggregates(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY % ":Aggregates")
        assert results == [
            {"bound": PROBS.ExactBound, "measurement": Decimal('155000000000')}, # Obs 2+4
            {"bound": PROBS.ExactBound, "measurement": Decimal('157000000000')}, # Obs 3+4
        ]


class TestSimplifiedBGSExampleTwoYears:
    """Test longer chains of inferred observations including both composition and equivalence.

    The issue arises when A = B + C

    but B has two observations, one direct and one inferred via composition AND equivalence
    """

    @pytest.fixture(scope="class")
    def all_facts(self):
        """Sample data about the objects."""
        return (
            SIMPLIFIED_OBJECT_FACTS
            + make_observation(object=":BGS1", time=":TimePeriod_YearOf2014", measurement=101000000000.0)  # Obs3
            + make_observation(object=":CrushedStone", time=":TimePeriod_YearOf2014", measurement=99000000000.0)  # Obs 2
            + make_observation(object=":BGS1", time=":TimePeriod_YearOf2018", measurement=69722551000.0)  # Obs 1
            + make_observation(object=":SandGravel", time=":TimePeriod_YearOf2014", measurement=56000000000.0)  # Obs 4
            + make_observation(object=":SandGravel", time=":TimePeriod_YearOf2018", measurement=56660203000.0)  # Obs 6
        )

    @pytest.fixture(scope="class")
    def rdfox(self, probs_endpoint_from_facts, all_facts):
        with probs_endpoint_from_facts(all_facts) as rdfox:
            yield rdfox

    def test_observations_crushed_stone(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY_TIME % ":CrushedStone")
        assert results == [
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('99000000000')},  # Obs 2 (direct)
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('101000000000')}, # Obs 3 (inferred)
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2018, "measurement": Decimal('69722551000')}, # Obs 1 (direct)
        ]

    def test_observations_sand_gravel(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY_TIME % ":SandGravel")
        assert results == [
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('56000000000')},  # Obs 4
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2018, "measurement": Decimal('56660203000')},  # Obs 6
        ]


    def test_observations_aggregates(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY_TIME % ":Aggregates")
        assert results == [
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('155000000000')}, # Obs 2+4
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('157000000000')}, # Obs 3+4
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2018, "measurement": Decimal('126382754000')}, # Obs 1+6
        ]


FULL_OBJECT_FACTS = r"""
:BGS1 a :Object .
:BGS2 a :Object .
:BGS3 a :Object .
:Prodcom1 a :Object .
:Prodcom2 a :Object .
:Prodcom3 a :Object .
:Prodcom4 a :Object .
:Prodcom5 a :Object .
:BGSCrushedStone a :Object .
:ProdcomCrushedStone a :Object .
:BGSSandGravel a :Object .
:ProdcomSandGravel a :Object .
:CrushedStone a :Object .
:SandGravel a :Object .
:Aggregates a :Object .

:Aggregates :objectComposedOf :CrushedStone, :SandGravel .
:CrushedStone :objectEquivalentTo :BGSCrushedStone, :ProdcomCrushedStone .
:SandGravel :objectEquivalentTo :BGSSandGravel, :ProdcomSandGravel .
:BGSCrushedStone :objectComposedOf :BGS1, :BGS2, :BGS3 .
:ProdcomCrushedStone :objectComposedOf :Prodcom1, :Prodcom2, :Prodcom3 .
:ProdcomSandGravel :objectComposedOf :Prodcom4, :Prodcom5 .
"""


class TestBGSExampleIncomplete2018:
    """More complex test based on BGS data, with incomplete 2018 observations leading to a lower bound."""

    @pytest.fixture(scope="class")
    def all_facts(self):
        """Sample data about the objects."""
        return (
            FULL_OBJECT_FACTS
            + make_observation(object=":BGS1", time=":TimePeriod_YearOf2014", measurement=38000000000.0)  # ObsA |
            + make_observation(object=":BGS2", time=":TimePeriod_YearOf2014", measurement=53000000000.0)  # ObsB |-> Obs3
            + make_observation(object=":BGS3", time=":TimePeriod_YearOf2014", measurement=10000000000.0)  # ObsC |
            + make_observation(object=":BGSCrushedStone", time=":TimePeriod_YearOf2014", measurement=99000000000.0)  # Obs 2
            + make_observation(object=":BGSSandGravel", time=":TimePeriod_YearOf2014", measurement=56000000000.0)  # Obs 4
            + make_observation(object=":Prodcom1", time=":TimePeriod_YearOf2018", measurement=68391115000.0)  # ObsX |
            + make_observation(object=":Prodcom2", time=":TimePeriod_YearOf2018", measurement=0.0)            # ObsY |-> Obs 1
            + make_observation(object=":Prodcom3", time=":TimePeriod_YearOf2018", measurement=1331436000.0)   # ObsZ |
            + make_observation(object=":Prodcom4", time=":TimePeriod_YearOf2014", measurement=26817475000.0) # | Obs 5
            + make_observation(object=":Prodcom5", time=":TimePeriod_YearOf2014", measurement=24192579000.0) # |
        )

    @pytest.fixture(scope="class")
    def rdfox(self, probs_endpoint_from_facts, all_facts):
        with probs_endpoint_from_facts(all_facts) as rdfox:
            yield rdfox

    def test_observations_crushed_stone(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY % ":CrushedStone")
        assert results == [
            {"bound": PROBS.ExactBound, "measurement": Decimal('69722551000')},  # Obs 1
            {"bound": PROBS.ExactBound, "measurement": Decimal('99000000000')},  # Obs 2
            {"bound": PROBS.ExactBound, "measurement": Decimal('101000000000')}, # Obs 3 (A+B+C)
        ]

    def test_observations_sand_gravel(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY % ":SandGravel")
        assert results == [
            {"bound": PROBS.ExactBound, "measurement": Decimal('51010054000')},  # Obs 5
            {"bound": PROBS.ExactBound, "measurement": Decimal('56000000000')},  # Obs 4
        ]

    def test_observations_aggregates(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY_TIME % ":Aggregates")
        assert results == [
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('150010054000')},  # Obs 2+5
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('152010054000')},  # Obs 3+5
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('155000000000')},  # Obs 2+4
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('157000000000')},  # Obs 3+4
            {"bound": PROBS.LowerBound, "year": PROBS.TimePeriod_YearOf2018, "measurement": Decimal('69722551000')},  # Obs 1 (incomplete)
        ]


class TestBGSExampleComplete2018:
    """More complex test based on BGS data, with complete observations for 2018."""

    @pytest.fixture(scope="class")
    def all_facts(self):
        """Sample data about the objects."""
        return (
            FULL_OBJECT_FACTS
            + make_observation(object=":BGS1", time=":TimePeriod_YearOf2014", measurement=38000000000.0)  # ObsA |
            + make_observation(object=":BGS2", time=":TimePeriod_YearOf2014", measurement=53000000000.0)  # ObsB |-> Obs3
            + make_observation(object=":BGS3", time=":TimePeriod_YearOf2014", measurement=10000000000.0)  # ObsC |
            + make_observation(object=":BGSCrushedStone", time=":TimePeriod_YearOf2014", measurement=99000000000.0)  # Obs 2
            + make_observation(object=":BGSSandGravel", time=":TimePeriod_YearOf2014", measurement=56000000000.0)  # Obs 4
            + make_observation(object=":Prodcom1", time=":TimePeriod_YearOf2018", measurement=68391115000.0)  # ObsX |
            + make_observation(object=":Prodcom2", time=":TimePeriod_YearOf2018", measurement=0.0)            # ObsY |-> Obs 1
            + make_observation(object=":Prodcom3", time=":TimePeriod_YearOf2018", measurement=1331436000.0)   # ObsZ |
            + make_observation(object=":Prodcom4", time=":TimePeriod_YearOf2018", measurement=27047315000.0) # | Obs 6
            + make_observation(object=":Prodcom5", time=":TimePeriod_YearOf2018", measurement=29612888000.0) # |
            + make_observation(object=":Prodcom4", time=":TimePeriod_YearOf2014", measurement=26817475000.0) # | Obs 5
            + make_observation(object=":Prodcom5", time=":TimePeriod_YearOf2014", measurement=24192579000.0) # |
        )

    @pytest.fixture(scope="class")
    def rdfox(self, probs_endpoint_from_facts, all_facts):
        with probs_endpoint_from_facts(all_facts) as rdfox:
            yield rdfox

    def test_observations_crushed_stone(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY % ":CrushedStone")
        assert results == [
            {"bound": PROBS.ExactBound, "measurement": Decimal('69722551000')},  # Obs 1
            {"bound": PROBS.ExactBound, "measurement": Decimal('99000000000')},  # Obs 2
            {"bound": PROBS.ExactBound, "measurement": Decimal('101000000000')}, # Obs 3 (A+B+C)
        ]

    def test_observations_sand_gravel(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY % ":SandGravel")
        assert results == [
            {"bound": PROBS.ExactBound, "measurement": Decimal('51010054000')},  # Obs 5
            {"bound": PROBS.ExactBound, "measurement": Decimal('56000000000')},  # Obs 4
            {"bound": PROBS.ExactBound, "measurement": Decimal('56660203000')},  # Obs 6
        ]


    def test_observations_aggregates(self, rdfox):
        results = rdfox.query_records(OBJECT_QUERY_TIME % ":Aggregates")
        assert results == [
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('150010054000')},  # Obs 2+5
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('152010054000')},  # Obs 3+5
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('155000000000')},  # Obs 2+4
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2014, "measurement": Decimal('157000000000')},  # Obs 3+4
            {"bound": PROBS.ExactBound, "year": PROBS.TimePeriod_YearOf2018, "measurement": Decimal('126382754000')},  # Obs 1+6
        ]
