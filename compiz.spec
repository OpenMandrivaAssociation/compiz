%define name compiz
%define version 0.5.0
%define rel 1
%define cvs_version 0

%if  %{cvs_version}
%define srcname %{name}-%{version}-%{cvs_version}
%define distname %{name}
%define release %mkrel 0.%{cvs_version}.%{rel}
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
Source: http://xorg.freedesktop.org/archive/individual/app/%{srcname}.tar.bz2 
Source1: compiz.defaults
Source2: compiz-window-decorator
Patch0: compiz-0.3.6-indirect-detection.patch
# Patches for AIGLX
# Thanks Kristian HÃ¸gsberg
# Patch1 updated by Johannes (Hanno) Böck to automatically detect AIGLX
# http://svn.hboeck.de/xgl-overlay/x11-wm/compiz/files/compiz-tfp
Patch1: 0001-Also-check-for-tfp-in-server-extensions.txt
Patch3: 0003-Set-_NET_WM_CM_S-d-selection-instead-of-older-WM_S-d.txt
# Patch from mandriva
Patch5: compiz-mandriva-top.patch
Patch8: minimize-unminimize.patch
# From gandalfn
Patch9: 90-fix-no-border-window-shadow.patch

Patch10:	compiz-0.3.6-kde-mem-leak.patch

License: GPL
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: libx11-devel >= 1.0.0
BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: x11-proto-devel
BuildRequires: libsvg-cairo-devel
BuildRequires: libpng-devel
BuildRequires: GL-devel
BuildRequires: libwnck-devel
BuildRequires: metacity-devel
BuildRequires: libgnome-window-settings-devel
BuildRequires: libgnome-desktop-2-devel
BuildRequires: libxcomposite-devel
BuildRequires: libxdamage-devel
BuildRequires: intltool
BuildRequires: automake
BuildRequires: libdbus-qt-1-devel
BuildRequires: kdebase-devel
BuildRequires: fuse-devel
Requires(post): GConf2
Requires(preun): GConf2
Requires: compositing-wm-common
Provides: compositing-wm
Requires: compiz-decorator

%description
OpenGL composite manager for Xgl and AIGLX.

%package decorator-gtk
Summary: GTK window decorator for compiz
Group: System/X11
Provides: compiz-decorator
Conflicts: compiz < 0.3.6-7mdv2007.1

%description decorator-gtk
This package provides a GTK window decorator for the compiz OpenGL
compositing manager.

%package decorator-kde
Summary: KDE window decorator for compiz
Group: System/X11
Provides: compiz-decorator
Conflicts: compiz < 0.3.6-4mdv2007.1

%description decorator-kde
This package provides a KDE window decorator for the compiz OpenGL
compositing manager.

%package devel
Summary: Development files for compiz
Group: Development/X11
Requires: %{name} = %{version}
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

%description devel
Development files for compiz

%prep
%setup -q -n %{distname}
%patch0 -p1 -R
%patch1 -p1 -b .tfp_server_ext
%patch3 -p1 -b .net_wm_cm
%patch5 -p1 -b .top
%patch8 -p1 -b .minimize
%patch9 -p1 -b .white
%patch10 -p1 -b .fix_kde_windows_decoration_mem_leak

%build
%if %{cvs_version}
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%else
  aclocal
  automake
  autoconf
%endif
perl -pi -e "s|(QTDIR/)lib|\1%{_lib}|" configure
%configure2_5x \
		--enable-kde \
		--enable-gnome \
		--with-default-plugins="png,decoration,wobbly,fade,minimize,cube,rotate,zoom,scale,move,resize,place,switcher,water,screenshot,dbus,annotate,clone" \
		--enable-libsvg-cairo
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -m755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-window-decorator
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/compositing-wm/%{name}.defaults
%find_lang %{name}

%post
%post_install_gconf_schemas %{name}

%preun
%preun_uninstall_gconf_schemas %{name}

%post decorator-gtk
%post_install_gconf_schemas gwd

%preun decorator-gtk
%preun_uninstall_gconf_schemas gwd

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%{_bindir}/%{name}-window-decorator
%{_libdir}/libdecoration.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.a
%{_libdir}/window-manager-settings/lib%{name}.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.png
%{_datadir}/gnome/wm-properties/%{name}.desktop
%{_datadir}/compositing-wm/%{name}.defaults

%files decorator-gtk
%defattr(-,root,root)
%{_bindir}/gtk-window-decorator
%{_sysconfdir}/gconf/schemas/gwd.schemas

%files decorator-kde
%defattr(-,root,root)
%{_bindir}/kde-window-decorator

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/%{name}.h
%{_includedir}/%{name}/decoration.h
%{_libdir}/libdecoration.a
%{_libdir}/libdecoration.la
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/libdecoration.pc


