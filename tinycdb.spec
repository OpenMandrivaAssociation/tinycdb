%define	name	tinycdb
%define	version	0.77
%define	release	%mkrel 2
%define major 1
%define libcmajor 2

# Macro: %%{mklibname <name> [<major> [<minor>]] [-s] [-d]}
%define libname %mklibname %name %major
%define dlibname %mklibname %name %major -d

Summary:	Constant Database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		Databases
URL:		http://www.corpit.ru/mjt/tinycdb.html
Source0:	http://www.corpit.ru/mjt/tinycdb/%{name}_%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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
Summary: Constant database library
Group: System/Libraries

%description -n nss_%{name}
The tinycdb nss library allows creating passwd/group file using a
constant database.

%package -n %{libname}
Summary: Constant database library
Group: System/Libraries

%description -n %{libname}
Tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases. The database
structure is tuned for fast reading.

%package -n %{dlibname}
Summary: Development libraries and headers for %{libname}
Group: Development/Databases
Requires: %{libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}
Conflicts: cdb-devel
Requires: pkgconfig

%description -n %{dlibname}
Libraries and header files needed to develop applications using
constant databases.

%prep
%setup -q -n %{name}-%{version}

%build
%make CFLAGS="$RPM_OPT_FLAGS" \
 staticlib sharedlib cdb-shared nss \
 sysconfdir=%{_sysconfdir}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n nss_%{name} -p /sbin/ldconfig

%postun -n nss_%{name} -p /sbin/ldconfig

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig
%endif

%files 
%defattr(-,root,root)
%{_bindir}/cdb
%{_mandir}/man1/cdb.1*
%{_mandir}/man5/cdb.5*
%doc ChangeLog NEWS debian/changelog

%files -n nss_tinycdb
%defattr(-,root,root)
%doc nss_cdb-Makefile
/%{_lib}/libnss_cdb.so.%{libcmajor}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcdb.so.%{major}

%files -n %{dlibname}
%defattr(-,root,root)
%{_includedir}/cdb.h
%{_libdir}/libcdb.a
%{_libdir}/libcdb_pic.a
%{_libdir}/libcdb.so
%{_libdir}/pkgconfig/libcdb.pc
%{_mandir}/man3/cdb.3*

