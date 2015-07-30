Name:       mpb
Version:    1.5.1
Release:    13%{?dist}
Summary:    Unofficial MPB RPM package

%global commit d7d4930ebe84c5ca9abe750021e106e204ab79ae

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
#Patch4:     mpb-configure_ac_libctl.patch

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

# Don't really know how to package devel files
# I inspired myself from the fftw3 .spec file
%package devel
Summary: Development files for mpb
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
Development files for mpb.

%package static
Summary: Static libraries files for mpb (untested)
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
%description static
Static libraries files for mpb (untested)

%package mpich
Summary:    Unofficial MPB RPM package with mpich support
BuildRequires: mpich-devel
BuildRequires: fftw2-mpich-devel
%description mpich
The MIT Photonic-Bands (MPB) with MPI (mpich).

%package mpich-devel
Summary:    Unofficial MPB RPM package with mpich support development library
Requires:   %{name}-mpich{?_isa} = %{version}-%{release}
%description mpich-devel
The MIT Photonic-Bands (MPB) with MPI (mpich) development libraries.

%package mpich-static
Summary:    Unofficial MPB RPM package with mpich support static libraries
Requires:   %{name}-mpich-devel{?_isa} = %{version}-%{release}
%description mpich-static
The MIT Photonic-Bands (MPB) with MPI (mpich) static libraries.

%package openmpi
Summary:    Unofficial MPB RPM package with openmpi support
BuildRequires: openmpi-devel
BuildRequires: fftw2-openmpi-devel
%description openmpi
The MIT Photonic-Bands (MPB) with MPI (openmpi).

%package openmpi-devel
Summary:    Unofficial MPB RPM package with openmpi support development library
Requires:   %{name}-openmpi{?_isa} = %{version}-%{release}
%description openmpi-devel
The MIT Photonic-Bands (MPB) with MPI (openmpi) development libraries.

%package openmpi-static
Summary:    Unofficial MPB RPM package with openmpi support static libraries
Requires:   %{name}-openmpi-devel{?_isa} = %{version}-%{release}
%description openmpi-static
The MIT Photonic-Bands (MPB) with MPI (openmpi) stati libraries.


%prep
%setup -qn %{name}-%{commit}
%patch3 -p1

# autoconf is required because for now patch 14 patches the configure.ac file
%build
autoreconf --verbose --install --symlink --force
cd ..

rm -rf %{name}-%{commit}-build
cp -p -R %{name}-%{commit} %{name}-%{commit}-build
pushd %{name}-%{commit}-build
%configure --enable-maintainer-mode --enable-portable-binary --enable-shared
make %{?_smp_mflags}
popd

previous_LDFLAGS=${LDFLAGS}


for mpi in %{mpi_list}
do
rm -rf %{name}-%{commit}-build-$mpi

cp -p -R %{name}-%{commit} %{name}-%{commit}-build-$mpi

pushd %{name}-%{commit}-build-$mpi
module load mpi/${mpi}-%{_arch}

export LDFLAGS=-L%{_libdir}/$mpi/lib

%configure \
    --enable-maintainer-mode \
    --enable-portable-binary \
    --enable-shared \
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

export LDFLAGS=%{previous_LDFLAGS}



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

%post
/sbin/ldconfig

%postun
/sbin/ldconfig


#####%doc
%files
%doc
%{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/mpb
%{_libdir}/*.so.*

%files static
%{_libdir}/*.a

%files devel
%{_libdir}/*.so
%{_includedir}/*.h
%{_includedir}/mpb


%files mpich
%{_libdir}/mpich/bin/*
%{_libdir}/mpich/lib/*.so.*
%{_libdir}/mpich/share/man/man1/*

%files mpich-devel
%{_libdir}/mpich/lib/*.so
%{_includedir}/mpich-%{_arch}/*.h
%{_includedir}/mpich-%{_arch}/mpb

%files mpich-static
%{_libdir}/mpich/lib/*.a

%files openmpi
%{_libdir}/openmpi/bin/*
%{_libdir}/openmpi/lib/*.so.*
%{_libdir}/openmpi/share/man/man1/*

%files openmpi-devel
%{_libdir}/openmpi/lib/*.so
%{_includedir}/openmpi-%{_arch}/*.h
%{_includedir}/openmpi-%{_arch}/mpb

%files openmpi-static
%{_libdir}/openmpi/lib/*.a


%changelog
* Thu Jul 30 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.5.1-13
- Correct placement of .h files

* Wed Jul 22 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.5.1-12
- With shared libraries

* Tue Jul 21 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.5.1-11
- Adding shared libraries

* Wed Jul 08 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.5.1-10
- rebuilt

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

