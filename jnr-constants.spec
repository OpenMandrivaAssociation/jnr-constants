%{?_javapackages_macros:%_javapackages_macros}
%global commit_hash 7cb9fc2
%global tag_hash 874071e

Name:           jnr-constants
Version:        0.8.4
Release:        6.3
Summary:        Java Native Runtime constants 
Group:		Development/Java
License:        ASL 2.0
URL:            http://github.com/jnr/%{name}/
Source0:        https://github.com/jnr/%{name}/tarball/%{version}/jnr-%{name}-%{version}-0-g%{commit_hash}.tar.gz
BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit

Requires:       java
Requires:       jpackage-utils

%description
Provides java values for common platform C constants (e.g. errno).

%package javadoc
Summary:        Javadocs for %{name}

Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jnr-%{name}-%{tag_hash}
find ./ -name '*.jar' -delete
find ./ -name '*.class' -delete

%build
%mvn_build

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
# link to older version jarname, so that gradle works
ln -s %{_javadir}/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/constantine.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files -f .mfiles
%doc LICENSE
%{_javadir}/constantine.jar

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.4-2
- Provide a constantine.jar simlink for gradle.

* Tue Feb 05 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.4-1
- Updated to version 0.8.4.
- Switch from ant to maven.

* Tue Oct 09 2012 gil cattaneo <puntogil@libero.it> 0.7-6
- add maven pom
- adapt to current guideline

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 02 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.7-2
- Fixed incorrect Source0 url

* Fri Jan 22 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.7-1
- Unorphaned / updated package

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 6 2008 Conrad Meyer <konrad@tylerc.org> - 0.4-2
- Include LICENSE in rpm.

* Fri Nov 28 2008 Conrad Meyer <konrad@tylerc.org> - 0.4-1
- Include symlink from non-versioned jar to versioned jar.
- Bump to 0.4.

* Fri Nov 28 2008 Conrad Meyer <konrad@tylerc.org> - 0.1-1
- Initial package (needed for jruby 1.1.5).

