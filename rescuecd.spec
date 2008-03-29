# TODO:
# - more verbose description
# - pl description and summary
Summary:	PLD RescueCD
Name:		rescuecd
Version:	2.95
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86/RCDx86_%(echo %{version} | tr -d .).iso
# Source0-md5:	84b9a3917a16c5148f881b33f92ca446
Source1:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86/rcdmod.x86
# Source1-md5:	d712792e3216e49aec85bf5046d1e212
Source2:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86_64/RCDx64_%(echo %{version} | tr -d .).iso
# Source2-md5:	91567cb34cbe73130df7a41dd7987ca3
Source3:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86_64/rcdmod.x64
# Source3-md5:	5d89cd4d8b6ff135da5d9ae9a2c0e5b8
Source4:	%{name}.image
URL:		http://rescuecd.pld-linux.org/
BuildRequires:	/usr/bin/isoinfo
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PLD RescueCD

%package -n rc-boot-image-rescuecd
Summary:	rescuecd image for rc-boot
Summary(pl.UTF-8):	Obraz rescuecd dla rc-boot
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	rc-boot

%description -n rc-boot-image-rescuecd
rescuecd image for rc-boot.

%description -n rc-boot-image-rescuecd -l pl.UTF-8
Obraz rescuecd dla rc-boot.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-boot/images
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rc-boot/images/%{name}

install -d $RPM_BUILD_ROOT/boot
%ifarch %{ix86}
isoinfo -R -i %{SOURCE0} -x /rescue.cpi > $RPM_BUILD_ROOT/boot/%{name}.initrd
isoinfo -R -i %{SOURCE0} -x /boot/isolinux/vmlinuz > $RPM_BUILD_ROOT/boot/%{name}.vmlinuz
%endif
%ifarch %{x8664}
isoinfo -R -i %{SOURCE2} -x /rescue6.cpi > $RPM_BUILD_ROOT/boot/%{name}.initrd
isoinfo -R -i %{SOURCE2} -x /boot/isolinux/vmlinuz6 > $RPM_BUILD_ROOT/boot/%{name}.vmlinuz
%endif

install -d $RPM_BUILD_ROOT%{_bindir}
%ifarch %{ix86}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}/rcdmod
%endif
%ifarch %{x8664}
install %{SOURCE3} $RPM_BUILD_ROOT/%{_bindir}/rcdmod
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%postun -n rc-boot-image-rescuecd
/sbin/rc-boot 1>&2 || :

%post -n rc-boot-image-rescuecd
/sbin/rc-boot 1>&2 || :

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rcdmod
/boot/%{name}.initrd
/boot/%{name}.vmlinuz

%files -n rc-boot-image-rescuecd
%defattr(644,root,root,755)
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-boot/images/%{name}
