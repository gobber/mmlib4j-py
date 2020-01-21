import numpy as np
from jnius import autoclass
from .utils import *

AbstractNdArray = autoclass('ndarrays4j.arrays.AbstractNdArray')
ByteImageUnsafe = autoclass('mmlib4j.images.impl.ByteImageUnsafe')
ShortImageUnsafe = autoclass('mmlib4j.images.impl.ShortImageUnsafe')

numpy_dtype_to_conversion_method = {
    np.dtype('uint8'): ByteImageUnsafe,
    np.dtype('uint16'): ShortImageUnsafe
}


def to_mmlib4j(np_img):
    if not np_img.dtype in numpy_dtype_to_conversion_method:
        raise NotImplementedError("Can not convert dtype to mmlib4j type yet: {}".format(np_img.dtype))
    elif len(np_img.shape) != 2:
        raise NotImplementedError("Can only convert from 2D arrays, use reshape if it is a 1D array")
    else:
        if np_img.flags['CARRAY']:
            return numpy_dtype_to_conversion_method[np_img.dtype](get_address(np_img),np_img.shape[0],np_img.shape[1],AbstractNdArray.ORDER_C)
        else:
            return numpy_dtype_to_conversion_method[np_img.dtype](get_address(np_img),np_img.shape[0],np_img.shape[1],AbstractNdArray.ORDER_F)

