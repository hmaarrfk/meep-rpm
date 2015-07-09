
Unofficial Fedora .spec files for packaging MEEP and related software.

MPB:
requires HDF5

MEEP:
requires MPB and HDF5

fftw2-mpi libraries are available:
https://copr.fedoraproject.org/coprs/hmaarrfk/fftw2-mpi/

I am testing this as I am using MEEP and MPB, so there are no guarantees

Repository can be found here:
https://copr.fedoraproject.org/coprs/hmaarrfk/meep/

I stopped building the 32bit packages because I figure you will be running this on a half modern computer which will be running 64 bit. The builds take a bit of time on COPR and when they fail, it forces me to wait even longer. I'll build the 32bit packages on request.
