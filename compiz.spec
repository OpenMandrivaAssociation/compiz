Name: compiz

%define major 0
%define libname %mklibname %{name} %major
%define libname_devel %mklibname -d %{name}

Version: 0.6.2
Release: %mkrel 5
Summary: OpenGL composite manager for Xgl and AIGLX
Group: System/X11
URL: http://www.go-compiz.org/
Source: http://xorg.freedesktop.org/archive/individual/app/%{name}-%{version}.tar.gz 
Source1: compiz.defaults
Source2: compiz-window-decorator
# Patches for AIGLX
# Thanks Kristian Høgsberg
# Patch1 updated by Johannes (Hanno) B�ck to automatically detect AIGLX
# http://svn.hboeck.de/xgl-overlay/x11-wm/compiz/files/compiz-tfp
Patch1: 0001-Also-check-for-tfp-in-server-extensions-rediff.txt
Patch2:	compiz-0.3.6-kde-mem-leak.patch
# Patches for Mandriva defaults
Patch3: compiz-default-plugins.patch
Patch4: compiz-mandriva-top.patch
Patch6: compiz-decoration-command.patch
Patch7: compiz-window-decorator.patch
Patch8: compiz-fix-kde-screensaver.patch
Patch9: CVE-2007-3920-screensaver-password-bypass.patch

License: GPL
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: x11-util-macros			>= 1.1.5
BuildRequires: libx11-devel			>= 1.1.3
BuildRequires: libxext-devel			>= 1.0.3
BuildRequires: libxtst-devel			>= 1.0.3
BuildRequires: libxcursor-devel			>= 1.1.9
BuildRequires: libxrender-devel			>= 0.9.4
BuildRequires: libxcomposite-devel		>= 0.4.0
BuildRequires: libxdamage-devel			>= 1.1.1
BuildRequires: libxinerama-devel		>= 1.0.2
BuildRequires: libxrandr-devel			>= 1.2.2
BuildRequires: libxfixes-devel			>= 4.0.3
BuildRequires: freetype2-devel			>= 2.3.5
BuildRequires: xft2-devel			>= 2.1.12
BuildRequires: fontconfig-devel			>= 2.5.0

BuildRequires: mesagl-devel			>= 7.0.2
BuildRequires: mesaglu-devel			>= 7.0.2

BuildRequires: libpng-devel			>= 2:1.2.24
BuildRequires: zlib-devel

BuildRequires: dbus-glib-devel			>= 0.74
BuildRequires: libGConf2-devel			>= 2.21.1
BuildRequires: libgnome-window-settings-devel	>= 2.21.4
BuildRequires: libwnck-devel			>= 2.21.2.1
BuildRequires: metacity-devel			>= 2.21.5
BuildRequires: pango-devel			>= 1.19.2
BuildRequires: gnome-desktop-devel		>= 2.21.4
BuildRequires: startup-notification-devel	>= 0.9
BuildRequires: kdebase-devel			>= 1:3.5.8
BuildRequires: bonoboui-devel			>= 2.20.0
BuildRequires: libxslt-devel			>= 1.1.22
BuildRequires: libxslt-proc			>= 1.1.22
BuildRequires: librsvg-devel			>= 2.18.2
BuildRequires: libcairo-devel			>= 1.4.10
BuildRequires: libsvg-cairo-devel		>= 0.1.6
BuildRequires: libdbus-qt-devel			>= 0.70
BuildRequires: libfuse-devel			>= 2.7.2

Requires(post): GConf2
Requires(preun): GConf2
Requires: %{libname} = %{version}-%{release}
Requires: compositing-wm-common
Provides: compositing-wm
Requires: compiz-decorator
Obsoletes: beryl-core

%description
Compiz is an OpenGL composite manager for Xgl and AIGLX.

#----------------------------------------------------------------------------

%package decorator-gtk
Summary: GTK window decorator for compiz
Group: System/X11
Provides: compiz-decorator
Conflicts: %{name} < 0.3.6-4mdv2007.1
Requires:  %{name} = %{version}-%{release}
Obsoletes: heliodor

%description decorator-gtk
This package provides a GTK window decorator for the compiz OpenGL
compositing manager.

#----------------------------------------------------------------------------

%package decorator-kde
Summary: KDE window decorator for compiz
Group: System/X11
Provides: compiz-decorator
Conflicts: %{name} < 0.3.6-4mdv2007.1
Requires:  %{name} = %{version}-%{release}
Obsoletes: aquamarine

