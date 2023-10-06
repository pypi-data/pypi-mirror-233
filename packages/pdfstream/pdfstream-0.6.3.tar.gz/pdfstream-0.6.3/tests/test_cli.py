from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np
import pytest

import pdfstream.cli as cli
import pdfstream.io as io


@pytest.mark.parametrize(
    "bg_img_file, mask_file, kwargs",
    [
        (None, None, {}),
        ("Ni_img_file", "mask_file", {}),
        (None, None, {"parallel": True, "plot_setting": "OFF", "img_setting": "OFF"}),
    ],
)
def test_integrate(test_data, bg_img_file, mask_file, kwargs):
    with TemporaryDirectory() as tempdir:
        img_file = Path(test_data["Ni_img_file"])
        chi_file = Path(tempdir).joinpath(img_file.with_suffix(".chi").name)
        cli.integrate(
            test_data["Ni_poni_file"],
            str(img_file),
            bg_img_file=test_data.get(bg_img_file, None),
            mask_file=test_data.get(mask_file, None),
            output_dir=tempdir,
            **kwargs,
            test=True
        )
        assert chi_file.exists()
    plt.close()


@pytest.mark.parametrize("kwargs", [{}, {"weights": [1, 1]}])
def test_average(test_data, kwargs):
    with TemporaryDirectory() as tempdir:
        img_file = Path(tempdir).joinpath("new_dir/average.tiff")
        cli.average(
            img_file, test_data["white_img_file"], test_data["white_img_file"], **kwargs
        )
        avg_img = io.load_img(img_file)
        white_img = io.load_img(test_data["white_img_file"])
        assert np.array_equal(avg_img, white_img)


@pytest.mark.parametrize(
    "keys,kwargs",
    [
        (["Ni_gr_file", "Ni_gr_file"], {"mode": "line", "legends": ["Ni0", "Ni1"]}),
        (["Ni_gr_file", "Ni_gr_file"], {"mode": "line", "stack": False}),
        (
            ["Ni_gr_file", "Ni_gr_file"],
            {"mode": "line", "xy_kwargs": {"color": "black"}, "texts": ["Ni0", "Ni1"]},
        ),
        (
            ["Ni_gr_file", "Ni_gr_file"],
            {"mode": "line", "colors": ["r", "b"], "texts": ["Ni0", "Ni1"]},
        ),
        (["Ni_fgr_file", "Ni_fgr_file"], {"mode": "fit", "texts": ["Ni0", "Ni1"]}),
        (["Ni_fgr_file", "Ni_fgr_file"], {"mode": "fit", "stack": False}),
        (
            ["Ni_fgr_file", "Ni_fgr_file"],
            {"mode": "fit", "xy_kwargs": {"color": "black"}},
        ),
    ],
)
def test_waterfall(test_data, keys, kwargs):
    data_files = (test_data[key] for key in keys)
    cli.waterfall(*data_files, **kwargs, show_fig=False)
    plt.close()


def test_waterfall_exception():
    with pytest.raises(ValueError):
        cli.waterfall(*tuple())
        plt.close()


@pytest.mark.parametrize(
    "key,kwargs",
    [
        ("Ni_gr_file", {"mode": "line", "text": "Ni", "xy_kwargs": {"color": "black"}}),
        (
            "Ni_gr_file",
            {"mode": "line", "legends": "Ni", "xy_kwargs": {"color": "black"}},
        ),
        ("Ni_fgr_file", {"mode": "fit", "text": "Ni", "xy_kwargs": {"color": "black"}}),
    ],
)
def test_visualize(test_data, key, kwargs):
    cli.visualize(test_data[key], **kwargs, show_fig=False)
    plt.close()
