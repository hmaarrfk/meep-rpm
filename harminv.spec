Name:       harminv
Version:    1.3.1
Release:    3%{?dist}
Summary:    Unofficial Harminv Package

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/wiki/index.php/Harminv
Source0:    http://ab-initio.mit.edu/harminv/%{name}-%{version}.tar.gz

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


%prep
%setup -q


%build
%configure
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
* Sat Mar 21 2015 Mark Harfouche - 1.3.1-3
- BuildDepends modifications

* Fri Mar 20 2015 Mark Harfouche - 1.3.1-2
- Added a few build requires.

* Fri Mar 20 2015 Mark Harfouche - 1.3.1-1
- First build

