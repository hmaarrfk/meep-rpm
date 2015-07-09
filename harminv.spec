Name:       harminv
Version:    1.4.0
Release:    1%{?dist}
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
BuildRequires: libmatheval

#Requires:

%description
Harminv is a free program (and accompanying library) to solve the problem of
harmonic inversion — given a discrete-time, finite-length signal that consists
of a sum of finitely-many sinusoids (possibly exponentially decaying) in a
given bandwidth, it determines the frequencies, decay constants, amplitudes,
and phases of those sinusoids.


%prep
%setup -qn harminv-%{commit}


%build
libtoolize --force
autoreconf --verbose --install --symlink --force
autoreconf --verbose --install --symlink --force
autoreconf --verbose --install --symlink --force
%configure \
    --enable-maintainer-mode
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man1/*



%changelog
* Wed Jul 8 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.4.0-1
- Updated versions of harminv

* Sat Mar 21 2015 Mark Harfouche - 1.3.1-3
- BuildDepends modifications

* Fri Mar 20 2015 Mark Harfouche - 1.3.1-2
- Added a few build requires.

* Fri Mar 20 2015 Mark Harfouche - 1.3.1-1
- First build

