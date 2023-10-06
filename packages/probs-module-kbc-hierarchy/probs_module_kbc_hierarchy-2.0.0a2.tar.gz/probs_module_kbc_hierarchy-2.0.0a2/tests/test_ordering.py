# -*- coding: utf-8 -*-
"""Test case of an object composed of objects with different numbers of observations."""

import pytest
from random import random
from utils import make_observation

@pytest.mark.slow
def test_ordering_1000_1000_max_top(probs_count_inferred_obs):
    """
    *Input*
    1 Object
    1000 components
    1000 Observations for the first Object
    1 Observation for each other Object
    All compatible observations (max)
    
    *Output*
    Observations to be inferred: 1000
    
    *Stats (1 thread)*
    Lexicographical order:
     - User time (seconds): ~14
     - Maximum resident set size (MB): ~240
    Number of observations order:
     - User time (seconds): ~14
     - Maximum resident set size (MB): ~190
    """

    # Number of components
    num_components = 1000

    # Number of observations of the first component
    num_observations_first = 1000

    run_ordering_test(probs_count_inferred_obs, num_components, num_observations_first)

@pytest.mark.slow
def test_ordering_1000_1000_max_bottom(probs_count_inferred_obs):
    """
    *Input*
    1 Object
    1000 components
    1000 Observations for the first Object
    1 Observation for each other Object
    All compatible observations (max)
    
    *Output*
    Observations to be inferred: 1000
    
    *Stats (1 thread)*
    Lexicographical order:
     - User time (seconds): ~17
     - Maximum resident set size (MB): ~440
    Number of observations order:
     - User time (seconds): ~14
     - Maximum resident set size (MB): ~190
    """

    # Number of components
    num_components = 1000

    # Number of observations of the first component
    num_observations_first = 1000

    run_ordering_test(probs_count_inferred_obs, num_components, num_observations_first, False)

@pytest.mark.slow
def test_ordering_1000_2000_max_top(probs_count_inferred_obs):
    """
    *Input*
    1 Object
    1000 components
    2000 Observations for the first Object
    1 Observation for each other Object
    All compatible observations (max)
    
    *Output*
    Observations to be inferred: 2000

    *Stats (1 thread)*
    Lexicographical order:
     - User time (seconds): ~25
     - Maximum resident set size (MB): ~460
    Number of observations order:
     - User time (seconds): ~25
     - Maximum resident set size (MB): ~360
    """

    # Number of components
    num_components = 1000

    # Number of observations of the first component
    num_observations_first = 2000

    run_ordering_test(probs_count_inferred_obs, num_components, num_observations_first)

@pytest.mark.slow
def test_ordering_1000_2000_max_bottom(probs_count_inferred_obs):
    """
    *Input*
    1 Object
    1000 components
    2000 Observations for the first Object
    1 Observation for each other Object
    All compatible observations (max)
    
    *Output*
    Observations to be inferred: 2000

    *Stats (1 thread)*
    Lexicographical order:
     - User time (seconds): ~34
     - Maximum resident set size (MB): ~850
    Number of observations order:
     - User time (seconds): ~25
     - Maximum resident set size (MB): ~360
    """

    # Number of components
    num_components = 1000

    # Number of observations of the first component
    num_observations_first = 2000

    run_ordering_test(probs_count_inferred_obs, num_components, num_observations_first, False)

def run_ordering_test(probs_count_inferred_obs, num_components, num_observations_first, from_top=True):
    """
    Utility function
    """

    # First from top or bottom
    if from_top:
        num = "1"
    else:
        num = str(num_components)

    # Components
    components = [
        f":Component{i+1}" for i in range(num_components)
    ]

    # Composition hierarchy
    OBJECT_FACTS = '\n'.join(
        [f":Object :objectComposedOf {obj}." for obj in components]
    )

    # 1 observation for each component
    input_obs = "\n".join(
        make_observation(
            object=obj,
            measurement=round(random(), 6),
        )
        for obj in components
    )

    # Additional observations for the first component
    additional_obs = "\n".join(
        make_observation(
            object=":Component" + num,
            measurement=round(random(), 6),
        )
        for _ in range(num_observations_first-1)
    )

    # Check that the number of inferred observations is the same as the number of observations of the first component
    assert probs_count_inferred_obs(OBJECT_FACTS + '\n' + input_obs + '\n' + additional_obs, ":Object") == num_observations_first
