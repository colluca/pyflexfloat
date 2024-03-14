#!/usr/bin/env python3
# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>
import pyflexfloat as ff
from pyflexfloat import FlexFloat
import numpy as np

np.set_printoptions(formatter={'object': str})

if __name__ == '__main__':
    # FP16 math
    print('= FP16 math =')
    a = FlexFloat('fp16', 3.14)
    b = FlexFloat('fp16', 2)
    c = FlexFloat('fp16')
    print(a)
    print(b)
    print(a + b)
    a += b
    print(a)

    # FP32 math
    print('= FP32 math =')
    a = FlexFloat('fp32', 3.14)
    b = FlexFloat('fp32', 2)
    c = FlexFloat('fp32')
    print(a)
    print(b)
    print(a + b)
    a += b
    print(a)

    # FP16 math with numpy
    print('= FP16 math with numpy =')
    length = 4
    A = np.array([FlexFloat((5, 10), i + .14) for i in range(length*length)]).reshape(length, length)
    B = np.array([[FlexFloat((5, 10), 2)]*length]*length)
    C = A + B
    print(A)
    print(B)
    C = np.matmul(A, B)
    print(C)

    # Random numpy data
    print('= Random FP8 array with numpy =')
    A = np.random.rand(length, length)
    B = ff.array(A, 'e5m2')
    print(A, B)

    # Test implicit type casting
    print('= RHS type casting =')
    a = FlexFloat('fp32', 3.14)
    print(a * 2)
    print('= LHS type casting =')
    a = FlexFloat('fp32', 3.14)
    print(2 * a)

    # Test exp and frac functions
    print('= exp() and frac() =')
    a = FlexFloat('e5m2', 3.14)
    print(a)
    print(f'exp: {a.exp()}')
    print(f'frac: {a.frac()}')
    print(f'bits: {a.bitstring()}')
    print(f'hex: {hex(a.bits())}')

    # Test FlexFloat initialization from bytes
    print('= FlexFloat(..., bytes) =')
    b = FlexFloat('e5m2', a.bits().to_bytes(1, 'big'))
    print(f'bits: {b.bitstring()}')
    print(f'hex: {hex(b.bits())}')

    # Test comparisons
    print('= Comparisons =')
    a = FlexFloat('fp32', -3.14)
    b = FlexFloat('fp32', 3.14)
    print(f'{a} < 0: {a < 0}')
    print(f'{b} < 0: {b < 0}')

    # Neg and abs test
    print('= Neg and abs =')
    a = FlexFloat('fp32', -3.14)
    print(f'a: {a}')
    print(f'-a: {-a}')
    print(f'abs(a): {abs(a)}')
