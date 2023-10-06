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
                            :Object0.6 .
:Object0.0 :objectComposedOf    :Object0.0.0 ,
                                :Object0.0.1 ,
                                :Object0.0.2 ,
                                :Object0.0.3 ,
                                :Object0.0.4 ,
                                :Object0.0.5 ,
                                :Object0.0.6 .
:Object0.1 :objectComposedOf    :Object0.1.0 ,
                                :Object0.1.1 ,
                                :Object0.1.2 ,
                                :Object0.1.3 ,
                                :Object0.1.4 ,
                                :Object0.1.5 ,
                                :Object0.1.6 .
:Object0.2 :objectComposedOf    :Object0.2.0 ,
                                :Object0.2.1 ,
                                :Object0.2.2 ,
                                :Object0.2.3 ,
                                :Object0.2.4 ,
                                :Object0.2.5 ,
                                :Object0.2.6 .
:Object0.3 :objectComposedOf    :Object0.3.0 ,
                                :Object0.3.1 ,
                                :Object0.3.2 ,
                                :Object0.3.3 ,
                                :Object0.3.4 ,
                                :Object0.3.5 ,
                                :Object0.3.6 .
:Object0.4 :objectComposedOf    :Object0.4.0 ,
                                :Object0.4.1 ,
                                :Object0.4.2 ,
                                :Object0.4.3 ,
                                :Object0.4.4 ,
                                :Object0.4.5 ,
                                :Object0.4.6 .
:Object0.5 :objectComposedOf    :Object0.5.0 ,
                                :Object0.5.1 ,
                                :Object0.5.2 ,
                                :Object0.5.3 ,
                                :Object0.5.4 ,
                                :Object0.5.5 ,
                                :Object0.5.6 .
:Object0.6 :objectComposedOf    :Object0.6.0 ,
                                :Object0.6.1 ,
                                :Object0.6.2 ,
                                :Object0.6.3 ,
                                :Object0.6.4 ,
                                :Object0.6.5 ,
                                :Object0.6.6 .
"""

def test_obs_1_5x5_1eachsame_inferred_obs_37(probs_count_inferred_obs):
    """
    1 Object, 5 components each with 5 components, 1 Observations each, same probsObs
    Observations to be inferred: 37
    User time (seconds): ~1E0
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(5)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(5) for k in range(5)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(1)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 37

    # Full version: 5+32 (see below for some details)
    # WDF version:
    # Iteration 1:
    #   [:Object1.1 + ... + :Object1.5 -> :Object1]
    #     1  (D1.1+D1.2+D1.3+D1.4+D1.5)
    #   [:Object1.1.1 + ... + :Object1.1.5 -> :Object1.1]
    #     1  (D1.1.1+D1.1.2+D1.1.3+D1.1.4+D1.1.5)
    #   [:Object1.2.1 + ... + :Object1.2.5 -> :Object1.2]
    #     1  (D1.2.1+D1.2.2+D1.2.3+D1.2.4+D1.2.5)
    #   [:Object1.3.1 + ... + :Object1.3.5 -> :Object1.3]
    #     1  (D1.3.1+D1.3.2+D1.3.3+D1.3.4+D1.3.5)
    #   [:Object1.4.1 + ... + :Object1.4.5 -> :Object1.4]
    #     1  (D1.4.1+D1.4.2+D1.4.3+D1.4.4+D1.4.5)
    #   [:Object1.5.1 + ... + :Object1.5.5 -> :Object1.5]
    #     1  (D1.5.1+D1.5.2+D1.5.3+D1.5.4+D1.5.5)
    # Deleting duplicates:
    #     No duplicates
    # Iteration 2:
    #   [:Object1.1 + ... + :Object1.5 -> :Object1]
    #     32 (
    #     -1  ~~D1.1+D1.2+D1.3+D1.4+D1.5~~ already there
    #         D1.1+D1.2+D1.3+D1.4+I1.5,
    #         D1.1+D1.2+D1.3+I1.4+D1.5, D1.1+D1.2+D1.3+I1.4+I1.5,
    #         D1.1+D1.2+I1.3+D1.4+D1.5, D1.1+D1.2+I1.3+D1.4+I1.5, D1.1+D1.2+I1.3+I1.4+D1.5, D1.1+D1.2+I1.3+I1.4+I1.5,
    #         D1.1+I1.2+D1.3+D1.4+D1.5, D1.1+I1.2+D1.3+D1.4+I1.5, D1.1+I1.2+D1.3+I1.4+D1.5, D1.1+I1.2+D1.3+I1.4+I1.5, D1.1+I1.2+I1.3+D1.4+D1.5, D1.1+I1.2+I1.3+D1.4+I1.5, D1.1+I1.2+I1.3+I1.4+D1.5, D1.1+I1.2+I1.3+I1.4+I1.5,
    #         I1.1+D1.2+D1.3+D1.4+D1.5,
    #         I1.1+D1.2+D1.3+D1.4+I1.5,
    #         I1.1+D1.2+D1.3+I1.4+D1.5, I1.1+D1.2+D1.3+I1.4+I1.5,
    #         I1.1+D1.2+I1.3+D1.4+D1.5, I1.1+D1.2+I1.3+D1.4+I1.5, I1.1+D1.2+I1.3+I1.4+D1.5, I1.1+D1.2+I1.3+I1.4+I1.5,
    #         I1.1+I1.2+D1.3+D1.4+D1.5, I1.1+I1.2+D1.3+D1.4+I1.5, I1.1+I1.2+D1.3+I1.4+D1.5, I1.1+I1.2+D1.3+I1.4+I1.5, I1.1+I1.2+I1.3+D1.4+D1.5, I1.1+I1.2+I1.3+D1.4+I1.5, I1.1+I1.2+I1.3+I1.4+D1.5, I1.1+I1.2+I1.3+I1.4+I1.5,
    #        )
    #      or, equivalently
    #       DDDDD
    #       DDDDI
    #       DDDID DDDII
    #       DDIDD DDIDI DDIID DDIII
    #       DIDDD DIDDI DIDID DIDII DIIDD DIIDI DIIID DIIII
    #       IDDDD
    #       IDDDI
    #       IDDID IDDII
    #       IDIDD IDIDI IDIID IDIII
    #       IIDDD IIDDI IIDID IIDII IIIDD IIIDI IIIID IIIII
    # Deleting duplicates:
    #     No duplicates
    #

