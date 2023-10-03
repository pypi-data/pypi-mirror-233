from habana_frameworks.mediapipe.backend.nodes import opnode_tensor_info
from habana_frameworks.mediapipe.operators.media_nodes import MediaHPUNode
from habana_frameworks.mediapipe.backend.utils import get_str_dtype
import numpy as np


class media_hpu_ops(MediaHPUNode):
    """
    Class representing media hpu node.

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
        self.batch_size = 1
        self.params = params
        self.out_tensor_info = []
        for i in range(len(node_attr)):
            dtype = get_str_dtype(node_attr[i]['outputType'])
            o = opnode_tensor_info(
                dtype, np.array([0], dtype=np.uint32), "")
            self.out_tensor_info.append(o)

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
        return self.out_tensor_info


class media_hpu_user_ops(MediaHPUNode):
    """
    Class representing media hpu node.

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
        self.batch_size = 1
        self.params = params
        self.cparams = cparams
        self.out_tensor_info = []
        self.syn_params = None
        for i in range(len(node_attr)):
            dtype = get_str_dtype(node_attr[i]['outputType'])
            o = opnode_tensor_info(
                dtype, np.array([0], dtype=np.uint32), "")
            self.out_tensor_info.append(o)

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
        return self.out_tensor_info
