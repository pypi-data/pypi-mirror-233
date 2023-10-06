# -*- coding: utf-8 -*-
"""Test case of an object composed of objects, composed of objects, ... with
observations only in the bottom level of this hierarchy."""

import pytest
from random import randrange, random

from utils import make_observation


OBJECT_FACTS = r"""
:Object0 :objectComposedOf  :Object0.0 ,
                            :Object0.1 ,
                            :Object0.2 .

:Object0.0 :objectComposedOf    :Object0.0.0 ,
                                :Object0.0.1 ,
                                :Object0.0.2 .
:Object0.1 :objectComposedOf    :Object0.1.0 ,
                                :Object0.1.1 ,
                                :Object0.1.2 .
:Object0.2 :objectComposedOf    :Object0.2.0 ,
                                :Object0.2.1 ,
                                :Object0.2.2 .

:Object0.0.0 :objectComposedOf  :Object0.0.0.0 ,
                                :Object0.0.0.1 ,
                                :Object0.0.0.2 .
:Object0.0.1 :objectComposedOf  :Object0.0.1.0 ,
                                :Object0.0.1.1 ,
                                :Object0.0.1.2 .
:Object0.0.2 :objectComposedOf  :Object0.0.2.0 ,
                                :Object0.0.2.1 ,
                                :Object0.0.2.2 .
:Object0.1.0 :objectComposedOf  :Object0.1.0.0 ,
                                :Object0.1.0.1 ,
                                :Object0.1.0.2 .
:Object0.1.1 :objectComposedOf  :Object0.1.1.0 ,
                                :Object0.1.1.1 ,
                                :Object0.1.1.2 .
:Object0.1.2 :objectComposedOf  :Object0.1.2.0 ,
                                :Object0.1.2.1 ,
                                :Object0.1.2.2 .
:Object0.2.0 :objectComposedOf  :Object0.2.0.0 ,
                                :Object0.2.0.1 ,
                                :Object0.2.0.2 .
:Object0.2.1 :objectComposedOf  :Object0.2.1.0 ,
                                :Object0.2.1.1 ,
                                :Object0.2.1.2 .
:Object0.2.2 :objectComposedOf  :Object0.2.2.0 ,
                                :Object0.2.2.1 ,
                                :Object0.2.2.2 .
"""


def test_obs_obj1_comp3_obs2_min_inferred_obs_6(probs_count_inferred_obs):
    """
    1 Object
    3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 6
    User time (seconds): ~1E0
    """

    objects = [f":Object{i}.{j}" for i in range(1) for j in range(3)]
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 6


def test_obs_obj1_comp3_obs2_max_inferred_obs_8(probs_count_inferred_obs):
    """
    1 Object
    3 components
    2 Observations for each object at the bottom
    upper bound (compatible observations)
    Observations to be inferred: 8
    User time (seconds): ~1E0
    """

    objects = [f":Object{i}.{j}" for i in range(1) for j in range(3)]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R-same-for-all",
        )
        for obj in objects
        for repeat in "ab"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 8


def test_obs_obj1_comp3x3_obs2_min_inferred_obs_18(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 18
    User time (seconds): ~1E0
    """

    objects = [
        f":Object{i}.{j}.{k}" for i in range(1) for j in range(3) for k in range(3)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 18


def test_obs_obj1_comp3x3_obs2_max_inferred_obs_512(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components
    2 Observations for each object at the bottom
    upper bound (compatible observations)
    Observations to be inferred: 512
    User time (seconds): ~1E0
    """

    objects = [
        f":Object{i}.{j}.{k}" for i in range(1) for j in range(3) for k in range(3)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R-same-for-all",
        )
        for obj in objects
        for repeat in "ab"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 512


def test_obs_obj1_comp3x3x3_obs2_min_inferred_obs_54(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 54
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}" for i in range(3) for j in range(3) for k in range(3)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 54


@pytest.mark.skip(reason="our computers cannot process this, it is too big")
def test_obs_obj1_comp3x3x3_obs2_max_inferred_obs_134217728(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components
    2 Observations for each object at the bottom
    upper bound (compatible observations)
    Observations to be inferred: 134217728
    """

    objects = [
        f":Object0.{i}.{j}.{k}" for i in range(3) for j in range(3) for k in range(3)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R-same-for-all",
        )
        for obj in objects
        for repeat in "ab"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 134217728
