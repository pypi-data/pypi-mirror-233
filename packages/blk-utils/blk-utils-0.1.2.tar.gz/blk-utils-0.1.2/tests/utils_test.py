from hypothesis import given, assume, strategies as st
import sys
sys.path.append("..")
from blk_utils import quantize, timer, create_output_path, get_relative_project_dir, cprint

@given(s=st.integers())
def test_integers_return_float(s):
    assume(len(str(s)) < 23)
    assert type(quantize(s)) == float



