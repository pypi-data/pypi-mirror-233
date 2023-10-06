# -*- coding: utf-8 -*-
"""
"""

from decimal import Decimal

from probs_runner import PROBS

from rdflib import Namespace

QUANTITYKIND = Namespace("http://qudt.org/vocab/quantitykind/")


FACTS = r"""
    PREFIX quantitykind:        <http://qudt.org/vocab/quantitykind/>

    :CementInCOMTRADE :objectEquivalentTo :Cement .
    :CementInPRODCOM :objectEquivalentTo :Cement .

    :Obs1 :objectDirectlyDefinedBy :CementInCOMTRADE .
    :Obs2 :objectInferredDefinedBy :CementInCOMTRADE .

    :Obs1 :hasRole :Role0 ; :hasTime :TP0 ; :hasRegion :R0 ; :hasMetric quantitykind:Mass ; :hasBound :ExactBound .
    :Obs2 :hasRole :Role0 ; :hasTime :TP0 ; :hasRegion :R0 ; :hasMetric quantitykind:Mass ; :hasBound :ExactBound .

    :CementInCOMTRADE :objectComposedOf :Object1 .
    # :CementInCOMTRADE :objectComposedOf :Object2 .
    :CementInCOMTRADE :objectComposedOf :Object3 .
    :Object3 :objectComposedOf :Object4 .
    :Object5 :objectComposedOf :Object4 .
    :Object5 :objectComposedOf :Object6 .

    :Obs3 :objectDirectlyDefinedBy :Object1 .
    :Obs4 :objectDirectlyDefinedBy :Object1 .
    # :Obs4 :objectInferredDefinedBy :Object1 .
    :Obs5 :objectDirectlyDefinedBy :Object3 .
    :Obs44 :objectDirectlyDefinedBy :Object4 .
    :Obs66 :objectDirectlyDefinedBy :Object6 .

    :Obs3 :hasRole :Role1 ; :hasTime :TP1 ; :hasRegion :R1 ; :hasMetric quantitykind:Mass .
    :Obs4 :hasRole :Role2 ; :hasTime :TP1 ; :hasRegion :R1 ; :hasMetric quantitykind:Mass .
    :Obs5 :hasRole :Role1 ; :hasTime :TP1 ; :hasRegion :R1 ; :hasMetric quantitykind:Mass .
    :Obs44 :hasRole :Role1 ; :hasTime :TP1 ; :hasRegion :R1 ; :hasMetric quantitykind:Mass .
    :Obs66 :hasRole :Role3 ; :hasTime :TP1 ; :hasRegion :R1 ; :hasMetric quantitykind:Mass .

    :Obs3 :measurement 10 .
    :Obs4 :measurement 100 .
    :Obs5 :measurement 1000 .
    :Obs44 :measurement 2 .
    :Obs66 :measurement 3 .

    :Obs3 :hasBound :ExactBound .
    :Obs4 :hasBound :ExactBound .
    :Obs5 :hasBound :ExactBound .
    :Obs44 :hasBound :ExactBound .
    :Obs66 :hasBound :ExactBound .
"""


QUERY_INF_ODB = r"""
    SELECT ?Object ?Observation
    WHERE {
        ?Observation :objectDefinedBy ?Object ;
             :objectInferredDefinedBy ?Object .
    }
    ORDER BY ?Observation ?Object
"""

QUERY_BOUNDS = r"""
    SELECT ?Observation ?Bound ?Measurement
    WHERE {
        ?Observation :measurement ?Measurement ;
             :hasBound ?Bound .
    }
    ORDER BY ?Observation ?Bound ?Measurement
"""

QUERY_WDF = r"""
    PREFIX prov: <http://www.w3.org/ns/prov#>
    SELECT ?Observation ?WDF ?Measurement
    WHERE {
        ?Observation :measurement ?Measurement ;
             prov:wasDerivedFrom ?WDF .
    }
    ORDER BY ?Observation ?WDF ?Measurement
"""

QUERY_PROPS = r"""
    SELECT ?Observation ?Role ?TimePeriod ?Region ?Metric ?Measurement
    WHERE {
        ?Observation :hasRole ?Role ;
             :hasTime ?TimePeriod ;
             :hasRegion ?Region ;
             :hasMetric ?Metric ;
             :measurement ?Measurement .
    }
    ORDER BY ?Observation ?Role ?TimePeriod ?Region ?Metric ?Measurement
"""

