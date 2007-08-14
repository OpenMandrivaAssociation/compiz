%define name compiz
%define version 0.5.2
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
Source: http://xorg.freedesktop.org/archive/individual/app/%{srcname}.tar.bz2 
Source1: compiz.defaults
Source2: compiz-window-decorator
# Patches for AIGLX
# Thanks Kristian Høgsberg
# Patch1 updated by Johannes (Hanno) B�ck to automatically detect AIGLX
# http://svn.hboeck.de/xgl-overlay/x11-wm/compiz/files/compiz-tfp
Patch1: 0001-Also-check-for-tfp-in-server-extensions-rediff.txt
Patch3: 0003-Set-_NET_WM_CM_S-d-selection-instead-of-older-WM_S-d.txt
# Patch from mandriva
Patch4: compiz-default-plugins.patch
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
BuildRequires: librsvg-devel
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
BuildRequires: libxslt-devel
BuildRequires: libxslt-proc
Requires(post): GConf2
Requires(preun): GConf2
Requires: %{libname} = %{version}-%{release}
Requires: compositing-wm-common
Provides: compositing-wm
Requires: compiz-decorator
Obsoletes: beryl-core

%description
OpenGL composite manager for Xgl and AIGLX.

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
Shared libraries for compiz

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
Development files for compiz

#----------------------------------------------------------------------------

%prep
%setup -q -n %{distname}
%patch1 -p1 -b .tfp_server_ext
%patch3 -p1 -b .net_wm_cm
%patch4 -p1 -b .defplug
%patch5 -p1 -b .top
%patch8 -p1 -b .minimize
%patch9 -p1 -b .white
%patch10 -p1 -b .fix_kde_windows_decoration_mem_leak

%build
%if %{git}
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%else
  aclocal
  automake
  autoconf
%endif
#perl -pi -e "s|(QTDIR/)lib|\1%{_lib}|" configure
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
%{_datadir}/gnome-control-center/keybindings/50-%{name}-key.xml
%{_datadir}/gnome-control-center/keybindings/50-%{name}-desktop-key.xml

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
