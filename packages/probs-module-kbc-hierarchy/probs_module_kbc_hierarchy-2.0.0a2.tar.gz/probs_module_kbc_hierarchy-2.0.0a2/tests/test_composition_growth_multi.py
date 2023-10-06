# -*- coding: utf-8 -*-
"""Test case of an object composed of objects, composed of objects, ... with
observations at different level of this hierarchy."""

import pytest
from random import random
from utils import make_observation

levels = 6

OBJECT_FACTS = \
    '\n'.join([f":Object0 :objectComposedOf :Object0.{i} ." for i in range(levels)]) + \
        '\n'.join([f":Object0.{i} :objectComposedOf :Object0.{i}.{j} ." for i in range(levels) for j in range(levels)]) + \
            '\n'.join([f":Object0.{i}.{j} :objectComposedOf :Object0.{i}.{j}.{k} ." for i in range(levels) for j in range(levels) for k in range(levels)]) + \
                '\n'.join([f":Object0.{i}.{j}.{k} :objectComposedOf :Object0.{i}.{j}.{k}.{l} ." for i in range(levels) for j in range(levels) for k in range(levels) for l in range(levels)]) + \
                    '\n'.join([f":Object0.{i}.{j}.{k}.{l} :objectComposedOf :Object0.{i}.{j}.{k}.{l}.{m} ." for i in range(levels) for j in range(levels) for k in range(levels) for l in range(levels) for m in range(levels)]) + \
                        '\n'.join([f":Object0.{i}.{j}.{k}.{l}.{m} :objectComposedOf :Object0.{i}.{j}.{k}.{l}.{m}.{n} ." for i in range(levels) for j in range(levels) for k in range(levels) for l in range(levels) for m in range(levels) for n in range(levels)])

def test_obs_obj1_comp3x3x3x3x3_obs2x2_min_inferred_obs_648(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components each with 3 components each with 3 components
    2 Observations for each object for the bottom 2 levels
    lower bound (non-compatible observations)
    Observations to be inferred: 648
    User time (seconds): ~1E0
    """

    components = 3
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in "ab"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,5)+2*pow(components,4)

def test_obs_obj1_comp3x3x3x3x3_obs2x2x2_min_inferred_obs_702(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components each with 3 components each with 3 components
    2 Observations for each object for the bottom 3 levels
    lower bound (non-compatible observations)
    Observations to be inferred: 702
    User time (seconds): ~1E0
    """

    components = 3
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}" for i in range(components) for j in range(components) for k in range(components)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in "ab"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,5)+2*pow(components,4)+2*pow(components,3)

def test_obs_obj1_comp3x3x3x3x3_obs5x5_min_inferred_obs_1620(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components each with 3 components each with 3 components
    5 Observations for each object for the bottom 2 levels
    lower bound (non-compatible observations)
    Observations to be inferred: 1620
    User time (seconds): ~1E0
    """

    components = 3
    obs_labels = "abcde"
    n_obs = len(obs_labels)
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in obs_labels
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == n_obs*pow(components,5)+n_obs*pow(components,4)

def test_obs_obj1_comp3x3x3x3x3_obs5x5x5_min_inferred_obs_1755(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components each with 3 components each with 3 components
    5 Observations for each object for the bottom 3 levels
    lower bound (non-compatible observations)
    Observations to be inferred: 1755
    User time (seconds): ~1E0
    """

    components = 3
    obs_labels = "abcde"
    n_obs = len(obs_labels)
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}" for i in range(components) for j in range(components) for k in range(components)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in obs_labels
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == n_obs*pow(components,5)+n_obs*pow(components,4)+n_obs*pow(components,3)

@pytest.mark.slow
def test_obs_obj1_comp5x5x5x5x5_obs5x5_min_inferred_obs_18750(probs_count_inferred_obs):
    """
    1 Object
    5 components each with 5 components each with 5 components each with 5 components each with 5 components
    5 Observations for each object for the bottom 2 levels
    lower bound (non-compatible observations)
    Observations to be inferred: 18750
    User time (seconds): ~1E1
    """

    components = 5
    obs_labels = "abcde"
    n_obs = len(obs_labels)
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in obs_labels
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == n_obs*pow(components,5)+n_obs*pow(components,4)

@pytest.mark.slow
def test_obs_obj1_comp5x5x5x5x5_obs5x5x5_min_inferred_obs_19375(probs_count_inferred_obs):
    """
    1 Object
    5 components each with 5 components each with 5 components each with 5 components each with 5 components
    5 Observations for each object for the bottom 3 levels
    lower bound (non-compatible observations)
    Observations to be inferred: 19375
    User time (seconds): ~1E1
    """

    components = 5
    obs_labels = "abcde"
    n_obs = len(obs_labels)
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}" for i in range(components) for j in range(components) for k in range(components)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in obs_labels
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == n_obs*pow(components,5)+n_obs*pow(components,4)+n_obs*pow(components,3)

@pytest.mark.slow
def test_obs_obj1_comp5x5x5x5x5_obs5x5x5x5_min_inferred_obs_19500(probs_count_inferred_obs):
    """
    1 Object
    5 components each with 5 components each with 5 components each with 5 components each with 5 components
    5 Observations for each object for the bottom 4 levels
    lower bound (non-compatible observations)
    Observations to be inferred: 19500
    User time (seconds): ~1E1
    """

    components = 5
    obs_labels = "abcde"
    n_obs = len(obs_labels)
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
    ] + [
        f":Object0.{i}.{j}.{k}" for i in range(components) for j in range(components) for k in range(components)
    ] + [
        f":Object0.{i}.{j}" for i in range(components) for j in range(components)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in obs_labels
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == n_obs*pow(components,5)+n_obs*pow(components,4)+n_obs*pow(components,3)+n_obs*pow(components,2)