def test_inferred_odb(probs_answer_query):

    results = probs_answer_query(FACTS, QUERY_INF_ODB)

    assert len(results) == 17

    to_check = set([(row["Object"]) for row in results])
    # note that `set()` removes all duplicates
    assert to_check == set([
            # Obs1
            (PROBS.Cement),
            (PROBS.CementInPRODCOM),
            # Obs2
            (PROBS.Cement),
            (PROBS.CementInCOMTRADE),
            (PROBS.CementInPRODCOM),
            # Obs3 - Obs5
            (PROBS.Cement),
            (PROBS.CementInCOMTRADE),
            (PROBS.CementInPRODCOM),
            # Obs4 (lower-bound)
            (PROBS.Cement),
            (PROBS.CementInCOMTRADE),
            (PROBS.CementInPRODCOM),
            # Obs44
            (PROBS.Object3),
            (PROBS.Object5),
            # Obs66
            (PROBS.Object5),
            # Obs3 - inferred from Obs44
            (PROBS.Cement),
            (PROBS.CementInCOMTRADE),
            (PROBS.CementInPRODCOM),
    ])


def test_bounds(probs_answer_query):

    results = probs_answer_query(FACTS, QUERY_BOUNDS)

    assert len(results) == 11

    to_check = set([(row["Bound"], row["Measurement"]) for row in results])
    # note that `set()` removes all duplicates
    assert to_check == set([
            # Obs3
            (PROBS.ExactBound, Decimal("10")),
            # Obs4
            (PROBS.ExactBound, Decimal("100")),
            # Obs5
            (PROBS.ExactBound, Decimal("1000")),
            # Obs44
            (PROBS.ExactBound, Decimal("2")),
            # Obs44 -> Object3
            (PROBS.ExactBound, Decimal("2")),
            # Obs44 -> Object5
            (PROBS.LowerBound, Decimal("2")),
            # Obs66
            (PROBS.ExactBound, Decimal("3")),
            # Obs66 -> Object5
            (PROBS.LowerBound, Decimal("3")),
            # Obs3 - Obs5
            (PROBS.ExactBound, Decimal("1010")),
            # Obs4 (lower-bound)
            (PROBS.LowerBound, Decimal("100")),
            # Obs3 - inferred from Obs44
            (PROBS.ExactBound, Decimal("12")),
    ]) # note that those of Obs1 and Obs2 are not included here because they have no measurement (and the query asks explicitly about the measurement)


def test_wdf(probs_answer_query):

    results = probs_answer_query(FACTS, QUERY_WDF)

    assert len(results) == 11

    to_check = set([(row["WDF"], row["Measurement"]) for row in results])
    # note that `set()` removes all duplicates
    # we cannot check all of them because some IRIs are automatically generated (and so we need to use `issuperset`)
    assert to_check.issuperset(set([
            # Obs44 -> Object3
            (PROBS.Obs44, Decimal("2")),
            # Obs44 -> Object5
            (PROBS.Obs44, Decimal("2")),
            # Obs66 -> Object5
            (PROBS.Obs66, Decimal("3")),
            # Obs3 - Obs5 -> Cement in COMTRADE
            (PROBS.Obs3, Decimal("1010")),
            (PROBS.Obs5, Decimal("1010")),
            # Obs4 (lower-bound) -> Cement in COMTRADE
            (PROBS.Obs4, Decimal("100")),
            # Obs3 - inferred from "Obs44 -> Object3" -> Cement in COMTRADE
            (PROBS.Obs3, Decimal("12")),
            # (PROBS.Obs44, Decimal("12")), #we now include only the directly connected ones
    ])) # note that those of Obs1 and Obs2 are not included here because they have no measurement (and the query asks explicitly about the measurement)

    # there are 3 additional ones due to Equivalence (we partially check them below)
    derived_from_self = [
        True
        for row in results
        if row["Observation"] == row["WDF"]
    ]
    assert len(derived_from_self) == 3

    # and one for "inferred from Obs44 -> Object3" -> Cement in COMTRADE (we partially check it below),
    measurement_equals_12 = [
        True
        for row in results
        if row["Measurement"] == Decimal("12")
    ]
    assert len(measurement_equals_12) == 3


def test_props(probs_answer_query):

    results = probs_answer_query(FACTS, QUERY_PROPS)

    assert len(results) == 11

    to_check = set([(row["Role"], row["TimePeriod"], row["Region"], row["Metric"], row["Measurement"]) for row in results])
    # note that `set()` removes all duplicates
    assert to_check == set([
            # Obs3
            (PROBS.Role1, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("10")),
            # Obs4 or Obs4 (lower-bound)
            (PROBS.Role2, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("100")),
            # Obs5
            (PROBS.Role1, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("1000")),
            # Obs44 or Obs44 -> Object3
            (PROBS.Role1, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("2")),
            # Obs44 or Obs44 -> Object5
            (PROBS.Role1, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("2")),
            # Obs66 or Obs66 -> Object5
            (PROBS.Role3, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("3")),
            # Obs66 or Obs66 -> Object5
            (PROBS.Role3, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("3")),
            # Obs3 - Obs5
            (PROBS.Role1, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("1010")),
            # Obs3 - inferred from Obs44
            (PROBS.Role1, PROBS.TP1, PROBS.R1, QUANTITYKIND.Mass, Decimal("12")),
    ])