def test_obs_1_2x2_2eachsame_inferred_obs_44(probs_count_inferred_obs):
    """
    1 Object, 2 components each with 2 components, 2 Observations each, same probsObs.
    Observations to be inferred: 44
    User time (seconds): ~1E0
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(2)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(2) for k in range(2)]
    input_obs = "\n".join(
        make_observation(object=obj, obs_id=f"-{obj[7:]}{repeat}", measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for repeat in "ab"
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 44

    # Full version: 4+4+4+36-4 (see below for some details)
    # WDF version:
    # Iteration 1:
    #   [:Object1.1 + :Object1.2 -> :Object1]
    #     4  (D1.1a+D1.2a, D1.1a+D1.2b, D1.1b+D1.2a, D1.1b+D1.2b)
    #   [:Object1.1.1 + :Object1.1.2 -> :Object1.1]
    #     4  (D1.1.1a+D1.1.2a, D1.1.1a+D1.1.2b, D1.1.1b+D1.1.2a, D1.1.1b+D1.1.2b)
    #   [:Object1.2.1 + :Object1.2.2 -> :Object1.2]
    #     4  (D1.2.1a+D1.2.2a, D1.2.1a+D1.1.2b, D1.2.1b+D1.2.2a, D1.2.1b+D1.2.2b)
    # Deleting duplicates:
    #     No duplicates
    # Iteration 2:
    #   [:Object1.1 + :Object1.2 -> :Object1]
    #     36 (
    #     -4  ~~D1.1a+D1.2a, D1.1a+D1.2b, D1.1b+D1.2a, D1.1b+D1.2b~~ already there
    #         D1.1a+I1.2aa, D1.1a+I1.2ab, D1.1a+I1.2ba, D1.1a+I1.2bb,
    #         D1.1b+I1.2aa, D1.1b+I1.2ab, D1.1b+I1.2ba, D1.1b+I1.2bb,
    #         I1.1aa+D1.2a, I1.1ab+D1.2a, I1.1ba+D1.2a, I1.1bb+D1.2a,
    #         I1.1aa+D1.2b, I1.1ab+D1.2b, I1.1ba+D1.2b, I1.1bb+D1.2b,
    #         I1.1aa+I1.2aa, I1.1aa+I1.2ab, I1.1aa+I1.2ba, I1.1aa+I1.2bb,
    #         I1.1ab+I1.2aa, I1.1ab+I1.2ab, I1.1ab+I1.2ba, I1.1ab+I1.2bb,
    #         I1.1ba+I1.2aa, I1.1ba+I1.2ab, I1.1ba+I1.2ba, I1.1ba+I1.2bb,
    #         I1.1bb+I1.2aa, I1.1bb+I1.2ab, I1.1bb+I1.2ba, I1.1bb+I1.2bb,
    #        )
    # Deleting duplicates:
    #     No duplicates
    #

def test_obs_1_3x3_2eachsame_inferred_obs_1024(probs_count_inferred_obs):
    """
    1 Object, 3 components each with 3 components, 2 Observations each, same probsObs.
    Observations to be inferred: 1024
    User time (seconds): ~1E0
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(3)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(3) for k in range(3)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 1024 # 8*3+8+1000-8

