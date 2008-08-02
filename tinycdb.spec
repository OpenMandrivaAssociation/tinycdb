# compatability macros
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

%{?!_with_unstable: %{error:%(echo -e "\n\n\nYou are building package for a stable release, please see \nhttp://qa.mandrakesoft.com/twiki/bin/view/Main/DistroSpecificReleaseTag\nif you think this is incorrect\n\n\n ")}%(sleep 2)}

%define	name	tinycdb
%define	version	0.74
%define	release	%mkrel 7
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
Source0:	ftp://ftp.corpit.ru/pub/tinycdb/%{name}-%{version}.tar.bz2
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
%description -n %{dlibname}
Libraries and header files needed to develop applications using
constant databases.

%prep
%setup -q -n %{name}-%{version}

%build
%make CFLAGS="$RPM_OPT_FLAGS" all pic shared nss

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
%makeinstall syslibdir=%{buildroot}/%{_lib} \
	install-all install-nss install-shared
rm -f %{buildroot}%{_sysconfdir}/cdb-Makefile

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n nss_%{name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n nss_%{name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files 
%defattr(-,root,root)
%doc NEWS ChangeLog
%{_bindir}/cdb
%{_mandir}/man1/cdb.1*
%{_mandir}/man5/cdb.5*

%files -n nss_tinycdb
%defattr(-,root,root)
%doc cdb-Makefile
/%{_lib}/libnss_cdb.so.%{libcmajor}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcdb.so.%{major}

%files -n %{dlibname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libcdb.a
%{_libdir}/libcdb.so
%{_mandir}/man3/cdb.3*

