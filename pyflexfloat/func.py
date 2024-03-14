#!/usr/bin/env python3
# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>
from pyflexfloat import FlexFloat
import numpy as np


def array(a, desc):
    shape = a.shape
    a = [FlexFloat(desc, val) for val in a.flatten().tolist()]
    return np.array(a).reshape(shape)


def frombuffer(buffer, desc):
    """Return a FlexFloat array from a Python buffer object."""
    size = FlexFloat(desc).size()
    assert size == 8, "frombuffer method currently supports only 8-bit sized FlexFloat types"
    # Cast to a buffer with byte-sized elements
    memview = memoryview(buffer).cast('B')
    return np.array([FlexFloat(desc, byte.to_bytes(1, "big")) for byte in memview])


# TODO: is this needed or not? Looks redundant to FlexFloat.__iadd__ to me
def acc(a, b):
    # void ff_acc(flexfloat_t *dest, const flexfloat_t *a);
    pass


def min(a, b):
    # TODO: what precision should we use for result?
    result = FlexFloat(a.desc)
    lib.ff_min(result.ptr, a.ptr, b.ptr)
    return result


def max(a, b):
    # TODO: what precision should we use for result?
    result = FlexFloat(a.desc)
    lib.ff_max(result.ptr, a.ptr, b.ptr)
    return result


def fma(a, b, c):
    # TODO: what precision should we use for result?
    result = FlexFloat(a.desc)
    lib.ff_fma(result.ptr, a.ptr, b.ptr, c.ptr)
    return result