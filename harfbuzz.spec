%global optflags %{optflags} -O3

%define major 0
%define api 0.0
%define libname %mklibname %{name} %{major}
%define slibname %mklibname %{name}-subset %{major}
%define libicu %mklibname %{name}-icu %{major}
%define libgob %mklibname %{name}-gobject %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname %{name} -d
%bcond_with bootstrap

Summary:	OpenType text shaping engine
Name:		harfbuzz
Version:	2.6.4
Release:	2
License:	MIT
Group:		Development/Other
Url:		http://www.freedesktop.org/wiki/Software/HarfBuzz
Source0:	http://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.xz
%if !%{with bootstrap}
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
%endif
BuildRequires:	pkgconfig(icu-uc) >= 60
BuildRequires:	pkgconfig(graphite2)

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

%prep
%autosetup -p1
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--with-cairo=yes \
	--with-freetype=yes \
	--with-glib=yes \
	--with-gobject=yes \
	--with-graphite2=yes \
	--with-icu=yes \
	--with-fontconfig=yes \
	--enable-introspection

%make_build

%install
%make_install
