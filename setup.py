# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>
import setuptools
import cmake_build_extension
import subprocess
from pathlib import Path


class CMakeBuild(setuptools.command.build.build):

	def run(self):
		# Required to generate "flexfloat_config.h"
		builddir = Path(__file__).parent / 'flexfloat/build'
		builddir.mkdir(parents=True, exist_ok=True)
		subprocess.run(['pwd'], cwd=builddir, check=True)
		subprocess.run(['ls', '..'], cwd=builddir, check=True)
		subprocess.run(['cmake', '..'], cwd=builddir, check=True)


setuptools.setup(
	packages=setuptools.find_packages(),
	setup_requires=['cffi'],
	install_requires=['cffi'],
	cffi_modules=["pyflexfloat/build_flexfloat_ffi.py:ffibuilder"],
	cmdclass={'build': CMakeBuild}
)
