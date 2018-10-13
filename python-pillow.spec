# NOTE: -qt supports PyQt5 > PyQt4 > PySide modules (in order of preference)
#
# bootstrap building docs (pillow is required by docutils, docutils are
#  required by sphinx; pillow build-requires sphinx)

# Conditional build:
%bcond_with	doc	# Sphinx documentation (crashes - without DISPLAY?)
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	pillow
Summary:	Python 2 image processing library
Summary(pl.UTF-8):	Biblioteka do przetwarzania obrazów dla Pythona 2
Name:		python-%{module}
Version:	5.3.0
Release:	1
# License: see http://www.pythonware.com/products/pil/license.htm
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pillow/
Source0:	https://files.pythonhosted.org/packages/source/P/Pillow/Pillow-%{version}.tar.gz
# Source0-md5:	0da5a4c9c548aa5cfe999302aea8c8f1
Patch0:		%{name}-subpackage.patch
Patch1:		x32.patch
URL:		http://python-pillow.github.io/
BuildRequires:	freetype-devel >= 2
BuildRequires:	ghostscript
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libimagequant-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libraqm-devel
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	tk-devel
BuildRequires:	zlib-devel
%if %{with python2}
BuildRequires:	python-cffi
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-numpy
BuildRequires:	python-setuptools
BuildRequires:	python-tkinter
%endif
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-2
%endif
%if %{with python3}
BuildRequires:	python3-cffi
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-numpy
BuildRequires:	python3-setuptools
BuildRequires:	python3-tkinter
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
%endif
# For EpsImagePlugin.py
Requires:	ghostscript
Provides:	python-PIL = %{version}-%{release}
Provides:	pythonegg(pil) = %{version}
Obsoletes:	python-PIL < 1:1.1.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		py2_libbuilddir %(python -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')
%define		py3_libbuilddir %(python3 -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')

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
Requires:	python-devel >= 1:2.7
Requires:	zlib-devel
Provides:	python-PIL-devel = %{version}-%{release}
Obsoletes:	python-PIL-devel < 1:1.1.8

%description devel
Development files for Pillow module.

%description devel -l pl.UTF-8
Pliki programistyczne modułu Pillow.

%package doc
Summary:	Documentation for Pillow module
Summary(pl.UTF-8):	Dokumentacja do modułu Pillow
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for Pillow module.

%description doc -l pl.UTF-8
Dokumentacja do modułu Pillow.

%package tk
Summary:	Tk interface for Pillow module
Summary(pl.UTF-8):	Interfejs Tk do modułu Pillow
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-tkinter
Provides:	python-PIL-tk = %{version}-%{release}
Obsoletes:	python-PIL-tk < 1:1.1.8

%description tk
Tk interface for Pillow module.

%description tk -l pl.UTF-8
Interfejs Tk do modułu Pillow.

%package qt
Summary:	PIL image wrapper for Qt
Summary(pl.UTF-8):	Obudowanie obrazów PIL dla Qt
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-PyQt4
Provides:	python-PIL-qt = %{version}-%{release}

%description qt
PIL image wrapper for Qt.

%description qt -l pl.UTF-8
Obudowanie obrazów PIL dla Qt.

%package -n python3-%{module}
Summary:	Python 3 image processing library
Summary(pl.UTF-8):	Biblioteka do przetwarzania obrazów dla Pythona 3
Group:		Libraries/Python
Provides:	python3-PIL = %{version}-%{release}

%description -n python3-%{module}
Python image processing library, fork of the Python Imaging Library
(PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are four additional subpackages:
- tk (tk interface),
- qt (PIL image wrapper for Qt),
- devel (development),
- doc (documentation).

%description -n python3-%{module} -l pl.UTF-8
Pythonowa biblioteka do przetwarzania obrazów - odgałęzienie projektu
PIL (Python Imaging Library).

Ta biblioteka zapewnia obsługę wielu formatów plików, wydajną
reprezentację wewnętrzną oraz potężne możliwości przetwarzania.

Są cztery dodatkowe podpakiety:
- tk (interfejs Tk),
- qt (obudowanie obrazów PIL dla Qt),
- devel (do programowania),
- doc (dokumentacja).

%package -n python3-%{module}-devel
Summary:	Development files for Pillow module
Summary(pl.UTF-8):	Pliki programistyczne modułu Pillow
Group:		Development/Libraries
Requires:	libjpeg-devel
Requires:	python3-%{module} = %{version}-%{release}
Requires:	python3-devel >= 1:3.4
Requires:	zlib-devel

%description -n python3-%{module}-devel
Development files for Pillow module.

%description -n python3-%{module}-devel -l pl.UTF-8
Pliki programistyczne modułu Pillow.

%package -n python3-%{module}-doc
Summary:	Documentation for Pillow module
Summary(pl.UTF-8):	Dokumentacja do modułu Pillow
Group:		Documentation
Requires:	python3-%{module} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n python3-%{module}-doc
Documentation for Pillow module.

%description -n python3-%{module}-doc -l pl.UTF-8
Dokumentacja do modułu Pillow.

%package -n python3-%{module}-tk
Summary:	Tk interface for Pillow module
Summary(pl.UTF-8):	Interfejs Tk do modułu Pillow
Group:		Libraries/Python
Requires:	python-tkinter
Requires:	python3-%{module} = %{version}-%{release}

%description -n python3-%{module}-tk
Tk interface for Pillow module.

%description -n python3-%{module}-tk -l pl.UTF-8
Interfejs Tk do modułu Pillow.

%package -n python3-%{module}-qt
Summary:	PIL image wrapper for Qt
Summary(pl.UTF-8):	Obudowanie obrazów PIL dla Qt
Group:		Libraries/Python
Requires:	python3-%{module} = %{version}-%{release}
Requires:	python3-PyQt4
Obsoletes:	python3-%{module} <= 2.0.0-5.git93a488e8

%description -n python3-%{module}-qt
PIL image wrapper for Qt.

%description -n python3-%{module}-qt -l pl.UTF-8
Obudowanie obrazów PIL dla Qt.

%prep
%setup -q -n Pillow-%{version}
%patch0 -p1
%if "%{_lib}" == "libx32"
%patch1 -p1
%endif

# Strip shebang on non-executable file
#sed -i 1d PIL/OleFileIO.py

# Fix file encoding
iconv --from=ISO-8859-1 --to=UTF-8 PIL/WalImageFile.py > PIL/WalImageFile.py.new && \
touch -r PIL/WalImageFile.py PIL/WalImageFile.py.new && \
%{__mv} PIL/WalImageFile.py.new PIL/WalImageFile.py

%build
%py_build

%if %{with doc}
PYTHONPATH=$(pwd)/build-2/%{py2_libbuilddir} \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%if %{with python3}
%py3_build

%if %{with doc}
PYTHONPATH=$(pwd)/build-3/%{py3_libbuilddir} \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif
%endif

%if %{with tests}
# Check Python 2 modules
cp -R $PWD/Tests $PWD/build-2/%py2_libbuilddir/Tests
cp -R $PWD/selftest.py $PWD/build-2/%py2_libbuilddir/selftest.py
cd build-2/%py2_libbuilddir
PYTHONPATH=$PWD %{__python} selftest.py
cd ../..

%if %{with python3}
# Check Python 3 modules
cp -R $PWD/Tests $PWD/build-3/%py3_libbuilddir/Tests
cp -R $PWD/selftest.py $PWD/build-3/%py3_libbuilddir/selftest.py
cd build-3/%py3_libbuilddir
PYTHONPATH=$PWD %{__python3} selftest.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
# Install Python 2 modules
install -d $RPM_BUILD_ROOT%{py_incdir}/Imaging
cp -p src/libImaging/*.h $RPM_BUILD_ROOT%{py_incdir}/Imaging
%py_install

# Fix non-standard-executable-perm
chmod +x $RPM_BUILD_ROOT%{py_sitedir}/PIL/*.so

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/{Tests,selftest.py*}
%py_postclean
%endif

%if %{with python3}
# Install Python 3 modules
install -d $RPM_BUILD_ROOT%{py3_incdir}/Imaging
cp -p src/libImaging/*.h $RPM_BUILD_ROOT%{py3_incdir}/Imaging
%py3_install

# Fix non-standard-executable-perm
chmod +x $RPM_BUILD_ROOT%{py3_sitedir}/PIL/*.so

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/{Tests,selftest.py,__pycache__/selftest.*}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst docs/COPYING
%dir %{py_sitedir}/PIL
%{py_sitedir}/PIL/*.py[co]
%attr(755,root,root) %{py_sitedir}/PIL/_imaging.so
%attr(755,root,root) %{py_sitedir}/PIL/_imagingcms.so
%attr(755,root,root) %{py_sitedir}/PIL/_imagingft.so
%attr(755,root,root) %{py_sitedir}/PIL/_imagingmath.so
%attr(755,root,root) %{py_sitedir}/PIL/_imagingmorph.so
%attr(755,root,root) %{py_sitedir}/PIL/_webp.so
%{py_sitedir}/Pillow-%{version}-py*.egg-info
# These are in subpackages
%exclude %{py_sitedir}/PIL/ImageQt.py*
%exclude %{py_sitedir}/PIL/ImageTk.py*
%exclude %{py_sitedir}/PIL/SpiderImagePlugin.py*
%exclude %{py_sitedir}/PIL/_tkinter_finder.py*

%files devel
%defattr(644,root,root,755)
%{py_incdir}/Imaging

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/PIL/_imagingtk.so
%{py_sitedir}/PIL/ImageTk.py[co]
%{py_sitedir}/PIL/SpiderImagePlugin.py[co]
%{py_sitedir}/PIL/_tkinter_finder.py[co]

%files qt
%defattr(644,root,root,755)
%{py_sitedir}/PIL/ImageQt.py[co]

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst docs/COPYING
%dir %{py3_sitedir}/PIL
%{py3_sitedir}/PIL/*.py
%attr(755,root,root) %{py3_sitedir}/PIL/_imaging.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingcms.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingft.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingmath.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_imagingmorph.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/PIL/_webp.cpython-*.so
%dir %{py3_sitedir}/PIL/__pycache__
%{py3_sitedir}/PIL/__pycache__/*.py[co]
%{py3_sitedir}/Pillow-%{version}-py*.egg-info
# These are in subpackages
%exclude %{py3_sitedir}/PIL/ImageQt.py
%exclude %{py3_sitedir}/PIL/ImageTk.py
%exclude %{py3_sitedir}/PIL/SpiderImagePlugin.py
%exclude %{py3_sitedir}/PIL/_tkinter_finder.py
%exclude %{py3_sitedir}/PIL/__pycache__/ImageQt.cpython-*.py[co]
%exclude %{py3_sitedir}/PIL/__pycache__/ImageTk.cpython-*.py[co]
%exclude %{py3_sitedir}/PIL/__pycache__/SpiderImagePlugin.cpython-*.py[co]
%exclude %{py3_sitedir}/PIL/__pycache__/_tkinter_finder.cpython-*.py[co]

%files -n python3-%{module}-devel
%defattr(644,root,root,755)
%{py3_incdir}/Imaging

%if %{with doc}
%files -n python3-%{module}-doc
%defattr(644,root,root,755)
%doc docs/_build/html
%endif

%files -n python3-%{module}-tk
%defattr(644,root,root,755)
%{py3_sitedir}/PIL/_imagingtk.cpython-*.so
%{py3_sitedir}/PIL/ImageTk.py
%{py3_sitedir}/PIL/SpiderImagePlugin.py
%{py3_sitedir}/PIL/_tkinter_finder.py
%{py3_sitedir}/PIL/__pycache__/ImageTk.cpython-*.py[co]
%{py3_sitedir}/PIL/__pycache__/SpiderImagePlugin.cpython-*.py[co]
%{py3_sitedir}/PIL/__pycache__/_tkinter_finder.cpython-*.py[co]

%files -n python3-%{module}-qt
%defattr(644,root,root,755)
%{py3_sitedir}/PIL/ImageQt.py
%{py3_sitedir}/PIL/__pycache__/ImageQt.cpython-*.py[co]
%endif
