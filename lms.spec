# TODO
# - test build on amd64 and check /usr/lib64 patch
# - cosmetics (sort in %%files and %%install)
# - contrib split
#
# Conditional build:
%bcond_without	lmsd		# without lmsd daemon
#
%define		lmsver		1.10
%define		lmssubver	0
Summary:	LAN Managment System
Summary(pl.UTF-8):	System Zarządzania Siecią Lokalną
Name:		lms
Version:	%{lmsver}.%{lmssubver}
Release:	3
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://www.lms.org.pl/download/%{lmsver}/%{name}-%{version}.tar.gz
# Source0-md5:	01d76c3b82ccc5219aa15b65d67d787d
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-amd64.patch
Patch2:		%{name}-smarty.patch
URL:		http://www.lms.org.pl/
BuildRequires:	bison
BuildRequires:	flex
%{?with_lmsd:BuildRequires:	libgadu-devel}
%{?with_lmsd:BuildRequires:	mysql-devel}
%{?with_lmsd:BuildRequires:	postgresql-devel}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_lmsd:Requires(post,preun):	/sbin/chkconfig}
Requires:	Smarty >= 2.6.18-2
Requires:	php(gd)
Requires:	php(iconv)
Requires:	php(pcre)
Requires:	php(posix)
Requires:	webapps
Requires:	webserver(php)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_lmsdir		%{_datadir}/%{name}
%define		_lmsvar		/var/lib/%{name}
%define		_smartyplugindir	/usr/share/php/Smarty/plugins
%define		_webapps	/etc/webapps
%define		_webapp		%{name}

%description
This is a package of applications in PHP and Perl for managing LANs.
It's using MySQL or PostgreSQL. The main goal is to get the best
service of users at provider's level. The main features in LMS are:
- database of users (name, surname, address, telephone number,
  commentary);
- database of computers (IP, MAC);
- easy-ridden financial system and funds of network;
- different subscriptions;
- sending warnings to users;
- many levels of access for LMS administrators;
- autogenerating ipchains, iptables, dhcpd, ethers file, oidentd,
  openbsd packet filter configuration files/scripts;
- autogenerating almost any kind of config file using templates.

%description -l pl.UTF-8
"LMS" jest skrótem od "LAN Management System". Jest to zestaw
aplikacji w PHP i Perlu, ułatwiających zarządzanie sieciami
osiedlowymi (popularnie zwanymi Amatorskimi Sieciami Komputerowymi),
opartych o bazę danych MySQL lub PostgreSQL. Główne założenia to
uzyskanie jakości usług oraz obsługi użytkowników na poziomie
providera z prawdziwego zdarzenia. Najbardziej podstawowe cechy LMS
to:
- baza danych użytkowników (imię, nazwisko, adres, numer telefonu,
  uwagi);
- baza danych komputerów (adres IP, adres MAC);
- prowadzenie prostego rachunku operacji finansowych oraz stanu
  funduszów sieci;
- różne taryfy abonamentowe;
- wysyłanie pocztą elektroniczną upomnień do użytkowników;
- automatyczne naliczanie opłat miesięcznych;
- różne poziomy dostępu do funkcji LMS dla administratorów;
- generowanie reguł i plików konfiguracyjnych dla ipchains, iptables,
  dhcpd, oidentd, packet filtra openbsd, wpisów /etc/ethers
- generowanie praktycznie każdego pliku konfiguracyjnego na podstawie
  danych w bazie przy użyciu prostych szablonów.

%package scripts
Summary:	LAN Managment System - scripts
Summary(pl.UTF-8):	LAN Managment System - skrypty
Group:		Networking/Utilities
Requires:	perl-Config-IniFiles
Requires:	perl-DBI
Requires:	perl-Net-SMTP-Server

%description scripts
This package contains scripts to integrate LMS with your system,
monthly billing, notify users about their debts and cutting off
customers. Also you can build probably any kind of config file using
lms-mgc.

%description scripts -l pl.UTF-8
Ten pakiet zawiera skrypty do zintegrowania LMS z systemem, naliczania
comiesięcznych opłat, powiadamiania użytkowników o ich zadłużeniu oraz
ich automagicznego odłączania. Możesz także zbudować prawdopodobnie
każdy typ pliku konfiguracyjnego przy użyciu lms-mgc.

