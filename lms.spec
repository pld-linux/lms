# TODO
# - cosmetics (sort in %%files and %%install)
# - contrib split
#
# Conditional build:
%bcond_without	lmsd		# without lmsd daemon
%bcond_with	lmsd_debug	# with lmsd debugging

%define		lmsver		1.11
%define		lmssubver	13
Summary:	LAN Managment System
Summary(pl.UTF-8):	System Zarządzania Siecią Lokalną
Name:		lms
Version:	%{lmsver}.%{lmssubver}
Release:	2
License:	GPL v2
Group:		Networking/Utilities
Source0:	http://www.lms.org.pl/download/%{lmsver}/%{name}-%{version}.tar.gz
# Source0-md5:	294899358ae2585a4030580d79a06ee8
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
BuildRequires:	net-snmp-devel
%{?with_lmsd:BuildRequires:	postgresql-devel >= 8.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.461
BuildRequires:	yacc
%{?with_lmsd:Requires(post,preun):	/sbin/chkconfig}
Requires:	Smarty >= 2.6.18-2
Requires:	php(gd)
Requires:	php(iconv)
Requires:	php(mbstring)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(posix)
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_lmsdir		%{_datadir}/%{name}
%define		_lmsvar		/var/lib/%{name}
%define		_smartyplugindir	%{php_data_dir}/Smarty/plugins
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

%package userpanel
Summary:	LAN Managment System - Userpanel
Summary(pl.UTF-8):	System Zarządzania Siecią Lokalną - Panel Użytkownika
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description userpanel
Userpanel is automated virtual customer service, based on LMS and
using its core features. It enables customers (or it's intended to) to
do review their payments, change their personal details or computer
properties, modify subscriptions, submit problems, track their
requests on Helpdesk and print invoices. It means, it makes a closer
contact with their ISP.

%description userpanel -l pl.UTF-8
Userpanel jest opartą na szkielecie LMS (i ściśle z LMS
współpracującą) implementacją tzw. e-boku. Umożliwia (albo będzie
umożliwiał) klientom przeglądanie stanu swoich wpłat, zmianę swoich
danych osobowych, edycję właściwości swoich komputerów, zmianę taryf,
zgłaszanie błędów oraz awarii do Helpdesku, wydruk faktur oraz
formularza przelewu.

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
lib/Smarty/plugins/function.{bankaccount,gentime,handle,memory,number,size,sum,tip}.php \
lib/Smarty/plugins/modifier.{money_format,striphtml,to_words}.php \
	smarty-plugins
rm -rf lib/Smarty

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%if %{with lmsd}

cd daemon

./configure --with-mysql %{?with_lmsd_debug:--enable-debug0 --enable-debug1}
%{__make} \
	CC='%{__cc}' \
	CFLAGS='%{rpmcflags} -fPIC -DUSE_MYSQL -DLMS_LIB_DIR=\"%{_libdir}/lms/\" -I../..'
mv lmsd lmsd-mysql

./configure --with-pgsql %{?with_lmsd_debug:--enable-debug0 --enable-debug1}
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

#userpanel
install -d $RPM_BUILD_ROOT%{_lmsdir}/userpanel
install -d $RPM_BUILD_ROOT%{_lmsdir}/www/userpanel/modules
install -d $RPM_BUILD_ROOT%{_lmsvar}/userpanel/templates_c

cp -R {userpanel/lib,userpanel/modules,userpanel/templates}           $RPM_BUILD_ROOT%{_lmsdir}/userpanel
cp -R {userpanel/index.php,userpanel/style}                 $RPM_BUILD_ROOT%{_lmsdir}/www/userpanel
ln -s %{_lmsdir}/www/userpanel/style    $RPM_BUILD_ROOT%{_lmsdir}/userpanel
ln -s %{_lmsvar}/userpanel/templates_c  $RPM_BUILD_ROOT%{_lmsdir}/userpanel

for MODULE in $RPM_BUILD_ROOT%{_lmsdir}/userpanel/modules/*; do
    MODULE=$(basename $MODULE)
    mkdir $RPM_BUILD_ROOT%{_lmsdir}/www/userpanel/modules/$MODULE
    ln -s %{_lmsdir}/userpanel/modules/$MODULE/style    \
        $RPM_BUILD_ROOT%{_lmsdir}/www/userpanel/modules/$MODULE
done

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
%exclude %{_lmsdir}/www/userpanel
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
%{_lmsdir}/sample/radius-sql.conf
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

%files userpanel
%defattr(644,root,root,755)
%dir %{_lmsdir}/userpanel
%{_lmsdir}/userpanel/lib
%{_lmsdir}/userpanel/modules
%{_lmsdir}/userpanel/templates
%{_lmsdir}/userpanel/templates_c
%{_lmsdir}/userpanel/style
%dir %{_lmsdir}/www/userpanel
%{_lmsdir}/www/userpanel/style
%{_lmsdir}/www/userpanel/index.php
%dir %{_lmsvar}/userpanel
%attr(770,root,http) %{_lmsvar}/userpanel/templates_c
