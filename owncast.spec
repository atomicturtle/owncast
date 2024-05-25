%global debug_package %{nil}

Name:           owncast
Version:        0.1.3
Release:        2%{?dist}
Summary:        Self-hosted live video and web chat server

License:        MIT
URL:            https://owncast.online
Source0:        https://github.com/owncast/owncast/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	owncast.service

BuildRequires:  golang
BuildRequires:  git
Requires:       glibc
Requires:	/usr/bin/ffmpeg

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
getent passwd owncast >/dev/null || \
	useradd -r -g owncast -d /var/lib/owncast -s /sbin/nologin \
	-c "Owncast User" owncast

%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
if [ $1 -eq 0 ]; then
    userdel owncast || :
    groupdel owncast || :
fi
%systemd_postun_with_restart %{name}.service


%files
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}.service
%attr(0755,owncast,owncast)  /var/lib/owncast



%changelog
* Sat May 25 2024 Your Name <scott@atomicrocketturtle.com> - 0.1.3-2
- Updates for better container support

* Wed May 22 2024 Your Name <scott@atomicrocketturtle.com> - 0.1.3-1
- Initial package for Owncast

