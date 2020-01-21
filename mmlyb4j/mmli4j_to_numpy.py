import numpy as np
import ctypes
from jnius import autoclass

AbstractNdArray = autoclass('ndarrays4j.arrays.AbstractNdArray')
ByteImageUnsafe = autoclass('mmlib4j.images.impl.ByteImageUnsafe')
ShortImageUnsafe = autoclass('mmlib4j.images.impl.ShortImageUnsafe')

dtype_selector = {
    "ByteImage": np.dtype('uint8'),
    "ShortImage": np.dtype('uint16')
}

ctype_conversions_mmlib4j = {
    "ByteImage": ctypes.c_uint8,
    "ShortImage": ctypes.c_uint16
}


def to_numpy_img(mmlib4j_img):
    address = mmlib4j_img.getAddress()
    pointer = ctypes.cast(address, ctypes.POINTER(ctype_conversions_mmlib4j[mmlib4j_img.getType()]))
    shape = tuple(mmlib4j_img.getShape())
    dtype = dtype_selector[mmlib4j_img.getType()]
    order = 'C' if mmlib4j_img.getOrder() == AbstractNdArray.ORDER_C else 'F'
    return np.ndarray(shape=shape, dtype=dtype, buffer=np.ctypeslib.as_array(pointer, shape=shape), order=order)