@pytest.mark.slow
def test_obs_1_4x4_2eachsame_inferred_obs_105040(probs_count_inferred_obs):
    """
    1 Object, 4 components each with 4 components, 2 Observations each, same probsObs.
    Observations to be inferred: 105040
    User time (seconds): ~1E1
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(4)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(4) for k in range(4)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 105040 # 16*4+16+104976-16

@pytest.mark.slow
def test_obs_1_4x5_2eachsame_inferred_obs_1336464(probs_count_inferred_obs):
    """
    1 Object, 4 components each with 5 components, 2 Observations each, same probsObs.
    Observations to be inferred: 1336464
    User time (seconds): ~1E2
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(4)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(4) for k in range(5)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 1336464 # 2^5*4+2^4+1336336-16

@pytest.mark.skip(reason="our computers cannot process this, it is too big")
def test_obs_1_4x6_2eachsame_inferred_obs_18974992(probs_count_inferred_obs):
    """
    1 Object, 4 components each with 6 components, 2 Observations each, same probsObs.
    Observations to be inferred: 18974992
    User time (seconds): ~1E3
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(4)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(4) for k in range(6)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 18974992 # 2^6*4+2^4+(2^6+2)^4-16=256+18974736

@pytest.mark.skip(reason="our computers cannot process this, it is too big")
def test_obs_1_5x5_2eachsame_inferred_obs_45435584(probs_count_inferred_obs):
    """
    1 Object, 5 components each with 5 components, 2 Observations each, same
    probsObs.
    Observations to be inferred: 45435584
    
    CANNOT WORK! It should create 45'435'584 of new Observations!!
    Assuming 1 byte per character and that each observation contains around 1000
    characters (I have checked this in the output of PRODCOM), only to store
    them we would need more than 40 GB to store them (in RAM, while processing
    it, they would be much more)
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(5)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(5) for k in range(5)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(2)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 45435584 # 32*5+32+45435424-32

# @pytest.mark.slow
def test_obs_1_3x3_3eachsame_inferred_obs_27081(probs_count_inferred_obs):
    """
    1 Object, 3 components each with 3 components, 3 Observations each, same probsObs.
    Observations to be inferred: 27081
    User time (seconds): ~1E0
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(3)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(3) for k in range(3)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(3)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 27081 # 27*3+27+27000-27

@pytest.mark.skip(reason="our computers cannot process this, it is too big")
def test_obs_1_4x4_3eachsame_inferred_obs_49787460(probs_count_inferred_obs):
    """
    1 Object, 4 components each with 4 components, 3 Observations each, same
    probsObs.
    Observations to be inferred: 49787460

    CANNOT WORK! It should create 49'787'460 of new Observations!!
    """

    obj_level1 = [f":Object{i}.{j}" for i in range(1) for j in range(4)]
    obj_level2 = [f":Object{i}.{j}.{k}" for i in range(1) for j in range(4) for k in range(4)]
    input_obs = "\n".join(
        make_observation(object=obj, measurement=round(random(), 6))
        for obj_list in [obj_level1, obj_level2]
        for obj in obj_list
        for _ in range(3)
    )
    assert probs_count_inferred_obs(OBJECT_FACTS + input_obs) == 49787460 # 81*4+81+49787136-81
