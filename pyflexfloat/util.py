#!/usr/bin/env python3
# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>

def max_precision(a, b):
    '''Calculates the maximum precision between two FlexFloat types.

    Returns:
        A FlexFloat descriptor able to represent both FlexFloat variables
        `a` and `b`.
    '''
    return (max(a.exp_bits, b.exp_bits), max(a.frac_bits, b.frac_bits))
