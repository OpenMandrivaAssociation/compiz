%define name compiz
%define version 0.8.4
%define rel 4
%define git 0

%define major 0
%define libname %mklibname %{name} %major
%define libname_devel %mklibname -d %{name}

%if %{git}
%define srcname %{name}-%{git}.tar.lzma
%define distname %{name}-%{git}
%define release %mkrel 0.%{git}.%{rel}
%else
%define srcname %{name}-%{version}.tar.bz2
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

%if %{mdkversion} > 200900
 %define build_kde3 0
%else
 %define build_kde3 1
%endif



Name: %name
Version: %version
Release: %release
Summary: OpenGL composite manager for Xgl and AIGLX
Group: System/X11
URL: http://www.compiz.org/
Source: http://cgit.compiz-fusion.org/compiz/core/snapshot/%{srcname}
Source1: compiz.defaults
Source2: compiz-window-decorator
Source3: kstylerc.xinit

# (cg) Using git to manage patches
# To recreate the structure
# git clone git://git.freedesktop.org/git/xorg/app/compiz
# git checkout compiz-0.8.0
# git checkout -b mdv-0.8.0-cherry-picks
# git am 00*.patch
# git checkout -b mdv-0.8.0-patches
# git am 05*.patch

# To apply new custom patches
# git checkout mdv-0.8.0-patches
# (do stuff)

# To apply new cherry-picks
# git checkout mdv-0.8.0-cherry-picks
# git cherry-pick <blah>
# git checkout mdv-0.8.0-patches
# git rebase mdv-0.8.0-cherry-picks

# Cherry Pick Patches
# git format-patch compiz-0.8.4..compiz-0.8
Patch0100: 0100-Post-release-version-increment.patch
Patch0101: 0101-Fix-crash-in-multi-screen-setups.patch
Patch0102: 0102-Fix-Gnome-keybinding-list.patch
Patch0103: 0103-Make-short-descriptions-of-bindings-a-_little_-more-.patch
Patch0104: 0104-Clean-up-focus-functions.patch
Patch0105: 0105-Fix-some-focus-issues.patch
Patch0106: 0106-Fix-gravity-handling.patch
Patch0107: 0107-Minor-consistency-fix.patch
Patch0108: 0108-Only-keep-windows-on-screen-that-were-fully-on-scree.patch
Patch0109: 0109-Correctly-reflect-that-the-switcher-window-is-manage.patch
Patch0110: 0110-Fix-icon-property-reading-if-the-icon-pixmap-has-a-d.patch
Patch0111: 0111-Don-t-pull-in-unstable-API-it-s-not-needed-any-longe.patch
Patch0112: 0112-Revert-Don-t-pull-in-unstable-API-it-s-not-needed-an.patch
Patch0113: 0113-Fix-crash.patch
Patch0114: 0114-Better-resize-constraint-and-snap-for-combined-work-.patch
Patch0115: 0115-Minor-whitespace-fixes-and-optimizations.patch
Patch0116: 0116-Do-the-resize-output-snap-only-when-outside.patch
Patch0117: 0117-Complete-the-work-area-optimization.patch
Patch0118: 0118-wobbly-Fix-y-constraint-on-throwing.patch
Patch0119: 0119-wobbly-Fix-warning.patch
Patch0120: 0120-wobbly-Constrain-throwing-at-the-bottom-as-well.patch
Patch0121: 0121-Fix-window-region-calculation-for-windows-that-have-.patch
Patch0122: 0122-Fix-crash-on-opening-windows.patch
Patch0123: 0123-Fix-handling-of-windows-that-have-a-server-border-se.patch
Patch0124: 0124-Also-handle-windows-that-have-a-server-border-set-pr.patch
Patch0125: 0125-Fix-typo.patch
Patch0126: 0126-Properly-send-ClientMessage-event-after-aquiring-com.patch
Patch0127: 0127-Only-accept-ConfigureRequest-_NET_MOVERESIZE_WINDOW-.patch
Patch0128: 0128-Kde-4.4-support.patch
Patch0129: 0129-Better-detection-of-tooltip-windows-KDE-backport.patch
Patch0130: 0130-Fake-enlightment-desktop-property-to-make-qt-ignore-.patch
Patch0131: 0131-Fix-window-position-validation-for-windows-that-chan.patch
Patch0132: 0132-Link-all-required-libraries-explicitly.patch
Patch0133: 0133-Cleanup-key-binding-list-from-redundant-and-unneeded.patch
Patch0134: 0134-Also-place-windows-that-are-marked-unmovable.patch
Patch0135: 0135-Fix-png-plugin-to-work-with-libpng-1.4.patch
Patch0136: 0136-Keep-pixmaps-of-unmapped-windows-around-if-they-are-.patch
Patch0137: 0137-Make-sure-w-width-and-w-height-always-reflect-the-si.patch
Patch0138: 0138-gtk-decorator-Replace-deprecated-GTK_WIDGET_VISIBLE-.patch

