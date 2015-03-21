Name:       meep
Version:    1.2.2
Release:    2%{?dist}
Summary:    Unofficial meep RPM package

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/meep/
%global commit 7c9aeb2f0324565247542a36865d0b0e7c8cceb4
Source0:    meep-%{commit}.tar.gz
# github patches
# patch 14 fixes issues for Fedora 21
# patch is for the new interface of harminv
# Patch 0 and 1 are required for version 1.2.1
#Patch0: 14.patch
#Patch1: 15.patch


# Patch 2 helps makes autogen do less
# alos return the correct exit status
Patch2: meep-patch0_autogenExitStatus.patch
# Patch 3 makes the mpb interface work. They updated something
Patch3: meep-patch1_newmpbEigensolver.patch

BuildRequires: blas
BuildRequires: lapack
BuildRequires: libctl-devel
BuildRequires: guile-devel

# Not so optional
BuildRequires: hdf5-devel

# Optional libraries but come on, these are small packages that are useful
BuildRequires: harminv
BuildRequires: mpb

# need to compile against mpich
BuildRequires: mpich-devel

# Without this meep fails at
# ERROR: In procedure apply-smob/1:
# ERROR: In procedure open-file: No such file or directory: "/usr/share/libctl/base/include.scm"
Requires:      libctl-devel

Requires:      %{name}-common

%description
Meep is a free finite-difference time-domain (FDTD) simulation software package
developed at MIT to model electromagnetic systems, along with our MPB eigenmode
package.

%package common
Summary:       Common headers between meep and meep-mpi

%description common
Common files to meep and meep-mpi

%package mpi
Summary:    Unofficial meep RPM package with mpi support
%description mpi
Meep is a free finite-difference time-domain (FDTD) simulation software package
developed at MIT to model electromagnetic systems, along with our MPB eigenmode
package. With MPI support (mpich).



%prep
%setup -qn meep-%{commit}
#%patch0 -p0
#%patch1 -p0
%patch2 -p1
%patch3 -p1


%build
sh autogen.sh

# Do out of tree builds
%global _configure ../configure


# this helps find some files that are not good with out of tree builds
mkdir build
mkdir build/libctl
cp -p libctl/* build/libctl/.
pushd build
ln -s ../configure .

# Make once for without mpi
%configure --enable-maintainer-mode
make %{?_smp_mflags}

popd

module load mpi/mpich-%{_arch}

mkdir build-mpi
mkdir build-mpi/libctl
cp -p libctl/* build-mpi/libctl/.
pushd build-mpi
ln -s ../configure .

# Make once for without mpi
%configure --enable-maintainer-mode --with-mpi
make %{?_smp_mflags}

module purge
popd

%install
make -C build     install DESTDIR=%{buildroot}
make -C build-mpi install DESTDIR=%{buildroot}


%files
%{_bindir}/meep
%{_libdir}/libmeep.la
%{_libdir}/libmeep.a
%{_libdir}/pkgconfig/meep.pc

%files common
%doc
%{_datadir}/meep
%{_includedir}/meep.hpp
%{_includedir}/meep/vec.hpp
%{_includedir}/meep/mympi.hpp

%files mpi
%{_bindir}/meep-mpi
%{_libdir}/libmeep_mpi.la
%{_libdir}/libmeep_mpi.a
%{_libdir}/pkgconfig/meep_mpi.pc


%changelog
* Fri Mar 20 2015 Mark Harfouche - 1.2.2-2
- Trying to split up the package to allow for simultaneous install of meep and
  meep-mpi.

* Fri Mar 20 2015 Mark Harfouche - 1.2.2-1
- Using git version now

* Fri Mar 20 2015 Mark Harfouche - 1.2.1-2
- Added libctl-devel requirement

* Thu Mar 19 2015 Mark Harfouche - 1.2.1-1
- First build

