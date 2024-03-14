#!/usr/bin/env python3
# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>
from cffi import FFI
ffibuilder = FFI()

# Assumes FLEXFLOAT_ON_DOUBLE configuration
ffibuilder.cdef("""
typedef double fp_t;
typedef uint64_t uint_t;

typedef struct _flexfloat_desc_t {
    uint8_t exp_bits;
    uint8_t frac_bits;
} flexfloat_desc_t;

struct _flexfloat_t {
    fp_t value;
    flexfloat_desc_t desc;
};

typedef struct _flexfloat_t flexfloat_t;

// Helper functions

int_fast16_t flexfloat_exp(const flexfloat_t *a);
uint_t flexfloat_frac(const flexfloat_t *a);

// Bit-level access

uint_t flexfloat_get_bits(flexfloat_t *a);
void flexfloat_set_bits(flexfloat_t *a, uint_t bits);

// Constructors

void ff_init(flexfloat_t *obj, flexfloat_desc_t desc);
void ff_init_double(flexfloat_t *obj, double value, flexfloat_desc_t desc);

// Casts

double ff_get_double(const flexfloat_t *obj);

// Artihmetic operators

void ff_add_any(flexfloat_t *dest, const flexfloat_t *a, const flexfloat_t *b);
void ff_sub_any(flexfloat_t *dest, const flexfloat_t *a, const flexfloat_t *b);
void ff_mul_any(flexfloat_t *dest, const flexfloat_t *a, const flexfloat_t *b);
void ff_div_any(flexfloat_t *dest, const flexfloat_t *a, const flexfloat_t *b);
void ff_sqrt(flexfloat_t *dest, const flexfloat_t *a);
void ff_acc(flexfloat_t *dest, const flexfloat_t *a);
void ff_min(flexfloat_t *dest, const flexfloat_t *a, const flexfloat_t *b);
void ff_max(flexfloat_t *dest, const flexfloat_t *a, const flexfloat_t *b);
void ff_fma(flexfloat_t *dest, const flexfloat_t *a, const flexfloat_t *b, const flexfloat_t *c);

// Relational operators

bool ff_eq(const flexfloat_t *a, const flexfloat_t *b);
bool ff_neq(const flexfloat_t *a, const flexfloat_t *b);
bool ff_le(const flexfloat_t *a, const flexfloat_t *b);
bool ff_lt(const flexfloat_t *a, const flexfloat_t *b);
bool ff_ge(const flexfloat_t *a, const flexfloat_t *b);
bool ff_gt(const flexfloat_t *a, const flexfloat_t *b);
""")

ffibuilder.set_source("_flexfloat",
"""
    #include "flexfloat.h"
""",
    sources=['flexfloat/src/flexfloat.c'],
    include_dirs=['flexfloat/include'],
    # extra_compile_args=['--std=c++11']
    # libraries=['m']
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
