# -*- coding: utf-8 -*-
"""When an Object is composed of other objects, inferred observations should be
marked as lower bounds if any observations are missing.

"""

from decimal import Decimal

from probs_runner import PROBS

from utils import make_observation


# These are the sample objects we will test.
BAKED_GOODS_FACTS = r"""
    :Cake a :Object .
    :Bread a :Object .
    :BakedGoods a :Object .
    :BakedGoods :objectComposedOf :Cake, :Bread .
"""

QUERY = r"""
    SELECT ?measurement ?bound
    WHERE {
        ?obs :objectDefinedBy :BakedGoods ;
                :measurement ?measurement ;
                :hasBound ?bound .
    }
    ORDER BY ?measurement ?bound
"""


def test_nothing_is_inferred_with_no_inputs(probs_answer_query):
    """
    This seems a fairly trivial test, but it could allow to test if we generate too many `EmptyObservation`.
    """
    results = probs_answer_query(BAKED_GOODS_FACTS, QUERY)
    assert len(results) == 0


def test_lower_bound_is_inferred_with_missing_observation(probs_answer_query):
    """
    A lower bound should be generated when we have no observation for `Bread`. This inferred observation should have the same `measurement` of the only observation we have for `Cake`.
    """
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Cake", measurement=5.1)
        # no observation for bread
    )
    results = probs_answer_query(facts, QUERY)
    assert results == [
        {"bound": PROBS.LowerBound, "measurement": Decimal("5.1")},
    ]


def test_lower_bound_is_inferred_with_missing_measurement(probs_answer_query):
    """
    If an observation does not have a measurement, the output is the same as `test_lower_bound_is_inferred_with_missing_observation`
    """
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Cake", measurement=5.1)
        + make_observation(object=":Bread", measurement=None)
    )
    results = probs_answer_query(facts, QUERY)
    assert results == [
        {"bound": PROBS.LowerBound, "measurement": Decimal("5.1")},
    ]


def test_lower_bound_is_inferred_with_only_missing_measurements(probs_answer_query):
    """
    If we combine two observations without measurements, we should get a lower bound with `0` as `measurement`.
    """
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Cake", measurement=None)
        + make_observation(object=":Bread", measurement=None)
    )
    results = probs_answer_query(facts, QUERY)
    assert results == [
        {"bound": PROBS.LowerBound, "measurement": Decimal("0")},
    ]


def test_exact_bound_is_inferred_with_zero_measurement(probs_answer_query):
    """
    If the `measurement` is `0`, the behaviour should be the same as for any other value.
    """
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Cake", measurement=5.1)
        + make_observation(object=":Bread", measurement=0)
    )
    results = probs_answer_query(facts, QUERY)
    assert results == [
        {"bound": PROBS.ExactBound, "measurement": Decimal("5.1")},
    ]


def test_exact_bound_is_inferred_with_only_zero_measurements(probs_answer_query):
    """
    If the `measurement` is `0`, the behaviour should be the same as for any other value.
    """
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Cake", measurement=0)
        + make_observation(object=":Bread", measurement=0)
    )
    results = probs_answer_query(facts, QUERY)
    assert results == [
        {"bound": PROBS.ExactBound, "measurement": Decimal("0")},
    ]


def test_lower_bound_is_inferred_with_zero_and_missing_measurement(probs_answer_query):
    """
    If the `measurement` is `0`, the behaviour should be the same as for any other value. 
    But since we have no measurement for `Bread` here, a lower bound should be derived.
    """
    facts = (
        BAKED_GOODS_FACTS
        + make_observation(object=":Cake", measurement=0)
        + make_observation(object=":Bread", measurement=None)
    )
    results = probs_answer_query(facts, QUERY)
    assert results == [
        {"bound": PROBS.LowerBound, "measurement": Decimal("0")},
    ]
