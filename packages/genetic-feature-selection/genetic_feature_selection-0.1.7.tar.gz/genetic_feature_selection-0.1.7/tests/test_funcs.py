from genetic_feature_selection.genetic_funcs import weighted_selection
import pytest


@pytest.fixture
def evaluted_feature_vectors():
    efvs = [
        (0.9, [1,2,3,4]),
        (0.88, [5,6,7,8]),
    ]
    return efvs


@pytest.fixture
def evaluted_feature_vectors_0_score():
    efvs = [
        (0.9, [1,2,3,4]),
        (0.0, [5,6,7,8]),
    ]
    return efvs


def test_weighted_selection(evaluted_feature_vectors):
    child = weighted_selection(
        evaluted_feature_vectors[0], evaluted_feature_vectors[1]
    )

    assert len(child) == len(evaluted_feature_vectors[0][1])


def test_weighted_selection_1_0(evaluted_feature_vectors_0_score):
    """When one of the parents have score equal to zero"""
    p1_genes = evaluted_feature_vectors_0_score[0][1] 

    child = weighted_selection(
        evaluted_feature_vectors_0_score[0], 
        evaluted_feature_vectors_0_score[1]
    )

    assert len(child) == len(evaluted_feature_vectors_0_score[0][1])

