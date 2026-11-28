import subprocess
from pathlib import Path
from unittest.mock import Mock

import numpy as np
import pytest

import first_seminar as seminar


def test_rgb_to_yuv_primary_colors():
    red, green, blue = np.eye(3) * 255
    y, u, v = seminar.ColorTranslator.rgb_to_yuv(red, green, blue)
    np.testing.assert_allclose(y, [76.245, 149.685, 29.07])
    np.testing.assert_allclose(u, [-37.51815, -73.6593, 111.18])
    np.testing.assert_allclose(v, [156.825, -131.32245, -25.50255])


def test_yuv_to_rgb_neutral_gray():
    assert seminar.ColorTranslator.yuv_to_rgb(128, 0, 0) == (128, 128, 128)


def test_color_round_trip():
    rgb = (25, 255, 3)
    yuv = seminar.ColorTranslator.rgb_to_yuv(*rgb)
    assert seminar.ColorTranslator.yuv_to_rgb(*yuv) == pytest.approx(rgb, abs=0.01)


@pytest.mark.parametrize("algorithm", ["", "bilinear", "bicubic", "lanczos", "neighbor"])
@pytest.mark.parametrize("factor", [2, 4, 8])
def test_image_resize_builds_ffmpeg_command(monkeypatch, factor, algorithm):
    run = Mock()
    monkeypatch.setattr(seminar.subprocess, "run", run)
    seminar.image_resize(factor, "input with spaces.jpg", algorithm)
    args, kwargs = run.call_args
    command, = args
    assert kwargs == {"check": True}
    assert command[:7] == [
        "ffmpeg", "-i", "input with spaces.jpg", "-update", "1",
        "-vf", f"scale=iw/{factor}:ih/{factor}",
    ]
    suffix = f"_{algorithm}" if algorithm else ""
    assert command[7:-1] == (["-sws_flags", algorithm] if algorithm else [])
    assert Path(command[-1]).as_posix() == (
        f"Exercise4_sources/output_4/resized_{factor}{suffix}.jpg"
    )


@pytest.mark.parametrize(("factor", "algorithm"), [(3, ""), (2, "unknown")])
def test_image_resize_rejects_invalid_options(monkeypatch, capsys, factor, algorithm):
    run = Mock()
    monkeypatch.setattr(seminar.subprocess, "run", run)
    seminar.image_resize(factor, "input.jpg", algorithm)
    run.assert_not_called()
    assert "ERROR" in capsys.readouterr().out


def test_image_resize_propagates_ffmpeg_failure(monkeypatch):
    error = subprocess.CalledProcessError(1, ["ffmpeg"])
    monkeypatch.setattr(seminar.subprocess, "run", Mock(side_effect=error))
    with pytest.raises(subprocess.CalledProcessError) as raised:
        seminar.image_resize(2, "missing.jpg")
    assert raised.value is error


@pytest.mark.parametrize(
    ("matrix", "values"),
    [
        ([[1, 2, 3], [4, 5, 6]], [1, 2, 4, 5, 3, 6]),
        ([[1, 2, 3]], [1, 2, 3]),
        ([[1], [2], [3]], [1, 2, 3]),
        ([[42]], [42]),
    ],
)
def test_zigzag_and_inverse(matrix, values):
    assert seminar.zigzag(matrix) == values
    assert seminar.inverse_zigzag(values, len(matrix), len(matrix[0])) == matrix


def test_inverse_zigzag_rejects_wrong_length():
    with pytest.raises(ValueError, match="List length"):
        seminar.inverse_zigzag([1, 2, 3], rows=2, cols=2)


@pytest.mark.parametrize(
    ("quality", "first_row"),
    [
        (1, [255] * 8),
        (25, [32, 22, 20, 32, 48, 80, 102, 122]),
        (50, [16, 11, 10, 16, 24, 40, 51, 61]),
        (75, [8, 6, 5, 8, 12, 20, 26, 31]),
        (100, [1] * 8),
    ],
)
def test_get_quantization_table(quality, first_row):
    table = seminar.get_quantization_table(quality)
    assert table.shape == (8, 8)
    assert np.all((table >= 1) & (table <= 255))
    np.testing.assert_array_equal(table[0], first_row)


def test_quality_50_returns_independent_table():
    table = seminar.get_quantization_table(50)
    table[0, 0] = 0
    assert seminar.get_quantization_table(50)[0, 0] == 16


@pytest.mark.parametrize(
    ("sample", "dtype", "dc"), [(144, int, 8), (112, np.uint8, -8)]
)
def test_dct_encode_constant_block(sample, dtype, dc):
    block = np.full((8, 8), sample, dtype=dtype)
    assert seminar.DCTEncoder().encode(block) == [dc] + [0] * 63


@pytest.mark.parametrize(("dc", "sample"), [(8, 144), (-8, 112), (128, 255), (-128, 0)])
def test_dct_decode_constant_block_and_clipping(dc, sample):
    assert seminar.DCTEncoder().decode([dc] + [0] * 63) == [[sample] * 8 for _ in range(8)]


def test_dct_decode_rejects_wrong_coefficient_count():
    with pytest.raises(ValueError, match="List length"):
        seminar.DCTEncoder().decode([0] * 63)


def test_dct_round_trip_preserves_gradient_approximately():
    block = np.arange(64).reshape(8, 8) + 96
    encoder = seminar.DCTEncoder()
    recovered = encoder.decode(encoder.encode(block, quality=90), quality=90)
    np.testing.assert_allclose(recovered, block, atol=2, rtol=0)


@pytest.mark.parametrize(
    ("samples", "runs"),
    [
        ([], []),
        ([7], [(1, 7)]),
        ([0, 0, -2, -2, -2, 0], [(2, 0), (3, -2), (1, 0)]),
    ],
)
def test_run_length_encode(samples, runs):
    assert seminar.Runlenght_encode(samples) == runs


@pytest.mark.parametrize(
    ("runs", "samples"),
    [([], []), ([(1, 7)], [7]), ([(2, 0), (3, -2), (1, 0)], [0, 0, -2, -2, -2, 0])],
)
def test_run_length_decode(runs, samples):
    assert seminar.Runlenght_decode(runs) == samples
