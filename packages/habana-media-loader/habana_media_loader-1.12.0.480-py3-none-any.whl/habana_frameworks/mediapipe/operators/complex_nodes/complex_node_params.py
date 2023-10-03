from habana_frameworks.mediapipe.media_types import ftype as ft
from habana_frameworks.mediapipe.media_types import randomCropType as rct
from habana_frameworks.mediapipe.media_types import decoderStage as ds

# INFO: Here we will give params and its default arguments order doesnt matter
# INFO: if any parameter is not set here it will be set to zero
generic_in1_key = ["input"]
gaussian_blur_in_keys = ["images", "sigma"]

gaussian_blur_params = {
    'max_sigma': 0,
    'min_sigma': 0,
    'shape': [1, 1, 1, 1, 1],  # [W,H,D,C,N]
}


reduce_params = {
    "reductionDimension": [0]
}
