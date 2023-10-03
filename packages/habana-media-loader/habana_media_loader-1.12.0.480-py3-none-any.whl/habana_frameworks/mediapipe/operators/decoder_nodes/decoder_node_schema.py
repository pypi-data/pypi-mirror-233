from habana_frameworks.mediapipe.media_types import dtype as dt
from habana_frameworks.mediapipe.backend.operator_specs import schema
from habana_frameworks.mediapipe.operators.decoder_nodes.decoder_nodes import image_decoder
from habana_frameworks.mediapipe.operators.decoder_nodes.decoder_nodes import video_decoder
from habana_frameworks.mediapipe.operators.decoder_nodes.decoder_node_params import *

import media_pipe_params as mpp  # NOQA
import media_pipe_nodes as mpn  # NOQA


# add operators to the list of supported ops
# schema.add_operator(oprator_name,guid, min_inputs,max_inputs,num_outputs,params_of_operator)

schema.add_operator("ImageDecoder", "image_decoder", 1, 2, image_decoder_in_keys, 1,
                    image_decoder_params, mpn.ImageDecoderParams_t, image_decoder, dt.UINT8)

schema.add_operator("VideoDecoder", None, 2, 3, video_decoder_in_keys, 1,
                    video_decoder_params, None, video_decoder, dt.UINT8)
