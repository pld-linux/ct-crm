# TODO:
# - make it work without global_variables=On
Summary:	A CRM for small to medium firms
Summary(pl):	CRM dla ma³ych i ¶rednich instytucji
Name:		ct-crm
Version:	1.6
%define		_pre	pre
Release:	0.%{_pre}.2
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
BuildRequires:	unzip
Requires:	php-mysql
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cthtmldir	%{_datadir}/%{name}
%define		_configdir	/etc/%{name}

%description
An easy to use and install CRM for small to medium firms.

%description -l pl
Prosty w u¿yciu i instalacji CRM (Customer Relationship Management)
dla ma³ych i ¶rednich instytucji.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
for i in *.php; do
	cat $i | sed -e 's#\"config.inc.php\"#\"%{_configdir}/config.inc.php\"#' > $i.tmp
	mv -f $i.tmp $i
done
for i in */*.php; do
	cat $i | sed -e 's#\"config.inc.php\"#\"%{_configdir}/config.inc.php\"#' > $i.tmp
	mv -f $i.tmp $i
done
for i in *.php; do
	cat $i | sed -e 's#\"includes/config.inc.php\"#\"%{_configdir}/config.inc.php\"#' > $i.tmp
	mv -f $i.tmp $i
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_cthtmldir}/{Doc/manual_install,languages/polish},/etc/httpd,%{_configdir}}

for i in uploads modules languages includes images email ; do
	cp -Rf $i $RPM_BUILD_ROOT%{_cthtmldir}
done
install *.php *.js *.css $RPM_BUILD_ROOT%{_cthtmldir}
cp -Rf Doc/manual_install/* $RPM_BUILD_ROOT%{_cthtmldir}/Doc/manual_install

touch $RPM_BUILD_ROOT%{_configdir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_cthtmldir}/languages/polish/global.inc.php
install %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc Doc/*.txt Doc/{CHANGELOG,README} Doc/manual_install/readme
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%attr(750,root,http) %dir %{_configdir}
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_configdir}/config.inc.php
%dir %{_cthtmldir}
%{_cthtmldir}/*.css
%{_cthtmldir}/[!^c]*.php
%{_cthtmldir}/c[asu]*.php
%{_cthtmldir}/*.js
%dir %{_cthtmldir}/uploads
%dir %{_cthtmldir}/modules
%{_cthtmldir}/modules/mwhois
%dir %{_cthtmldir}/languages
%{_cthtmldir}/languages/*/global.inc.php
%dir %{_cthtmldir}/includes
%{_cthtmldir}/includes/*.php
%dir %{_cthtmldir}/images
%{_cthtmldir}/images/*.gif
%dir %{_cthtmldir}/email
%{_cthtmldir}/email/readme.txt
%dir %{_cthtmldir}/Doc
%{_cthtmldir}/Doc/manual_install
