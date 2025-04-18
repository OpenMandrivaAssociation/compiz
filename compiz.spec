%define debug_package %{nil}
%define _disable_ld_no_undefined 1
%define git 20211217

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
%else
%define srcname %{name}-%{version}.tar.xz
%define distname %{name}-%{version}
%endif

Name:	compiz
Version:	0.9.14.2
Release:	6
Summary:	OpenGL composite manager for Xgl and AIGLX
Group:		System/X11
License:	GPLv2+ and LGPLv2+ and MIT
URL:		https://www.compiz.org/
Patch0:		compiz-0.9.14.2-compile.patch
Patch1:         protobuf.patch
# Current source lives at https://launchpad.net/compiz
Source0:	https://launchpad.net/compiz/0.9.14/%{version}/+download/%{name}-%{version}.tar.xz
Source1:	compiz.defaults
Source2:	compiz-window-decorator
Source3:	kstylerc.xinit

# fedora sources bumped by x10
Source11:	compiz-gtk
Source12:	compiz-gtk.desktop
Source13:	compiz-gnome.desktop
Source14:	compiz-gnome.session

#Patch100:		compiz-0.9.14.1-python-sitearch.patch

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
# bring back this patch in future, need rework it from Mandriva to OpenMandriva (angry)
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
BuildRequires:  lcov
BuildRequires:	glibmm2.4-devel
BuildRequires:  xsltproc
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(gconf-2.0) 
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(dri)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	egl-devel
BuildRequires:	mesa-common-devel
BuildRequires:	python-pyrex
BuildRequires:	desktop-file-utils
BuildRequires:	metacity-devel
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
# As of git from 20211217 no longer compile with protobuf.
# /builddir/build/BUILD/compiz-0.9.14.1/build/compizconfig/libcompizconfig/src/compizconfig.pb.cc:40:127: 
# error: 'constinit' variable 'metadata::_PluginInfo_Dependencies_default_instance_' does not have a constant initializer
# 40 | PROTOBUF_ATTRIBUTE_NO_DESTROY PROTOBUF_CONSTINIT PROTOBUF_ATTRIBUTE_INIT_PRIORITY1 
# PluginInfo_DependenciesDefaultTypeInternal _PluginInfo_Dependencies_default_instance_;                                                                                                                               ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# /builddir/build/BUILD/compiz-0.9.14.1/build/compizconfig/libcompizconfig/src/compizconfig.pb.cc:40:127: error: 
# 'metadata::PluginInfo_DependenciesDefaultTypeInternal{metadata::PluginInfo_DependenciesDefaultTypeInternal::<unnamed union>
BuildRequires:  pkgconfig(libprotobuf-c)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:	cmake(absl)
BuildRequires:	pkgconfig(python)
BuildRequires:	python-cython
BuildRequires:  python3dist(cython)
BuildRequires:	python-pkg-resources

Requires(post): GConf2
Requires(preun): GConf2
Requires:	%{libname} = %{EVRD}
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
Requires:	%{name} = %{EVRD}

%description decorator-gtk
This package provides a GTK window decorator for the compiz OpenGL
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
Requires:	%{libname} = %{EVRD}

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
%setup -qn %{name}-%{version}
%autopatch -p1

%build
export CXXFLAGS="%{optflags} -std=c++17"
# GCC is needed or we see in Clang: "error: no matching function for call to 'scandir'"
export CC=gcc
export CXX=g++

export CFLAGS+=" -fno-strict-aliasing -Wno-error=deprecated-declarations" CXXFLAGS+=" -fno-strict-aliasing" FFLAGS+=" -fno-strict-aliasing"

%cmake -DCOMPIZ_PACKAGING_ENABLED=ON \
	-DCYTHON_BIN=/usr/bin/cython \
	-DBUILD_GNOME_KEYBINDINGS=OFF \
	-DCOMPIZ_BUILD_WITH_RPATH=OFF \
	-DCOMPIZ_DISABLE_SCHEMAS_INSTALL=ON \
	-DCOMPIZ_WERROR=Off \
        -DCOMPIZ_DEFAULT_PLUGINS="composite,opengl,decor,resize,place,move,compiztoolbox,staticswitcher,regex,animation,ccp" \
	-DCOMPIZ_DISABLE_PLUGIN_DBUS=ON \
	-DOpenGL_GL_PREFERENCE=LEGACY \
	-DCOMPIZ_INSTALL_GCONF_SCHEMA_DIR=%{_sysconfdir}/gconf/schemas ..
	
# Needed for fix build on new Clang and GCC version (angry)
# error: unknown warning option '-Wno-subobject-linkage' [-Werror,-Wunknown-warning-option]
find -name flags.make | while read l; do sed -i 's|\ -Werror\ | |g' $l; done

%make_build

%install
rm -rf %{buildroot}
%make_install -C build
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

#rm -f %{buildroot}%{py_puresitedir}/*.egg-info

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
%optional %{_bindir}/%{name}_autopilot_acceptance_tests
%{_bindir}/%{name}-window-decorator
%{_bindir}/compiz-decorator
%dir %{_libdir}/%{name}
# why do a for loop if all the files go in the same pkg???
%{_libdir}/%{name}/lib*.so
%exclude %{_libdir}/%{name}/libannotate.so
%exclude %{_libdir}/%{name}/libgnomecompat.so
#exclude #{_libdir}/%{name}/libkde.so
# why do a for loop if all the files go in the same pkg???
#{_sysconfdir}/gconf/schemas/%{name}-*.schemas
#exclude #{_sysconfdir}/gconf/schemas/%{name}-annotate.schemas
#exclude #{_sysconfdir}/gconf/schemas/%{name}-gnomecompat.schemas
#exclude #{_sysconfdir}/gconf/schemas/%{name}-kde.schemas
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.xml
#exclude #{_datadir}/%{name}/annotate.xml
#exclude #{_datadir}/%{name}/gnomecompat.xml
#exclude #{_datadir}/%{name}/kde.xml
%dir %{_datadir}/%{name}/cube
%dir %{_datadir}/%{name}/cube/images
%{_datadir}/%{name}/cube/images/*.png
%{_datadir}/%{name}/cubeaddon
%{_datadir}/%{name}/mag
%{_datadir}/%{name}/showmouse
%{_datadir}/%{name}/splash
%{_datadir}/applications/%{name}.desktop
%{_datadir}/compositing-wm/%{name}.defaults
%{_datadir}/%{name}/colorfilter/*
%{_datadir}/%{name}/notification/*
%{_datadir}/%{name}/scale/images/*.png
%{_datadir}/gnome-control-center/keybindings/50-compiz-*.xml

%files decorator-gtk
%{_bindir}/compiz-gtk
%{_bindir}/gtk-window-decorator
#{_sysconfdir}/gconf/schemas/gwd.schemas
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
%{python_sitelib}/ccsm-%{version}-py*.*.egg-info
%{_datadir}/applications/ccsm.desktop
%{_iconsdir}/hicolor/*/apps/ccsm.*
%config(noreplace) %{_sysconfdir}/compizconfig/config.conf

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
