#
# bootstrap building docs (pillow is required by docutils, docutils are
#  required by sphinx; pillow build-requires sphinx)
# TODO:
# - python3: missing python3-PyQt4

# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	pillow
Summary:	Python image processing library
Name:		python-%{module}
Version:	2.6.1
Release:	0.1
# License: see http://www.pythonware.com/products/pil/license.htm
License:	MIT
Group:		Libraries/Python
Source0:	https://github.com/python-pillow/Pillow/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9f27c63e7a662a5d8d99abbebe29dc51
URL:		http://python-pillow.github.io/
BuildRequires:	freetype-devel
BuildRequires:	ghostscript
BuildRequires:	lcms2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libwebp-devel
BuildRequires:	openjpeg2-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sane-backends-devel
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
BuildRequires:	python-sphinx-theme-better
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
BuildRequires:	python3-sphinx-theme-better
%endif
%endif
# For EpsImagePlugin.py
Requires:	ghostscript
Provides:	python-PIL = %{version}-%{release}
Obsoletes:	python-PIL < 1.1.8

%define		py2_incdir %{_includedir}/python%{python_version}
%define		py3_incdir %{_includedir}/python%{python3_version}
%define		py2_libbuilddir %(python -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')
%define		py3_libbuilddir %(python3 -c 'import sys; import sysconfig; print("lib.{p}-{v[0]}.{v[1]}".format(p=sysconfig.get_platform(), v=sys.version_info))')

%description
Python image processing library, fork of the Python Imaging Library
(PIL)

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

There are five subpackages: tk (tk interface), qt (PIL image wrapper
for Qt), sane (scanning devices interface), devel (development) and
doc (documentation).

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-devel
Requires:	python-devel
Requires:	zlib-devel
Provides:	python-PIL-devel = %{version}-%{release}
Obsoletes:	python-PIL-devel < 1.1.8

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

%package sane
Summary:	Python module for using scanners
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	python-PIL-sane = %{version}-%{release}
Obsoletes:	python-PIL-sane < 1.1.8

%description sane
This package contains the sane module for Python which provides access
to various raster scanning devices such as flatbed scanners and
digital cameras.

%package tk
Summary:	Tk interface for %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-tkinter
Provides:	python-PIL-tk = %{version}-%{release}
Obsoletes:	python-PIL-tk < 1.1.8

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

There are five subpackages: tk (tk interface), qt (PIL image wrapper
for Qt), sane (scanning devices interface), devel (development) and
doc (documentation).

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

%package -n python3-%{module}-sane
Summary:	Python module for using scanners
Group:		Libraries
Requires:	python3-%{module} = %{version}-%{release}

%description -n python3-%{module}-sane
This package contains the sane module for Python which provides access
to various raster scanning devices such as flatbed scanners and
digital cameras.

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

# Fix spurious-executable-perm
chmod -x libImaging/Jpeg2KEncode.c

# Strip shebang on non-executable file
sed -i 1d PIL/OleFileIO.py

# Fix file encoding
iconv --from=ISO-8859-1 --to=UTF-8 PIL/WalImageFile.py > PIL/WalImageFile.py.new && \
touch -r PIL/WalImageFile.py PIL/WalImageFile.py.new && \
mv PIL/WalImageFile.py.new PIL/WalImageFile.py

%if %{with python3}
# Create Python 3 source tree
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
# Build Python 2 modules
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python}|'
CFLAGS="%{rpmcflags}" %{__python} setup.py build

cd Sane
CFLAGS="%{rpmcflags}" %{__python} setup.py build
cd ..

%if %{with doc}
cd docs
PYTHONPATH=$PWD/../build/%py2_libbuilddir %{__make} html
rm -f _build/html/.buildinfo
cd ..
%endif

%if %{with python3}
# Build Python 3 modules
cd %{py3dir}
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python3}|'
CFLAGS="%{rpmcflags}" %{__python3} setup.py build

cd Sane
CFLAGS="%{rpmcflags}" %{__python3} setup.py build
cd ..

