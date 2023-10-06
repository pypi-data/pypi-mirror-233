# -*- coding: utf-8 -*-
"""Test case of an object composed of objects, composed of objects, ... with
observations only in the bottom level of this hierarchy."""

import pytest
from random import random
from utils import make_observation

# Min: (lower bound) Nobs * Ncomp_{n} * Ncomp_{n-1} * ... * Ncomp_{0}
# Max: (upper bound) (...(Nobs ^ Ncomp_{n}) ^ Ncomp_{n-1}) ^ ...) ^ Ncomp_{0}

levels = 6

OBJECT_FACTS = \
    '\n'.join([f":Object0 :objectComposedOf :Object0.{i} ." for i in range(levels)]) + \
        '\n'.join([f":Object0.{i} :objectComposedOf :Object0.{i}.{j} ." for i in range(levels) for j in range(levels)]) + \
            '\n'.join([f":Object0.{i}.{j} :objectComposedOf :Object0.{i}.{j}.{k} ." for i in range(levels) for j in range(levels) for k in range(levels)]) + \
                '\n'.join([f":Object0.{i}.{j}.{k} :objectComposedOf :Object0.{i}.{j}.{k}.{l} ." for i in range(levels) for j in range(levels) for k in range(levels) for l in range(levels)]) + \
                    '\n'.join([f":Object0.{i}.{j}.{k}.{l} :objectComposedOf :Object0.{i}.{j}.{k}.{l}.{m} ." for i in range(levels) for j in range(levels) for k in range(levels) for l in range(levels) for m in range(levels)]) + \
                        '\n'.join([f":Object0.{i}.{j}.{k}.{l}.{m} :objectComposedOf :Object0.{i}.{j}.{k}.{l}.{m}.{n} ." for i in range(levels) for j in range(levels) for k in range(levels) for l in range(levels) for m in range(levels) for n in range(levels)])

def test_obs_obj1_comp1x2x3_obs2_min_inferred_obs_12(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 12
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}" for i in range(1) for j in range(2) for k in range(3)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*3*2*1

def test_obs_obj1_comp1x2x3_obs2_max_inferred_obs_64(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 64
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}" for i in range(1) for j in range(2) for k in range(3)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == pow(pow(pow(2,3),2),1)

def test_obs_obj1_comp1x2x3_obs3_min_inferred_obs_18(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components
    3 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 18
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}" for i in range(1) for j in range(2) for k in range(3)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in "abc"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 3*3*2*1

def test_obs_obj1_comp1x2x3_obs3_max_inferred_obs_729(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components
    3 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 729
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}" for i in range(1) for j in range(2) for k in range(3)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R-same-for-all",
        )
        for obj in objects
        for repeat in "abc"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == pow(pow(pow(3,3),2),1)

