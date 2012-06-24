Summary:	LAN Managment System
Summary(pl):	System Zarz�dzania Siec� Lokaln�
Name:		lms
Version:	1.0pre10
Release:	0.1
License:	GPL
Vendor:		LMS Developers
Group:		Networking/Utilities
Source0:	http://lms.rulez.pl/download/%{name}-%{version}.tar.gz
# Source0-md5:	976fe1c627369c01e9868e326c11de09
Patch0:		%{name}-PLD.patch
URL:		http://lms.rulez.pl/
Requires:	php
Requires:	php-posix
Requires:	php-pcre
Requires:	webserver
Requires:	Smarty >= 2.5.0
Requires:	adodb >= 2.90
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_lmsdir		/home/services/httpd/html/%{name}
%define		_sharedstatedir	/var/lib
# when spec'll be finished, this sould go to RA-branch
# because sharedstatedir is already defined at rpm macros from HEAD

%description
This is a package of applications in PHP and Perl for managing LANs.
It's using MySQL (for now) but PostgreSQL will be supported in near
future. The main goal is to get the best service of users at
provider's level.
The main features in LMS are:
- database of users (name, surname, address, telefon number, 
  commentary);
- database of computers (IP, MAC);
- easy-ridden financial system and funds of network;
- different subscriptions;
- sending warnings to users;
- autogenerating dhcpd.conf;
- autogenerating firewall rules (ipchains/iptables);
- autogenerating idents for ident daemon;
- many levels of access for LMS administrators;
- integration with LinuxStat package;
- autogenerating ARP rules (ether auth);
- autogenerating DNS files.

%description -l pl
"LMS" jest skr�tem od "LAN Management System". Jest to zestaw
aplikacji w PHP i Perlu, u�atwiaj�cych zarz�dzanie sieciami
osiedlowymi (popularnie zwanymi Amatorskimi Sieciami Komputerowymi),
opartych o baz� danych MySQL (docelowo, do wyboru, MySQL lub
PostgreSQL). G��wne za�o�enia to uzyskanie jako�ci us�ug oraz obs�ugi
u�ytkownik�w na poziomie providera z prawdziwego zdarzenia.
Najbardziej podstawowe cechy LMS to:
- baza danych u�ytkownik�w (imi�, nazwisko, adres, numer telefonu,
  uwagi);
- baza danych komputer�w (adres IP, adres MAC);
- prowadzenie prostego rachunku operacji finansowych oraz stanu
  fundusz�w sieci;
- r�ne taryfy abonamentowe;
- wysy�anie poczt� elektroniczn� upomnie� do u�ytkownik�w;
- automatyczne naliczanie op�at miesi�cznych;
- generowanie dhcpd.conf;
- generowanie regu� firewalla (ipchains/iptables);
- generowanie ident�w dla demona oidentd;
- r�ne poziomy dost�pu do funkcji LMS dla administrator�w;
- integracja z pakietem LinuxStat;
- generowanie wpis�w ARP (blokada adres�w IP po ARP);
- generowanie wpis�w do DNS.

%package scripts
Summary:	LAN Managment System - scripts
Summary(pl):	LAN Managment System - skrypty
Requires:	perl-Net-SMTP-Server
Requires:	perl-Config-IniFiles
Requires:	perl-DBI
BuildArch:	noarch
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
ka�dy typ pliku konfiguracyjnego przy u�yciu lms-mgc.

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_lmsdir}/img
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/{backups,templates_c}
install -d $RPM_BUILD_ROOT%{_libexecdir}/%{name}/{lib,modules,templates}

install *.php $RPM_BUILD_ROOT%{_lmsdir}
install bin/* $RPM_BUILD_ROOT%{_bindir}
install lib/* $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lib
install img/* $RPM_BUILD_ROOT%{_lmsdir}/img
install modules/* $RPM_BUILD_ROOT%{_libexecdir}/%{name}/modules
install templates/* $RPM_BUILD_ROOT%{_libexecdir}/%{name}/templates
install sample/%{name}.ini $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* sample/*.ini sample/*txt sample/rc.reminder_1st sample/crontab-entry
%dir %{_lmsdir}
%dir %{_libexecdir}/%{name}
%dir %{_sharedstatedir}/%{name}
%attr(770,root,http) %{_sharedstatedir}/%{name}/templates_c
%attr(770,root,http) %{_sharedstatedir}/%{name}/backups
%{_lmsdir}/*.php
%{_lmsdir}/img
%{_libexecdir}/%{name}/lib
%{_libexecdir}/%{name}/modules
%{_libexecdir}/%{name}/templates
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/*.ini

%files scripts
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lms-*
%doc sample/*.ini
