%define _disable_ld_no_undefined 1
%define rel 5
%define git 0

%define major 0
%define libname %mklibname %{name} %major
%define libname_devel %mklibname -d %{name}

%if %{git}
%define srcname %{name}-%{git}.tar.xz
%define distname %{name}-%{git}
%define release 0.%{git}.%{rel}
%else
%define srcname %{name}-%{version}.tar.bz2
%define distname %{name}-%{version}
%define release %{rel}
%endif

%global default_plugins core composite opengl copytex compiztoolbox decor scale resize gnomecompat staticswitcher place move mousepoll vpswitch regex snap session wall workarounds ezoom

Name: compiz
Version: 0.9.5.92.1
Release: %release
Summary: OpenGL composite manager for Xgl and AIGLX
Group: System/X11
License: GPLv2+,LGPLv2+,MIT
URL: http://www.compiz.org/
Source: http://cgit.compiz-fusion.org/compiz/core/snapshot/%{srcname}
Source1: compiz.defaults
Source2: compiz-window-decorator
Source3: kstylerc.xinit

# fedora sources bumped by x10
Source11: compiz-gtk
Source12: compiz-gtk.desktop
Source13: compiz-gnome.desktop
Source14: compiz-gnome.session

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

# Mandriva Patches
# git format-patch --start-number 500 mdv-0.8.0-cherry-picks..mdv-0.8.0-patches
Patch501: 0501-Add-Mandriva-graphic-to-the-top-of-the-cube.patch
Patch502: 0502-Use-our-compiz-window-decorator-script-as-the-defaul.patch
Patch503: 0503-Do-not-put-window-decorations-on-KDE-screensaver.patch
# Next to impossible to rediff
#Patch504: 0504-Also-check-for-tfp-in-server-extensions.patch

# fedora patches
# Allow installation of GNOME keybindings without GNOME window manager
# settings stuff (sent upstream)
Patch122: compiz-0.9.2.1-keybindings.patch

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
BuildRequires: libglade2.0-devel
BuildRequires: startup-notification-devel
BuildRequires: libcanberra-gtk-devel
BuildRequires: libgtop2.0-devel

BuildRequires: kdebase4-devel
BuildRequires: kdebase4-workspace-devel
BuildRequires: kdelibs4-devel

BuildRequires: libbonoboui-devel
BuildRequires: libxslt-devel
BuildRequires: libxslt-proc
BuildRequires: librsvg-devel
BuildRequires: libcairo-devel
BuildRequires: libsvg-cairo-devel
BuildRequires: fuse-devel
# needed by autoreconf:
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: glibmm2.4-devel


Requires(post): GConf2
Requires(preun): GConf2
Requires: %{libname} = %{version}-%{release}
Requires: compositing-wm-common
Provides: compositing-wm
Requires: compiz-decorator
Obsoletes: beryl-core
%rename compiz-bcop

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

%package decorator-kde4
Summary: KDE4 window decorator for compiz
Group: System/X11
Provides: compiz-decorator
Requires:  %{name} = %{version}-%{release}

%description decorator-kde4
This package provides a KDE4 window decorator for the compiz OpenGL
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
%description -n %libname_devel
This package provides development files for compiz.

#----------------------------------------------------------------------------

%prep
%setup -qn %{distname}
%apply_patches

%build
%if %{git}
# no idea if this is still valid 2011-11-02
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif

%cmake -DCOMPIZ_DEFAULT_PLUGINS="%{default_plugins}" \
    -DCOMPIZ_PACKAGING_ENABLED=ON \
	-DBUILD_GNOME_KEYBINDINGS=OFF \
	-DCOMPIZ_BUILD_WITH_RPATH=OFF \
	-DCOMPIZ_DISABLE_SCHEMAS_INSTALL=ON \
	-DCOMPIZ_INSTALL_GCONF_SCHEMA_DIR=%{_sysconfdir}/gconf/schemas ..
make -j2
#%%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build
pushd build
# This should work, but is buggy upstream:
# make DESTDIR=%{buildroot} findcompiz_install
# So we do this instead:
mkdir -p %{buildroot}%{_datadir}/cmake/Modules
cmake -E copy ../cmake/FindCompiz.cmake %{buildroot}%{_datadir}/cmake/Modules
popd

install -m755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-window-decorator
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/compositing-wm/%{name}.defaults

%find_lang %{name}

#fedora sources
install %SOURCE11 %{buildroot}/%{_bindir}

# set up an X session
mkdir -p %{buildroot}%{_datadir}/xsessions
install %SOURCE13 %{buildroot}/%{_datadir}/xsessions
mkdir -p %{buildroot}%{_datadir}/gnome-session/sessions
install %SOURCE14 %{buildroot}/%{_datadir}/gnome-session/sessions

