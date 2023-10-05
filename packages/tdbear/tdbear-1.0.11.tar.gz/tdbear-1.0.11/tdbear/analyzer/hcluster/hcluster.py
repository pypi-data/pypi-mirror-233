from __future__ import annotations
from typing import (
    Iterator,
    Iterable,
    Self,
    Any,
)

import itertools
import functools
import warnings

import matplotlib.pyplot as plt
import matplotlib.figure as figure
import numpy as np

from ..._util import Float64Array
from ..labels import Labels
from ..analysis_model import AnalysisModel


class HCluster(AnalysisModel):
    pass
