%global debug_package %{nil}

Name:           owncast
Version:        0.2.3
Release:        1%{?dist}
Summary:        Self-hosted live video and web chat server

License:        MIT
URL:            https://owncast.online
Source0:        https://github.com/owncast/owncast/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	owncast.service
Source2:	owncast.sysusers

BuildRequires:  golang
BuildRequires:  git
BuildRequires:  systemd-rpm-macros
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
install -d -m 0755 %{buildroot}/%{_sysusersdir}
install -m 0644 %{SOURCE2} %{buildroot}/%{_sysusersdir}/%{name}.conf
install -d %{buildroot}/var/lib/owncast


# docs
install -d -m 0755 %{buildroot}/usr/share/doc/%{name}/
install -m 0644 LICENSE %{buildroot}/usr/share/doc/%{name}/
install -m 0644 README.md %{buildroot}/usr/share/doc/%{name}/
install -m 0644 docs/*.md %{buildroot}/usr/share/doc/%{name}/

%pre
%if 0%{?fedora} || 0%{?rhel} >= 9
%sysusers_create_compat %{SOURCE2}
%else
getent group owncast >/dev/null || groupadd -r owncast
getent passwd owncast >/dev/null || \
	useradd -r -g owncast -d /var/lib/owncast -s /sbin/nologin \
	-c "Owncast" owncast
%endif

%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files
%doc README.md LICENSE
%doc backend.md DESIGN.md product-definition.md Release.md SECURITY.md
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}.service
%attr(0755,owncast,owncast)  /var/lib/owncast
%{_sysusersdir}/owncast.conf




%changelog
* Tue Dec 30 2025 Scott R. Shinn <scott@atomicrocketturtle.com> - 0.2.3-1
- Update to version 0.2.3
- Includes v0.2.0: Backend refactor, admin password hashing, profanity filter
- Includes v0.2.1: Bugfix release
- Includes v0.2.2: Translation support, updated codec support
- Includes v0.2.3: Bug fixes for Prometheus metrics, FediAuth, and private Federation

* Sat May 25 2024 Scott R. Shinn <scott@atomicrocketturtle.com> - 0.1.3-3
- adding documentation 

* Sat May 25 2024 Scott R. Shinn <scott@atomicrocketturtle.com> - 0.1.3-2
- Updates for better container support

* Wed May 22 2024 Scott R. Shinn <scott@atomicrocketturtle.com> - 0.1.3-1
- Initial package for Owncast

