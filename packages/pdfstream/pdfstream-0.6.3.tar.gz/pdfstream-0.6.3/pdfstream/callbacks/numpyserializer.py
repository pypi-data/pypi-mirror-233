import typing as T
from pathlib import Path

import event_model
import numpy as np
import pdfstream.io as io

from .serializerbase import SerializerBase


class NumpySerializer(SerializerBase):
    def __init__(
        self,
        base: str,
        fields: T.List[str],
        stream_name: str = "primary",
        folder: str = "mask",
    ) -> None:
        super().__init__(base, folder)
        self._fields = fields
        self._stream_name = stream_name
        self._descriptor = ""

    def _get_filepath(self, filename: str, field: str) -> Path:
        f = filename + "_" + field
        filepath = self._directory.joinpath(f).with_suffix(".npy")
        return filepath

    def _export(self, doc: dict, field: str) -> None:
        if field in doc["data"]:
            f = self._get_filepath(doc["data"]["filename"], field)
            a = doc["data"][field]
            np.save(f, a)
            io.server_message("Save '{}' in '{}'".format(field, f.name))
        else:
            io.server_message("Missing '{}' in data.".format(field))
        return

    def descriptor(self, doc):
        if doc["name"] == self._stream_name:
            self._descriptor = doc["uid"]
        return doc

    def event(self, doc):
        if doc["descriptor"] == self._descriptor:
            for field in self._fields:
                if field in doc["data"]:
                    self._export(doc, field)
        return doc

    def event_page(self, doc):
        for event in event_model.unpack_event_page(doc):
            self.event(event)
        return doc
