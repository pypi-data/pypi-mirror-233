from habana_frameworks.mediapipe.backend.nodes import opnode_tensor_info
from habana_frameworks.mediapipe.operators.media_nodes import MediaComplexNode
from habana_frameworks.mediapipe.operators.media_nodes import media_layout
from habana_frameworks.mediapipe.media_types import dtype as dt
from habana_frameworks.mediapipe.media_types import ftype as ft
from habana_frameworks.mediapipe.media_types import decoderType as dect
from habana_frameworks.mediapipe import fn  # NOQA
import numpy as np
import math as pmath


class reduce_min(MediaComplexNode):
    """
    Class defining media decoder node.

    """

    def __init__(self, name, device, params, node_attr):
        """
        Constructor method.

        :params params: node specific params.
        :params node_attr: node output information
        """
        if(device == "cpu"):
            raise ValueError("CPU reduction op not supported")
        super().__init__(name, device, node_attr)
        dtype = node_attr[0]["outputType"]
        reductionDimension = params['reductionDimension']
        self.minOps = []
        for r in reductionDimension:
            self.minOps.append(fn._ReduceMin_(
                reductionDimension=r, dtype=dtype))

    def __call__(self, images):
        """
        Callable class method.

        """
        img = images
        for m in self.minOps:
            img, idx = m(img)
        return img, idx


class reduce_max(MediaComplexNode):
    """
    Class defining media decoder node.

    """

    def __init__(self, name, device, params, node_attr):
        """
        Constructor method.

        :params params: node specific params.
        :params node_attr: node output information
        """
        if(device == "cpu"):
            raise ValueError("CPU reduction op not supported")
        super().__init__(name, device, node_attr)
        dtype = node_attr[0]["outputType"]
        reductionDimension = params['reductionDimension']
        self.maxOps = []
        for r in reductionDimension:
            self.maxOps.append(fn._ReduceMax_(reductionDimension=r, dtype=dtype))

    def __call__(self, images):
        """
        Callable class method.

        """
        img = images
        for m in self.maxOps:
            img, idx = m(img)
        return img, idx
