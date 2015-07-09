Name:       h5utils
Version:    1.12.1
Release:    3%{?dist}
Summary:    Unofficial h5utils RPM package

#Group:
License:    MIT
URL:        http://ab-initio.mit.edu/wiki/index.php/H5utils
Source0:    http://ab-initio.mit.edu/h5utils/%{name}-%{version}.tar.gz
Patch0:     h5utils-1.12.1-png_get_.patch

BuildRequires: cpio
BuildRequires: hdf5-devel
BuildRequires: libjpeg-turbo
BuildRequires: libpng-devel
BuildRequires: libmatheval-devel

#Requires:

%description
h5utils is a set of utilities for visualization and conversion of scientific data in the free, portable HDF5 format.

Besides providing a simple tool for batch visualization as PNG images, h5utils also includes programs to convert HDF5 datasets into the formats required by other free visualization software (e.g. plain text, Vis5d, and VTK).

This package is developed by Steven G. Johnson (stevenj@alum.mit.edu), and is free software that should easily install under any Unix-like operating system (e.g. GNU/Linux).


%prep
%setup -q

%patch0 -p0


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*



%changelog
* Fri Mar 20 2015 makerpm - 1.12.1-3
- Added the dependency required to build h5math
* Fri Mar 20 2015 makerpm - 1.12.1-2
-Apparently png frees the memory itself for the palette.

* Thu Mar 19 2015 Mark Harfouche - 1.12.1-1
- First build

