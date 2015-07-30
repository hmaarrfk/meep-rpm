Name:       meep
Version:    1.3.0
Release:    5%{?dist}
Summary:    Unofficial meep RPM package

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/meep/
%global commit 3ae453dfbe32f463713c274bf0da2a980905f3bb
Source0:    meep-%{commit}.zip
# Patch 0 helps makes autogen do less
# alos return the correct exit status
Patch0: meep-patch0_autogenExitStatus.patch
Patch1: meep-requireMPB.patch


BuildRequires: autoconf
BuildRequires: automake
BuildRequires: blas-devel
BuildRequires: guile-devel
BuildRequires: lapack-devel
BuildRequires: libctl-devel
BuildRequires: libgfortran
BuildRequires: libquadmath-devel
BuildRequires: gsl-devel
BuildRequires: libtool
BuildRequires: swig

# Not so optional
BuildRequires: hdf5-devel

# Optional libraries but come on, these are small packages that are useful
BuildRequires: harminv-devel >= 1.4
BuildRequires: mpb-devel >= 1.5.1-12
BuildRequires: fftw2-devel


# Without this meep fails at
# ERROR: In procedure apply-smob/1:
# ERROR: In procedure open-file: No such file or directory: "/usr/share/libctl/base/include.scm"
Requires:      libctl-devel

%description
Meep is a free finite-difference time-domain (FDTD) simulation software package
developed at MIT to model electromagnetic systems, along with our MPB eigenmode
package.

# List of MPIs to compile for
%global mpi_list mpich openmpi

%package devel
Summary: Development files for meep
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
Development files for meep.

%package static
Summary: Static libraries for meep
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description static
Static libraries for meep.

%package mpich
Summary:    Unofficial meep RPM package with mpich support
# need to compile against mpich
BuildRequires: mpich-devel
BuildRequires: mpb-mpich
BuildRequires: fftw2-mpich-devel
%description mpich
Meep finite-difference time-domain (FDTD) simulation software with mpich.

%package mpich-devel
Summary: Development files for meep with MPICH (MPI)
Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}
%description mpich-devel
Development files for meep with MPICH (MPI).

%package mpich-static
Summary: Static libraries for meep with MPICH (MPI)
Requires:       %{name}-mpich-devel%{?_isa} = %{version}-%{release}
%description mpich-static
Static libraries for meep with MPICH (MPI).

%package openmpi
Summary:    Unofficial meep RPM package with openmpi support
# need to compile against mpich
BuildRequires: openmpi-devel
BuildRequires: mpb-openmpi
BuildRequires: fftw2-openmpi-devel

%description openmpi
Meep finite-difference time-domain (FDTD) simulation software with openmpi.

%package openmpi-devel
Summary: Development files for meep with openmpi (MPI)
Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}
%description openmpi-devel
Development files for meep with openmpi (MPI).

%package openmpi-static
Summary: Static libraries for meep with openmpi (MPI)
Requires:       %{name}-openmpi-devel%{?_isa} = %{version}-%{release}
%description openmpi-static
Static libraries for meep with openmpi (MPI).


%prep
%setup -qn meep-%{commit}
%patch0 -p1
%patch1 -p1


%build
cd ..

rm -rf %{name}-%{commit}-build
cp -p -R %{name}-%{commit} %{name}-%{commit}-build

pushd %{name}-%{commit}-build
autoreconf --verbose --install --symlink --force
# Make once for without mpi
%configure --enable-maintainer-mode --enable-portable-binary --enable-shared
make %{?_smp_mflags}
popd

for mpi in %{mpi_list}
do
rm -rf %{name}-%{commit}-build-$mpi

cp -p -R %{name}-%{commit} %{name}-%{commit}-build-$mpi

pushd %{name}-%{commit}-build-$mpi
module load mpi/${mpi}-%{_arch}

autoreconf --verbose --install --symlink --force

%configure \
    --enable-maintainer-mode \
    --enable-portable-binary \
    --enable-shared \
    --with-mpi \
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



%install
cd ..
make -C %{name}-%{commit}-build  install DESTDIR=%{buildroot}
for mpi in %{mpi_list}
do
make -C %{name}-%{commit}-build-${mpi} install DESTDIR=%{buildroot}
done

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'


%files
%doc AUTHORS COPYING COPYRIGHT NEWS README.md TODO
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/meep.pc
%{_libdir}/*.so

%files static
%{_libdir}/*.a

%files mpich
%doc AUTHORS COPYING COPYRIGHT NEWS README.md TODO
%{_libdir}/mpich/bin/*
%{_libdir}/mpich/lib/*.so.*

%files mpich-devel
%{_includedir}/mpich-%{_arch}/*
%{_libdir}/mpich/lib/pkgconfig/meep_mpi.pc
%{_libdir}/mpich/lib/*.so

%files mpich-static
%{_libdir}/mpich/lib/*.a

%files openmpi
%doc AUTHORS COPYING COPYRIGHT NEWS README.md TODO
%{_libdir}/openmpi/bin/*
%{_libdir}/openmpi/lib/*.so.*

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}/*
%{_libdir}/openmpi/lib/pkgconfig/meep_mpi.pc
%{_libdir}/openmpi/lib/*.so

%files openmpi-static
%{_libdir}/openmpi/lib/*.a


%changelog
* Thu Jul 30 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.3.0-5
- Added documentation

* Wed Jul 29 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.3.0-4
- With GSL for near to far field

* Wed Jul 22 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.3.0-3
- With shared libraries and separated out the static files

* Thu Jul 09 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.3.0-2
- Updated version of harminv

* Wed Jul 8 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.3.0-1
- Updated versions of MEEP

* Mon Mar 23 2015 Mark Harfouche - 1.2.2-5
- Trying to make sure that it is compiled with MPB

* Sun Mar 22 2015 Mark Harfouche - 1.2.2-4
- I think the dependencies on meep are fixed. No longer requires mpi

* Sun Mar 22 2015 Mark Harfouche - 1.2.2-3
- I think it actually has MPB support now. Also compiles for openmpi and mpich

* Fri Mar 20 2015 Mark Harfouche - 1.2.2-2
- Trying to split up the package to allow for simultaneous install of meep and
  meep-mpi.

* Fri Mar 20 2015 Mark Harfouche - 1.2.2-1
- Using git version now

* Fri Mar 20 2015 Mark Harfouche - 1.2.1-2
- Added libctl-devel requirement

* Thu Mar 19 2015 Mark Harfouche - 1.2.1-1
- First build

