%global varnishver %(pkg-config --silence-errors --modversion varnishapi || echo 0)
%global gittag 0.18.0

%if 0%{?rhel} == 7 || 0%{?rhel} == 6
%global docutils python34-docutils
%global rst2man rst2man-3.4
%else
%global docutils python3-docutils
%global rst2man rst2man
%endif

Name:    varnish-modules
Version: 0.18.0
Release: 1%{?dist}
Summary: A collection of modules ("vmods") extending Varnish VCL

License: BSD
URL:     https://github.com/varnish/varnish-modules
Source:  https://github.com/varnish/varnish-modules/archive/%{gittag}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(varnishapi)
BuildRequires: varnish

# Build from a git checkout
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: %docutils

Requires: varnish = %varnishver

Provides: vmod-bodyaccess = %{version}-%{release}
Provides: vmod-header = %{version}-%{release}
Provides: vmod-saintmode = %{version}-%{release}
Provides: vmod-tcp = %{version}-%{release}
Provides: vmod-var = %{version}-%{release}
Provides: vmod-vsthrottle = %{version}-%{release}
Provides: vmod-xkey = %{version}-%{release}


%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods:
bodyaccess, header, saintmode, tcp, var, vsthrottle, xkey


%prep
%autosetup -n %{name}-%{gittag}


%build
sh bootstrap
export RST2MAN=%{rst2man}
%configure 
%make_build


%install
%make_install docdir=%_pkgdocdir
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'
rm %{buildroot}%{_pkgdocdir}/LICENSE # Rather use license macro


%check
%ifarch %ix86 %arm ppc
# 64-bit specific test
sed -i 's,tests/xkey/test12.vtc,,' src/Makefile
%endif
%make_build check VERBOSE=1


%files
#doc docs AUTHORS CHANGES.rst COPYING README.rst
%doc AUTHORS CHANGES.rst COPYING README.md
%license LICENSE
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*


%changelog
* Mon Feb 21 2022 Luboš Uhliarik <luhliari@redhat.com> - 0.18.0-1
- Resolves: #2056622 - rebase varnish-modules to 18.0
- new version 18.0

* Thu Aug 19 2021 Luboš Uhliarik <luhliari@redhat.com> - 0.17.1-6
- Resolves: #1995450 - rebuild

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 0.17.1-5
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue Jul 27 2021 Luboš Uhliarik <luhliari@redhat.com> - 0.17.1-4
- Resolves: #1986346 - Rebase varnish-modules to the latest release
- Rebuild for varnish 6.5.2

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.17.1-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Mar 17 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> 0.17.1-1
- New upstream release
- Switched back to original varnish github upstream, as it has catched up
- Includes fix for CVE-2021-28543, VSV00006, bz#1939669

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-0.3.klarlack.20200916git4d6593c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 29 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.17.0-0.2.klarlack.20200916git
- Rebuilt for varnish-6.5.1

* Wed Sep 16 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.17.0-0.1.klarlack.20200916git
- Switched upstream to Nils Goroll's fork which is the defacto current upstream
- Synced description to reality
- This is a snapshot build that needs autotools for building
- Rebuilt for varnish-6.5.0

* Mon Aug 17 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.16.0-3
- Rebuilt for varnish-6.4.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Mar 28 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.16.0-1
- New upstream release

* Tue Mar 17 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.16.0-0.1.20200317git21d0c84
- Snapshot from 6.4 branch, rebuilt against varnish-6.4.0
- Removed patches merged upstream
- Delete 64-bit specific test on 32-bit arches

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 29 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-7
- Added patch from Nils Goroll, compatibility for varnish-6.3, closes bz#1736943
- Rebuilt against varnish-6.3.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-5
- Install docs in correct docdir

* Fri Feb 15 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-4
- Added a simple patch from upstream, fixing a formatting bug trigged on 32bit
- Removed dependency on docutils. It is not necessary on released tarballs

* Thu Feb 14 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 0.15.0-3
- Added a proposed patch from Nils Goroll providing support for vmod_saintmode
  on varnish-6.1.1 (closes rhbz #1676183)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Dridi Boukelmoune <dridi@fedoraproject.org> 0.15.0-1
- Update to 0.15.0
- Drop EPEL and older Fedora releases support
- Drop broken manual ABI dependency to Varnish
- Drop commented out references to past patches
- Verbose test suite
- Simplified configure step
- Dependencies cleanup

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 21 2017 Dridi Boukelmoune <dridi@fedoraproject.org> 0.12.1-5
- Update varnishabi requirement for f28

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
