#!/usr/bin/env python3

import gzip
from probs_runner import probs_enhance_data
from utils import make_observation


def test_output_in_nt_format(tmp_path, script_source_dir):
    original_filename = tmp_path / "original.ttl"
    enhanced_filename = tmp_path / "enhanced.nt.gz"
    with open(original_filename, "wt") as f:
        f.write(make_observation(object=":Cake", measurement=5.1) + "\n")
        f.write(":Cake :objectEquivalentTo :Torta .\n")

    probs_enhance_data(
        original_filename,
        enhanced_filename,
        tmp_path / "working_enhanced",
        script_source_dir,
    )

    with gzip.open(enhanced_filename, "rt") as f:
        lines = f.readlines()

    # Basic check for NT format (no "@prefix")
    assert lines[0].startswith("<")
