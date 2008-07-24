Version: 	1.1.0
Summary: 	A GTK+ based Yahoo! Chat client
Name: 		gyachi
Release: 	%mkrel 3
License: 	GPLv2+
Group: 		Networking/Instant messaging
Source0: 	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		gyachi-1.1.0-disable_doc_install.patch
URL: 		http://gyachi.sourceforge.net
BuildRoot: 	%{_tmppath}/%{name}-buildroot
# Voice part is 32-bit only according to upstream, can't see any way
# to disable voice but build the rest of the app - AdamW 2007/12
ExclusiveArch:	%{ix86}
BuildRequires:  gtk+2-devel
BuildRequires:	gettext-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	jasper-devel
BuildRequires:	autoconf
BuildRequires:	expat-devel
BuildRequires:	gpgme-devel
BuildRequires:  libmcrypt-devel
BuildRequires:  xmms-devel
BuildRequires:	gtkhtml2-devel
BuildRequires:	ImageMagick
BuildRequires:	desktop-file-utils

Obsoletes:	gyach <= 0.9.8
Provides:	gyach = %{version}

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

%package	plugin-xmms
Summary:	XMMS plugin for GyachI
Group:		Networking/Instant messaging
Requires:	%{name} >= %{version}
Requires:	xmms

%description plugin-xmms
%{summary}.

%prep
%setup -q
%patch0 -p1 -b .doc

perl -pi -e 's,%{name}.png,%{name},g' %{name}.desktop

%build
./autogen.sh
%configure2_5x --disable-rpath --enable-maintainer-mode --enable-v4l2
%make

%install
rm -rf %{buildroot}
%makeinstall
desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-key="Encoding" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -m 644 -D pixmaps/gyach-icon_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 -D pixmaps/gyach-icon_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

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
%{_libdir}/%{name}-*
%{_datadir}/%{name}
%{_datadir}/applications/gyachi.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files plugin-blowfish
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/%{name}blowfish.so

%files plugin-gpgme
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/%{name}gpgme.so

%files plugin-mcrypt
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/%{name}mcrypt.so

%files plugin-photosharing
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/%{name}photos.so

%files plugin-xmms
%defattr(-, root, root, 0775)
%{_libdir}/%{name}/plugins/%{name}xmms.so
