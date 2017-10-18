%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %{name} %{major}
%define libicu %mklibname %{name}-icu %{major}
%define devname %mklibname %{name} -d
%bcond_with bootstrap

Summary:	OpenType text shaping engine
Name:		harfbuzz
Version:	1.4.8
Release:	1
License:	MIT
Group:		Development/Other
Url:		http://www.freedesktop.org/wiki/Software/HarfBuzz
Source0:	http://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.bz2
%if !%{with bootstrap}
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(graphite2)

%description
HarfBuzz is an OpenType text shaping engine.
There are two HarfBuzz code trees in existence today.

%files
%{_bindir}/*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for the %{name} package
Group:		System/Libraries

%description -n %{libname}
Shared library for the %{name} package.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

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
Requires:	%{libicu} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Conflicts:	harfbuzz < 0.9.28-3

%description -n %{devname}
%{name} development headers and libraries.

%files -n %{devname}
%doc AUTHORS README
%{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*

#----------------------------------------------------------------------------

%prep
%setup -q

%build
CXXFLAGS="%{optflags} -std=c++14" \
%configure \
	--disable-static \
	--with-graphite2

%make

%install
%makeinstall_std
