#
# Conditional build:
%bcond_without	almsd		# without almsd daemon
#
# TODO:
# - fix lms-amd64.patch
# - almsd description
# - cosmetics (sort in %%files and %%install)
Summary:	LAN Managment System
Summary(pl):	System Zarz±dzania Sieci± Lokaln±
Name:		lms
Version:	1.5.0
Release:	0.6
License:	GPL
Vendor:		LMS Developers
Group:		Networking/Utilities
Source0:	http://lms.rulez.pl/download/devel/%{name}-%{version}.tar.gz
# Source0-md5:	2775bd6d1a962bc289b73b224100b7ed
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:         %{name}-PLD.patch
Patch1:		%{name}-amd64.patch
URL:		http://lms.rulez.pl/
%{?with_almsd:BuildRequires:	libgadu-devel}
%{?with_almsd:BuildRequires:	mysql-devel}
%{?with_almsd:BuildRequires:	postgresql-devel}
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
"LMS" jest skrótem od "LAN Management System". Jest to zestaw
aplikacji w PHP i Perlu, u³atwiaj±cych zarz±dzanie sieciami
osiedlowymi (popularnie zwanymi Amatorskimi Sieciami Komputerowymi),
opartych o bazê danych MySQL lub PostgreSQL. G³ówne za³o¿enia to 
uzyskanie jako¶ci us³ug oraz obs³ugi u¿ytkowników na poziomie 
providera z prawdziwego zdarzenia. 
Najbardziej podstawowe cechy LMS to:
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
  danych w bazie przy u¿yciu prostych szablonów;

%package scripts
Summary:	LAN Managment System - scripts
Summary(pl):	LAN Managment System - skrypty
Group:		Networking/Utilities
Requires:	perl-Net-SMTP-Server
Requires:	perl-Config-IniFiles
Requires:	perl-DBI

%description scripts
This package contains scripts to integrate LMS with your system,
monthly billing, notify users about their debts and cutting off
customers. Also you can build propably any kind of config file using
lms-mgc.

%description scripts -l pl
Ten pakiet zawiera skrypty do zintegrowania LMS z systemem, naliczania
comiesiêcznych op³at, powiadamiania u¿ytkowników o ich zad³u¿eniu oraz
ich automagicznego od³±czania. Mo¿esz tak¿e zbudowaæ prawdopodobnie
ka¿dy typ pliku konfiguracyjnego przy u¿yciu lms-mgc;

%package sqlpanel
Summary:	LAN Managment System - sqlpanel module
Summary(pl):	LAN Managment System - modu³ sqlpanel
Group:		Networking/Utilities
Requires:	%{name}

%description sqlpanel
SQL-panel module allows you to execute SQL queries and directly modify data.

%description sqlpanel -l pl
Modu³ 'SQL - panel' daje mo¿liwo¶æ bezpo¶redniego dostêpu
do bazy danych poprzez zadawanie zapytañ SQL. Wyniki wy¶wietlane s±
w formie tabeli. Ponadto podawany jest czas wykonania zapytania.

%package user
Summary:	LAN Managment System - simple user interface
Summary(pl):	LAN Managment System - prosty interfejs u¿ytkownika
Group:		Networking/Utilities
Requires:	%{name}

%description user
Simple user interface.

%description user -l pl
Prosty interfejs u¿ytkownika.

%package almsd
Summary:	LAN Managment System - almsd
Group:		Networking/Utilities
Requires:	%{name}

%description almsd
TODO

%prep
%setup -q -n %{name}
%patch0 -p1
%ifarch amd64
%patch1 -p1
%endif

%build
%if %{with almsd}

cd daemon

./configure --with-mysql
make \
	CC='%{__cc}' CFLAGS='%{rpmcflags} -DUSE_MYSQL -I../..'
mv almsd almsd-mysql

rm db.o

./configure --with-pgsql
make almsd \
	CC='%{__cc}' \
	CFLAGS='%{rpmcflags} -DUSE_PGSQL -I../..'
mv almsd almsd-pgsql

cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir} \
           $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,httpd,lms} \
           $RPM_BUILD_ROOT{%{_lmsvar}/{backups,templates_c},/usr/lib/lms} \
	   $RPM_BUILD_ROOT%{_lmsdir}/www/{img,doc,user}
	   
install *.php $RPM_BUILD_ROOT%{_lmsdir}/www
install img/* $RPM_BUILD_ROOT%{_lmsdir}/www/img
cp -r doc/html $RPM_BUILD_ROOT%{_lmsdir}/www/doc
cp -r lib config_templates modules templates $RPM_BUILD_ROOT%{_lmsdir}
install bin/* $RPM_BUILD_ROOT%{_sbindir}

install sample/%{name}.ini $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

# sqlpanel
install contrib/sqlpanel/sql.php $RPM_BUILD_ROOT%{_lmsdir}/modules
install contrib/sqlpanel/*.html $RPM_BUILD_ROOT%{_lmsdir}/templates

# user
install contrib/customer/* $RPM_BUILD_ROOT%{_lmsdir}/www/user

# daemon
%if %{with almsd}
install daemon/almsd-* $RPM_BUILD_ROOT%{_sbindir}
install daemon/modules/*/*.so $RPM_BUILD_ROOT/usr/lib/lms
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
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

%triggerpostun -- %{name} <= 1.0.4
echo "WARNING!!!"
echo "_READ_ and upgrade LMS database:"
echo "MySQL: /usr/share/doc/%{name}-%{version}/UPGRADE-1.0-1.5.mysql.gz"
echo "PostgreSQL: /usr/share/doc/%{name}-%{version}/UPGRADE-1.0-1.5.pgsql.gz"
echo

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,ChangeLog*,README,TODO,UPGRADE*,lms*}
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.ini
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
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
%{_lmsdir}/config_templates
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

%if %{with almsd}
%files almsd
%defattr(644,root,root,755)
#%dir /usr/lib/lms
%attr(755,root,root) %{_sbindir}/almsd-*
%attr(755,root,root) /usr/lib/lms/*.so
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif
