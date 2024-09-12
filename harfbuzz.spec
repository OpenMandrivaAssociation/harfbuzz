# harfbuzz is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%if %{cross_compiling}
# Workaround for libtool being a broken mess
%global prefer_gcc 1
%endif

%global optflags %{optflags} -O3

%define major 0
%define api 0.0
%define libname %mklibname %{name}
%define oldlibname %mklibname %{name} %{major}
%define calibname %mklibname %{name}-cairo
%define slibname %mklibname %{name}-subset
%define oldslibname %mklibname %{name}-subset %{major}
%define libicu %mklibname %{name}-icu
%define oldlibicu %mklibname %{name}-icu %{major}
%define libgob %mklibname %{name}-gobject
%define oldlibgob %mklibname %{name}-gobject %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname %{name} -d
%define cadev %mklibname %{name}-cairo -d
%define girdev %mklibname %{name}-gir -d
%define subdev %mklibname %{name}-subset -d
%define icudev %mklibname %{name}-icu -d
%define gobdev %mklibname %{name}-gobject -d
%define lib32name %mklib32name %{name}
%define oldlib32name %mklib32name %{name} %{major}
%define calib32name %mklib32name %{name}-cairo
%define slib32name %mklib32name %{name}-subset
%define oldslib32name %mklib32name %{name}-subset %{major}
%define lib32icu %mklib32name %{name}-icu
%define oldlib32icu %mklib32name %{name}-icu %{major}
%define lib32gob %mklib32name %{name}-gobject
%define oldlib32gob %mklib32name %{name}-gobject %{major}
%define gir32name %mklib32name %{name}-gir %{api}
%define dev32name %mklib32name %{name} -d
%bcond_with bootstrap
# Omitting gir is useful for multi-stage bootstrapping
# and for systems without gtk
%bcond_without gir

Summary:	OpenType text shaping engine
Name:		harfbuzz
Version:	9.0.0
Release:	3
License:	MIT
Group:		Development/Other
Url:		https://www.freedesktop.org/wiki/Software/HarfBuzz
Source0:	https://github.com/harfbuzz/harfbuzz/releases/download/%{version}/harfbuzz-%{version}.tar.xz

%if !%{with bootstrap}
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glib-2.0)
%if %{with gir}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
%else
BuildConflicts:	pkgconfig(gobject-introspection-1.0)
%endif
%endif
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(icu-uc) >= 60
BuildRequires:	pkgconfig(graphite2)
BuildRequires:	pkgconfig(fontconfig)
%if %{with compat32}
BuildRequires:	libc6
BuildRequires:	devel(libcairo)
BuildRequires:	devel(libpangocairo-1.0)
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libfontconfig)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libicuuc)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
%endif
BuildRequires:	meson

%description
HarfBuzz is an OpenType text shaping engine.
There are two HarfBuzz code trees in existence today.

%files
%if !%{with bootstrap}
%{_bindir}/*
%endif

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for the %{name} package
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Shared library for the %{name} package.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------
%package -n %{calibname}
Summary:	Shared library for the %{name} cairo package
Group:		System/Libraries

%description -n %{calibname}
Shared library for the %{name} cairo package.

%files -n %{calibname}
%{_libdir}/libharfbuzz-cairo.so.*

#----------------------------------------------------------------------------

%package -n %{slibname}
Summary:	Shared library for the %{name} subset package
Group:		System/Libraries
%rename %{oldslibname}

%description -n %{slibname}
Shared library for the %{name} subset package.

%files -n %{slibname}
%{_libdir}/lib%{name}-subset.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libicu}
Summary:	Shared ICU library for the %{name} package
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3
%rename %{oldlibicu}

%description -n %{libicu}
Shared ICU library for the %{name} package.

%files -n %{libicu}
%{_libdir}/lib%{name}-icu.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libgob}
Summary:	Shared GObject library for the %{name} package
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3
%rename %{oldlibgob}

%description -n %{libgob}
Shared GObject library for the %{name} package.

%files -n %{libgob}
%{_libdir}/lib%{name}-gobject.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface description for HarfBuzz
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{girname}
GObject Introspection interface description for HarfBuzz

%if %{with gir}
%files -n %{girname}
%{_libdir}/girepository-1.0/HarfBuzz-%{api}.typelib
%endif

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers and development libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{slibname} = %{EVRD}
Requires:	%{libicu} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Conflicts:	harfbuzz < 0.9.28-3

%description -n %{devname}
%{name} development headers and libraries.

%files -n %{devname}
%doc AUTHORS README
%{_libdir}/pkgconfig/harfbuzz.pc
%{_libdir}/pkgconfig/harfbuzz-subset.pc
%{_libdir}/cmake/harfbuzz
%{_libdir}/libharfbuzz.so
%{_libdir}/libharfbuzz-subset.so
%{_includedir}/*
%exclude %{_includedir}/harfbuzz/hb-cairo.h
%exclude %{_includedir}/harfbuzz/hb-icu.h
%exclude %{_includedir}/harfbuzz/hb-gobject*.h

#----------------------------------------------------------------------------
%package -n %{cadev}
Summary:	Headers and development libraries from %{name}'s cairo support
Group:		Development/C
Requires:	%{calibname} = %{EVRD}

%description -n %{cadev}
Headers and development libraries from %{name}'s cairo support

%files -n %{cadev}
%{_libdir}/pkgconfig/harfbuzz-cairo.pc
%{_includedir}/harfbuzz/hb-cairo.h
%{_libdir}/libharfbuzz-cairo.so

#----------------------------------------------------------------------------
%package -n %{icudev}
Summary:	Headers and development libraries from %{name}'s ICU support
Group:		Development/C
Requires:	%{libicu} = %{EVRD}

%description -n %{icudev}
Headers and development libraries from %{name}'s ICU support

%files -n %{icudev}
%{_libdir}/pkgconfig/harfbuzz-icu.pc
%{_includedir}/harfbuzz/hb-icu.h
%{_libdir}/libharfbuzz-icu.so

#----------------------------------------------------------------------------
%package -n %{gobdev}
Summary:	Headers and development libraries from %{name}'s gobject bindings
Group:		Development/C
Requires:	%{libgob} = %{EVRD}

%description -n %{gobdev}
Headers and development libraries from %{name}'s gobject bindings

%files -n %{gobdev}
%doc %{_datadir}/gtk-doc/html/harfbuzz
%{_libdir}/pkgconfig/harfbuzz-gobject.pc
%{_includedir}/harfbuzz/hb-gobject*.h
%{_libdir}/libharfbuzz-gobject.so

#----------------------------------------------------------------------------
%if %{with gir}
%package -n %{girdev}
Summary:	Headers and development libraries from %{name}'s gobject-introspection bindings
Group:		Development/C
%if %{with gir}
Requires:	%{girname} = %{EVRD}
%endif

%description -n %{girdev}
Headers and development libraries from %{name}'s gobject-introspection bindings

%files -n %{girdev}
%{_datadir}/gir-1.0/HarfBuzz-%{api}.gir
%endif

#----------------------------------------------------------------------------
%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared library for the %{name} package (32-bit)
Group:		System/Libraries
%rename %{oldlib32name}

%description -n %{lib32name}
Shared library for the %{name} package.

%files -n %{lib32name}
%{_prefix}/lib/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------
%package -n %{calib32name}
Summary:	Shared library for the %{name} cairo package (32-bit)
Group:		System/Libraries

%description -n %{calib32name}
Shared library for the %{name} cairo package.

%files -n %{calib32name}
%{_prefix}/lib/libharfbuzz-cairo.so.*


#----------------------------------------------------------------------------

%package -n %{slib32name}
Summary:	Shared library for the %{name} subset package (32-bit)
Group:		System/Libraries
%rename %{oldslib32name}

%description -n %{slib32name}
Shared library for the %{name} subset package.

%files -n %{slib32name}
%{_prefix}/lib/lib%{name}-subset.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{lib32icu}
Summary:	Shared ICU library for the %{name} package (32-bit)
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3
%rename %{oldlib32icu}

%description -n %{lib32icu}
Shared ICU library for the %{name} package.

%files -n %{lib32icu}
%{_prefix}/lib/lib%{name}-icu.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{lib32gob}
Summary:	Shared GObject library for the %{name} package (32-bit)
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3
%rename %{oldlib32gob}

%description -n %{lib32gob}
Shared GObject library for the %{name} package.

%files -n %{lib32gob}
%{_prefix}/lib/lib%{name}-gobject.so.%{major}*

#----------------------------------------------------------------------------

# We can get away with not having 32-bit GIR cruft
%if 0
%package -n %{gir32name}
Summary:	GObject Introspection interface description for HarfBuzz (32-bit)
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{gir32name}
GObject Introspection interface description for HarfBuzz

%files -n %{gir32name}
%{_prefix}/lib/girepository-1.0/HarfBuzz-%{api}.typelib
%endif

#----------------------------------------------------------------------------

%package -n %{dev32name}
Summary:	Headers and development libraries from %{name} (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}
Requires:	%{slib32name} = %{EVRD}
Requires:	%{lib32icu} = %{EVRD}
#Requires:	%{lib32gob} = %{EVRD}
#Requires:	%{gir32name} = %{EVRD}

%description -n %{dev32name}
%{name} development headers and libraries.

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/*
%{_prefix}/lib/cmake/harfbuzz
%{_prefix}/lib/*.so
%endif

#----------------------------------------------------------------------------

%prep
%autosetup -p1
%if %{with compat32}
%meson32 \
	-Dcairo=enabled \
	-Dchafa=disabled \
	-Dintrospection=disabled || :
if ! [ -e build32/build.ninja ]; then
	cat build32/meson-logs/meson-log.txt
	exit 1
fi
%endif

%meson \
	-Dchafa=disabled \
	-Dexperimental_api=true \
	-Dgraphite2=enabled \
%if %{with gir}
	-Dintrospection=enabled
%else
	-Dintrospection=disabled
%endif

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build
