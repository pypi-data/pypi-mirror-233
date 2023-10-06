# -*- coding: utf-8 -*-

import pytest
from random import randrange, random


from utils import make_observation


OBJECT_FACTS = r"""
    :Object0 :objectComposedOf  :Object0.0 ,
                                :Object0.1 ,
                                :Object0.2 ,
                                :Object0.3 ,
                                :Object0.4 ,
                                :Object0.5 ,
                                :Object0.6 ,
                                :Object0.7 ,
                                :Object0.8 ,
                                :Object0.9 .
    :Object1 :objectComposedOf  :Object1.0 ,
                                :Object1.1 ,
                                :Object1.2 ,
                                :Object1.3 ,
                                :Object1.4 ,
                                :Object1.5 ,
                                :Object1.6 ,
                                :Object1.7 ,
                                :Object1.8 ,
                                :Object1.9 .
"""


def test_obs_1_10_1each_inferred_obs_1(probs_count_inferred_obs):
    """
    1 Object, 10 components, 1 Observation each
    Observations to be inferred: 1
    User time (seconds): ~1E0
    """
    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=1)
        for i in range(1)
        for j in range(10)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 1


def test_obs_2_10_1each_inferred_obs_2(probs_count_inferred_obs):
    """
    2 Objects, 10 components, 1 Observation each
    Observations to be inferred: 2
    User time (seconds): ~1E0
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=1)
        for i in range(2)
        for j in range(10)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 2


def test_obs_2_10_2each_inferred_obs_4(probs_count_inferred_obs):
    """
    2 Object, 10 components, 2 Observation each
    Observations to be inferred: 4
    User time (seconds): ~1E0
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=1, region=f":R{k}")
        for i in range(2)
        for j in range(10)
        for k in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 4


def test_obs_2_10_3each_inferred_obs_6(probs_count_inferred_obs):
    """
    2 Object, 10 components, 3 Observation each
    Observations to be inferred: 6
    User time (seconds): ~1E0
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=1, region=f":R{k}")
        for i in range(2)
        for j in range(10)
        for k in range(3)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 6


def test_obs_1_10_2eachsame_inferred_obs_1024(probs_count_inferred_obs):
    """
    1 Object, 10 components, 2 Observation each, same probsObs
    Observations to be inferred: 1024
    User time (seconds): ~1E0
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=randrange(100000))
        for i in range(1)
        for j in range(10)
        for _ in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 1024


# @pytest.mark.slow
def test_obs_2_10_2eachsame_inferred_obs_2048(probs_count_inferred_obs):
    """
    2 Object, 10 components, 2 Observation each, same probsObs
    Observations to be inferred: 2048
    User time (seconds): ~1E0
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=randrange(100000))
        for i in range(2)
        for j in range(10)
        for _ in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 2048


@pytest.mark.slow
def test_obs_1_10_3eachsame_inferred_obs_59049(probs_count_inferred_obs):
    """
    1 Object, 10 components, 3 Observations each, same probsObs
    Observations to be inferred: 59049
    User time (seconds): ~1E1
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=randrange(100000))
        for i in range(1)
        for j in range(10)
        for _ in range(3)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 59049


@pytest.mark.slow
def test_obs_2_10_3eachsame_inferred_obs_118098(probs_count_inferred_obs):
    """
    2 Object, 10 components, 3 Observations each, same probsObs
    Observations to be inferred: 118098
    User time (seconds): ~1E1
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=randrange(100000))
        for i in range(2)
        for j in range(10)
        for _ in range(3)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 118098


# @pytest.mark.slow
def test_obs_1_5_5eachsame_inferred_obs_3125(probs_count_inferred_obs):
    """
    1 Object, 5 components, 5 Observations each, same probsObs
    Observations to be inferred: 3125
    User time (seconds): ~1E0
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=randrange(100000))
        for i in range(1)
        for j in range(5)
        for _ in range(5)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 3125


@pytest.mark.slow
def test_obs_1_6_6eachsame_inferred_obs_46656(probs_count_inferred_obs):
    """
    1 Object, 6 components, 6 Observations each, same probsObs
    Observations to be inferred: 46656
    User time (seconds): ~1E1
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=randrange(100000))
        for i in range(1)
        for j in range(6)
        for _ in range(6)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 46656


@pytest.mark.slow
def test_obs_1_7_6eachsame_inferred_obs_279936(probs_count_inferred_obs):
    """
    1 Object, 7 components, 6 Observations each, same probsObs
    Observations to be inferred: 279936
    User time (seconds): ~1E2
    """

    input_obs = "\n".join(
        make_observation(object=f":Object{i}.{j}", measurement=randrange(100000))
        for i in range(1)
        for j in range(7)
        for _ in range(6)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 279936
