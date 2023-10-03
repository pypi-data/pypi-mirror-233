import numpy as np
from habana_frameworks.mediapipe.backend.nodes import opnode_tensor_info
from habana_frameworks.mediapipe.operators.media_nodes import MediaCPUNode
from habana_frameworks.mediapipe.media_types import dtype as dt


class gather_video_indices(MediaCPUNode):
    """
    Class to generate gather indices (to be used by fn.GatherND) for video decode.

    """

    def __init__(self, name, guid, device, inputs, params, cparams, node_attr):
        """
        Constructor method.

        :params name: node name.
        :params guid: guid of node.
        :params device: device on which this node should execute.
        :params params: node specific params.
        :params cparams: backend params.
        :params node_attr: node output information
        """
        super().__init__(
            name, None, device, inputs, params, cparams, node_attr)
        self.max_frame_vid = params['max_frame_per_clip']
        self.frame_per_clip = params['frames_per_clip']
        print("gather_video_indices frames_per_clip {} max_frame_per_clip {}".format(
            self.frame_per_clip, self.max_frame_vid))

    def set_params(self, params):
        """
        Setter method to set mediapipe specific params.

        :params params: mediapipe params of type "opnode_params".
        """
        self.batch_size = params.batch_size

    def gen_output_info(self):
        """
        Method to generate output type information.

        :returns : output tensor information of type "opnode_tensor_info".
        """
        self.gather_shape = [1, self.frame_per_clip * self.batch_size]
        self.gather_shape_np = self.gather_shape[::-1]
        self.gather_dtype = dt.INT32
        out_info = []
        o = opnode_tensor_info(self.gather_dtype, np.array(
            self.gather_shape, dtype=np.uint32), "")
        out_info.append(o)
        return out_info

    def __call__(self, resample_idx):
        """
        Callable class method.

        :params resample_idx: frame index to be used for each video
        """
        op_gather_index = np.zeros(
            shape=self.gather_shape_np, dtype=self.gather_dtype)

        # assert resample_idx.shape == (self.batch_size, self.frame_per_clip), "invalid resample_idx"

        idx = 0
        for i in range(self.batch_size):
            base = (i * self.max_frame_vid)
            for j in range(len(resample_idx[i])):
                op_gather_index[idx][0] = base + \
                    (resample_idx[i][j] - resample_idx[i][0])
                idx += 1

        return op_gather_index