%package sqlpanel
Summary:	LAN Managment System - sqlpanel module
Summary(pl.UTF-8):	LAN Managment System - moduł sqlpanel
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description sqlpanel
SQL-panel module allows you to execute SQL queries and directly modify
data.

%description sqlpanel -l pl.UTF-8
Moduł 'SQL - panel' daje możliwość bezpośredniego dostępu do bazy
danych poprzez zadawanie zapytań SQL. Wyniki wyświetlane są w formie
tabeli. Ponadto podawany jest czas wykonania zapytania.

%package user
Summary:	LAN Managment System - simple user interface
Summary(pl.UTF-8):	LAN Managment System - prosty interfejs użytkownika
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description user
Simple user interface.

%description user -l pl.UTF-8
Prosty interfejs użytkownika.

%package lmsd
Summary:	LAN Managment System - LMS system backend
Summary(pl.UTF-8):	LAN Managment System - backend systemu LMS
Group:		Networking/Utilities
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Obsoletes:	lms-almsd

%description lmsd
A program to manage the server by creating configuration files based
upon LMS database and restarting selected services.

%description lmsd -l pl.UTF-8
Program zarządzający serwerem poprzez tworzenie plików
konfiguracyjnych na podstawie bazy danych LMS-a i restartowanie
wybranych usług.

%prep
%setup -q -n %{name}
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif
%patch2 -p1

mkdir smarty-plugins
mv \
lib/Smarty/plugins/block.t.php \
lib/Smarty/plugins/function.{bankaccount,handle,number,size,sum,tip}.php \
lib/Smarty/plugins/modifier.{money_format,striphtml,to_words}.php \
	smarty-plugins
rm -rf lib/Smarty

%build
%if %{with lmsd}

cd daemon

./configure --with-mysql
%{__make} \
	CC='%{__cc}' \
	CFLAGS='%{rpmcflags} -fPIC -DUSE_MYSQL -DLMS_LIB_DIR=\"%{_libdir}/lms/\" -I../..'
mv lmsd lmsd-mysql

./configure --with-pgsql
%{__make} lmsd \
	CC='%{__cc}' \
	CFLAGS='%{rpmcflags} -fPIC -DUSE_PGSQL -DLMS_LIB_DIR=\"%{_libdir}/lms/\" -I../..'
mv lmsd lmsd-pgsql

cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir} \
	   $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	   $RPM_BUILD_ROOT/etc/lms/modules/{dns,ggnofity,nofity} \
	   $RPM_BUILD_ROOT{%{_lmsvar}/{backups,templates_c,documents},%{_libdir}/lms} \
	   $RPM_BUILD_ROOT%{_lmsdir}/www/{img,doc,user} \
	   $RPM_BUILD_ROOT%{_lmsdir}/www/img/core \
	   $RPM_BUILD_ROOT%{_smartyplugindir}

install *.php $RPM_BUILD_ROOT%{_lmsdir}/www
install img/core/* $RPM_BUILD_ROOT%{_lmsdir}/www/img/core/*
install img/*.gif $RPM_BUILD_ROOT%{_lmsdir}/www/img
install img/*.jpg $RPM_BUILD_ROOT%{_lmsdir}/www/img
install img/*.png $RPM_BUILD_ROOT%{_lmsdir}/www/img
install img/*.css $RPM_BUILD_ROOT%{_lmsdir}/www/img
install img/*.js $RPM_BUILD_ROOT%{_lmsdir}/www/img
install img/*.fdb $RPM_BUILD_ROOT%{_lmsdir}/www/img
cp -a doc/html $RPM_BUILD_ROOT%{_lmsdir}/www/doc
cp -a lib contrib modules templates sample $RPM_BUILD_ROOT%{_lmsdir}
install bin/* $RPM_BUILD_ROOT%{_sbindir}
cp -a smarty-plugins/* $RPM_BUILD_ROOT%{_smartyplugindir}

install sample/%{name}.ini $RPM_BUILD_ROOT%{_sysconfdir}

install -d $RPM_BUILD_ROOT%{_webapps}/%{_webapp}
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

# sqlpanel
install contrib/sqlpanel/sql.php $RPM_BUILD_ROOT%{_lmsdir}/modules
install contrib/sqlpanel/*.html $RPM_BUILD_ROOT%{_lmsdir}/templates

# user
cp -r contrib/customer/* $RPM_BUILD_ROOT%{_lmsdir}/www/user

# daemon
%if %{with lmsd}
install daemon/lmsd-* $RPM_BUILD_ROOT%{_sbindir}
install daemon/modules/*/*.so $RPM_BUILD_ROOT%{_libdir}/lms
cp -r daemon/modules/dns/sample $RPM_BUILD_ROOT%{_sysconfdir}/modules/dns
cp -r daemon/modules/ggnotify/sample $RPM_BUILD_ROOT%{_sysconfdir}/modules/ggnotify
cp -r daemon/modules/dns/sample $RPM_BUILD_ROOT%{_sysconfdir}/modules/nofity
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/lmsd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post lmsd
/sbin/chkconfig --add lmsd
%service lmsd restart "lmsd daemon"

