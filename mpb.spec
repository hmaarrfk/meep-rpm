Name:       mpb
Version:    1.5.1
Release:    1%{?dist}
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

BuildRequires: atlas
BuildRequires: blas
BuildRequires: fftw-devel
BuildRequires: fftw-libs-double
BuildRequires: guile-devel
BuildRequires: hdf5-devel
BuildRequires: lapack
BuildRequires: libctl
BuildRequires: libgfortran
BuildRequires: libiscsi
BuildRequires: libquadmath
BuildRequires: mpich-devel

Requires:      libctl-devel

%description
The MIT Photonic-Bands (MPB) package is a free program for computing the band
structures (dispersion relations) and electromagnetic modes of periodic
dielectric structures, on both serial and parallel computers. It was developed
by Steven G. Johnson at MIT along with the Joannopoulos Ab Initio Physics
group.

%package mpi
Summary:    Unofficial MPB RPM package with mpi support
Requires:   mpich
Requires:   mpb

%description mpi
The MIT Photonic-Bands (MPB) with MPI.



%prep
%setup -qn %{name}-%{commit}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1


# autoconf is required because for now patch 14 patches the configure.ac file
%build
sh autogen.sh

cd ..
rm -rf %{name}-%{commit}-build
rm -rf %{name}-%{commit}-build-mpi

cp -p -R %{name}-%{commit} %{name}-%{commit}-build-mpi

pushd %{name}-%{commit}-build-mpi
module load mpi/mpich-%{_arch}
%configure --enable-maintainer-mode --with-mpi --with-fftw2
make %{?_smp_mflags}
module purge
popd

cp -p -R %{name}-%{commit} %{name}-%{commit}-build
pushd %{name}-%{commit}-build
%configure --enable-maintainer-mode
make %{?_smp_mflags}
popd

%install
cd ..
pushd %{name}-%{commit}-build
make install DESTDIR=%{buildroot}
popd
pushd %{name}-%{commit}-build-mpi
make install DESTDIR=%{buildroot}
popd


%files
%doc
%{_bindir}/mpb
%{_bindir}/mpb-data
%{_bindir}/mpb-split
%{_datadir}/mpb
%{_includedir}/mpb.h
%{_includedir}/mpb/*
%{_libdir}/libmpb.la
%{_libdir}/libmpb.a
%{_mandir}/man1/*

%files mpi
%{_bindir}/mpb-mpi
%{_libdir}/libmpb_mpi.la
%{_libdir}/libmpb_mpi.a
%{_includedir}/mpb_mpi.h



%changelog
* Fri Mar 20 2015 Mark Harfouche - 1.5.1-1
- First build

