Summary:	LAN Managment System
Summary(pl):	System Zarz�dzania Sieci� Lokaln�
Name:		lms
Version:	1.3.6
Release:	0.1
License:	GPL
Vendor:		LMS Developers
Group:		Networking/Utilities
Source0:	http://lms.rulez.pl/download/devel/%{name}-%{version}.tar.gz
# Source0-md5:	81cd6c52cd34ad00bae970cee461adf0
Source1:	%{name}.conf
URL:		http://lms.rulez.pl/
BuildRequires:	libgadu-devel
BuildRequires:	mysql-devel
Requires:	php
Requires:	php-posix
Requires:	php-pcre
Requires:	webserver
Requires:	Smarty >= 2.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_lmsdir		%{_datadir}/%{name}
%define		_lmsvar		/var/lib/%{name}

%description
This is a package of applications in PHP and Perl for managing LANs.
It's using MySQL or PostgreSQL. The main goal is to get the best 
service of users at provider's level.
The main features in LMS are:
- database of users (name, surname, address, telefon number,
  commentary);
- database of computers (IP, MAC);
- easy-ridden financial system and funds of network;
- different subscriptions;
- sending warnings to users;
- many levels of access for LMS administrators;
- autogenerating ipchains, iptables, dhcpd, ethers file, oidentd,
  openbsd packet filter configuration files/scripts;
- autogenerating almost any kind of config file using templates;

%description -l pl
"LMS" jest skr�tem od "LAN Management System". Jest to zestaw
aplikacji w PHP i Perlu, u�atwiaj�cych zarz�dzanie sieciami
osiedlowymi (popularnie zwanymi Amatorskimi Sieciami Komputerowymi),
opartych o baz� danych MySQL lub PostgreSQL. G��wne za�o�enia to 
uzyskanie jako�ci us�ug oraz obs�ugi u�ytkownik�w na poziomie 
providera z prawdziwego zdarzenia. 
Najbardziej podstawowe cechy LMS to:
- baza danych u�ytkownik�w (imi�, nazwisko, adres, numer telefonu,
  uwagi);
- baza danych komputer�w (adres IP, adres MAC);
- prowadzenie prostego rachunku operacji finansowych oraz stanu
  fundusz�w sieci;
- r�ne taryfy abonamentowe;
- wysy�anie poczt� elektroniczn� upomnie� do u�ytkownik�w;
- automatyczne naliczanie op�at miesi�cznych;
- r�ne poziomy dost�pu do funkcji LMS dla administrator�w;
- generowanie regu� i plik�w konfiguracyjnych dla ipchains, iptables,
  dhcpd, oidentd, packet filtra openbsd, wpis�w /etc/ethers
- generowanie praktycznie ka�dego pliku konfiguracyjnego na podstawie
  danych w bazie przy u�yciu prostych szablon�w;

%package scripts
Summary:	LAN Managment System - scripts
Summary(pl):	LAN Managment System - skrypty
Requires:	perl-Net-SMTP-Server
Requires:	perl-Config-IniFiles
Requires:	perl-DBI
Group:		Networking/Utilities

%description scripts
This package contains scripts to integrate LMS with your system,
monthly billing, notify users about their debts and cutting off
customers. Also you can build propably any kind of config file using
lms-mgc.

%description scripts -l pl
Ten pakiet zawiera skrypty do zintegrowania LMS z systemem, naliczania
comiesi�cznych op�at, powiadamiania u�ytkownik�w o ich zad�u�eniu oraz
ich automagicznego od��czania. Mo�esz tak�e zbudowa� prawdopodobnie
ka�dy typ pliku konfiguracyjnego przy u�yciu lms-mgc;

%package sqlpanel
Summary:	LAN Managment System - sqlpanel module
Summary(pl):	LAN Managment System - modu� sqlpanel
Requires:	%{name}
Group:		Networking/Utilities

%description sqlpanel
SQL-panel module allows you to execute SQL queries and directly modify data.

%description sqlpanel -l pl
Modu� 'SQL - panel' daje mo�liwo�� bezpo�redniego dost�pu
do bazy danych poprzez zadawanie zapyta� SQL. Wyniki wy�wietlane s�
w formie tabeli. Ponadto podawany jest czas wykonania zapytania.

%package user
Summary:	LAN Managment System - simple user interface
Summary(pl):	LAN Managment System - prosty interfejs u�ytkownika
Requires:	%{name}
Group:		Networking/Utilities

%description user
Simple user interface.

%description user -l pl
Prosty interfejs u�ytkownika.

%package almsd
Summary:	LAN Managment System - almsd
Group:		Networking/Utilities

%description almsd
TODO

%prep
%setup -q -n %{name}

%build
cd daemon
./configure
make CC='%{__cc}' CFLAGS='%{rpmcflags} -DUSE_MYSQL -I../..'
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd/httpd.conf,%{_sysconfdir},%{_lmsvar}/{backups,templates_c},/usr/lib/lms}
install -d $RPM_BUILD_ROOT%{_lmsdir}/{www/{img,doc,user},scripts,config_templates,contrib}

install *.php $RPM_BUILD_ROOT%{_lmsdir}/www
install img/* $RPM_BUILD_ROOT%{_lmsdir}/www/img
cp -r doc/html $RPM_BUILD_ROOT%{_lmsdir}/www/doc
cp -r lib modules templates config_templates $RPM_BUILD_ROOT%{_lmsdir}
install bin/* $RPM_BUILD_ROOT%{_lmsdir}/scripts
#cp -r contrib $RPM_BUILD_ROOT%{_lmsdir}

install sample/%{name}.ini $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/httpd.conf/99_%{name}.conf

# sqlpanel
install contrib/sqlpanel/sql.php $RPM_BUILD_ROOT%{_lmsdir}/modules
install contrib/sqlpanel/*.html $RPM_BUILD_ROOT%{_lmsdir}/templates

# user
install contrib/customer/* $RPM_BUILD_ROOT%{_lmsdir}/www/user

# daemon
install daemon/almsd daemon/modules/*/*.so $RPM_BUILD_ROOT/usr/lib/lms

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl graceful 1>&2
fi

%postun
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl graceful 1>&2
fi

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,ChangeLog*,README,TODO,UPGRADE*,lms*}
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.ini
%config(noreplace) %verify(not size mtime md5) /etc/httpd/httpd.conf/99_%{name}.conf
#
%dir %{_lmsvar} 
%attr(770,root,http) %{_lmsvar}/backups
%attr(770,root,http) %{_lmsvar}/templates_c
#
%dir %{_lmsdir}
%{_lmsdir}/www
%exclude %{_lmsdir}/www/user
%{_lmsdir}/lib
%{_lmsdir}/modules
%exclude %{_lmsdir}/modules/sql.php
%{_lmsdir}/templates
%exclude %{_lmsdir}/templates/sql.html
%exclude %{_lmsdir}/templates/sqlprint.html

%files scripts
%defattr(644,root,root,755)
%dir %{_lmsdir}/scripts
%attr(755,root,root) %{_lmsdir}/scripts/*
%{_lmsdir}/config_templates

%files sqlpanel
%defattr(644,root,root,755)
%{_lmsdir}/modules/sql.php
%{_lmsdir}/templates/sql.html
%{_lmsdir}/templates/sqlprint.html

%files user
%defattr(644,root,root,755)
%{_lmsdir}/www/user

%files almsd
%defattr(644,root,root,755)
%dir /usr/lib/lms
%attr(755,root,root) /usr/lib/lms/almsd
/usr/lib/lms/*.so
