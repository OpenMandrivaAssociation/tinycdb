%define major 1
%define libcmajor 2
%define _disable_lto 1

# Macro: %%{mklibname <name> [<major> [<minor>]] [-s] [-d]}
%define libname %mklibname %{name} %{major}
%define dlibname %mklibname %{name} %{major} -d

Summary:	Constant Database
Name:		tinycdb
Version:	0.77
Release:	15
License:	Public Domain
Group:		Databases
URL:		http://www.corpit.ru/mjt/tinycdb.html
Source0:	http://www.corpit.ru/mjt/tinycdb/%{name}_%{version}.tar.bz2
Source100:	tinycdb.rpmlintrc
%description
Tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases. The database
structure is tuned for fast reading:

 - Successful lookups take normally just two disk accesses.
 - Unsuccessful lookups take only one disk access.
 - Small disk space and memory size requirements; a database
   uses 2048 bytes for the header and 24 bytes plus size of
   (key,value) per record.
 - Maximum database size is 4GB; individual record size is not
   otherwise limited.
 - Portable file format.
 - Fast creation of new databases.
 - No locking, updates are atomical.

%package -n nss_%{name}
Summary:	Constant database library
Group:		System/Libraries

%description -n nss_%{name}
The tinycdb nss library allows creating passwd/group file using a
constant database.

%package -n %{libname}
Summary:	Constant database library
Group:		System/Libraries

%description -n %{libname}
Tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases. The database
structure is tuned for fast reading.

%package -n %{dlibname}
Summary:	Development libraries and headers for %{libname}
Group:		Development/Databases
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Conflicts:	cdb-devel

%description -n %{dlibname}
Libraries and header files needed to develop applications using
constant databases.

%prep
%setup -q

%build
%make CFLAGS="%{optflags}" \
 staticlib sharedlib cdb-shared nss \
 sysconfdir=%{_sysconfdir}

%install
mkdir -p %{buildroot}
%makeinstall DESTDIR=%{buildroot} \
 libdir=%{_libdir} bindir=%{_bindir} mandir=%{_mandir} \
 syslibdir=/%{_lib} sysconfdir=%{_sysconfdir} \
 includedir=%{_includedir} \
 install-all install-nss install-piclib install-sharedlib \
 INSTALLPROG=cdb-shared CP="cp -p"
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -p debian/libcdb.pc %{buildroot}%{_libdir}/pkgconfig
rm -f %{buildroot}%{_sysconfdir}/cdb-Makefile

# Fix permissions to avoid unstripped-binary-or-object
chmod 0755 %{buildroot}/%{_lib}/libnss_cdb.so.%{libcmajor}
chmod 0755 %{buildroot}%{_libdir}/libcdb.so.%{major}

%files 
%{_bindir}/cdb
%{_mandir}/man1/cdb.1*
%{_mandir}/man5/cdb.5*
%doc ChangeLog NEWS debian/changelog

%files -n nss_tinycdb
%doc nss_cdb-Makefile
/%{_lib}/libnss_cdb.so.%{libcmajor}

%files -n %{libname}
%{_libdir}/libcdb.so.%{major}

%files -n %{dlibname}
%{_includedir}/cdb.h
%{_libdir}/libcdb.a
%{_libdir}/libcdb_pic.a
%{_libdir}/libcdb.so
%{_libdir}/pkgconfig/libcdb.pc
%{_mandir}/man3/cdb.3*



%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.77-3mdv2011.0
+ Revision: 670707
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.77-2mdv2011.0
+ Revision: 607999
- rebuild

* Sun Jan 24 2010 Luca Berra <bluca@mandriva.org> 0.77-1mdv2010.1
+ Revision: 495485
- new version 0.77

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 0.74-8mdv2010.0
+ Revision: 434389
- rebuild

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 0.74-7mdv2009.0
+ Revision: 261542
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 0.74-6mdv2009.0
+ Revision: 254562
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.74-4mdv2008.1
+ Revision: 128462
- kill re-definition of %%buildroot on Pixel's request
- import tinycdb


* Sun Aug 28 2005 Luca Berra <bluca@vodka.it> 0.74-4mdk
- rebuild

* Fri Apr 15 2005 Luca Berra <bluca@vodka.it> 0.74-3mdk
- %%mkrel tag, rebuild

* Wed Feb 25 2004 Luca Berra <bluca@vodka.it> 0.74-2mdk
- CFL: cdb-devel

* Mon Jan 19 2004 Luca Berra <bluca@vodka.it> 0.74-1mdk
- Initial mandrake contrib
