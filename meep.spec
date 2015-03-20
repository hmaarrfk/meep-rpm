Name:       meep
Version:    1.2.2
Release:    1%{?dist}
Summary:    Unofficial meep RPM package

#Group:
License:    GNU GPL
URL:        http://ab-initio.mit.edu/meep/
%global commit 7c9aeb2f0324565247542a36865d0b0e7c8cceb4
Source0:    meep-%{commit}.tar.gz
# github patches
# patch 14 fixes issues for Fedora 21
# patch is for the new interface of harminv
# Patch 0 and 1 are required for version 1.2.1
#Patch0: 14.patch
#Patch1: 15.patch


# Patch 2 helps makes autogen do less
# alos return the correct exit status
Patch2: meep-patch0_autogenExitStatus.patch
# Patch 3 makes the mpb interface work. They updated something
Patch3: meep-patch1_newmpbEigensolver.patch

BuildRequires: blas
BuildRequires: lapack
BuildRequires: libctl-devel
BuildRequires: guile-devel

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
package. Its features include:


%prep
%setup -qn meep-%{commit}
#%patch0 -p0
#%patch1 -p0
%patch2 -p1
%patch3 -p1


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
%{_includedir}/%{name}.hpp
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}.la
%{_libdir}/lib%{name}.a
%{_libdir}/pkgconfig/*


%changelog
* Fri Mar 20 2015 Mark Harfouche - 1.2.2-1
- Using git version now

* Fri Mar 20 2015 Mark Harfouche - 1.2.1-2
- Added libctl-devel requirement

* Thu Mar 19 2015 Mark Harfouche - 1.2.1-1
- First build

