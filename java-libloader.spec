#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname	libloader
Summary:	Resource Loading Framework
Name:		java-libloader
Version:	1.1.3
Release:	1
License:	LGPL v2+
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreereport/%{srcname}-%{version}.zip
# Source0-md5:	f124dafb3f8acd1c1fbffa3e346666c4
Patch0:		build.patch
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	java-libbase >= 1.1.3
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-libbase >= 1.1.3
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibLoader is a general purpose resource loading framework. It has been
designed to allow to load resources from any physical location and to
allow the processing of that content data in a generic way, totally
transparent to the user of that library.

%package javadoc
Summary:	Javadoc for LibLoader
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description javadoc
Javadoc for LibLoader.

%prep
%setup -qc
%patch0 -p1
%undos README.txt licence-LGPL.txt ChangeLog.txt

find -name "*.jar" | xargs rm -v

install -d lib
ln -sf %{_javadir}/ant lib/ant-contrib

%build
build-jar-repository -s -p lib libbase commons-logging-api
%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a bin/javadoc/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc README.txt ChangeLog.txt
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
