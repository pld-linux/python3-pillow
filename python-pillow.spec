#
# bootstrap building docs (pillow is required by docutils, docutils are
#  required by sphinx; pillow build-requires sphinx)

# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	pillow
Summary:	Python image processing library
Name:		python-%{module}
Version:	3.2.0
Release:	3
# License: see http://www.pythonware.com/products/pil/license.htm
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/e2/af/0a3981fffc5cd43078eb8b1057702e0dd2d5771e5aaa36cbd140e32f8473/Pillow-%{version}.tar.gz
# Source0-md5:	7cfd093c11205d9e2ebe3c51dfcad510
Patch0:		x32.patch
URL:		http://python-pillow.github.io/
BuildRequires:	freetype-devel
BuildRequires:	ghostscript
BuildRequires:	lcms2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel
BuildRequires:	openjpeg2-devel
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	tk-devel
BuildRequires:	zlib-devel
%if %{with python2}
BuildRequires:	python-PyQt4
BuildRequires:	python-cffi
BuildRequires:	python-devel
BuildRequires:	python-numpy
BuildRequires:	python-setuptools
BuildRequires:	python-tkinter
%endif
%if %{with doc}
BuildRequires:	python-Sphinx
BuildRequires:	python-sphinx_rtd_theme
%endif
%if %{with python3}
BuildRequires:	python3-PyQt4
BuildRequires:	python3-cffi
BuildRequires:	python3-devel
BuildRequires:	python3-numpy
BuildRequires:	python3-setuptools
BuildRequires:	python3-tkinter
%if %{with doc}
BuildRequires:	python3-sphinx
BuildRequires:	python3-sphinx_rtd_theme
%endif
%endif
# For EpsImagePlugin.py
Requires:	ghostscript
Provides:	python-PIL = %{version}-%{release}
Provides:	pythonegg(pil) = %{version}
Obsoletes:	python-PIL < 1:1.1.8

