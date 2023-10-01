from __future__ import annotations

from pathlib import Path

from holoviews import Curve
from pytest import mark

from utilities.holoviews import apply_opts, relabel_plot, save_plot
from utilities.platform import SYSTEM, System


class TestApplyOpts:
    def test_main(self) -> None:
        curve = Curve([])
        _ = apply_opts(curve)


class TestRelabelPlot:
    def test_main(self) -> None:
        curve = Curve([])
        assert not curve.label
        curve = relabel_plot(curve, "label")
        assert curve.label == "label"


class TestSavePlot:
    @mark.skipif(SYSTEM is not System.linux, reason="Linux only")
    def test_main(self, tmp_path: Path) -> None:
        curve = Curve([])
        save_plot(curve, tmp_path.joinpath("plot.png"))
