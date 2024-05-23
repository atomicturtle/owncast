%global debug_package %{nil}

Name:           owncast
Version:        0.1.3
Release:        0.1%{?dist}
Summary:        Self-hosted live video and web chat server

License:        MIT
URL:            https://owncast.online
Source0:        https://github.com/owncast/owncast/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	owncast.service

BuildRequires:  golang
Requires:       glibc

%description
Owncast is a self-hosted live video and web chat server for use with existing popular broadcasting software.

%prep
%setup -q

%build
#export CGO_ENABLED=0
go build -ldflags "-buildid=owncast_build_id" -o %{name}


%install
install -d %{buildroot}%{_bindir}
install -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

install -d %{buildroot}/usr/lib/systemd/system/
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service

install -d %{buildroot}/var/lib/owncast

%pre
getent group owncast >/dev/null || groupadd -r owncast
getent passwd owncast >/dev/null || useradd -r -g owncast -d /var/lib/owncast -s /sbin/nologin -c "Owncast User" owncast
mkdir -p /var/lib/owncast
chown owncast:owncast /var/lib/owncast

%post
systemctl daemon-reload

%preun
if [ $1 -eq 0 ]; then
    systemctl stop owncast.service
    systemctl disable owncast.service
fi

%postun
if [ $1 -eq 0 ]; then
    userdel owncast
    groupdel owncast
    rm -rf /var/lib/owncast
    systemctl daemon-reload
fi


%files
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}.service



%changelog
* Wed May 22 2024 Your Name <scott@atomicrocketturtle.com> - 0.1.3-1
- Initial package for Owncast

