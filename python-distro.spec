#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-distro.spec)

%define 	module	distro
Summary:	An OS platform information API
Summary(pl.UTF-8):	API do intermacji o platformie systemu operacyjnego
Name:		python-%{module}
# keep 1.6.x here for python2 support
Version:	1.6.0
Release:	4
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/nir0s/distro/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	50fbf6f3f123747a438c2749e9d903eb
URL:		https://github.com/nir0s/distro
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3 >= 1:3.6
BuildRequires:	sphinx-pdg-3 >= 2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
distro provides information about the OS distribution it runs on, such
as a reliable machine-readable ID, or version information.

%description -l pl.UTF-8
distro udostępnia informacje o dystrybucji systemu operacyjnego, na
jakim działa, takie jak wiarygodny, czytelny dla maszyny identyfikator
albo informację o wersji.

%package -n python3-%{module}
Summary:	An OS platform information API
Summary(pl.UTF-8):	API do intermacji o platformie systemu operacyjnego
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
distro provides information about the OS distribution it runs on, such
as a reliable machine-readable ID, or version information.

It is the recommended replacement for Python's original
platform.linux_distribution function removed in Python 3.8.

%description -n python3-%{module} -l pl.UTF-8
distro udostępnia informacje o dystrybucji systemu operacyjnego, na
jakim działa, takie jak wiarygodny, czytelny dla maszyny identyfikator
albo informację o wersji.

Jest to zalecany zamiennik oryginalnej pythonowej funkcji
platform.linux_distribution, usuniętej w Pythonie 3.8.

%package apidocs
Summary:	API documentation for Python distro module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona distro
Group:		Documentation

%description apidocs
API documentation for Python distro module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona distro.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTORS.md LICENSE README.md
%{py_sitescriptdir}/distro.py[co]
%{py_sitescriptdir}/distro-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/distro
%doc CHANGELOG.md CONTRIBUTORS.md LICENSE README.md
%{py3_sitescriptdir}/distro.py
%{py3_sitescriptdir}/__pycache__/distro.cpython-*.py[co]
%{py3_sitescriptdir}/distro-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
