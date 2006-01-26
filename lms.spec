# TODO
# - test build on amd64 and sheck /usr/lib64 patch
# - cosmetics (sort in %%files and %%install)
# - contrib split
#
# Conditional build:
%bcond_without	lmsd		# without lmsd daemon
#
%define		lmsver		1.6
%define		lmssubver	6
Summary:	LAN Managment System
Summary(pl):	System Zarz±dzania Sieci± Lokaln±
Name:		lms
Version:	%{lmsver}.%{lmssubver}
Release:	1.1
License:	GPL
Vendor:		LMS Developers
Group:		Networking/Utilities
Source0:	http://lms.rulez.pl/download/%{lmsver}/%{name}-%{version}.tar.gz
# Source0-md5:	8500349fc938d66504dca033abc3a5f5
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-amd64.patch
URL:		http://lms.rulez.pl/
%{?with_lmsd:BuildRequires:	libgadu-devel}
%{?with_lmsd:BuildRequires:	mysql-devel}
%{?with_lmsd:BuildRequires:	postgresql-devel}
%{?with_lmsd:Requires(post,preun):	/sbin/chkconfig}
Requires:	Smarty >= 2.5.0
Requires:	php
Requires:	php-gd
Requires:	php-iconv
Requires:	php-pcre
Requires:	php-posix
%{?with_lmsd:Requires: rc-scripts}
Requires:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_lmsdir		%{_datadir}/%{name}
%define		_lmsvar		/var/lib/%{name}

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

%description -l pl
"LMS" jest skrótem od "LAN Management System". Jest to zestaw
aplikacji w PHP i Perlu, u³atwiaj±cych zarz±dzanie sieciami
osiedlowymi (popularnie zwanymi Amatorskimi Sieciami Komputerowymi),
opartych o bazê danych MySQL lub PostgreSQL. G³ówne za³o¿enia to
uzyskanie jako¶ci us³ug oraz obs³ugi u¿ytkowników na poziomie
providera z prawdziwego zdarzenia. Najbardziej podstawowe cechy LMS
to:
- baza danych u¿ytkowników (imiê, nazwisko, adres, numer telefonu,
  uwagi);
- baza danych komputerów (adres IP, adres MAC);
- prowadzenie prostego rachunku operacji finansowych oraz stanu
  funduszów sieci;
- ró¿ne taryfy abonamentowe;
- wysy³anie poczt± elektroniczn± upomnieñ do u¿ytkowników;
- automatyczne naliczanie op³at miesiêcznych;
- ró¿ne poziomy dostêpu do funkcji LMS dla administratorów;
- generowanie regu³ i plików konfiguracyjnych dla ipchains, iptables,
  dhcpd, oidentd, packet filtra openbsd, wpisów /etc/ethers
- generowanie praktycznie ka¿dego pliku konfiguracyjnego na podstawie
  danych w bazie przy u¿yciu prostych szablonów.

%package scripts
Summary:	LAN Managment System - scripts
Summary(pl):	LAN Managment System - skrypty
Group:		Networking/Utilities
Requires:	perl-Config-IniFiles
Requires:	perl-DBI
Requires:	perl-Net-SMTP-Server

%description scripts
This package contains scripts to integrate LMS with your system,
monthly billing, notify users about their debts and cutting off
customers. Also you can build probably any kind of config file using
lms-mgc.

%description scripts -l pl
Ten pakiet zawiera skrypty do zintegrowania LMS z systemem, naliczania
comiesiêcznych op³at, powiadamiania u¿ytkowników o ich zad³u¿eniu oraz
ich automagicznego od³±czania. Mo¿esz tak¿e zbudowaæ prawdopodobnie
ka¿dy typ pliku konfiguracyjnego przy u¿yciu lms-mgc.

%package sqlpanel
Summary:	LAN Managment System - sqlpanel module
Summary(pl):	LAN Managment System - modu³ sqlpanel
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description sqlpanel
SQL-panel module allows you to execute SQL queries and directly modify
data.

%description sqlpanel -l pl
Modu³ 'SQL - panel' daje mo¿liwo¶æ bezpo¶redniego dostêpu do bazy
danych poprzez zadawanie zapytañ SQL. Wyniki wy¶wietlane s± w formie
tabeli. Ponadto podawany jest czas wykonania zapytania.

%package user
Summary:	LAN Managment System - simple user interface
Summary(pl):	LAN Managment System - prosty interfejs u¿ytkownika
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description user
Simple user interface.

%description user -l pl
Prosty interfejs u¿ytkownika.

%package lmsd
Summary:	LAN Managment System - LMS system backend
Summary(pl):	LAN Managment System - backend systemu LMS
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lms-almsd

%description lmsd
A program to manage the server by creating configuration files based
upon LMS database and restarting selected services.

%description lmsd -l pl
Program zarz±dzaj±cy serwerem poprzez tworzenie plików
konfiguracyjnych na podstawie bazy danych LMS'a i restartowanie
wybranych us³ug.

%prep
%setup -q -n %{name}
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

%build
%if %{with lmsd}

cd daemon

./configure --with-mysql
%{__make} \
	CC='%{__cc}' CFLAGS='%{rpmcflags} -fPIC -DUSE_MYSQL -DLMS_LIB_DIR=\"%{_libdir}/lms/\" -I../..'
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
	   $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,httpd} \
	   $RPM_BUILD_ROOT/etc/lms/modules/{dns,ggnofity,nofity} \
	   $RPM_BUILD_ROOT{%{_lmsvar}/{backups,templates_c},%{_libdir}/lms} \
	   $RPM_BUILD_ROOT%{_lmsdir}/www/{img,doc,user}

install *.php $RPM_BUILD_ROOT%{_lmsdir}/www
install img/* $RPM_BUILD_ROOT%{_lmsdir}/www/img
cp -r doc/html $RPM_BUILD_ROOT%{_lmsdir}/www/doc
cp -r lib contrib modules templates sample $RPM_BUILD_ROOT%{_lmsdir}
install bin/* $RPM_BUILD_ROOT%{_sbindir}

install sample/%{name}.ini $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

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

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%post lmsd
/sbin/chkconfig --add lmsd
if [ -f /var/lock/subsys/lmsd ]; then
	/etc/rc.d/init.d/lmsd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/lmsd start\" to start lmsd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun lmsd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/lmsd ]; then
		/etc/rc.d/init.d/lmsd stop >&2
	fi
	/sbin/chkconfig --del lmsd
fi

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

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,ChangeLog*,INSTALL,README,UPGRADE*,lms*}
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.ini
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
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
%{_lmsdir}/contrib
%{_lmsdir}/sample
%attr(755,root,root) %{_lmsdir}/sample/traffic_ipt.pl
%{_lmsdir}/templates
%exclude %{_lmsdir}/templates/sql.html
%exclude %{_lmsdir}/templates/sqlprint.html

%files scripts
%defattr(644,root,root,755)
%dir %{_sbindir}
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
%attr(755,root,root) %{_libdir}/lms/*.so
%attr(754,root,root) /etc/rc.d/init.d/lmsd
/etc/lms/modules/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif
