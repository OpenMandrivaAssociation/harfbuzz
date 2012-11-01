%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %{name} %major
%define develname %mklibname %{name} -d

Summary:	OpenType text shaping engine
Name:		harfbuzz
Version:	0.9.5
Release:	1
License:	MIT
Group:		Development/Other
URL:		http://www.freedesktop.org/wiki/Software/HarfBuzz
Source0:	http://www.freedesktop.org/software/harfbuzz/release/%{name}-%{version}.tar.bz2
BuildRequires:	glib2-devel
BuildRequires:	cairo-devel
BuildRequires:	icu-devel
BuildRequires:	freetype-devel

%description
HarfBuzz is an OpenType text shaping engine.
There are two HarfBuzz code trees in existence today.

%package -n %{libname}
Summary:	Libraries for the %{name} package
Group:		System/Libraries

%description -n %{libname}
Libraries for %{name}.

%package -n %{develname}
Summary:	Headers and development libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
%{name} development headers and libraries.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std

find %{buildroot} -name *.la | xargs rm

%files
%{_bindir}/*

%files -n %{libname}
%doc AUTHORS README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*