# Mandriva Patches
# git format-patch --start-number 500 mdv-0.8.0-cherry-picks..mdv-0.8.0-patches
Patch500: 0500-Fix-memory-leak-in-KDE3-window-decorator.patch
Patch501: 0501-Add-Mandriva-graphic-to-the-top-of-the-cube.patch
Patch502: 0502-Use-our-compiz-window-decorator-script-as-the-defaul.patch
Patch503: 0503-Do-not-put-window-decorations-on-KDE-screensaver.patch
Patch504: 0504-Also-check-for-tfp-in-server-extensions.patch
Patch505: 0505-Fix-KDE3-linking-by-changing-the-directory-order.patch

License: GPLv2+ and LGPLv2+ and MIT
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
BuildRequires: libglade2-devel
BuildRequires: startup-notification-devel
BuildRequires: libcanberra-devel
BuildRequires: libgtop2.0-devel

%if %{build_kde3}
BuildRequires: kdebase3-devel
%if %{mdkversion} > 200810
BuildRequires: kde3-macros
%endif
%endif

%if %{build_kde4}
BuildRequires: kdebase4-devel
BuildRequires: kdebase4-workspace-devel
%if %{mdkversion} >= 200910
BuildRequires: kdelibs4-devel
%endif
%endif

BuildRequires: bonoboui-devel
BuildRequires: libxslt-devel
BuildRequires: libxslt-proc
BuildRequires: librsvg-devel
BuildRequires: libcairo-devel
BuildRequires: libsvg-cairo-devel
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

%if %{build_kde3}
%package decorator-kde
Summary: KDE window decorator for compiz
Group: System/X11
Provides: compiz-decorator
Conflicts: %{name} < 0.3.6-4mdv2007.1
Conflicts: compositing-wm-common <= compositing-wm-common-2009.0-3mdv2009.0
Requires:  %{name} = %{version}-%{release}
Obsoletes: aquamarine

%description decorator-kde
This package provides a KDE window decorator for the compiz OpenGL
compositing manager.
%endif

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

%if %{build_kde3}
%package config-kconfig
Summary: KDE config backend compiz
Group: System/X11
Requires:  %{name} = %{version}-%{release}

%description config-kconfig
This package provides a KDE config backend for the compiz OpenGL
compositing manager.
%endif

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

%apply_patches


%build
%if %{git}
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%else
  # (Anssi 03/2008) Needed to get rid of RPATH=/usr/lib64 on lib64:
  autoreconf -i
  # build fails without this:
  intltoolize --force
%endif

# (cg) the QTDIR stuff is needed for kde3/qt3 (to find moc) :s
export QTDIR=/usr/lib/qt3
%configure2_5x \
%if !%{build_kde3}
  --disable-kde \
%endif
%if !%{build_kde4}
  --disable-kde4 \
%endif
  --with-default-plugins=core,png,decoration,wobbly,fade,minimize,cube,rotate,zoom,scale,move,resize,place,switcher,screenshot,dbus

%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -m755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-window-decorator
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/compositing-wm/%{name}.defaults
%if %{build_kde3}
install -D -m 0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xinit.d/41kstylerc
%else
rm -f %{buildroot}%{_sysconfdir}/gconf/schemas/compiz-kconfig.schemas
%endif
%find_lang %{name}

#remove unpackaged files
#rm -f %{buildroot}%{_libdir}/compiz/*.a


# Define the plugins
# NB not all plugins are listed here as some ar packaged separately.
%define plugins annotate blur clone commands cube dbus decoration fade fs gconf glib gnomecompat ini inotify minimize move obs place png regex resize rotate scale screenshot svg switcher video water wobbly zoom
%define schemas compiz-core %(for plugin in %{plugins}; do echo -n " compiz-$plugin"; done)

%post
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %{build_kde3}
%post config-kconfig
%post_install_gconf_schemas compiz-kconfig

%preun config-kconfig
%preun_uninstall_gconf_schemas compiz-kconfig
%endif

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
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome/wm-properties/%{name}-wm.desktop
%{_datadir}/compositing-wm/%{name}.defaults

%files decorator-gtk
%defattr(-,root,root)
%{_bindir}/gtk-window-decorator
%{_sysconfdir}/gconf/schemas/gwd.schemas
%if %{mdkversion} > 200710
%{_datadir}/gnome-control-center/keybindings/50-%{name}-key.xml
%{_datadir}/gnome-control-center/keybindings/50-%{name}-desktop-key.xml
%endif


%if %{build_kde3}
%files decorator-kde
%defattr(-,root,root)
%{_bindir}/kde-window-decorator
%{_kde3_configdir}/*
%{_sysconfdir}/X11/xinit.d/41kstylerc
%endif

%if %{build_kde4}
%files decorator-kde4
%defattr(-,root,root)
%{_bindir}/kde4-window-decorator
%endif

%if %{build_kde3}
%files config-kconfig
%defattr(-,root,root)
%{_libdir}/%{name}/libkconfig.so
%{_libdir}/%{name}/libkconfig.la
%{_libdir}/%{name}/libkconfig.a
%{_sysconfdir}/gconf/schemas/compiz-kconfig.schemas
%{_kde3_datadir}/config.kcfg
%endif

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
