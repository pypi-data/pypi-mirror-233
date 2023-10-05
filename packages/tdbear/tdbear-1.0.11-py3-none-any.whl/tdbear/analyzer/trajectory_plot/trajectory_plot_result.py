from __future__ import annotations
from typing import Any

import matplotlib.figure as figure
import matplotlib.pyplot as plt

from ..._util import Float64Array
from ..analysis_result import AnalysisResult
from ..curves import TDSCurve
from ..labels import Labels


class TrajectoryPlotResult(AnalysisResult):

    tds_curves: tuple[TDSCurve]
    scores: tuple[Float64Array]
