%define name compiz
%define version 0.7.0
%define rel 4
%define git 0

%define major 0
%define libname %mklibname %{name} %major
%define libname_devel %mklibname -d %{name}


%if  %{git}
%define srcname %{name}-%{git}
%define distname %{name}
%define release %mkrel 0.%{git}.%{rel}
%else
%define srcname %{name}-%{version}
%define distname %{name}-%{version}
%define release %mkrel %{rel}
%endif

Name: %name
Version: %version
Release: %release
Summary: OpenGL composite manager for Xgl and AIGLX
Group: System/X11
URL: http://www.go-compiz.org/
Source: http://xorg.freedesktop.org/archive/individual/app/%{srcname}.tar.gz
Source1: compiz.defaults
Source2: compiz-window-decorator
Patch1:	compiz-0.3.6-kde-mem-leak.patch
# Patches for Mandriva defaults
Patch2: compiz-default-plugins.patch
Patch3: compiz-mandriva-top.patch
Patch4: compiz-decoration-command.patch
Patch5: compiz-window-decorator.patch
Patch6: compiz-fix-kde-screensaver.patch
Patch7: CVE-2007-3920-screensaver-password-bypass.patch

# Cherry picked patches from master:
Patch1001: 0001-Added-wrappable-callback-functions-for-session-manag.patch
Patch1002: 0002-Don-t-allow-minimization-of-skip-taskbar-dialogs.patch
Patch1003: 0003-Do-not-try-to-produce-broken-introspection-informati.patch
Patch1004: 0004-Do-no-register-core-path-twice.patch
Patch1005: 0005-Export-session-client-id-to-sessionSaveYourself.patch
Patch1006: 0006-Don-t-overwrite-new-client-id-with-the-one-passed-vi.patch
Patch1007: 0007-Don-t-showdesktop-grabbed-windows.patch
Patch1008: 0008-only-allow-rotate-to-faces-that-exist.patch
Patch1009: 0009-Fix-saving-session-client-id-to-session-manager.patch

License: GPL
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: x11-util-macros
BuildRequires: libx11-devel
BuildRequires: libxext-devel
BuildRequires: libxtst-devel
BuildRequires: libxcursor-devel
BuildRequires: libxrender-devel
BuildRequires: libxcomposite-devel
BuildRequires: libxdamage-devel
BuildRequires: libxinerama-devel
BuildRequires: libxrandr-devel
BuildRequires: libxfixes-devel
BuildRequires: freetype2-devel
BuildRequires: xft2-devel
BuildRequires: fontconfig-devel

BuildRequires: mesagl-devel
BuildRequires: mesaglu-devel

BuildRequires: libpng-devel
BuildRequires: zlib-devel

BuildRequires: dbus-glib-devel
BuildRequires: libGConf2-devel
BuildRequires: libgnome-window-settings-devel
BuildRequires: libwnck-devel
BuildRequires: metacity-devel
BuildRequires: pango-devel
BuildRequires: gnome-desktop-devel
BuildRequires: startup-notification-devel
BuildRequires: kdebase-devel
BuildRequires: bonoboui-devel
BuildRequires: libxslt-devel
BuildRequires: libxslt-proc
BuildRequires: librsvg-devel
BuildRequires: libcairo-devel
BuildRequires: libsvg-cairo-devel
BuildRequires: libdbus-qt-1-devel
BuildRequires: fuse-devel

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

%package config-kconfig
Summary: KDE config backend compiz
Group: System/X11
Requires:  %{name} = %{version}-%{release}

%description config-kconfig
This package provides a KDE config backend for the compiz OpenGL
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
%setup -q -n %{distname}
# Cherry picked patches
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1
%patch1009 -p1

%patch1 -p1 -b .fix_kde_windows_decoration_mem_leak
%patch2 -p1 -b .defplug
%patch3 -p1 -b .top
%patch4 -p1 -b .decorator_command
%patch5 -p1 -b .compiz_decorator
%patch6 -p1 -b .kde_screensaver
%patch7 -p1 -b .cve_pw_bypass


%build
%if %{git}
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif
%if %{mdkversion} < 200800
  # (colin) This seems to be needed on 2007.1 but breaks things on 2008+
  autoreconf
%endif
perl -pi -e "s|(QTDIR/)lib|\1%{_lib}|" configure
%configure2_5x --disable-kde4
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -m755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-window-decorator
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/compositing-wm/%{name}.defaults
%find_lang %{name}

# Define the plugins
# NB not all plugins are listed here as some ar packaged separately.
%define plugins annotate blur clone cube dbus decoration fade fs gconf glib ini inotify minimize move place plane png regex resize rotate scale screenshot svg switcher video water wobbly zoom
%define schemas compiz-core %(for plugin in %{plugins}; do echo -n " compiz-$plugin"; done)

%post
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%post config-kconfig
%post_install_gconf_schemas compiz-kconfig

%preun config-kconfig
%preun_uninstall_gconf_schemas compiz-kconfig

%post decorator-gtk
%post_install_gconf_schemas gwd

%preun decorator-gtk
%preun_uninstall_gconf_schemas gwd


%triggerpostun -- beryl-core

if [ -w %{_sysconfdir}/sysconfig/compositing-wm ]; then
  sed -i 's/COMPOSITING_WM=beryl/COMPOSITING_WM=compiz-fusion/' \
   %{_sysconfdir}/sysconfig/compositing-wm
fi

%clean
rm -rf %{buildroot}

#----------------------------------------------------------------------------

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}-window-decorator
%dir %{_libdir}/%{name}
%(for plugin in %{plugins}; do
   echo "%{_libdir}/%{name}/lib$plugin.so"
   echo "%{_libdir}/%{name}/lib$plugin.la"
   echo "%{_libdir}/%{name}/lib$plugin.a"
  done)
%{_libdir}/window-manager-settings/lib%{name}.*
%(for schema in %{schemas}; do
   echo "%{_sysconfdir}/gconf/schemas/$schema.schemas"
   echo "%{_datadir}/config.kcfg/$schema.kcfg"
  done)
%{_datadir}/config/%{name}rc
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

%files config-kconfig
%defattr(-,root,root)
%{_libdir}/%{name}/libkconfig.so
%{_libdir}/%{name}/libkconfig.la
%{_libdir}/%{name}/libkconfig.a
%{_sysconfdir}/gconf/schemas/compiz-kconfig.schemas
%{_datadir}/config.kcfg/compiz-kconfig.kcfg

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libdecoration.so.%{major}*

%files -n %libname_devel
%defattr(-,root,root)
%{_includedir}/%{name}/%{name}*.h
%{_includedir}/%{name}/decoration.h
%{_libdir}/libdecoration.a
%{_libdir}/libdecoration.la
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/pkgconfig/libdecoration.pc
