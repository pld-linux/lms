%define		_add pre5
Summary:	LAN Managment System
Summary(pl):	System Zarz±dzania Siec± Lokaln±
Name:		lms
Version:	1.0
Release:	0.1.%{_add}
License:	GPL
Group:		Networking/Utilities
Source0:	http://lms.rulez.pl/download/%{name}-%{version}%{_add}+libs.tar.gz
Requires:	php
Requires:	webserver
Requires:	mysql
Requires:	perl-POSIX
Requires:	perl-GetOpt-Long
Requires:	perl-Net-SMTP
Requires:	perl-Config-IniFiles
Requires:	perl-DBI
Requires:	perl-DBD-mysql
Requires:	perl-DBD-pg
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_lmsdir	/home/services/httpd/html/%{name}

%description

%description -l pl

%prep
%setup -q -n lms

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_lmsdir}/{img,lib,modules,templates,templates_c}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}/

install *.php $RPM_BUILD_ROOT%{_lmsdir}
install -d {img,lib,modules,templates,templates_c} $RPM_BUILD_ROOT%{_lmsdir}
install -d backup $RPM_BUILD_ROOT%{_localstatedir}/%{name}/
install bin/* $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc 
%dir %{_lmsdir}
%attr(770,root,http) %{_lmsdir}/templates_c
%{_lmsdir}/*.php
%{_lmsdir}/img
%{_lmsdir}/lib
%{_lmsdir}/modules
%{_lmsdir}/templates
%{_localstatedir}/%{name}
%{_bindir}/lms-*
