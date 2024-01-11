%define abi 6.1

%bcond_without python2
%bcond_with python3

%if %{with python2} == %{with python3}
%error Pick exactly one Python version
%endif

Name:    varnish-modules
Version: 0.15.0
Release: 6%{?dist}
Summary: A collection of modules ("vmods") extending Varnish VCL

Group:   System Environment/Daemons
License: BSD
URL:     https://github.com/varnish/%{name}

Source: https://download.varnish-software.com/varnish-modules/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch1: varnish-modules-0.15.0-vmod-tcp-int.patch

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish

%if %{with python3}
BuildRequires: python3-docutils
BuildRequires: python3-devel
%define rst2man %{_bindir}/rst2man
%define vpython %{_bindir}/python3
%else
BuildRequires: python-docutils
BuildRequires: python2-devel
%define rst2man %{_bindir}/rst2man
%define vpython %{_bindir}/python2
%endif

Requires: varnish

Provides: vmod-bodyaccess = %{version}-%{release}
Provides: vmod-cookie = %{version}-%{release}
Provides: vmod-header = %{version}-%{release}
Provides: vmod-saintmode = %{version}-%{release}
Provides: vmod-tcp = %{version}-%{release}
Provides: vmod-var = %{version}-%{release}
Provides: vmod-vsthrottle = %{version}-%{release}
Provides: vmod-xkey = %{version}-%{release}


%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods (previously
kept individually): cookie, vsthrottle, header, saintmode, softpurge,
tcp, var, xkey


%prep
%setup -q

%patch1 -p1 -b .vmod-tcp-int

%build
%configure
%make_build


%install
%make_install
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'


%check
make check VERBOSE=1


%files
%doc docs AUTHORS CHANGES.rst COPYING README.rst LICENSE
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*
%{_pkgdocdir}


%changelog
* Mon Jul 26 2021 Luboš Uhliarik <luhliari@redhat.com> - 0.15.0-6
- Related: #1982862 - rebuild for new varnish version

* Thu Apr 16 2020 Lubos Uhliarik <luhliari@redhat.com> - 0.15.0-5
- Related: #1795673 - RFE: rebase varnish:6 to latest 6.0.x LTS

* Mon Dec 03 2018 Lubos Uhliarik <luhliari@redhat.com> - 0.15.0-4
- Resolves: #1649358 - Unable to install varnish module

* Sun Aug 05 2018 Lubos Uhliarik <luhliari@redhat.com> - 0.15.0-2
- Fixed i686 build failure

* Sun Aug 05 2018 Lubos Uhliarik <luhliari@redhat.com> - 0.15.0-1
- updated to newer version (0.15.0)
- Drop EPEL and older Fedora releases support
- Drop broken manual ABI dependency to Varnish
- Drop commented out references to past patches
- Verbose test suite
- Simplified configure step
- Dependencies cleanup

* Tue Apr 24 2018 Luboš Uhliarik <luhliari@redhat.com> - 0.12.16
- use rst2man binary for both python2 and python3

* Mon Apr 16 2018 Joe Orton <jorton@redhat.com> - 0.12.1-4.4
- fix abi requires (#1566046)

* Thu Mar 29 2018 Joe Orton <jorton@redhat.com> - 0.12.1-4.2
- fix use of rst2man with python3-docutils

* Wed Mar 28 2018 Joe Orton <jorton@redhat.com> - 0.12.1-4.1
- add Python build conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.12.1-2
- Set correct varnishabi requirement for the different fedoras

* Wed May 31 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.12.1-1
- New uptream release
- Pull el5 support

* Mon Mar 20 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.11.0-1
- New upstream release

* Sat Sep 24 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.9.2-0.1.20160924gitdaa4f1d
- Upstream git checkout with support for varnish-5.0
- Removed patches that are included upstream
- el5 build fix

* Fri Aug 05 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.9.1-1
- New upstream release
- Build man pages, buildrequires python-docutils
- Added a patch for tests/cookie/08-overflow.vtc, upping workspace_client,
  the default is too small on 32bit
- Removed extra cflags for el5, fixed with patch from upstream
- Force readable docs and debug files, they tend to end up with mode 600

* Tue Apr 05 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.9.0-1
- First wrap for fedora
- Uses some old-style specfile components for el5 compatibility, including
  the usage of the BuildRoot header and cleaning the buildroot before install