%description decorator-kde
This package provides a KDE window decorator for the compiz OpenGL
compositing manager.

#----------------------------------------------------------------------------

%package -n %libname
Summary: Shared libraries for compiz
Group: System/X11
Conflicts: %{name} < 0.5.1
Obsoletes: %mklibname beryl-core 0

%description -n %libname
This package provides shared libraries for compiz.

#----------------------------------------------------------------------------

%package -n %libname_devel
Summary: Development files for compiz
Group: Development/X11
Provides:  %{name}-devel = %{version}-%{release}
Obsoletes: %{name}-devel
Requires: %{libname} = %{version}-%{release}
Requires: png-devel
Requires: libxcomposite-devel
Requires: libxdamage-devel
Requires: libxfixes-devel
Requires: libxrandr-devel
Requires: libxinerama-devel
Requires: libice-devel
Requires: libsm-devel
Requires: startup-notification-devel
Requires: GL-devel
Requires: libxslt-devel
Requires: libxslt-proc
Requires: glib2-devel

Obsoletes: %mklibname -d beryl-core 0

%description -n %libname_devel
This package provides development files for compiz.

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .tfp_server_ext
%patch2 -p1 -b .fix_kde_windows_decoration_mem_leak
%patch3 -p1 -b .defplug
%patch4 -p1 -b .top
%patch6 -p1 -b .decorator_command
%patch7 -p1 -b .compiz_decorator
%patch8 -p1 -b .kde_screensaver
%patch9 -p1 -b .cve_pw_bypass


%build
%if %{mdkversion} < 200800
  # (colin) This seems to be needed on 2007.1 but breaks things on 2008+
  autoreconf
%endif
perl -pi -e "s|(QTDIR/)lib|\1%{_lib}|" configure
%configure2_5x 
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -m755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-window-decorator
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/compositing-wm/%{name}.defaults
%find_lang %{name}

%define schemas compiz-annotate compiz-blur compiz-clone compiz-core compiz-cube compiz-dbus compiz-decoration compiz-fade compiz-fs compiz-gconf compiz-glib compiz-ini compiz-inotify compiz-minimize compiz-move compiz-place compiz-plane compiz-png compiz-regex compiz-resize compiz-rotate compiz-scale compiz-screenshot compiz-svg compiz-switcher compiz-video compiz-water compiz-wobbly compiz-zoom

%post
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%triggerpostun -- beryl-core

if [ -w %{_sysconfdir}/sysconfig/compositing-wm ]; then
  sed -i 's/COMPOSITING_WM=beryl/COMPOSITING_WM=compiz-fusion/' \
   %{_sysconfdir}/sysconfig/compositing-wm
fi

%post decorator-gtk
%post_install_gconf_schemas gwd

%preun decorator-gtk
%preun_uninstall_gconf_schemas gwd

%clean
rm -rf %{buildroot}

#----------------------------------------------------------------------------

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}-window-decorator
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.a
%{_libdir}/window-manager-settings/lib%{name}.*
%(for schema in %schemas; do
   echo "%{_sysconfdir}/gconf/schemas/$schema.schemas"
  done)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.xml
%{_datadir}/%{name}/*.xslt
%{_datadir}/gnome/wm-properties/%{name}.desktop
%{_datadir}/compositing-wm/%{name}.defaults

%files decorator-gtk
%defattr(-,root,root)
%{_bindir}/gtk-window-decorator
%{_sysconfdir}/gconf/schemas/gwd.schemas
%if %{mdkversion} > 200710
%{_datadir}/gnome-control-center/keybindings/50-%{name}-key.xml
%{_datadir}/gnome-control-center/keybindings/50-%{name}-desktop-key.xml
%endif

%files decorator-kde
%defattr(-,root,root)
%{_bindir}/kde-window-decorator

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libdecoration.so.*

%files -n %libname_devel
%defattr(-,root,root)
%{_includedir}/%{name}/%{name}.h
%{_includedir}/%{name}/cube.h
%{_includedir}/%{name}/decoration.h
%{_includedir}/%{name}/scale.h
%{_libdir}/libdecoration.a
%{_libdir}/libdecoration.la
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-cube.pc
%{_libdir}/pkgconfig/%{name}-gconf.pc
%{_libdir}/pkgconfig/%{name}-scale.pc
%{_libdir}/pkgconfig/libdecoration.pc
