%define debug_package %{nil}
%define _disable_ld_no_undefined 1
%define rel 1
%define git 0

%define major 0
%define libname %mklibname %{name} %major
%define libname_devel %mklibname -d %{name}

%define libcompizconfig %mklibname compizconfig %{major}
%define libcompizconfig_devel %mklibname compizconfig -d

%if %{_use_internal_dependency_generator}
%define __noautoreq 'libgtk_window_decorator_(.*)'
%endif

%if %{git}
%define srcname %{name}-%{git}.tar.xz
%define distname %{name}-%{git}
%define release 0.%{git}.%{rel}
%else
%define srcname %{name}-%{version}.tar.xz
%define distname %{name}-%{version}
%define release %{rel}
%endif

Name:	compiz
Version:	0.9.14.1
Release:	%{release}
Summary:	OpenGL composite manager for Xgl and AIGLX
Group:		System/X11
License:	GPLv2+ and LGPLv2+ and MIT
URL:		http://www.compiz.org/
# Current source lives at https://launchpad.net/compiz
Source0:	http://cgit.compiz-fusion.org/compiz/core/snapshot/%{srcname}
Source1:	compiz.defaults
Source2:	compiz-window-decorator
Source3:	kstylerc.xinit

# fedora sources bumped by x10
Source11:	compiz-gtk
Source12:	compiz-gtk.desktop
Source13:	compiz-gnome.desktop
Source14:	compiz-gnome.session

Patch100:		compiz-0.9.14.1-python-sitearch.patch
#Patch101:		compiz-0.9.14.0-alt-ascii-to-utf8.patch
#Patch0:		compiz-0.9.8.2-rosa-linking.patch
#Patch1:		compiz-0.9.9.0-mga-boost-1.53.patch

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
#Patch501: 0501-Add-Mandriva-graphic-to-the-top-of-the-cube.patch
#Patch502: 0502-Use-our-compiz-window-decorator-script-as-the-defaul.patch
#Patch503: 0503-Do-not-put-window-decorations-on-KDE-screensaver.patch
# Next to impossible to rediff
#Patch504: 0504-Also-check-for-tfp-in-server-extensions.patch

# needed by autoreconf:
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	glibmm2.4-devel
BuildRequires:  xsltproc
#BuildRequires:	kdebase4-workspace-devel
BuildRequires:	libxslt-devel
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(gconf-2.0) 
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(gl) pkgconfig(glu)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(glesv2)	
BuildRequires:	python-pyrex
BuildRequires:	desktop-file-utils
BuildRequires:	metacity-devel
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(libprotobuf-c)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:	pkgconfig(python)
BuildRequires:	python-cython
BuildRequires:  python3dist(cython)
BuildRequires:  python3egg(cython)	
BuildRequires:	python-pkg-resources

Requires(post): GConf2
Requires(preun): GConf2
Requires:	%{libname} = %{version}-%{release}
Requires:	compositing-wm-common
Provides:	compositing-wm
Requires:	compiz-decorator
%rename	compiz-bcop

%description
Compiz is an OpenGL composite manager for Xgl and AIGLX.

#----------------------------------------------------------------------------

%package decorator-gtk
Summary:	GTK window decorator for compiz
Group:		System/X11
Provides:	compiz-decorator
Requires:	%{name} = %{version}-%{release}

%description decorator-gtk
This package provides a GTK window decorator for the compiz OpenGL
compositing manager.

#----------------------------------------------------------------------------

%package decorator-kde4
Summary:	KDE4 window decorator for compiz
Group:		System/X11
Provides:	compiz-decorator
Requires:	%{name} = %{version}-%{release}

%description decorator-kde4
This package provides a KDE4 window decorator for the compiz OpenGL
compositing manager.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared libraries for compiz
Group:		System/X11
Conflicts:	%{name} < 0.5.1

%description -n %{libname}
This package provides shared libraries for compiz.

#----------------------------------------------------------------------------

%package -n %{libname_devel}
Summary:	Development files for compiz
Group:		Development/X11
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{name}-devel < %{EVRD}
Requires:	%{libname} = %{version}-%{release}

%description -n %libname_devel
This package provides development files for compiz.

#----------------------------------------------------------------------------

%package -n ccsm
Summary: Compiz Config Settings Manager
Group: System/X11
BuildArch: noarch
Provides: python-ccm = %{EVRD}
Requires: python-compizconfig

%description -n ccsm
Configuration tool for Compiz when used with the ccp configuration plugin.

#----------------------------------------------------------------------------

%package -n %{libcompizconfig}
Summary: Backend configuration library from Compiz Fusion
Group: System/X11
Requires: compizconfig-backends

%description -n %{libcompizconfig}
Backend configuration library from Compiz Fusion.

#----------------------------------------------------------------------------

%package -n %{libcompizconfig_devel}
Summary: Development files for libcompizconfig
Group: Development/X11
Provides: compizconfig-devel
Requires: %{libcompizconfig} = %{version}

%description -n %{libcompizconfig_devel}
Development files for libcompizconfig.

#----------------------------------------------------------------------------

%package -n compizconfig-backends
Summary: Backend modules for libcompizconfig
Group: System/X11

%description -n compizconfig-backends
Backend modules for libcompizconfig.

#----------------------------------------------------------------------------

%package -n python-compizconfig
Summary: Python bindings for libcompizconfig
Group: System/X11

%description -n python-compizconfig
Python bindings for libcompizconfig.

#----------------------------------------------------------------------------

%prep
%setup -qn %{distname}
%apply_patches

%build
export CC=gcc
export CXX=g++

%if %{git}
# no idea if this is still valid 2011-11-02
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif

export CFLAGS+=" -fno-strict-aliasing -Wno-error=deprecated-declarations" CXXFLAGS+=" -fno-strict-aliasing" FFLAGS+=" -fno-strict-aliasing"

%cmake -DCOMPIZ_PACKAGING_ENABLED=ON \
	-DCYTHON_BIN=/usr/bin/cython \
	-DBUILD_GNOME_KEYBINDINGS=OFF \
	-DCOMPIZ_BUILD_WITH_RPATH=OFF \
	-DCOMPIZ_DISABLE_SCHEMAS_INSTALL=ON \
	-DCOMPIZ_INSTALL_GCONF_SCHEMA_DIR=%{_sysconfdir}/gconf/schemas ..
	
find -name flags.make | while read l; do sed -i 's|\ -Werror\ | |g' $l; done
%make

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
%find_lang ccsm

#fedora sources
install %SOURCE11 %{buildroot}/%{_bindir}

# set up an X session
mkdir -p %{buildroot}%{_datadir}/xsessions
install %SOURCE13 %{buildroot}/%{_datadir}/xsessions
mkdir -p %{buildroot}%{_datadir}/gnome-session/sessions
install %SOURCE14 %{buildroot}/%{_datadir}/gnome-session/sessions

desktop-file-install --vendor="" \
	--dir %{buildroot}%{_datadir}/applications \
	%SOURCE12

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# Define the plugins
# NB not all plugins are listed here as some ar packaged separately.
%define plugins annotate blur clone commands cube dbus decoration fade fs gconf glib gnomecompat ini inotify minimize move obs place png regex resize rotate scale screenshot svg switcher video water wobbly zoom
%define schemas compiz-core %(for plugin in %{plugins}; do echo -n " compiz-$plugin"; done)

#ifarch x86_64
#mv -f %{buildroot}%{_prefix}/lib/compizconfig %{buildroot}%{_libdir}/
#mv -f %{buildroot}%{_prefix}/lib/libcompizconfig_gsettings_backend.so %{buildroot}%{_libdir}/
#endif

rm -f %{buildroot}%{py_puresitedir}/*.egg-info

desktop-file-install \
--vendor="" \
--remove-category="Compiz" \
--add-category="GTK" \
--add-category="Settings" \
--add-category="DesktopSettings" \
--add-category="X-MandrivaLinux-CrossDesktop" \
--dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/%{name}.desktop

#----------------------------------------------------------------------------

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}-window-decorator
%{_bindir}/compiz-decorator
%dir %{_libdir}/%{name}
# why do a for loop if all the files go in the same pkg???
%{_libdir}/%{name}/lib*.so
%exclude %{_libdir}/%{name}/libannotate.so
%exclude %{_libdir}/%{name}/libgnomecompat.so
%exclude %{_libdir}/%{name}/libkde.so
# why do a for loop if all the files go in the same pkg???
#{_sysconfdir}/gconf/schemas/%{name}-*.schemas
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
%{_datadir}/%{name}/cubeaddon
%{_datadir}/%{name}/mag
%{_datadir}/%{name}/showmouse
%{_datadir}/%{name}/splash
%{_datadir}/applications/%{name}.desktop
%{_datadir}/compositing-wm/%{name}.defaults

%files decorator-gtk
%{_bindir}/compiz-gtk
%{_bindir}/gtk-window-decorator
%{_sysconfdir}/gconf/schemas/gwd.schemas
#%{_datadir}/gnome-control-center/keybindings/50-%{name}-*.xml
%{_datadir}/applications/compiz-gtk.desktop
# split into gnome pkg ???
%{_datadir}/xsessions/compiz-gnome.desktop
%{_datadir}/gnome-session/sessions/compiz-gnome.session
%{_libdir}/%{name}/libannotate.so
%{_libdir}/%{name}/libgnomecompat.so
%{_datadir}/%{name}/annotate.xml
%{_datadir}/%{name}/gnomecompat.xml
#{_sysconfdir}/gconf/schemas/%{name}-annotate.schemas
#{_sysconfdir}/gconf/schemas/%{name}-gnomecompat.schemas

%files decorator-kde4
%{_bindir}/kde4-window-decorator
#{_libdir}/%{name}/libkde.so
#{_datadir}/%{name}/kde.xml
#{_sysconfdir}/gconf/schemas/%{name}-kde.schemas

%files -n %{libname}
%{_libdir}/libdecoration.so.%{major}*
%{_libdir}/libcompiz_core.so.*

%files -n %{libname_devel}
%dir %{_datadir}/%{name}/xslt
%{_includedir}/%{name}/*
%{_libdir}/libcompiz_core.so
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/pkgconfig/libdecoration.pc
%{_datadir}/cmake/Modules/*cmake
%{_datadir}/%{name}/cmake
%{_datadir}/%{name}/xslt/*.xslt
%{_datadir}/cmake-*/FindCompiz.cmake
%{_datadir}/cmake-*/FindOpenGLES2.cmake

%files -n ccsm -f ccsm.lang
%{_bindir}/ccsm
%{_datadir}/ccsm
%{py_puresitedir}/ccm
%{_datadir}/applications/ccsm.desktop
%{_iconsdir}/hicolor/*/apps/ccsm.*

%files -n %{libcompizconfig}
%{_libdir}/libcompizconfig.so.%{major}*

%files -n %{libcompizconfig_devel}
%{_libdir}/libcompizconfig.so
%{_includedir}/compizconfig
%{_libdir}/pkgconfig/libcompizconfig.pc
%{_datadir}/cmake-*/FindCompizConfig.cmake

%files -n compizconfig-backends
%dir %{_libdir}/compizconfig
%{_libdir}/compizconfig/backends
%{_libdir}/libcompizconfig_gsettings_backend.so

%files -n python-compizconfig
%{py_platsitedir}/compizconfig*
