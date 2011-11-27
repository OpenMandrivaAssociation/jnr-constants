Name:           jnr-constants
Version:        0.7
Release:        5
Summary:        Java Native Runtime constants 
Group:          Development/Java
License:        MIT
URL:            http://github.com/wmeissner/jnr-constants/
Source0:        http://download.github.com/wmeissner-jnr-constants-0.7-0-g8b45ca7.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils
Requires:       java >= 0:1.6.0
Requires:       jpackage-utils

%description
Provides java values for common platform C constants (e.g. errno).

%prep
%setup -q -n wmeissner-%{name}-8b45ca7
find ./ -name '*.jar' -exec rm -f '{}' \; 
find ./ -name '*.class' -exec rm -f '{}' \; 

%build
ant jar

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}

# project was renamed from 'constantine' to jnr-constants, but jar has
# yet to be renamed http://fedoraproject.org/wiki/Packaging/Java#Jar_file_naming
cp -p dist/constantine.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{_javadir}/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{_javadir}/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/constantine.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/constantine.jar

