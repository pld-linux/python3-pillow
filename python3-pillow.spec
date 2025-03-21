# NOTE: -qt supports PyQt5 > PySide2 modules (in order of preference)
#
# bootstrap building docs (pillow is required by docutils, docutils are
#  required by sphinx; pillow build-requires sphinx)

# Conditional build:
%bcond_with	doc	# Sphinx documentation (crashes - without DISPLAY?)
%bcond_without	tests	# unit tests

%define		module	pillow
Summary:	Python 3 image processing library
Summary(pl.UTF-8):	Biblioteka do przetwarzania obrazów dla Pythona 3
Name:		python3-%{module}
Version:	11.1.0
Release:	1
# License: see http://www.pythonware.com/products/pil/license.htm
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pillow/
Source0:	https://files.pythonhosted.org/packages/source/P/Pillow/pillow-%{version}.tar.gz
# Source0-md5:	ede5dce0bbbeff02099e2e297919a82a
Patch1:		x32.patch
URL:		https://python-pillow.org/
BuildRequires:	freetype-devel >= 2
BuildRequires:	ghostscript
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libimagequant-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libraqm-devel
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libwebp-devel
BuildRequires:	libxcb-devel
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	pkgconfig
BuildRequires:	python3-cffi
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-setuptools >= 1:67.8
BuildRequires:	python3-tkinter
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tk-devel
BuildRequires:	zlib-devel
%if %{with tests}
BuildRequires:	python3-olefile
%endif
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-olefile
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_inline_tabs
BuildRequires:	python3-sphinxext.opengraph
BuildRequires:	sphinx-pdg-3 >= 8.1
%endif
# For EpsImagePlugin.py
Requires:	ghostscript
Provides:	python3-PIL = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python image processing library, fork of the Python Imaging Library
(PIL).

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are four additional subpackages:
- tk (Tk interface),
- qt (PIL image wrapper for Qt),
- devel (development),
- doc (documentation).

%description -l pl.UTF-8
Pythonowa biblioteka do przetwarzania obrazów - odgałęzienie projektu
PIL (Python Imaging Library).

Ta biblioteka zapewnia obsługę wielu formatów plików, wydajną
reprezentację wewnętrzną oraz potężne możliwości przetwarzania.

Są cztery dodatkowe podpakiety:
- tk (interfejs Tk),
- qt (obudowanie obrazów PIL dla Qt),
- devel (do programowania),
- doc (dokumentacja).

%package devel
Summary:	Development files for Pillow module
Summary(pl.UTF-8):	Pliki programistyczne modułu Pillow
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-devel
Requires:	python3-devel >= 1:3.9
Requires:	zlib-devel

%description devel
Development files for Pillow module.

%description devel -l pl.UTF-8
Pliki programistyczne modułu Pillow.

%package doc
Summary:	Documentation for Pillow module
Summary(pl.UTF-8):	Dokumentacja do modułu Pillow
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for Pillow module.

%description doc -l pl.UTF-8
Dokumentacja do modułu Pillow.

%package tk
Summary:	Tk interface for Pillow module
Summary(pl.UTF-8):	Interfejs Tk do modułu Pillow
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-tkinter >= 1:3.9

%description tk
Tk interface for Pillow module.

%description tk -l pl.UTF-8
Interfejs Tk do modułu Pillow.

%package qt
Summary:	PIL image wrapper for Qt
Summary(pl.UTF-8):	Obudowanie obrazów PIL dla Qt
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-PyQt5 >= 5

%description qt
PIL image wrapper for Qt.

%description qt -l pl.UTF-8
Obudowanie obrazów PIL dla Qt.

%prep
%setup -q -n pillow-%{version}
%if "%{_lib}" == "libx32"
%patch -P 1 -p1
%endif

%build
%py3_build

libbuilddir="$(cd build-3 ; echo lib.*)"
%if %{with doc}
PYTHONPATH=$(pwd)/build-3/${libbuilddir} \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%if %{with tests}
# Check Python 3 modules
cp -R $PWD/Tests $PWD/build-3/${libbuilddir}/Tests
cp -R $PWD/selftest.py $PWD/build-3/${libbuilddir}/selftest.py
cd build-3/${libbuilddir}
PYTHONPATH=$PWD \
%{__python3} selftest.py
cd ../..
# qt test crashes without DISPLAY
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$PWD/build-3/${libbuilddir} \
%{__python3} -m pytest Tests -k 'not test_qt_image_qapplication'
%{__rm} -r build-3/${libbuilddir}/Tests
%{__rm} build-3/${libbuilddir}/selftest.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

# Install Python 3 modules
install -d $RPM_BUILD_ROOT%{py3_incdir}/Imaging
cp -p src/libImaging/*.h $RPM_BUILD_ROOT%{py3_incdir}/Imaging
%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.md
%dir %{py3_sitedir}/PIL
%{py3_sitedir}/PIL/*.py
%{py3_sitedir}/PIL/*.pyi
%{py3_sitedir}/PIL/py.typed
%attr(755,root,root) %{py3_sitedir}/PIL/_imaging.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingcms.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingft.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingmath.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingmorph.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_webp.cpython-*.so
%dir %{py3_sitedir}/PIL/__pycache__
%{py3_sitedir}/PIL/__pycache__/*.py[co]
%{py3_sitedir}/pillow-%{version}-py*.egg-info
# These are in subpackages
%exclude %{py3_sitedir}/PIL/ImageQt.py
%exclude %{py3_sitedir}/PIL/ImageTk.py
%exclude %{py3_sitedir}/PIL/SpiderImagePlugin.py
%exclude %{py3_sitedir}/PIL/_tkinter_finder.py
%exclude %{py3_sitedir}/PIL/__pycache__/ImageQt.cpython-*.py[co]
%exclude %{py3_sitedir}/PIL/__pycache__/ImageTk.cpython-*.py[co]
%exclude %{py3_sitedir}/PIL/__pycache__/SpiderImagePlugin.cpython-*.py[co]
%exclude %{py3_sitedir}/PIL/__pycache__/_tkinter_finder.cpython-*.py[co]

%files devel
%defattr(644,root,root,755)
%{py3_incdir}/Imaging

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html
%endif

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingtk.cpython-*.so
%{py3_sitedir}/PIL/ImageTk.py
%{py3_sitedir}/PIL/SpiderImagePlugin.py
%{py3_sitedir}/PIL/_tkinter_finder.py
%{py3_sitedir}/PIL/__pycache__/ImageTk.cpython-*.py[co]
%{py3_sitedir}/PIL/__pycache__/SpiderImagePlugin.cpython-*.py[co]
%{py3_sitedir}/PIL/__pycache__/_tkinter_finder.cpython-*.py[co]

%files qt
%defattr(644,root,root,755)
%{py3_sitedir}/PIL/ImageQt.py
%{py3_sitedir}/PIL/__pycache__/ImageQt.cpython-*.py[co]
