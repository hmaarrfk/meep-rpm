Name:       meep
Version:    1.2.2
Release:    4%{?dist}
Summary:    Unofficial meep RPM package

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/meep/
%global commit 7c9aeb2f0324565247542a36865d0b0e7c8cceb4
Source0:    meep-%{commit}.tar.gz
# Patch 0 helps makes autogen do less
# alos return the correct exit status
Patch0: meep-patch0_autogenExitStatus.patch
# Patch 1 makes the mpb interface work. They updated something
Patch1: meep-patch1_newmpbEigensolver.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: blas-devel
BuildRequires: guile-devel
BuildRequires: lapack-devel
BuildRequires: libctl-devel
BuildRequires: libgfortran
BuildRequires: libquadmath-devel
BuildRequires: libtool
BuildRequires: swig

# Not so optional
BuildRequires: hdf5-devel

# Optional libraries but come on, these are small packages that are useful
BuildRequires: harminv
BuildRequires: mpb


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

%package mpich
Summary:    Unofficial meep RPM package with mpich support
# need to compile against mpich
BuildRequires: mpich-devel
BuildRequires: mpb-mpich

%description mpich
Meep finite-difference time-domain (FDTD) simulation software with mpich.

%package openmpi
Summary:    Unofficial meep RPM package with openmpi support
# need to compile against mpich
BuildRequires: openmpi-devel
BuildRequires: mpb-openmpi

%description openmpi
Meep finite-difference time-domain (FDTD) simulation software with openmpi.


%prep
%setup -qn meep-%{commit}
%patch0 -p1
%patch1 -p1


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
# Make once for without mpi
%configure --enable-maintainer-mode --enable-portable-binary
make %{?_smp_mflags}
popd

%install
cd ..
make -C %{name}-%{commit}-build  install DESTDIR=%{buildroot}
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
%{_libdir}/*.a
%{_libdir}/pkgconfig/meep.pc
#%{_mandir}/man1/*

%files mpich
%doc
%{_libdir}/mpich/bin/*
%{_libdir}/mpich/lib/*
%{_includedir}/mpich-%{_arch}/*
#%{_libdir}/mpich/share/man/man1/*

%files openmpi
%doc
%{_libdir}/openmpi/bin/*
%{_libdir}/openmpi/lib/*
%{_includedir}/openmpi-%{_arch}/*
#%{_libdir}/openmpi/share/man/man1/*


%changelog
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

