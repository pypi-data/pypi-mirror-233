from habana_frameworks.mediapipe.media_types import dtype as dt
from habana_frameworks.mediapipe.backend.operator_specs import complex_schema
from habana_frameworks.mediapipe.operators.complex_nodes.gaussian_blur import gaussian_blur
from habana_frameworks.mediapipe.operators.complex_nodes.reduction import reduce_min, reduce_max
from habana_frameworks.mediapipe.operators.complex_nodes.complex_node_params import *

import media_pipe_params as mpp  # NOQA
import media_pipe_nodes as mpn  # NOQA


# add operators to the list of supported ops
# complex_schema.add_operator(oprator_name,guid, min_inputs,max_inputs,num_outputs,params_of_operator)

complex_schema.add_operator("GaussianBlur", "", 2, 2, gaussian_blur_in_keys, 1,
                            gaussian_blur_params, None, gaussian_blur, dt.UINT8)

complex_schema.add_operator("ReduceMin", "", 1, 2, generic_in1_key, 2,
                            reduce_params, None, reduce_min, dt.UINT8)

complex_schema.add_operator("ReduceMax", "", 1, 2, generic_in1_key, 2,
                            reduce_params, None, reduce_max, dt.UINT8)
