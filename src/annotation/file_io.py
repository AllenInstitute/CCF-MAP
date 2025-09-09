# Utilities for reading and writing nifti image volumes

import SimpleITK as sitk
import numpy as np
from typing import List

def sitk_to_npy(image):
    
    permuted_image = sitk.PermuteAxes(image,[2,1,0])

    return sitk.GetArrayFromImage(permuted_image)

def npy_to_sitk(image_npy):
    
    image = sitk.GetImageFromArray(image_npy)
    
    return sitk.PermuteAxes(image,[2,1,0])

def write_volume_to_file(volume: np.ndarray,
                         output_filename: str):
    
    img = npy_to_sitk(volume)
    sitk.WriteImage(img, output_filename)

def read_image(image_volume_filename: str):

    img = sitk.ReadImage(image_volume_filename)
    return sitk_to_npy(img)
