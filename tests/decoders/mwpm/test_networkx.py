from qec.decoders.mwpm.networkx import (
    correction_spans_code,
    mwpm_3d,
    mwpm_pairs,
)


def test_empty_matching():
    assert mwpm_pairs([], "vertical", distance=3) == []
    assert mwpm_3d([], "vertical", distance=3) == []


def test_single_defect_matches_boundary():
    pairs = mwpm_pairs(
        [0],
        "vertical",
        distance=3,
    )

    assert len(pairs) == 1
    assert "B" in pairs[0]


def test_mwpm_3d_single_defect_matches_boundary():
    pairs = mwpm_3d(
        [(0, 0)],
        "vertical",
        distance=3,
    )

    assert len(pairs) == 1
    assert "B" in pairs[0]


def test_two_defects_match_together():
    pairs = mwpm_pairs(
        [0, 1],
        "vertical",
        distance=3,
    )

    assert len(pairs) == 1
    assert "B" not in pairs[0]


def test_mwpm_3d_two_defects_match_together():
    pairs = mwpm_3d(
        [(0, 0), (1, 0)],
        "vertical",
        distance=3,
    )

    assert len(pairs) == 1
    assert "B" not in pairs[0]


def test_empty_correction_does_not_span_code():
    assert correction_spans_code(
        [],
        boundary_mode="vertical",
        distance=3,
    ) is False


def test_non_spanning_correction():
    pairs = [("a0", "a2")]

    assert correction_spans_code(
        pairs,
        boundary_mode="vertical",
        distance=3,
    ) is False