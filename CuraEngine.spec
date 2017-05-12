%define oname CuraEngine
%define lname %(echo %oname | tr [:upper:] [:lower:])

Summary:	An engine for processing 3D models into G-code instructions for 3D printers
Name:		%{oname}
Version:	2.3.1
Release:	1
Group:		Development/Other
License:	AGPLv3+
URL:		https://github.com/Ultimaker/%{name}
Source0:	https://github.com/Ultimaker/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{oname}-2.3.1-CMakeLists.patch
Patch1:		%{oname}-2.3.1-exclude-failing-test.patch

BuildRequires:	cmake
BuildRequires:	cmake(Arcus)
BuildRequires:	cmake(RapidJSON)
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	protobuf-compiler > 3.0.0
BuildRequires:	pkgconfig(polyclipping) >= 6.1.2
BuildRequires:	pkgconfig(protobuf) > 3.0.0
# for tests
BuildRequires:	python
BuildRequires:	pkgconfig(cppunit)

%description
CuraEngine is a powerful, fast and robust engine for processing 3D
models into 3D printing instruction for Ultimaker and other GCode
based 3D printers.

It is part of the larger open source project called "Cura".

%files
%{_bindir}/%{name}
%doc docs/html
%doc README.md
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q

# Apply all patches
%patch0 -p1 -b .orig
#patch1 -p1 -b .orig

# bundle libs
rm -rf libs/clipper
rm -rf libs/rapidjson

# use polyclipping for clipper
sed -i -e 's|#include <clipper/clipper.hpp>|#include <polyclipping/clipper.hpp>|' src/utils/*.h src/raft.cpp

%build
%cmake \
	-DENABLE_ARCUS:BOOL=ON \
	-DCMAKE_SKIP_RPATH:BOOL=ON \
	-DBUILD_TESTS:BOOL=ON \
	-DCMAKE_BUILD_TYPE=Debug \
	%{nil}
%make

# documentation
%make doc

%install
%makeinstall_std -C build

%check
%make test -C build

