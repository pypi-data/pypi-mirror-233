from pathlib import Path

import matplotlib.pyplot as plt
from databroker.v2 import Broker
from pdfstream.callbacks.analysispipeline import AnalysisPipeline
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.serializationpipeline import SerializationPipeline
from pdfstream.callbacks.visualizationpipeline import VisualizationPipeline

plt.ioff()


def test_Pipelines(db_with_new_xpdacq: Broker, local_dir: Path):
    """Test if the analysis pipeline can correctly subtract dark image, average the frames to get 2D image, integrate 2D image to XRD, transform XRD to PDF and publish the manipluated document.

    Parameters
    ----------
    db_with_new_xpdacq : Broker
        The databroker that contains a temperature ramping scan.
        The detector data is `pe1_image` and the temperature is `temperature`.
    local_dir : Path
        The local directory to save the dark subtracted image plots.
    """
    db = db_with_new_xpdacq
    run = db[-1]
    config = Config()
    config.set_analysis_config(
        {"detectors": "pe1, pe2", "image_fields": "pe1_image, pe2_image"}
    )
    config.set_analysis_config(
        {
            "tiff_base": str(local_dir),
            "save_plots": True,
            "is_test": True,
            "publish": False,
        }
    )
    pipeline1 = AnalysisPipeline(config)
    pipeline2 = VisualizationPipeline(config)
    pipeline3 = SerializationPipeline(config)
    for name, doc in run.documents():
        name, doc = pipeline1(name, doc)
        pipeline2(name, doc)
        pipeline3(name, doc)
    return


def test_use_mask(db_with_mask_in_run: Broker, local_dir: Path):
    """Test if the mask settings can be changed for a run.

    Parameters
    ----------
    db_with_new_xpdacq : Broker
        The databroker that contains a temperature ramping scan.
        The detector data is `pe1_image` and the temperature is `temperature`.
    local_dir : Path
        The local directory to save the dark subtracted image plots.
    """
    db = db_with_mask_in_run
    run = db[-1]
    config = Config()
    config.set_analysis_config(
        {"detectors": "pe1, pe2", "image_fields": "pe1_image, pe2_image"}
    )
    config.set_analysis_config({"auto_mask": False})
    config.set_analysis_config(
        {
            "tiff_base": str(local_dir),
            "save_plots": True,
            "is_test": True,
            "publish": False,
        }
    )
    pipeline1 = AnalysisPipeline(config)
    pipeline2 = VisualizationPipeline(config)
    pipeline3 = SerializationPipeline(config)
    for name, doc in run.documents():
        name, doc = pipeline1(name, doc)
        pipeline2(name, doc)
        pipeline3(name, doc)
    return


def test_Calibration(db_with_new_calib: Broker, local_dir: Path):
    db = db_with_new_calib
    run = db[-1]
    config = Config()
    config.set_analysis_config({"detectors": "pe1", "image_fields": "pe1_image"})
    config.set_analysis_config(
        {
            "tiff_base": str(local_dir),
            "save_plots": True,
            "is_test": True,
            "publish": False,
        }
    )
    pipeline1 = AnalysisPipeline(config)
    pipeline2 = VisualizationPipeline(config)
    pipeline3 = SerializationPipeline(config)
    for name, doc in run.documents():
        name, doc = pipeline1(name, doc)
        pipeline2(name, doc)
        pipeline3(name, doc)
    return
