# TODO:
# - more verbose description
Summary:	PLD RescueCD bootable from hard disk
Summary(pl.UTF-8):	PLD RescueCD w postaci uruchamialnej z dysku
Name:		rescuecd
Version:	11.02
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86/RCDx86_%(echo %{version} | tr . _).iso
# Source0-md5:	861bed4d650537606a4cb4f674c2974b
Source1:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86/rcdmod.x86
# Source1-md5:	ca584f61150394c39b500ecc7e08ebd2
Source2:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86_64/RCDx64_%(echo %{version} | tr . _).iso
# Source2-md5:	2ad7aab2cf131d9e99c75254d88d5ac9
Source3:	http://rescuecd.pld-linux.org/download/PLDRescueCD-%{version}/x86_64/rcdmod.x64
# Source3-md5:	9d74622095b809359abfdf9293a267db
Source4:	%{name}.image
URL:		http://rescuecd.pld-linux.org/
BuildRequires:	/usr/bin/isoinfo
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PLD RescueCD as files runable from bootloader.

%description -l pl.UTF-8
PLD RescueCD w postaci plików zdatnych do uruchomienia z poziomu
bootloadera.

%package -n rc-boot-image-rescuecd
Summary:	rescuecd image for rc-boot
Summary(pl.UTF-8):	Obraz rescuecd dla rc-boota
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	rc-boot

%description -n rc-boot-image-rescuecd
rescuecd image for rc-boot.

%description -n rc-boot-image-rescuecd -l pl.UTF-8
Obraz rescuecd dla rc-boota.

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
