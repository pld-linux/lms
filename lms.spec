%define		_add pre5
Summary:	LAN Managment System
Summary(pl):	System Zarz±dzania Siec± Lokaln±
Name:		lms
Version:	1.0
Release:	0.2.%{_add}
License:	GPL
Group:		Networking/Utilities
Source0:	http://lms.rulez.pl/download/%{name}-%{version}%{_add}.tar.gz
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
Requires:	Smarty
Requires:	ADOdb
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_lmsdir	/home/services/httpd/html/%{name}

%description
This is a package of applications in PHP and Perl to managing LANs.
It's using MySQL (for now) but PostgreSQL will be supported in near
future. Main foundation is get the best service of users at
providiers level.
The main sign in LMS are:
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
- autogenerating DNS files;

%description -l pl
"LMS" jest skrótem od "LAN Management System". Jest to zestaw
aplikacji w PHP i Perlu, u³atwiaj±cych zarz±dzanie sieciami
osiedlowymi (popularnie zwanymi Amatorskimi Sieciami Komputerowymi),
opartych o bazê danych MySQL (docelowo, do wyboru, MySQL lub
PostgreSQL). G³ówne za³o¿enia to uzyskanie jako¶ci us³ug oraz obs³ugi
u¿ytkowników na poziomie providera z prawdziwego zdarzenia.
Najbardziej podstawowe cechy LMS to:
- baza danych u¿ytkowników (imiê, nazwisko, adres, numer telefonu,
  uwagi);
- baza danych komputerów (adres IP, adres MAC);
- prowadzenie prostego rachunku operacji finansowych oraz stanu
  funduszów sieci;
- ró¿ne taryfy abonamentowe;
- wysy³anie poczt± elektroniczn± upomnieñ do u¿ytkowników;
- automatyczne naliczanie op³at miesiêcznych;
- generowanie dhcpd.conf;
- generowanie regu³ firewalla (ipchains/iptables);
- generowanie identów dla demona oidentd;
- ró¿ne poziomy dostêpu do funkcji LMS dla administratorów;
- integracja z pakietem LinuxStat;
- generowanie wpisów ARP (blokada adresów IP po ARP);
- generowanie wpisów do DNS;

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
