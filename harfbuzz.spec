%global optflags %{optflags} -O3
%define major 0
%define libname %mklibname %{name} %{major}
%define slibname %mklibname %{name}-subset %{major}
%define libicu %mklibname %{name}-icu %{major}
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
BuildRequires:	cmake
BuildRequires:	ninja
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
Summary:	Shared library for the %{name} package
Group:		System/Libraries
Conflicts:	%{_lib}harfbuzz0 < 0.9.28-3

%description -n %{libicu}
Shared library for the %{name} package.

%files -n %{libicu}
%{_libdir}/lib%{name}-icu.so.%{major}*

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
%{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/harfbuzz
%{_libdir}/*.so
%{_includedir}/*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
%if !%{with bootstrap}
    -DHB_HAVE_FREETYPE=ON \
    -DHB_HAVE_GRAPHITE2=ON \
    -DHB_HAVE_GLIB=ON \
    -DHB_HAVE_GOBJECT=ON \
    -DHB_HAVE_INTROSPECTION=ON \
%endif
    -DHB_HAVE_ICU=ON \
    -G Ninja

%ninja_build

%install
%ninja_install
