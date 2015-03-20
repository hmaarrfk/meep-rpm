Name:       meep
Version:    1.2.1
Release:    2%{?dist}
Summary:    Unofficial meep RPM package

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/meep/
Source0:    %{name}-%{version}.tar.gz
# github patches
# patch 14 fixes issues for Fedora 21
Patch0: 14.patch
# patch is for the new interface of harminv
Patch1: 15.patch

BuildRequires: autoconf
BuildRequires: blas
BuildRequires: cpio
BuildRequires: fftw-devel
BuildRequires: fftw-libs-double
BuildRequires: gc-devel
BuildRequires: gcc-gfortran
BuildRequires: glibc
BuildRequires: glibc-common
BuildRequires: glibc-devel
BuildRequires: glibc-headers
BuildRequires: gmp-devel
BuildRequires: gsl-devel
BuildRequires: guile-devel
BuildRequires: harminv
BuildRequires: hdf5-devel
BuildRequires: lapack
BuildRequires: libctl-devel
BuildRequires: libgcc
BuildRequires: libgfortran
BuildRequires: libiscsi
BuildRequires: libquadmath

# Without this meep fails at
# ERROR: In procedure apply-smob/1:
# ERROR: In procedure open-file: No such file or directory: "/usr/share/libctl/base/include.scm"
Requires:      libctl-devel

%description
Meep is a free finite-difference time-domain (FDTD) simulation software package
developed at MIT to model electromagnetic systems, along with our MPB eigenmode
package. Its features include:


%prep
%setup -q
%patch0 -p0
#%patch1 -p0


# autoconf is required because for now patch 14 patches the configure.ac file
%build
autoconf
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc
%{_bindir}/*
%{_datadir}/%{name}
%{_includedir}/%{name}.hpp
%{_includedir}/%{name}
%{_libdir}/lib%{name}.la
%{_libdir}/lib%{name}.a
%{_libdir}/pkgconfig/*


%changelog
* Fri Mar 20 2015 makerpm - 1.2.1-2
- Added libctl-devel requirement

* Thu Mar 19 2015 Mark Harfouche - 1.2.1-1
- First build

