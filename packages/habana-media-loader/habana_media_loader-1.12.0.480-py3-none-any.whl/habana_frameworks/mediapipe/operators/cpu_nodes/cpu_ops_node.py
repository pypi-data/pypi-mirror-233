from habana_frameworks.mediapipe.operators.media_nodes import MediaCPUNode
from habana_frameworks.mediapipe.backend.utils import get_numpy_dtype
from habana_frameworks.mediapipe.backend.utils import get_media_dtype
import numpy as np


class cpu_ops_node(MediaCPUNode):
    """
    Class representing media random biased crop cpu node.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        super().__init__(
            name, guid, device, inputs, params, cparams, node_attr)

    def set_params(self, params):
        """
        Setter method to set mediapipe specific params.

        :params params: mediapipe params of type "opnode_params".
        """
        pass

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """
        pass

    def __call__(self):
        """
        Callable class method.

        :params img: image data
        :params lbl: label data
        """
        pass


class cpu_media_const_node(cpu_ops_node):
    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params guid: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        if not isinstance(params["data"], np.ndarray):
            raise ValueError(
                "constant kernel data must be of type numpy array")
        dtype = get_numpy_dtype(node_attr[0]['outputType'])
        if(dtype != params["data"].dtype):
            raise ValueError("dtype mismatch for media const node")
        params["dtype"] = get_media_dtype(node_attr[0]['outputType'])
        super().__init__(
            name, guid, device, inputs, params, cparams, node_attr)
