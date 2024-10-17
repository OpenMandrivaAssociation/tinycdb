%define major 1
%define libcmajor 2
# For static lib
%define _disable_lto 1

# Macro: %%{mklibname <name> [<major> [<minor>]] [-s] [-d]}
%define libname %mklibname %{name} %{major}
%define dlibname %mklibname %{name} -d
%define olddlibname %mklibname %{name} %{major} -d

Summary:	Constant Database
Name:		tinycdb
Version:	0.78
Release:	3
License:	Public Domain
Group:		Databases
URL:		https://www.corpit.ru/mjt/tinycdb.html
Source0:	http://www.corpit.ru/mjt/tinycdb/%{name}-%{version}.tar.gz
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
Requires:	%{libname} = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Conflicts:	cdb-devel
%rename %{olddlibname}

%description -n %{dlibname}
Libraries and header files needed to develop applications using
constant databases.

%prep
%setup -q

%build
%make CFLAGS="%{optflags}" \
 CC=%{__cc} \
 staticlib sharedlib cdb-shared nss \
 sysconfdir=%{_sysconfdir}

%install
mkdir -p %{buildroot}
%makeinstall DESTDIR=%{buildroot} \
 libdir=%{_libdir} bindir=%{_bindir} mandir=%{_mandir} \
 CC=%{__cc} \
 syslibdir=/%{_lib} sysconfdir=%{_sysconfdir} \
 includedir=%{_includedir} \
 install-all install-nss install-piclib install-sharedlib \
 INSTALLPROG=cdb-shared CP="cp -p"
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat >%{buildroot}%{_libdir}/pkgconfig/libcdb.pc <<EOF
prefix=%{_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/%{_lib}
includedir=\${prefix}/include

Name: libcdb
Description: tinycdb - Constant Data Base library
Version: %{version}
Libs: -lcdb
EOF
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
