# TODO:
# - make it work without global_variables=On
%define		_pre	pre
%define		_rel	3
Summary:	A CRM for small to medium firms
Summary(pl.UTF-8):   CRM dla małych i średnich instytucji
Name:		ct-crm
Version:	1.6
Release:	0.%{_pre}.%{_rel}
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/customer-touch/%{name}%{version}%{_pre}.zip
# Source0-md5:	ffe5c4e7b183173832f4c1157a645e05
Source1:	%{name}-polish_lang
Source2:	%{name}.conf
Patch0:		%{name}-lang_pl.patch
Patch1:		%{name}-dbz.patch
Patch2:		%{name}-ne.patch
URL:		http://www.customer-touch.com/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	php(mysql)
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
An easy to use and install CRM for small to medium firms.

%description -l pl.UTF-8
Prosty w użyciu i instalacji CRM (Customer Relationship Management)
dla małych i średnich instytucji.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e '
	s#"config.inc.php"#"%{_sysconfdir}/config.inc.php"#
	s#"includes/config.inc.php"#"%{_sysconfdir}/config.inc.php"#
' *.php */*.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/{Doc/manual_install,languages/polish},/etc/httpd,%{_sysconfdir}}

for i in uploads modules languages includes images email; do
	cp -Rf $i $RPM_BUILD_ROOT%{_appdir}
done
install *.php *.js *.css $RPM_BUILD_ROOT%{_appdir}
cp -Rf Doc/manual_install/* $RPM_BUILD_ROOT%{_appdir}/Doc/manual_install

touch $RPM_BUILD_ROOT%{_sysconfdir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_appdir}/languages/polish/global.inc.php
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Doc/*.txt Doc/{CHANGELOG,README} Doc/manual_install/readme
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
%{_appdir}/*.css
%{_appdir}/[!^c]*.php
%{_appdir}/c[asu]*.php
%{_appdir}/*.js
%dir %{_appdir}/uploads
%dir %{_appdir}/modules
%{_appdir}/modules/mwhois
%dir %{_appdir}/languages
%{_appdir}/languages/*/global.inc.php
%dir %{_appdir}/includes
%{_appdir}/includes/*.php
%dir %{_appdir}/images
%{_appdir}/images/*.gif
%dir %{_appdir}/email
%{_appdir}/email/readme.txt
%dir %{_appdir}/Doc
%{_appdir}/Doc/manual_install