# create compiz keybindings file based on the metacity ones
# lifted straight from Ubuntu, as long as installation of the upstream
# ones is broken at least (I've reported this upstream)
mkdir -p %{buildroot}/%{_datadir}/gnome-control-center/keybindings
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-launchers.xml > %{buildroot}/%{_datadir}/gnome-control-center/keybindings/50-compiz-launchers.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-navigation.xml > %{buildroot}/%{_datadir}/gnome-control-center/keybindings/50-compiz-navigation.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-screenshot.xml > %{buildroot}/%{_datadir}/gnome-control-center/keybindings/50-compiz-screenshot.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-system.xml > %{buildroot}/%{_datadir}/gnome-control-center/keybindings/50-compiz-system.xml
	sed 's/wm_name=\"Metacity\" package=\"metacity\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/gnome-control-center/keybindings/50-metacity-windows.xml > %{buildroot}/%{_datadir}/gnome-control-center/keybindings/50-compiz-windows.xml
	sed -i 's#key=\"/apps/metacity/general/num_workspaces\" comparison=\"gt\"##g' %{buildroot}/%{_datadir}/gnome-control-center/keybindings/50-compiz-navigation.xml
	sed -i 's#key=\"/apps/metacity/general/num_workspaces\" comparison=\"gt\"##g' %{buildroot}/%{_datadir}/gnome-control-center/keybindings/50-compiz-windows.xml

desktop-file-install --vendor="" \
	--dir %{buildroot}%{_datadir}/applications \
	%SOURCE12

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# Define the plugins
# NB not all plugins are listed here as some ar packaged separately.
%define plugins annotate blur clone commands cube dbus decoration fade fs gconf glib gnomecompat ini inotify minimize move obs place png regex resize rotate scale screenshot svg switcher video water wobbly zoom
%define schemas compiz-core %(for plugin in %{plugins}; do echo -n " compiz-$plugin"; done)

%if %mdkversion < 200900
%post
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%post decorator-gtk
%post_install_gconf_schemas gwd

%preun decorator-gtk
%preun_uninstall_gconf_schemas gwd
%endif

%clean
rm -rf %{buildroot}

#----------------------------------------------------------------------------

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}-window-decorator
%dir %{_libdir}/%{name}
# why do a for loop if all the files go in the same pkg???
%{_libdir}/%{name}/lib*.so
%exclude %{_libdir}/%{name}/libannotate.so
%exclude %{_libdir}/%{name}/libgnomecompat.so
%exclude %{_libdir}/%{name}/libkde.so
# why do a for loop if all the files go in the same pkg???
%{_sysconfdir}/gconf/schemas/%{name}-*.schemas
%exclude %{_sysconfdir}/gconf/schemas/%{name}-annotate.schemas
%exclude %{_sysconfdir}/gconf/schemas/%{name}-gnomecompat.schemas
%exclude %{_sysconfdir}/gconf/schemas/%{name}-kde.schemas
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.xml
%exclude %{_datadir}/%{name}/annotate.xml
%exclude %{_datadir}/%{name}/gnomecompat.xml
%exclude %{_datadir}/%{name}/kde.xml
%dir %{_datadir}/%{name}/cube
%dir %{_datadir}/%{name}/cube/images
%{_datadir}/%{name}/cube/images/*.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/compositing-wm/%{name}.defaults

%files decorator-gtk
%defattr(-,root,root)
%{_bindir}/compiz-gtk
%{_bindir}/gtk-window-decorator
%{_sysconfdir}/gconf/schemas/gwd.schemas
%{_datadir}/gnome-control-center/keybindings/50-%{name}-*.xml
%{_datadir}/applications/compiz-gtk.desktop
# split into gnome pkg ???
%{_datadir}/xsessions/compiz-gnome.desktop
%{_datadir}/gnome-session/sessions/compiz-gnome.session
%{_libdir}/%{name}/libannotate.so
%{_libdir}/%{name}/libgnomecompat.so
%{_datadir}/%{name}/annotate.xml
%{_datadir}/%{name}/gnomecompat.xml
%{_sysconfdir}/gconf/schemas/%{name}-annotate.schemas
%{_sysconfdir}/gconf/schemas/%{name}-gnomecompat.schemas

%files decorator-kde4
%defattr(-,root,root)
%{_bindir}/kde4-window-decorator
%{_libdir}/%{name}/libkde.so
%{_datadir}/%{name}/kde.xml
%{_sysconfdir}/gconf/schemas/%{name}-kde.schemas

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libdecoration.so.%{major}*

%files -n %libname_devel
%defattr(-,root,root)
%dir %{_datadir}/%{name}/xslt
%{_includedir}/%{name}/*
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/pkgconfig/libdecoration.pc
%{_datadir}/cmake/Modules/*cmake
%{_datadir}/%{name}/cmake
%{_datadir}/%{name}/xslt/*.xslt
