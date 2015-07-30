Name:           fftw2
Version:        2.1.5
Release:        29%{?dist}
Summary:        Fast Fourier Transform library (version 2)
%define         real_name fftw

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.fftw.org/
Source0:        ftp://ftp.fftw.org/pub/fftw/fftw-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-gfortran


# MPI support inspired by MPI support on the hdf5 package
#No mpich on ppc64
%ifarch ppc64
%global mpi_list openmpi
%else
%global mpi_list mpich openmpi
%endif

%description
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.


%package        devel
Summary:        Headers, libraries and docs for the FFTW library (version 2)
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
FFTW is a C subroutine library for computing the Discrete Fourier Transform
(DFT) in one or more dimensions, of both real and complex data, and of
arbitrary input size. We believe that FFTW, which is free software, should
become the FFT library of choice for most applications. Our benchmarks,
performed on on a variety of platforms, show that FFTW's performance is
typically superior to that of other publicly available FFT software.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library version 2.


%package        static
Summary:        Static version of the FFTW library (version 2)
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
This package contains the static linked libraries of the FFTW fast Fourier
transform library (version 2).

%ifnarch ppc64
%package        mpich
Summary:        Fast Fourier Transform library (version 2) with mpich
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       mpich
BuildRequires:  mpich-devel

%description    mpich
FFTW 2 with mpich libraries.

%package        mpich-devel
Summary:        Libraries for the FFTW library (version 2) with mpich
Group:          Development/Libraries
Requires:       %{name}-mpich = %{version}-%{release}
Requires:       mpich

%description    mpich-devel
FFTW 2 with mpich development files.

%package        mpich-static
Summary:        FFTW static library (version 2) with mpich
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    mpich-static
FFTW 2 with mpich static libraries.
%endif

%package        openmpi
Summary:        Fast Fourier Transform library (version 2) with openmpi
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       openmpi
BuildRequires:  openmpi-devel

%description    openmpi
FFTW 2 with openmpi libraries.

%package        openmpi-devel
Summary:        Libraries for the FFTW library (version 2) with openmpi
Group:          Development/Libraries
Requires:       %{name}-openmpi = %{version}-%{release}
Requires:       openmpi

%description    openmpi-devel
FFTW 2 with openmpi development files.

%package        openmpi-static
Summary:        FFTW static library (version 2) with openmpi
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    openmpi-static
FFTW 2 with openmpi static libraries.

%prep
%setup -q -c %{real_name}-%{version}
mv %{real_name}-%{version} single
cp -a single double

for mpi in %{mpi_list}
do
    cp -a single double-${mpi}
done

%build
pushd double
	%ifarch i386
		%configure \
			--enable-shared \
			--enable-threads \
			--enable-i386-hacks
	%else
		%configure \
			--enable-shared \
			--enable-threads
	%endif
	make %{?_smp_mflags}
popd
pushd single
	%configure \
		--enable-shared \
		--enable-type-prefix \
		--enable-threads \
		--enable-float
	make %{?_smp_mflags}
popd

# MPI builds
for mpi in %{mpi_list}
do
    module load mpi/$mpi-%{_arch}
    pushd double-$mpi
    %configure \
        --enable-shared \
		--enable-threads \
%ifarch i386
        --enable-i386-hacks \
%endif
        --enable-mpi \
        --libdir=%{_libdir}/$mpi/lib \
        --bindir=%{_libdir}/$mpi/bin \
        --sbindir=%{_libdir}/$mpi/sbin \
        --includedir=%{_includedir}/$mpi-%{_arch} \
        --mandir=%{_libdir}/$mpi/share/man
    make %{?_smp_mflags}
    # MPI support is only available for the double library

    module purge

    popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
pushd double
	make install DESTDIR=${RPM_BUILD_ROOT}
	cp -a AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO ../
	cp -a FAQ/fftw-faq.html/ doc/ ../
popd
pushd single
	make install DESTDIR=${RPM_BUILD_ROOT}
popd

for mpi in %{mpi_list}
do
    make -C double-$mpi install DESTDIR=${RPM_BUILD_ROOT}
done

rm -f doc/Makefile*
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%clean
rm -rf ${RPM_BUILD_ROOT}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc  doc/
%{_includedir}/*
%{_libdir}/*.so
%{_infodir}/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%ifnarch ppc64
# defattr no longer needed
%files mpich
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/mpich/lib/*.so.*

%files mpich-devel
%{_includedir}/mpich-%{_arch}
%{_libdir}/mpich/lib/lib*.so

%files mpich-static
%{_libdir}/mpich/lib/*.a
%endif

%files openmpi
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/openmpi/lib/*.so.*

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}
%{_libdir}/openmpi/lib/lib*.so

%files openmpi-static
%{_libdir}/openmpi/lib/*.a


%changelog
* Sat Mar 21 2015 Mark harfouche <mark.harfouche@gmail.com> - 2.1.5.29
- added mpich and opennmpi

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 22 2010 José Matos <jamatos@fc.up.pt> - 2.1.5-21
- Move static libraries to a static subpackage (bz556047)
- Add remarks that this is version 2 of fftw to description and summaries

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.5-20
- drop static libs (bz556047)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Robert Scheck <robert@fedoraproject.org> - 2.1.5-18
- Removed the shipping and owning of %%{_infodir}/dir file

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 14 2008 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-16
- Rebuild for gcc 4.3

* Tue Aug 28 2007 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-15
- License fix, rebuild for devel (F8).

* Sat Apr 21 2007 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-14
- Rebuild for F7.

* Tue Aug 29 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-13
- Rebuild for FE6

* Sat Feb 18 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-12
- Rebuild for FC-5.

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-11
- Fix incomplete substitution

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-10
- Add disttag to release.

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 2.1.5-9
- Rename package to fftw2.

* Mon May 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.1.5-8
- BuildReq gcc-gfortran (#156490).

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.1.5-7
- rebuild on all arches
- buildrequire compat-gcc-32-g77

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 2.1.5-5
- Bump release to provide Extras upgrade path.

* Tue Apr 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.4
- BuildReq gcc-g77.

* Mon Sep 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.3
- Dropped post/preun scripts for info.

* Wed Sep 17 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.2
- Remove aesthetic comments.
- buildroot -> RPM_BUILD_ROOT.
- post/preun for info files.

* Mon Apr 07 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.5-0.fdr.1
- Updated to 2.1.5.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.1.4-0.fdr.2
- Added Epoch:0.
- Added ldconfig to post and postun.

* Sun Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.4-0.fdr.1
- Updated to 2.1.4.

* Fri Mar 14 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 2.1.3-0.fdr.1
- Fedorafied.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.

