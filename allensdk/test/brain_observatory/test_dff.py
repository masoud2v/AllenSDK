# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2017. Allen Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Redistributions for commercial purposes are not permitted without the
# Allen Institute's written permission.
# For purposes of this license, commercial purposes is the incorporation of the
# Allen Institute's software into anything for which you will charge fees or
# other compensation. Contact terms@alleninstitute.org for commercial licensing
# opportunities.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
import allensdk.brain_observatory.dff as dff
import numpy as np
import pytest
from matplotlib.pyplot import Figure
from mock import patch


def test_movingmode_fast():
    # check basic behavior
    x = np.array([0, 10, 0, 0, 20, 0, 0, 0, 30])
    kernelsize = 4
    y = np.zeros(x.shape)

    dff.movingmode_fast(x, kernelsize, y)

    assert np.all(y == 0)

    # check window edges
    x = np.array([0, 0, 1, 1, 2, 2, 3, 3])
    kernelsize = 2
    y = np.zeros(x.shape)

    dff.movingmode_fast(x, kernelsize, y)

    assert np.all(x == y)

    # check > 16 bit
    x = np.array([4097, 4097, 4097, 4097])
    kernelsize = 2
    y = np.zeros(x.shape)

    dff.movingmode_fast(x, kernelsize, y)

    assert np.all(y == 4097)

    # check floats
    x = np.array([0, 0, 1, 1, 2, 2, 3, 3], dtype=np.float32)
    kernelsize = 2
    y = np.zeros(x.shape)

    dff.movingmode_fast(x, kernelsize, y)

    assert np.all(x == y)


def test_compute_dff():
    x = np.array([[1, 5, 0, 0, 1, 10, 0, 0, 30, 5]])

    with pytest.warns(FutureWarning):
        dff.compute_dff(x)


def test_compute_dff_windowed_mode():
    x = np.array([[1, 5, -2, 3, 1, 10, 1, -2, 30, 5]])

    with pytest.raises(ValueError):
        dff.compute_dff_windowed_mode(x, mode_kernelsize=0)
    with pytest.raises(ValueError):
        dff.compute_dff_windowed_mode(x, mean_kernelsize=0)

    y = dff.compute_dff_windowed_mode(x)

    assert(y.shape == x.shape)


def test_calculate_dff():
    x = np.array([[1, 5, -2, 3, 1, 10, 1, -2, 30, 5]])

    with patch("os.makedirs") as mock_makedirs:
        with patch.object(Figure, "savefig") as mock_save:
            y = dff.calculate_dff(x)
    assert mock_makedirs.call_count == 0
    assert mock_save.call_count == 0

    with patch("os.makedirs") as mock_makedirs:
        with patch.object(Figure, "savefig") as mock_save:
            y = dff.calculate_dff(x, save_plot_dir="./test")
    assert mock_makedirs.called_once_with("./test")
    assert mock_save.called_once()