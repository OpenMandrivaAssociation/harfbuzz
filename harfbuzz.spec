# harfbuzz is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global optflags %{optflags} -O3

%define major 0
%define api 0.0
%define libname %mklibname %{name} %{major}
%define slibname %mklibname %{name}-subset %{major}
%define libicu %mklibname %{name}-icu %{major}
%define libgob %mklibname %{name}-gobject %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define slib32name %mklib32name %{name}-subset %{major}
%define lib32icu %mklib32name %{name}-icu %{major}
%define lib32gob %mklib32name %{name}-gobject %{major}
%define gir32name %mklib32name %{name}-gir %{api}
%define dev32name %mklib32name %{name} -d
%bcond_with bootstrap

Summary:	OpenType text shaping engine
Name:		harfbuzz
Version:	3.3.2
Release:	1
License:	MIT
Group:		Development/Other
Url:		http://www.freedesktop.org/wiki/Software/HarfBuzz
Source0:	https://github.com/harfbuzz/harfbuzz/releases/download/%{version}/harfbuzz-%{version}.tar.xz

%if !%{with bootstrap}
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
%endif
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(icu-uc) >= 60
BuildRequires:	pkgconfig(graphite2)
BuildRequires:	pkgconfig(fontconfig)
%if %{with compat32}
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libfontconfig)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libicuuc)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libffi)
%endif

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

%description -n %{libname}
Shared library for the %{name} package.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{slibname}
Summary:	Shared library for the %{name} subset package
Group:		System/Libraries

%description -n %{slibname}
Shared library for the %{name} subset package.

%files -n %{slibname}
%{_libdir}/lib%{name}-subset.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libicu}
Summary:	Shared ICU library for the %{name} package
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3

%description -n %{libicu}
Shared ICU library for the %{name} package.

%files -n %{libicu}
%{_libdir}/lib%{name}-icu.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libgob}
Summary:	Shared GObject library for the %{name} package
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3

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

%files -n %{girname}
%{_libdir}/girepository-1.0/HarfBuzz-%{api}.typelib

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers and development libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{slibname} = %{EVRD}
Requires:	%{libicu} = %{EVRD}
Requires:	%{libgob} = %{EVRD}
Requires:	%{girname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Conflicts:	harfbuzz < 0.9.28-3

%description -n %{devname}
%{name} development headers and libraries.

%files -n %{devname}
%doc AUTHORS README
%{_datadir}/gir-1.0/HarfBuzz-%{api}.gir
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/harfbuzz
%{_libdir}/*.so
%{_includedir}/*

#----------------------------------------------------------------------------
%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared library for the %{name} package (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
Shared library for the %{name} package.

%files -n %{lib32name}
%{_prefix}/lib/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{slib32name}
Summary:	Shared library for the %{name} subset package (32-bit)
Group:		System/Libraries

%description -n %{slib32name}
Shared library for the %{name} subset package.

%files -n %{slib32name}
%{_prefix}/lib/lib%{name}-subset.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{lib32icu}
Summary:	Shared ICU library for the %{name} package (32-bit)
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3

%description -n %{lib32icu}
Shared ICU library for the %{name} package.

%files -n %{lib32icu}
%{_prefix}/lib/lib%{name}-icu.so.%{major}*

#----------------------------------------------------------------------------

# We can probably get away without 32-bit gobject crap
%if 0
%package -n %{lib32gob}
Summary:	Shared GObject library for the %{name} package (32-bit)
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3

%description -n %{lib32gob}
Shared GObject library for the %{name} package.

%files -n %{lib32gob}
%{_prefix}/lib/lib%{name}-gobject.so.%{major}*

#----------------------------------------------------------------------------

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
NOCONFIGURE=1 ./autogen.sh

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--without-cairo
cd ..
%endif

mkdir build
cd build
%configure \
	--with-cairo=yes \
	--with-freetype=yes \
	--with-glib=yes \
	--with-gobject=yes \
	--with-graphite2=yes \
	--with-icu=yes \
	--with-fontconfig=yes \
	--enable-introspection

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build
