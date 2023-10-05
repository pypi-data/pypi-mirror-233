from __future__ import annotations as __anotations
from typing import (
    overload,
    Callable,
    Iterable,
)

import itertools

import matplotlib.pyplot as plt
import numpy as np
from sklearn import decomposition

from ..._util import Float64Array
from ..curves import TDSCurve
from ..labels import Labels
from .trajectory_plot_result import TrajectoryPlotResult


class TrajectoryPlot:
    """# `tdbear.analyzer.TrajectoryPlot`"""

    @overload
    def __init__(self, n_components: int = 2, /):
        ...

    @overload
    def __init__(self, model: decomposition.PCA, /):
        ...

    def __init__(self, arg1: int | decomposition.PCA = 2, /):
        self.model: decomposition.PCA = (
            decomposition.PCA(arg1) if isinstance(arg1, int) else arg1
        )
        self.tds_curves: tuple[TDSCurve, ...] = ()
        self.labels: Labels = Labels.get_instance([])

    def fit(
        self,
        *tds_curves: TDSCurve,
    ) -> TrajectoryPlotResult:
        result: TrajectoryPlotResult = TrajectoryPlotResult()
        result.tds_curves = tds_curves

        data: Float64Array = np.concatenate([curve.data[:-1].T for curve in tds_curves])

        scores: Float64Array = self.model.fit(data).transform(data)

        result.scores = (*map(np.transpose, np.array_split(scores, len(tds_curves))),)

        components: Float64Array = getattr(self.model, "components_")
        result.components = components
        result.variance = getattr(self.model, "explained_variance_")
        result.variance_ratio = getattr(self.model, "explained_variance_ratio_")
        result.singular_values = getattr(self.model, "singular_values_")

        def draw():
            fig = plt.figure()
            ax: plt.Axes = fig.add_subplot()

            for score in result.scores:
                ax.plot(score[0], score[1])

            [vx0, vy0] = result.scores[0][[0, 1], 0]

            m = max(
                (((score[0] - vx0) ** 2 + (score[1] - vy0) ** 2) ** 0.5).max()
                for score in result.scores
            ) / max(
                ((c[0] - vx0) ** 2 + (c[1] - vy0) ** 2) ** 0.5 for c in components.T
            )

            plt.gca().set_prop_cycle(None)

            for k, c in enumerate(components.T):
                plt.plot(
                    (
                        vx0,
                        (c[0] - vx0) * m + vx0,
                    ),
                    (
                        vy0,
                        (c[1] - vy0) * m + vy0,
                    ),
                    **{
                        "label": tds_curves[0].attr_words[k]
                        if k < len(tds_curves[0].attr_words)
                        else "delay",
                        "linestyle": "dashed" if k > 9 else "solid",
                    },
                )
            ax.legend()
            plt.show()

        return result