%define		py2_libbuilddir %(python -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')
%define		py3_libbuilddir %(python3 -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')

%description
Python image processing library, fork of the Python Imaging Library
(PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are five subpackages:
- tk (tk interface),
- qt (PIL image wrapper for Qt),
- devel (development),
- doc (documentation).

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-devel
Requires:	python-devel
Requires:	zlib-devel
Provides:	python-PIL-devel = %{version}-%{release}
Obsoletes:	python-PIL-devel < 1:1.1.8

%description devel
Development files for %{name}.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for %{name}.

%package tk
Summary:	Tk interface for %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-tkinter
Provides:	python-PIL-tk = %{version}-%{release}
Obsoletes:	python-PIL-tk < 1:1.1.8

%description tk
Tk interface for %{name}.

%package qt
Summary:	PIL image wrapper for Qt
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-PyQt4
Provides:	python-PIL-qt = %{version}-%{release}

%description qt
PIL image wrapper for Qt.

%package -n python3-%{module}
Summary:	Python 3 image processing library
Provides:	python3-PIL = %{version}-%{release}

%description -n python3-%{module}
Python image processing library, fork of the Python Imaging Library
(PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are five subpackages:
- tk (tk interface),
- qt (PIL image wrapper for Qt),
- devel (development),
- doc (documentation).

%package -n python3-%{module}-devel
Summary:	Development files for python3-%{module}
Group:		Development/Libraries
Requires:	libjpeg-devel
Requires:	python3-%{module} = %{version}-%{release}
Requires:	python3-devel
Requires:	zlib-devel

%description -n python3-%{module}-devel
Development files for python3-%{module}.

%package -n python3-%{module}-doc
Summary:	Documentation for python3-%{module}
Group:		Documentation
Requires:	python3-%{module} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n python3-%{module}-doc
Documentation for python3-%{module}.

%package -n python3-%{module}-tk
Summary:	Tk interface for python3-%{module}
Group:		Libraries
Requires:	python-tkinter
Requires:	python3-%{module} = %{version}-%{release}

%description -n python3-%{module}-tk
Tk interface for python3-%{module}.

%package -n python3-%{module}-qt
Summary:	PIL image wrapper for Qt
Group:		Libraries
Requires:	python3-%{module} = %{version}-%{release}
Requires:	python3-PyQt4
Obsoletes:	python3-%{module} <= 2.0.0-5.git93a488e8

%description -n python3-%{module}-qt
PIL image wrapper for Qt.

%prep
%setup -q -n Pillow-%{version}

%if "%{_lib}" == "libx32"
%patch0 -p1
%endif

# Strip shebang on non-executable file
sed -i 1d PIL/OleFileIO.py

# Fix file encoding
iconv --from=ISO-8859-1 --to=UTF-8 PIL/WalImageFile.py > PIL/WalImageFile.py.new && \
touch -r PIL/WalImageFile.py PIL/WalImageFile.py.new && \
mv PIL/WalImageFile.py.new PIL/WalImageFile.py

# Make sample scripts non-executable
chmod -x Scripts/pilprint.py

%build
%py_build

%if %{with doc}
cd docs
PYTHONPATH=$PWD/../build-2/%{py2_libbuilddir} %{__make} html
rm -f _build/html/.buildinfo
cd ..
%endif

%if %{with python3}
%py3_build

%if %{with doc}
cd docs
PYTHONPATH=$PWD/../build-3/%{py3_libbuilddir} %{__make} html SPHINXBUILD=sphinx-build-%python3_version
rm -f _build/html/.buildinfo
cd ..
%endif
%endif

%if %{with tests}
# Check Python 2 modules
ln -s $PWD/Images $PWD/build-2/%py2_libbuilddir/Images
cp -R $PWD/Tests $PWD/build-2/%py2_libbuilddir/Tests
cp -R $PWD/selftest.py $PWD/build-2/%py2_libbuilddir/selftest.py
cd build-2/%py2_libbuilddir
PYTHONPATH=$PWD %{__python} selftest.py
cd ..

%if %{with python3}
# Check Python 3 modules
ln -s $PWD/Images $PWD/build-3/%py3_libbuilddir/Images
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
install -d $RPM_BUILD_ROOT/%{py_incdir}/Imaging
cp -p libImaging/*.h $RPM_BUILD_ROOT/%{py_incdir}/Imaging
%py_install

%py_postclean
%endif

# Fix non-standard-executable-perm
chmod +x $RPM_BUILD_ROOT%{py_sitedir}/PIL/*.so

%if %{with python3}
# Install Python 3 modules
install -d $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
cp -p libImaging/*.h $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
%py3_install

# Fix non-standard-executable-perm
chmod +x $RPM_BUILD_ROOT%{py3_sitedir}/PIL/*.so
%endif

# The scripts are packaged in %doc
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst CHANGES.rst docs/COPYING
%dir %{py_sitedir}/PIL
%{py_sitedir}/PIL/*.py[co]
%{py_sitedir}/PIL/OleFileIO-README.md
%attr(755,root,root) %{py_sitedir}/PIL/_*.so
%{py_sitedir}/Pillow-%{version}-py*.egg-info

# These are in subpackages
%exclude %{py_sitedir}/PIL/_imagingtk*
%exclude %{py_sitedir}/PIL/ImageTk*
%exclude %{py_sitedir}/PIL/SpiderImagePlugin*
%exclude %{py_sitedir}/PIL/ImageQt*

%files devel
%defattr(644,root,root,755)
%{py_incdir}/Imaging

%files doc
%defattr(644,root,root,755)
%doc Scripts
%if %{with doc}
%doc docs/_build/html
%endif

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/PIL/_imagingtk.so
%{py_sitedir}/PIL/ImageTk.py[co]
%{py_sitedir}/PIL/SpiderImagePlugin.py[co]

%files qt
%defattr(644,root,root,755)
%{py_sitedir}/PIL/ImageQt.py[co]

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst CHANGES.rst docs/COPYING
%{py3_sitedir}/*
# These are in subpackages
%exclude %{py3_sitedir}/PIL/_imagingtk*
%exclude %{py3_sitedir}/PIL/ImageTk*
%exclude %{py3_sitedir}/PIL/SpiderImagePlugin*
%exclude %{py3_sitedir}/PIL/ImageQt*

%files -n python3-%{module}-devel
%defattr(644,root,root,755)
%{py3_incdir}/Imaging

%files -n python3-%{module}-doc
%defattr(644,root,root,755)
%doc Scripts
%if %{with doc}
%doc docs/_build/html
%endif

%files -n python3-%{module}-tk
%defattr(644,root,root,755)
%{py3_sitedir}/PIL/_imagingtk*
%{py3_sitedir}/PIL/ImageTk*
%{py3_sitedir}/PIL/SpiderImagePlugin*

%files -n python3-%{module}-qt
%defattr(644,root,root,755)
%{py3_sitedir}/PIL/ImageQt*
%endif
