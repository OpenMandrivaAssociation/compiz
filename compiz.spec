%define name compiz
%define version 0.7.7
%define rel 1
%define git 20080713

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

%if %{mdkversion} > 200810
 %define build_kde4 1
%else
 %define build_kde4 0
 %define _kde3_datadir %{_datadir}
 %define _kde3_configdir %{_kde3_datadir}/config
%endif

Name: %name
Version: %version
Release: %release
Summary: OpenGL composite manager for Xgl and AIGLX
Group: System/X11
URL: http://www.go-compiz.org/
Source: http://xorg.freedesktop.org/archive/individual/app/%{srcname}.tar.bz2
Source1: compiz.defaults
Source2: compiz-window-decorator
Patch1:	compiz-0.3.6-kde-mem-leak.patch
# Patches for Mandriva defaults
Patch2: compiz-default-plugins.patch
Patch3: compiz-mandriva-top.patch
Patch4: compiz-decoration-command.patch
Patch5: compiz-window-decorator.patch
Patch6: compiz-fix-kde-screensaver.patch
Patch7: 0001-Also-check-for-tfp-in-server-extensions-rediff.txt
Patch8: compiz-kde3-lib-dir-order.patch

# Upstream cherry picks
Patch101: 0001-Revert-Try-to-start-decorator-in-initScreen-because.patch

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
BuildRequires: libgnome-menu-devel
BuildRequires: gnome-panel-devel
BuildRequires: startup-notification-devel
%if %{mdkversion} > 200810
BuildRequires: kde3-macros
%endif
BuildRequires: kdebase3-devel
%if %{build_kde4}
BuildRequires: kdebase4-devel
BuildRequires: kdebase4-workspace-devel
%endif
BuildRequires: bonoboui-devel
BuildRequires: libxslt-devel
BuildRequires: libxslt-proc
BuildRequires: librsvg-devel
BuildRequires: libcairo-devel
BuildRequires: libsvg-cairo-devel
BuildRequires: libdbus-qt-1-devel
BuildRequires: fuse-devel
# needed by autoreconf:
BuildRequires: intltool

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

%if %{build_kde4}
%package decorator-kde4
Summary: KDE4 window decorator for compiz
Group: System/X11
Provides: compiz-decorator
Requires:  %{name} = %{version}-%{release}

%description decorator-kde4
This package provides a KDE4 window decorator for the compiz OpenGL
compositing manager.
%endif

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

# Upstream cherry picks
%patch101 -p1

%patch1 -p1 -b .fix_kde_windows_decoration_mem_leak
%patch2 -p1 -b .defplug
%patch3 -p1 -b .top
%patch4 -p1 -b .decorator_command
%patch5 -p1 -b .compiz_decorator
%patch6 -p1 -b .kde_screensaver
%patch7 -p1 -b .server-extensions
%patch8 -p1 -b .kde3libdir

%build
%if %{git}
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%else
  # (Anssi 03/2008) Needed to get rid of RPATH=/usr/lib64 on lib64:
  autoreconf
  # build fails without this:
  intltoolize --force
%endif

%configure2_5x \
%if !%{build_kde4}
  --disable-kde4 \
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -m755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-window-decorator
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/compositing-wm/%{name}.defaults
%find_lang %{name}


# Define the plugins
# NB not all plugins are listed here as some ar packaged separately.
%define plugins annotate blur clone cube dbus decoration fade fs gconf glib ini inotify minimize move place png regex resize rotate scale screenshot svg switcher video water wobbly zoom
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
%{_kde3_configdir}/*

%if %{build_kde4}
%files decorator-kde4
%defattr(-,root,root)
%{_bindir}/kde4-window-decorator
%endif

%files config-kconfig
%defattr(-,root,root)
%{_libdir}/%{name}/libkconfig.so
%{_libdir}/%{name}/libkconfig.la
%{_libdir}/%{name}/libkconfig.a
%{_sysconfdir}/gconf/schemas/compiz-kconfig.schemas
%{_kde3_datadir}/config.kcfg

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
