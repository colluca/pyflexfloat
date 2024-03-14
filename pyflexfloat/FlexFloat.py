#!/usr/bin/env python3
# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>
from _flexfloat import ffi, lib
from pyflexfloat.util import max_precision
from collections.abc import Sequence, Mapping
import re


class FlexFloat():

    def __init__(self, desc, val=None):
        ''' Initialize a FlexFloat variable.
        
        Arguments:
            desc: A descriptor specifying the precision of the flexfloat
                type, as defined by the flexfloat library. Can be a
                `Sequence` type instance, a `Mapping` type instance with
                the 'exp_bits' and 'frac_bits' keys, a string of the form
                'fpXX' indicating a standardized IEEE floating-point type
                of XX bits (e.g. fp16), or a string of the form 'eXmY' to
                indicate a custom type with X exponent bits and Y mantissa
                bits.
            val: A variable of type float, integer or bytes used to
                derive the flexfloat value.  The pyflexfloat API only
                implements a subset of the flexfloat API, and allows
                initializing flexfloat values from doubles only. Integers
                are implicitly cast to double before eventually being
                downcasted to the same precision as `self`. A variable of
                type bytes can be passed to initialize the flexfloat
                variable to the exact binary representation provided.
        '''
        # Parse desc argument
        self.desc = desc
        if isinstance(desc, str):
            # Standard IEEE FP formats
            if desc == 'fp16':
                self.exp_bits, self.frac_bits = 5, 10
            elif desc == 'fp32':
                self.exp_bits, self.frac_bits = 8, 23
            elif desc == 'fp64':
                self.exp_bits, self.frac_bits = 11, 52
            # Custom FP formats
            else:
                # This regex pattern matches a string that:
                # - starts with "e"
                # - is followed by one or more digits (\d+)
                # - has "m" right after the digits
                # - ends with one or more digits (\d+)
                match = re.match(r'^e(\d+)m(\d+)$', desc)
                if match:
                    # Extracting N and M from the capturing groups
                    self.exp_bits, self.frac_bits = map(int, match.groups())
                else:
                    raise ValueError('Unsupported description string')
        elif isinstance(desc, Sequence):
            self.exp_bits, self.frac_bits = desc[0:2]
        elif isinstance(desc, Mapping):
            self.exp_bits, self.frac_bits = desc['exp_bits'], desc['frac_bits']
        else:
            raise ValueError('Unsupported type for parameter desc')

        # Create and initialize flexfloat variable
        self.ptr = ffi.new('flexfloat_t *')
        desc = ffi.new('flexfloat_desc_t *', [self.exp_bits, self.frac_bits])
        if val is not None:
            if isinstance(val, float):
                lib.ff_init_double(self.ptr, val, desc[0])
            elif isinstance(val, int):
                lib.ff_init_double(self.ptr, float(val), desc[0])
            elif isinstance(val, bytes):
                lib.ff_init(self.ptr, desc[0])
                lib.flexfloat_set_bits(self.ptr, int.from_bytes(val, 'big'))
            else:
                raise ValueError(f'val has unsupported type {type(val)}')
        else:
            lib.ff_init(self.ptr, desc[0])

    def __str__(self):
        return str(lib.ff_get_double(self.ptr))

    def _uniformize(self, other):
        """Ensures that `self` and `other` have compatible types.

        Ensures that `self` and `other` have compatible types, i.e.
        can be used as the two operands of a binary operation.

        Operations between FlexFloats (of any type) are already allowed.
        This method casts `other` to the FlexFloat type of `self` iff it
        is not already a FlexFloat. See the `__init__` method for more
        information.
        """
        if not isinstance(other, FlexFloat):
            return FlexFloat(self.desc, other)
        else:
            return other


    def __add__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_add_any(result.ptr, self.ptr, other.ptr)
        return result

    def __radd__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_add_any(result.ptr, other.ptr, self.ptr)
        return result

    def __iadd__(self, other):
        lib.ff_add_any(self.ptr, self.ptr, other.ptr)
        return self

    def __sub__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_sub_any(result.ptr, self.ptr, other.ptr)
        return result

    def __rsub__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_sub_any(result.ptr, other.ptr, self.ptr)
        return result

    def __isub__(self, other):
        lib.ff_sub_any(self.ptr, self.ptr, other.ptr)
        return self

    def __mul__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_mul_any(result.ptr, self.ptr, other.ptr)
        return result

    def __rmul__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_mul_any(result.ptr, other.ptr, self.ptr)
        return result

    def __imul__(self, other):
        lib.ff_mul_any(self.ptr, self.ptr, other.ptr)
        return self

    def __truediv__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_div_any(result.ptr, self.ptr, other.ptr)
        return result

    def __rtruediv__(self, other):
        other = self._uniformize(other)
        result = FlexFloat(max_precision(self, other))
        lib.ff_div_any(result.ptr, other.ptr, self.ptr)
        return result

    def __itruediv__(self, other):
        lib.ff_div_any(self.ptr, self.ptr, other.ptr)
        return self

    def __lt__(self, other):
        other = self._uniformize(other)
        return lib.ff_lt(self.ptr, other.ptr)

    def __le__(self, other):
        other = self._uniformize(other)
        return lib.ff_le(self.ptr, other.ptr)

    def __eq__(self, other):
        other = self._uniformize(other)
        return lib.ff_eq(self.ptr, other.ptr)

    def __ne__(self, other):
        other = self._uniformize(other)
        return lib.ff_neq(self.ptr, other.ptr)

    def __ge__(self, other):
        other = self._uniformize(other)
        return lib.ff_ge(self.ptr, other.ptr)

    def __gt__(self, other):
        other = self._uniformize(other)
        return lib.ff_gt(self.ptr, other.ptr)

    def __neg__(self):
        return 0 - self

    def __abs__(self):
        return -self if self < 0 else self

    def sqrt(self):
        result = FlexFloat(self.desc)
        lib.ff_sqrt(result.ptr, self.ptr)
        return result

    def size(self):
        return self.exp_bits + self.frac_bits + 1

    def exp(self):
        return lib.flexfloat_exp(self.ptr)

    def frac(self):
        return lib.flexfloat_frac(self.ptr)

    def bits(self):
        return lib.flexfloat_get_bits(self.ptr)

    def bitstring(self):
        return format(self.bits(), f'0>{self.size()}b')