%preun lmsd
if [ "$1" = "0" ]; then
	%service lmsd stop
	/sbin/chkconfig --del lmsd
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} <= 1.0.4
echo "WARNING!!!"
echo "_READ_ and upgrade LMS database:"
echo "MySQL: /usr/share/doc/%{name}-%{version}/UPGRADE-1.0-1.5.mysql.gz"
echo "PostgreSQL: /usr/share/doc/%{name}-%{version}/UPGRADE-1.0-1.5.pgsql.gz"

%triggerpostun -- %{name} <= 1.2.0
echo "BEWARE:"
echo "Automatic upgrade from LMS<= 1.2.0 is NO LONGER SUPPORTED by lms team"
echo "You are advised to upgrade it manually"
echo

%triggerpostun -- %{name} < 1.6.6-1.4
# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_webapps}/%{_webapp}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_webapps}/%{_webapp}/httpd.conf
fi

rm -f /etc/httpd/httpd.conf/99_%{name}.conf
/usr/sbin/webapp register httpd %{_webapp}
%service -q httpd reload

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,ChangeLog,INSTALL,README*,lms*}
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.ini
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%{_smartyplugindir}/*
#
%dir %{_lmsvar}
%attr(770,root,http) %{_lmsvar}/backups
%attr(770,root,http) %{_lmsvar}/templates_c
%attr(770,root,http) %{_lmsvar}/documents
#
%dir %{_lmsdir}
%{_lmsdir}/www
%exclude %{_lmsdir}/www/user
%{_lmsdir}/lib
%{_lmsdir}/modules
%exclude %{_lmsdir}/modules/sql.php
%{_lmsdir}/contrib
%dir %{_lmsdir}/sample
%{_lmsdir}/sample/crontab-entry
%{_lmsdir}/sample/lms-mgc-netx-sample.ini
%{_lmsdir}/sample/lms-mgc.ini
%{_lmsdir}/sample/lms.apache.conf
%{_lmsdir}/sample/lms.ini
%{_lmsdir}/sample/mailtemplate.txt
%{_lmsdir}/sample/mailtemplate_en.txt
%{_lmsdir}/sample/rc.lmsd
%{_lmsdir}/sample/rc.reminder_1st
%{_lmsdir}/sample/smstemplate.txt
%{_lmsdir}/sample/tekst_1.txt
%{_lmsdir}/sample/test.txt
%attr(755,root,root) %{_lmsdir}/sample/traffic_ipt.pl

%{_lmsdir}/templates
%exclude %{_lmsdir}/templates/sql.html
%exclude %{_lmsdir}/templates/sqlprint.html

%files scripts
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*

%files sqlpanel
%defattr(644,root,root,755)
%{_lmsdir}/modules/sql.php
%{_lmsdir}/templates/sql.html
%{_lmsdir}/templates/sqlprint.html

%files user
%defattr(644,root,root,755)
%{_lmsdir}/www/user

%if %{with lmsd}
%files lmsd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lmsd-*
%dir %{_libdir}/lms
%attr(755,root,root) %{_libdir}/lms/*.so
%attr(754,root,root) /etc/rc.d/init.d/lmsd
# XXX: dir shared with base
%dir %{_sysconfdir}
%dir %{_sysconfdir}/modules
%{_sysconfdir}/modules/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif
