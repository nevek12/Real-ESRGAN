import numpy as np
import os
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
def process_image_with_esrgan(original_image):
    img = np.array(original_image)
    MODEL_NAME = 'net_g_85000'

    model_path = os.path.join('weights', MODEL_NAME + '.pth')
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    upsampler = RealESRGANer(
        scale=4,
        model_path=model_path,
        dni_weight=None,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        gpu_id=None)
    outscale = 4
    try:
        output, _ = upsampler.enhance(img, outscale=outscale)
    except RuntimeError as error:
        print('Error', error)
        print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')
    except Exception as e:
        print(e)
    return output



