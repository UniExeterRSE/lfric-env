# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os
import platform
from spack import *

class LfricEnv(BundlePackage):
    """A bundle package that sets the necessary environment variables needed
    to build an LFRic application"""

    version("dev")

    depends_on("mpi")
    depends_on("hdf5+mpi")

    # NetCDF seemingly needs to be built with --enable_dap for MacOS - it is
    # recommended not to use external curl, as spack has issues finding libs
    if sys.platform == 'darwin':
        depends_on("netcdf-c+mpi+dap")
    else:
        depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran ^netcdf-c+mpi")

    depends_on("yaxt")
    depends_on("xios@2.5")
    depends_on("pfunit")
    depends_on("py-jinja2")
    depends_on("py-psyclone@2.3.1")
    depends_on("rose-picker")

    def setup_run_environment(self, env):

        env.set("FC", self.compiler.fc)
        env.set("CXX", self.compiler.cxx)
        env.set("FPP", "cpp -traditional-cpp")
        env.set("LFRIC_TARGET_PLATFORM", "meto-xc40")

        # Use compiler to link for MPI variants which dont include an MPI
        # compiler wrapper
        if self.spec['mpi'].satisfies("cray-mpich"):
            env.set("LDMPI", self.compiler.fc)
        else:
            env.set("LDMPI", self.spec['mpi'].mpifc)

        extra_ldflags = ""
        if sys.platform == 'darwin':
            if int(platform.release().split(".")[0]) >= 23:
                extra_ldflags = "-ld_classic"

        env.set("FFLAGS", f"-I{self.spec['mpi'].prefix}/lib -I{self.spec['mpi'].prefix}/include \
                            -I{self.spec['netcdf-fortran'].prefix}/include \
                            -I{self.spec['yaxt'].prefix}/include \
                            -I{self.spec['xios'].prefix}/include \
                            -I{self.spec['pfunit'].prefix}/include")

        env.set("LDFLAGS", f"-L{self.spec['mpi'].prefix}/lib \
                             -L{self.spec['hdf5'].prefix}/lib \
                             -L{self.spec['netcdf-c'].prefix}/lib \
                             -L{self.spec['netcdf-fortran'].prefix}/lib \
                             -L{self.spec['yaxt'].prefix}/lib \
                             -L{self.spec['xios'].prefix}/lib \
                             -L{self.spec['pfunit'].prefix}/lib \
                             {extra_ldflags}")

        env.set("LD_LIBRARY_PATH", f"{self.spec['mpi'].prefix}/lib:\
                                     {self.spec['hdf5'].prefix}/lib:\
                                     {self.spec['netcdf-c'].prefix}/lib:\
                                     {self.spec['netcdf-fortran'].prefix}/lib:\
                                     {self.spec['yaxt'].prefix}/lib:\
                                     {self.spec['xios'].prefix}/lib:\
                                     {self.spec['pfunit'].prefix}/lib")

        env.set("PSYCLONE_CONFIG", os.path.join(self.spec['py-psyclone'].prefix.share, "psyclone/psyclone.cfg"))

