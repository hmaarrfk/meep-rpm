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

#Requires:      libctl-devel

%description
The MIT Photonic-Bands (MPB) package is a free program for computing the band
structures (dispersion relations) and electromagnetic modes of periodic
dielectric structures, on both serial and parallel computers. It was developed
by Steven G. Johnson at MIT along with the Joannopoulos Ab Initio Physics
group.



%prep
%setup -qn %{name}-%{commit}
%patch0 -p0
%patch1 -p0
%patch2 -p0


# autoconf is required because for now patch 14 patches the configure.ac file
%build
sh autogen.sh
%configure --enable-maintainer-mode
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc
%{_bindir}/*
%{_datadir}/%{name}
%{_includedir}/%{name}.h
%{_includedir}/%{name}
%{_libdir}/lib%{name}.la
%{_libdir}/lib%{name}.a
%{_mandir}/man1/*


%changelog
* Fri Mar 20 2015 Mark Harfouche - 1.5.1-1
- First build

