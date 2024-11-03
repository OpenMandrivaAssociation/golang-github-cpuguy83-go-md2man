%global debug_package %{nil}

# Run tests in check section
%bcond_without check

# https://github.com/cpuguy83/go-md2man
%global goipath		github.com/cpuguy83/go-md2man
%global goaltipaths	github.com/cpuguy83/go-md2man/v2
%global forgeurl	https://github.com/cpuguy83/go-md2man
Version:			2.0.5

%gometa

%global goaltipaths	github.com/cpuguy83/go-md2man/v2

Summary:	Process markdown into manpages
Name:		golang-github-cpuguy83-go-md2man

Release:	1
Source0:	https://github.com/cpuguy83/go-md2man/archive/v%{version}/go-md2man-%{version}.tar.gz
URL:		https://github.com/cpuguy83/go-md2man
License:	MIT
Group:		Development/Other

BuildRequires:	compiler(go-compiler)
BuildRequires:  golang-ipath(github.com/russross/blackfriday/v2)

Provides:       go-md2man = %{version}-%{release}

%description
go-md2man is a golang tool using blackfriday to process markdown into
manpages.

%files
%license LICENSE.md
%doc README.md
%{_bindir}/go-md2man
%{_mandir}/man1/go-md2man.1*

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch
#Provides:	golang(github.com/cpuguy83/go-md2man/v2/md2man) = %{EVRD}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE.md
%doc README.md
#{_datadir}/gocode/src/%{goipath}/v2

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n go-md2man-%{version}

rm -fr vendor

%build
%gobuildroot
%gobuild -o _bin/go-md2man %{goipath}

# manpage
_bin/go-md2man -in=go-md2man.1.md -out=go-md2man.1

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

# install alternative name
ln -fs . %{buildroot}%{_datadir}/gocode/src/%{goaltipaths}
echo \"%{_datadir}/gocode/src/%{goaltipaths}\" >> devel.file-list

# binary
install -Dpm 0755 -d %{buildroot}%{_bindir}
install -Dpm 0755 _bin/go-md2man %{buildroot}%{_bindir}

# manpage
install -Dpm 0755 -d %{buildroot}%{_mandir}/man1
install -Dpm 0644 go-md2man.1 %{buildroot}%{_mandir}/man1

%check
%if %{with check}
%gochecks
%endif