%if %{with doc}
cd docs
PYTHONPATH=$PWD/../build/%py3_libbuilddir make html SPHINXBUILD=sphinx-build-%python3_version
rm -f _build/html/.buildinfo
cd ..
%endif
cd ..
%endif

%if %{with tests}
# Check Python 2 modules
ln -s $PWD/Images $PWD/build/%py2_libbuilddir/Images
cp -R $PWD/Tests $PWD/build/%py2_libbuilddir/Tests
cp -R $PWD/selftest.py $PWD/build/%py2_libbuilddir/selftest.py
cd build/%py2_libbuilddir
PYTHONPATH=$PWD %{__python} selftest.py
cd ..

%if %{with python3}
# Check Python 3 modules
cd %{py3dir}
ln -s $PWD/Images $PWD/build/%py3_libbuilddir/Images
cp -R $PWD/Tests $PWD/build/%py3_libbuilddir/Tests
cp -R $PWD/selftest.py $PWD/build/%py3_libbuilddir/selftest.py
cd build/%py3_libbuilddir
PYTHONPATH=$PWD %{__python3} selftest.py
cd ../..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
# Install Python 2 modules
install -d $RPM_BUILD_ROOT/%{py2_incdir}/Imaging
cp -p libImaging/*.h $RPM_BUILD_ROOT/%{py2_incdir}/Imaging
%{__python} setup.py install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd Sane
%{__python} setup.py install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd ..

%py_postclean
%endif

# Fix non-standard-executable-perm
chmod +x $RPM_BUILD_ROOT%{py_sitedir}/PIL/*.so
chmod +x $RPM_BUILD_ROOT%{py_sitedir}/*.so

%if %{with python3}
# Install Python 3 modules
cd %{py3dir}
install -d $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
cp -p libImaging/*.h $RPM_BUILD_ROOT/%{py3_incdir}/Imaging
%{__python3} setup.py install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd Sane
%{__python3} setup.py install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd ../..

# Fix non-standard-executable-perm
chmod +x $RPM_BUILD_ROOT%{python3_sitearch}/PIL/*.so
chmod +x $RPM_BUILD_ROOT%{python3_sitearch}/*.so
%endif

# The scripts are packaged in %doc
rm -rf $RPM_BUILD_ROOT%{_bindir}

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
%exclude %{py_sitedir}/*sane*
%exclude %{py_sitedir}/PIL/_imagingtk*
%exclude %{py_sitedir}/PIL/ImageTk*
%exclude %{py_sitedir}/PIL/SpiderImagePlugin*
%exclude %{py_sitedir}/PIL/ImageQt*

%files devel
%defattr(644,root,root,755)
%{py2_incdir}/Imaging

%files doc
%defattr(644,root,root,755)
%doc Scripts
%if %{with doc}
%doc docs/_build/html
%endif

%files sane
%defattr(644,root,root,755)
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%attr(755,root,root) %{py_sitedir}/_sane.so
%{py_sitedir}/sane.py[co]
%{py_sitedir}/pysane-2.0-py*.egg-info

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
%{python3_sitearch}/*
# These are in subpackages
%exclude %{python3_sitearch}/*sane*
%exclude %{python3_sitearch}/PIL/_imagingtk*
%exclude %{python3_sitearch}/PIL/ImageTk*
%exclude %{python3_sitearch}/PIL/SpiderImagePlugin*
%exclude %{python3_sitearch}/PIL/ImageQt*

%files -n python3-%{module}-devel
%defattr(644,root,root,755)
%{py3_incdir}/Imaging

%files -n python3-%{module}-doc
%defattr(644,root,root,755)
%doc Scripts
%if %{with doc}
%doc docs/_build/html
%endif

%files -n python3-%{module}-sane
%defattr(644,root,root,755)
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%{python3_sitearch}/*sane*

%files -n python3-%{module}-tk
%defattr(644,root,root,755)
%{python3_sitearch}/PIL/_imagingtk*
%{python3_sitearch}/PIL/ImageTk*
%{python3_sitearch}/PIL/SpiderImagePlugin*

%files -n python3-%{module}-qt
%defattr(644,root,root,755)
%{python3_sitearch}/PIL/ImageQt*
%endif
