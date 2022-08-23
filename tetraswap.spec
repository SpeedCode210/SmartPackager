%global __provides_exclude_from /*
%global __requires_exclude_from /*
Name:           tetraswap
Version:        1.3.2
Release:        1%{?dist}
Summary:        A simple but challengeous puzzle game !

License:        Proprietary
URL:            https://eclipium.xyz/tetraswap
Source0:        %{name}-%{version}.tar.gz

%description
A simple but challengeous puzzle game !

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}/TetraSwap
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
cp -r ./* $RPM_BUILD_ROOT/%{_bindir}/TetraSwap
mv $RPM_BUILD_ROOT/%{_bindir}/TetraSwap/TetraSwap.desktop $RPM_BUILD_ROOT/usr/share/applications/TetraSwap.desktop

%files
/usr/bin/TetraSwap/*
/usr/share/applications/TetraSwap.desktop
