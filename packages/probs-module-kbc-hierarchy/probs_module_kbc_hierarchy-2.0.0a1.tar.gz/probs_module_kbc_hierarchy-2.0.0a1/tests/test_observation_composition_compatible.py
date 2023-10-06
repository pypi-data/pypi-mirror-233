# -*- coding: utf-8 -*-
"""When an Object is composed of other objects, the measurements of compatible
objects should be summed.

"""

from decimal import Decimal
import pytest

from probs_runner import PROBS

from utils import make_observation


BAKED_GOODS_FACTS = r"""
    :Cake a :Object .
    :Bread a :Object .
    :BakedGoods a :Object .
    :BakedGoods :objectComposedOf :Cake, :Bread .
"""


QUERY = r"""
    SELECT ?observation ?role ?time ?region ?metric ?measurement ?bound
    WHERE {
        ?observation :objectDefinedBy :BakedGoods ;
        :hasRole ?role ;
        :hasTime ?time ;
        :hasRegion ?region ;
        :hasMetric ?metric ;
        :measurement ?measurement ;
        :hasBound ?bound .
    }
    ORDER BY ?role ?time ?region ?metric
"""


@pytest.mark.parametrize("role", [":SoldProduction", ":Consumption", ":Import", ":Export"])
def test_two_compatible_observations_are_summed_for_roles_with_only_object(probs_answer_query, role):
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(role=role, object=":Cake", measurement=5.1)
        + make_observation(role=role, object=":Bread", measurement=22.6)
    )
    results = probs_answer_query(facts, QUERY)

    assert len(results) == 1
    result = results[0]
    assert "ComposedInferredObservation-" in result["observation"]
    assert result["role"] == PROBS[role[1:]]  # remove empty : prefix
    assert result["time"] == PROBS.TimePeriod_YearOf2018
    assert result["region"] == PROBS.UnitedKingdom
    assert result["metric"] == "mass"
    assert result["measurement"] == Decimal("27.7")
    assert result["bound"] == PROBS.ExactBound


@pytest.mark.parametrize("role", [":ProcessInput", ":ProcessOutput"])
def test_two_compatible_observations_are_summed_for_process_input_output(probs_answer_query, role):
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(role=role, process=":Bakery", object=":Cake", measurement=5.1)
        + make_observation(role=role, process=":Bakery", object=":Bread", measurement=22.6)
    )
    results = probs_answer_query(facts, QUERY)

    assert len(results) == 1
    result = results[0]
    assert "ComposedInferredObservation-" in result["observation"]
    assert result["role"] == PROBS[role[1:]]  # remove empty : prefix
    assert result["time"] == PROBS.TimePeriod_YearOf2018
    assert result["region"] == PROBS.UnitedKingdom
    assert result["metric"] == "mass"
    assert result["measurement"] == Decimal("27.7")
    assert result["bound"] == PROBS.ExactBound


def test_compatible_sets_of_observations_are_summed_separately(probs_answer_query):
    """Like the previous test, but now with some observations from 2019 too."""
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(
            time=":TimePeriod_YearOf2018", object=":Cake", measurement=5.1
        )
        + make_observation(
            time=":TimePeriod_YearOf2018", object=":Bread", measurement=22.6
        )
        + make_observation(
            time=":TimePeriod_YearOf2019", object=":Cake", measurement=3.1
        )
        + make_observation(
            time=":TimePeriod_YearOf2019", object=":Bread", measurement=20.0
        )
    )
    results = probs_answer_query(facts, QUERY)

    to_check = [(x["time"], x["measurement"], x["bound"]) for x in results]
    assert to_check == [
        (PROBS.TimePeriod_YearOf2018, Decimal("27.7"), PROBS.ExactBound),
        (PROBS.TimePeriod_YearOf2019, Decimal("23.1"), PROBS.ExactBound),
    ]


def test_observations_with_different_roles_are_not_composed(probs_answer_query):
    """Different roles are not compatible -- only lower bounds are inferred for
    BakedGoods."""
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Bread", role=":Import", measurement=3.2)
        + make_observation(object=":Cake", role=":SoldProduction", measurement=5.4)
    )
    results = probs_answer_query(facts, QUERY)

    to_check = [(x["role"], x["measurement"], x["bound"]) for x in results]
    assert to_check == [
        (PROBS.Import, Decimal("3.2"), PROBS.LowerBound),
        (PROBS.SoldProduction, Decimal("5.4"), PROBS.LowerBound),
    ]


def test_observations_with_different_time_periods_are_not_composed(probs_answer_query):
    """Different time periods are not compatible."""
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(
            object=":Cake", time=":TimePeriod_YearOf2018", measurement=3.2
        )
        + make_observation(
            object=":Bread", time=":TimePeriod_YearOf2019", measurement=5.4
        )
    )
    results = probs_answer_query(facts, QUERY)

    to_check = [(x["time"], x["measurement"], x["bound"]) for x in results]
    assert to_check == [
        (PROBS.TimePeriod_YearOf2018, Decimal("3.2"), PROBS.LowerBound),
        (PROBS.TimePeriod_YearOf2019, Decimal("5.4"), PROBS.LowerBound),
    ]


def test_observations_with_different_regions_are_not_composed(probs_answer_query):
    """Different regions are not compatible."""
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Bread", region=":Italy", measurement=3.2)
        + make_observation(object=":Cake", region=":UnitedKingdom", measurement=5.4)
    )
    results = probs_answer_query(facts, QUERY)

    to_check = [(x["region"], x["measurement"], x["bound"]) for x in results]
    assert to_check == [
        (PROBS.Italy, Decimal("3.2"), PROBS.LowerBound),
        (PROBS.UnitedKingdom, Decimal("5.4"), PROBS.LowerBound),
    ]


def test_observations_with_different_metrics_are_not_composed(probs_answer_query):
    """Different metrics are not compatible."""
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Cake", metric='"mass"', measurement=3.2)
        + make_observation(object=":Bread", metric='"volume"', measurement=5.4)
    )
    results = probs_answer_query(facts, QUERY)

    to_check = [(x["metric"], x["measurement"], x["bound"]) for x in results]
    assert to_check == [
        ("mass", Decimal("3.2"), PROBS.LowerBound),
        ("volume", Decimal("5.4"), PROBS.LowerBound),
    ]
