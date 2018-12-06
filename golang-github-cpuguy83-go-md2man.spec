# https://github.com/cpuguy83/go-md2man
%global goipath         github.com/cpuguy83/go-md2man
Version:                1.0.8

%gometa

%if 0%{?fedora}
%bcond_with ignore_tests
%else
%bcond_without ignore_tests
%endif

Name:           golang-github-cpuguy83-go-md2man
Release:        2%{?dist}
Summary:        Process markdown into manpages
License:        MIT
URL:            %{gourl}
Source0:        %{gosource}
Source1:        glide.lock
Source2:        glide.yaml

Provides:       go-md2man = %{version}-%{release}

%description
go-md2man is a golang tool using blackfriday to process markdown into
manpages.

%package devel
Summary:        A golang registry for global request variables
BuildArch:      noarch

BuildRequires:  golang(gopkg.in/russross/blackfriday.v1)

%description devel
%{goipath} is a golang tool using blackfriday to process markdown into
manpages.

This package contains library source intended for building other packages
which use %{goipath}.

%prep
%forgesetup
cp %{SOURCE1} %{SOURCE2} .

# Replace blackfriday import path to avoid conflict with v2
sed -i 's|"github.com/russross/blackfriday|"gopkg.in/russross/blackfriday.v1|' $(find . -name '*.go')

%build
%gobuildroot
%gobuild -o _bin/go-md2man %{goipath}

%install
# install go-md2man binary
install -d %{buildroot}%{_bindir}
install -p -m 755 _bin/go-md2man %{buildroot}%{_bindir}
# generate man page
install -d -p %{buildroot}%{_mandir}/man1
_bin/go-md2man -in=go-md2man.1.md -out=go-md2man.1
install -p -m 644 go-md2man.1 %{buildroot}%{_mandir}/man1

%goinstall glide.lock glide.yaml

%if %{without ignore_tests}
%check
%gochecks
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE.md
%doc README.md
%{_bindir}/go-md2man
%{_mandir}/man1/go-md2man.1*

%files devel -f devel.file-list
%license LICENSE.md
%doc README.md

%changelog
* Thu Oct 25 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.8-2
- Replace blackfriday import path

* Thu Oct 25 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.0.8-1
- Update to release v1.0.8

* Tue Oct 23 2018 Nicolas Mailhot <nim@fedoraproject.org> - 1.0.7-9
- redhat-rpm-config-123 triggers bugs in gosetup, remove it from Go spec files as it’s just an alias
- https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/RWD5YATAYAFWKIDZBB7EB6N5DAO4ZKFM/

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.0.7-8
- Rebuild with fixed binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-7.20180312git1d903dc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 09 2018 Jan Chaloupka <jchaloup@redhat.com> - 1.0.7-6.20180312git1d903dc
- Upload glide file

* Wed Mar 07 2018 Jan Chaloupka <jchaloup@redhat.com> - 1.0.7-5.git1d903dc
- Fix go vet warning: Fatal -> Fatalf

* Wed Feb 28 2018 Jan Chaloupka <jchaloup@redhat.com>
- Autogenerate some parts using the new macros

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.7-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 19 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.0.7-1
- Bump to upstream 1d903dcb749992f3741d744c0f8376b4bd7eb3e1
  related: #1222796

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.0.4-7
- Bump to upstream a65d4d2de4d5f7c74868dfa9b202a3c8be315aaa
  related: #1222796

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- https://fedoraproject.org/wiki/Changes/golang1.7

* Sun Mar 06 2016 jchaloup <jchaloup@redhat.com> - 1.0.4-4
- Update list of provided packages
  resolves: #1222796

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 jchaloup <jchaloup@redhat.com> - 1.0.4-1
- Rebase to 1.0.4
  resolves: #1291379

* Thu Sep 10 2015 jchaloup <jchaloup@redhat.com> - 1-13
- Generate man page as well
  related: #1222796

* Sun Aug 30 2015 jchaloup <jchaloup@redhat.com> - 1-12
- Change deps on compiler(go-compiler)
- Update %%build, %%test and main section accordingaly
  related: #1222796

* Sat Aug 29 2015 jchaloup <jchaloup@redhat.com> - 1-11
- Reduce build section after update of go-srpm-macros
- BUILD_ID for debug is needed only for golang compiler
  related: #1222796

* Tue Aug 25 2015 jchaloup <jchaloup@redhat.com> - 1-10
- Provide devel package on rhel7
  related: #1222796

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-9
- Update spec file to spec-2.0
  related: #1222796

* Mon Jul 20 2015 jchaloup <jchaloup@redhat.com> - 1-8
- Add with_* macros

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 jchaloup <jchaloup@redhat.com> - 1-6
- Remove runtime deps of devel on golang
- Polish spec file
  related: #1222796

* Sun May 17 2015 jchaloup <jchaloup@redhat.com> - 1-5
- Add debug info
- Add license
- Update spec file to build on secondary architectures as well
  related: #1222796

* Wed Feb 25 2015 jchaloup <jchaloup@redhat.com> - 1-4
- Bump to upstream 2831f11f66ff4008f10e2cd7ed9a85e3d3fc2bed
  related: #1156492

* Wed Feb 25 2015 jchaloup <jchaloup@redhat.com> - 1-3
- Add commit and shortcommit global variable
  related: #1156492

* Mon Oct 27 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1-2
- Resolves: rhbz#1156492 - initial fedora upload
- quiet setup
- no test files, disable check

* Thu Sep 11 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1-1
- Initial package
