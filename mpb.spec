Name:       mpb
Version:    1.5.1
Release:    9%{?dist}
Summary:    Unofficial MPB RPM package

%global commit 69b17e86a56f08d5a06cd15a7fbe12dad7e4458c

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/wiki/index.php/MIT_Photonic_Bands
# git commit number
Source0:    %{name}-%{commit}.zip
# seems to also work
Patch0:     mpb-Fedoralibctl.patch
Patch1:     mpb-testCTL.patch
Patch2:     mpb-utilsCTL.patch
Patch3:     mpb-autogenRemoveConfigure.patch
Patch4:     mpb-configure_ac_libctl.patch

%global mpi_list mpich openmpi

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: blas-devel
BuildRequires: fftw2
BuildRequires: fftw2-devel
BuildRequires: guile-devel
BuildRequires: hdf5-devel
BuildRequires: lapack-devel
BuildRequires: libctl-devel
BuildRequires: libgfortran
BuildRequires: libquadmath-devel
BuildRequires: libtool

Requires:      libctl-devel

%description
The MIT Photonic-Bands (MPB) package is a free program for computing the band
structures (dispersion relations) and electromagnetic modes of periodic
dielectric structures, on both serial and parallel computers. It was developed
by Steven G. Johnson at MIT along with the Joannopoulos Ab Initio Physics
group.

%package mpich
Summary:    Unofficial MPB RPM package with mpich support
BuildRequires: mpich-devel
BuildRequires: fftw2-mpich-devel

%description mpich
The MIT Photonic-Bands (MPB) with MPI (mpich).

%package openmpi
Summary:    Unofficial MPB RPM package with openmpi support
BuildRequires: openmpi-devel
BuildRequires: fftw2-openmpi-devel

%description openmpi
The MIT Photonic-Bands (MPB) with MPI (openmpi).


%prep
%setup -qn %{name}-%{commit}
%patch3 -p1
%patch4 -p0

# autoconf is required because for now patch 14 patches the configure.ac file
%build
sh autogen.sh

cd ..
for mpi in %{mpi_list}
do
rm -rf %{name}-%{commit}-build-$mpi

cp -p -R %{name}-%{commit} %{name}-%{commit}-build-$mpi

pushd %{name}-%{commit}-build-$mpi
module load mpi/${mpi}-%{_arch}

%configure \
    --enable-maintainer-mode \
    --enable-portable-binary \
    --with-mpi \
    --with-fftw2 \
    --libdir=%{_libdir}/$mpi/lib \
    --bindir=%{_libdir}/$mpi/bin \
    --sbindir=%{_libdir}/$mpi/sbin \
    --includedir=%{_includedir}/$mpi-%{_arch} \
    --datarootdir=%{_libdir}/$mpi/share \
    --mandir=%{_libdir}/$mpi/share/man

make %{?_smp_mflags}

module purge
popd
done


rm -rf %{name}-%{commit}-build
cp -p -R %{name}-%{commit} %{name}-%{commit}-build
pushd %{name}-%{commit}-build
%configure --enable-maintainer-mode --enable-portable-binary
make %{?_smp_mflags}
popd

%install
cd ..
for mpi in %{mpi_list}
do
make -C %{name}-%{commit}-build-${mpi} install DESTDIR=%{buildroot}
# seems some binaries are being installed in the wrong place
# mv %{buildroot}/%{_bindir}/* %{buildroot}/%{_libdir}/$mpi/bin
done
make -C %{name}-%{commit}-build install DESTDIR=%{buildroot}

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'


%files
%doc
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.a
%{_datadir}/*
#%{_bindir}/mpb
#%{_bindir}/mpb-data
#%{_bindir}/mpb-split
#%{_includedir}/mpb.h
#%{_includedir}/mpb/eigensolver.h
#%{_includedir}/mpb/matrices.h
#%{_includedir}/mpb/maxwell.h
#%{_includedir}/mpb/scalar.h
#%{_libdir}/libmpb.a
#%{_datadir}/mpb/mpb.scm
#%{_mandir}/man1/*

%files mpich
%{_libdir}/mpich/bin/*
%{_libdir}/mpich/lib/*
%{_includedir}/mpich-%{_arch}/*
%{_libdir}/mpich/share/man/man1/*

%files openmpi
%{_libdir}/openmpi/bin/*
%{_libdir}/openmpi/lib/*
%{_includedir}/openmpi-%{_arch}/*
%{_libdir}/openmpi/share/man/man1/*


%changelog
* Mon Apr 06 2015 Mark Harfouche - 1.5.1-9
- Simplified the patch for fidning the correct libctl path.

* Sun Mar 22 2015 Mark Harfouche - 1.5.1-8
- Fixed a problem with mpb requiring openmpi and mpich

* Sun Mar 22 2015 Mark Harfouche- 1.5.1-7
- Got portable libraries now

* Sun Mar 22 2015 Mark Harfouche - 1.5.1-6
- Finally got the right dependencies, I think

* Sat Mar 21 2015 Mark Harfouche - 1.5.1-5
- rebuilt

* Sat Mar 21 2015 Mark Harfouche - 1.5.1-4
- rebuilt

* Sat Mar 21 2015 Mark Harfouche - 1.5.1-3
- Added BuildRequires autocom and automake

* Sat Mar 21 2015 Mark Harfouche - 1.5.1-2
- Added openmpi and mpich

* Fri Mar 20 2015 Mark Harfouche - 1.5.1-1
- First build

