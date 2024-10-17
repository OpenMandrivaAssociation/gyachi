Version:	1.2.11
Summary:	A GTK+ based Yahoo! Chat client
Name:		gyachi
Release:	4
License:	GPLv2+
Group:		Networking/Instant messaging
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
source1:	.abf.yml
Patch0:		gyachi-1.1.71-disable_doc_install.patch
Patch1:		gyachi-1.1.71-fix-linkage.patch
Patch2:		gyachi-1.1.71-fix-str-fmt.patch
Patch3:		gyachi-1.1.71-fix-gpgme-build.patch
URL:		https://sourceforge.net/projects/gyachi/
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	gettext-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	jasper-devel
BuildRequires:	autoconf
BuildRequires:	expat-devel
BuildRequires:	gpgme-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	gtkhtml2-devel
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	gtkspell-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(libv4l2)
buildrequires:	pkgconfig(alsa)
buildrequires:	pkgconfig(openssl)

Obsoletes:	gyach <= 0.9.8
Provides:	gyach = %{version}
Suggests:	plugin-pulseaudio

%description
GyachI is a GTK+ based Yahoo! Chat client. It is a continuation of
Gyach Enhanced, which was itself a fork of Gyach. GyachI supports
almost all of the features you would expect to find on the official
Windows Yahoo! client: Voice chat, webcams, faders, 'nicknames',
audibles, avatars, display images, and more.

%package  	plugin-blowfish
Summary:	Blowfish encryption plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}

%description plugin-blowfish
%{summary}.

%package	plugin-gpgme
Summary:	GPGMe encryption plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}

%description plugin-gpgme
%{summary}.

%package	plugin-mcrypt
Summary:	MCrypt encryption plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}
      
%description plugin-mcrypt
%{summary}.

%package	plugin-photosharing
Summary:	Photo sharing plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}

%description plugin-photosharing
%{summary}.

%package	plugin-pulseaudio
Summary:	PulseAudio plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}

%description plugin-pulseaudio
%{summary}.

%package	plugin-gtkspell
Summary:	Spell check plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}

%description plugin-gtkspell
%{summary}.

%prep
%setup -q
%patch0 -p1 -b .doc
%patch1 -p0 -b .link
%patch2 -p0 -b .str
%patch3 -p1 -b .gpgme

perl -pi -e 's,%{name}.png,%{name},g' %{name}.desktop

%build
./autogen.sh
export CPPFLAGS='-D_FILE_OFFSET_BITS=64'
export LDFLAGS='-lm'
%configure2_5x \
%ifarch x86_64
	--disable-wine \
%endif
	--disable-rpath --enable-maintainer-mode \
	--disable-plugin_libnotify \
	--enable-plugin_photo_album
%make

%install
%makeinstall_std
desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-key="Encoding" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -m 644 -D themes/gyachi-classic/gyach-icon_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 -D themes/gyachi-classic/gyach-icon_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%find_lang %{name}

%files -f %{name}.lang
%defattr (-,root,root)
%doc ChangeLog
%doc doc/txt/gyachi-help-short.txt doc/txt/jasper-memory-leak.patch.txt doc/txt/webcams.txt doc/txt/README
%doc doc/html/gyachi-help.html doc/html/gyachi-ylinks.html doc/html/HOWTO-SIP.html
%{_bindir}/%{name}*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}-*
%{_libdir}/lib%{name}.so
%{_libdir}/%{name}/plugins/lib%{name}alsa.so
%{_datadir}/%{name}
%{_datadir}/applications/gyachi.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files plugin-blowfish
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}blowfish.so

%files plugin-gpgme
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}gpgme.so

%files plugin-mcrypt
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}mcrypt.so

%files plugin-photosharing
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}photos.so

%files plugin-pulseaudio
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}pulseaudio.so

%files plugin-gtkspell
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}gtkspell.so


%changelog
* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 1.2.10-3mdv2011.0
+ Revision: 661427
- update file list
- disable notify plugin
- rebuild

* Fri Apr 01 2011 Funda Wang <fwang@mandriva.org> 1.2.10-2
+ Revision: 649574
- fix build with latest kernel

* Sun Nov 28 2010 Funda Wang <fwang@mandriva.org> 1.2.10-1mdv2011.0
+ Revision: 602228
- new version 1.2.10

* Wed Jun 02 2010 Pascal Terjan <pterjan@mandriva.org> 1.2.4-3mdv2010.1
+ Revision: 546912
- Fix webcam support (#59603)

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 1.2.4-2mdv2010.1
+ Revision: 537369
- rebuild

* Sat Feb 13 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.2.4-1mdv2010.1
+ Revision: 505412
- update to 1.2.4

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 1.2.2-3mdv2010.1
+ Revision: 492238
- rebuild for new libjpeg v8

* Tue Nov 17 2009 Ahmad Samir <ahmadsamir@mandriva.org> 1.2.2-2mdv2010.1
+ Revision: 466920
- Really update to new version
- New version 1.2.2
- Fix gpgme configuration error by passing a CPPFLAGS

  + Pascal Terjan <pterjan@mandriva.org>
    - Fix build of gpgme plugin

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Funda Wang <fwang@mandriva.org>
    - New versino 1.1.71

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Dec 04 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.59-1mdv2009.1
+ Revision: 310076
- new version 1.1.59, update file lists &c

* Wed Oct 22 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.48-1mdv2009.1
+ Revision: 296606
- adjust file list for changes with new release
- add subpackage for pulse plugin
- have main package own plugins dir (previously nothing did)
- new path in source for icon
- use makeinstall_std (makeinstall no longer works)
- have to explicitly enable xmms and photo album plugins now
- suggest pulseaudio plugin
- new buildrequires: pulseaudio-devel and libnotify-devel
- enable x86_64 build and disable voice plugin build on x86-64 (now possible)
- rediff disable_doc_install.patch
- new release 1.1.48

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Dec 14 2007 Adam Williamson <awilliamson@mandriva.org> 1.1.0-1mdv2008.1
+ Revision: 120266
- buildrequires desktop-file-utils
- exclusivearch %%ix86 (voice part can't build on x86-64)
- buildrequires imagemagick
- BuildRequires gtkhtml2-devel
- import gyachi


