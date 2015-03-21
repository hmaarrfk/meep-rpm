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

%global mpi_list mpich openmpi

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

%package mpich
Summary:    Unofficial MPB RPM package with mpich support
BuildRequires: mpich-devel
Requires:   mpich
Requires:   mpb

%description mpich
The MIT Photonic-Bands (MPB) with MPI (mpich).

%package openmpi
Summary:    Unofficial MPB RPM package with openmpi support
BuildRequires: openmpi-devel
Requires:   openmpi
Requires:   mpb

%description openmpi
The MIT Photonic-Bands (MPB) with MPI (openmpi).


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
for mpi in %{mpi_list}
do
rm -rf %{name}-%{commit}-build-$mpi

cp -p -R %{name}-%{commit} %{name}-%{commit}-build-$mpi

pushd %{name}-%{commit}-build-$mpi
module load mpi/${mpi}-%{_arch}

%configure \
    --enable-maintainer-mode \
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
%configure --enable-maintainer-mode
make %{?_smp_mflags}
popd

%install
cd ..
pushd %{name}-%{commit}-build
make install DESTDIR=%{buildroot}
popd
for mpi in %{mpi_list}
do
make -C %{name}-%{commit}-build-${mpi} install DESTDIR=%{buildroot}
done

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'


%files
%doc
%{_bindir}/*
%{_datadir}/*
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man1/*

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
* Sat Mar 21 2015 Mark Harfouche - 1.5.1-2
- Added openmpi and mpich

* Fri Mar 20 2015 Mark Harfouche - 1.5.1-1
- First build

