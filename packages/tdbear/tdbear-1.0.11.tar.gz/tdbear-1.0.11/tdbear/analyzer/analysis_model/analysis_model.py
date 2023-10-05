from __future__ import annotations
from typing import Any

import abc

from ..analysis_result import AnalysisResult


class AnalysisModel(metaclass=abc.ABCMeta):
    """# `tdbear.analyzer.AnalysisModel`"""

    @abc.abstractmethod
    def fit(self, *args: Any, **kwargs: Any) -> AnalysisResult:
        raise NotImplementedError("fit() method not implemented")
