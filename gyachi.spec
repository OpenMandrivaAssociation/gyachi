Version: 	1.1.71
Summary: 	A GTK+ based Yahoo! Chat client
Name: 		gyachi
Release: 	%mkrel 2
License: 	GPLv2+
Group: 		Networking/Instant messaging
Source0: 	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		gyachi-1.1.71-disable_doc_install.patch
Patch1:		gyachi-1.1.71-fix-linkage.patch
Patch2:		gyachi-1.1.71-fix-str-fmt.patch
Patch3:		gyachi-1.1.71-fix-gpgme-build.patch
URL: 		http://gyachi.sourceforge.net
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:  gtk+2-devel
BuildRequires:	gettext-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	jasper-devel
BuildRequires:	autoconf
BuildRequires:	expat-devel
BuildRequires:	gpgme-devel
BuildRequires:  libmcrypt-devel
BuildRequires:  xmms-devel
BuildRequires:	gtkhtml2-devel
BuildRequires:	libnotify-devel
BuildRequires:	gtkspell-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils

Obsoletes:	gyach <= 0.9.8
Provides:	gyach = %{version}
Suggests:	plugin-pulseaudio

%description
GyachI is a GTK+ based Yahoo! Chat client. It is a continuation of
Gyach Enhanced, which was itself a fork of Gyach. GyachI supports
almost all of the features you would expect to find on the official
Windows Yahoo! client: Voice chat, webcams, faders, 'nicknames',
audibles, avatars, display images, and more.

%package	plugin-blowfish
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

%package	plugin-xmms
Summary:	XMMS plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}
Requires:	xmms

%description plugin-xmms
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
%configure2_5x \
%ifarch x86_64
	--disable-wine \
%endif
	--disable-rpath --enable-maintainer-mode \
	--enable-plugin_photo_album --enable-plugin_xmms \
	CPPFLAGS='-D_FILE_OFFSET_BITS=64'
%make

%install
rm -rf %{buildroot}
%makeinstall_std
desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-key="Encoding" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -m 644 -D themes/gyachi-classic/gyach-icon_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 -D themes/gyachi-classic/gyach-icon_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# don't think these are any use for anything, if they are, we can
# re-add them in -devel packages - AdamW 2008/12
rm -f %{buildroot}%{_libdir}/%{name}/plugins/*.la
rm -f %{buildroot}%{_libdir}/libgyachi.la

%find_lang %{name}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif
 
%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

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
%{_libdir}/%{name}/plugins/lib%{name}libnotify.so
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

%files plugin-xmms
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}xmms.so

%files plugin-gtkspell
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/lib%{name}gtkspell.so
