# -*- coding: utf-8 -*-
"""Test effect of :objectEquivalentTo on Observations"""

from decimal import Decimal
import pytest

from probs_runner import PROBS

from utils import make_observation


############################################################
# Process and object definitions reused
############################################################

CAKE_ROLE_DEFS = r"""
:Cake a :Object ;
    rdfs:label "Cake" .
:Torta a :Object ;
    rdfs:label "Torta" .
:Baking a :Process ;
    rdfs:label "Baking" .
:CakeBaking a :Process ;
    rdfs:label "Baking" .
:Eating a :Process ;
    rdfs:label "Eating" .
:HavingTea a :Process ;
    rdfs:label "Eating" .
"""


############################################################
# Basic checks
############################################################

def test_basic_observations(probs_answer_query):
    """This is not a very good test, but checks everything is running ok."""
    facts = (
        CAKE_ROLE_DEFS
        + make_observation(obs_id="1", object=":Cake", measurement=15.4)
    )
    results = probs_answer_query(facts, r"""
        SELECT ?role ?measurement WHERE {
            :Observation1 :hasRole ?role ;
            :measurement ?measurement .
        }
    """)
    assert results == [
        {"role": PROBS.SoldProduction, "measurement": Decimal('15.4')}
    ]


def test_no_observation_without_equivalence(probs_answer_query):
    """When two objects not equivalent, observations should not be inferred across."""
    facts = (
        CAKE_ROLE_DEFS
        + make_observation(object=":Cake", measurement=15.4)
    )
    results = probs_answer_query(facts, r"""
        SELECT ?observation WHERE { ?observation :objectDefinedBy :Torta . }
    """)
    assert len(results) == 0


############################################################
# Check observations are propagated through equivalence
############################################################

@pytest.mark.parametrize("role", [":SoldProduction", ":Consumption", ":Import", ":Export"])
def test_object_only_roles_object_equivalence(probs_answer_query, role):
    facts = (
        CAKE_ROLE_DEFS
        + make_observation(role=role, object=":Cake", measurement=1)
        + ":Cake :objectEquivalentTo :Torta ."
    )
    results = probs_answer_query(facts, r"""
        SELECT ?observation WHERE { ?observation :objectDefinedBy :Torta . }
    """)
    assert len(results) == 1


def test_process_input_object_equivalence(probs_answer_query):
    facts = (
        CAKE_ROLE_DEFS
        + make_observation(role=":ProcessInput", object=":Cake", process=":Eating", measurement=1)
        + ":Cake :objectEquivalentTo :Torta ."
    )
    results = probs_answer_query(facts, r"""
        SELECT ?observation WHERE { ?observation :objectDefinedBy :Torta . }
    """)
    assert len(results) == 1


def test_process_output_object_equivalence(probs_answer_query):
    facts = (
        CAKE_ROLE_DEFS
        + make_observation(role=":ProcessOutput", object=":Cake", process=":CakeBaking", measurement=1)
        + ":Cake :objectEquivalentTo :Torta ."
    )
    results = probs_answer_query(facts, r"""
        SELECT ?observation WHERE { ?observation :objectDefinedBy :Torta . }
    """)
    assert len(results) == 1