def test_obs_obj1_comp1x2x3x4_obs2_min_inferred_obs_48(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 48
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(1) for j in range(2) for k in range(3) for l in range(4)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*4*3*2*1

@pytest.mark.skip(reason="our computers cannot process this, it is too big")
def test_obs_obj1_comp1x2x3x4_obs2_max_inferred_obs_16777216(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 16'777'216
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(1) for j in range(2) for k in range(3) for l in range(4)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") ==  pow(pow(pow(pow(2,4),3),2),1)

def test_obs_obj1_comp1x2x3x4x5_obs2_min_inferred_obs_240(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components each with 5 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 240
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(1) for j in range(2) for k in range(3) for l in range(4) for m in range(5)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*5*4*3*2*1

def test_obs_obj1_comp1x2x3x4x5x6_obs2_min_inferred_obs_1440(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components each with 5 components each with 6 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 1440
    User time (seconds): ~1E0
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(1) for j in range(2) for k in range(3) for l in range(4) for m in range(5) for n in range(6)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*6*5*4*3*2*1

@pytest.mark.slow
def test_obs_obj1_comp1x2x3x4x5x6_obs3_min_inferred_obs_2160(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components each with 5 components each with 6 components
    3 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 2160
    User time (seconds): ~1E1
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(1) for j in range(2) for k in range(3) for l in range(4) for m in range(5) for n in range(6)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in "abc"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 3*6*5*4*3*2*1

@pytest.mark.slow
def test_obs_obj1_comp1x2x3x4x5x6_obs4_min_inferred_obs_2880(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components each with 5 components each with 6 components
    4 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 2880
    User time (seconds): ~1E1
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(1) for j in range(2) for k in range(3) for l in range(4) for m in range(5) for n in range(6)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in "abcd"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 4*6*5*4*3*2*1

@pytest.mark.slow
def test_obs_obj1_comp1x2x3x4x5x6_obs5_min_inferred_obs_3600(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components each with 5 components each with 6 components
    5 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 3600
    User time (seconds): ~1E1
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(1) for j in range(2) for k in range(3) for l in range(4) for m in range(5) for n in range(6)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in "abcde"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 5*6*5*4*3*2*1

@pytest.mark.slow
def test_obs_obj1_comp1x2x3x4x5x6_obs6_min_inferred_obs_4320(probs_count_inferred_obs):
    """
    1 Object
    1 components each with 2 components each with 3 components each with 4 components each with 5 components each with 6 components
    5 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 4320
    User time (seconds): ~1E1
    """

    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(1) for j in range(2) for k in range(3) for l in range(4) for m in range(5) for n in range(6)
    ]
    input_obs = "\n".join(
        make_observation(
            object=obj,
            obs_id=f"-{obj[7:]}{repeat}",
            measurement=round(random(), 6),
            region=f":R{obj[7:]}{repeat}",
        )
        for obj in objects
        for repeat in "abcdef"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 6*6*5*4*3*2*1

def test_obs_obj1_comp2x2x2_obs2_max_inferred_obs_256(probs_count_inferred_obs):
    """
    1 Object
    2 components each with 2 components each with 2 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 256
    User time (seconds): ~1E0
    """

    components = 2
    objects = [
        f":Object0.{i}.{j}.{k}" for i in range(components) for j in range(components) for k in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") ==  pow(pow(pow(2,components),components),components)

@pytest.mark.skip(reason="our computers cannot process this, it is too big")
def test_obs_obj1_comp3x3x3_obs2_max_inferred_obs_134217728(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 134'217'728
    """

    components = 3
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == pow(pow(pow(2,components),components),components)

@pytest.mark.slow
def test_obs_obj1_comp2x2x2x2_obs2_max_inferred_obs_65536(probs_count_inferred_obs):
    """
    1 Object
    2 components each with 2 components each with 2 components each with 2 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 65536
    User time (seconds): ~1E1
    """

    components = 2
    objects = [
        f":Object0.{i}.{j}.{k}.{l}" for i in range(components) for j in range(components) for k in range(components) for l in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") ==  pow(pow(pow(pow(2,components),components),components),components)

def test_obs_obj1_comp2x2x2x2x2_obs2_min_inferred_obs_64(probs_count_inferred_obs):
    """
    1 Object
    2 components each with 2 components each with 2 components each with 2 components each with 2 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 64
    User time (seconds): ~1E0
    """

    components = 2
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,5)

def test_obs_obj1_comp3x3x3x3x3_obs2_min_inferred_obs_486(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components each with 3 components each with 3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 486
    User time (seconds): ~1E0
    """

    components = 3
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,5)

@pytest.mark.slow
def test_obs_obj1_comp4x4x4x4x4_obs2_min_inferred_obs_2048(probs_count_inferred_obs):
    """
    1 Object
    4 components each with 4 components each with 4 components each with 4 components each with 4 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 2048
    User time (seconds): ~1E1
    """

    components = 4
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,5)

@pytest.mark.slow
def test_obs_obj1_comp5x5x5x5x5_obs2_min_inferred_obs_6250(probs_count_inferred_obs):
    """
    1 Object
    5 components each with 5 components each with 5 components each with 5 components each with 5 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 6250
    User time (seconds): ~1E1
    """

    components = 5
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,5)

def test_obs_obj1_comp2x2x2x2x2x2_obs2_min_inferred_obs_128(probs_count_inferred_obs):
    """
    1 Object
    2 components each with 2 components each with 2 components each with 2 components each with 2 components each with 2 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 128
    User time (seconds): ~1E0
    """

    components = 2
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components) for n in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,levels)

def test_obs_obj1_comp3x3x3x3x3x3_obs2_min_inferred_obs_1458(probs_count_inferred_obs):
    """
    1 Object
    3 components each with 3 components each with 3 components each with 3 components each with 3 components each with 3 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 1458
    User time (seconds): ~1E0
    """

    components = 3
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components) for n in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,levels)

@pytest.mark.slow
def test_obs_obj1_comp4x4x4x4x4x4_obs2_min_inferred_obs_8192(probs_count_inferred_obs):
    """
    1 Object
    4 components each with 4 components each with 4 components each with 4 components each with 4 components each with 4 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 8192
    User time (seconds): ~1E1
    """

    components = 4
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components) for n in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,levels)

@pytest.mark.slow
def test_obs_obj1_comp5x5x5x5x5x5_obs2_min_inferred_obs_31250(probs_count_inferred_obs):
    """
    1 Object
    5 components each with 5 components each with 5 components each with 5 components each with 5 components each with 5 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 31250
    User time (seconds): ~1E2
    """

    components = 5
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components) for n in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,levels)

@pytest.mark.slow
def test_obs_obj1_comp6x6x6x6x6x6_obs2_min_inferred_obs_93312(probs_count_inferred_obs):
    """
    1 Object
    6 components each with 6 components each with 6 components each with 6 components each with 6 components each with 6 components
    2 Observations for each object at the bottom
    lower bound (non-compatible observations)
    Observations to be inferred: 93312
    User time (seconds): ~1E2
    """

    components = 6
    objects = [
        f":Object0.{i}.{j}.{k}.{l}.{m}.{n}" for i in range(components) for j in range(components) for k in range(components) for l in range(components) for m in range(components) for n in range(components)
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
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs, ":Object0") == 2*pow(components,levels)
