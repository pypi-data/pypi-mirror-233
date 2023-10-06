import typing as T

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pdfstream.io as io
from xray_vision.backend.mpl.cross_section_2d import CrossSection

from .plotterbase import PlotterBase


class ImagePlotter(PlotterBase):
    """Live image show of a image with a mask."""

    def __init__(
        self,
        bases: T.List[Path],
        image_field: str,
        mask_field: str = None,
        *,
        cmap: str = "viridis",
        norm: T.Callable = None,
        limit_func: T.Callable = None,
        auto_redraw: bool = True,
        interpolation: str = None,
        window_title: str = None,
        name: str = "image",
        save: bool = False,
        suffix: str = ".png"
    ):
        fig = plt.figure()
        self.image_field = image_field
        self.mask_field = mask_field
        self._filename = ""
        self._directory = None
        self._cs = CrossSection(fig, cmap, norm, limit_func, auto_redraw, interpolation)
        if window_title:
            self._cs._fig.canvas.set_window_title(window_title)
        super().__init__(bases, name, fig, save_at_event=save, suffix=suffix)

    def update(self, data: np.ndarray) -> None:
        self._cs.update_image(data)
        return

    def plot_event(self, doc):
        if self.image_field not in doc["data"]:
            io.server_message("No '{}' in data.".format(self.image_field))
            return
        mask = doc["data"][self.mask_field] if self.mask_field in doc["data"] else None
        image = doc["data"][self.image_field]
        data_arr = np.ma.masked_array(image, mask)
        self.update(data_arr)
        self._updated = True
        return
