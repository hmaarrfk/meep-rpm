Name:       harminv
Version:    1.4.0
Release:    4%{?dist}
Summary:    Unofficial Harminv Package

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/wiki/index.php/Harminv
%global commit ba947a42c5c2ade0c3c3b48d539575ebc87db8a1
#Source0:    http://ab-initio.mit.edu/harminv/%{name}-%{version}.tar.gz
Source0:    harminv-%{commit}.zip

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: blas-devel
BuildRequires: gcc
BuildRequires: gcc-gfortran
BuildRequires: glibc-devel
BuildRequires: glibc-headers
BuildRequires: lapack-devel
BuildRequires: libgcc
BuildRequires: libgfortran
BuildRequires: libquadmath-devel
BuildRequires: libstdc++-devel

#Requires:

%description
Harminv is a free program (and accompanying library) to solve the problem of
harmonic inversion — given a discrete-time, finite-length signal that consists
of a sum of finitely-many sinusoids (possibly exponentially decaying) in a
given bandwidth, it determines the frequencies, decay constants, amplitudes,
and phases of those sinusoids.


# Don't really know how to package devel files
# I inspired myself from the fftw3 .spec file
%package devel
Summary: Development files for harminv
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for harminv.

%package static
Summary: Static libraries files for harminv (untested)
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libraries files for harminv (untested)


%prep
%setup -qn harminv-%{commit}


%build
libtoolize --force
autoreconf --verbose --install --symlink --force
%configure \
    --enable-maintainer-mode \
    --enable-shared
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc
%{_bindir}/*
%{_libdir}/libharminv.so.*
%{_mandir}/man1/*

%files devel
%{_includedir}/*
%{_libdir}/libharminv.so
%{_libdir}/pkgconfig/*

%files static
%{_libdir}/libharminv.a

%changelog
* Thu Jul 23 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.4.0-4
- Removed .la

* Tue Jul 21 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.4.0-3
- Adding shared libraries (*.so files)

* Wed Jul 8 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.4.0-2
- rebuild

* Wed Jul 8 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.4.0-1
- Updated versions of harminv

* Sat Mar 21 2015 Mark Harfouche - 1.3.1-3
- BuildDepends modifications

* Fri Mar 20 2015 Mark Harfouche - 1.3.1-2
- Added a few build requires.

* Fri Mar 20 2015 Mark Harfouche - 1.3.1-1
- First build

